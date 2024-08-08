""" File containing constant and functions required in various places, but without dependencies """

import numpy as np
from math import sqrt, ceil
from typing import Sequence


# Constants needed for down scaling spectra and images
fwhm_factor = np.sqrt(8*np.log(2))
hanning_factor = 1129/977


# Math operations

def get_resolution(array: Sequence):
    return np.mean(np.diff(array)) * hanning_factor

def grid(start: int|float, end: int|float, res: int):
    """ Returns uniform grid points for the non-integer range that are divisible by the selected step """
    if (shift := start % res) != 0:
        start += res - shift
    if end % res == 0:
        end += 1 # to include the last point
    return np.arange(start, end, res, dtype='uint16')

def is_smooth(array: Sequence|np.ndarray):
    """ Boolean function, checks the second derivative for sign reversal, a simple criterion for smoothness """
    diff2 = np.diff(np.diff(array, axis=0), axis=0)
    return np.all(diff2 <= 0) | np.all(diff2 >= 0)

def integrate(array: Sequence|np.ndarray, step: int|float):
    """ Riemann sum with midpoint rule for integrating both spectra and spectral cubes """
    return step * 0.5 * np.sum(array[:-1] + array[1:], axis=0)

def gaussian_width(current_resolution, target_resolution):
    return np.sqrt(np.abs(target_resolution**2 - current_resolution**2)) / fwhm_factor

def gaussian_convolution(nm0: Sequence, br0: Sequence, nm1: Sequence, step: int|float):
    """
    Applies Gaussian convolution to a non-uniform sparse mesh. Eliminates holes and noise from spectral axis.

    Args
    - nm0: original spectral axis
    - br0: original spectrum
    - nm1: required uniform grid
    - step: standard deviation of the Gaussian
    """
    factor = -0.5 / step**2 # Gaussian exponent multiplier
    br1 = np.empty_like(nm1, dtype='float64')
    for i in range(len(nm1)):
        br0_convolved = br0 * np.exp(factor*(nm0 - nm1[i])**2)
        br1[i] = np.average(br0, weights=br0_convolved)
    return br1

def spectral_downscaling(nm0: Sequence, br0: np.ndarray, nm1: Sequence, step: int|float):
    """
    Returns spectrum brightness values with decreased resolution.
    Incoming graphs or point clouds may have holes and areas of varying resolution.

    Args
    - nm0: original spectral axis
    - br0: original spectrum or spectral cube
    - nm1: required uniform grid
    - step: resolution of the required uniform grid

    It is known that the Gaussian standard deviation, without any assumptions, must correspond to the grid step.
    Knowing the required "blur" and the local "blur", the missing degree of "blur" can be calculated from
    the error propagation equation.

    The idea is inspired by https://gist.github.com/keflavich/37a2705fb4add9a2491caf2dfa195efd
    """
    cube_flag = br0.ndim == 3 # spectral cube processing
    if br0.min() < 0:
        br0 = np.clip(br0, 1e-10, None) # strange NumPy errors with weights without it
    # Obtaining a graph of standard deviations for a Gaussian
    nm_diff = np.diff(nm0)
    nm_mid = (nm0[1:] + nm0[:-1]) * 0.5
    sd_local = gaussian_convolution(nm_mid, nm_diff, nm1, step*2)
    # Convolution with Gaussian of variable standard deviation
    br1 = np.empty_like(nm1, dtype='float64')
    if cube_flag: 
        br1 = scope2cube(br1, br0.shape[1:3])
    for i in range(len(nm1)):
        sd = gaussian_width(sd_local[i], step) # missing "blur" for required step
        factor = -0.5 / sd**2 # Gaussian exponent multiplier
        gaussian = np.exp(factor*(nm0 - nm1[i])**2)
        if cube_flag:
            gaussian = scope2cube(gaussian, br0.shape[1:3])
        try:
            br1[i] = np.average(br0, weights=br0*gaussian, axis=0)
        except ZeroDivisionError:
            br1[i] = np.average(br0, axis=0)
    return br1

