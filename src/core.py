import numpy as np
from copy import deepcopy

def divisible(array: np.ndarray, number: int):
    """ Boolean function, checks all array to be divisible by the number """
    return not np.any(array % number > 0)

def averaging(x1: np.ndarray, x0: np.ndarray, y0: np.ndarray):
    """ Returns brightness values of spectrum with decreased resolution """
    semistep = (x1[1] - x1[0]) / 2 # most likely semistep = 2.5 nm
    y1 = [np.mean(y0[np.where(x0 < x1[0]+semistep)])]
    for x in x1[1:-1]:
        y = np.mean(y0[np.where((x-semistep < x0) & (x0 < x+semistep))]) # average the brightness around X points
        y1.append(y)
    y1.append(np.mean(y0[np.where(x0 > x1[-1]-semistep)]))
    return np.array(y1)


class Spectrum:
    def __init__(self, name: str, nm: np.ndarray, br: np.ndarray, to_res=-1):
        """
        Constructor of the class to work with single, continuous spectrum.
        When creating an object, the spectrum grid is automatically checked and adjusted to uniform, if necessary.
        
        Args:
        - name (str): human-readable identification. May include source (separated by "|")
        and additional info (separated by ":")
        - nm (np.array): list of wavelengths in nanometers
        - br (np.array): same-size list of linear physical property, representing "brightness"
        - to_res (int, optional): spectrum resolution in nanometers, checks are canceled
        """
        self.name = name

        # --- Checking and creating a uniform grid ---
        if to_res == -1:
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
        else:
            res = to_res # force setting
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
    
    _resolutions = [5, 10, 20, 40] # nm

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
            # TODO: make it Error
            print(f'Invalid operation: resolution change allowed only for {self._resolutions}, not {request} nm.')
        elif request == self.res:
            print(f'Note: current and requested resolutions are the same ({request} nm), nothing changed.')
        else:
            if request > other.res:
                while request != other.res: # remove all odd elements
                    other.res *= 2
                    other.nm = np.arange(self.nm[0], self.nm[-1]+1, other.res, dtype=int)
                    other.br = self.br[::2]
            else:
                while request != other.res: # middle linear interpolation
                    new_br = np.empty(self.br.size * 2 - 1)
                    new_br[0::2] = self.br
                    new_br[1::2] = (self.br[:-1] + self.br[1:]) / 2
                    other.res = int(other.res / 2)
                    other.nm = np.arange(self.nm[0], self.nm[-1]+1, other.res, dtype=int)
                    other.br = new_br
        return other
    
    def integrate(self):
        """ Calculates the flux over the spectrum using the mean rectangle method """
        midpoints = (self.br[:-1] + self.br[1:]) / 2
        area = np.sum(midpoints * self.res)
        return area # / 1e9 # convert to SI (nm -> m)