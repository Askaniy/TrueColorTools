from scipy.interpolate import Akima1DInterpolator
from typing import TypeVar, Iterable, Tuple
from copy import deepcopy
import traceback
import numpy as np
import src.data_import as di



# This code was written in an effort to work not only with the optical range, but with any, depending on the data.
# But too long and heterogeneous FITS files demanded to set the upper limit of the range to mid-wavelength infrared (3 μm).
nm_limit = 3000 # nm

# For the sake of simplifying work with the spectrum, its discretization steps are strictly given below.
# Grid points are divisible by the selected step.
resolutions = [5, 10, 20, 40, 80, 160] # nm

# To calculate color, it is necessary to achieve a definition of the spectrum in the visible range.
# Boundaries have been defined based on the CMF (color matching functions) used, but can be any.
visible_range = np.arange(390, 780, 5) # nm

# Returned on problems with initialization
nm_br_stub = (np.array([550, 555]), np.zeros(2))



h = 6.626e-34 # Planck constant
c = 299792458 # Speed of light
k = 1.381e-23 # Boltzmann constant
const1 = 2 * np.pi * h * c * c
const2 = h * c / k
r = 6.957e8 # Solar radius, meters
au = 149597870700 # astronomical unit, meters
w = (1 - np.sqrt(1 - (r / au)**2)) / 2 # dilution to compare with Solar light on Earth
temp_coef_to_make_it_work = 1.8 / 0.448 # 1.8 is expected of irradiance(500, 5770), 0.448 is actual. TODO

# Now it does not work as intended: the spectrum should be comparable to the sun_SI
def irradiance(nm: int|float|np.ndarray, T: int|float) -> float|np.ndarray:
    m = nm / 1e9
    return temp_coef_to_make_it_work * w * const1 / (m**5 * (np.exp(const2 / (m * T)) - 1)) / 1e9 # per m -> per nm

def mag2irradiance(m: int|float|np.ndarray, vega_zero_point: float):
    return vega_zero_point * 10**(-0.4 * m)



class Photometry:
    def __init__(self, name: str, dictionary: dict):
        """
        Constructor of the class to work with photometric parameters, imported from the database.

        Supported input dictionary keys:
        - `nm` (list): list of wavelengths in nanometers
        - `br` (list): same-size list of "brightness" of an energy counter detector (not photon counter)
        - `mag` (list): same-size list of magnitudes
        - `nm_range` (list): list of [`start`, `stop`, `step`] integer values with including endpoint
        - `file` (str): path to a FITS file in the `spectra` folder
        - `filters` (list): filter system, linked with [`filters.py`](src/filters.py)
        - `indices` (list): dictionary of color indices, use only with `filters`
        - `bands` (list): list of filters' names, use only with `filters`
        - `albedo` (bool or float, optional):
            - `albedo=True` means that the input brightness is in the [0, 1] range
            - `albedo=False` means that albedo mode is impossible
            - `albedo=`*float* means that brightness after converting to spectrum can be scaled to be in the range
        - `sun` (bool, optional): `True` if spectrum must be divided by the Solar to become reflective
        - `vega` (bool, optional): `True` if spectrum must be divided by the Vegan to become reflective
        - `tags` (list, optional): list of strings, categorizes a spectrum
        """
        self.name = name
        self.file = ''
        self.nm = np.array([])
        self.br = np.array([])
        self.sun = False
        self.vega = False
        self.albedo = False
        try:
            self.nm = np.array(dictionary['nm'])
        except KeyError:
            pass
        try:
            self.br = np.array(dictionary['br'])
        except KeyError:
            pass
        try:
            self.sun = dictionary['sun']
        except KeyError:
            pass
        try:
            self.vega = dictionary['vega']
        except KeyError:
            pass
        try:
            self.albedo = dictionary['albedo']
        except KeyError:
            pass
        try:
            start, stop, step = dictionary['nm_range']
            self.nm = np.arange(start, stop+1, step)
        except KeyError:
            pass
        except ValueError:
            print(f'# Note for the Photometry object "{self.name}"')
            print(f'- Wavelength range issues during object initialization: [start, end, step]={dictionary["nm_range"]}')
        try:
            self.file = dictionary['file']
        except KeyError:
            pass
        try: # TODO: this code needs reworking!
            filters = dictionary['filters']
            if 'bands' in dictionary: # replacement of filters for their wavelengths
                nm = []
                for band in dictionary['bands']:
                    for filter, info in legacy_filters[filters].items():
                        if filter == band.lower():
                            nm.append(info['nm'])
                self.nm = np.array(nm)
            elif 'indices' in dictionary: # spectrum from color indices
                result = {}
                for index, value in dictionary['indices'].items():
                    band1, band2 = index.lower().split('-')
                    if result == {}:
                        result |= {band1: 1.0}
                    if band1 in result:
                        k = legacy_filters[filters][band1]['zp'] - legacy_filters[filters][band2]['zp']
                        result |= {band2: result[band1] * 10**(0.4*(value + k))}
                nm = []
                br = []
                for band, value in result.items():
                    nm.append(legacy_filters[filters][band]['nm'])
                    br.append(value / (legacy_filters[filters][band]['nm']/1e9)**2)
                self.nm = np.array(nm)
                self.br = np.array(br)
        except KeyError:
            pass
        try: # spectrum from magnitudes
            self.br = 10**(-0.4*np.array(dictionary['mag']))
        except KeyError:
            pass
        if self.file == '': # file reading parsed in the Spectrum class. TODO: move magnitudes there too
            if 0 in (self.nm.size, self.br.size):
                print(f'# Note for the Photometry object "{self.name}"')
                print(f'- No wavelengths or brightness data: nm={self.nm}, br={self.br}')
                self.nm, self.br = nm_br_stub
            elif self.nm.size != self.br.size:
                print(f'# Note for the Photometry object "{self.name}"')
                print(f'- The sizes of the wavelengths ({self.nm.size}) and brightness ({self.br.size}) arrays do not match.')
                min_size = min(self.nm.size, self.br.size)
                self.nm = self.nm[:min_size]
                self.br = self.br[:min_size]
                print('- The larger array is reduced to a smaller one.')



