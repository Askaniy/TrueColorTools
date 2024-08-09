
"""
Describes the main spectral data storage classes and related functions.

The hierarchy of core classes in a project:
- TrueColorToolsObject
- - SpectralObject
- - - 1D: Spectrum
- - - 2D: FilterSystem
- - - 3D: SpectralCube
- - PhotospectralObject
- - - 1D: Photospectrum
- - - 3D: PhotospectralCube

(Self-complete classes system would include a 2D `PhotospectrumSet` and
`SpectrumSet` instead of `FilterSystem`, with convolution operation defined.
But this is not required by the current functionality of the TCT.
This could be useful to process an entire spectral database without loops.)
"""

from copy import deepcopy
from typing import Sequence, Callable, Self
from pathlib import Path
from operator import mul, truediv
from functools import lru_cache
from traceback import format_exc
import numpy as np

from src.data_import import file_reader
import src.auxiliary as aux
import src.strings as tr
import src.image_import as ii


class ObjectName:
    """
    Class to work with a (celestial object) name.
    It parses the original string (raw_name) and stores the components:
    - index
    - name(lang)
    - note(lang)
    - info
    - reference
    """

    unnamed_count = 0 # class attribute to track the number of unnamed objects

    def __init__(self, name: str = None) -> None:
        """
        Initializes the ObjectName with name parsing.
        The template is `(index) name: note (info) | reference`.
        If no name is specified, a numbered unnamed object will be created.
        """
        self.index = self._note_en = self.info = self.reference = None
        if name is None:
            ObjectName.unnamed_count += 1
            self.raw_name = ObjectName.unnamed_count
            self._name_en = f'Unnamed object {ObjectName.unnamed_count}'
        else:
            self.raw_name = name
            if '|' in name:
                name, reference = name.split('|')
                self.reference = reference.strip()
            if name[0] == '(': # minor body index or something else
                index, name = name.split(')', 1)
                self.index = index[1:].strip()
            elif '/' in name: # comet name
                index, name = name.split('/', 1)
                self.index = index.strip() + '/'
            if '(' in name: # stellar spectral type or something else
                name, info = name.split('(', 1)
                self.info = info.split(')', 1)[0].strip()
            if ':' in name:
                name, note = name.split(':', 1)
                self._note_en = note.strip()
            self._name_en = name.strip()
    
    def name(self, lang: str = 'en') -> str:
        """ Returns the name in the specified language """
        return self._name_en if lang == 'en' else self.translate(self._name_en, tr.names, lang)
    
    def note(self, lang: str = 'en') -> str:
        """ Returns the note in the specified language """
        if self._note_en:
            return self._note_en if lang == 'en' else self.translate(self._note_en, tr.notes, lang)
        else:
            return None
    
    def indexed_name(self, lang: str = 'en') -> str:
        """ Returns the name with the index in the specified language """
        name = self.name(lang)
        if self.index:
            if self.index[-1] == '/':
                # a comet with a number prefix
                name = f'{self.index}{name}'
            elif '/' in self.index:
                # a comet without a number prefix
                name = f'{self.index} ({name})'
            elif name[:4].isnumeric():
                # index of an unnamed asteroid
                name = f'({self.index}) {name}'
            else:
                name = f'{self.index} {name}'
        return name

    @lru_cache(maxsize=None)
    def __call__(self, lang: str = 'en') -> str:
        """ Returns a string composed of the available attributes """
        name = self.indexed_name(lang)
        if self._note_en:
            name = f'{name}: {self.note(lang)}'
        if self.info:
            name = f'{name} ({self.info})'
        if self.reference:
            name = f'{name} [{self.reference}]'
        return name
    
    @staticmethod
    def translate(target: str, translations: dict[str, dict[str, str]], lang: str) -> str:
        """ Searches part of the target string to be translated and replaces it with translation """
        for original, translation in translations.items():
            if target.startswith(original) or target.endswith(original) or original in target.split():
                target = target.replace(original, translation[lang])
                break
        return target
    
    @staticmethod
    def as_ObjectName(input) -> Self:
        """ Guaranteed to return an object of the given class, even if the input may have already been one """
        return input if isinstance(input, ObjectName) else ObjectName(input)
    
    def __hash__(self) -> int:
        """ Returns the hash value of the object """
        return hash(self.raw_name)
    
    def __eq__(self, other) -> bool:
        """ Checks equality with another ObjectName instance """
        if isinstance(other, ObjectName):
            return self.raw_name == other.raw_name
        return False
    
    def __str__(self) -> str:
        return self()



