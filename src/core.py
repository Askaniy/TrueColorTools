from typing import TypeVar, Iterable, Tuple
from copy import deepcopy
from traceback import format_exc
import numpy as np
import src.data_import as di


# This code was written in an effort to work not only with the optical range, but with any, depending on the data.
# But too long and heterogeneous FITS files demanded to set the upper limit of the range to mid-wavelength infrared (3 μm).
nm_red_limit = 3000 # nm
# Actually, dtype=uint16 is used to store wavelength. It's possible to set the limit to 65535 nm with no compression,
# and to 327 675 nm with 5 nm compression.

# For the sake of simplifying work with the spectrum, its discretization step in only 5 nm.
resolution = 5 # nm

# To calculate color, it is necessary to achieve a definition of the spectrum in the visible range.
# Boundaries have been defined based on the CMF (color matching functions) used, but can be any.
visible_range = np.arange(390, 780, 5) # nm

# Returned on problems with initialization
spectrum_stub = (np.array([555]), np.zeros(1), None)
photometry_stub = (['Generic_Bessell.V'], [0], None)



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



def is_smooth(br: Iterable):
    """ Boolean function, checks the second derivative for sign reversal, a simple criterion for smoothness """
    diff2 = np.diff(np.diff(br))
    return np.all(diff2 <= 0) | np.all(diff2 >= 0)

def averaging(x0: np.ndarray, y0: np.ndarray, x1: np.ndarray, step: int|float):
    """ Returns spectrum brightness values with decreased resolution """
    semistep = step * 0.5
    y1 = [np.mean(y0[np.where(x0 < x1[0]+semistep)])]
    for x in x1[1:-1]:
        flag = np.where((x-semistep < x0) & (x0 < x+semistep))
        if flag[0].size == 0: # the spectrum is no longer dense enough to be averaged down to 5 nm
            y = y1[-1] # lengthening the last recorded brightness is the simplest solution
        else:
            y = np.mean(y0[flag]) # average the brightness around X points
        y1.append(y)
    y1.append(np.mean(y0[np.where(x0 > x1[-1]-semistep)]))
    return np.array(y1)

def custom_interp(xy0: np.ndarray, k=16):
    """
    Returns curve values with twice the resolution. Can be used in a loop.
    Optimal in terms of speed to quality ratio: around 2 times faster than splines in scipy.

    Args:
    - `xy0` (np.ndarray): values to be interpolated in shape (2, N)
    - `k` (int): lower -> more chaotic, higher -> more linear, best results around 10-20
    """
    xy1 = np.empty((2, xy0.shape[1]*2-1), dtype=xy0.dtype)
    xy1[:,0::2] = xy0
    xy1[:,1::2] = (xy0[:,:-1] + xy0[:,1:]) * 0.5
    delta_left = np.append(0., xy0[1,1:-1] - xy0[1,:-2])
    delta_right = np.append(xy0[1,2:] - xy0[1,1:-1], 0.)
    xy1[1,1::2] += (delta_left - delta_right) / k
    return xy1

def interpolating(x0: np.ndarray, y0: np.ndarray, x1: np.ndarray, step: int|float) -> np.ndarray:
    """
    Returns interpolated brightness values on uniform grid.
    Combination of custom_interp (which returns an uneven mesh) and linear interpolation after it.
    The chaotic-linearity parameter increases with each iteration to reduce the disadvantages of custom_interp.
    """
    xy0 = np.array([x0, y0])
    for i in range(int(np.log2(np.diff(x0).max() / step))):
        xy0 = custom_interp(xy0, k=11+i)
    return np.interp(x1, xy0[0], xy0[1])

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

