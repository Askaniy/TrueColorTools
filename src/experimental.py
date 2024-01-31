""" Provides incomplete or unnecessary functionality. """

import numpy as np


h = 6.626e-34 # Planck constant
c = 299792458 # Speed of light
k = 1.381e-23 # Boltzmann constant
const1 = 2 * np.pi * h * c * c
const2 = h * c / k
r = 6.957e8 # Solar radius, meters
au = 149597870700 # astronomical unit, meters
w = (1 - np.sqrt(1 - (r / au)**2)) / 2 # dilution to compare with Solar light on Earth
temp_coef_to_make_it_work = 1.8 / 0.448 # 1.8 is expected of irradiance(500, 5770), 0.448 is actual. TODO

# Now it does not work as intended: the spectrum should be comparable to the sun_SI
def irradiance(nm: int|float|np.ndarray, T: int|float) -> float|np.ndarray:
    m = nm / 1e9
    return temp_coef_to_make_it_work * w * const1 / (m**5 * (np.exp(const2 / (m * T)) - 1)) / 1e9 # per m -> per nm



# Phase curves processing functions
def lambert(phase: float):
    phi = abs(np.deg2rad(phase))
    return (np.sin(phi) + np.pi * np.cos(phi) - phi * np.cos(phi)) / np.pi # * 2/3 * albedo


# Linear extrapolation
def line_generator(x1, y1, x2, y2):
    return np.vectorize(lambda wl: y1 + (wl - x1) * (y2 - y1) / (x2 - x1))


# Magnitudes processing functions

V = 2.518021002e-8 # 1 Vega in W/m^2, https://arxiv.org/abs/1510.06262

def mag2intensity(m: int|float|np.ndarray):
    return V * 10**(-0.4 * m)

def intensity2mag(e):
    return -2.5 * np.log10(e / V)



# Legacy core.py multiresolution spectrum processing
# Code of summer 2023. Simplified in November 2023.

resolutions = (5, 10, 20, 40, 80, 160) # nm
def standardize_resolution(input: int):
    """ Redirects the step size to one of the valid values """
    res = resolutions[-1] # max possible step
    for i in range(1, len(resolutions)):
        if input < resolutions[i]:
            res = resolutions[i-1] # accuracy is always in reserve
            break
    return res

#    def to_resolution(self, request: int):
#        """ Returns a new Spectrum object with changed wavelength grid step size """
#        other = deepcopy(self)
#        if request not in resolutions:
#            print(f'# Note for the Spectrum object "{self.name}"')
#            print(f'- Resolution change allowed only for {resolutions} nm, not {request} nm.')
#            request = standardize_resolution(request)
#            print(f'- The optimal resolution was chosen automatically: {request} nm.')
#        if request > other.res:
#            while request != other.res: # remove all odd elements
#                other.res *= 2
#                other.nm = np.arange(other.nm[0], other.nm[-1]+1, other.res, dtype=int)
#                other.br = other.br[::2]
#        elif request < other.res:
#            while request != other.res: # middle linear interpolation
#                other.res = int(other.res / 2)
#                other.nm = np.arange(other.nm[0], other.nm[-1]+1, other.res, dtype=int)
#                other.br = custom_interp(other.br)
#        else:
#            print(f'# Note for the Spectrum object "{self.name}"')
#            print(f'- Current and requested resolutions are the same ({request} nm), nothing changed.')
#        return other