# TCT was written in an effort to work not only with the optical range, but with any, depending on the data.
# But too long and heterogeneous FITS files demanded to set the upper limit of the range to mid-wavelength infrared (3 μm).
nm_red_limit = 3000 # nm
# Actually, dtype=uint16 is used to store wavelength. It's possible to set the limit to 65535 nm with no compression,
# and to 327 675 nm with 5 nm compression.

# For the sake of simplifying work with the spectrum, its discretization step in only 5 nm.
nm_step = 5 # nm

# To calculate color, it is necessary to achieve a definition of the spectrum in the visible range.
# Boundaries have been defined based on the CMF (color matching functions) used, but can be any.
visible_range = np.arange(390, 780, nm_step) # nm


class _TrueColorToolsObject:
    """ Internal class for inheriting spectral data properties """
    br = np.empty(0)
    sd = None
    
    def __len__(self):
        """ Returns the spectral axis length """
        return self.br.shape[0]
    
    @property
    def shape(self):
        """ Returns the spatial axes shape: number of filters or (width, hight) """
        return self.br.shape[1:]
    
    @property
    def ndim(self):
        """ Shortcut to get the number of dimensions """
        return self.br.ndim
    
    def apply_linear_operator(self, operator: Callable, operand: int|float|np.ndarray) -> Self:
        """
        Returns a new object of the same class transformed according to the linear operator.
        Linearity is needed because values and uncertainty are handled uniformly.
        """
        output = deepcopy(self)
        output.br = operator(self.br.T, operand).T
        output.sd = None
        if self.sd is not None:
            output.sd = operator(self.sd.T, operand).T
        return output
    
    def __mul__(self, other: int|float|np.ndarray) -> Self:
        if isinstance(other, (int, float, np.ndarray)):
            return self.apply_linear_operator(other, mul)
        return NotImplemented
    
    def __rmul__(self, other: int|float|np.ndarray) -> Self:
        return self.__mul__(other)
    
    def __truediv__(self, other: int|float|np.ndarray) -> Self:
        if isinstance(other, (int, float, np.ndarray)):
            return self.apply_linear_operator(other, truediv)
        return NotImplemented


