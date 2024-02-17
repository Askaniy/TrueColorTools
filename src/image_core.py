"""
Describes the main image data storage classes and related functions.

- To work with an image of continuous spectra, use the SpectralCube class.
- To work with images made in several passbands, use the PhotometricCube class.
"""

from typing import Sequence, Callable
from operator import mul, truediv
from traceback import format_exc
from functools import lru_cache
import numpy as np
from src.data_core import Spectrum, get_filter
from src.data_processing import photon_spectral_density
import src.auxiliary as aux
import src.image_import as ii


class SpectralCube:
    """ Class to work with an image of continuous spectra, with strictly defined wavelength resolution step """

    @staticmethod
    def stub(x, y):
        """ Initializes an object in case of input data problems. """
        return SpectralCube(np.array([555]), np.zeros((1, x, y)), None)

    def __init__(self, nm: Sequence, br: np.ndarray, sd: np.ndarray = None):
        """
        It is assumed that the input wavelength grid can be trusted. If preprocessing is needed, see `SpectralCube.from_array`.
        `br` and `sd` have the following index order: [Spectral axis, X axis, Y axis]

        Args:
        - `nm` (Sequence): list of wavelengths in nanometers with resolution step of 5 nm
        - `br` (np.ndarray): 3D array of "brightness", flux in units of energy (not a photon counter)
        - `sd` (np.ndarray, optional): 3D array of standard deviations
        """
        self.nm = nm
        self.br = br
        if sd is not None:
            self.sd = sd
        else:
            self.sd = None
        if np.any(np.isnan(self.br)):
            self.br = np.nan_to_num(self.br)
            print(f'# Note for the SpectralCube object')
            print(f'- NaN values detected during object initialization, they been replaced with zeros.')
    
    @staticmethod
    def from_array(nm: Sequence, br: np.ndarray, sd: np.ndarray = None):
        """
        Creates a SpectralCube object from a 3D array with a check for wavelength uniformity and possible extrapolation.
        The 3D array has the following index order: [Spectral axis, X axis, Y axis]

        Args:
        - `nm` (Sequence): list of wavelengths, arbitrary grid
        - `br` (np.ndarray): 3D array of "brightness", flux in units of energy (not a photon counter)
        - `sd` (np.ndarray): 3D array of standard deviations
        """
        len_br, x, y = br.shape
        if (len_nm := len(nm)) != len_br:
            print(f'# Note for the SpectralCube object')
            print(f'- Arrays of wavelengths and brightness do not match ({len_nm} vs {len_br}). SpectralCube stub object was created.')
            return SpectralCube.stub(x, y)
        if sd is not None and (len_sd := sd.shape[0]) != len_br:
            print(f'# Note for the SpectralCube object')
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
                br = br[flag,:,:]
                if sd is not None:
                    sd = sd[flag,:,:]
            if np.any((diff := np.diff(nm)) != aux.resolution): # if not uniform 5 nm grid
                sd = None # standard deviations is undefined then. TODO: process somehow
                uniform_nm = aux.grid(nm[0], nm[-1], aux.resolution)
                if diff.mean() >= aux.resolution: # interpolation, increasing resolution
                    br = aux.interpolating(nm, br, uniform_nm, aux.resolution)
                else: # decreasing resolution if step less than 5 nm
                    br = aux.spectral_downscaling(nm, br, uniform_nm, aux.resolution)
                nm = uniform_nm
            if br.min() < 0:
                br = np.clip(br, 0, None)
            return SpectralCube(nm, br, sd)
        except Exception:
            print(f'# Note for the SpectralCube object')
            print(f'- Something unexpected happened while trying to create the object from array. It was replaced by a stub.')
            print(f'- More precisely, {format_exc(limit=0).strip()}')
            return SpectralCube.stub(x, y)
    
    @staticmethod
    @lru_cache(maxsize=1)
    def from_file(file: str):
        """ Creates a SpectralCube object based on loaded data from the specified file """
        return SpectralCube.from_array(*ii.cube_reader(file))
    
    def downscale(self, pixels_limit: int):
        """ Brings the spatial resolution of the cube to approximately match the number of pixels """
        br = aux.spatial_downscaling(self.br, pixels_limit)
        sd = None
        if self.sd is not None:
            sd = aux.spatial_downscaling(self.sd, pixels_limit)
        return SpectralCube(self.nm, br, sd)
    
    def to_scope(self, scope: np.ndarray):
        """ Returns a new SpectralCube object with a guarantee of definition on the requested scope """
        return SpectralCube(*aux.extrapolating(self.nm, self.br, scope, aux.resolution))
    
    def photons2energy(self):
        """ Returns a new SpectralCube object converted from photon spectral density to energy one """
        return self * photon_spectral_density

    def integrate(self) -> np.ndarray:
        """ Collapses the SpectralCube along the spectral axis into a two-dimensional image """
        return aux.integrate(self.br, aux.resolution)
    
    def apply_linear_operator(self, operator: Callable, operand: int|float):
        """
        Returns a new SpectralCube object transformed according to the linear operator.
        Linearity is needed because values and uncertainty are handled uniformly.
        """
        br = operator(self.br.T, operand).T
        sd = None
        if self.sd is not None:
            sd = operator(self.sd.T, operand).T
        return SpectralCube(self.nm, br, sd)
    
    def apply_elemental_operator(self, operator: Callable, other: Spectrum, operator_sign: str = ', '):
        """
        Returns a new SpectralCube object formed from element-wise operator on two spectra,
        such as multiplication or division.

        Works only at the intersection of spectra! If you need to extrapolate one spectrum
        to the range of another, for example, use `SpectralCube.to_scope(filter.nm) @ filter`

        Note: the PhotometricCube data would be erased because consistency with the SpectralCube object
        cannot be maintained after conversion. TODO: uncertainty processing.
        """
        start = max(self.nm[0], other.nm[0])
        end = min(self.nm[-1], other.nm[-1])
        if start > end: # `>` is needed to process operations with stub objects with no extra logs
            print(f'# Note for spectral element-wise operation "{operator_sign.strip()}"')
            print(f'- The first operand ends on {end} nm and the second starts on {start} nm.')
            print('- There is no intersection between the spectra. SpectralCube stub object was created.')
            _, x, y = self.br.shape
            return SpectralCube.stub(x, y)
        else:
            nm = np.arange(start, end+1, aux.resolution, dtype='uint16')
            br0 = self.br[np.where((self.nm >= start) & (self.nm <= end))]
            br1 = other.br[np.where((other.nm >= start) & (other.nm <= end))]
            return SpectralCube(nm, operator(br0.T, br1).T) # numpy iterates over the last axis

    def __mul__(self, other):
        """
        Returns a new SpectralCube object modified by the overloaded multiplication operator.
        If the operand is a number (or an array of spectral axis size), a scaled cube is returned.
        If the operand is a Spectrum, an emitter spectrum is applied to the intersection.
        """
        if isinstance(other, (int, float, np.ndarray)):
            return self.apply_linear_operator(mul, other)
        elif isinstance(other, Spectrum):
            return self.apply_elemental_operator(mul, other, ' ∙ ')
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        """
        Returns a new SpectralCube object modified by the overloaded division operator.
        If the operand is a number (or an array of spectral axis size), a scaled cube is returned.
        If the operand is a Spectrum, an emitter spectrum is removed from the intersection.
        """
        if isinstance(other, (int, float, np.ndarray)):
            return self.apply_linear_operator(truediv, other)
        elif isinstance(other, Spectrum):
            return self.apply_elemental_operator(truediv, other, ' / ')
    
    def __matmul__(self, other) -> np.ndarray:
        """ Implementation of convolution between emission spectral cube and transmission spectrum """
        return (self * other).integrate()



