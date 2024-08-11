"""
Provides classes for obtaining and processing color from the spectrum.
Needs improvement, see https://github.com/Askaniy/TrueColorTools/issues/22
"""

from typing import Sequence
from copy import deepcopy
import numpy as np
from src.auxiliary import gamma_correction
from src.core import *


def xy2xyz(xy):
    return np.array((xy[0], xy[1], 1-xy[0]-xy[0])) # (x, y, 1-x-y)

class ColorSystem:
    def __init__(self, red: Sequence, green: Sequence, blue: Sequence, white: Sequence):
        """
        Initialise the ColorSystem object.
        The implementation is based on https://scipython.com/blog/converting-a-spectrum-to-a-colour/
        Defining the color system requires four 2d vectors (primary illuminants and the "white point")
        """
        self.red, self.green, self.blue, self.white = map(xy2xyz, [red, green, blue, white]) # chromaticities
        self.M = np.vstack((self.red, self.green, self.blue)).T # the chromaticity matrix (rgb -> xyz) and its inverse
        self.MI = np.linalg.inv(self.M) # white scaling array
        self.wscale = self.MI.dot(self.white) # xyz -> rgb transformation matrix
        self.T = self.MI / self.wscale[:, np.newaxis]

# Used white points
illuminant_E = (1/3, 1/3)
#illuminant_D65 = (0.3127, 0.3291)

# Used color systems
srgb_system = ColorSystem((0.64, 0.33), (0.30, 0.60), (0.15, 0.06), illuminant_E)
#hdtv_system = ColorSystem((0.67, 0.33), (0.21, 0.71), (0.15, 0.06), illuminant_D65)
#smpte_system = ColorSystem((0.63, 0.34), (0.31, 0.595), (0.155, 0.070), illuminant_D65)

# Stiles & Burch (1959) 2-deg color matching data, direct experimental data
# http://www.cvrl.org/stilesburch2_ind.htm
# Edge sensitivity modulo values less than 10⁴ were previously removed
rgb_cmf = FilterSystem.from_list(('StilesBurch2deg.r', 'StilesBurch2deg.g', 'StilesBurch2deg.b'))

# CIE XYZ functions transformed from the CIE (2006) LMS functions, 2-deg
# http://www.cvrl.org/ciexyzpr.htm
# Edge sensitivity values less than 10⁴ were previously removed
xyz_cmf = FilterSystem.from_list(('cie2deg.x', 'cie2deg.y', 'cie2deg.z')) / 339.12
# TODO: find a correct way to calibrate brightness for albedo!
# 339.12 was guessed so that the equal-energy spectrum of unit brightness has color (1, 1, 1)


class ColorImage:
    """
    A class for working with three-channel images.
    Internal representation as a numpy array of the shape (3, hight, width) with values between 0 and 1.
    (Note that the PhotospectralCube class has a transposed order of the axes.)
    """

    def __init__(self, rgb: Sequence, maximize_brightness=True):
        """
        The albedo flag on means that you have already normalized the brightness over the range.
        By default, initialization implies normalization and you get chromaticity.

        Args:
        - `rgb` (Sequence): array of three values that are red, green and blue
        - `maximize_brightness` (bool): to find the maximum value of the array and divide by it
        """
        self.rgb = np.clip(np.flip(np.nan_to_num(rgb)), 0, None, dtype='float')
        if maximize_brightness and rgb.max() != 0:
            self.rgb /= self.rgb.max()

    @staticmethod
    def from_spectral_data(spectral_cube: SpectralCube, maximize_brightness=True, srgb=False):
        """ Convolves the spectral cube with one of the available CMF systems """
        # TODO: add sRGB support for images!
        return ColorImage((spectral_cube @ rgb_cmf).br, maximize_brightness)

    def gamma_corrected(self):
        """ Creates a new Color object with applied gamma correction """
        other = deepcopy(self)
        other.rgb = gamma_correction(other.rgb)
        return other
    
    def grayscale(self):
        """ Converts rgb values to grayscale using sRGB luminance of the CIE 1931 """
        return np.dot(self.rgb, (0.2126, 0.7152, 0.0722))


class ColorPoint(ColorImage):
    """
    A class for working with three-channel point.
    Internal representation as a numpy array of the shape (3) with values between 0 and 1.
    """

    @staticmethod
    def from_spectral_data(spectrum: Spectrum, maximize_brightness=True, srgb=False):
        """ Convolves the spectrum with one of the available CMF systems """
        if srgb:
            xyz = (spectrum @ xyz_cmf).br
            rgb = srgb_system.T.dot(xyz)
            if np.any(rgb < 0):
                print(f'# Note for the Color object "{spectrum.name}"')
                print(f'- RGB derived from XYZ turned out to be outside the color space: rgb={rgb}')
                rgb -= rgb.min()
                print(f'- Approximating by desaturating: rgb={rgb}')
        else:
            rgb = (spectrum @ rgb_cmf).br
        return ColorPoint(rgb, maximize_brightness)

    def to_bit(self, bit: int) -> np.ndarray:
        """ Returns rounded color array, scaled to the appropriate power of two """
        return self.rgb * (2**bit - 1)

    def to_html(self):
        """ Converts fractional rgb values to HTML-style hex string """
        html = '#{:02x}{:02x}{:02x}'.format(*self.to_bit(8).round().astype('int'))
        if len(html) != 7:
            #print(f'# Note for the Color object "{self.name}"')
            #print(f'- HTML-style color code feels wrong: {html}')
            html = '#FFFFFF'
            #print(f'- It has been replaced with {html}.')
        return html
