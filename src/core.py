"""
Describes the main data storage classes and related functions.

Naming:
- ObjectName

Data:
- TrueColorToolsObject
- - SpectralObject
- - - Spectrum (1D)
- - - SpectralSquare (2D)
- - - - FilterSystem
- - - SpectralCube (3D)
- - PhotospectralObject
- - - Photospectrum (1D)
- - - PhotospectralSquare (2D)
- - - PhotospectralCube (3D)

Phase photometry:
- PhotometricModel
- - PhaseCoefficient
- - Exponentials
- - HG
- - HG1G2
- - Hapke

Database:
- EmittingBody
- ReflectingBody

Color:
- ColorSystem
- ColorObject
- - ColorPoint (1D)
- - ColorLine (2D)
- - ColorImage (3D)
"""

from copy import deepcopy
from typing import Sequence, Callable, Self
from pathlib import Path
from functools import lru_cache
from traceback import format_exc
from PIL import Image
from scipy.optimize import minimize
from scipy.linalg import solve
import numpy as np

from src.data_import import file_reader
import src.auxiliary as aux
import src.strings as tr
import src.data_import as di
import src.image_import as ii



# ------------ Naming Section ------------

class ObjectName:
    """
    Class to work with a (celestial object) name.
    It parses the original string (raw_name) and stores the components:
    - index
    - name(lang)
    - note(lang)
    - info(lang)
    - reference
    """

    unnamed_count = 0 # class attribute to track the number of unnamed objects

    def __init__(self, name: str = None):
        """
        Initializes the ObjectName with name parsing.
        The template is `(index) name: note (info) | reference`.
        If no name is specified, a numbered unnamed object will be created.
        """
        self.index = self._note_en = self._info_en = self.reference = None
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
                self.index = self.formatting_provisional_designation(index[1:].strip())
            if '(' in name: # stellar spectral type or something else
                info, name = name[::-1].split('(', 1) # getting the last bracket
                name = name[::-1] # reversing back
                self._info_en = self.formatting_provisional_designation(info[::-1].split(')', 1)[0].strip())
            if ':' in name: # note
                name, note = name.split(':', 1)
                self._note_en = self.formatting_provisional_designation(note.strip())
            if '/' in name: # comet name
                # the last "if" because "/" may encountered in info or notes
                index, name = name.split('/', 1)
                self.index = index.strip() + '/'
            self._name_en = self.formatting_provisional_designation(name.strip())
    
    def name(self, lang: str = 'en') -> str:
        """ Returns the name in the specified language """
        return self._name_en if lang == 'en' else self.translate(self._name_en, tr.names, lang)
    
    def note(self, lang: str = 'en') -> str:
        """ Returns the note in the specified language """
        if self._note_en:
            return self._note_en if lang == 'en' else self.translate(self._note_en, tr.notes, lang)
        else:
            return None
    
    def info(self, lang: str = 'en') -> str:
        """ Returns the info in the specified language """
        if self._info_en:
            return self._info_en if lang == 'en' else self.translate(self._info_en, tr.names, lang)
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
        if self._info_en:
            name = f'{name} ({self.info(lang)})'
        if self.reference:
            name = f'{name} [{self.reference}]'
        return name
    
    @staticmethod
    def formatting_provisional_designation(string: str):
        """
        Checks if the string contains a provisional designation and subscripts the last number
        (of previous letter alphabetic cycles).

        See https://www.minorplanetcenter.net/iau/info/DesDoc.html
        """
        words = string.split()
        if len(words) > 1:
            for i, word in enumerate(words):
                if i+1 != len(words) and word[-4:].isnumeric() and word[-4:-2] in ('19', '20'):
                    letters = words[i+1]
                    if 2 < len(letters) < 7 and letters[:2].isalpha() and letters[2:].isnumeric():
                        words[i+1] = letters[:2] + aux.subscript(letters[2:])
        return ' '.join(words)
    
    @staticmethod
    def translate(target: str, translations: dict[str, dict[str, str]], lang: str) -> str:
        """ Searches part of the target string to be translated and replaces it with translation """
        for original, translation in translations.items():
            if target.startswith(original) or target.endswith(original) or original in target.split():
                if lang in translation:
                    target = target.replace(original, translation[lang])
                break
        return target
    
    @staticmethod
    def as_ObjectName(input):
        """ Guaranteed to return an object of the given class, even if the input may have already been one """
        return input if isinstance(input, ObjectName) else ObjectName(input)
    
    def __hash__(self) -> int:
        """ Returns the hash value based on the object's raw name """
        return hash(self.raw_name)
    
    def __eq__(self, other) -> bool:
        """ Checks equality with another ObjectName instance """
        if isinstance(other, ObjectName):
            return self.raw_name == other.raw_name
        return False
    
    def __str__(self) -> str:
        return self()
    
    def __repr__(self) -> str:
        output = 'ObjectName('
        if self.index:
            output += f'index={self.index}, '
        if self._name_en:
            output += f'name={self._name_en}, '
        if self._note_en:
            output += f'note={self._note_en}, '
        if self._info_en:
            output += f'info={self._info_en}, '
        if self.reference:
            output += f'reference={self.reference}, '
        return output[:-2] + ')'


# ------------ Data Section ------------

# TCT was written in an effort to work not only with the optical range, but with any, depending on the data.
# But too long and heterogeneous FITS files demanded to set the upper limit of the range to mid-wavelength infrared (3 μm).
nm_red_limit = 3000 # nm
# Actually, dtype=uint16 is used to store wavelength. It's possible to set the limit to 65535 nm with no compression,
# (and up to 327 675 nm with compression by 5 nm step, but it was not implemented).

# For the sake of simplifying work with the spectrum, its discretization step is fixed.
nm_step = 5 # nm

# To calculate color, it is necessary to achieve a definition of the spectrum in the visible range.
# Boundaries have been defined based on the CMF (color matching functions) used, but can be any.
visible_range = np.arange(390, 780, nm_step) # nm

# When processing images through spectral cubes, performance is prioritized, and uncertainty is not saved (yet).
# Therefore it is disabled by default.
ignore_sd_for_cubes = True


