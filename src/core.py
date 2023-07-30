import numpy as np
from copy import deepcopy

def divisible(array: np.ndarray, number: int):
    """ Boolean function, checks all array to be divisible by the number """
    return not np.any(array % number > 0)

def averaging(x1: np.ndarray, x0: np.ndarray, y0: np.ndarray):
    """ Returns spectrum brightness values with decreased resolution """
    semistep = (x1[1] - x1[0]) / 2 # most likely semistep = 2.5 nm
    y1 = [np.mean(y0[np.where(x0 < x1[0]+semistep)])]
    for x in x1[1:-1]:
        y = np.mean(y0[np.where((x-semistep < x0) & (x0 < x+semistep))]) # average the brightness around X points
        y1.append(y)
    y1.append(np.mean(y0[np.where(x0 > x1[-1]-semistep)]))
    return np.array(y1)

def custom_interp(y0: np.ndarray, k=8):
    """
    Returns curve values on an uniform grid with twice the resolution.
    Optimal in terms of speed to quality ratio. Invented while trying to sleep.

    Args:
    - y0 (np.ndarray): values to be interpolated
    - k (int): lower -> more chaotic, higher -> more linear, best results around 5-10
    """
    y1 = np.empty(y0.size * 2 - 1)
    y1[0::2] = y0
    delta_left = np.append(0., y0[1:-1] - y0[:-2])
    delta_right = np.append(y0[2:] - y0[1:-1], 0.)
    y1[1::2] = (y0[:-1] + y0[1:] + (delta_left - delta_right) / k) / 2
    return y1

class Spectrum:
    def __init__(self, name: str, nm: np.ndarray, br: np.ndarray):
        """
        Constructor of the class to work with single, continuous spectrum.
        When creating an object, the spectrum grid is automatically checked and adjusted to uniform, if necessary.
        
        Args:
        - name (str): human-readable identification. May include source (separated by "|")
        and additional info (separated by ":")
        - nm (np.array): list of wavelengths in nanometers
        - br (np.array): same-size list of linear physical property, representing "brightness"
        """
        self.name = name

        # --- Checking and creating a uniform grid ---
        steps = nm[1:] - nm[:-1] # =np.diff(nm)
        blocks = set(steps)
        if len(blocks) == 1: # uniform grid
            res = int(*blocks)
            if divisible(nm, res) and res in self._resolutions: # perfect grid
                self.br = br
                self.nm = nm.astype(int)
                self.res = res
                return
        else:
            res = np.mean(steps)
        self.res = self._standardize_resolution(res)
        if nm[0] % self.res == 0:
            start_point = nm[0]
        else:
            start_point = nm[0] + self.res - nm[0] % self.res
        self.nm = np.arange(start_point, nm[-1]+1, self.res, dtype=int) # new grid
        if self.res <= res: # interpolation, increasing resolution
            self.br = np.interp(self.nm, nm, br)
        else: # decreasing resolution if step less than 5 nm
            self.br = averaging(self.nm, nm, br)
    
    _resolutions = [5, 10, 20, 40, 80, 160] # nm

    def _standardize_resolution(self, input: int):
        """ Redirects the step size to one of the valid values """
        res = self._resolutions[-1] # max possible step
        for i in range(1, len(self._resolutions)):
            if input < self._resolutions[i]:
                res = self._resolutions[i-1] # accuracy is always in reserve
                break
        return res
    
    def to_resolution(self, request: int):
        """ Creates new Spectrum object with changed wavelength grid step size """
        other = deepcopy(self)
        if request not in self._resolutions:
            print(f'# Note for the Spectrum object "{self.name}"')
            print(f'- Resolution change allowed only for {self._resolutions} nm, not {request} nm.')
            request = self._standardize_resolution(request)
            print(f'- The optimal resolution was chosen automatically: {request} nm.')
        if request > other.res:
            while request != other.res: # remove all odd elements
                other.res *= 2
                other.nm = np.arange(other.nm[0], other.nm[-1]+1, other.res, dtype=int)
                other.br = other.br[::2]
        elif request < other.res:
            while request != other.res: # middle linear interpolation
                other.res = int(other.res / 2)
                other.nm = np.arange(other.nm[0], other.nm[-1]+1, other.res, dtype=int)
                other.br = custom_interp(other.br)
        else:
            print(f'# Note for the Spectrum object "{self.name}"')
            print(f'- Current and requested resolutions are the same ({request} nm), nothing changed.')
        return other

    def __mul__(self, other):
        """ Implementation of convolution between emission spectrum and transmission spectrum """
        name = f'{self.name} * {other.name}'
        start = max(self.nm[0], other.nm[0])
        end = min(self.nm[-1], other.nm[-1])
        if start > end:
            print(f'# Note for convolution "{name}"')
            print('- Zero will be returned since there is no intersection between the spectra.')
            the_first = self.name
            the_second = other.name
            if self.nm[0] > other.nm[0]:
                the_first, the_second = the_second, the_first
            print(f'- "{the_first}" ends on {end} nm and "{the_second}" starts on {start} nm.')
            return 0.
        else:
            if self.res < other.res:
                other = other.to_resolution(self.res)
            elif self.res > other.res:
                self = self.to_resolution(other.res)
            nm = np.arange(start, end+1, self.res)
            br0 = self.br[np.where((self.nm >= start) & (self.nm <= end))]
            br1 = other.br[np.where((other.nm >= start) & (other.nm <= end))]
            return Spectrum(name, nm, br0*br1).integrate()
    
    def integrate(self):
        """ Calculates the flux over the spectrum after interpolation using the mean rectangle method """
        curve = self.to_resolution(self._resolutions[0])
        midpoints = (curve.br[:-1] + curve.br[1:]) / 2
        area = np.sum(midpoints * curve.res)
        return area # / 1e9 # convert to SI (nm -> m)