def extrapolating(x: np.ndarray, y: np.ndarray, scope: np.ndarray, step: int|float, avg_steps=20):
    """
    Defines a curve with an intuitive continuation on the scope, if needed.
    `avg_steps` is a number of corner curve points to be averaged if the curve is not smooth.
    Averaging weights on this range grow linearly closer to the edge (from 0 to 1).
    """
    if len(x) == 1: # filling with equal-energy spectrum
        x = np.arange(min(scope[0], x[0]), max(scope[-1], x[0])+1, step, dtype='uint16')
        y = np.full_like(x, y[0], dtype='float')
    else:
        if x[0] > scope[0]: # extrapolation to blue
            x1 = np.arange(scope[0], x[0], step)
            y_scope = y[:avg_steps]
            if is_smooth(y_scope):
                diff = y[1]-y[0]
                corner_y = y[0]
            else:
                avg_weights = np.abs(np.arange(-avg_steps, 0)[avg_steps-y_scope.size:]) # weights could be more complicated, but there is no need
                diff = np.average(np.diff(y_scope), weights=avg_weights[:-1])
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
                avg_weights = np.arange(avg_steps)[:y_scope.size] + 1
                diff = np.average(np.diff(y_scope), weights=avg_weights[1:])
                corner_y = np.average(y_scope, weights=avg_weights) + diff * avg_steps * weights_center_of_mass
            y1 = custom_extrap(x1, diff/step, x[-1], corner_y)
            x = np.append(x, x1)
            y = np.append(y, y1)
    return x, y

def grid(start: int|float, end: int|float, res: int):
    """ Returns uniform grid points for the non-integer range that are divisible by the selected step """
    if (shift := start % res) != 0:
        start += res - shift
    if end % res == 0:
        end += 1 # to include the last point
    return np.arange(start, end, res, dtype='uint16')