class _SpectralObject(_TrueColorToolsObject):
    """
    Internal parent class for Spectrum (1D), FilterSystem (2D) and SpectralCube (3D).
    The first index of the "brightness" array iterates over the spectral axis.

    Attributes:
    - `nm` (np.ndarray): spectral axis, list of wavelengths in nanometers on a uniform grid
    - `br` (np.ndarray): array of "brightness" in energy density units (not a photon counter)
    - `sd` (np.ndarray): optional array of standard deviations
    - `name` (ObjectName): name as an instance of a class that stores its components
    - `photometry` (PhotospectralObject): optional, way to store the pre-reconstructed data
    """
    
    def __init__(self, nm: Sequence, br: Sequence, sd: Sequence = None, name: str|ObjectName = None, photometry=None) -> None:
        """
        It is assumed that the input wavelength grid can be trusted. If preprocessing is needed, see `SpectralObject.from_array`.
        There are no checks for negativity, since such spectra exist, for example, red CMF.

        Args:
        - `nm` (Sequence): spectral axis, list of wavelengths in nanometers on a uniform grid
        - `br` (Sequence): array of "brightness" in energy density units (not a photon counter)
        - `sd` (Sequence): optional array of standard deviations
        - `name` (str|ObjectName): name as a string or an instance of a class that stores its components
        - `photometry` (PhotospectralObject): optional, way to store the pre-reconstructed data
        """
        self.nm = np.asarray(nm, dtype='int16')
        self.br = np.asarray(br, dtype='float64')
        self.sd = None if sd is None else np.asarray(sd, dtype='float64')
        self.name = ObjectName.as_ObjectName(name)
        self.photometry = photometry
        if np.any(np.isnan(self.br)):
            self.br = np.nan_to_num(self.br)
            print(f'# Note for the SpectralObject "{self.name}"')
            print(f'- NaN values detected during object initialization, they been replaced with zeros.')
    
    @staticmethod
    def from_array(nm: np.ndarray, br: np.ndarray, sd: np.ndarray = None, name: str|ObjectName = None) -> Self:
        """
        Creates a SpectralObject from wavelength array with a check for uniformity and possible extrapolation.

        Args:
        - `nm` (Sequence): list of wavelengths in nanometers on an arbitrary grid
        - `br` (Sequence): array of "brightness" in energy density units (not a photon counter)
        - `sd` (Sequence): optional array of standard deviations
        - `name` (str|ObjectName): name as a string or an instance of a class that stores its components
        """
        nm = np.asarray(nm) # numpy decides int or float
        br = np.asarray(br, dtype='float64')
        if sd is not None:
            sd = np.asarray(sd, dtype='float64')
        name = ObjectName.as_ObjectName(name)
        match br.ndim:
            case 1:
                target_class = Spectrum
            case 2:
                target_class = FilterSystem
            case 3:
                target_class = SpectralCube
        target_class_name = target_class.__name__
        try:
            if (len_nm := nm.size) != (len_br := br.shape[0]):
                print(f'# Note for the {target_class_name} "{name}"')
                print(f'- Arrays of wavelengths and brightness do not match ({len_nm} vs {len_br}). {target_class_name} stub object was created.')
                return target_class.stub(br.shape[1:], name)
            if sd is not None and (len_sd := sd.shape[0]) != len_br:
                print(f'# Note for the {target_class_name} "{name}"')
                print(f'- Array of standard deviations do not match brightness array ({len_sd} vs {len_br}). Uncertainty was erased.')
                sd = None
            if np.any(nm[:-1] > nm[1:]): # fast increasing check
                order = np.argsort(nm)
                nm = nm[order]
                br = br[order]
                if sd is not None:
                    sd = sd[order]
            if nm[-1] > nm_red_limit:
                flag = np.where(nm < nm_red_limit + nm_step) # with reserve to be averaged
                nm = nm[flag]
                br = br[flag]
                if sd is not None:
                    sd = sd[flag]
            if np.any((diff := np.diff(nm)) != nm_step): # if not uniform 5 nm grid
                sd = None # standard deviations is undefined then. TODO: process somehow
                uniform_nm = aux.grid(nm[0], nm[-1], nm_step)
                if diff.mean() >= nm_step: # interpolation, increasing resolution
                    br = aux.interpolating(nm, br, uniform_nm, nm_step)
                else: # decreasing resolution if step less than 5 nm
                    br = aux.spectral_downscaling(nm, br, uniform_nm, nm_step)
                nm = uniform_nm
            if br.min() < 0:
                br = np.clip(br, 0, None)
                #print(f'# Note for the {target_class_name} "{name}"')
                #print(f'- Negative values detected while trying to create the object from array, they been replaced with zeros.')
            return target_class(nm, br, sd, name=name)
        except Exception:
            print(f'# Note for the {target_class_name} "{name}"')
            print(f'- Something unexpected happened while trying to create an object from the array. It was replaced by a stub.')
            print(f'- More precisely, {format_exc(limit=0).strip()}')
            return target_class.stub(name=name)
    
    def scaled_at(self, where, how: int|float = 1, sd: int|float = None) -> Self:
        """
        Returns a new SpectralObject to fit the request brightness (1 by default)
        at specified filter profile or wavelength.
        """
        # TODO: uncertainty processing
        # TODO: problems with cubes?
        if isinstance(where, str):
            where = get_filter(where)
        if isinstance(where, Spectrum):
            current_br = self @ where
        else: # scaling at wavelength
            if where in self.nm: # on the grid
                current_br = self.br[np.where(self.nm == where)][0]
            else:
                if self.nm[0] < where < self.nm[-1]: # in a range of the grid
                    nm = self.nm
                    br = self.br
                else: # out of range, extrapolation is needed
                    start = min(self.nm[0], where)
                    end = max(self.nm[-1], where)
                    nm = aux.grid(start, end, nm_step)
                    nm, br = aux.extrapolating(self.nm, self.br, nm, nm_step)
                index = np.abs(nm - where).argmin() # closest wavelength
                current_br = np.interp(where, nm[index-1:index+1], br[index-1:index+1])
        if current_br == 0:
            return deepcopy(self)
        return self * (how / current_br)
    
    def integrate(self) -> np.ndarray:
        """ Collapses the SpectralObject along the spectral axis into a two-dimensional image """
        return aux.integrate(self.br, nm_step)
    
    def normalize(self) -> Self:
        """ Returns a new SpectralObject with each spectrum divided by its area """
        return self / self.integrate()
    
    def convert_from_photon_spectral_density(self) -> Self:
        """
        Returns a new SpectralObject converted from photon spectral density
        to energy spectral density, using the fact that E = h c / λ.
        """
        return (self / self.nm).normalize()
    
    def convert_from_frequency_spectral_density(self) -> Self:
        """
        Returns a new SpectralObject converted from frequency spectral density
        to energy spectral density, using the fact that f_λ = f_ν c / λ².
        """
        return (self / self.nm**2).normalize()
    
    def mean_wavelength(self) -> float|np.ndarray[np.floating]:
        """ Returns mean wavelength or array of mean wavelengths """
        try:
            match self.ndim:
                case 1:
                    return np.average(self.nm, weights=self.br)
                case 2:
                    return np.average(aux.scope2matrix(self.nm, self.shape), weights=self.br, axis=1)
                case 3: # not tested
                    return np.average(aux.scope2cube(self.nm, self.shape), weights=self.br, axis=(1, 2))
        except ZeroDivisionError:
            print(f'# Note for the SpectralObject "{self.name}"')
            print(f'- Bolometric brightness is zero, the mean wavelength cannot be calculated. Returns 0 nm.')
            return 0.
    
    def standard_deviation(self) -> np.ndarray[np.floating]:
        """ Returns uncorrected standard deviation or an array of uncorrected standard deviations """
        match self.ndim:
            case 1:
                return np.sqrt(np.average((self.nm - self.mean_wavelength())**2, weights=self.br))
            case 2:
                return np.sqrt(np.average((aux.scope2matrix(self.nm, self.shape).T - self.mean_wavelength()).T**2, weights=self.br, axis=1))
            case 3: # not tested
                return np.sqrt(np.average((aux.scope2cube(self.nm, self.shape).T - self.mean_wavelength()).T**2, weights=self.br, axis=(1, 2)))
    
    def get_br_in_range(self, start: int, end: int) -> np.ndarray:
        """ Returns brightness values over a range of wavelengths (ends included!) """
        # TODO: round up to a multiple of 5
        return self.br[np.where((self.nm >= start) & (self.nm <= end))]
    
    def to_scope(self, scope: np.ndarray, crop: bool = False) -> Self:
        """ Returns a new SpectralObject with a guarantee of definition on the requested scope """
        if self.photometry is None:
            extrapolated = self.__class__(*aux.extrapolating(self.nm, self.br, scope, nm_step), name=self.name)
        else:
            extrapolated = self.photometry.to_scope(scope) # repeat reconstruction on a new scope
        if crop:
            start = max(extrapolated.nm[0], scope[0])
            end = min(extrapolated.nm[-1], scope[-1])
            extrapolated.br = extrapolated.get_br_in_range(start, end)
        return extrapolated
    
    def apply_linear_operator(self, operand: int|float|np.ndarray, operator: Callable) -> Self:
        """
        Returns a new object of the same class transformed according to the linear operator.
        Linearity is needed because values and uncertainty are handled uniformly.
        """
        br = operator(self.br.T, operand).T
        sd = None
        if self.sd is not None:
            sd = operator(self.sd.T, operand).T
        photometry = None
        if self.photometry is not None:
            photometry = operator(deepcopy(self.photometry), operand)
        return self.__class__(self.nm, br, sd, name=self.name, photometry=photometry)
    
    def __matmul__(self, other):
        """
        Implementation of convolution (in the meaning of synthetic photometry).
        If necessary, extrapolates over the wavelength interval of the second operand.

        Only 8 convolution options make physical sense:
        - Spectrum @ Spectrum              -> float
        - Spectrum @ FilterSystem          -> Photospectrum
        - SpectralCube @ Spectrum          -> image array
        - SpectralCube @ FilterSystem      -> PhotospectralCube
        - Photospectrum @ Spectrum         -> float
        - Photospectrum @ FilterSystem     -> Photospectrum
        - PhotospectralCube @ Spectrum     -> image array
        - PhotospectralCube @ FilterSystem -> PhotospectralCube
        """
        # TODO: uncertainty processing
        operand1_class_name = self.__class__.__name__
        operand1 = self.to_scope(other.nm)
        operand2 = other.to_scope(self.nm) # also reconstructs PhotospectralObj to SpectralObj
        match operand1.ndim:
            case 1: # Spectrum or Photospectrum
                match operand2.ndim:
                    case 1: # Spectrum
                        return aux.integrate(operand2.br * operand1.br, nm_step)
                    case 2: # FilterSystem
                        br = aux.integrate((operand2.br.T * operand1.br).T, nm_step)
                        return Photospectrum(operand2, br, name=operand1.name)
            case 2: # FilterSystem
                print(f'# Note for the {operand1_class_name} "{operand1.name}"')
                print(f'- Convolution of a filter system makes no physical sense.')
            case 3: # SpectralCube or PhotospectralCube
                match operand2.ndim:
                    case 1: # Spectrum
                        return aux.integrate((operand2.br.T * operand1.br).T, nm_step)
                    case 2: # FilterSystem
                        br = np.empty((len(operand1), *other.shape))
                        for i, profile in enumerate(operand1.br):
                            br[i] = aux.integrate((operand2.br.T * profile).T, nm_step)
                        return PhotospectralCube(operand2, br, name=operand1.name)
        return NotImplemented


