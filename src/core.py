
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
from typing import Sequence, Callable
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
    def as_ObjectName(input):
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
    
    @property
    def ndim(self):
        """ Shortcut to get the number of dimensions """
        return self.br.ndim
    
    @property
    def nm_len(self):
        """ Returns the spectral axis length """
        return self.br.shape[0]
    
    @property
    def shape(self):
        """ Returns the spatial axes shape: number of filters or (width, hight) """
        return self.br.shape[1:]
    
    def scaled_at(self, where, how: int|float = 1, sd: int|float = None):
        """
        Returns a new object to fit the request brightness (1 by default)
        at specified filter profile or wavelength.
        """
        # TODO: uncertainty processing
        # TODO: problems with cubes?
        output = deepcopy(self)
        if isinstance(where, (str, int, float)):
            where = get_filter(where)
        current_br = self @ where
        if current_br == 0:
            return output
        return output * (how / current_br)
    
    def apply_linear_operator(self, operator: Callable, operand: int|float|np.ndarray):
        """
        Returns a new object of the same class transformed according to the linear operator.
        Operand is assumed to be a number or an array along the spectral axis.
        Linearity is needed because values and uncertainty are handled uniformly.
        """
        output = deepcopy(self)
        if isinstance(operand, np.ndarray) and self.nm_len == operand.size:
            # operand is an array with spectral axis size
            output.br = operator(output.br.T, operand).T
            if self.sd is not None:
                output.sd = operator(output.sd.T, operand).T
        else:
            # operand is a number or an array with spatial axis size
            output.br = operator(output.br, operand)
            if self.sd is not None:
                output.sd = operator(output.sd, operand)
        return output
    
    def __mul__(self, other: int|float|np.ndarray):
        if isinstance(other, (int, float, np.ndarray)):
            return self.apply_linear_operator(mul, other)
        return NotImplemented
    
    def __rmul__(self, other: int|float|np.ndarray):
        return self.__mul__(other)
    
    def __truediv__(self, other: int|float|np.ndarray):
        if isinstance(other, (int, float, np.ndarray)):
            return self.apply_linear_operator(truediv, other)
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
    """
    
    def __init__(self, nm: Sequence, br: Sequence, sd: Sequence = None, name: str|ObjectName = None) -> None:
        """
        It is assumed that the input wavelength grid can be trusted. If preprocessing is needed, see `SpectralObject.from_array`.
        There are no checks for negativity, since such spectra exist, for example, red CMF.

        Args:
        - `nm` (Sequence): spectral axis, list of wavelengths in nanometers on a uniform grid
        - `br` (Sequence): array of "brightness" in energy density units (not a photon counter)
        - `sd` (Sequence): optional array of standard deviations
        - `name` (str|ObjectName): name as a string or an instance of a class that stores its components
        """
        self.nm = np.asarray(nm, dtype='int16')
        self.br = np.asarray(br, dtype='float64')
        self.sd = None if sd is None else np.asarray(sd, dtype='float64')
        self.name = ObjectName.as_ObjectName(name)
        if np.any(np.isnan(self.br)):
            self.br = np.nan_to_num(self.br)
            print(f'# Note for the SpectralObject "{self.name}"')
            print(f'- NaN values detected during object initialization, they been replaced with zeros.')
    
    @staticmethod
    def from_array(nm: np.ndarray, br: np.ndarray, sd: np.ndarray = None, name: str|ObjectName = None):
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
                return target_class.stub(name)
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
            #if br.min() < 0:
            #    br = np.clip(br, 0, None)
            #    print(f'# Note for the {target_class_name} "{name}"')
            #    print(f'- Negative values detected while trying to create the object from array, they been replaced with zeros.')
            return target_class(nm, br, sd, name=name)
        except Exception:
            print(f'# Note for the {target_class_name} "{name}"')
            print(f'- Something unexpected happened while trying to create an object from the array. It was replaced by a stub.')
            print(f'- More precisely, {format_exc(limit=0).strip()}')
            return target_class.stub(name)
    
    def integrate(self) -> np.ndarray:
        """ Collapses the SpectralObject along the spectral axis into a two-dimensional image """
        return aux.integrate(self.br, nm_step)
    
    def normalize(self):
        """ Returns a new SpectralObject with each spectrum divided by its area """
        return self / self.integrate()
    
    def convert_from_photon_spectral_density(self):
        """
        Returns a new SpectralObject converted from photon spectral density
        to energy spectral density, using the fact that E = h c / λ.
        """
        return (self / self.nm).normalize()
    
    def convert_from_frequency_spectral_density(self):
        """
        Returns a new SpectralObject converted from frequency spectral density
        to energy spectral density, using the fact that f_λ = f_ν c / λ².
        """
        return (self / self.nm**2).normalize()
    
    def mean_spectrum(self):
        """ Returns the mean spectrum along the spatial axes """
        # TODO: add std
        match self.ndim:
            case 1:
                br = self.br
            case 2:
                br = np.mean(self.br, axis=1)
            case 3:
                br = np.mean(self.br, axis=(1, 2))
        return Spectrum(self.nm, br, name=self.name)
    
    def median_spectrum(self):
        """ Returns the median spectrum along the spatial axes """
        match self.ndim:
            case 1:
                br = self.br
            case 2:
                br = np.median(self.br, axis=1)
            case 3:
                br = np.median(self.br, axis=(1, 2))
        return Spectrum(self.nm, br, name=self.name)

    def mean_nm(self) -> float|np.ndarray[np.floating]:
        """ Returns mean wavelength or array of mean wavelengths """
        try:
            return np.average(aux.expand_1D_array(self.nm, self.shape), weights=self.br, axis=0)
        except ZeroDivisionError:
            print(f'# Note for the SpectralObject "{self.name}"')
            print(f'- Bolometric brightness is zero, the mean wavelength cannot be calculated. Returns 0 nm.')
            return 0.
    
    def sd_of_nm(self) -> np.ndarray[np.floating]:
        """ Returns uncorrected standard deviation or an array of uncorrected standard deviations """
        return np.sqrt(np.average((aux.expand_1D_array(self.nm, self.shape) - self.mean_nm())**2, weights=self.br, axis=0))
    
    def get_br_in_range(self, start: int, end: int) -> np.ndarray[np.floating]:
        """ Returns brightness values over a range of wavelengths (ends included!) """
        # TODO: round up to a multiple of 5
        return self.br[np.where((self.nm >= start) & (self.nm <= end))]
    
    def to_scope(self, scope: np.ndarray, crop: bool = False):
        """ Returns a new SpectralObject with a guarantee of definition on the requested scope """
        extrapolated = self.__class__(*aux.extrapolating(self.nm, self.br, scope, nm_step), name=self.name)
        if crop:
            start = max(extrapolated.nm[0], scope[0])
            end = min(extrapolated.nm[-1], scope[-1])
            extrapolated.br = extrapolated.get_br_in_range(start, end)
        return extrapolated
    
    def __matmul__(self, other):
        return other.__rmatmul__(self)
    
    def __rmatmul__(self, other):
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
        operand1 = other.to_scope(self.nm) # also reconstructs PhotospectralObj to SpectralObj
        operand2 = self.to_scope(other.nm)
        # Why Spectrum/FilterSystem is also extrapolated?
        # For the cases of bolometric albedo operations such as `Sun @ Mercury`.
        match operand1.ndim:
            case 1: # Spectrum or Photospectrum
                match operand2.ndim:
                    case 1: # Spectrum
                        return aux.integrate(operand1.br * operand2.br, nm_step)
                    case 2: # FilterSystem
                        br = aux.integrate((operand2.br.T * operand1.br).T, nm_step)
                        return Photospectrum(operand2, br, name=operand1.name)
            case 2: # FilterSystem
                print(f'# Note for the {operand1.__class__.__name__} "{operand1.name}"')
                print(f'- Convolution of a filter system makes no physical sense.')
            case 3: # SpectralCube or PhotospectralCube
                match operand2.ndim:
                    case 1: # Spectrum
                        return aux.integrate((operand1.br.T * operand2.br).T, nm_step)
                    case 2: # FilterSystem
                        br = np.empty((len(operand2), *operand1.shape))
                        for i in range(len(operand2)):
                            profile = operand2.br[:,i]
                            br[i] = aux.integrate((operand1.br.T * profile).T, nm_step)
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
    
    def __init__(self, nm: Sequence, br: Sequence, sd: Sequence = None,
                 name: str|ObjectName = None, photospectrum=None):
        """
        It is assumed that the input wavelength grid can be trusted. If preprocessing is needed, see `SpectralObject.from_array`.
        There are no checks for negativity, since such spectra exist, for example, red CMF.

        Args:
        - `nm` (Sequence): spectral axis, list of wavelengths in nanometers on a uniform grid
        - `br` (Sequence): array of "brightness" in energy density units (not a photon counter)
        - `sd` (Sequence): optional array of standard deviations
        - `name` (str|ObjectName): name as a string or an instance of a class that stores its components
        - `photospectrum` (Photospectrum): optional, way to store the pre-reconstructed data
        """
        super().__init__(nm, br, sd, name)
        self.photospectrum = photospectrum
    
    @staticmethod
    def stub(name=None):
        """ Initializes an object in case of the data problems """
        return Spectrum((555,), np.ones(1), name=name)
    
    @staticmethod
    @lru_cache(maxsize=32)
    def from_file(file: str, name: str|ObjectName = None):
        """ Creates a Spectrum object based on loaded data from the specified file """
        return Spectrum.from_array(*file_reader(file), name=name)
    
    @staticmethod
    def from_nm(nm_point: int|float):
        """
        Creates a point Spectrum on the uniform grid (normalized and with zeroed edges).
        If the input on the grid, returns a single-point spectrum. Two-point otherwise.
        Make sure you use the rectangle method for integration, otherwise it won't be equal to 1.
        """
        nm_point /= nm_step
        nm_point_int = int(nm_point)
        nm0 = nm_point_int * nm_step
        if nm_point == nm_point_int:
            nm = (nm0-nm_step, nm0, nm0+nm_step)
            br = (0., 1., 0.)
        else:
            proximity_factor = nm_point - nm_point_int
            nm = (nm0-nm_step, nm0, nm0+nm_step, nm0+nm_step*2)
            br = (0., 1.-proximity_factor, proximity_factor, 0.)
        return Spectrum(nm, np.array(br)/nm_step, name=f'{nm_point} nm')
    
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
            br = aux.irradiance(scope*doppler*grav, temperature)
        else:
            br = np.zeros(scope.size)
        return Spectrum(scope, br, name=f'BB with T={round(temperature)} K')
    
    def edges_zeroed(self):
        """
        Returns a new Spectrum object with zero brightness to the edges added.
        This is necessary to mitigate the consequences of abruptly cutting off filter profiles.
        """
        profile = deepcopy(self)
        #limit = profile.br.max() * 0.1 # adding point if an edge brightness higher than 10% of the peak
        # Now always adding zeroes because it affects on extrapolation and filter system
        if profile.br[0] != 0:
            profile.nm = np.append(profile.nm[0]-nm_step, profile.nm)
            profile.br = np.append(0., profile.br)
        if profile.br[-1] != 0:
            profile.nm = np.append(profile.nm, profile.nm[-1]+nm_step)
            profile.br = np.append(profile.br, 0.)
        return profile
    
    def to_scope(self, scope: np.ndarray, crop: bool = False):
        """ Returns a new Spectrum with a guarantee of definition on the requested scope """
        if self.photospectrum is None:
            extrapolated = super().to_scope(scope, crop)
        else:
            extrapolated = self.photospectrum.to_scope(scope, crop) # repeat reconstruction on a new scope
        return extrapolated
    
    def apply_linear_operator(self, operator: Callable, operand: int|float|np.ndarray):
        """
        Returns a new object of the same class transformed according to the linear operator.
        Operand is assumed to be a number or an array along the spectral axis.
        Linearity is needed because values and uncertainty are handled uniformly.
        """
        output = super().apply_linear_operator(operator, operand)
        if output.photospectrum is not None:
            output.photospectrum = operator(output.photospectrum, operand)
        return output
    
    def apply_spectral_element_wise_operation(self, operator: Callable, other: _SpectralObject) -> _SpectralObject:
        """
        Returns a new SpectralObject formed from element-wise operation with the Spectrum,
        such as multiplication or division.
        
        Element-wise are only possible with 1D SpectralObjects: other would produce 4D+ arrays,
        which most computers do not have enough memory for.

        Works only at the intersection of the spectral axes! If you need to extrapolate one axis
        to the range of another, use `SpectralObject.to_scope()`.
        """
        # TODO: uncertainty processing
        operand1, operand2 = (self, other) if self.ndim >= other.ndim else (other, self) # order is important for division
        start = max(operand1.nm[0], operand2.nm[0])
        end = min(operand1.nm[-1], operand2.nm[-1])
        if start > end: # `>` is needed to process operations with stub objects with no extra logs
            the_first = operand1.name
            the_second = operand2.name
            if operand1.nm[0] > operand2.nm[0]:
                the_first, the_second = the_second, the_first
            print(f'# Note for SpectralObject element-wise operation "{operator.__name__}"')
            print(f'- "{the_first}" ends on {end} nm and "{the_second}" starts on {start} nm.')
            print('- There is no intersection between the spectra. SpectralObject stub object was created.')
            return operand1.__class__.stub(operand1.name)
        else:
            br1 = operand1.get_br_in_range(start, end)
            br2 = operand2.get_br_in_range(start, end)
            return operand1.__class__(aux.grid(start, end, nm_step), operator(br1.T, br2).T, name=operand1.name)
    
    def apply_photospectral_element_wise_operation(self, operator: Callable, photospectrum_or_system):
        """
        Returns a new PhotospectralObject formed from element-wise operation with the Spectrum,
        such as multiplication or division.
        Note that element-wise also distort the effective filter profiles, but since we assume
        the filter system to be already in regular energy density units, they would not change.
        
        Element-wise are only possible with 1D SpectralObjects: other would produce 4D+ arrays,
        which most computers do not have enough memory for.
        """
        # TODO: uncertainty processing
        self_photospectrum = self @ photospectrum_or_system.filter_system
        output = operator(photospectrum_or_system, self_photospectrum.br)
        #distorted_profiles = operator(photospectrum_or_system.filter_system, self)
        #output.filter_system = distorted_profiles.normalize()
        return output
    
    def __mul__(self, other):
        if isinstance(other, _SpectralObject):
            return self.apply_spectral_element_wise_operation(mul, other)
        elif isinstance(other, _PhotospectralObject):
            return self.apply_photospectral_element_wise_operation(mul, other)
        else:
            return super().__mul__(other)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, _SpectralObject):
            return self.apply_spectral_element_wise_operation(truediv, other)
        elif isinstance(other, _PhotospectralObject):
            return self.apply_photospectral_element_wise_operation(truediv, other)
        else:
            return super().__truediv__(other)
    
    def __rtruediv__(self, other):
        return self.__truediv__(other)


@lru_cache(maxsize=32)
def get_filter(name: str|int|float) -> Spectrum:
    """
    Creates a scaled to the unit area (normalized) Spectrum object.
    Requires file name to be found in the `filters` folder to load profile
    or wavelength in nanometers to generate single-point profile.
    """
    if not isinstance(name, str) or name.isnumeric():
        # no need to normalize if integration by the rectangle method
        return Spectrum.from_nm(float(name))
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
    It supports len() to get the number of filters and getitem() to get a profile.

    Common logic: filters should be zeroed on the edges, so FilterSystem too.
    Such behavior is an indicator for the extrapolator.

    Attributes:
    - `nm` (np.ndarray): total wavelength range of the filter profiles
    - `br` (np.ndarray): matrix of the profiles with shape [len(nm), len(filters)]
    - `name` (ObjectName): name as an instance of a class that stores its components
    - `names` (tuple[ObjectName]): storage of the original filter names
    """
    
    def __init__(self, nm: Sequence, br: Sequence, sd: Sequence = None,
                 name: str|ObjectName = None, names: tuple[ObjectName] = ()):
        super().__init__(nm, br, sd, name)
        self.names = names
    
    @staticmethod
    def stub(name=None):
        """ Initializes an object in case of the data problems """
        return FilterSystem((555,), np.ones((1, 1)), name=name, names=(None))
    
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
        names = []
        for i, profile in enumerate(filters):
            if isinstance(profile, (str, int, float)):
                profile = get_filter(profile)
                filters[i] = profile
            min_arr.append(profile.nm[0])
            max_arr.append(profile.nm[-1])
            names.append(profile.name)
        # Matrix packing
        nm = aux.grid(min(min_arr), max(max_arr), nm_step)
        br = np.zeros((len(nm), len(filters)))
        for i, profile in enumerate(filters):
            br[np.where((nm >= min_arr[i]) & (nm <= max_arr[i])), i] = profile.br
        return FilterSystem(nm, br, name=ObjectName.as_ObjectName(name), names=tuple(names))
    
    def __iter__(self):
        """ Creates an iterator over the filters in the system """
        for i in range(len(self)):
            yield self[i]
    
    def __getitem__(self, index: int) -> Spectrum:
        """ Returns the filter profile with extra zeros trimmed off """
        profile = self.br[:, index]
        non_zero_indices = np.nonzero(profile)[0]
        start = non_zero_indices[0] - 1
        end = non_zero_indices[-1] + 2
        return Spectrum(self.nm[start:end], profile[start:end], name=self.names[index])
    
    def __len__(self) -> int:
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
        if (len_filters := len(filter_system)) != (len_br := self.br.shape[0]):
            print(f'# Note for the PhotospectralObject "{name}"')
            print(f'- Arrays of wavelengths and brightness do not match ({len_filters} vs {len_br}). PhotospectralCube stub object was created.')
            return self.stub(name)
        if self.sd is not None and (len_sd := self.sd.shape[0]) != len_br:
            print(f'# Note for the PhotospectralObject "{name}"')
            print(f'- Array of standard deviations do not match brightness array ({len_sd} vs {len_br}). Uncertainty was erased.')
            self.sd = None
        if np.any(np.isnan(self.br)):
            self.br = np.nan_to_num(self.br)
            print(f'# Note for the PhotospectralObject object "{self.name}"')
            print(f'- NaN values detected during object initialization, they been replaced with zeros.')
    
    @property
    def nm(self) -> np.ndarray[np.integer]:
        """ Returns the definition range of the filter system """
        nm0 = self.mean_nm()
        return aux.grid(nm0[0], nm0[-1], nm_step) 
        #return self.filter_system.nm    # TODO: use this line after new reconstruction algorithm!
    
    def convert_from_photon_spectral_density(self):
        """
        Returns a new PhotospectralObject converted from photon spectral density
        to energy spectral density, using the fact that E = h c / λ.
        """
        profiles = self.filter_system.normalize()
        scale_factors = (profiles / profiles.nm).integrate()
        return self * scale_factors
    
    def convert_from_frequency_spectral_density(self):
        """
        Returns a new PhotospectralObject converted from frequency spectral density
        to energy spectral density, using the fact that f_λ = f_ν c / λ².
        """
        profiles = self.filter_system.normalize()
        scale_factors = (profiles / profiles.nm**2).integrate()
        return self * scale_factors
    
    def mean_nm(self) -> np.ndarray[np.floating]:
        """ Returns an array of mean wavelengths for each filter """
        return self.filter_system.mean_nm()
    
    def to_scope(self, scope: np.ndarray, crop: bool = False) -> _SpectralObject: # TODO: use kriging here!
        """ Reconstructs a SpectralObject with inter- and extrapolated photospectrum data to fit the wavelength scope """
        match self.ndim:
            case 1:
                target_class = Spectrum
            case 3:
                target_class = SpectralCube
        try:
            nm0 = self.mean_nm()
            br0 = self.br
            if len(self.filter_system) == 1: # single-point PhotospectralObject support
                nm1, br1 = aux.extrapolating((nm0[0],), (br0[0],), scope, nm_step)
            else:
                if np.any(nm0[:-1] > nm0[1:]): # fast increasing check
                    order = np.argsort(nm0)
                    nm0 = nm0[order]
                    br0 = br0[order]
                nm1 = aux.grid(nm0[0], nm0[-1], nm_step)
                br1 = aux.interpolating(nm0, br0, nm1, nm_step)
                nm1, br1 = aux.extrapolating(nm1, br1, scope, nm_step)
            if crop:
                start = max(nm1[0], scope[0])
                end = min(nm1[-1], scope[-1])
                br1 = br1[np.where((nm1 >= start) & (nm1 <= end))]
            if isinstance(target_class, Spectrum):
                return target_class(nm1, br1, name=self.name, photometry=deepcopy(self))
            else:
                return target_class(nm1, br1, name=self.name)
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
    def stub(name=None):
        """ Initializes an object in case of the data problems """
        return Photospectrum(FilterSystem.from_list(('Generic_Bessell.B', 'Generic_Bessell.V')), np.ones(2), name=name)



class _Cube(_TrueColorToolsObject):
    """ Internal class for inheriting spatial data properties """
    
    def downscale(self, pixels_limit: int):
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
    def stub(name=None):
        """ Initializes an object in case of the data problems """
        return SpectralCube((555,), np.zeros((1, 1, 1)), name=name)
    
    @staticmethod
    @lru_cache(maxsize=1)
    def from_file(file: str):
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
    def stub(name=None):
        """ Initializes an object in case of the data problems """
        return PhotospectralCube(FilterSystem.from_list(('Generic_Bessell.B', 'Generic_Bessell.V')), np.ones((2, 1, 1)), name=name)
