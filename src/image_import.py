""" Responsible for converting image data into a working form. """

import numpy as np
import astropy.units as u
from spectral_cube import SpectralCube
from spectral_cube.utils import WCSWarning

# Disabling warnings about supplier non-compliance with FITS unit storage standards
from warnings import filterwarnings
filterwarnings(action='ignore', category=WCSWarning, append=True)
filterwarnings(action='ignore', category=u.UnitsWarning, append=True)


def cube_reader(file: str) -> tuple[np.ndarray, np.ndarray]:
    """ Imports spectral cube from a FITS file """
    cube = SpectralCube.read(file, hdu=1)
    nm = np.array(cube.spectral_axis.to(u.nm))
    br = np.array(cube) # [s, y, x]?
    return nm, br