def is_divisible(array: np.ndarray, number: int):
    """ Boolean function, checks all array to be divisible by the number """
    return not np.any(array % number > 0)

def is_smooth(br: Iterable):
    """ Boolean function, checks the second derivative for sign reversal, a simple criterion for smoothness """
    diff2 = np.diff(np.diff(br))
    return np.all(diff2 <= 0) | np.all(diff2 >= 0)

def averaging(x0: np.ndarray, y0: np.ndarray, x1: np.ndarray):
    """ Returns spectrum brightness values with decreased resolution """
    semistep = (x1[1] - x1[0]) / 2 # most likely semistep = 2.5 nm
    y1 = [np.mean(y0[np.where(x0 < x1[0]+semistep)])]
    for x in x1[1:-1]:
        flag = np.where((x-semistep < x0) & (x0 < x+semistep))
        if flag[0].size == 0: # the spectrum is no longer dense enough to be averaged down to 5 nm
            y = y1[-1] # lengthening the last recorded brightness as the simplest solution
        else:
            y = np.mean(y0[flag]) # average the brightness around X points
        y1.append(y)
    y1.append(np.mean(y0[np.where(x0 > x1[-1]-semistep)]))
    return np.array(y1)

def custom_interp(y0: np.ndarray, k=8):
    """
    Returns curve values on an uniform grid with twice the resolution. Can be used in a loop.
    Optimal in terms of speed to quality ratio. Invented while trying to sleep.

    Args:
    - `y0` (np.ndarray): values to be interpolated
    - `k` (int): lower -> more chaotic, higher -> more linear, best results around 5-10
    """
    y1 = np.empty(y0.size * 2 - 1)
    y1[0::2] = y0
    delta_left = np.append(0., y0[1:-1] - y0[:-2])
    delta_right = np.append(y0[2:] - y0[1:-1], 0.)
    y1[1::2] = (y0[:-1] + y0[1:] + (delta_left - delta_right) / k) / 2
    return np.clip(y1, 0, None)

def custom_extrap(grid: np.ndarray, derivative: float, corner_x: int|float, corner_y: float) -> np.ndarray:
    """
    Returns an intuitive continuation of the function on the grid using information about the last point.
    Extrapolation bases on function f(x) = exp( (1-x²)/2 ): f' has extrema of ±1 in (-1, 1) and (1, 1).
    Therefore, it scales to complement the spectrum more easily than similar functions.
    """
    if derivative == 0: # extrapolation by constant
        return np.full(grid.size, corner_y)
    else:
        sign = np.sign(derivative)
        return np.exp((1 - (np.abs(derivative) * (grid - corner_x) / corner_y - sign)**2) / 2) * corner_y