class _TrueColorToolsObject:
    """ Internal class for inheriting spectral data properties """
    name = ''
    nm = np.empty(0)
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
        """ Returns the spatial axes shape: number of filters or (width, height) """
        return self.br.shape[1:]
    
    @staticmethod
    def stub(name=None):
        """ Initializes an object in case of the data problems """
        raise NotImplementedError('Implemented in the inherited classes of SpectralObject and PhotospectralObject.')
    
    def convert_from_photon_spectral_density(self):
        """
        Returns a new TrueColorToolsObject converted from photon spectral density
        to energy spectral density, using the fact that E = h c / λ.
        """
        raise NotImplementedError('Implemented in the classes SpectralObject and PhotospectralObject.')
    
    def convert_from_frequency_spectral_density(self):
        """
        Returns a new TrueColorToolsObject converted from frequency spectral density
        to energy spectral density, using the fact that f_λ = f_ν c / λ².
        """
        raise NotImplementedError('Implemented in classes SpectralObject and PhotospectralObject.')
    
    def define_on_range(self, nm_arr: np.ndarray, crop: bool = False):
        """ Returns a new SpectralObject with a guarantee of definition on the requested wavelength array """
        raise NotImplementedError('Implemented in classes SpectralObject and PhotospectralObject.')
    
    def scaled_at(self, where, how: int|float = 1, sd: int|float = None):
        """
        Returns a new object that matches the query brightness (1 by default)
        at the specified filter profile or wavelength.
        """
        output = deepcopy(self)
        if isinstance(where, str|int|float):
            where = get_filter(where)
        current_br, sd = self @ where
        if current_br == 0:
            return output
        if isinstance(how, Sequence):
            how = how[0] # likely a [value, std]
        return output * (how / current_br)
    
    def apply_element_wise_operation(self, operand: Self, br_handling: Callable, sd_handling: Callable) -> Self:
        """ Returns a new object formed from element-wise operation """
        raise NotImplementedError('Implemented in classes SpectralObject and PhotospectralObject, use them instead.')
    
    def apply_scalar_operation(self, operand, br_handling: Callable, sd_handling: Callable) -> Self:
        """
        Returns a new object of the same class transformed according to the operator.
        Operand is assumed to be a number or an array along the spectral axis.
        """
        output = deepcopy(self)
        output.br = br_handling(self.br, operand)
        output.sd = sd_handling(self.br, self.sd, operand, None)
        return output
    
    def __add__(self, other) -> Self:
        if isinstance(other, _TrueColorToolsObject):
            return self.apply_element_wise_operation(other, aux.add_br, aux.add_sd)
        else:
            return self.apply_scalar_operation(other, aux.add_br, aux.add_sd)
    
    def __sub__(self, other) -> Self:
        if isinstance(other, _TrueColorToolsObject):
            return self.apply_element_wise_operation(other, aux.sub_br, aux.sub_sd)
        else:
            return self.apply_scalar_operation(other, aux.sub_br, aux.sub_sd)
    
    def __mul__(self, other) -> Self:
        if isinstance(other, _TrueColorToolsObject):
            return self.apply_element_wise_operation(other, aux.mul_br, aux.mul_sd)
        else:
            return self.apply_scalar_operation(other, aux.mul_br, aux.mul_sd)
    
    def __truediv__(self, other) -> Self:
        if isinstance(other, _TrueColorToolsObject):
            return self.apply_element_wise_operation(other, aux.div_br, aux.div_sd)
        else:
            return self.apply_scalar_operation(other, aux.div_br, aux.div_sd)
    
    def __matmul__(self, other: Self):
        """
        Implementation of convolution (in the meaning of synthetic photometry).
        If necessary, extrapolates over the wavelength interval of the second operand.

        Only 8 convolution options make physical sense:
        - Spectrum @ Spectrum                -> value, std
        - Spectrum @ FilterSystem            -> Photospectrum
        - SpectralSquare @ Spectrum          -> value array, std array
        - SpectralSquare @ FilterSystem      -> PhotospectralSquare
        - SpectralCube @ Spectrum            -> value image, std image
        - SpectralCube @ FilterSystem        -> PhotospectralCube
        - Photospectrum @ Spectrum           -> value, std
        - Photospectrum @ FilterSystem       -> Photospectrum
        - PhotospectralSquare @ Spectrum     -> value array, std array
        - PhotospectralSquare @ FilterSystem -> PhotospectralSquare
        - PhotospectralCube @ Spectrum       -> value image, std image
        - PhotospectralCube @ FilterSystem   -> PhotospectralCube
        """
        if isinstance(other, _SpectralObject) and other.is_edges_zeroed():
            # No extrapolation is required for a filter-like object
            operand1 = self.define_on_range(other.nm, crop=True)
            operand2 = other.define_on_range(other.nm, crop=True)
        elif isinstance(self, _SpectralObject) and self.is_edges_zeroed():
            # No extrapolation is required for a filter-like object
            operand1 = other.define_on_range(self.nm, crop=True)
            operand2 = self.define_on_range(self.nm, crop=True)
        else:
            # For the cases of bolometric albedo operations such as `Sun @ Mercury`.
            operand1 = other.define_on_range(self.nm, crop=False)
            operand2 = self.define_on_range(other.nm, crop=False)
        # other.define_on_range() reconstructed the PhotospectralObj to a some SpectralObj, so 4 options left:
        match (operand1, operand2):
            case (_, Spectrum()):
                br = aux.integrate(aux.mul_br(operand1.br, operand2.br), nm_step)
                sd = aux.mul_sd(operand1.br, operand1.sd, operand2.br, operand2.sd)
                if sd is not None:
                    sd = aux.integrate(sd, nm_step)
                return br, sd
            case (Spectrum(), FilterSystem()):
                br = aux.integrate(aux.mul_br(operand1.br, operand2.br), nm_step)
                sd = aux.mul_sd(operand1.br, operand1.sd, operand2.br, operand2.sd)
                if sd is not None:
                    sd = aux.integrate(sd, nm_step)
                return Photospectrum(operand2, br, sd, name=operand1.name)
            case (SpectralSquare(), FilterSystem()):
                br = aux.integrate(operand1.br[:, :, np.newaxis] * operand2.br[:, np.newaxis, :], nm_step).T
                # TODO: uncertainty processing
                return PhotospectralSquare(operand2, br, name=operand1.name)
            case (SpectralCube(), FilterSystem()):
                # A loop-less implementation would require a 4D array,
                # which most computers do not have enough memory for.
                br = np.empty((len(operand2), *operand1.shape))
                #for i, profile in enumerate(operand2):
                for i in range(len(operand2)):
                    profile = operand2.br[:,i]
                    br[i] = aux.integrate((operand1.br.T * profile).T, nm_step)
                # TODO: uncertainty processing
                return PhotospectralCube(operand2, br, name=operand1.name)
            case _:
                return NotImplemented
    
    def __hash__(self) -> int:
        """ Returns the hash value based on the object's name """
        return hash(self.name)
    
    def __eq__(self, other: Self) -> bool:
        """ Checks equality with another TrueColorToolsObject instance """
        if isinstance(other, _TrueColorToolsObject):
            return np.array_equal(self.nm, other.nm) and np.array_equal(self.br, other.br)
        return False
    
    #def __repr__(self) -> str:
    #    output = f'{self.__class__.__name__}('
    #    if len(self.nm > 3):
    #        output += f'nm=[{self.nm[1]}, {self.nm[2]}, ..., {self.nm[-1]}], '
    #    else:
    #        output += f'nm=[{self.nm}], '
    #    if len(self.br > 3):
    #        output += f'br=[{self.br[1]:.3f}, {self.br[2]:.3f}, ..., {self.br[-1]:.3f}], '
    #    else:
    #        output += f'br=[{self.br}], '
    #    return output[:-2] + ')'


class _SpectralObject(_TrueColorToolsObject):
    """
    Internal parent class for Spectrum (1D), SpectralSquare (2D) and SpectralCube (3D).
    The first index of the "brightness" array iterates over the spectral axis.

    Attributes:
    - `nm` (np.ndarray): spectral axis, list of wavelengths in nanometers on a uniform grid
    - `br` (np.ndarray): array of "brightness" in energy density units (not a photon counter)
    - `sd` (np.ndarray): optional array of standard deviations
    - `name` (ObjectName): name as an instance of a class that stores its components
    """
    
    def __init__(self, ndim: int, nm: Sequence, br: Sequence, sd: Sequence = None, name: str|ObjectName = None):
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
        if ndim != self.br.ndim:
            raise ValueError(f'Expected brightness array of dimension {ndim}, not {self.br.ndim}')
        if sd is None or (ignore_sd_for_cubes and ndim == 3):
            self.sd = None
        else:
            self.sd = np.asarray(sd, dtype='float64')
        self.name = ObjectName.as_ObjectName(name)
        if np.any(np.isnan(self.br)):
            self.br = np.nan_to_num(self.br)
            print(f'# Note for the SpectralObject "{self.name}"')
            print(f'- NaN values detected during object initialization, they been replaced with zeros.')
    
    @classmethod
    def from_array(cls, nm: np.ndarray, br: np.ndarray, sd: np.ndarray = None, name: str|ObjectName = None):
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
        if ignore_sd_for_cubes and isinstance(cls, _Cube):
            sd = None
        if sd is not None:
            sd = np.asarray(sd, dtype='float64')
        name = ObjectName.as_ObjectName(name)
        target_class_name = cls.__name__
        try:
            if (len_nm := nm.size) != (len_br := br.shape[0]):
                print(f'# Note for the {target_class_name} "{name}"')
                print(f'- Arrays of wavelengths and brightness do not match ({len_nm} vs {len_br}). {target_class_name} stub object was created.')
                return cls.stub(name)
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
                mask = np.where(nm < nm_red_limit + nm_step) # with reserve to be averaged
                nm = nm[mask]
                br = br[mask]
                if sd is not None:
                    sd = sd[mask]
            if np.any((diff := np.diff(nm)) != nm_step): # if not an uniform 5 nm grid
                nm_uniform = aux.grid(nm[0], nm[-1], nm_step)
                if diff.mean() >= nm_step: # interpolation, increasing resolution
                    br = aux.interpolating(nm, br, nm_uniform, nm_step)
                    if sd is not None:
                        sd = aux.interpolating(nm, sd, nm_uniform, nm_step)
                else: # decreasing resolution if step less than 5 nm
                    br, sd = aux.spectral_downscaling(nm, br, sd, nm_uniform, nm_step)
                nm = nm_uniform
            #if br.min() < 0:
            #    br = np.clip(br, 0, None)
            #    print(f'# Note for the {target_class_name} "{name}"')
            #    print(f'- Negative values detected while trying to create the object from array, they been replaced with zeros.')
            return cls(nm, br, sd, name=name)
        except Exception:
            print(f'# Note for the {target_class_name} "{name}"')
            print(f'- Something unexpected happened while trying to create an object from the array. It was replaced by a stub.')
            print(f'- More precisely, {format_exc(limit=0).strip()}')
            return cls.stub(name)
    
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
        scale_factors = 1 / self.nm / self.nm # squaring nm will overflow uint16
        return (self / scale_factors).normalize()
    
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
        """ Returns the weighted average wavelength or an array of wavelengths """
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
        """ Returns standard deviation values over a range of wavelengths (ends included!) """
        # TODO: round the input up to a multiple of 5
        return self.br[(self.nm >= start) & (self.nm <= end)]
    
    def get_sd_in_range(self, start: int, end: int) -> np.ndarray[np.floating]:
        """ Returns standard deviation values over a range of wavelengths (ends included!) """
        if self.sd is None:
            return None
        else:
            # TODO: round the input up to a multiple of 5
            return self.sd[(self.nm >= start) & (self.nm <= end)]
    
    def define_on_range(self, nm_arr: np.ndarray, crop: bool = False):
        """ Returns a new SpectralObject with a guarantee of definition on the requested wavelength array """
        extrapolated = self.__class__(*aux.extrapolating(self.nm, self.br, self.sd, nm_arr, nm_step), name=self.name)
        if crop:
            start = max(extrapolated.nm[0], nm_arr[0])
            end = min(extrapolated.nm[-1], nm_arr[-1])
            extrapolated.br = extrapolated.get_br_in_range(start, end)
            extrapolated.sd = extrapolated.get_sd_in_range(start, end)
            extrapolated.nm = aux.grid(start, end, nm_step)
        return extrapolated
    
    def is_edges_zeroed(self) -> bool:
        """ Checks that the first and last brightness entries on the spectral axis are zero """
        return np.all(self.br[0] == 0) and np.all(self.br[-1] == 0)
    
    def apply_element_wise_operation(self, other: _TrueColorToolsObject, br_handling: Callable, sd_handling: Callable) -> Self:
        """
        Returns a new SpectralObject formed from element-wise operation between SpectralObjects
        of the same nature or with a Spectrum.

        Only works at the intersection of the spectral axes! If you need to extrapolate one axis
        to the range of another, use the `define_on_range()` method.
        """
        if isinstance(other, _SpectralObject):
            higher_dim = (self, other)[self.ndim < other.ndim]
            start = max(self.nm[0], other.nm[0])
            end = min(self.nm[-1], other.nm[-1])
            if start > end: # `>` is needed to process operations with stub objects with no extra logs
                the_first = other.name
                the_second = other.name
                if self.nm[0] > other.nm[0]:
                    the_first, the_second = the_second, the_first
                print(f'# Note for SpectralObject element-wise operation "{br_handling.__name__}"')
                print(f'- "{the_first}" ends on {end} nm and "{the_second}" starts on {start} nm.')
                print('- There is no intersection between the spectra. SpectralObject stub object was created.')
                return higher_dim.__class__.stub(self.name)
            else:
                br1 = self.get_br_in_range(start, end)
                br2 = other.get_br_in_range(start, end)
                br = br_handling(br1, br2)
                sd = sd_handling(br1, self.get_sd_in_range(start, end), br2, other.get_sd_in_range(start, end))
                return higher_dim.__class__(aux.grid(start, end, nm_step), br, sd, name=higher_dim.name)
        else:
            return NotImplemented


