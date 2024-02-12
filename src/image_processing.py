""" Processes raw image input into a picture that can be shown and saved. """

from typing import Callable
from traceback import format_exc
from io import BytesIO
from time import strftime, monotonic
from PIL import Image
import numpy as np
import src.auxiliary as aux
import src.image_core as ic
import src.image_import as ii
import src.color_processing as cp
from src.data_processing import sun_norm


def create_log(window) -> Callable:
    """ Creates a function that sends messages to the window main thread """
    def log(message: str):
        window.write_event_value(('T2_thread', f'{strftime("%H:%M:%S")} {message}'), None)
    return log

def image_parser(
        window, image_mode: int, save_folder: str, pixels_limit: int, single_file: str, files: list, filters: list, factors: list,
        gamma_correction: bool, srgb: bool, makebright: bool, desun: bool, factor: float
    ):
    """ Receives user input and performs processing in a parallel thread """
    preview_flag = save_folder == ''
    log = create_log(window)
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
                factors = np.array(factors, dtype='float64')[not_empty_files]
                log(f'Importing the images')
                cube = ic.PhotometricCube(filters, ii.bw_list_reader(files)).sorted()
                if preview_flag:
                    log('Down scaling')
                    cube = cube.downscale(pixels_limit)
                cube.br = (cube.br.T * factors).T
                if desun:
                    log('Removing Sun as emitter')
                    cube /= sun_norm
                log('Interpolating and extrapolating')
                cube = cube.to_scope(aux.visible_range)
                log('Color calculating')
                img = cube2img(cube, gamma_correction, srgb, makebright, factor)
            # RGB image
            case 1:
                factors = np.array(factors, dtype='float64')
                log(f'Importing the RGB image')
                cube = ic.PhotometricCube(filters, ii.rgb_reader(single_file)).sorted()
                if preview_flag:
                    log('Down scaling')
                    cube = cube.downscale(pixels_limit)
                cube.br = (cube.br.T * factors).T
                if desun:
                    log('Removing Sun as emitter')
                    cube /= sun_norm
                log('Interpolating and extrapolating')
                cube = cube.to_scope(aux.visible_range)
                log('Color calculating')
                img = cube2img(cube, gamma_correction, srgb, makebright, factor)
            # Spectral cube
            case 2:
                log('Importing the spectral cube (only the first loading is slow)')
                cube = ic.SpectralCube.from_file(single_file)
                if preview_flag:
                    log('Down scaling')
                    cube = cube.downscale(pixels_limit)
                if desun:
                    log('Removing Sun as emitter')
                    cube /= sun_norm
                log('Extrapolating')
                cube = cube.to_scope(aux.visible_range)
                log('Color calculating')
                img = cube2img(cube, gamma_correction, srgb, makebright, factor)
        end_time = monotonic()
        time = end_time-start_time
        speed = img.height * img.width / time
        log(f'Processing took {time:.1f} seconds, average speed is {speed:.1f} px/sec')
        if preview_flag:
            window.write_event_value(('T2_thread', 'Sending the resulting preview to the main thread'), img)
        else:
            img.save(f'{save_folder}/TCT_{strftime("%Y-%m-%d_%H-%M")}.png')
    except Exception:
        log(f'Image processing failed with {format_exc(limit=0).strip()}')
        print(format_exc())

def cube2img(cube: ic.SpectralCube, gamma_correction: bool, srgb: bool, makebright: bool, factor: float):
    """ Creates a Pillow image from the spectral cube """
    # TODO: add CIE white points support
    _, x, y = cube.br.shape
    rgb = np.empty((3, x, y))
    rgb[0] = cube @ cp.r
    rgb[1] = cube @ cp.g
    rgb[2] = cube @ cp.b
    if makebright:
        rgb /= rgb.max()
    rgb *= factor
    rgb = np.clip(rgb, 0, 1)
    if gamma_correction:
        rgb = cp.gamma_correction(rgb)
    rgb = (255 * rgb).astype(np.uint8)
    return Image.fromarray(rgb.transpose())

def convert_to_bytes(img: Image.Image):
    """ Prepares PIL's image to be displayed in the window """
    bio = BytesIO()
    img.save(bio, format='png')
    del img
    return bio.getvalue()
