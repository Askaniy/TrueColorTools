""" Responsible for converting image data into a working form. """

from pathlib import Path
import numpy as np
import astropy.units as u
from astropy.convolution import Gaussian1DKernel
from spectral_cube import SpectralCube
import src.auxiliary as aux

from warnings import filterwarnings
filterwarnings(action='ignore')

# Disabling warnings about supplier non-compliance with FITS unit storage standards and spectral-cube warnings
# Strange, but not work in the main program
#from spectral_cube.utils import WCSWarning, ExperimentalImplementationWarning
#filterwarnings(action='ignore', category=u.UnitsWarning, append=True)
#filterwarnings(action='ignore', category=ExperimentalImplementationWarning, append=True)
#filterwarnings(action='ignore', category=WCSWarning, append=True)


# cache?
def cube_reader(file: str) -> tuple[str, np.ndarray, np.ndarray]:
    """ Imports a spectral cube from the FITS file and down scaling spatial resolutions to the specified one. """
    # See https://gist.github.com/keflavich/37a2705fb4add9a2491caf2dfa195efd

    cube = SpectralCube.read(file, hdu=1).with_spectral_unit(u.nm)
    print(cube) # general info

    # Getting target wavelength range
    nm = aux.grid(*cube.spectral_extrema.value, aux.resolution)
    flag = np.where(nm < aux.nm_red_limit + aux.resolution) # with reserve to be averaged
    nm = nm[flag]

    # Spectral smoothing and down scaling
    current_resolution = aux.get_resolution(cube.spectral_axis.value)
    sd = aux.gaussian_width(current_resolution, aux.resolution)
    print('Beginning spectral smoothing')
    cube = cube.spectral_smooth(Gaussian1DKernel(sd)) # parallel execution doesn't work
    print('Beginning spectral down scaling')
    cube = cube.spectral_interpolate(nm * u.nm, suppress_smooth_warning=True)
    print() # workaround "enter" for interpolation progress bar

    # Spatial smoothing and down scaling
    # Replaced by image_core.SpectralCube.downscale()
    #if isinstance(pixels_number, int):
    #    smooth_factor = int(cube.shape[1] * cube.shape[2] / pixels_number)
    #    print('Beginning spatial smoothing')
    #    cube = cube.spatial_smooth(Gaussian2DKernel(smooth_factor))
    #    print('Beginning spatial down scaling')
    #    cube = cube[:,::smooth_factor,::smooth_factor]
    
    return Path(file).name, nm, np.array(cube).transpose((0, 2, 1))
