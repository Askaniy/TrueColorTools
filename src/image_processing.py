""" Processes raw image input into a picture that can be shown and saved. """

from io import BytesIO
from time import strftime
from PIL import Image
import numpy as np
from src.data_core import Spectrum
from src.image_core import SpectralCube
import src.color_processing as cp


def cube2img(cube: SpectralCube, makebright: bool = False, gamma_correction: bool = False):
    """ Creates a Pillow image from the spectral cube """
    # TODO: add CIE white points support
    l, x, y = cube.br.shape
    cube_rgb = np.empty((3, x, y))
    cube_rgb[0,:,:] = cube @ cp.r
    cube_rgb[1,:,:] = cube @ cp.g
    cube_rgb[2,:,:] = cube @ cp.b
    if makebright:
        cube_rgb /= cube_rgb.max()
    if gamma_correction:
        cube_rgb = cp.gamma_correction(cube_rgb)
    return Image.fromarray(cube_rgb.transpose())

def save(img: Image.Image, folder: str):
    """ Saves the image in the specified folder """
    img.save(f'{folder}/TCT_{strftime("%Y-%m-%d_%H-%M")}.png')

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