class Spectrum:
    """ Class to work with single, continuous spectrum, with strictly defined resolution step. """

    def __init__(self, name: str, nm: Iterable, br: Iterable, sd: Iterable = None, photometry=None):
        """
        It is assumed that the input grid can be trusted. If preprocessing is needed, see `Spectrum.from_array`.

        Args:
        - `name` (str): human-readable identification. May include source (separated by "|") and notes (separated by ":")
        - `nm` (Iterable): list of wavelengths in nanometers with resolution step of 5 nm
        - `br` (Iterable): same-size list of "brightness", flux in units of energy (not a photon counter)
        - `sd` (Iterable, optional): same-size list of standard deviations
        - `photometry` (Photometry, optional): way to store original information, for example, to plot it
        """
        self.name = name
        self.nm = np.array(nm, dtype='uint16')
        self.br = np.array(br, dtype='float')
        if sd is not None:
            self.sd = np.array(sd, dtype='float')
        else:
            self.sd = None
        self.photometry = photometry
        if np.any(np.isnan(self.br)):
            self.br = np.nan_to_num(self.br)
            print(f'# Note for the Spectrum object "{self.name}"')
            print(f'- NaN values detected during object initialization, they been replaced with zeros.')
        # There are no checks for negativity, since such spectra exist, for example, red CMF.

    @staticmethod
    def from_array(name: str, nm: Iterable, br: Iterable, sd: Iterable = None):
        """
        Creates a Spectrum object from wavelength array with a check for uniformity and possible extrapolation.

        Args:
        - `name` (str): human-readable identification. May include source (separated by "|") and notes (separated by ":")
        - `nm` (Iterable): list of wavelengths, any grid
        - `br` (Iterable): same-size list of "brightness", flux in units of energy (not a photon counter)
        - `sd` (Iterable): same-size list of standard deviations
        """
        if (len_nm := len(nm)) != (len_br := len(br)):
            print(f'# Note for the Spectrum object "{name}"')
            print(f'- Arrays of wavelengths and brightness do not match ({len_nm} vs {len_br}). Spectrum stub object was created.')
            return Spectrum(name, *spectrum_stub)
        if sd is not None and (len_sd := len(sd)) != len_br:
            print(f'# Note for the Spectrum object "{name}"')
            print(f'- Array of standard deviations do not match brightness array ({len_sd} vs {len_br}). Uncertainty was erased.')
            sd = None
        try:
            nm = np.array(nm) # numpy decides int or float
            br = np.array(br, dtype='float')
            if sd is not None:
                sd = np.array(sd, dtype='float')
            if nm[-1] > nm_red_limit:
                flag = np.where(nm < nm_red_limit + resolution) # with reserve to be averaged
                nm = nm[flag]
                br = br[flag]
                if sd is not None:
                    sd = sd[flag]
            if np.any((diff := np.diff(nm)) != resolution): # if not uniform 5 nm grid
                sd = None # standard deviations is undefined then. TODO: process somehow
                uniform_nm = grid(nm[0], nm[-1], resolution)
                if diff.mean() >= resolution: # interpolation, increasing resolution
                    br = interpolating(nm, br, uniform_nm, resolution)
                else: # decreasing resolution if step less than 5 nm
                    br = averaging(nm, br, uniform_nm, resolution)
                nm = uniform_nm
            if br.min() < 0:
                br = np.clip(br, 0, None)
                #print(f'# Note for the Spectrum object "{name}"')
                #print(f'- Negative values detected while trying to create the object from array, they been replaced with zeros.')
        except Exception:
            nm, br, sd = spectrum_stub
            print(f'# Note for the Spectrum object "{name}"')
            print(f'- Something unexpected happened while trying to create the object from array. It was replaced by a stub.')
            print(f'- More precisely, {format_exc(limit=0)}')
        return Spectrum(name, nm, br, sd)
    
    @staticmethod
    def from_file(name: str, file: str):
        """ Creates a Spectrum object based on loaded data from the specified file """
        nm, br, sd = di.file_reader(file)
        return Spectrum.from_array(name, nm, br, sd)

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
        return Spectrum(f'BB with T={round(temperature)}', scope, br)
    
    def to_scope(self, scope: np.ndarray):
        """ Returns a new Spectrum object with a guarantee of definition on the requested scope """
        if self.photometry is None:
            return Spectrum(self.name, *extrapolating(self.nm, self.br, scope, resolution))
        else:
            return self.photometry.to_scope(scope)

    def integrate(self) -> float:
        """ Calculates the area over the spectrum using the mean rectangle method, per nm """
        return np.sum(resolution * (self.br[:-1] + self.br[1:]) / 2)

    def scaled_by_area(self, factor: int|float = 1):
        """ Returns a new Spectrum object with brightness scaled to its area be equal the scale factor """
        return Spectrum(self.name, self.nm, self.br / self.integrate() * factor)

    def scaled_on_wavelength(self, wavelength: int|float, request: int|float = 1):
        """ Returns a new Spectrum object with brightness scaled to be equal the request at the specified wavelength """
        if wavelength not in self.nm:
            print(f'# Note for the Spectrum object "{self.name}"')
            print(f'- Requested wavelength to normalize ({wavelength}) not in the spectrum range ({self.nm[0]} to {self.nm[-1]} by {resolution} nm).')
            wavelength = self.nm[np.abs(self.nm - wavelength).argmin()]
            print(f'- {wavelength} was chosen as the closest value.')
        scale_factor = request / self.br[np.where(self.nm == wavelength)]
        sd = None
        if self.sd is not None:
            sd = self.sd * scale_factor
        photometry = None
        if self.photometry is not None:
            photometry = self.photometry
            photometry.br *= scale_factor
            if photometry.sd is not None:
                photometry.sd *= scale_factor
        return Spectrum(self.name, self.nm, self.br*scale_factor, sd, photometry)

    def scaled_to_albedo(self, albedo: float, transmission):
        """ Returns a new Spectrum object with brightness scaled to give the albedo after convolution with the filter """
        current_albedo = self ** transmission
        if current_albedo == 0:
            print(f'# Note for the Spectrum object "{self.name}"')
            print(f'- The spectrum cannot be scaled to an albedo of {albedo} because its current albedo is zero, nothing changed.')
            return self
        else:
            scale_factor = albedo / current_albedo
            sd = None
            if self.sd is not None:
                sd = self.sd * scale_factor
            photometry = None
            if self.photometry is not None:
                photometry = self.photometry
                photometry.br *= scale_factor
                if photometry.sd is not None:
                    photometry.sd *= scale_factor
            return Spectrum(self.name, self.nm, self.br*scale_factor, sd, photometry)
    
    def scaled(self, where: str|int|float, how: int|float, sd: int|float = None):
        """ Returns a new Spectrum object to fit the request of wavelength zone and brightness there """
        if isinstance(where, str):
            return self.scaled_to_albedo(how, get_filter(where))
        else: # assuming number
            return self.scaled_on_wavelength(where, how)

    def mean_wavelength(self) -> float:
        """ Returns mean wavelength of the spectrum """
        try:
            return np.average(self.nm, weights=self.br)
        except ZeroDivisionError:
            print(f'# Note for the Spectrum object "{self.name}"')
            print(f'- Bolometric brightness is zero, the mean wavelength cannot be calculated. Returns 0 nm.')
            return 0.

    def standard_deviation(self) -> float:
        """ Returns uncorrected standard deviation of the spectrum """
        return np.sqrt(np.average((self.nm - self.mean_wavelength())**2, weights=self.br))

    def __pow__(self, other) -> float:
        """ Implementation of convolution between emission spectrum and transmission spectrum """
        return (self * other).integrate()

    def __mul__(self, other):
        """ Returns a new Photometry object with the emitter added (untied from a white standard spectrum) """
        name = f'{self.name} ∙ {other.name}'
        start = max(self.nm[0], other.nm[0])
        end = min(self.nm[-1], other.nm[-1])
        if start >= end:
            print(f'# Note for spectral multiplication "{name}"')
            print('- There is no intersection between the spectra, nothing changed.') # TODO: extrapolate, if it ends not about zero
            the_first = self.name
            the_second = other.name
            if self.nm[0] > other.nm[0]:
                the_first, the_second = the_second, the_first
            print(f'- "{the_first}" ends on {end} nm and "{the_second}" starts on {start} nm.')
            return self
        else:
            nm = np.arange(start, end+1, resolution, dtype='uint16')
            br0 = self.br[np.where((self.nm >= start) & (self.nm <= end))]
            br1 = other.br[np.where((other.nm >= start) & (other.nm <= end))]
            return Spectrum(name, nm, br0 * br1)

    def __truediv__(self, other):
        """ Returns a new Spectrum object with the emitter removed (apply a white standard spectrum) """
        name = f'{self.name} / {other.name}'
        start = max(self.nm[0], other.nm[0])
        end = min(self.nm[-1], other.nm[-1])
        if start >= end:
            print(f'# Note for spectral division "{name}"')
            print('- There is no intersection between the spectra, nothing changed.')
            the_first = self.name
            the_second = other.name
            if self.nm[0] > other.nm[0]:
                the_first, the_second = the_second, the_first
            print(f'- "{the_first}" ends on {end} nm and "{the_second}" starts on {start} nm.')
            return self
        else:
            nm = np.arange(start, end+1, resolution, dtype='uint16')
            br0 = self.br[np.where((self.nm >= start) & (self.nm <= end))]
            br1 = other.br[np.where((other.nm >= start) & (other.nm <= end))]
            return Spectrum(name, nm, br0 / br1)