class Spectrum(_SpectralObject):
    """
    Class to work with a single spectrum (1D SpectralObject).

    Attributes:
    - `nm` (np.ndarray): spectral axis, list of wavelengths in nanometers on a uniform grid
    - `br` (np.ndarray): array of "brightness" in energy density units (not a photon counter)
    - `sd` (np.ndarray): optional array of standard deviations
    - `name` (ObjectName): name as an instance of a class that stores its components
    - `photospectrum` (Photospectrum): optional, way to store the pre-reconstructed data
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
        super().__init__(1, nm, br, sd, name)
        self.photospectrum: Photospectrum = photospectrum
    
    @staticmethod
    def stub(name=None):
        """ Initializes an object in case of the data problems """
        return Spectrum((555,), np.zeros(1), name=name)
    
    @staticmethod
    @lru_cache(maxsize=32)
    def from_file(file: str, name: str|ObjectName = None):
        """ Creates a Spectrum object based on loaded data from the specified file """
        spectrum = Spectrum.from_array(*file_reader(file), name=name)
        if 'p' in Path(file).suffix.lower():
            spectrum = spectrum.convert_from_photon_spectral_density()
        return spectrum
    
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
    def from_spectral_lines(nm: Sequence, br: Sequence, sd: Sequence = None, name: str|ObjectName = None):
        """
        Creates an emission spectrum from the spectral lines wavelength and brightness lists.

        Args:
        - `nm` (Sequence): list of wavelengths in nanometers
        - `br` (Sequence): array of "brightness" in energy density units (not a photon counter)
        - `sd` (Sequence): optional array of standard deviations
        - `name` (str|ObjectName): name as a string or an instance of a class that stores its components
        """
        nm = np.array(nm) # numpy decides int or float
        order = np.argsort(nm)
        nm = nm[order]
        br = np.array(br, dtype='float64')[order]
        if sd is not None:
            sd = np.array(sd, dtype='float64')[order]
        spectral_lines = tuple(Spectrum.from_nm(a) * b for a, b in zip(nm, br))
        nm = aux.grid(spectral_lines[0].nm[0], spectral_lines[-1].nm[-1], nm_step)
        output: Spectrum = spectral_lines[0].define_on_range(nm)
        for line in spectral_lines[1:]:
            output += line.define_on_range(nm)
        output.name = ObjectName.as_ObjectName(name)
        return output
    
    @staticmethod
    def from_blackbody_redshift(nm_arr: np.ndarray, temperature: int|float, velocity=0., vII=0.):
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
            br = aux.irradiance(nm_arr*doppler*grav, temperature)
        else:
            br = np.zeros(nm_arr.size)
        return Spectrum(nm_arr, br, name=f'BB with T={round(temperature)} K')
    
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
    
    def define_on_range(self, nm_arr: np.ndarray, crop: bool = False):
        """ Returns a new Spectrum with a guarantee of definition on the requested wavelength array """
        if self.photospectrum is None:
            extrapolated = super().define_on_range(nm_arr, crop)
        else:
            # Repeating the spectral reconstruction on the new wavelength range
            extrapolated = self.photospectrum.define_on_range(nm_arr, crop)
        return extrapolated
    
    def apply_scalar_operation(self, operand, br_handling: Callable, sd_handling: Callable):
        """
        Returns a new object of the same class transformed according to the linear operator.
        Operand is assumed to be a number or an array along the spectral axis.
        Linearity is needed because values and uncertainty are handled uniformly.
        """
        output = super().apply_scalar_operation(operand, br_handling, sd_handling)
        if output.photospectrum is not None:
            output.photospectrum = output.photospectrum.apply_scalar_operation(operand, br_handling, sd_handling)
        return output


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


class _Square(_TrueColorToolsObject):
    """ Internal class for inheriting spatial data properties """
    
    @property
    def size(self):
        """ Returns the spatial axis length """
        return self.shape[0]
    
    def __len__(self) -> int:
        """ Returns the spatial axis length """
        return self.size
    
    def __getitem__(self, item: slice):
        """ Returns the spatial axis slice """
        if isinstance(item, slice):
            output = deepcopy(self)
            output.br = output.br[:,item]
            output.sd = None if output.sd is None else output.sd[:,item]
            return output


class SpectralSquare(_SpectralObject, _Square):
    """
    Class to work with a line of continuous spectra (2D SpectralObject).

    Attributes:
    - `nm` (np.ndarray): spectral axis, list of wavelengths in nanometers on a uniform grid
    - `br` (np.ndarray): array of "brightness" in energy density units (not a photon counter)
    - `sd` (np.ndarray): optional array of standard deviations
    - `name` (ObjectName): name as an instance of a class that stores its components
    - `size` (int): spatial axis length
    """

    def __init__(self, nm: Sequence, br: Sequence, sd: Sequence = None, name: str | ObjectName = None):
        super().__init__(2, nm, br, sd, name)
    
    @staticmethod
    def stub(name=None):
        """ Initializes an object in case of the data problems """
        return SpectralSquare((555,), np.zeros((1, 1)), name=name)


class FilterSystem(SpectralSquare):
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
    - `size` (int): spatial axis length
    """
    
    def __init__(self, nm: Sequence, br: Sequence, sd: Sequence = None,
                 name: str|ObjectName = None, names: tuple[ObjectName] = ()):
        super().__init__(nm, br, sd, name)
        self.names = names
    
    @staticmethod
    def stub(name=None):
        """ Initializes an object in case of the data problems """
        return FilterSystem((555,), np.zeros((1, 1)), name=name, names=(None,))
    
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
            if isinstance(profile, str|int|float):
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
        return FilterSystem(nm, br, name=name, names=tuple(names))
    
    def __iter__(self):
        """ Creates an iterator over the filters in the system """
        for i in range(len(self)):
            yield self[i]
    
    @lru_cache(maxsize=32)
    def __getitem__(self, index: int) -> Spectrum:
        """ Returns the filter profile with extra zeros trimmed off """
        if isinstance(index, int):
            profile = self.br[:, index]
            non_zero_indices = np.nonzero(profile)[0]
            start = non_zero_indices[0] - 1
            end = non_zero_indices[-1] + 2
            return Spectrum(self.nm[start:end], profile[start:end], name=self.names[index])


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
    
    def flatten(self):
        """ Returns a (photo)spectral square with linearized spatial axis """
        br = self.br.reshape(self.nm_len, self.size)
        sd = None if self.sd is None else self.br.reshape(self.nm_len, self.size)
        if isinstance(self, _SpectralObject):
            return SpectralSquare(self.nm, br, sd, self.name)
        elif isinstance(self, _PhotospectralObject):
            return PhotospectralSquare(self.filter_system, br, sd, self.name)
    
    @property
    def width(self):
        """ Returns horizontal spatial axis length """
        return self.shape[0]
    
    @property
    def height(self):
        """ Returns vertical spatial axis length """
        return self.shape[1]
    
    @property
    def size(self):
        """ Returns the number of pixels """
        return self.width * self.height


