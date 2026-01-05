""" Responsible for converting image data into a working form. """

from collections.abc import Sequence
from pathlib import Path
from functools import lru_cache
import numpy as np
from astropy.io import fits
from PIL import Image

@lru_cache(maxsize=1)
def cube_reader(file: str) -> tuple[np.ndarray, np.ndarray]:
    """ Imports spectral data from the spectral cube in FITS format """
    with fits.open(file) as hdul:
        #hdul.info()
        #print(repr(hdul[0].header))
        br = np.array(hdul['sci'].data).transpose((0, 2, 1))
        nm = np.array(hdul['wavelength'].data)
    return nm, br

@lru_cache(maxsize=8)
def cached_open(file: str):
    """ Increases the speed of image reloading """
    if file.split('.')[-1].lower() in ('fts', 'fit', 'fits'):
        # FITS is tested only with OPAL formatting
        with fits.open(file) as hdul:
            #hdul.info()
            #print(repr(hdul[0].header))
            array = hdul[0].data
        return Image.fromarray(array)
    else:
        return Image.open(file)

def rgb_reader(file: str, formulas: list = None) -> np.ndarray:
    """ Imports spectral data from a RGB image """
    img = cached_open(file)
    img = img.convert(to_supported_mode(img.mode))
    br = np.transpose(img2array(img).astype('float64') / color_depth(img.mode))[::-1]
    if formulas is not None:
        br[0] = eval(formulas[0], {'x': br[0]})
        br[1] = eval(formulas[1], {'x': br[1]})
        br[2] = eval(formulas[2], {'x': br[2]})
    return br

@lru_cache(maxsize=1)
def bw_reader(file: str) -> np.ndarray:
    """ Imports spectral data from a black and white image """
    img = cached_open(file)
    img = img.convert(to_supported_mode(img.mode))
    br = img2array(img).astype('float64') / color_depth(img.mode)
    br = br.transpose()
    if br.ndim == 3:
        print(f'# Note for the image "{Path(file).name}"')
        print('- This is a multi-channel image, but should be single-channel. The brightest channel is extracted.')
        br = br[np.argmax(br.sum(axis=(1,2)))]
    return br

def bw_list_reader(files: Sequence[str], formulas: list[str]) -> np.ndarray:
    """ Imports and combines the list of black and white images into one array """
    br = np.stack([eval(formula, {'x': bw_reader(file)}) for file, formula in zip(files, formulas)])
    return br

def to_supported_mode(mode: str):
    """ Corresponds the image mode of the Pillow library and supported one """
    # https://pillow.readthedocs.io/en/latest/handbook/concepts.html#concept-modes
    match mode:
        case 'P' | 'RGB' | 'RGBX' | 'CMYK' | 'YCbCr' | 'LAB' | 'HSV':
            # 8-bit int color
            return 'RGB'
        case 'PA' | 'RGBA' | 'RGBa':
            # 8-bit int color with alpha channel
            return 'RGB' # return 'RGBA' for alpha channel support
        case 'L':
            # 8-bit int grayscale
            return 'L'
        case 'La' | 'LA':
            # 8-bit int grayscale with alpha channel
            return 'L' # return 'LA' for alpha channel support
        case 'I' | 'I;16' | 'I;16L' | 'I;16B' | 'I;16N':
            # 32-bit int grayscale
            return 'I'
        case 'F':
            # 32-bit float grayscale
            return 'F'
        case _:
            print(f'Mode {mode} is not recognized. Would be processed as RGB image.')
            return 'RGB'

def color_depth(mode: str):
    """ Corresponds the image mode of the Pillow library and its bitness """
    match mode:
        case 'RGB' | 'RGBA' | 'L' | 'LA':
            # 8-bit int
            return 255
        case 'I':
            # 32-bit int
            return 65535
        case 'F':
            # 32-bit float
            return 1
        case _:
            print(f'Mode {mode} is not supported. Would be processed as 8-bit image.')
            return 255

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
        _, s, d = e.encode(bufsize)
        mem[offset:offset + len(d)] = d
        offset += len(d)
    if s < 0:
        raise RuntimeError(f'encoder error {s} in tobytes')
    return data