def get_filter(name: str): # TODO: cache them!
    """ Creates a scaled to the unit area Spectrum object based on data file to be found in the `filters` folder """
    try:
        return Spectrum.from_file(name, di.find_filter(name)).scaled_by_area()
    except StopIteration:
        print(f'# Note for the Spectrum object "{name}"')
        print(f'- No filter with the same name in the "filters" folder. Spectrum stub object was created.')
        return Spectrum(name, *spectrum_stub)


bessell_V = get_filter('Generic_Bessell.V')

sun_SI = Spectrum.from_file('Sun', 'spectra/files/CALSPEC/sun_reference_stis_002.fits') # W / (m² nm)
sun_in_V = sun_SI ** bessell_V
sun_norm = sun_SI.scaled_to_albedo(1, bessell_V)

vega_SI = Spectrum.from_file('Vega', 'spectra/files/CALSPEC/alpha_lyr_stis_011.fits') # W / (m² nm)
vega_in_V = vega_SI ** bessell_V
vega_norm = vega_SI.scaled_to_albedo(1, bessell_V)

lambdas = np.arange(5, nm_red_limit+1, 5)
equal_frequency_density = Spectrum('AB', lambdas, 1/lambdas**2).scaled_to_albedo(1, bessell_V) # f_lambda=f_nu*c/lambda^2
del lambdas


