"""
Describes the main image data storage classes and related functions.

- To work with an image of continuous spectra, use the SpectralCube class.
- To work with images made in several passbands, use the PhotometricCube class.
"""

from typing import Sequence, Callable
from itertools import product
from operator import mul, truediv
from traceback import format_exc
from functools import lru_cache
from math import sqrt, ceil
import numpy as np
from src.data_core import Spectrum
import src.auxiliary as aux
import src.image_import as ii


def interpolating(nm0: Sequence, br0: np.ndarray, nm1: Sequence, step: int|float):
    """ Wrapper around single-spectrum function """
    _, x, y = br0.shape
    br1 = np.zeros((len(nm1), x, y), br0.dtype)
    for i, j in product(range(x), range(y)):
        br1[:, i, j] = aux.interpolating(nm0, br0[:, i, j], nm1, step)
    return br1


class SpectralCube:
    """ Class to work with an image of continuous spectra, with strictly defined wavelength resolution step """

    def stub(self):
        """
        Initializes an object in case of input data problems.
        Preserves the spatial dimension of the cube.
        """
        _, x, y = self.br.shape
        return SpectralCube(np.array([555]), np.zeros((1, x, y)), None)

    def __init__(self, nm: Sequence, br: np.ndarray, sd: np.ndarray = None):
        """
        It is assumed that the input wavelength grid can be trusted. If preprocessing is needed, see `SpectralCube.from_array`.
        `br` and `sd` have the following index order: [Spectral axis, X axis, Y axis]

        Args:
        - `nm` (Sequence): list of wavelengths in nanometers with resolution step of 5 nm
        - `br` (np.ndarray): same-size list of "brightness", flux in units of energy (not a photon counter)
        - `sd` (np.ndarray, optional): same-size list of standard deviations
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
            return SpectralCube(np.array([555]), np.zeros((1, x, y)))
        if sd is not None and (len_sd := sd.shape[2]) != len_br:
            print(f'# Note for the SpectralCube object')
            print(f'- Array of standard deviations do not match brightness array ({len_sd} vs {len_br}). Uncertainty was erased.')
            sd = None
        try:
            nm = np.array(nm) # numpy decides int or float
            br = np.array(br, dtype='float64')
            br_upper_limit = br.max()
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
                    br = interpolating(nm, br, uniform_nm, aux.resolution)
                else: # decreasing resolution if step less than 5 nm
                    br = aux.spectral_downscaling(nm, br, uniform_nm, aux.resolution)
                nm = uniform_nm
            if br.min() < 0 or br.max() > br_upper_limit:
                br = np.clip(br, 0, br_upper_limit) # br_upper_limit is a bug workaround? I got max 1.0155->61400.1 after downscaling
        except Exception:
            nm, br, sd = np.array([555]), np.zeros((1, x, y)), None
            print(f'# Note for the SpectralCube object')
            print(f'- Something unexpected happened while trying to create the object from array. It was replaced by a stub.')
            print(f'- More precisely, {format_exc(limit=0).strip()}')
        return SpectralCube(nm, br, sd)
    
    @staticmethod
    @lru_cache(maxsize=1)
    def from_file(file: str):
        """ Creates a SpectralCube object based on loaded data from the specified file """
        return SpectralCube.from_array(*ii.cube_reader(file))
    
    def downscale(self, pixels_limit: int):
        """ Brings the spatial resolution of the cube to approximately match the number of pixels """
        # TODO: averaging like in https://stackoverflow.com/questions/10685654/reduce-resolution-of-array-through-summation
        _, x, y = self.br.shape
        factor = ceil(sqrt(x * y / pixels_limit))
        br = self.br[:,::factor,::factor]
        sd = None
        if self.sd is not None:
            sd = self.sd[:,::factor,::factor]
        return SpectralCube(self.nm, br, sd)
    
    def to_scope(self, scope: np.ndarray):
        """ Returns a new SpectralCube object with a guarantee of definition on the requested scope """
        return SpectralCube(*aux.extrapolating(self.nm, self.br, scope, aux.resolution))

    def integrate(self) -> np.ndarray:
        """ Collapses the SpectralCube along the spectral axis into a two-dimensional image """
        return aux.integrate(self.br, aux.resolution)
    
    def apply_linear_operator(self, operator: Callable, operand: int|float):
        """
        Returns a new SpectralCube object transformed according to the linear operator.
        Linearity is needed because values and uncertainty are handled uniformly.
        """
        br = operator(self.br, operand)
        sd = None
        if self.sd is not None:
            sd = operator(self.sd, operand)
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
            return self.stub()
        else:
            nm = np.arange(start, end+1, aux.resolution, dtype='uint16')
            br0 = self.br[np.where((self.nm >= start) & (self.nm <= end))]
            br1 = aux.scope2cube(other.br[np.where((other.nm >= start) & (other.nm <= end))], br0.shape[1:3])
            return SpectralCube(nm, operator(br0, br1))

    def __mul__(self, other):
        """
        Returns a new SpectralCube object modified by the overloaded multiplication operator.
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
        Returns a new SpectralCube object modified by the overloaded division operator.
        If the operand is a number, a scaled spectrum is returned.
        If the operand is a Spectrum, an emitter spectrum is removed from the intersection.
        """
        if isinstance(other, (int, float)):
            return self.apply_linear_operator(truediv, other)
        else:
            return self.apply_elemental_operator(truediv, other, ' / ')
    
    def __matmul__(self, other) -> np.ndarray:
        """ Implementation of convolution between emission spectral cube and transmission spectrum """
        return (self * other).integrate()
