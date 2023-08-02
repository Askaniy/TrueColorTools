import numpy as np
from scipy.interpolate import Akima1DInterpolator
from typing import TypeVar, Iterable, Tuple
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
    def __init__(self, name: str, nm: Iterable, br: np.ndarray, res=0):
        """
        Constructor of the class to work with single, continuous spectrum, with strictly defined resolutions.
        When creating an object, the spectrum grid is automatically checked and adjusted to uniform, if necessary.
        Specifying resolution removes checks. This is only recommended for speeding up code that is definitely trustworthy.
        
        Args:
        - name (str): human-readable identification. May include source (separated by "|") and info (separated by ":")
        - nm (np.array): list of wavelengths in nanometers
        - br (np.array): same-size list of linear physical property, representing "brightness"
        - res (int, optional): 
        """
        self.name = name
        nm = np.array(nm, dtype=int)
        if res == 0: # checking and creating a uniform grid if necessary
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
                self.br = Akima1DInterpolator(nm, br)(self.nm)
            else: # decreasing resolution if step less than 5 nm
                self.br = averaging(self.nm, nm, br)
        else: # input could be trusted
            self.nm = nm
            self.br = br
            self.res = res
    
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
        """ Creates a new Spectrum object with changed wavelength grid step size """
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
        #else:
        #    print(f'# Note for the Spectrum object "{self.name}"')
        #    print(f'- Current and requested resolutions are the same ({request} nm), nothing changed.')
        return other

    def __mul__(self, other):
        """ Implementation of convolution between emission spectrum and transmission spectrum """
        name = f'{self.name} * {other.name}'
        start = max(self.nm[0], other.nm[0])
        end = min(self.nm[-1], other.nm[-1])
        if start >= end:
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
            return Spectrum(name, nm, br0*br1, res=self.res).integrate()

    def integrate(self) -> float:
        """ Calculates the area over the spectrum using the mean rectangle method. Divide by 1e9 to use as a SI flux. """
        curve = self.to_resolution(self._resolutions[0])
        midpoints = (curve.br[:-1] + curve.br[1:]) / 2
        area = np.sum(midpoints * curve.res)
        return area



def xy2xyz(xy):
    return np.array((xy[0], xy[1], 1-xy[0]-xy[0])) # (x, y, 1-x-y)

class ColorSystem:
    def __init__(self, red: Iterable, green: Iterable, blue: Iterable, white: Iterable):
        """
        Initialise the ColorSystem object.
        The implementation is based on https://scipython.com/blog/converting-a-spectrum-to-a-colour/

        Defining the color system requires four 2d vectors (primary illuminants and the "white point")
        """
        self.red, self.green, self.blue, self.white = map(xy2xyz, [red, green, blue, white]) # chromaticities
        self.M = np.vstack((self.red, self.green, self.blue)).T # the chromaticity matrix (rgb -> xyz) and its inverse
        self.MI = np.linalg.inv(self.M) # white scaling array
        self.wscale = self.MI.dot(self.white) # xyz -> rgb transformation matrix
        self.T = self.MI / self.wscale[:, np.newaxis]



# Used white points
illuminant_E = (0.33333, 0.33333)
#illuminant_D65 = (0.3127, 0.3291)

# Used color systems
srgb = ColorSystem((0.64, 0.33), (0.30, 0.60), (0.15, 0.06), illuminant_E)
#hdtv = ColorSystem((0.67, 0.33), (0.21, 0.71), (0.15, 0.06), illuminant_D65)
#smpte = ColorSystem((0.63, 0.34), (0.31, 0.595), (0.155, 0.070), illuminant_D65)

# Stiles & Burch (1959) 10-deg color matching data, direct experimental data
# http://www.cvrl.org/stilesburch10_ind.htm
# Sensitivity modulo values less than 10^-4 were previously removed
r = Spectrum('r', *np.loadtxt('cmf/StilesBurch10deg.r.dat').transpose(), res=5)
g = Spectrum('g', *np.loadtxt('cmf/StilesBurch10deg.g.dat').transpose(), res=5)
b = Spectrum('b', *np.loadtxt('cmf/StilesBurch10deg.b.dat').transpose(), res=5)
# Normalization (integral of each one to be 1)
r.br /= r.integrate()
g.br /= g.integrate()
b.br /= b.integrate()