class SpectralCube(_SpectralObject, _Cube):
    """
    Class to work with an image of continuous spectra (3D SpectralObject).

    Attributes:
    - `nm` (np.ndarray): spectral axis, list of wavelengths in nanometers on a uniform grid
    - `br` (np.ndarray): array of "brightness" in energy density units (not a photon counter)
    - `sd` (np.ndarray): optional array of standard deviations
    - `name` (ObjectName): name as an instance of a class that stores its components
    - `width` (int): horizontal spatial axis length
    - `height` (int): vertical spatial axis length
    - `size` (int): number of pixels
    """

    def __init__(self, nm: Sequence, br: Sequence, sd: Sequence = None, name: str | ObjectName = None):
        super().__init__(3, nm, br, sd, name)
    
    @staticmethod
    def stub(name=None):
        """ Initializes an object in case of the data problems """
        return SpectralCube((555,), np.zeros((1, 1, 1)), name=name)
    
    @staticmethod
    def from_file(file: str):
        """ Creates a SpectralCube object based on loaded data from the specified file """
        return SpectralCube.from_array(*ii.cube_reader(file))


class _PhotospectralObject(_TrueColorToolsObject):
    """
    Internal parent class for Photospectrum (1D), PhotospectralSquare (2D) and PhotospectralCube (3D).

    Attributes:
    - `filter_system` (FilterSystem): instance of the class storing filter profiles
    - `nm` (np.ndarray): shortcut for filter_system.nm, the definition range
    - `br` (np.ndarray): array of "brightness" in energy density units (not a photon counter)
    - `sd` (np.ndarray): optional array of standard deviations
    - `name` (ObjectName): name as an instance of a class that stores its components
    """
    
    def __init__(self, ndim: int, filter_system: FilterSystem, br: Sequence, sd: Sequence = None, name: str|ObjectName = None):
        """
        Args:
        - `filter_system` (FilterSystem): instance of the class storing filter profiles
        - `br` (Sequence): array of "brightness" in energy density units (not a photon counter)
        - `sd` (Sequence): optional array of standard deviations
        - `name` (str|ObjectName): name as a string or an instance of a class that stores its components
        """
        self.br = np.asarray(br, dtype='float64')
        if ndim != self.br.ndim:
            raise ValueError(f'Expected brightness array of dimension {ndim}, not {self.br.ndim}')
        if not isinstance(filter_system, FilterSystem):
            raise ValueError('`filter_system` argument is not a FilterSystem instance')
        self.filter_system = filter_system
        if sd is None or (ignore_sd_for_cubes and ndim == 3):
            self.sd = None
        else:
            self.sd = np.asarray(sd, dtype='float64')
        self.name = ObjectName.as_ObjectName(name)
        if (len_filters := len(filter_system)) != (len_br := self.br.shape[0]):
            raise ValueError(f'Arrays of wavelengths and brightness do not match ({len_filters} vs {len_br})')
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
        return self.filter_system.nm
    
    def convert_from_photon_spectral_density(self):
        """
        Returns a new PhotospectralObject converted from photon spectral density
        to energy spectral density, using the fact that E = h c / λ.
        """
        profiles = self.filter_system.normalize()
        scale_factors = (profiles / profiles.nm).integrate()
        return self * (scale_factors / scale_factors.mean())
    
    def convert_from_frequency_spectral_density(self):
        """
        Returns a new PhotospectralObject converted from frequency spectral density
        to energy spectral density, using the fact that f_λ = f_ν c / λ².
        """
        profiles = self.filter_system.normalize()
        scale_factors = (profiles / profiles.nm / profiles.nm).integrate() # squaring nm will overflow uint16
        return self * (scale_factors / scale_factors.mean())
    
    def define_on_range(self, nm_arr: np.ndarray, crop: bool = False) -> _SpectralObject:
        """
        Reconstructs a SpectralObject from photospectral data to fit the wavelength array.

        Interpolation is not used because it is not a solution to the inverse ill-posed problem
        (i.e., looking at the spectrum through the filters does not give exactly the original photometry).

        The function uses the Tikhonov regularization method, with a combination of first-order
        and second-order differential operators for the Tikhonov matrix.
        That is, it tries to minimize height variations and curvature in the spectrum.
        
        Confidence bands for spectral squares and cubes are not computed,
        even if possible, to save computational resources.
        """
        match self.ndim:
            case 1:
                target_class = Spectrum
            case 2:
                target_class = SpectralSquare
            case 3:
                target_class = SpectralCube
        try:
            nm0 = self.filter_system.mean_nm()
            br0 = self.br
            sd0 = None if ignore_sd_for_cubes and self.ndim == 3 else self.sd
            sd1 = None
            if len(self.filter_system) == 1: # single-point PhotospectralObject support
                nm1, br1 = aux.extrapolating(nm0, br0, sd0, nm_arr, nm_step)
            else:
                filter_system = self.filter_system.define_on_range(nm_arr)
                nm1 = filter_system.nm
                T = filter_system.br.T * nm_step
                #L = aux.smoothness_matrix(T.shape[1], order=2)
                #A = T.T @ T + 0.05 * L.T @ L
                L1 = aux.smoothness_matrix(T.shape[1], order=1)
                L2 = aux.smoothness_matrix(T.shape[1], order=2)
                # TODO: research on some known spectra to find which ratios (0.005, 1) fit best
                A = aux.covar_matrix(T) + 0.005 * aux.covar_matrix(L1) + 1 * aux.covar_matrix(L2)
                if self.ndim == 3:
                    # scipy supports batch mode for 2d arrays, but not for 3D arrays
                    br0 = br0.reshape(T.shape[0], -1)
                b = T.T @ br0
                br1 = solve(A, b) # x1.5 faster than np.linalg.inv(A) @ b
                if self.ndim == 3:
                    # Reshape spectral cube back from square
                    br1 = br1.reshape(-1, *self.br.shape[1:])
                if self.ndim == 1 and br1.min() < 0:
                    # To avoid negative spectra, a lower bound is set and iterative
                    # optimization is performed using quadratic programming methods.
                    # The processing speed drops by a factor of about five,
                    # so the use is blocked for spectral squares and cubes:
                    # background noise near zero can be most of the pixels.
                    def objective(Y):
                        # Tikhonov-regularized quadratic objective: 0.5 * Y^T A Y - b^T Y
                        return 0.5 * Y @ A @ Y - b @ Y
                    def gradient(Y):
                        # Gradient of the objective
                        return A @ Y - b
                    bounds = ((0, None) for _ in range(A.shape[1]))
                    result = minimize(
                        fun=objective,
                        x0=np.maximum(br1, 0),
                        jac=gradient,
                        bounds=bounds,
                        method='L-BFGS-B',
                    )
                    if not result.success:
                        raise ValueError(f'Optimization failed: {result.message}')
                    br1 = result.x
                if self.ndim == 1 and sd0 is not None:
                    # Measurement confidence band calculation
                    # Confidence bands for spectral squares and cubes are not computed to save computational resources
                    A_inv = np.linalg.inv(A)
                    sd1 = np.sqrt(np.diag(A_inv @ T.T @ np.diag(sd0**2) @ T @ A_inv))
                    # An attempt to account for the sensitivity confidence band of the method
                    sd1 = np.sqrt(sd1**2 + (0.01 * np.median(br1))**2 * np.diag(A_inv))
                    # TODO: needs research, `0.01 * np.median(br1)` sd scale factor selected manually
            if self.ndim == 1:
                # Retain the photometric data for the resulting spectral object.
                spectral_obj = Spectrum(nm1, br1, sd1, name=self.name, photospectrum=deepcopy(self))
            else:
                # It may be too costly to retain photometry for spectral squares and cubes.
                spectral_obj = target_class(nm1, br1, sd1, name=self.name)
            if crop:
                start = max(nm1[0], nm_arr[0])
                end = min(nm1[-1], nm_arr[-1])
                spectral_obj.br = spectral_obj.get_br_in_range(start, end)
                spectral_obj.sd = spectral_obj.get_sd_in_range(start, end)
                spectral_obj.nm = aux.grid(start, end, nm_step)
            return spectral_obj
        except ZeroDivisionError:
            print(f'# Note for the PhotospectralObject "{self.name}"')
            print(f'- Something unexpected happened in spectral reconstruction to {target_class.__name__}. It was replaced by a stub.')
            print(f'- More precisely, {format_exc(limit=0).strip()}')
            return target_class.stub(self.name)

    def apply_element_wise_operation(self, other: _TrueColorToolsObject, br_handling: Callable, sd_handling: Callable) -> Self:
        """
        Returns a new PhotospectralObject formed from element-wise operation with
        a SpectralObject or another PhotospectralObject. Operations between objects
        of the same dimensionality and all (photo)spectrum operations are supported.

        The filter system of the second object, if it does not match, is converted
        to the filter system of the first object!
        """
        filter_system = self.filter_system
        if isinstance(other, _SpectralObject) or (isinstance(other, _PhotospectralObject) and other.filter_system != filter_system):
            # Converting to a PhotospectralObject of the same filter system
            other = other @ filter_system
        br = br_handling(self.br, other.br)
        sd = sd_handling(self.br, self.sd, other.br, other.sd)
        higher_dim = (self, other)[self.ndim < other.ndim]
        return higher_dim.__class__(filter_system, br, sd, name=higher_dim.name)