class Photometry:
    """ Class to work with set of filters measurements. """

    def __init__(self, name: str, filters: Iterable[Spectrum], br: Iterable, sd: Iterable = None):
        """
        It is assumed that the input can be trusted. If preprocessing is needed, see `Photometry.from_list`.

        Args:
        - `name` (str): human-readable identification. May include source (separated by "|") and notes (separated by ":")
        - `filters` (Iterable): list of energy response functions scaled to the unit area, storing as Spectrum objects
        - `br` (Iterable): same-size list of intensity
        - `sd` (Iterable): same-size list of standard deviations
        """
        self.name = name
        self.filters = tuple(filters)
        self.br = np.array(br, dtype='float')
        if sd is not None:
            self.sd = np.array(sd, dtype='float')
        else:
            self.sd = None
        if np.any(np.isnan(self.br)):
            self.br = np.nan_to_num(self.br)
            print(f'# Note for the Photometry object "{self.name}"')
            print(f'- NaN values detected during object initialization, they been replaced with zeros.')
    
    @staticmethod
    def from_list(name: str, filters: Iterable[str], br: Iterable, sd: Iterable = None):
        """
        Creates a Photometry object from a list of filter's names. Files with such names must be in the `filters` folder.

        Args:
        - `name` (str): human-readable identification. May include source (separated by "|") and notes (separated by ":")
        - `filters` (Iterable): list of file names in the `filters` folder
        - `br` (Iterable): same-size list of intensity
        - `sd` (Iterable): same-size list of standard deviations
        """
        if (len_filters := len(filters)) != (len_br := len(br)):
            print(f'# Note for the Photometry object "{name}"')
            print(f'- Arrays of wavelengths and brightness do not match ({len_filters} vs {len_br}). Photometry stub object was created.')
            return Photometry(name, *photometry_stub)
        if sd is not None and (len_sd := len(sd)) != len_br:
            print(f'# Note for the Photometry object "{name}"')
            print(f'- Array of standard deviations do not match brightness array ({len_sd} vs {len_br}). Uncertainty was erased.')
            sd = None
        return Photometry(name, [get_filter(passband) for passband in filters], br, sd)
    
    def to_scope(self, scope: np.ndarray): # TODO: use optimization algorithm here!
        """ Creates a Spectrum object with inter- and extrapolated photometry data to fit the wavelength scope """
        try:
            nm0 = self.mean_wavelengths()
            nm1 = grid(nm0[0], nm0[-1], resolution)
            br = interpolating(nm0, self.br, nm1, resolution)
            nm, br = extrapolating(nm1, br, scope, resolution)
            return Spectrum(self.name, nm, br, photometry=self)
        except Exception:
            print(f'# Note for the Photometry object "{self.name}"')
            print(f'- Something unexpected happened while trying to inter/extrapolate to Spectrum object. It was replaced by a stub.')
            print(f'- More precisely, {format_exc(limit=0)}')
            return Spectrum(self.name, *spectrum_stub)
    
    def mean_wavelengths(self):
        """ Returns an array of mean wavelengths for each filter """
        return np.array([passband.mean_wavelength() for passband in self.filters])
    
    def standard_deviations(self):
        """ Returns an array of uncorrected standard deviations for each filter """
        return np.array([passband.standard_deviation() for passband in self.filters])

    def __pow__(self, other: Spectrum) -> np.ndarray[float]:
        """ Convolve all the filters with a spectrum """
        return np.array([other ** passband for passband in self.filters])

    def __mul__(self, other: Spectrum):
        """ Returns a new Photometry object with the emitter added (untied from a white standard spectrum) """
        # Scaling brightness scales filters' profiles too!
        filters = [(passband * other).scaled_by_area() for passband in self.filters]
        return Photometry(f'{self.name} ∙ {other.name}', filters, self.br * (self ** other))

    def __truediv__(self, other: Spectrum):
        """ Returns a new Photometry object with the emitter removed (apply a white standard spectrum) """
        # Scaling brightness scales filters' profiles too!
        filters = [(passband / other).scaled_by_area() for passband in self.filters]
        return Photometry(f'{self.name} / {other.name}', filters, self.br / (self ** other))


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
r = Spectrum('r CMF', *np.loadtxt('src/cmf/StilesBurch10deg.r.dat').transpose()).scaled_by_area()
g = Spectrum('g CMF', *np.loadtxt('src/cmf/StilesBurch10deg.g.dat').transpose()).scaled_by_area()
b = Spectrum('b CMF', *np.loadtxt('src/cmf/StilesBurch10deg.b.dat').transpose()).scaled_by_area()

# CIE XYZ functions transformed from the CIE (2006) LMS functions, 10-deg
# http://www.cvrl.org/ciexyzpr.htm
# Sensitivity modulo values less than 10^-4 were previously removed
x = Spectrum('x CMF', *np.loadtxt('src/cmf/cie10deg.x.dat').transpose())
y = Spectrum('y CMF', *np.loadtxt('src/cmf/cie10deg.y.dat').transpose())
z = Spectrum('z CMF', *np.loadtxt('src/cmf/cie10deg.z.dat').transpose())
# Normalization. TODO: find an official way to calibrate brightness for albedo!
# 355.5 was guessed so that the brightness was approximately the same as that of the legacy version
x.br /= 355.5
y.br /= 355.5
z.br /= 355.5