# The CIE color matching function for 380-780 nm in 5 nm intervals
# https://scipython.com/static/media/blog/colours/cie-cmf.txt
x = Spectrum('x', *np.loadtxt('cmf/cie-cmf.x.dat').transpose(), res=5)
y = Spectrum('y', *np.loadtxt('cmf/cie-cmf.y.dat').transpose(), res=5)
z = Spectrum('z', *np.loadtxt('cmf/cie-cmf.z.dat').transpose(), res=5)
# Normalization (255 was guessed, result seems to be brighter than necessary, to check later)
x.br /= 255
y.br /= 255
z.br /= 255



gamma_correction = np.vectorize(lambda p: p * 12.92 if p < 0.0031308 else 1.055 * p**(1.0/2.4) - 0.055)

class Color:
    def __init__(self, name: str, rgb: Iterable, albedo=False):
        """
        Constructor of the class to work with color represented by three float values in [0, 1] range.
        The albedo flag on means that you have already normalized the brightness over the range.
        By default, initialization implies normalization and you get chromaticity.
        
        Args:
        - name (str): human-readable identification. May include source (separated by "|") and info (separated by ":")
        - rgb (Iterable): array of three values that are red, green and blue
        - albedo (bool): flag to disable normalization
        """
        self.name = name
        rgb = np.array(rgb, dtype=float)
        if rgb.min() < 0:
            print(f'# Note for the Color object "{self.name}"')
            print(f'- Negative values detected during object initialization: rgb={rgb}')
            rgb = np.clip(rgb, 0, None)
            print('- These values have been replaced with zeros.')
        rgb_max = rgb.max()
        if rgb_max == 0:
            print(f'# Note for the Color object "{self.name}"')
            print(f'- All values are zero: rgb={rgb}')
        else:
            if rgb_max > 1 and albedo:
                albedo = False
                print(f'# Note for the Color object "{self.name}"')
                print(f'- Values greater than 1 detected in the albedo mode: rgb={rgb}')
                print('- Not recommended. The processing mode has been switched to chromaticity.')
            if not albedo: # normalization
                rgb /= rgb_max
        self.rgb = rgb

    def from_spectrum_legacy(spectrum: Spectrum, albedo=False):
        """ A simple and concrete color processing method based on experimental eye sensitivity curves """
        rgb = [spectrum * i for i in (r, g, b)] # convolution
        return Color(spectrum.name, rgb, albedo)

    def from_spectrum(spectrum: Spectrum, albedo=False, color_system=srgb):
        """ Conventional color processing method: spectrum -> CIE XYZ -> sRGB with illuminant E """
        name = spectrum.name
        xyz = [spectrum * i for i in (x, y, z)] # convolution
        rgb = color_system.T.dot(xyz)
        if np.any(rgb < 0):
            print(f'# Note for the Color object "{name}"')
            print(f'- RGB derived from XYZ turned out to be outside the color space: rgb={rgb}')
            rgb -= rgb.min()
            print(f'- Approximating by desaturating: rgb={rgb}')
        return Color(name, rgb, albedo)

    def gamma_corrected(self):
        """ Creates a new Color object with applied gamma correction """
        other = deepcopy(self)
        other.rgb = gamma_correction(other.rgb)
        return other

    def to_bit(self, bit: int) -> np.ndarray:
        """ Returns rounded color array, scaled to the appropriate power of two """
        return self.rgb * (2**bit - 1)

    def to_html(self):
        """ Converts fractional rgb values to HTML-style hex string """
        html = '#{:02x}{:02x}{:02x}'.format(*self.to_bit(8).round().astype(int))
        if len(html) != 7:
            print(f'# Note for the Color object "{self.name}"')
            print(f'- HTML-style color code feels wrong: {html}')
            html = '#000000'
            print(f'- It has been replaced with {html}.')
        return html