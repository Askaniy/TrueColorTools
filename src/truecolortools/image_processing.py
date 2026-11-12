""" Processes raw image input into a picture that can be shown and saved. """

from collections.abc import Callable
from io import BytesIO
from math import sqrt
from time import monotonic
from traceback import format_exc
from typing import cast

import astrocolor as ac
import numpy as np
from PIL import Image
from tifffile import imwrite

import truecolortools.image_import as ii
from truecolortools.core import sun_norm


def image_parser(
        image_mode: int, preview_flag: bool, px_lower_limit: int, px_upper_limit: int,
        single_file: str, files: list, filters: list, formulas: list,
        sun_divide: bool, sun_multiply: bool, photons: bool, upscale: bool, log: Callable
    ):
    """ Receives user input and performs processing in a parallel thread """
    log('Starting the image processing thread')
    start_time = monotonic()
    try:
        # AstroColor splits large color cubes into batches internally.
        ac.Config.pixel_upper_limit = px_upper_limit
        match image_mode:
            case 0: # Multiband image
                selected = [
                    (file, filter_obj, formula)
                    for file, filter_obj, formula in zip(files, filters, formulas)
                    if file != ''
                ]
                files = [item[0] for item in selected]
                selected_filters = [item[1] for item in selected]
                formulas = [item[2] for item in selected]
                filter_set = ac.FilterSet.from_filters(selected_filters)
                log('Importing the images')
                cube: ac.PhotospectralCube | ac.SpectralCube = ac.PhotospectralCube(
                    filter_set,
                    ii.bw_list_reader(files, formulas),
                )
            case 1: # RGB image
                filter_set = ac.FilterSet.from_filters(filters)
                log('Importing the RGB image')
                cube = ac.PhotospectralCube(filter_set, ii.rgb_reader(single_file, formulas))
            case 2: # Spectral cube
                log('Importing the spectral cube')
                wavelength_nm, spectral_dist = ii.cube_reader(single_file)
                cube = ac.SpectralCube(wavelength_nm, spectral_dist)
            case _:
                raise ValueError(f'Unknown image mode: {image_mode}')
        if preview_flag:
            log('Downscaling')
            cube = cube.downscale(px_lower_limit)
        if photons:
            log('Converting photon spectral density to energy density')
            cube = cube.convert_from_photon_spectral_density()
        sun = cast(ac.Spectrum, sun_norm)
        if sun_divide:
            log('Dividing by Solar spectrum to remove the reflected color of the Sun')
            cube = cube / sun
        if sun_multiply:
            log('Multiplying by Solar spectrum to simulate the reflection of sunlight')
            cube = cube * sun
        px_num = cube.spatial_size
        log('Color calculating')
        img = ac.ColorImage.from_spectral_data(cube)
        if upscale and px_num < px_lower_limit and (times := round(sqrt(px_lower_limit / px_num))) != 1:
            log('Upscaling')
            img = img.upscale(times)
        # End of processing, summarizing
        time = monotonic() - start_time
        speed = px_num / time
        log(f'Processing took {time:.1f} seconds, average speed is {speed:.1f} px/sec')
        if preview_flag:
            log('Sending the preview to the main thread', img)
        else:
            log('Sending the image to the main thread', img)
    except Exception:  # noqa: BLE001
        log(f'Image processing failed with {format_exc(limit=0).strip()}')
        print(format_exc())


def color_image_to_bytes(img: ac.ColorImage, settings: ac.DisplaySettings) -> bytes:
    """ Renders a linear color image and encodes it as PNG bytes for the GUI. """
    arr = np.round(np.clip(img.render(settings), 0, 1) * 255).astype('uint8')
    bio = BytesIO()
    Image.fromarray(arr.transpose((1, 2, 0))).save(bio, format='png')
    return bio.getvalue()


supported_formats = ('JPEG int8', 'PNG int8', 'TIFF int16', 'TIFF int32', 'TIFF float16', 'TIFF float32', 'TIFF float64')

def save_image(arr: np.ndarray, format: str, image_name: str):
    match format:
        case 'JPEG int8':
            arr = np.round(np.clip(arr, 0, 1) * 255).astype('uint8')
            Image.fromarray(arr.T).save(image_name + '.jpg', quality=95)
        case 'PNG int8':
            arr = np.round(np.clip(arr, 0, 1) * 255).astype('uint8')
            Image.fromarray(arr.T).save(image_name + '.png', optimize=True)
        case 'TIFF int16':
            arr = np.round(np.clip(arr, 0, 1) * 65535).astype('uint16')
            imwrite(image_name + '.tif', arr.T, photometric='rgb')
        case 'TIFF int32':
            arr = np.round(np.clip(arr, 0, 1) * 4294967295).astype('uint32')
            imwrite(image_name + '.tif', arr.T, photometric='rgb')
        case 'TIFF float16':
            arr = arr.astype('float16')
            imwrite(image_name + '.tif', arr.T, photometric='rgb')
        case 'TIFF float32':
            arr = arr.astype('float32')
            imwrite(image_name + '.tif', arr.T, photometric='rgb')
        case 'TIFF float64':
            arr = arr.astype('float64')
            imwrite(image_name + '.tif', arr.T, photometric='rgb')
