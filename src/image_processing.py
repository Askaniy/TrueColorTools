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
        desun: bool = False,
        photons: bool = False,
        makebright: bool = False,
        factor: float = 1.,
        enlarge: bool = True,
        log: Callable = print
    ):
    """ Receives user input and performs processing in a parallel thread """
    log('Starting the image processing thread')
    start_time = monotonic()
    try:
        match image_mode:
            # Multiband image
            case 0:
                files = np.array(files)
                not_empty_files = np.where(files != '')
                files = files[not_empty_files]
                filters = np.array(filters)[not_empty_files]
                formulas = np.array(formulas)[not_empty_files]
                log(f'Importing the images')
                cube = PhotospectralCube(filters, ii.bw_list_reader(files, formulas))
                if preview_flag:
                    log('Down scaling')
                    cube = cube.downscale(pixels_limit)
                if photons:
                    log('Converting photon spectral density to energy density')
                    cube = cube.convert_from_photon_spectral_density()
                if desun:
                    log('Removing Sun as emitter')
                    cube /= sun_norm
                log('Interpolating and extrapolating')
                cube = cube.to_scope(visible_range)
                log('Color calculating')
                img = cube2img(cube, gamma_correction, srgb, makebright, factor)
            # RGB image
            case 1:
                log(f'Importing the RGB image')
                cube = PhotospectralCube(filters, ii.rgb_reader(single_file, formulas))
                if preview_flag:
                    log('Down scaling')
                    cube = cube.downscale(pixels_limit)
                if photons:
                    log('Converting photon spectral density to energy density')
                    cube = cube.convert_from_photon_spectral_density()
                if desun:
                    log('Removing Sun as emitter')
                    cube /= sun_norm
                log('Interpolating and extrapolating')
                cube = cube.to_scope(visible_range)
                log('Color calculating')
                img = cube2img(cube, gamma_correction, srgb, makebright, factor)
            # Spectral cube
            case 2:
                log('Importing the spectral cube (only the first loading is slow)')
                cube = SpectralCube.from_file(single_file)
                if preview_flag:
                    log('Down scaling')
                    cube = cube.downscale(pixels_limit)
                if photons:
                    log('Converting photon spectral density to energy density')
                    cube = cube.convert_from_photon_spectral_density()
                if desun:
                    log('Removing Sun as emitter')
                    cube /= sun_norm
                log('Extrapolating')
                cube = cube.to_scope(visible_range)
                log('Color calculating')
                img = cube2img(cube, gamma_correction, srgb, makebright, factor)
        time = monotonic() - start_time
        pixels_num = img.width * img.height
        speed = pixels_num / time
        log(f'Processing took {time:.1f} seconds, average speed is {speed:.1f} px/sec')
        if enlarge and pixels_num < pixels_limit:
            factor = round(sqrt(pixels_limit / pixels_num))
            img = img.resize((img.width * factor, img.height * factor), Image.Resampling.NEAREST)
        if preview_flag:
            log('Sending the resulting preview to the main thread', (img, cube.median_spectrum()))
        else:
            img.save(f'{save_folder}/TCT_{strftime("%Y-%m-%d_%H-%M-%S")}.png')
    except Exception:
        log(f'Image processing failed with {format_exc(limit=0).strip()}')
        print(format_exc())

def cube2img(cube: SpectralCube, gamma_correction: bool, srgb: bool, makebright: bool, factor: float):
    """ Creates a Pillow image from the spectral cube """
    # TODO: add CIE white points support
    _, x, y = cube.br.shape
    img = ColorImage(cube.br, makebright)
    img.br = np.clip(img.br * factor, 0, 1)
    if gamma_correction:
        img = img.gamma_corrected()
    return Image.fromarray((255 * img.br).astype('uint8').transpose())

def convert_to_bytes(img: Image.Image):
    """ Prepares PIL's image to be displayed in the window """
    bio = BytesIO()
    img.save(bio, format='png')
    del img
    return bio.getvalue()