class Spectrum(_SpectralObject):
    """
    Class to work with a single spectrum (1D SpectralObject).

    Attributes:
    - `nm` (np.ndarray): spectral axis, list of wavelengths in nanometers on a uniform grid
    - `br` (np.ndarray): array of "brightness" in energy density units (not a photon counter)
    - `sd` (np.ndarray): optional array of standard deviations
    - `name` (ObjectName): name as an instance of a class that stores its components
    """
    
    @staticmethod
    def stub(name=None) -> Self:
        """ Initializes an object in case of the data problems """
        return Spectrum((555,), np.zeros(1), name=name)
    
    @staticmethod
    def from_file(file: str, name: str|ObjectName = None) -> Self:
        """ Creates a Spectrum object based on loaded data from the specified file """
        return Spectrum.from_array(*file_reader(file), name=name)
    
    @staticmethod
    def from_nm(nm_point: int|float) -> Self:
        """
        Creates a point Spectrum on the grid of allowed values.
        Returns single point with brightness 1 for on-grid wavelength
        and two points otherwise with a total brightness of 1.
        """
        nm_point_int = int(nm_point)
        if nm_point_int % nm_step == 0 and nm_point == nm_point_int:
            nm = (nm_point_int,)
            br = ((1.,))
        else:
            nm_point_floor = nm_point // nm_step
            nm0 = nm_point_floor * nm_step
            nm0_proximity_factor = nm_point/nm_step - nm_point_floor
            nm = (nm0, nm0+nm_step)
            br = (1.-nm0_proximity_factor, nm0_proximity_factor)
        return Spectrum(nm, br, name=f'{nm_point} nm')
    
    @staticmethod
    def from_blackbody_redshift(scope: np.ndarray, temperature: int|float, velocity=0., vII=0.) -> Self:
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
            br = aux.irradiance(scope*doppler*grav, temperature)
        else:
            br = np.zeros(scope.size)
        return Spectrum(scope, br, name=f'BB with T={round(temperature)} K')
    
    def edges_zeroed(self) -> Self:
        """
        Returns a new Spectrum object with zero brightness to the edges added.
        This is necessary to mitigate the consequences of abruptly cutting off filter profiles.
        """
        profile = deepcopy(self)
        limit = profile.br.max() * 0.1 # adding point if an edge brightness higher than 10% of the peak
        if profile.br[0] >= limit:
            profile.nm = np.append(profile.nm[0]-nm_step, profile.nm)
            profile.br = np.append(0., profile.br)
        if profile.br[-1] >= limit:
            profile.nm = np.append(profile.nm, profile.nm[-1]+nm_step)
            profile.br = np.append(profile.br, 0.)
        return profile
    
    def apply_spectral_element_wise_operation(self, other: _SpectralObject, operator: Callable) -> _SpectralObject:
        """
        Returns a new SpectralObject formed from element-wise operation with the Spectrum,
        such as multiplication or division.
        
        Element-wise are only possible with 1D SpectralObjects: other would produce 4D+ arrays,
        which most computers do not have enough memory for.

        Works only at the intersection of the spectral axes! If you need to extrapolate one axis
        to the range of another, use `SpectralObject.to_scope()`.
        """
        # TODO: uncertainty processing
        start = max(self.nm[0], other.nm[0])
        end = min(self.nm[-1], other.nm[-1])
        if start > end: # `>` is needed to process operations with stub objects with no extra logs
            the_first = self.name
            the_second = other.name
            if self.nm[0] > other.nm[0]:
                the_first, the_second = the_second, the_first
            print(f'# Note for SpectralObject element-wise operation "{operator.__name__}"')
            print(f'- "{the_first}" ends on {end} nm and "{the_second}" starts on {start} nm.')
            print('- There is no intersection between the spectra. SpectralObject stub object was created.')
            return other.__class__.stub(other.shape, other.name)
        else:
            nm = np.arange(start, end+1, nm_step, dtype='uint16')
            br0 = self.get_br_in_range(start, end)
            br1 = other.get_br_in_range(start, end)
            return other.__class__(nm, operator(br0, br1.T).T, name=other.name)
    
    def apply_photospectral_element_wise_operation(self, photospectrum_or_system, operator: Callable, inverse_operator: Callable):
        """
        Returns a new PhotospectralObject formed from element-wise operation with the Spectrum,
        such as multiplication or division.
        Note that this also distorts the effective filter profiles!
        
        Element-wise are only possible with 1D SpectralObjects: other would produce 4D+ arrays,
        which most computers do not have enough memory for.
        """
        # TODO: uncertainty processing
        self_photospectrum = self @ photospectrum_or_system.filter_system
        output = operator(photospectrum_or_system, self_photospectrum.br)
        distorted_profiles = inverse_operator(photospectrum_or_system.filter_system, self)
        output.filter_system = operator(distorted_profiles, self_photospectrum.br)
        return output
    
    def __mul__(self, other):
        if isinstance(other, _SpectralObject):
            return self.apply_spectral_element_wise_operation(other, mul)
        elif isinstance(other, _PhotospectralObject):
            return self.apply_photospectral_element_wise_operation(other, mul, truediv)
        else:
            return super().__mul__(other)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, _SpectralObject):
            return self.apply_spectral_element_wise_operation(other, truediv)
        elif isinstance(other, _PhotospectralObject):
            return self.apply_photospectral_element_wise_operation(other, truediv, mul)
        else:
            return super().__truediv__(other)


