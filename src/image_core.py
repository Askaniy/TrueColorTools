"""
Describes the main image data storage classes and related functions.

- To work with an image of continuous spectra, use the SpectralCube class.
- To work with images made in several passbands, use the PhotometricCube class.
"""

from typing import Sequence
from traceback import format_exc
from itertools import product
import numpy as np
import src.data_core as dc


def interpolating(nm0: Sequence, br0: np.ndarray, nm1: Sequence, step: int|float):
    """ Wrapper around single-spectrum function """
    l, x, y = br0.shape
    br1 = np.zeros((len(nm1), x, y), br0.dtype)
    for i, j in product(range(x), range(y)):
        br1[:, i, j] = dc.interpolating(nm0, br0[:, i, j], nm1, step)
    return br1

def averaging(nm0: Sequence, br0: np.ndarray, nm1: Sequence, step: int|float):
    """ Wrapper around single-spectrum function """
    l, x, y = br0.shape
    br1 = np.zeros((len(nm1), x, y), br0.dtype)
    for i, j in product(range(x), range(y)):
        br1[:, i, j] = dc.averaging(nm0, br0[:, i, j], nm1, step)
    return br1


class SpectralCube:
    """ Class to work with an image of continuous spectra, with strictly defined wavelength resolution step """

    # Initializes an object in case of input data problems
    stub = (np.array([555]), np.zeros((1, 1, 1)), None)

    def __init__(self, name: str, nm: Sequence, br: np.ndarray, sd: np.ndarray = None, photometry: dc.Photometry = None):
        """
        It is assumed that the input wavelength grid can be trusted. If preprocessing is needed, see `SpectralCube.from_array`.
        `br` and `sd` have the following index order: [wavelength layer, X pixel coordinate, Y pixel coordinate]

        Args:
        - `name` (str): human-readable identification. May include references (separated by "|") and a note (separated by ":")
        - `nm` (Sequence): list of wavelengths in nanometers with resolution step of 5 nm
        - `br` (np.ndarray): same-size list of "brightness", flux in units of energy (not a photon counter)
        - `sd` (np.ndarray, optional): same-size list of standard deviations
        - `photometry` (Photometry, optional): way to store information about the passbands used
        """
        self.name = name
        self.nm = nm
        self.br = br
        if sd is not None:
            self.sd = sd
        else:
            self.sd = None
        if np.any(np.isnan(self.br)):
            self.br = np.nan_to_num(self.br)
            print(f'# Note for the SpectralCube object "{self.name}"')
            print(f'- NaN values detected during object initialization, they been replaced with zeros.')
    
    @staticmethod
    def from_array(name: str, nm: Sequence, br: np.ndarray, sd: np.ndarray = None):
        """
        Creates a SpectralCube object from a 3D array with a check for wavelength uniformity and possible extrapolation.
        The 3D array has the following index order: [wavelength layer, X pixel coordinate, Y pixel coordinate]

        Args:
        - `name` (str): human-readable identification. May include references (separated by "|") and a note (separated by ":")
        - `nm` (Sequence): list of wavelengths, arbitrary grid
        - `br` (np.ndarray): 3D array of "brightness", flux in units of energy (not a photon counter)
        - `sd` (np.ndarray): 3D array of standard deviations
        """
        if (len_nm := len(nm)) != (len_br := br.shape[0]):
            print(f'# Note for the SpectralCube object "{name}"')
            print(f'- Arrays of wavelengths and brightness do not match ({len_nm} vs {len_br}). SpectralCube stub object was created.')
            return SpectralCube(name, *SpectralCube.stub)
        if sd is not None and (len_sd := sd.shape[2]) != len_br:
            print(f'# Note for the SpectralCube object "{name}"')
            print(f'- Array of standard deviations do not match brightness array ({len_sd} vs {len_br}). Uncertainty was erased.')
            sd = None
        try:
            nm = np.array(nm) # numpy decides int or float
            br = np.array(br, dtype='float64')
            if sd is not None:
                sd = np.array(sd, dtype='float64')
            if nm[-1] > dc.nm_red_limit:
                flag = np.where(nm < dc.nm_red_limit + dc.resolution) # with reserve to be averaged
                nm = nm[flag]
                br = br[flag,:,:]
                if sd is not None:
                    sd = sd[flag,:,:]
            if np.any((diff := np.diff(nm)) != dc.resolution): # if not uniform 5 nm grid
                sd = None # standard deviations is undefined then. TODO: process somehow
                uniform_nm = dc.grid(nm[0], nm[-1], dc.resolution)
                if diff.mean() >= dc.resolution: # interpolation, increasing resolution
                    br = interpolating(nm, br, uniform_nm, dc.resolution)
                else: # decreasing resolution if step less than 5 nm
                    br = averaging(nm, br, uniform_nm, dc.resolution)
                nm = uniform_nm
            if br.min() < 0:
                br = np.clip(br, 0, None)
                #print(f'# Note for the SpectralCube object "{name}"')
                #print(f'- Negative values detected while trying to create the object from array, they been replaced with zeros.')
        except Exception:
            nm, br, sd = SpectralCube.stub
            print(f'# Note for the SpectralCube object "{name}"')
            print(f'- Something unexpected happened while trying to create the object from array. It was replaced by a stub.')
            print(f'- More precisely, {format_exc(limit=0).strip()}')
        return SpectralCube(name, nm, br, sd)
