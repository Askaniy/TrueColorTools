import numpy as np

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