@lru_cache(maxsize=32)
def get_filter(name: str|int|float) -> Spectrum:
    """
    Creates a scaled to the unit area Spectrum object.
    Requires file name to be found in the `filters` folder to load profile
    or wavelength in nanometers to generate single-point profile.
    """
    if not isinstance(name, str) or name.isnumeric():
        profile = Spectrum.from_nm(float(name))
    else:
        try:
            file = str(next(Path('filters').glob(f'{name}.*')))
            profile = Spectrum.from_file(file, name)
        except StopIteration:
            print(f'# Note for the Spectrum object {name}')
            print(f'- Filter "{name}" not found in the "filters" folder. It was replaced by a stub.')
            profile = Spectrum.stub(name)
    return profile.edges_zeroed().normalize()


class FilterSystem(_SpectralObject):
    """
    Class to work with a set of filters profiles.

    Attributes:
    - `nm` (np.ndarray): total wavelength range of the filter profiles
    - `br` (np.ndarray): matrix of the profiles with shape [len(nm), len(filters)]
    - `name` (ObjectName): name as an instance of a class that stores its components
    - `number` (int): number of filters in the system
    """
    # TODO: original filter names are lost!
    
    @staticmethod
    def stub(name=None) -> Self:
        """ Initializes an object in case of the data problems """
        return FilterSystem((555,), np.zeros((1, 1)), name=name)
    
    @staticmethod
    def from_list(filters: Sequence[str|Spectrum], name: str|ObjectName = None):
        """
        Creates a FilterSystem object from a list of names or profiles.

        Args:
        - `filters` (Sequence[str|Spectrum]): list of names or profiles (can be mixed)
        - `name` (str|ObjectName): name as a string or an instance of a class that stores its components
        """
        # Getting the wavelength info and filter names
        min_arr = []
        max_arr = []
        filters = list(filters)
        for i, profile in enumerate(filters):
            if isinstance(profile, str):
                profile = get_filter(profile)
                filters[i] = profile
            min_arr.append(profile.nm[0])
            max_arr.append(profile.nm[-1])
        # Matrix packing
        nm = aux.grid(min(min_arr), max(max_arr), nm_step)
        br = np.zeros((len(nm), len(filters)))
        for i, profile in enumerate(filters):
            br[np.where((nm >= min_arr[i]) & (nm <= max_arr[i])), i] = profile.br
        return FilterSystem(nm, br, name=name)
    
    @property
    def number(self) -> int:
        """ Returns the number of filters in the system """
        return self.shape[0]