weights_center_of_mass = 1 - 1 / np.sqrt(2)

def extrapolating(x: np.ndarray, y: np.ndarray, scope: np.ndarray, step: int, avg_steps=20):
    """
    Defines a curve with an intuitive continuation on the scope, if needed.
    `avg_steps` is a number of corner curve points to be averaged if the curve is not smooth.
    Averaging weights on this range grow linearly closer to the edge (from 0 to 1).
    """
    if x[0] > scope[0]: # extrapolation to blue
        x1 = np.arange(scope[0], x[0], step)
        y_scope = y[:avg_steps]
        if is_smooth(y_scope):
            diff = y[1]-y[0]
            corner_y = y[0]
        else:
            avg_weights = np.abs(np.arange(-avg_steps, 0)) # weights could be more complicated, but there is no need
            diff = np.average(y_scope[1:]-y_scope[:-1], weights=avg_weights[:-1])
            corner_y = np.average(y_scope, weights=avg_weights) - diff * avg_steps * weights_center_of_mass
        y1 = custom_extrap(x1, diff/step, x[0], corner_y)
        x = np.append(x1, x)
        y = np.append(y1, y)
    if x[-1] < scope[-1]: # extrapolation to red
        x1 = np.arange(x[-1], scope[-1], step) + step
        y_scope = y[-avg_steps:]
        if is_smooth(y_scope):
            diff = y[-1]-y[-2]
            corner_y = y[-1]
        else:
            avg_weights = np.arange(avg_steps) + 1
            diff = np.average(y_scope[1:]-y_scope[:-1], weights=avg_weights[1:])
            corner_y = np.average(y_scope, weights=avg_weights) + diff * avg_steps * weights_center_of_mass
        y1 = custom_extrap(x1, diff/step, x[-1], corner_y)
        x = np.append(x, x1)
        y = np.append(y, y1)
    return x, y

def grid(start: int|float, end: int|float, res: int):
    """ Returns grid points in the range that are divisible by the selected step """
    if start % res != 0:
        start += res - start % res
    if end % res == 0:
        end += 1 # to include the last point
    return np.arange(start, end, res, dtype=int)

def standardize_resolution(input: int):
    """ Redirects the step size to one of the valid values """
    res = resolutions[-1] # max possible step
    for i in range(1, len(resolutions)):
        if input < resolutions[i]:
            res = resolutions[i-1] # accuracy is always in reserve
            break
    return res

