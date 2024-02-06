""" Responsible for converting image data into a working form. """

import numpy as np
from astropy.io import fits

def cube_reader(file: str) -> tuple[np.ndarray, np.ndarray]:
    """ Imports spectral data from a FITS file in standard of HST STIS """
    with fits.open(file) as hdul:
        #hdul.info()
        #print(repr(hdul[0].header))
        br = np.array(hdul['sci'].data).transpose((0, 2, 1))
        nm = np.array(hdul['wavelength'].data)
    return nm, br
