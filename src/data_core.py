"""
Describes the main spectral data storage classes and related functions.

- To work with a continuous spectrum, use the Spectrum class.
- To work with measurements in several passbands, use the Photometry class.

The classes are functionally strongly intertwined: Photometry relies on Spectrum,
and Spectrum has the ability to contain and process the Photometry class from
whose information it was inter-/extrapolated.
"""

from typing import Sequence, Callable
from operator import mul, truediv
from traceback import format_exc
from functools import lru_cache
from copy import deepcopy
import numpy as np
import src.auxiliary as aux
import src.data_import as di
from src.experimental import irradiance


class Spectrum:
    """ Class to work with single, continuous spectrum, with strictly defined resolution step. """

    # Initializes an object in case of input data problems
    stub = (np.array([555]), np.zeros(1), None)

    def __init__(self, name: str, nm: Sequence, br: Sequence, sd: Sequence = None, photometry=None):
        """
        It is assumed that the input grid can be trusted. If preprocessing is needed, see `Spectrum.from_array`.

        Args:
        - `name` (str): human-readable identification. May include references (separated by "|") and a note (separated by ":")
        - `nm` (Sequence): list of wavelengths in nanometers with resolution step of 5 nm
        - `br` (Sequence): same-size list of "brightness", flux in units of energy (not a photon counter)
        - `sd` (Sequence, optional): same-size list of standard deviations
        - `photometry` (Photometry, optional): way to store information about the passbands used, for example, to plot it
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
    def from_array(name: str, nm: Sequence, br: Sequence, sd: Sequence = None):
        """
        Creates a Spectrum object from wavelength array with a check for uniformity and possible extrapolation.

        Args:
        - `name` (str): human-readable identification. May include references (separated by "|") and a note (separated by ":")
        - `nm` (Sequence): list of wavelengths, arbitrary grid
        - `br` (Sequence): same-size list of "brightness", flux in units of energy (not a photon counter)
        - `sd` (Sequence): same-size list of standard deviations
        """
        if (len_nm := len(nm)) != (len_br := len(br)):
            print(f'# Note for the Spectrum object "{name}"')
            print(f'- Arrays of wavelengths and brightness do not match ({len_nm} vs {len_br}). Spectrum stub object was created.')
            return Spectrum(name, *Spectrum.stub)
        if sd is not None and (len_sd := len(sd)) != len_br:
            print(f'# Note for the Spectrum object "{name}"')
            print(f'- Array of standard deviations do not match brightness array ({len_sd} vs {len_br}). Uncertainty was erased.')
            sd = None
        try:
            nm = np.array(nm) # numpy decides int or float
            br = np.array(br, dtype='float64')
            if sd is not None:
                sd = np.array(sd, dtype='float64')
            if nm[-1] > aux.nm_red_limit:
                flag = np.where(nm < aux.nm_red_limit + aux.resolution) # with reserve to be averaged
                nm = nm[flag]
                br = br[flag]
                if sd is not None:
                    sd = sd[flag]
            if np.any((diff := np.diff(nm)) != aux.resolution): # if not uniform 5 nm grid
                sd = None # standard deviations is undefined then. TODO: process somehow
                uniform_nm = aux.grid(nm[0], nm[-1], aux.resolution)
                if diff.mean() >= aux.resolution: # interpolation, increasing resolution
                    br = aux.interpolating(nm, br, uniform_nm, aux.resolution)
                else: # decreasing resolution if step less than 5 nm
                    br = aux.averaging(nm, br, uniform_nm, aux.resolution)
                nm = uniform_nm
            if br.min() < 0:
                br = np.clip(br, 0, None)
                #print(f'# Note for the Spectrum object "{name}"')
                #print(f'- Negative values detected while trying to create the object from array, they been replaced with zeros.')
        except Exception:
            nm, br, sd = Spectrum.stub
            print(f'# Note for the Spectrum object "{name}"')
            print(f'- Something unexpected happened while trying to create the object from array. It was replaced by a stub.')
            print(f'- More precisely, {format_exc(limit=0).strip()}')
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
            return Spectrum(self.name, *aux.extrapolating(self.nm, self.br, scope, aux.resolution))
        else:
            return self.photometry.to_scope(scope)

    def integrate(self) -> float:
        """ Calculates the area over the spectrum using the mean rectangle method, per nm """
        return aux.integrate(self.br, aux.resolution)

    def scaled_by_area(self, factor: int|float = 1):
        """ Returns a new Spectrum object with brightness scaled to its area be equal the scale factor """
        return Spectrum(self.name, self.nm, self.br / self.integrate() * factor)
    
    def scaled_at(self, where: str|int|float, how: int|float = 1, sd: int|float = None):
        """
        Returns a new Spectrum object to fit the request brightness (1 by default)
        at specified filter profile or wavelength. TODO: uncertainty processing.
        """
        if isinstance(where, str): # scaling at filter
            transmission = get_filter(where)
            current_br = self.to_scope(transmission.nm) @ transmission
        else: # scaling at wavelength
            if where in self.nm:
                current_br = self.br[np.where(self.nm == where)][0]
            else:
                index = np.abs(self.nm - where).argmin() # closest wavelength
                current_br = np.interp(where, self.nm[index-1:index+1], self.br[index-1:index+1])
        if current_br == 0:
            return deepcopy(self)
        return self * (how / current_br)

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
    
    def apply_linear_operator(self, operator: Callable, operand: int|float):
        """
        Returns a new Spectrum object transformed according to the linear operator.
        Linearity is needed because values and uncertainty are handled uniformly.
        """
        br = operator(self.br, operand)
        sd = None
        if self.sd is not None:
            sd = operator(self.sd, operand)
        photometry = None
        if self.photometry is not None:
            photometry: Photometry = deepcopy(self.photometry)
            photometry.br = operator(photometry.br, operand)
            if photometry.sd is not None:
                photometry.sd = operator(photometry.sd, operand)
        return Spectrum(self.name, self.nm, br, sd, photometry)
    
    def apply_elemental_operator(self, operator: Callable, other, operator_sign: str = ', '):
        """
        Returns a new Spectrum object formed from element-wise operator on two spectra,
        such as multiplication or division.

        Works only at the intersection of spectra! If you need to extrapolate one spectrum
        to the range of another, for example, use `spectrum.to_scope(filter.nm) @ filter`

        Note: the Photometry data would be erased because consistency with the Spectrum object
        cannot be maintained after conversion. TODO: uncertainty processing.
        """
        name = f'{self.name}{operator_sign}{other.name}'
        start = max(self.nm[0], other.nm[0])
        end = min(self.nm[-1], other.nm[-1])
        if start > end: # `>` is needed to process operations with stub objects with no extra logs
            the_first = self.name
            the_second = other.name
            if self.nm[0] > other.nm[0]:
                the_first, the_second = the_second, the_first
            print(f'# Note for spectral element-wise operation "{name.strip()}"')
            print(f'- "{the_first}" ends on {end} nm and "{the_second}" starts on {start} nm.')
            print('- There is no intersection between the spectra. Spectrum stub object was created.')
            return Spectrum(name, *Spectrum.stub)
        else:
            nm = np.arange(start, end+1, aux.resolution, dtype='uint16')
            br0 = self.br[np.where((self.nm >= start) & (self.nm <= end))]
            br1 = other.br[np.where((other.nm >= start) & (other.nm <= end))]
            return Spectrum(name, nm, operator(br0, br1))

    def __mul__(self, other):
        """
        Returns a new Spectrum object modified by the overloaded multiplication operator.
        If the operand is a number, a scaled spectrum is returned.
        If the operand is a Spectrum, an emitter spectrum is applied to the intersection.
        """
        if isinstance(other, (int, float)):
            return self.apply_linear_operator(mul, other)
        else:
            return self.apply_elemental_operator(mul, other, ' ∙ ')
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        """
        Returns a new Spectrum object modified by the overloaded division operator.
        If the operand is a number, a scaled spectrum is returned.
        If the operand is a Spectrum, an emitter spectrum is removed from the intersection.
        """
        if isinstance(other, (int, float)):
            return self.apply_linear_operator(truediv, other)
        else:
            return self.apply_elemental_operator(truediv, other, ' / ')
    
    def __matmul__(self, other) -> float:
        """ Implementation of convolution between emission spectrum and transmission spectrum """
        return (self * other).integrate()


@lru_cache(maxsize=32)
def get_filter(name: str):
    """ Creates a scaled to the unit area Spectrum object based on data file to be found in the `filters` folder """
    return Spectrum.from_file(name, di.find_filter(name)).scaled_by_area()


class Photometry:
    """ Class to work with set of filters measurements. """

    # Initializes an object in case of input data problems
    stub = ([get_filter('Generic_Bessell.V')], np.zeros(1), None)

    def __init__(self, name: str, filters: Sequence[Spectrum], br: Sequence, sd: Sequence = None):
        """
        It is assumed that the input can be trusted. If preprocessing is needed, see `Photometry.from_list`.

        Args:
        - `name` (str): human-readable identification. May include references (separated by "|") and a note (separated by ":")
        - `filters` (Sequence): list of energy response functions scaled to the unit area, storing as Spectrum objects
        - `br` (Sequence): same-size list of intensity
        - `sd` (Sequence): same-size list of standard deviations
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
    def from_list(name: str, filters: Sequence[str], br: Sequence, sd: Sequence = None):
        """
        Creates a Photometry object from a list of filter's names. Files with such names must be in the `filters` folder.

        Args:
        - `name` (str): human-readable identification. May include references (separated by "|") and a note (separated by ":")
        - `filters` (Sequence): list of file names in the `filters` folder
        - `br` (Sequence): same-size list of intensity
        - `sd` (Sequence): same-size list of standard deviations
        """
        if (len_filters := len(filters)) != (len_br := len(br)):
            print(f'# Note for the Photometry object "{name}"')
            print(f'- Arrays of wavelengths and brightness do not match ({len_filters} vs {len_br}). Photometry stub object was created.')
            return Photometry(name, *Photometry.stub)
        if sd is not None and (len_sd := len(sd)) != len_br:
            print(f'# Note for the Photometry object "{name}"')
            print(f'- Array of standard deviations do not match brightness array ({len_sd} vs {len_br}). Uncertainty was erased.')
            sd = None
        # Checking existing and ordering
        filters = list(filters)
        br = list(br)
        if sd is not None:
            sd = list(sd)
        mean_wavelengths = []
        for j, passband in enumerate(reversed(deepcopy(filters))):
            i = len_filters-1-j
            try:
                filters[i] = get_filter(passband)
                mean_wavelengths.append(filters[i].mean_wavelength())
            except di.FilterNotFoundError:
                print(f'# Note for the Photometry object "{name}"')
                print(f'- Filter "{passband}" not found in the "filters" folder. The corresponding data will be erased.')
                del filters[i], br[i]
                if sd is not None:
                    del sd[i]
        if len(filters) == 0:
            print(f'# Note for the Photometry object "{name}"')
            print(f'- No declared filter profiles were found in the "filters" folder. Photometry stub object was created.')
            return Photometry(name, *Photometry.stub)
        else:
            nm = np.array(mean_wavelengths)
            if np.any(nm[:-1] < nm[1:]): # fast decreasing check
                order = np.argsort(nm[::-1])
                filters = np.array(filters)[order]
                br = np.array(br)[order]
                if sd is not None:
                    sd = np.array(sd)[order]
            return Photometry(name, filters, br, sd)
    
    def to_scope(self, scope: np.ndarray): # TODO: use kriging here!
        """ Creates a Spectrum object with inter- and extrapolated photometry data to fit the wavelength scope """
        try:
            nm0 = self.mean_wavelengths()
            nm1 = aux.grid(nm0[0], nm0[-1], aux.resolution)
            br = aux.interpolating(nm0, self.br, nm1, aux.resolution)
            nm, br = aux.extrapolating(nm1, br, scope, aux.resolution)
            return Spectrum(self.name, nm, br, photometry=deepcopy(self))
        except Exception:
            print(f'# Note for the Photometry object "{self.name}"')
            print(f'- Something unexpected happened while trying to inter/extrapolate to Spectrum object. It was replaced by a stub.')
            print(f'- More precisely, {format_exc(limit=0).strip()}')
            return Spectrum(self.name, *Spectrum.stub)
    
    def mean_wavelengths(self):
        """ Returns an array of mean wavelengths for each filter """
        return np.array([passband.mean_wavelength() for passband in self.filters])
    
    def standard_deviations(self):
        """ Returns an array of uncorrected standard deviations for each filter """
        return np.array([passband.standard_deviation() for passband in self.filters])

    def __mul__(self, other: Spectrum):
        """ Returns a new Photometry object with the emitter added (untied from a white standard spectrum) """
        # Scaling brightness scales filters' profiles too!
        filters = [(passband * other).scaled_by_area() for passband in self.filters]
        return Photometry(f'{self.name} ∙ {other.name}', filters, self.br * (self @ other))
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other: Spectrum):
        """ Returns a new Photometry object with the emitter removed (apply a white standard spectrum) """
        # Scaling brightness scales filters' profiles too!
        filters = [(passband / other).scaled_by_area() for passband in self.filters]
        return Photometry(f'{self.name} / {other.name}', filters, self.br / (self @ other))

    def __matmul__(self, other: Spectrum) -> np.ndarray[float]:
        """ Convolve all the filters with a spectrum """
        return np.array([other @ passband for passband in self.filters])