class _PhotospectralObject(_TrueColorToolsObject):
    """
    Internal parent class for Photospectrum (1D) and PhotospectralCube (3D).

    Attributes:
    - `filter_system` (FilterSystem): instance of the class storing filter profiles
    - `nm` (np.ndarray): shortcut for filter_system.nm, the definition range
    - `br` (np.ndarray): array of "brightness" in energy density units (not a photon counter)
    - `sd` (np.ndarray): optional array of standard deviations
    - `name` (ObjectName): name as an instance of a class that stores its components
    """
    
    def __init__(self, filter_system: FilterSystem, br: Sequence, sd: Sequence = None, name: str|ObjectName = None) -> None:
        """
        Args:
        - `filter_system` (FilterSystem): instance of the class storing filter profiles
        - `br` (Sequence): array of "brightness" in energy density units (not a photon counter)
        - `sd` (Sequence): optional array of standard deviations
        - `name` (str|ObjectName): name as a string or an instance of a class that stores its components
        """
        self.filter_system = filter_system
        self.br = np.asarray(br, dtype='float64')
        self.sd = None if sd is None else np.asarray(sd, dtype='float64')
        self.name = ObjectName.as_ObjectName(name)
        if (filters_num := filter_system.number) != (len_br := br.shape[0]):
            print(f'# Note for the PhotospectralObject "{name}"')
            print(f'- Arrays of wavelengths and brightness do not match ({filters_num} vs {len_br}). PhotospectralCube stub object was created.')
            return self.stub(br.shape[1:], name)
        if sd is not None and (len_sd := sd.shape[0]) != len_br:
            print(f'# Note for the PhotospectralObject "{name}"')
            print(f'- Array of standard deviations do not match brightness array ({len_sd} vs {len_br}). Uncertainty was erased.')
            sd = None
        if np.any(np.isnan(self.br)):
            self.br = np.nan_to_num(self.br)
            print(f'# Note for the PhotospectralObject object "{self.name}"')
            print(f'- NaN values detected during object initialization, they been replaced with zeros.')
    
    @property
    def nm(self) -> np.ndarray[np.integer]:
        """ Returns the definition range of the filter system """
        return self.filter_system.nm
    
    def convert_from_photon_spectral_density(self) -> Self:
        """
        Returns a new PhotospectralObject converted from photon spectral density
        to energy spectral density, using the fact that E = h c / λ.
        """
        profiles = self.filter_system.normalize()
        scale_factors = (profiles / profiles.nm).integrate()
        return self * scale_factors
    
    def convert_from_frequency_spectral_density(self) -> Self:
        """
        Returns a new PhotospectralObject converted from frequency spectral density
        to energy spectral density, using the fact that f_λ = f_ν c / λ².
        """
        profiles = self.filter_system.normalize()
        scale_factors = (profiles / profiles.nm**2).integrate()
        return self * scale_factors
    
    def mean_wavelength(self) -> np.ndarray[np.floating]:
        """ Returns an array of mean wavelengths for each filter """
        return self.filter_system.mean_wavelength()
    
    def to_scope(self, scope: np.ndarray) -> _SpectralObject: # TODO: use kriging here!
        """ Reconstructs a SpectralObject with inter- and extrapolated photospectrum data to fit the wavelength scope """
        match self.ndim:
            case 1:
                target_class = Spectrum
            case 3:
                target_class = SpectralCube
        try:
            nm0 = self.mean_wavelength()
            br0 = self.br
            if self.filter_system.number > 1:
                if np.any(nm0[:-1] > nm0[1:]): # fast increasing check
                    order = np.argsort(nm0)
                    nm0 = nm0[order]
                    br0 = br0[order]
                nm1 = aux.grid(nm0[0], nm0[-1], nm_step)
                br1 = aux.interpolating(nm0, br0, nm1, nm_step)
                nm1, br1 = aux.extrapolating(nm1, br1, scope, nm_step)
            else: # single-point PhotospectralObject support
                nm1, br1 = aux.extrapolating((nm0[0],), (br0[0],), scope, nm_step)
            return target_class(nm1, br1, name=self.name, photometry=deepcopy(self))
        except Exception:
            print(f'# Note for the PhotospectralObject "{self.name}"')
            print(f'- Something unexpected happened while trying to inter/extrapolate to a {target_class.__name__}. It was replaced by a stub.')
            print(f'- More precisely, {format_exc(limit=0).strip()}')
            return target_class.stub(self.name)