def spatial_downscaling(cube: np.ndarray, pixels_limit: int):
    """ Brings the spatial resolution of the cube to approximately match the number of pixels """
    # TODO: averaging like in https://stackoverflow.com/questions/10685654/reduce-resolution-of-array-through-summation
    _, x, y = cube.shape
    factor = ceil(sqrt(x * y / pixels_limit))
    return cube[:,::factor,::factor]

def expand2x(array0: np.ndarray):
    """ Expands the array along the first axis by half """
    l = 2 * array0.shape[0] - 1
    if array0.ndim == 3: # spectral cube processing
        array1 = np.empty((l, array0.shape[1], array0.shape[2]), dtype=array0.dtype)
    else:
        array1 = np.empty(l, dtype=array0.dtype)
    array1[0::2] = array0
    array1[1::2] = (array0[:-1] + array0[1:]) * 0.5
    return array1

def linear_interp(x0: Sequence, y0: np.ndarray, x1: Sequence):
    """ Equivalent to the `np.interp()`, but also works for cubes """
    idx = np.searchsorted(x0, x1)
    x_left = x0[idx-1]
    x_right = x0[idx]
    y_left = y0[idx-1]
    y_right = y0[idx]
    return y_left + ((x1 - x_left) / (x_right - x_left) * (y_right - y_left).T).T

def custom_interp(array0: np.ndarray, k=16):
    """
    Returns curve or cube values with twice the resolution. Can be used in a loop.
    Optimal in terms of speed to quality ratio: around 2 times faster than splines in scipy.

    Args:
    - `array0` (np.ndarray): values to be interpolated in shape (2, N)
    - `k` (int): lower -> more chaotic, higher -> more linear, best results around 10-20
    """
    array1 = expand2x(array0)
    if array0.ndim == 3: # spectral cube processing
        zero = np.zeros((1, array0.shape[1], array0.shape[2]))
        delta_left = np.concatenate((zero, array0[1:-1] - array0[:-2]))
        delta_right = np.concatenate((array0[2:] - array0[1:-1], zero))
    else:
        delta_left = np.append(0., array0[1:-1] - array0[:-2])
        delta_right = np.append(array0[2:] - array0[1:-1], 0.)
    array1[1::2] += (delta_left - delta_right) / k
    return array1

def interpolating(x0: Sequence, y0: np.ndarray, x1: Sequence, step: int|float) -> np.ndarray:
    """
    Returns interpolated brightness values on uniform grid.
    Combination of custom_interp (which returns an uneven mesh) and linear interpolation after it.
    The chaotic-linearity parameter increases with each iteration to reduce the disadvantages of custom_interp.
    """
    for i in range(int(np.log2(np.diff(x0).max() / step))):
        x0 = expand2x(x0)
        y0 = custom_interp(y0, k=11+i)
    return linear_interp(x0, y0, x1)

def scope2matrix(scope: Sequence, times: int, axis: int = 1):
    """ Gets ta 1D array and expands its dimensions to a 2D array based on the 1D slice shape """
    return np.repeat(np.expand_dims(scope, axis=axis), times, axis=axis)

def scope2cube(scope: Sequence, shape: tuple[int, int]):
    """ Gets ta 1D array and expands its dimensions to a 3D array based on the 2D slice shape """
    return np.repeat(np.repeat(np.expand_dims(scope, axis=(1, 2)), shape[0], axis=1), shape[1], axis=2)

def custom_extrap(grid: Sequence, derivative: float|np.ndarray, corner_x: int|float, corner_y: float|np.ndarray) -> np.ndarray:
    """
    Returns an intuitive continuation of the function on the grid using information about the last point.
    Extrapolation bases on function f(x) = exp( (1-x²)/2 ): f' has extrema of ±1 in (-1, 1) and (1, 1).
    Therefore, it scales to complement the spectrum more easily than similar functions.
    """
    if np.all(derivative) == 0: # extrapolation by constant
        return np.repeat(np.expand_dims(corner_y, axis=0), grid.size, axis=0)
    else:
        if corner_y.ndim == 2: # spectral cube processing
            grid = scope2cube(grid, corner_y.shape)
        sign = np.sign(derivative)
        return np.exp((1 - (np.abs(derivative) * (grid - corner_x) / corner_y - sign)**2) / 2) * corner_y