stub_filter_system = FilterSystem.from_list(('Generic_Bessell.B', 'Generic_Bessell.V'))

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

    def __init__(self, filter_system: FilterSystem, br: Sequence, sd: Sequence = None, name: str | ObjectName = None):
        super().__init__(1, filter_system, br, sd, name)
    
    @staticmethod
    def stub(name=None):
        """ Initializes an object in case of the data problems """
        return Photospectrum(stub_filter_system, np.zeros(2), name=name)


class PhotospectralSquare(_PhotospectralObject, _Square):
    """
    Class to work with set of filters measurements (2D PhotospectralObject).

    Attributes:
    - `filter_system` (FilterSystem): instance of the class storing filter profiles
    - `nm` (np.ndarray): shortcut for filter_system.nm, the definition range
    - `br` (np.ndarray): array of "brightness" in energy density units (not a photon counter)
    - `sd` (np.ndarray): optional array of standard deviations
    - `name` (ObjectName): name as an instance of a class that stores its components
    - `size` (int): spatial axis length
    """

    def __init__(self, filter_system: FilterSystem, br: Sequence, sd: Sequence = None, name: str | ObjectName = None):
        super().__init__(2, filter_system, br, sd, name)
    
    @staticmethod
    def stub(name=None):
        """ Initializes an object in case of the data problems """
        return PhotospectralSquare(stub_filter_system, np.zeros((2, 1)), name=name)


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
    - `height` (int): vertical spatial axis length
    - `size` (int): number of pixels
    """

    def __init__(self, filter_system: FilterSystem, br: Sequence, sd: Sequence = None, name: str | ObjectName = None):
        super().__init__(3, filter_system, br, sd, name)
    
    @staticmethod
    def stub(name=None):
        """ Initializes an object in case of the data problems """
        return PhotospectralCube(stub_filter_system, np.zeros((2, 1, 1)), name=name)



# ------------ Phase Photometry Section ------------

class _PhotometricModel:
    """
    Internal base class to store a photometric model parameters,
    calculate their phase functions and albedo.
    """
    params: dict = None
    filter_or_nm: str|int|float = None
    geometric_albedo: [float, float] = None
    phase_integral: [float, float] = None

    def __init__(self, params: dict = None, filter_or_nm: str|int|float = None) -> None:
        self.params = params
        self.filter_or_nm = filter_or_nm
        self._integrate()

    def _integrate(self) -> None:
        """ Analytically or numerically computes usable values from a model parameters """
        raise NotImplementedError('Must be implemented in the inherited classes.')
    
    def phase_function(self, alpha): # input in radians!
        return NotImplementedError('Must be implemented in the inherited classes.')
    
    @property
    def spherical_albedo(self):
        if self.geometric_albedo is not None and self.phase_integral is not None:
            a = aux.mul_br(self.geometric_albedo[0], self.phase_integral[0])
            a_sd = aux.mul_sd(self.geometric_albedo[0], self.geometric_albedo[1], self.phase_integral[0], self.phase_integral[1])
            return a, a_sd
        else:
            return None
    
    def estimate_geometric_albedo(self, spherical_in_V: [float, float]):
        """
        Returns exact or estimated value of geometric albedo with the flag showing the case.

        For phase integral estimation, model by Shevchenko et al. (2019) is used.
        https://ui.adsabs.harvard.edu/abs/2019A%26A...626A..87S/abstract
        q = 0.359 (± 0.005) + 0.47 (± 0.03) p, where `p` is geometric albedo.
        """
        if spherical_in_V is not None and self.phase_integral is not None:
            geometric_in_V = spherical_in_V[0] / self.phase_integral[0]
            return geometric_in_V, False
        else:
            geometric_in_V = (np.sqrt(0.359**2 + 4 * 0.47 * spherical_in_V[0]) - 0.359) / (2 * 0.47)
            return geometric_in_V, True

    def estimate_spherical_albedo(self, geometric_in_V: [float, float]):
        """
        Returns exact or estimated value of spherical albedo with the flag showing the case.

        For phase integral estimation, model by Shevchenko et al. (2019) is used.
        https://ui.adsabs.harvard.edu/abs/2019A%26A...626A..87S/abstract
        q = 0.359 (± 0.005) + 0.47 (± 0.03) p, where `p` is geometric albedo.
        """
        if geometric_in_V is not None and self.phase_integral is not None:
            spherical_in_V = geometric_in_V[0] * self.phase_integral[0]
            return spherical_in_V, False
        else:
            spherical_in_V = geometric_in_V[0] * (0.359 + 0.47 * geometric_in_V[0])
            return spherical_in_V, True


class DefaultModel(_PhotometricModel):
    """ Class for objects with unknown phase function """

    def _integrate(self) -> None:
        pass


class PhaseCoefficient(_PhotometricModel):
    """
    One-parameter model with phase coefficient β (in mag/deg).

    The integration formula used was derived in M. Noland, J. Veverka, 1976:
    https://www.sciencedirect.com/science/article/abs/pii/0019103576901548

    The error propagation formula was used to handle the uncertainty.
    """

    _k = 180 / np.pi * 0.4 * np.log(10) # ≈ 52.77

    def _integrate(self) -> None:
        beta, beta_sd = aux.parse_value_sd(self.params['beta'])
        beta *= self._k
        _exp = np.exp(-np.pi * beta)
        denominator = 1 + beta * beta
        phase_integral = 2 * (1 + _exp) / denominator
        if beta_sd is not None:
            phase_integral_sd = beta_sd * 2 * self._k * (np.pi * _exp + beta * phase_integral) / denominator
        else:
            phase_integral_sd = None
        self.phase_integral = (phase_integral, phase_integral_sd)
    
    def phase_function(self, alpha):
        beta, _ = aux.parse_value_sd(self.params['beta'])
        return np.exp(-self._k * beta * np.array(alpha))
        # equivalent to 10**(-0.4 * beta * alpha / np.pi * 180)


class Exponentials(_PhotometricModel):
    """
    Describes phase function with a sum of exponentials.
    Usually one (like phase coefficient), two (Akimov, 1988) or three (Velikodsky, 2011) are used.
    """

    def _integrate(self) -> None:
        n_exponentials = len(self.params) // 2
        self._A =  np.empty(n_exponentials)
        self._mu = np.empty(n_exponentials)
        for i in range(n_exponentials):
            self._A[i] = aux.parse_value_sd(self.params[f'A_{i+1}'])[0]
            self._mu[i] = aux.parse_value_sd(self.params[f'mu_{i+1}'])[0]
        if (zero_phase_angle := self._A.sum()) != 1:
            # if function was not normalized, it shows geometric albedo at 0 phase angle
            self.geometric_albedo = zero_phase_angle, None
        self.phase_integral = 2 * np.sum(self._A * (1 + np.exp(-self._mu * np.pi)) / (1 + self._mu**2)) / zero_phase_angle, None
    
    def phase_function(self, alpha):
        phi = np.sum(self._A[:, np.newaxis] * np.exp(-self._mu[:, np.newaxis] * alpha), axis=0)
        if phi.size == 1:
            phi = phi[0]
        if self.geometric_albedo is not None:
           phi /= self.geometric_albedo[0]
        return phi


class HG(_PhotometricModel):
    """
    Two-parameter magnitude system model:
    - H: “reduced magnitude” at zero phase angle
    - G: “slope parameter” that describes the shape of the phase curve

    See Bowell et al (1989). Application of photometric models to asteroids.
    https://ui.adsabs.harvard.edu/abs/1989aste.conf..524B/abstract
    """

    def _integrate(self) -> None:
        g, g_sd = aux.parse_value_sd(self.params['G'])
        q = 0.290 + 0.684 * g
        q_sd = None if g_sd is None else 0.684 * g_sd
        self.phase_integral = (q, q_sd)
    
    def phase_function(self, alpha):
        g, _ = aux.parse_value_sd(self.params['G'])
        alpha = np.array(alpha)
        alpha2 = 0.5 * alpha
        sin_alpha = np.sin(alpha)
        tan_alpha2 = np.tan(alpha2)
        sin_fraction = sin_alpha / (0.119 + 1.341 * sin_alpha - 0.754 * sin_alpha**2)
        phi1s = 1 - 0.986 * sin_fraction
        phi1l = np.exp(-3.332 * tan_alpha2**0.631)
        phi2s = 1 - 0.238 * sin_fraction
        phi2l = np.exp(-1.862 * tan_alpha2**1.218)
        w = np.exp(-90.56 * tan_alpha2**2)
        v = 1 - w
        phi1 = w * phi1s + v * phi1l
        phi2 = w * phi2s + v * phi2l
        return (1 - g) * phi1 + g * phi2
        # Approximation:
        # (1 - g) * np.exp(-3.33 * tan_alpha2**0.63) + g * np.exp(-1.87 * tan_alpha2**1.22)


class HG1G2(_PhotometricModel):
    """
    Three-parameter magnitude system model:
    - H: “reduced magnitude” at zero phase angle
    - G1: the first “slope parameter”
    - G2: the second “slope parameter”

    See Muinonen et al (2010). A three-parameter magnitude phase function for asteroids.
    https://www.sciencedirect.com/science/article/abs/pii/S001910351000151X
    """

    def _integrate(self) -> None:
        g1, g1_sd = aux.parse_value_sd(self.params['G_1'])
        g2, g2_sd = aux.parse_value_sd(self.params['G_2'])
        q = 0.009082 + 0.4061 * g1 + 0.8092 * g2
        if g1_sd is None and g2_sd is None:
            q_sd = None
        else:
            if g1_sd is None:
                g1_sd = 0
            if g2_sd is None:
                g2_sd = 0
            q_sd = 0.4061 * g1_sd + 0.8092 * g2_sd
        self.phase_integral = (q, q_sd)
    
    def phase_function(self, alpha):
        g1, _ = aux.parse_value_sd(self.params['G_1'])
        g2, _ = aux.parse_value_sd(self.params['G_2'])
        return g1 * aux.hg1g2_phi1(alpha) + g2 * aux.hg1g2_phi2(alpha) + (1 - g1 - g2) * aux.hg1g2_phi3(alpha)


class Hapke(_PhotometricModel):
    """
    Hapke photometric model. A common, partially empirical model.

    See Hapke, B. (1984). Bidirectional reflectance spectroscopy.
    Icarus, 59(1), 41–59. doi:10.1016/0019-1035(84)90054-x
    https://www.sciencedirect.com/science/article/abs/pii/001910358490054X
    """

    def _integrate(self):
        w, _ = aux.parse_value_sd(self.params['w']) # single particle scattering albedo
        bo, _ = aux.parse_value_sd(self.params['bo']) # amplitude of opposition surge
        h, _ = aux.parse_value_sd(self.params['h']) # width of opposition surge
        b, _ = aux.parse_value_sd(self.params['b']) # Henyey-Greenstein single particle scattering function parameter
        c, _ = aux.parse_value_sd(self.params['c']) # Henyey-Greenstein single particle scattering function parameter
        theta = np.radians(aux.parse_value_sd(self.params['theta'])[0]) # macroscopic roughness angle
        gamma = np.sqrt(1 - w)
        r0 = (1 - gamma) / (1 + gamma) # bihemispherical  reflectance
        # geometric albedo:
        C = 1 - r0 * (0.048 * theta + 0.0041 * theta**2) - r0**2 * (0.33 * theta + 0.0049 * theta**2)
        self.geometric_albedo = w / 8 * ((1 + bo) * aux.henyey_greenstein(0, b, c) - 1) + C * 0.5 * r0 * (1 + r0 / 3), None
        # phase function:
        def phase_function(alpha):
            # without this check the output would be nan
            alpha = np.array(alpha, dtype='float')
            mask = alpha == 0
            phi = np.empty_like(alpha)
            phi[mask] = 1.
            alpha = alpha[~mask]
            alpha2 = alpha * 0.5
            B = bo / (1 + np.tan(alpha2) / h)
            phi[~mask] = w / 8 * ((1 + B) * aux.henyey_greenstein(alpha, b, c) - 1) + 0.5 * r0 * (1 - r0)
            phi[~mask] *= 1 + np.sin(alpha2) * np.tan(alpha2) * np.log(np.tan(0.5 * alpha2))
            phi[~mask] += 2/3 * r0**2 * (np.sin(alpha) + (np.pi - alpha) * np.cos(alpha)) / np.pi
            phi[~mask] *= aux.hapke_k(alpha, theta) * phi[~mask] / self.geometric_albedo[0]
            return phi
        self.phase_function = phase_function
        # Numerical calculation of spherical albedo
        step = 0.01
        a = np.arange(0, np.pi, step) # 0°-180° phase angle array (radians)
        self.phase_integral = 2 * aux.integrate(phase_function(a) * np.sin(a), step=step, precisely=True), None



# ------------ Database Processing Section ------------

class EmittingBody:
    """
    High-level processing class, specializing on photometry of an emitting physical body,
    for which the concept of albedo is not applicable.
    """

    def __init__(self, name: ObjectName, spectrum: Spectrum):
        """
        Args:
        - `name` (ObjectName): name as an instance of a class that stores its components
        - `spectrum` (Spectrum): (photo)spectrum
        """
        self.name = name
        self.spectrum = spectrum
    
    def get_spectrum(self, *args, **kwargs):
        """
        Returns the spectrum as the first argument, and the `None` status (of albedo estimating)
        as the second one.
        """
        return self.spectrum, None


class ReflectingBody:
    """ High-level processing class, specializing on reflectance photometry of a physical body """

    def __init__(
            self, name: ObjectName, unscaled: Spectrum = None, geometric: Spectrum = None,
            spherical: Spectrum = None, photometric_model: _PhotometricModel = None
        ):
        """
        Args:
        - `name` (ObjectName): name as an instance of a class that stores its components 
        - `geometric` (Spectrum): geometric albedo (photo)spectrum
        - `spherical` (Spectrum): spherical albedo (photo)spectrum
        - `photometric_model` (PhotometricModel): describes the albedo behavior with phase angle
        """
        self.name = name
        self.unscaled = unscaled
        self.geometric = geometric
        self.spherical = spherical
        self.photometric_model = photometric_model
    
    def get_spectrum(self, mode: str):
        """
        Returns the albedo-scaled spectrum as the first argument, and the status as the second one.

        The status interpretation: "estimated = "
        - `True` means albedo was estimated using some assumptions
        - `False` means the requested albedo spectrum is known or calculated without assumptions
        - `None` means the spectrum can't be albedo-scaled
        """
        match mode:
            case 'geometric':
                if self.geometric is not None:
                    return self.geometric, False
                elif self.spherical is not None:
                    spherical_in_V = self.spherical @ get_filter('Generic_Bessell.V')
                    geometric_in_V, estimated = self.photometric_model.estimate_geometric_albedo(spherical_in_V)
                    return self.spherical.scaled_at(get_filter('Generic_Bessell.V'), geometric_in_V), estimated
                else:
                    return self.unscaled, None
            case 'spherical':
                if self.spherical is not None:
                    return self.spherical, False
                elif self.geometric is not None:
                    geometric_in_V = self.geometric @ get_filter('Generic_Bessell.V')
                    spherical_in_V, estimated = self.photometric_model.estimate_spherical_albedo(geometric_in_V)
                    return self.geometric.scaled_at(get_filter('Generic_Bessell.V'), spherical_in_V), estimated
                else:
                    return self.unscaled, None


sun_SI = Spectrum.from_file('spectra/files/CALSPEC/sun_reference_stis_002.fits', name='Sun') # W / (m² nm)
sun_SI.sd = None # removing uncertainty to facilitate calculations and simplify spectrum plots
sun_in_V, _ = sun_SI @ get_filter('Generic_Bessell.V')
sun_norm = sun_SI.scaled_at(get_filter('Generic_Bessell.V'))
sun_filter = sun_SI.normalize()

vega_SI = Spectrum.from_file('spectra/files/CALSPEC/alpha_lyr_stis_011.fits', name='Vega') # W / (m² nm)
vega_SI.sd = None # removing uncertainty to facilitate calculations and simplify spectrum plots
vega_in_V, _ = vega_SI @ get_filter('Generic_Bessell.V')
vega_norm = vega_SI.scaled_at(get_filter('Generic_Bessell.V'))


def _create_TCT_object(
        name: ObjectName, nm: Sequence[int|float], filters: Sequence[str], br: Sequence,
        sd: Sequence = None, filter_system: str = None, calib: str = None,
        is_sun: bool = False, is_emission_spectrum: bool = False
    ):
    """
    Decides whether we are dealing with photospectrum or continuous spectrum
    and calibrates the spectral object.
    """
    if len(nm) > 0:
        if is_emission_spectrum:
            TCT_obj = Spectrum.from_spectral_lines(nm, br, sd, name=name)
        else:
            TCT_obj = Spectrum.from_array(nm, br, sd, name=name)
    elif len(filters) > 0:
        TCT_obj = Photospectrum(FilterSystem.from_list(filters, name=filter_system), br, sd, name=name)
    else:
        print(f'# Note for the database object "{name}"')
        print(f'- No wavelength data. Spectrum stub object was created.')
        TCT_obj = Spectrum.stub(name)
    if calib is not None:
        match calib.lower():
            case 'vega':
                TCT_obj *= vega_norm
            case 'ab':
                TCT_obj = TCT_obj.convert_from_frequency_spectral_density()
            case _:
                pass
    if is_sun:
        TCT_obj /= sun_norm
    return TCT_obj

def database_parser(name: ObjectName, content: dict) -> EmittingBody | ReflectingBody:
    """
    Depending on the contents of the object read from the database, returns a class that has `get_spectrum()` method.

    Supported input keys of a database unit:
    - `tags` (list): strings categorizing the spectral data, optional
    - `nm` (list): list of wavelengths in nanometers
    - `br` (list): same-size list of "brightness" in energy spectral density units
    - `mag` (list): same-size list of magnitudes
    - `sd` (list/number): same-size list of standard deviations (or a common value)
    - `nm_range` (dict): wavelength range definition in the format `{start: …, stop: …, step: …}`
    - `slope` (dict): spectrum definition in the format `{start: …, stop: …, power/percent_per_100nm: …}`
    - `file` (str): path to a text or FITS file, recommended placing in `spectra` or `spectra_extras` folder
    - `filters` (list): list of filter names present in the `filters` folder (can be mixed with nm values)
    - `color_indices` (list): dictionary of color indices, formatted `{'filter1-filter2': …, …}`
    - `photometric_system` (str): a way to parenthesize the photometric system name (separator is a dot)
    - `calibration_system` (str): `Vega` or `AB` filters zero points calibration, `ST` is assumed by default
    - `geometric_albedo` (list): scales the data to geometric albedo spectrum, syntax is `[filter/nm, value]`
    - `spherical_albedo` (list): scales the data to spherical albedo spectrum, syntax is `[filter/nm, value]`
    - `albedo` (list): scales the data to both geom. and sphe. albedo spectra, syntax is `[filter/nm, value]`
    - `bond_albedo` (number): scales the data to spherical albedo spectrum using known Solar spectrum
    - `phase_integral` (number/list): transition factor from geometric albedo to spherical albedo
    - `phase_function` (list): phase function name and its parameters to compute phase integral
    - `br_geometric`, `br_spherical` (list): specifying unique spectra for different albedos
    - `sd_geometric`, `sd_spherical` (list/number): corresponding standard deviations or a common value
    - `is_geometric_albedo` (bool): `true` to interpret the data as a geometric albedo spectrum
    - `is_spherical_albedo` (bool): `true` to interpret the data as a spherical albedo spectrum
    - `is_albedo` (bool): `true` to interpret the data as a both geom. and sphe. albedo spectra
    - `is_reflecting_sunlight` (bool): `true` to divide the data by the reflected Solar spectrum
    - `is_emission_spectrum` (bool): `true` to interpret the data points as spectral lines
    - `is_emissive` (bool): `true` not expect albedo data and always render in the chromaticity mode
    """
    br = []
    sd = None
    nm = [] # Spectrum object indicator
    filters = [] # Photospectrum object indicator
    filter_system = None
    if 'file' in content:
        try:
            nm, br, sd = di.file_reader(content['file'])
        except Exception:
            stub = Spectrum.stub()
            nm = stub.nm
            br = stub.br
            print(f'# Note for the Spectrum object "{name}"')
            print(f'- Something unexpected happened during external file reading. The data was replaced by a stub.')
            print(f'- More precisely, {format_exc(limit=0).strip()}')
    else:
        # Brightness reading
        if 'br' in content:
            br, sd = aux.parse_value_sd_list(content['br'])
            if 'sd' in content:
                sd = aux.repeat_if_value(content['sd'], len(br))
        elif 'mag' in content:
            mag, sd = aux.parse_value_sd_list(content['mag'])
            br = aux.mag2irradiance(mag)
            br /= br.mean() # simple calibration for data not scaled by albedo
            if 'sd' in content:
                sd = aux.repeat_if_value(content['sd'], len(br))
            if sd is not None:
                sd = aux.sd_mag2sd_irradiance(sd, br)
        # Spectrum reading
        if 'nm' in content:
            nm = content['nm']
        elif 'nm_range' in content:
            nm_range = content['nm_range']
            nm = np.arange(nm_range['start'], nm_range['stop']+1, nm_range['step'])
            # important not to use aux.grid() here
        elif 'slope' in content:
            slope = content['slope']
            nm = aux.grid(slope['start'], slope['stop'], nm_step)
            if 'power' in slope:
                # spectral gradient with γ (power law like in Karkoschka (2001) doi:10.1006/icar.2001.6596)
                power, power_sd = aux.parse_value_sd(slope['power'])
                mid_nm = 0.5 * (slope['stop'] + slope['start'])
                br = (nm / mid_nm)**power # br=1 at nm midpoint
                if power_sd is not None:
                    sd = br * np.abs((nm / mid_nm)**power_sd - 1)
            elif 'percent_per_100nm' in slope:
                # spectral gradient with S' (like in Jewitt (2002) doi:10.1086/338692)
                pp100nm, pp100nm_sd = aux.parse_value_sd(slope['percent_per_100nm'])
                # The exact exponential formula, but astronomers don't use it:
                # br = (1 + 0.01 * percent_per_100nm)**(0.01 * nm)
                # They use just a line:
                nm_delta = slope['stop'] - slope['start']
                nm_scaled = (nm - slope['start']) / nm_delta - 0.5
                br = nm_delta * (0.5 + 0.01 * pp100nm * nm_scaled) # br=1 at nm midpoint
                if pp100nm_sd is not None:
                    sd = nm_delta * np.abs(0.01 * pp100nm_sd * nm_scaled)
        # Photospectrum reading
        elif 'filters' in content:
            filters = content['filters']
        elif 'color_indices' in content:
            filters, br, sd = aux.color_indices_parser(content['color_indices'])
        if 'photometric_system' in content:
            # regular filter if name is string, else "delta-filter" (wavelength)
            filter_system = content['photometric_system']
            filters = [f'{filter_system}.{short_name}' if isinstance(short_name, str) else short_name for short_name in filters]
    # Phase function reading
    if 'phase_function' in content:
        phase_func = content['phase_function']
        match len(phase_func):
            case 2:
                filter_or_nm = None
                model_name, params = phase_func
            case 3:
                filter_or_nm, model_name, params = phase_func
        match model_name:
            case 'phase coefficient':
                photometric_model = PhaseCoefficient(params, filter_or_nm)
            case 'exponentials':
                photometric_model = Exponentials(params, filter_or_nm)
            case 'HG':
                photometric_model = HG(params, filter_or_nm)
            case 'HG1G2':
                photometric_model = HG1G2(params, filter_or_nm)
            case 'Hapke':
                photometric_model = Hapke(params, filter_or_nm)
            case _:
                print(f'# Note for the database object "{name}"')
                print(f'- Phase function model "{model_name}" is not supported.')
                photometric_model = DefaultModel()
    else:
        photometric_model = DefaultModel()
    if 'phase_integral' in content:
        photometric_model.phase_integral = aux.parse_value_sd(content['phase_integral'])
    # Albedo reading
    geom_where = geom_how = sphe_where = sphe_how = None
    if photometric_model.geometric_albedo is not None:
        geom_where = photometric_model.filter_or_nm
        geom_how = photometric_model.geometric_albedo
    if photometric_model.spherical_albedo is not None:
        sphe_where = photometric_model.filter_or_nm
        sphe_how = photometric_model.spherical_albedo
    # "albedo" parsing
    is_geom_albedo = is_sphe_albedo = False if 'is_albedo' not in content else content['is_albedo']
    if 'albedo' in content:
        where, how = content['albedo']
        geom_where = sphe_where = where
        how = aux.parse_value_sd(how)
        geom_how = sphe_how = how
    # "geometric albedo" parsing
    if 'is_geometric_albedo' in content:
        is_geom_albedo = content['is_geometric_albedo']
    if 'geometric_albedo' in content:
        geom_where, geom_how = content['geometric_albedo']
        geom_how = aux.parse_value_sd(geom_how)
    # "spherical albedo" parsing
    if 'is_spherical_albedo' in content:
        is_sphe_albedo = content['is_spherical_albedo']
    if 'spherical_albedo' in content:
        sphe_where, sphe_how = content['spherical_albedo']
        sphe_how = aux.parse_value_sd(sphe_how)
    # Main part
    calib = content['calibration_system'] if 'calibration_system' in content else None
    is_sun = 'is_reflecting_sunlight' in content and content['is_reflecting_sunlight']
    is_emission = 'is_emission_spectrum' in content and content['is_emission_spectrum']
    # Goal is to create geometric and spherical albedo (photo)spectral objects
    TCT_obj = geometric = spherical = None
    if len(br) == 0:
        if 'br_geometric' in content:
            br_geom = content['br_geometric']
            sd_geom = aux.repeat_if_value(content['sd_geometric'], len(br_geom)) if 'sd_geometric' in content else None
            geometric = _create_TCT_object(name, nm, filters, br_geom, sd_geom, filter_system, calib, is_sun, is_emission)
            if sphe_how is not None:
                spherical = geometric.scaled_at(sphe_where, sphe_how)
            elif 'bond_albedo' in content:
                spherical = geometric.scaled_at(sun_filter, *aux.parse_value_sd(content['bond_albedo']))
        if 'br_spherical' in content:
            br_sphe = content['br_spherical']
            sd_sphe = aux.repeat_if_value(content['sd_spherical'], len(br_sphe)) if 'sd_spherical' in content else None
            spherical = _create_TCT_object(name, nm, filters, br_sphe, sd_sphe, filter_system, calib, is_sun, is_emission)
            if geom_how is not None:
                geometric = spherical.scaled_at(geom_where, geom_how)
        if geometric is None and spherical is None:
            print(f'# Note for the database object "{name}"')
            print(f'- No brightness data. Spectrum stub object was created.')
            TCT_obj = Spectrum.stub(name)
    else:
        TCT_obj = _create_TCT_object(name, nm, filters, br, sd, filter_system, calib, is_sun, is_emission)
        if is_geom_albedo:
            geometric = TCT_obj
        elif geom_how is not None:
            geometric = TCT_obj.scaled_at(geom_where, geom_how)
        if is_sphe_albedo:
            spherical = TCT_obj
        elif sphe_how is not None:
            spherical = TCT_obj.scaled_at(sphe_where, sphe_how)
        elif 'bond_albedo' in content:
            spherical = TCT_obj.scaled_at(sun_filter, *aux.parse_value_sd(content['bond_albedo']))
    #tags = set()
    #if 'tags' in content:
    #    for tag in content['tags']:
    #        tags |= set(tag.split('/'))
    if 'is_emissive' in content and content['is_emissive']:
        return EmittingBody(name, TCT_obj)
    else:
        return ReflectingBody(name, TCT_obj, geometric, spherical, photometric_model)



# ------------ Color Processing Section ------------
# Needs improvement, see https://github.com/Askaniy/TrueColorTools/issues/22

class ColorSystem:

    def __init__(self, red: Sequence, green: Sequence, blue: Sequence, white: Sequence):
        """
        Initialise the ColorSystem object.
        The implementation is based on https://scipython.com/blog/converting-a-spectrum-to-a-colour/
        Defining the color system requires four 2d vectors (primary illuminants and the "white point")
        """
        self.red, self.green, self.blue, self.white = map(self.xy2xyz, [red, green, blue, white]) # chromaticities
        self.M = np.vstack((self.red, self.green, self.blue)).T # the chromaticity matrix (rgb -> xyz) and its inverse
        self.MI = np.linalg.inv(self.M) # white scaling array
        self.wscale = self.MI.dot(self.white) # xyz -> rgb transformation matrix
        self.T = self.MI / self.wscale[:, np.newaxis]
    
    @staticmethod
    def xy2xyz(xy):
        return np.array((xy[0], xy[1], 1-xy[0]-xy[0])) # (x, y, 1-x-y)

# Used white points
illuminant_E = (1/3, 1/3)
#illuminant_D65 = (0.3127, 0.3291)

# Used color systems
srgb_system = ColorSystem((0.64, 0.33), (0.30, 0.60), (0.15, 0.06), illuminant_E)
#hdtv_system = ColorSystem((0.67, 0.33), (0.21, 0.71), (0.15, 0.06), illuminant_D65)
#smpte_system = ColorSystem((0.63, 0.34), (0.31, 0.595), (0.155, 0.070), illuminant_D65)

# Stiles & Burch (1959) 2-deg color matching data, direct experimental data
# http://www.cvrl.org/stilesburch2_ind.htm
# Edge sensitivity modulo values less than 10⁴ were previously removed
rgb_cmf = FilterSystem.from_list(('StilesBurch2deg.r', 'StilesBurch2deg.g', 'StilesBurch2deg.b'))

# CIE XYZ functions transformed from the CIE (2006) LMS functions, 2-deg
# http://www.cvrl.org/ciexyzpr.htm
# Edge sensitivity values less than 10⁴ were previously removed
xyz_cmf = FilterSystem.from_list(('cie2deg.x', 'cie2deg.y', 'cie2deg.z'))

# to be chosen depending on the bool flag (`cie`)
cmfs = (rgb_cmf, xyz_cmf)


class _ColorObject:
    """
    Internal class for inheriting color attributes and methods.
    Stores brightness values in the range 0 to 1 in the `br` attribute.
    To avoid data loss, brightness above 1 is not clipped before export.
    """

    def __init__(self, br: Sequence, maximize_brightness=False):
        """
        Args:
        - `br` (Sequence): array, the first axis of which is spectral (red, green, blue)
        - `maximize_brightness` (bool): normalization by the maximum value found
        """
        self.br: np.ndarray = np.clip(np.nan_to_num(br), 0, None, dtype='float')
        if maximize_brightness and self.br.max() != 0:
            self.br /= self.br.max()

    @classmethod
    def from_spectral_data(cls, data: _TrueColorToolsObject, maximize_brightness=False, srgb=False):
        """ Convolves the (photo)spectral object with one of the available CMF systems """
        if srgb:
            xyz = (data @ xyz_cmf).br / 3 # why? don't know, it works
            # single vector code: rgb = srgb_system.T.dot(xyz)
            rgb: np.ndarray = np.tensordot(srgb_system.T, xyz, axes=(1, 0))
            if np.any(rgb < 0):
                # RGB derived from XYZ turned out to be outside the color space, approximating by desaturating
                negative_mask = np.any(rgb < 0, axis=0)
                # single vector code: rgb -= rgb.min()
                rgb[:, negative_mask] -= rgb.min(axis=0)[negative_mask]
        else:
            rgb = (data @ rgb_cmf).br
        return cls(rgb, maximize_brightness)
 
    def gamma_corrected(self):
        """ Creates a new ColorObject with applied gamma correction """
        output = deepcopy(self)
        output.br = aux.gamma_correction(output.br)
        return output
    
    def grayscale(self):
        """ Converts color to grayscale using sRGB luminance of the CIE 1931 """
        # inaccurate CIE standard usage (TODO)
        return np.dot(self.br, (0.2126, 0.7152, 0.0722))


class ColorPoint(_ColorObject):
    """
    Class to work with an array of red, green and blue values.
    Stores brightness values in the range 0 to 1 in the `br` attribute, numpy array of shape (3).
    To avoid data loss, brightness above 1 is not clipped before export.
    """

    def to_bit(self, bit: int, clip: bool = False) -> np.ndarray:
        """ Returns color array, scaled to the appropriate power of two (not rounded) """
        factor = 2**bit - 1
        if clip:
            return np.clip(self.br, 0, 1) * factor
        else:
            return self.br * factor

    def to_html(self):
        """ Converts fractional rgb values to HTML-styled hexadecimal string """
        return '#{:02x}{:02x}{:02x}'.format(*self.to_bit(8, clip=True).round().astype('int'))


class ColorLine(_ColorObject):
    """
    Class to work with a line of red, green and blue channels.
    Stores brightness values in the range 0 to 1 in the `br` attribute, numpy array of shape (3, X).
    To avoid data loss, brightness above 1 is not clipped before export.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.br = np.atleast_2d(self.br) # interprets color points as lines
    
    @property
    def size(self):
        """ Returns spatial axis length """
        return self.br.shape[1]


class ColorImage(_ColorObject):
    """
    Class to work with an image of red, green and blue channels.
    Stores brightness values in the range 0 to 1 in the `br` attribute, numpy array of shape (3, X, Y).
    To avoid data loss, brightness above 1 is not clipped before export.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.br = np.atleast_3d(self.br) # interprets color points and lines as images
    
    def upscale(self, times: int):
        """ Creates a new ColorImage with increased size by an integer number of times """
        output = deepcopy(self)
        output.br = np.repeat(np.repeat(output.br, times, axis=0), times, axis=1) 
        return output

    def to_pillow_image(self):
        """ Converts ColorImage to the Image object of the Pillow library """
        # TODO: support export to 16 bit and other Pillow modes
        arr = np.clip(self.br, 0, 1) * 255 # 8 bit
        return Image.fromarray(np.around(arr).astype('uint8').transpose())
    
    @property
    def width(self):
        """ Returns horizontal spatial axis length """
        return self.br.shape[1]
    
    @property
    def height(self):
        """ Returns vertical spatial axis length """
        return self.br.shape[2]
