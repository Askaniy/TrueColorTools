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
                log('Importing RGB image')
                rgb_img = Image.open(single_file)
                rgb_img = rgb_img.convert(to_supported_mode(rgb_img.mode))
                br = img2array(rgb_img).astype('float64') / color_depth(rgb_img.mode)
                cube = ic.PhotometricCube(filters, br.T).sorted()
                if preview_flag:
                    log('Down scaling')
                    cube = cube.downscale(pixels_limit)
                log('Extrapolating')
                cube = cube.to_scope(aux.visible_range)
                log('Color calculating')
                img = cube2img(cube, gamma_correction, srgb, makebright, exposure)
            # Spectral cube
            case 2:
                log('Importing spectral cube (may take a long time for the first loading)')
                cube = ic.SpectralCube.from_file(single_file)
                if preview_flag:
                    log('Down scaling')
                    cube = cube.downscale(pixels_limit)
                log('Extrapolating')
                cube = cube.to_scope(aux.visible_range)
                log('Color calculating')
                img = cube2img(cube, gamma_correction, srgb, makebright, exposure)
        if preview_flag:
            window.write_event_value(('T2_thread', 'Sending the resulting preview to the main thread'), img)
        else:
            img.save(f'{save_folder}/TCT_{strftime("%Y-%m-%d_%H-%M")}.png')
    except Exception:
        log(f'Image processing failed with {format_exc(limit=0).strip()}')
        print(format_exc())

def cube2img(cube: ic.SpectralCube, gamma_correction: bool, srgb: bool, makebright: bool, exposure: float):
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

def to_supported_mode(mode: str):
    """ Corresponds the image mode of the Pillow library and supported one """
    # https://pillow.readthedocs.io/en/latest/handbook/concepts.html#concept-modes
    match mode:
        case 'P' | 'PA' | 'RGB' | 'RGBA' | 'RGBX' | 'RGBa' | 'CMYK' | 'YCbCr' | 'LAB' | 'HSV': # 8-bit indexed color palette, alpha channels, color spaces
            return 'RGB'
        case 'L' | 'La' | 'LA': # 8-bit grayscale
            return 'L'
        case 'I' | 'I;16' | 'I;16L' | 'I;16B' | 'I;16N' | 'BGR;15' | 'BGR;16' | 'BGR;24': # 32-bit grayscale
            return 'I'
        case 'F': # 32-bit floating point grayscale
            return 'F'
        case _:
            print(f'Mode {mode} is not recognized. Would be processed as RGB image.')
            return 'RGB'

def color_depth(mode: str):
    """ Corresponds the image mode of the Pillow library and its bitness """
    match mode:
        case 'RGB' | 'L': # 8 bit
            return 255
        case 'I' | 'F': # 32 bit
            return 65535
        case _:
            print(f'Mode {mode} is not supported. Would be processed as 8-bit image.')
            return 255