class Photospectrum(_PhotospectralObject):
    """
    Class to work with set of filters measurements (1D PhotospectralObject).

    Attributes:
    - `filter_system` (FilterSystem): instance of the class storing filter profiles
    - `nm` (np.ndarray): shortcut for filter_system.nm, the definition range
    - `br` (np.ndarray): array of "brightness" in energy density units (not a photon counter)
    - `sd` (np.ndarray): optional array of standard deviations
    - `name` (ObjectName): name as an instance of a class that stores its components
    """
    
    @staticmethod
    def stub(name=None) -> Self:
        """ Initializes an object in case of the data problems """
        return Photospectrum(FilterSystem.from_list(('Generic_Bessell.V',)), np.zeros(1), name=name)



class _Cube(_TrueColorToolsObject):
    """ Internal class for inheriting spatial data properties """
    
    def downscale(self, pixels_limit: int) -> Self:
        """ Brings the spatial resolution of the cube to approximately match the number of pixels """
        output = deepcopy(self)
        output.br = aux.spatial_downscaling(self.br, pixels_limit)
        output.sd = None
        if self.sd is not None:
            output.sd = aux.spatial_downscaling(self.sd, pixels_limit)
        return output
    
    @property
    def width(self):
        """ Returns horizontal spatial axis length """
        return self.shape[1]
    
    @property
    def hight(self):
        """ Returns vertical spatial axis length """
        return self.shape[2]