class Spectrum:
    def __init__(self, name: str, nm: Iterable, br: Iterable, res=0, scope: np.ndarray = None):
        """
        Constructor of the class to work with single, continuous spectrum, with strictly defined resolutions.
        When creating an object, the spectrum grid is automatically checked and adjusted to uniform, if necessary.
        Specifying resolution removes the check. This is only recommended for speeding up code that is definitely trustworthy.
        The idea has been simplified, and the initialization step is only 5 nanometers, but it works with other valid ones.

        Args:
        - `name` (str): human-readable identification. May include source (separated by "|") and info (separated by ":")
        - `nm` (Iterable): list of wavelengths in nanometers
        - `br` (Iterable): same-size list of "brightness" of an energy counter detector (not photon counter)
        - `res` (int, optional): assigns a number, cancel the check
        - `scope` (np.ndarray, optional): makes a spectrum of the same resolution as at least defined at the given wavelengths
        """
        self.name = name
        nm = np.array(nm)
        br = np.array(br)
        try:
            if nm[-1] > nm_limit:
                flag = np.where(nm < nm_limit + resolutions[0]) # to be averaged to nm_limit
                nm = nm[flag]
                br = br[flag]
            if res != 0: # input could be trusted
                self.nm = nm.astype(int)
                self.br = br
                self.res = res
            else:
                self.res = 5 # nm. Initialization simplification by leaving only one default option.
                mean_res = np.mean(nm[1:]-nm[:-1])
                if is_divisible(nm, self.res) and round(mean_res) == self.res:
                    self.nm = nm
                    self.br = br
                else:
                    self.nm = grid(nm[0], nm[-1], self.res)
                    if mean_res >= self.res: # interpolation, increasing resolution
                        self.br = Akima1DInterpolator(nm, br)(self.nm)
                    else: # decreasing resolution if step less than 5 nm
                        self.br = averaging(nm, br, self.nm)
            if isinstance(scope, np.ndarray):
                self.nm, self.br = extrapolating(self.nm, self.br, scope, self.res)
            if np.any(np.isnan(self.br)):
                self.br = np.nan_to_num(self.br)
                print(f'# Note for the Spectrum object "{self.name}"')
                print(f'- NaN values detected during object initialization, they been replaced with zeros.')
        except Exception:
            self.nm, self.br = nm_br_stub
            self.res = 5
            print(f'# Note for the Spectrum object "{self.name}"')
            print(f'- Something unexpected happened during initialization. The spectrum was replaced by a stub.')
            print(f'- More precisely, {traceback.format_exc(limit=0)}')

    @staticmethod
    def from_photometry(data: Photometry, scope: np.ndarray):
        """ Creates a Spectrum object with inter- and extrapolated photometry data to fit the wavelength scope """
        if data.file != '':
            try:
                if data.file.split('.')[-1].lower() in ('fits', 'fit'):
                    nm, br = di.fits_reader('spectra/'+data.file)
                else:
                    nm, br = di.txt_reader('spectra/'+data.file)
            except Exception:
                print(f'# Note for the Spectrum object "{data.name}"')
                print(f'- Something unexpected happened during external file reading. The data was replaced by a stub.')
                print(f'- More precisely, {traceback.format_exc(limit=0)}')
                nm, br = nm_br_stub
        else:
            nm, br = data.nm, data.br
        spectrum = Spectrum(data.name, nm, br, scope=scope)
        if spectrum.br.min() < 0:
            spectrum.br = np.clip(spectrum.br, 0, None)
            print(f'# Note for the Spectrum object "{spectrum.name}"')
            print(f'- Negative values detected during conversion from photometry, they been replaced with zeros.')
        return spectrum

    @staticmethod
    def from_filter(name: str):
        """ Creates a Spectrum object based on the loaded data in Filter Profile Service standard """
        return Spectrum(name, *di.txt_reader(f'filters/{name}.dat'))

    @staticmethod
    def from_CALSPEC(name: str, file: str):
        """ Creates a Spectrum object based on the external CALSPEC FITS file """
        return Spectrum(name, *di.fits_reader(f'spectra/files/CALSPEC/{file}.fits'))

    @staticmethod
    def from_blackbody_redshift(scope: np.ndarray, temperature: int|float, velocity=0., vII=0.):
        """ Creates a Spectrum object based on Planck's law and redshift formulas """
        if temperature == 0:
            physics = False
        else:
            physics = True
            if velocity == 0:
                doppler = 1
            else:
                if abs(velocity) != 1:
                    doppler = np.sqrt((1-velocity) / (1+velocity))
                else:
                    physics = False
            if vII == 0:
                grav = 1
            else:
                if vII != 1:
                    grav = np.exp(-vII*vII/2)
                else:
                    physics = False
        if physics:
            br = irradiance(scope*doppler*grav, temperature)
        else:
            br = np.zeros(scope.size)
        return Spectrum(f'BB with T={int(temperature)}', scope, br)

    def to_resolution(self, request: int):
        """ Returns a new Spectrum object with changed wavelength grid step size """
        other = deepcopy(self)
        if request not in resolutions:
            print(f'# Note for the Spectrum object "{self.name}"')
            print(f'- Resolution change allowed only for {resolutions} nm, not {request} nm.')
            request = standardize_resolution(request)
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

    def __truediv__(self, other):
        """ Returns a new Spectrum object with the emitter removed, i.e. the reflection spectrum """
        divided = deepcopy(self)
        divided.name = f'{divided.name} / {other.name}'
        start = max(divided.nm[0], other.nm[0])
        end = min(divided.nm[-1], other.nm[-1])
        if start >= end:
            print(f'# Note for spectral division "{divided.name}"')
            print('- There is no intersection between the spectra, nothing changed.')
            the_first = self.name
            the_second = other.name
            if divided.nm[0] > other.nm[0]:
                the_first, the_second = the_second, the_first
            print(f'- "{the_first}" ends on {end} nm and "{the_second}" starts on {start} nm.')
        else:
            if divided.res < other.res:
                other = other.to_resolution(divided.res)
            elif divided.res > other.res:
                divided = divided.to_resolution(other.res)
            divided.nm = np.arange(start, end+1, divided.res)
            br0 = divided.br[np.where((divided.nm >= start) & (divided.nm <= end))]
            br1 = other.br[np.where((other.nm >= start) & (other.nm <= end))]
            divided.br = br0 / br1
        return divided

    def integrate(self) -> float:
        """ Calculates the area over the spectrum using the mean rectangle method, per nm """
        curve = self.to_resolution(resolutions[0])
        midpoints = (curve.br[:-1] + curve.br[1:]) / 2
        area = np.sum(midpoints * curve.res)
        return area

    def normalized_by_area(self):
        """ Returns a new Spectrum object with brightness scaled to its area be equal 1 """
        other = deepcopy(self)
        other.br /= other.integrate()
        return other

    def normalized_on_wavelength(self, request: int):
        """ Returns a new Spectrum object with brightness scaled to be equal 1 at the specified wavelength """
        other = deepcopy(self)
        if request not in other.nm:
            print(f'# Note for the Spectrum object "{other.name}"')
            print(f'- Requested wavelength to normalize ({request}) not in the spectrum range ({other.nm[0]} to {other.nm[-1]} by {other.res} nm).')
            request = other.nm[np.abs(other.nm - request).argmin()]
            print(f'- {request} was chosen as the closest value.')
        other.br /= other.br[np.where(other.nm == request)]
        return other

    def scaled_to_albedo(self, albedo: float, transmission):
        """ Returns a new Spectrum object with brightness scaled to give the albedo after convolution with the filter """
        other = deepcopy(self)
        current_albedo = other * transmission.normalized_by_area()
        if current_albedo == 0:
            print(f'# Note for the Spectrum object "{other.name}"')
            print(f'- The spectrum cannot be scaled to an albedo of {albedo} because its current albedo is zero.')
        else:
            other.br *= albedo / current_albedo
        return other

    def mean_wavelength(self) -> float:
        return np.average(self.nm, weights=self.br)