gamma_correction = np.vectorize(lambda p: p * 12.92 if p < 0.0031308 else 1.055 * p**(1.0/2.4) - 0.055)

class Color:
    """ Class to work with color represented by three float values in [0, 1] range. """

    def __init__(self, name: str, rgb: Iterable, albedo=False):
        """
        The albedo flag on means that you have already normalized the brightness over the range.
        By default, initialization implies normalization and you get chromaticity.

        Args:
        - `name` (str): human-readable identification. May include source (separated by "|") and notes (separated by ":")
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
    def from_spectrum(spectrum: Spectrum, albedo=False):
        """ A simple and concrete color processing method based on experimental eye sensitivity curves """
        rgb = [spectrum ** i for i in (r, g, b)]
        return Color(spectrum.name, rgb, albedo)

    @staticmethod
    def from_spectrum_CIE(spectrum: Spectrum, albedo=False, color_system=srgb):
        """ Conventional color processing method: spectrum -> CIE XYZ -> sRGB with illuminant E """
        xyz = [spectrum ** i for i in (x, y, z)]
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


class NonReflectiveBody:
    """ High-level processing class, specializing on photometry of a physical body with not specified reflectance. """

    def __init__(self, name: str, tags: Iterable, spectrum: Spectrum):
        """
        Args:
        - `name` (str): human-readable identification. May include source (separated by "|") and notes (separated by ":")
        - `tags` (Iterable): list of categories that specify the physical body
        - `spectrum` (Spectrum): not assumed to be scaled
        """
        self.name = name
        self.tags = tags
        self.spectrum = spectrum
    
    def get_spectrum(self, mode: str):
        if mode == 'chromaticity' or 'star' in self.tags:
            return self.spectrum # means it's an emitter and we need to render it
        else:
            return Spectrum(self.name, *spectrum_stub).to_scope(visible_range) # means we don't need to render it


class ReflectiveBody:
    """
    High-level processing class, specializing on reflectance photometry of a physical body.

    Albedo formatting rules:
    1. `geometric_albedo` and `spherical_albedo` can be a boolean type or in [filter/nm, br, sd] format
    2. both values by default `false`
    3. no albedo is specified → emitter
    4. one is specified → another one is estimated with the phase integral model

    Phase integral model by Shevchenko et al.: https://ui.adsabs.harvard.edu/abs/2019A%26A...626A..87S/abstract
    q = 0.359 (± 0.005) + 0.47 (± 0.03) p, where `p` is geometric albedo.
    By definition, spherical albedo A is p∙q.
    """

    def __init__(self, name: str, tags: Iterable, geometric: Spectrum = None, spherical: Spectrum = None):
        """
        Args:
        - `name` (str): human-readable identification. May include source (separated by "|") and notes (separated by ":")
        - `tags` (Iterable): list of categories that specify the physical body
        - `geometric` (Spectrum): represents geometric albedo
        - `spherical` (Spectrum): represents spherical albedo
        """
        self.name = name
        self.tags = tags
        self.spherical = spherical
        self.geometric = geometric
    
    def get_spectrum(self, mode: str):
        if mode == 'chromaticity': # chromaticity mode
            if self.geometric:
                return self.geometric # most likely it's original (unscaled) data, so it's a bit better
            else:
                return self.spherical
        elif mode == 'geometric':
            if self.geometric:
                return self.geometric
            else:
                sphericalV = self.spherical ** bessell_V
                geometricV = (np.sqrt(0.359**2 + 4 * 0.47 * sphericalV) - 0.359) / (2 * 0.47)
                return self.spherical.scaled_to_albedo(geometricV, bessell_V)
        else:
            if self.spherical:
                return self.spherical
            else:
                geometricV = self.geometric ** bessell_V
                sphericalV = geometricV * (0.395 + 0.47 * geometricV)
                return self.geometric.scaled_to_albedo(sphericalV, bessell_V)


def number2array(target: int|float|Iterable, size: int):
    """ Makes an array of specified size even if input is a number """
    if isinstance(target, (int, float)):
        return np.full(size, target)
    else:
        return np.array(target)

def mag2flux(mag: int|float|np.ndarray, zero_point: float = 1.):
    """ Converts magnitudes to flux (by default in Vega units) """
    return zero_point * 10**(-0.4 * mag)

def sd_mag2sd_flux(sd_mag: int|float|np.ndarray, irr: int|float|np.ndarray):
    """ Converts standard deviation of magnitude to standard deviation of flux """
    return sd_mag * irr * 0.4 * np.log(10)

def sd_indices2sd_mag(sd_indices: Iterable):
    """ Calculates standard deviations from color indices' deviations """
    l = len(sd_indices)
    sd_mag = np.zeros(l+1, dtype='float')
    sd_mag[0:1] = sd_indices[0] / np.sqrt(2) # assuming the first two points to be with equal uncertainty
    for i in range(2, sd_mag.size):
        sd_mag[i] = np.sqrt(sd_indices[i-1]**2 - sd_mag[i-1]**2)
    return sd_mag

