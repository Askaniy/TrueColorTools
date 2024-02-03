""" Processes raw image input into a picture that can be shown and saved. """

from io import BytesIO
from PIL import Image
from time import strftime


def convert_to_bytes(img: Image.Image):
    """ Prepares PIL's image to be displayed in the window """
    bio = BytesIO()
    img.save(bio, format='png')
    del img
    return bio.getvalue()

def save(img: Image.Image, folder: str):
    """ Saves the image in the specified folder """
    img.save(f'{folder}/TCT_{strftime("%Y-%m-%d_%H-%M")}.png')