bessell_V = Spectrum.from_filter('Generic_Bessell.V')
bessell_V_norm = bessell_V.normalized_by_area() # used as an averager for the reference spectra

sun_SI = Spectrum.from_CALSPEC('Sun', 'sun_reference_stis_002') # W / (m² nm)
sun_in_V = sun_SI * bessell_V_norm
sun_norm = sun_SI.scaled_to_albedo(1, bessell_V)

vega_SI = Spectrum.from_CALSPEC('Vega', 'alpha_lyr_stis_011') # W / (m² nm)
vega_in_V = vega_SI * bessell_V_norm
vega_norm = vega_SI.scaled_to_albedo(1, bessell_V)



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
r = Spectrum('r CMF', *np.loadtxt('src/cmf/StilesBurch10deg.r.dat').transpose(), res=5).normalized_by_area()
g = Spectrum('g CMF', *np.loadtxt('src/cmf/StilesBurch10deg.g.dat').transpose(), res=5).normalized_by_area()
b = Spectrum('b CMF', *np.loadtxt('src/cmf/StilesBurch10deg.b.dat').transpose(), res=5).normalized_by_area()

# CIE XYZ functions transformed from the CIE (2006) LMS functions, 10-deg
# http://www.cvrl.org/ciexyzpr.htm
# Sensitivity modulo values less than 10^-4 were previously removed
x = Spectrum('x CMF', *np.loadtxt('src/cmf/cie10deg.x.dat').transpose(), res=5)
y = Spectrum('y CMF', *np.loadtxt('src/cmf/cie10deg.y.dat').transpose(), res=5)
z = Spectrum('z CMF', *np.loadtxt('src/cmf/cie10deg.z.dat').transpose(), res=5)
# Normalization. TODO: find an official way to calibrate brightness for albedo!
# 355.5 was guessed so that the brightness was approximately the same as that of the legacy version
x.br /= 355.5
y.br /= 355.5
z.br /= 355.5



gamma_correction = np.vectorize(lambda p: p * 12.92 if p < 0.0031308 else 1.055 * p**(1.0/2.4) - 0.055)