def color_index_splitter(index: str):
    """
    Dashes in filter names are allowed in the SVO Filter Profile Service.
    This function should fix all or most of the problems caused.
    """
    try:
        filter1, filter2 = index.split('-')
    except ValueError:
        dotpart1, dotpart2, dotpart3 = index.split('.') # one dot per full filter name
        dashpart1, dashpart2 = dotpart2.split('-', 1)
        filter1 = dotpart1 + '.' + dashpart1
        filter2 = dashpart2 + '.' + dotpart3
    return filter1, filter2

def color_indices_parser(indices: dict):
    """
    Converts color indices to linear brightness, assuming 1 Vega intensity in the first filter.
    Filters should be specified in ascending order, with the second filter having faster iteration.
    """
    filters = {color_index_splitter(tuple(indices.keys())[0])[0]: 1} # assuming 1 Vega intensity in the first filter
    for key, value in indices.items():
        reference_filter, current_filter = color_index_splitter(key)
        filters |= {current_filter: filters[reference_filter] - value}
    return filters.keys(), mag2flux(np.array(tuple(filters.values())))

def spectral_data2visible_spectrum(
        name: str, nm: Iterable[int|float], filters: Iterable[str], br: Iterable,
        sd: Iterable = None, calib: str = None, sun: bool = False
        ):
    """
    Decides whether we are dealing with photometry or continuous spectrum
    and guarantees the completeness of the spectrum in the visible range.
    """
    if len(nm) > 0:
        spectral_data = Spectrum.from_array(name, nm, br, sd)
    elif len(filters) > 0:
        spectral_data = Photometry.from_list(name, filters, br, sd)
    else:
        print(f'# Note for the database object "{name}"')
        print(f'- No wavelength data. Spectrum stub object was created.')
        spectral_data = Spectrum(name, *spectrum_stub)
    match calib:
        case 'vega':
            spectral_data *= vega_norm
        case 'ab':
            spectral_data *= equal_frequency_density
        case _:
            pass
    if sun:
        spectral_data /= sun_norm
    return spectral_data.to_scope(visible_range)

