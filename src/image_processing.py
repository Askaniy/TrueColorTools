""" Processes raw image input into a picture that can be shown and saved. """

from collections.abc import Callable
from traceback import format_exc
from time import monotonic
from math import sqrt, ceil
import numpy as np
from PIL import Image
from tifffile import imwrite

from src.core import FilterSystem, SpectralCube, PhotospectralCube, ColorLine, ColorImage, sun_norm, xyz_color_system
import src.image_import as ii


def image_parser(
        image_mode: int, preview_flag: bool, px_lower_limit: int, px_upper_limit: int,
        single_file: str, files: list, filters: list, formulas: list,
        desun: bool, photons: bool, upscale: bool, log: Callable
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
                log('Importing the spectral cube')
                cube = SpectralCube.from_file(single_file)
        if preview_flag:
            log('Downscaling')
            cube = cube.downscale(px_lower_limit)
        if photons:
            log('Converting photon spectral density to energy density')
            cube = cube.convert_from_photon_spectral_density()
        if desun:
            log('Removing Sun as emitter')
            cube /= sun_norm
        px_num = cube.size
        if preview_flag or px_num < px_upper_limit:
            log('Color calculating')
            img = ColorImage.from_spectral_data(cube)
        else:
            square = cube.flatten()
            chunk_num = ceil(px_num / px_upper_limit)
            img_array = np.empty((3, px_num))
            for i in range(chunk_num):
                j = i+1
                try:
                    chunk = square[i*px_upper_limit:j*px_upper_limit]
                except IndexError:
                    chunk = square[i*px_upper_limit:]
                img_chunk = ColorLine.from_spectral_data(chunk)
                img_array[:,i*px_upper_limit:j*px_upper_limit] = img_chunk.br
                log(f'Color calculated for {j} chunks out of {chunk_num}')
            img = ColorImage(img_array.reshape(3, cube.width, cube.height), xyz_color_system)
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
    except Exception:
        log(f'Image processing failed with {format_exc(limit=0).strip()}')
        print(format_exc())


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