class Color:
    def __init__(self, name: str, rgb: Iterable, albedo=False):
        """
        Constructor of the class to work with color represented by three float values in [0, 1] range.
        The albedo flag on means that you have already normalized the brightness over the range.
        By default, initialization implies normalization and you get chromaticity.

        Args:
        - `name` (str): human-readable identification. May include source (separated by "|") and info (separated by ":")
        - `rgb` (Iterable): array of three values that are red, green and blue
        - `albedo` (bool): flag to disable normalization
        """
        self.name = name
        rgb = np.array(rgb, dtype=float)
        if rgb.min() < 0:
            #print(f'# Note for the Color object "{self.name}"')
            #print(f'- Negative values detected during object initialization: rgb={rgb}')
            rgb = np.clip(rgb, 0, None)
            #print('- These values have been replaced with zeros.')
        if rgb.max() != 0 and not albedo: # normalization
            rgb /= rgb.max()
        if np.any(np.isnan(rgb)):
            print(f'# Note for the Color object "{self.name}"')
            print(f'- NaN values detected during object initialization: rgb={rgb}')
            rgb = np.array([0., 0., 0.])
            print(f'- It has been replaced with {rgb}.')
        self.rgb = rgb

    @staticmethod
    def from_spectrum_legacy(spectrum: Spectrum, albedo=False):
        """ A simple and concrete color processing method based on experimental eye sensitivity curves """
        rgb = [spectrum * i for i in (r, g, b)] # convolution
        return Color(spectrum.name, rgb, albedo)

    @staticmethod
    def from_spectrum(spectrum: Spectrum, albedo=False, color_system=srgb):
        """ Conventional color processing method: spectrum -> CIE XYZ -> sRGB with illuminant E """
        xyz = [spectrum * i for i in (x, y, z)] # convolution
        rgb = color_system.T.dot(xyz)
        if np.any(rgb < 0):
            print(f'# Note for the Color object "{spectrum.name}"')
            print(f'- RGB derived from XYZ turned out to be outside the color space: rgb={rgb}')
            rgb -= rgb.min()
            print(f'- Approximating by desaturating: rgb={rgb}')
        return Color(spectrum.name, rgb, albedo)

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
            #print(f'# Note for the Color object "{self.name}"')
            #print(f'- HTML-style color code feels wrong: {html}')
            html = '#FFFFFF'
            #print(f'- It has been replaced with {html}.')
        return html



# Pivot wavelengths and ZeroPoints of filter bandpasses. Legacy!
# https://www.stsci.edu/~INS/2010CalWorkshop/pickles.pdf

# HST https://www.stsci.edu/~WFC3/PhotometricCalibration/ZP_calculating_wfc3.html
# https://www.stsci.edu/files/live/sites/www/files/home/hst/instrumentation/legacy/nicmos/_documents/nicmos_ihb_v10_cy17.pdf

