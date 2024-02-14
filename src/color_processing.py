"""
Provides classes for obtaining and processing color from the spectrum.
Needs improvement, see https://github.com/Askaniy/TrueColorTools/issues/22
"""

from typing import Sequence
from copy import deepcopy
import numpy as np
from src.data_core import Spectrum


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
srgb = ColorSystem((0.64, 0.33), (0.30, 0.60), (0.15, 0.06), illuminant_E)
#hdtv = ColorSystem((0.67, 0.33), (0.21, 0.71), (0.15, 0.06), illuminant_D65)
#smpte = ColorSystem((0.63, 0.34), (0.31, 0.595), (0.155, 0.070), illuminant_D65)

# Stiles & Burch (1959) 2-deg color matching data, direct experimental data
# http://www.cvrl.org/stilesburch2_ind.htm
# Edge sensitivity modulo values less than 10⁴ were previously removed
r = Spectrum('r CMF', *np.loadtxt('src/cmf/StilesBurch2deg.r.dat').transpose()).scaled_by_area()
g = Spectrum('g CMF', *np.loadtxt('src/cmf/StilesBurch2deg.g.dat').transpose()).scaled_by_area()
b = Spectrum('b CMF', *np.loadtxt('src/cmf/StilesBurch2deg.b.dat').transpose()).scaled_by_area()

# CIE XYZ functions transformed from the CIE (2006) LMS functions, 10-deg
# http://www.cvrl.org/ciexyzpr.htm
# Edge sensitivity values less than 10⁴ were previously removed
x = Spectrum('x CMF', *np.loadtxt('src/cmf/cie2deg.x.dat').transpose())
y = Spectrum('y CMF', *np.loadtxt('src/cmf/cie2deg.y.dat').transpose())
z = Spectrum('z CMF', *np.loadtxt('src/cmf/cie2deg.z.dat').transpose())
# Normalization. TODO: find a correct way to calibrate brightness for albedo!
# 339.12 was guessed so that the equal-energy spectrum of unit brightness has color (1, 1, 1)
x.br /= 339.12
y.br /= 339.12
z.br /= 339.12



gamma_correction = np.vectorize(lambda p: p * 12.92 if p < 0.0031308 else 1.055 * p**(1.0/2.4) - 0.055)

class Color:
    """ Class to work with color represented by three float values in [0, 1] range. """

    def __init__(self, name: str, rgb: Sequence, albedo=False):
        """
        The albedo flag on means that you have already normalized the brightness over the range.
        By default, initialization implies normalization and you get chromaticity.

        Args:
        - `name` (str): human-readable identification. May include references (separated by "|") and a note (separated by ":")
        - `rgb` (Sequence): array of three values that are red, green and blue
        - `albedo` (bool): flag to disable normalization
        """
        self.name = name
        rgb = np.array(rgb, dtype=float)
        if rgb.min() < 0:
            #print(f'# Note for the Color object "{self.name}"')
            #print(f'- Negative values detected during object initialization: rgb={rgb}')
            rgb = np.clip(rgb, 0, None)
            #print('- These values have been replaced with zeros.')
        if rgb.max() != 0 and not albedo: # normalization
            rgb /= rgb.max()
        if np.any(np.isnan(rgb)):
            print(f'# Note for the Color object "{self.name}"')
            print(f'- NaN values detected during object initialization: rgb={rgb}')
            rgb = np.array([0., 0., 0.])
            print(f'- It has been replaced with {rgb}.')
        self.rgb = rgb

    @staticmethod
    def from_spectrum(spectrum: Spectrum, albedo=False):
        """ A simple and concrete color processing method based on experimental eye sensitivity curves """
        rgb = [spectrum @ i for i in (r, g, b)]
        return Color(spectrum.name, rgb, albedo)

    @staticmethod
    def from_spectrum_CIE(spectrum: Spectrum, albedo=False, color_system=srgb):
        """ Conventional color processing method: spectrum -> CIE XYZ -> sRGB with illuminant E """
        xyz = [spectrum @ i for i in (x, y, z)]
        rgb = color_system.T.dot(xyz)
        if np.any(rgb < 0):
            print(f'# Note for the Color object "{spectrum.name}"')
            print(f'- RGB derived from XYZ turned out to be outside the color space: rgb={rgb}')
            rgb -= rgb.min()
            print(f'- Approximating by desaturating: rgb={rgb}')
        return Color(spectrum.name, rgb, albedo)

    def gamma_corrected(self):
        """ Creates a new Color object with applied gamma correction """
        other = deepcopy(self)
        other.rgb = gamma_correction(other.rgb)
        return other

    def to_bit(self, bit: int) -> np.ndarray:
        """ Returns rounded color array, scaled to the appropriate power of two """
        return self.rgb * (2**bit - 1)

    def to_html(self):
        """ Converts fractional rgb values to HTML-style hex string """
        html = '#{:02x}{:02x}{:02x}'.format(*self.to_bit(8).round().astype(int))
        if len(html) != 7:
            #print(f'# Note for the Color object "{self.name}"')
            #print(f'- HTML-style color code feels wrong: {html}')
            html = '#FFFFFF'
            #print(f'- It has been replaced with {html}.')
        return html
