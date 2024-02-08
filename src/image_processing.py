""" Processes raw image input into a picture that can be shown and saved. """

from typing import Callable
from traceback import format_exc
from io import BytesIO
from time import strftime
from PIL import Image
import numpy as np
import src.auxiliary as aux
import src.image_core as ic
import src.color_processing as cp


def create_log(window) -> Callable:
    """ Creates a function that sends messages to the window main thread """
    def log(message: str):
        window.write_event_value(('T2_thread', message), None)
    return log

def image_parser(
        window, image_mode: int, save_folder: str, pixels_limit: int, filters: list, files: list, single_file: str,
        gamma_correction: bool, srgb: bool, makebright: bool, desun: bool, exposure: float
    ):
    """ Receives user input and performs processing in a parallel thread """
    preview_flag = save_folder == ''
    log = create_log(window)
    log('Starting the image processing thread')
    try:
        match image_mode:
            # Multiband image
            case 0:
                pass
            # RGB image
            case 1:
                pass
            # Spectral cube
            case 2:
                log('Importing spectral cube (may take a long time for the first time)')
                cube = ic.SpectralCube.from_file(single_file)
                if preview_flag:
                    log('Down scaling')
                    cube = cube.downscale(pixels_limit)
                log('Extrapolating')
                cube = cube.to_scope(aux.visible_range)
                log('Color calculating')
                img = cube2img(cube, gamma_correction, srgb, makebright, desun, exposure)
        if preview_flag:
            window.write_event_value(('T2_thread', 'Sending the resulting preview to the main thread'), img)
        else:
            img.save(f'{save_folder}/TCT_{strftime("%Y-%m-%d_%H-%M")}.png')
    except Exception:
        log(f'Image processing failed with {format_exc(limit=0).strip()}')
        print(format_exc())

def cube2img(cube: ic.SpectralCube, gamma_correction: bool, srgb: bool, makebright: bool, desun: bool, exposure: float):
    """ Creates a Pillow image from the spectral cube """
    # TODO: add CIE white points support
    l, x, y = cube.br.shape
    rgb = np.empty((3, x, y))
    rgb[0,:,:] = cube @ cp.r
    rgb[1,:,:] = cube @ cp.g
    rgb[2,:,:] = cube @ cp.b
    if makebright:
        rgb /= rgb.max()
    if gamma_correction:
        rgb = cp.gamma_correction(rgb)
    rgb *= exposure
    rgb = (255 * rgb).astype(np.uint8)
    return Image.fromarray(rgb.transpose())

def convert_to_bytes(img: Image.Image):
    """ Prepares PIL's image to be displayed in the window """
    bio = BytesIO()
    img.save(bio, format='png')
    del img
    return bio.getvalue()

def img2array(img: Image.Image):
    """
    Converting a Pillow image to a numpy array
    1.5-2.5 times faster than np.array() and np.asarray()
    Based on https://habr.com/ru/articles/545850/
    """
    img.load()
    e = Image._getencoder(img.mode, 'raw', img.mode)
    e.setimage(img.im)
    shape, type_str = Image._conv_type_shape(img)
    data = np.empty(shape, dtype=np.dtype(type_str))
    mem = data.data.cast('B', (data.data.nbytes,))
    bufsize, s, offset = 65536, 0, 0
    while not s:
        l, s, d = e.encode(bufsize)
        mem[offset:offset + len(d)] = d
        offset += len(d)
    if s < 0:
        raise RuntimeError(f'encoder error {s} in tobytes')
    return data