weights_center_of_mass = 1 - 1 / np.sqrt(2)

def extrapolating(x: np.ndarray, y: np.ndarray, scope: np.ndarray, step: int|float, avg_steps=20):
    """
    Defines a curve or a cube with an intuitive continuation on the scope, if needed.
    `avg_steps` is a number of corner curve points to be averaged if the curve is not smooth.
    Averaging weights on this range grow linearly closer to the edge (from 0 to 1).
    """
    if len(x) == 1: # filling with equal-energy spectrum
        x = grid(min(scope[0], x[0]), max(scope[-1], x[0]))
        y = scope2matrix(y[0], x.size, axis=0)
    else:
        # Extrapolation to blue
        if x[0] > scope[0]:
            x1 = np.arange(scope[0], x[0], step)
            y_scope = y[:avg_steps]
            if is_smooth(y_scope):
                diff = y[1]-y[0]
                corner_y = y[0]
            else:
                avg_weights = np.abs(np.arange(-avg_steps, 0)[avg_steps-y_scope.shape[0]:]) # weights could be more complicated, but there is no need
                if y.ndim == 3: # spectral cube processing
                    avg_weights = scope2cube(avg_weights, y.shape[1:3])
                diff = np.average(np.diff(y_scope, axis=0), weights=avg_weights[:-1], axis=0)
                corner_y = np.average(y_scope, weights=avg_weights, axis=0) - diff * avg_steps * weights_center_of_mass
            y1 = custom_extrap(x1, diff/step, x[0], corner_y)
            x = np.append(x1, x)
            y = np.append(y1, y, axis=0)
        # Extrapolation to red
        if x[-1] < scope[-1]:
            x1 = np.arange(x[-1], scope[-1], step) + step
            y_scope = y[-avg_steps:]
            if is_smooth(y_scope):
                diff = y[-1]-y[-2]
                corner_y = y[-1]
            else:
                avg_weights = np.arange(avg_steps)[:y_scope.shape[0]] + 1
                if y.ndim == 3: # spectral cube processing
                    avg_weights = scope2cube(avg_weights, y.shape[1:3])
                diff = np.average(np.diff(y_scope, axis=0), weights=avg_weights[1:], axis=0)
                corner_y = np.average(y_scope, weights=avg_weights, axis=0) + diff * avg_steps * weights_center_of_mass
            y1 = custom_extrap(x1, diff/step, x[-1], corner_y)
            x = np.append(x, x1)
            y = np.append(y, y1, axis=0)
    return x, y

def gamma_correction(arr0: np.ndarray):
    """ Applies gamma correction in CIE sRGB implementation to the array """
    arr1 = np.copy(arr0)
    mask = arr0 < 0.0031308
    arr1[mask] *= 12.92
    arr1[~mask] = 1.055 * np.power(arr1[~mask], 1./2.4) - 0.055
    return arr1

def export_colors(rgb: tuple):
    """ Generates formatted string of colors """
    lst = []
    mx = 0
    for i in rgb:
        lst.append(str(i))
        l = len(lst[-1])
        if l > mx:
            mx = l
    w = 8 if mx < 8 else mx+1
    return ''.join([i.ljust(w) for i in lst])

def get_flag_index(flags: tuple):
    """ Returns index of active radio button """
    for index, flag in enumerate(flags):
        if flag:
            return index

illegal_chars = (
    '#',  # pound
    '%',  # percent
    '&',  # ampersand
    '{',  # left curly bracket
    '}',  # right curly bracket
    '\\', # back slash
    '<',  # left angle bracket
    '>',  # right angle bracket
    '*',  # asterisk
    '?',  # question mark
    '/',  # forward slash
    ' ',  # blank spaces
    '$',  # dollar sign
    '!',  # exclamation point
    "'",  # single quotes
    '"',  # double quotes
    ':',  # colon
    '@',  # at sign
    '+',  # plus sign
    '`',  # backtick
    '|',  # pipe
    '=',  # equal sign
)

def normalize_string(string: str):
    """ Removes characters invalid for file names """
    result = ''
    for char in string:
        if char not in illegal_chars:
            result += char
    return result



# Blackbody spectra

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