legacy_filters = {
    'Tycho': {
        'b': {'nm': 419.6, 'zp': -0.108},
        'v': {'nm': 530.5, 'zp': -0.030}
    },
    'Landolt': {
        'u': {'nm': 354.6, 'zp': 0.761},
        'b': {'nm': 432.6, 'zp': -0.103},
        'v': {'nm': 544.5, 'zp': -0.014},
        'r': {'nm': 652.9, 'zp': 0.154},
        'i': {'nm': 810.4, 'zp': 0.405}
    },
    'UBVRI': {
        'u': {'nm': 358.9, 'zp': 0.763},
        'b': {'nm': 437.2, 'zp': -0.116},
        'v': {'nm': 549.3, 'zp': -0.014},
        'r': {'nm': 652.7, 'zp': 0.165},
        'i': {'nm': 789.1, 'zp': 0.368}
    },
    'Stromgren': {
        'us': {'nm': 346.1, 'zp': -0.290},
        'vs': {'nm': 410.7, 'zp': -0.316},
        'bs': {'nm': 467.0, 'zp': -0.181},
        'ys': {'nm': 547.6, 'zp': -0.041}
    },
    'Sloan Air': {
        "u'": {'nm': 355.2, 'zp': -0.033},
        "g'": {'nm': 476.6, 'zp': -0.009},
        "r'": {'nm': 622.6, 'zp': 0.004},
        "i'": {'nm': 759.8, 'zp': 0.008},
        "z'": {'nm': 890.6, 'zp': 0.009}
    },
    'Sloan Vacuum': {
        'u': {'nm': 355.7, 'zp': -0.034},
        'g': {'nm': 470.3, 'zp': -0.002},
        'r': {'nm': 617.6, 'zp': 0.003},
        'i': {'nm': 749.0, 'zp': 0.011},
        'z': {'nm': 889.2, 'zp': 0.007}
    },
    'New Horizons': { # New Horizons SOC to Instrument Pipeline ICD, p.76
        'pan1': {'nm': 651},
        'pan2': {'nm': 651},
        'blue': {'nm': 488},
        'red': {'nm': 612},
        'nir': {'nm': 850},
        'ch4': {'nm': 886}
    },
    'Hubble': {
        'f200lp': {'nm': 197.19, 'zp': 26.931},
        'f218w': {'nm': 222.8, 'zp': 21.278},
        'f225w': {'nm': 237.21, 'zp': 22.43},
        'f275w': {'nm': 270.97, 'zp': 22.677},
        'f280n': {'nm': 283.29, 'zp': 19.516},
        'f300x': {'nm': 282.05, 'zp': 23.565},
        'f336w': {'nm': 335.45, 'zp': 23.527},
        'f343n': {'nm': 343.52, 'zp': 22.754},
        'f350lp': {'nm': 587.39, 'zp': 26.81},
        'f373n': {'nm': 373.02, 'zp': 21.036},
        'f390m': {'nm': 389.72, 'zp': 23.545},
        'f390w': {'nm': 392.37, 'zp': 25.174},
        'f395n': {'nm': 395.52, 'zp': 22.712},
        'f410m': {'nm': 410.9, 'zp': 23.771},
        'f438w': {'nm': 432.62, 'zp': 25.003},
        'f467m': {'nm': 468.26, 'zp': 23.859},
        'f469n': {'nm': 468.81, 'zp': 21.981},
        'f475w': {'nm': 477.31, 'zp': 25.81},
        'f475x': {'nm': 494.07, 'zp': 26.216},
        'f487n': {'nm': 487.14, 'zp': 22.05},
        'f502n': {'nm': 500.96, 'zp': 22.421},
        'f547m': {'nm': 544.75, 'zp': 24.761},
        'f555w': {'nm': 530.84, 'zp': 25.841},
        'f600lp': {'nm': 746.81, 'zp': 25.554},
        'f606w': {'nm': 588.92, 'zp': 26.006},
        'f621m': {'nm': 621.89, 'zp': 24.465},
        'f625w': {'nm': 624.26, 'zp': 25.379},
        'f631n': {'nm': 630.43, 'zp': 21.723},
        'f645n': {'nm': 645.36, 'zp': 22.049},
        'f656n': {'nm': 656.14, 'zp': 19.868},
        'f657n': {'nm': 656.66, 'zp': 22.333},
        'f658n': {'nm': 658.4, 'zp': 20.672},
        'f665n': {'nm': 665.59, 'zp': 22.492},
        'f673n': {'nm': 676.59, 'zp': 22.343},
        'f680n': {'nm': 687.76, 'zp': 23.556},
        'f689m': {'nm': 687.68, 'zp': 24.196},
        'f763m': {'nm': 761.44, 'zp': 23.837},
        'f775w': {'nm': 765.14, 'zp': 24.48},
        'f814w': {'nm': 803.91, 'zp': 24.698},
        'f845m': {'nm': 843.91, 'zp': 23.316},
        'f850lp': {'nm': 917.61, 'zp': 23.326},
        'f953n': {'nm': 953.06, 'zp': 19.803},
        'f090m': {'nm': 900, 'zp': 0},
        'f110w': {'nm': 1100, 'zp': 0},
        'f110m': {'nm': 1100, 'zp': 0},
        'f140w': {'nm': 1400, 'zp': 0},
        'f145m': {'nm': 1450, 'zp': 0},
        'f150w': {'nm': 1500, 'zp': 0},
        'f160w': {'nm': 1600, 'zp': 0},
        'f165m': {'nm': 1700, 'zp': 0},
        'f170m': {'nm': 1700, 'zp': 0},
        'f171m': {'nm': 1715, 'zp': 0},
        'f175w': {'nm': 1750, 'zp': 0},
        'f180m': {'nm': 1800, 'zp': 0},
        'f187w': {'nm': 1875, 'zp': 0},
        'f204m': {'nm': 2040, 'zp': 0},
        'f205w': {'nm': 1900, 'zp': 0},
        'f207m': {'nm': 2100, 'zp': 0},
        'f222m': {'nm': 2300, 'zp': 0},
        'f237m': {'nm': 2375, 'zp': 0},
        'f240m': {'nm': 2400, 'zp': 0}
    }
}
