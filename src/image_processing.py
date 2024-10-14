""" Processes raw image input into a picture that can be shown and saved. """

from typing import Callable
from traceback import format_exc
from io import BytesIO
from time import strftime, monotonic
from math import sqrt
from PIL import Image
import numpy as np

from src.core import *
import src.image_import as ii


def image_parser(
        image_mode: int,
        preview_flag: bool = False,
        save_folder: str = '',
        pixels_limit: int = 256*128,
        single_file: str = None,
        files: list = None,
        filters: list = None,
        formulas: list = None,
        gamma_correction: bool = True,
        srgb: bool = False,
        maximize_brightness: bool = False,
        desun: bool = False,
        photons: bool = False,
        factor: float = 1.,
        upscale: bool = True,
        log: Callable = print
    ):
    """ Receives user input and performs processing in a parallel thread """
    log('Starting the image processing thread')
    start_time = monotonic()
    try:
        match image_mode:
            case 0: # Multiband image
                files = np.array(files)
                not_empty_files = np.where(files != '')
                files = files[not_empty_files]
                filters = np.array(filters)[not_empty_files]
                formulas = np.array(formulas)[not_empty_files]
                filter_system = FilterSystem.from_list(filters)
                log('Importing the images')
                cube = PhotospectralCube(filter_system, ii.bw_list_reader(files, formulas))
            case 1: # RGB image
                filter_system = FilterSystem.from_list(filters)
                log('Importing the RGB image')
                cube = PhotospectralCube(filter_system, ii.rgb_reader(single_file, formulas))
            case 2: # Spectral cube
                log('Importing the spectral cube (only the first loading is slow)')
                cube = SpectralCube.from_file(single_file)
        if preview_flag:
            log('Downscaling')
            cube = cube.downscale(pixels_limit)
        if photons:
            log('Converting photon spectral density to energy density')
            cube = cube.convert_from_photon_spectral_density()
        if desun:
            log('Removing Sun as emitter')
            cube /= sun_norm
        log('Color calculating')
        img = ColorImage.from_spectral_data(cube, maximize_brightness, srgb)
        if factor != 1:
            log('Scaling brightness')
            img *= factor
        if gamma_correction:
            log('Gamma correcting')
            img = img.gamma_corrected()
        pixels_num = img.width * img.height
        if upscale and pixels_num < pixels_limit and (times := round(sqrt(pixels_limit / pixels_num))) != 1:
            log('Upscaling')
            img = img.upscale(times)
        img = img.to_pillow_image()
        # End of processing, summarizing
        time = monotonic() - start_time
        speed = pixels_num / time
        log(f'Processing took {time:.1f} seconds, average speed is {speed:.1f} px/sec')
        if preview_flag:
            log('Sending the resulting preview to the main thread', img)
        else:
            img.save(f'{save_folder}/TCT_{strftime("%Y-%m-%d_%H-%M-%S")}.png')
    except Exception:
        log(f'Image processing failed with {format_exc(limit=0).strip()}')
        print(format_exc())

def convert_to_bytes(img: Image.Image):
    """ Prepares PIL's image to be displayed in the window """
    bio = BytesIO()
    img.save(bio, format='png')
    del img
    return bio.getvalue()