class SpectralCube(_SpectralObject, _Cube):
    """
    Class to work with an image of continuous spectra (3D SpectralObject).

    Attributes:
    - `nm` (np.ndarray): spectral axis, list of wavelengths in nanometers on a uniform grid
    - `br` (np.ndarray): array of "brightness" in energy density units (not a photon counter)
    - `sd` (np.ndarray): optional array of standard deviations
    - `name` (ObjectName): name as an instance of a class that stores its components
    - `width` (int): horizontal spatial axis length
    - `hight` (int): vertical spatial axis length
    """
    
    @staticmethod
    def stub(name=None) -> Self:
        """ Initializes an object in case of the data problems """
        return SpectralCube((555,), np.zeros((1, 1, 1)), name=name)
    
    @staticmethod
    @lru_cache(maxsize=1)
    def from_file(file: str) -> Self:
        """ Creates a SpectralCube object based on loaded data from the specified file """
        return SpectralCube.from_array(*ii.cube_reader(file))


class PhotospectralCube(_PhotospectralObject, _Cube):
    """
    Class to work with set of filters measurements (3D PhotospectralObject).

    Attributes:
    - `filter_system` (FilterSystem): instance of the class storing filter profiles
    - `nm` (np.ndarray): shortcut for filter_system.nm, the definition range
    - `br` (np.ndarray): array of "brightness" in energy density units (not a photon counter)
    - `sd` (np.ndarray): optional array of standard deviations
    - `name` (ObjectName): name as an instance of a class that stores its components
    - `width` (int): horizontal spatial axis length
    - `hight` (int): vertical spatial axis length
    """
    
    @staticmethod
    def stub(name=None) -> Self:
        """ Initializes an object in case of the data problems """
        return PhotospectralCube(FilterSystem.from_list(('Generic_Bessell.V',)), np.zeros(1, 1, 1), name=name)


#sun = Spectrum.from_file('spectra/files/CALSPEC/sun_reference_stis_002.fits') # W / (m² nm)
#test = FilterSystem.from_list(('Generic_Bessell.U', 'Generic_Bessell.B', 'Generic_Bessell.V'), name='test')
#v = get_filter('Generic_Bessell.V').to_scope(sun.nm)

#import matplotlib.pyplot as plt
#plt.plot(v.nm, v.br)
#plt.show()

#print((sun * v).nm)

#photospectrum = sun @ test
#print(photospectrum.br)
#print(v @ photospectrum)

#exit()
#print(test.standard_deviation())