class PhotometricCube:
    """ Class to work with set of filters measurements. """

    @staticmethod
    def stub(x, y):
        """ Initializes an object in case of input data problems. """
        return PhotometricCube([get_filter('Generic_Bessell.V')], np.zeros((1, x, y)), None)

    def __init__(self, filters: Sequence[Spectrum], br: np.ndarray, sd: np.ndarray = None):
        """
        Args:
        - `filters` (Sequence): list of energy response functions scaled to the unit area, storing as Spectrum objects
        - `br` (np.ndarray): 3D array of intensity
        - `sd` (np.ndarray): 3D array of standard deviations
        """
        self.filters = tuple(filters)
        self.br = np.array(br, dtype='float64')
        if sd is not None:
            self.sd = np.array(sd, dtype='float64')
        else:
            self.sd = None
        len_br, x, y = br.shape
        if (len_filters := len(filters)) != len_br:
            print(f'# Note for the PhotometricCube object')
            print(f'- Arrays of wavelengths and brightness do not match ({len_filters} vs {len_br}). PhotometricCube stub object was created.')
            return PhotometricCube.stub(x, y)
        if sd is not None and (len_sd := sd.shape[0]) != len_br:
            print(f'# Note for the PhotometricCube object')
            print(f'- Array of standard deviations do not match brightness array ({len_sd} vs {len_br}). Uncertainty was erased.')
            sd = None
        if np.any(np.isnan(self.br)):
            self.br = np.nan_to_num(self.br)
            print(f'# Note for the PhotometricCube object')
            print(f'- NaN values detected during object initialization, they been replaced with zeros.')

    def downscale(self, pixels_limit: int):
        """ Brings the spatial resolution of the cube to approximately match the number of pixels """
        br = aux.spatial_downscaling(self.br, pixels_limit)
        sd = None
        if self.sd is not None:
            sd = aux.spatial_downscaling(self.sd, pixels_limit)
        return PhotometricCube(self.filters, br, sd)
    
    def to_scope(self, scope: np.ndarray): # TODO: use kriging here!
        """ Creates a SpectralCube object with inter- and extrapolated PhotometricCube data to fit the wavelength scope """
        try:
            nm0 = self.mean_wavelengths()
            nm1 = aux.grid(nm0[0], nm0[-1], aux.resolution)
            br = aux.interpolating(nm0, self.br, nm1, aux.resolution)
            nm, br = aux.extrapolating(nm1, br, scope, aux.resolution)
            return SpectralCube(nm, br)
        except Exception:
            print(f'# Note for the PhotometricCube object')
            print(f'- Something unexpected happened while trying to inter/extrapolate to SpectralCube object. It was replaced by a stub.')
            print(f'- More precisely, {format_exc(limit=0).strip()}')
            _, x, y = self.br.shape
            return SpectralCube.stub(x, y)
    
    def photons2energy(self):
        """ Returns a new PhotometricCube object converted from photon spectral density to energy one """
        return self * (self @ photon_spectral_density)
    
    def sorted(self):
        """ Sorts the PhotometricCube by increasing wavelength """
        nm = self.mean_wavelengths()
        if np.any(nm[:-1] > nm[1:]): # fast increasing check
            order = np.argsort(nm)
            self.filters = tuple(np.array(self.filters)[order])
            self.br = self.br[order]
            if self.sd is not None:
                self.sd = self.sd[order]
        return self
    
    def mean_wavelengths(self):
        """ Returns an array of mean wavelengths for each filter """
        return np.array([passband.mean_wavelength() for passband in self.filters])
    
    def standard_deviations(self):
        """ Returns an array of uncorrected standard deviations for each filter """
        return np.array([passband.standard_deviation() for passband in self.filters])

    def apply_linear_operator(self, operator: Callable, operand: int|float):
        """
        Returns a new PhotometricCube object transformed according to the linear operator.
        Linearity is needed because values and uncertainty are handled uniformly.
        """
        br = operator(self.br.T, operand).T
        sd = None
        if self.sd is not None:
            sd = operator(self.sd.T, operand).T
        return PhotometricCube(self.filters, br, sd)
    
    def apply_elemental_operator(self, operator: Callable, other: Spectrum):
        """
        Returns a new PhotometricCube object formed from element-wise multiplication or division by the Spectrum.
        Note that this also distorts filter profiles.
        """
        filters = [operator(passband, other).scaled_by_area() for passband in self.filters]
        return operator(PhotometricCube(filters, self.br, self.sd), self @ other) # linear
    
    def __mul__(self, other):
        """
        Returns a new PhotometricCube object modified by the overloaded multiplication operator.
        If the operand is a number (or an array of spectral axis size), a scaled photometric cube is returned.
        If the operand is a Spectrum, an emitter spectrum is applied to the intersections with filters.
        """
        if isinstance(other, (int, float, np.ndarray)):
            return self.apply_linear_operator(mul, other)
        elif isinstance(other, Spectrum):
            return self.apply_elemental_operator(mul, other)
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other: Spectrum):
        """
        Returns a new PhotometricCube object modified by the overloaded division operator.
        If the operand is a number (or an array of spectral axis size), a scaled photometric cube is returned.
        If the operand is a Spectrum, an emitter spectrum is removed from the intersections with filters.
        """
        if isinstance(other, (int, float, np.ndarray)):
            return self.apply_linear_operator(truediv, other)
        elif isinstance(other, Spectrum):
            return self.apply_elemental_operator(truediv, other)

    def __matmul__(self, other: Spectrum) -> np.ndarray[float]:
        """ Convolve all the filters with the spectrum """
        return np.array([other @ passband for passband in self.filters])