def database_parser(name: str, content: dict) -> NonReflectiveBody | ReflectiveBody:
    """
    Depending on the contents of the object read from the database, returns a class that has `get_spectrum()` method

    Supported input keys of a database unit:
    - `nm` (list): list of wavelengths in nanometers
    - `br` (list): same-size list of "brightness", flux in units of energy (not a photon counter)
    - `mag` (list): same-size list of magnitudes
    - `sd` (list/number): same-size list of standard deviations or a general value
    - `nm_range` (list): list of [`start`, `stop`, `step`] integer values with including endpoint
    - `file` (str): path to a text or FITS file, recommended placing in `spectra` or `spectra_extras` folder
    - `filters` (list): list of filter names that can be found in the `filters` folder
    - `indices` (list): dictionary of color indices, formatted `{'filter1-filter2': *float*, ...}`
    - `system` (str): a way to bracket the name of the photometric system
    - `calib` (str): `Vega` or `AB` filters zero points calibration, `ST` is assumed by default
    - `albedo` (bool/list): indicates data as albedo scaled or tells how to do it with `[filter/nm, br, (sd)]`
    - `geometric_albedo` (bool/list): indicator of geometric/normal albedo data or how to scale to it
    - `spherical_albedo` (bool/list): indicator of spherical albedo data or how to scale to it
    - `br_geometric`, `br_spherical` (list): specifying unique spectra for different albedos
    - `sd_geometric`, `sd_spherical` (list/number): corresponding standard deviations or a general value
    - `sun` (bool): `true` to remove Sun as emitter
    - `tags` (list): strings, categorizes a spectrum
    """
    br = []
    sd = None
    nm = [] # Spectrum object indicator
    filters = [] # Photometry object indicator
    if 'file' in content:
        try:
            nm, br, sd = di.file_reader(content['file'])
        except Exception:
            nm, br, sd = spectrum_stub
            print(f'# Note for the Spectrum object "{name}"')
            print(f'- Something unexpected happened during external file reading. The data was replaced by a stub.')
            print(f'- More precisely, {format_exc(limit=0)}')
    else:
        # Brightness reading
        if 'br' in content:
            br = content['br']
        elif 'mag' in content:
            br = mag2flux(np.array(content['mag']))
        # Spectrum reading
        if 'nm' in content:
            nm = content['nm']
        elif 'nm_range' in content:
            start, stop, step = content['nm_range']
            nm = np.arange(start, stop+1, step)
        # Photometry reading
        elif 'filters' in content:
            filters = content['filters']
        elif 'indices' in content:
            filters, br = color_indices_parser(content['indices'])
        if 'system' in content:
            filters = [f'{content["system"]}.{short_name}' for short_name in filters]
        # Standard deviation reading
        if 'sd' in content:
            sd = number2array(content['sd'], len(br))
            if 'indices' in content:
                sd = sd_indices2sd_mag(sd)
            if 'indices' in content or 'mag' in content:
                sd = sd_mag2sd_flux(sd, br)
    geometric = None
    spherical = None
    calib = content['calib'].lower() if 'calib' in content else None
    sun = 'sun' in content and content['sun']
    if len(br) == 0:
        if 'br_geometric' in content or 'br_spherical' in content:
            if 'br_geometric' in content:
                br = content['br_geometric']
                sd = number2array(content['sd_geometric'], len(br)) if 'sd_geometric' in content else None
                geometric = spectral_data2visible_spectrum(name, nm, filters, br, sd, calib, sun)
            if 'br_spherical' in content:
                br = content['br_spherical']
                sd = number2array(content['sd_spherical'], len(br)) if 'sd_spherical' in content else None
                spherical = spectral_data2visible_spectrum(name, nm, filters, br, sd, calib, sun)
        else:
            print(f'# Note for the database object "{name}"')
            print(f'- No brightness data. Spectrum stub object was created.')
            spectrum = Spectrum(name, *spectrum_stub).to_scope(visible_range)
    else:
        spectrum = spectral_data2visible_spectrum(name, nm, filters, br, sd, calib, sun)
        # Non-specific albedo parsing
        if 'albedo' in content:
            if isinstance(content['albedo'], bool):
                geometric = spherical = spectrum
            elif isinstance(content['albedo'], list):
                geometric = spherical = spectrum.scaled(*content['albedo'])
            else:
                print(f'# Note for the database object "{name}"')
                print(f'- Invalid albedo value: {content["albedo"]}. Must be boolean or [filter/nm, br, (sd)].')
        # Geometric albedo parsing
        if 'geometric_albedo' in content:
            if isinstance(content['geometric_albedo'], bool):
                geometric = spectrum
            elif isinstance(content['geometric_albedo'], list):
                geometric = spectrum.scaled(*content['geometric_albedo'])
            else:
                print(f'# Note for the database object "{name}"')
                print(f'- Invalid geometric albedo value: {content["geometric_albedo"]}. Must be boolean or [filter/nm, br, (sd)].')
        # Spherical albedo parsing
        if 'spherical_albedo' in content:
            if isinstance(content['spherical_albedo'], bool):
                spherical = spectrum
            elif isinstance(content['spherical_albedo'], list):
                spherical = spectrum.scaled(*content['spherical_albedo'])
            else:
                print(f'# Note for the database object "{name}"')
                print(f'- Invalid spherical albedo value: {content["spherical_albedo"]}. Must be boolean or [filter/nm, br, (sd)].')
    tags = []
    if 'tags' in content:
        tags = content['tags']
    if geometric or spherical:
        return ReflectiveBody(name, tags, geometric, spherical)
    else:
        return NonReflectiveBody(name, tags, spectrum)