""" File containing constant and functions required in various places, but without dependencies """

import numpy as np
from scipy.interpolate import PchipInterpolator, CloughTocher2DInterpolator
from math import sqrt, ceil
from collections.abc import Sequence



# ------------ Core Section ------------

# Constants needed for down scaling spectra and images
fwhm_factor = np.sqrt(8 * np.log(2))

def grid(start: int|float, end: int|float, step: int):
    """ Returns uniform grid points for the non-integer range that are divisible by the selected step """
    if (shift := start % step) != 0:
        start += step - shift
    if end % step == 0:
        end += 1 # to include the last point
    return np.arange(start, end, step, dtype='uint16')

def is_smooth(array: Sequence|np.ndarray):
    """ Boolean function, checks the second derivative for sign reversal, a simple criterion for smoothness """
    diff2 = np.diff(np.diff(array, axis=0), axis=0)
    return np.all(diff2 <= 0) | np.all(diff2 >= 0)

def integrate(array: Sequence|np.ndarray, step: int|float, precisely: bool = False):
    """
    Integration along the spectral axis.
    Uses the rectangle method by default and Riemann sum with midpoint in the "precise" mode.

    It is the inaccurate method that is most often used. Not because of speed, but because
    it is equivalent to matrix multiplication, which is used in spectrum reconstruction.
    In practice, the difference between the methods gives an accuracy gain of less than
    one hundredth of a factor.
    """
    if precisely:
        return step * 0.5 * np.sum(array[:-1] + array[1:], axis=0) # Riemann sum
    else:
        return step * np.sum(array, axis=0) # rectangle method

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

def spectral_downscaling(nm0: Sequence, br0: np.ndarray, sd0: np.ndarray, nm1: Sequence, step: int|float):
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
        br0 = np.clip(br0, np.nextafter(0, 1), None) # strange NumPy errors with weights without it
    notnan = ~np.isnan(br0)
    nm0 = nm0[notnan]
    br0 = br0[notnan]
    if sd0 is not None:
        sd0 = sd0[notnan]
    # Obtaining a graph of standard deviations for a Gaussian
    nm_diff = np.diff(nm0)
    nm_mid = (nm0[1:] + nm0[:-1]) * 0.5
    # Calculates the continuous (smoothed by gaussian) density of the original spectral grid
    sd_local = gaussian_width(gaussian_convolution(nm_mid, nm_diff, nm1, step*2), step) # missing "blur"
    # Gaussian exponent multipliers (0.001 is a small value to prevent zero division error like with 203 Pompeja)
    factors = -0.5 / np.clip(sd_local, 0.001, None)**2
    # Convolution with Gaussian of variable standard deviation
    br1 = np.empty_like(nm1, dtype='float64')
    if cube_flag:
        br1 = array2cube(br1, br0.shape[1:3])
    if sd0 is None:
        sd1 = None
        uncertainty_weights = np.ones_like(nm0)
    else:
        sd1 = np.empty_like(br1)
        uncertainty_weights = sd0**(-2)
    for i in range(len(nm1)):
        # Variable convolution kernel
        gaussian_weights = np.exp(factors[i]*(nm0 - nm1[i])**2)
        weights = uncertainty_weights * gaussian_weights
        if cube_flag:
            weights = array2cube(weights, br0.shape[1:3])
        try:
            br1[i] = np.average(br0, weights=weights, axis=0)
            if sd0 is not None:
                # Assumed formula, not proved
                sd1[i] = np.sum(weights, axis=0)**(-0.5)
                # If we had normal binning (on a limited interval), the formula would be
                # np.sum(uncertainty_weights[i])**(-0.5),
                # and at the limit, it would give σ1 = σ0 / sqrt(N)
                # Taking advantage of the fact that gaussian_weights take values from 1
                # at the center to 0 at infinity, I use them for summation of uncertainty_weights
        except ZeroDivisionError:
            br1[i] = np.average(br0, axis=0)
            if sd0 is not None:
                sd1[i] = 0
    return br1, sd1

def spatial_downscaling(cube: np.ndarray, pixels_limit: int):
    """ Brings the spatial resolution of the cube to approximately match the number of pixels """
    # TODO: averaging like in https://stackoverflow.com/questions/10685654/reduce-resolution-of-array-through-summation
    _, x, y = cube.shape
    factor = ceil(sqrt(x * y / pixels_limit))
    return cube[:,::factor,::factor]


def smoothness_matrix(n: int, order: int = 1):
    """
    Generates a smoothness operator matrix of the specified size n.
    Supported options:
    - identity matrix (n x n), for hight restriction
    - first-order difference operator (n-1 x n), for height change restriction
    - second-order difference operator (n-2 x n), for curvature restriction
    """
    if order == 0:
        # Hight restriction
        return np.eye(n, dtype='unit8')
    else:
        m = n - order
        L = np.zeros((m, n), dtype='int8')
        # Note: int8 makes it ~2 times faster
        match order:
            # Note: numpy doesn't make it faster
            # tested: diag = np.eye(m, dtype='int8'); L[:,:-1] = diag; L[:,1:] -= diag
            case 1:
                # Height change restriction
                for i in range(m):
                    L[i, i] = 1
                    L[i, i+1] = -1
            case 2:
                # Curvature restriction
                for i in range(m):
                    L[i, i] = 1
                    L[i, i+1] = -2
                    L[i, i+2] = 1
            case _:
                raise ValueError(f'Order {order} of smoothness matrix is not supported.')
    return L

def covar_matrix(M: np.ndarray):
    """
    Returns matrix multiplication of the transposed matrix by the original matrix.
    (A covariance matrix if the rows represent different observations and
    the columns represent different variables.)
    """
    return M.T @ M

def expand2x(array0: np.ndarray):
    """ Expands the array along the first axis by half """
    l = 2 * array0.shape[0] - 1
    match array0.ndim:
        case 1:
            array1 = np.empty(l, dtype=array0.dtype)
        case 2: # spectral square processing
            array1 = np.empty((l, array0.shape[1]), dtype=array0.dtype)
        case 3: # spectral cube processing
            array1 = np.empty((l, array0.shape[1], array0.shape[2]), dtype=array0.dtype)
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
    match array0.ndim:
        case 1:
            zero = np.zeros((1,))
        case 2: # spectral square processing
            zero = np.zeros((1, array0.shape[1]))
        case 3: # spectral cube processing
            zero = np.zeros((1, array0.shape[1], array0.shape[2]))
    delta_left = np.concatenate((zero, array0[1:-1] - array0[:-2]))
    delta_right = np.concatenate((array0[2:] - array0[1:-1], zero))
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

def higher_dim(arr: Sequence|int|float, times: int, axis: int = 1):
    """ Gets the array and repeats it along a new dimension """
    return np.repeat(np.expand_dims(arr, axis=axis), times, axis=axis)

def array2cube(arr: Sequence, shape: tuple[int, int]):
    """ Gets the 1D array and expands its dimensions to a 3D array based on the 2D slice shape """
    return np.repeat(np.repeat(np.expand_dims(arr, axis=(1, 2)), shape[0], axis=1), shape[1], axis=2)

def expand_1D_array(arr: np.ndarray, shape: int|tuple):
    """
    Gets the 1D array and expands its dimensions to a 2D or 3D array based on the slice shape.
    Сan be rewritten with numpy.tile()?
    """
    match len(shape):
        case 0:
            return arr
        case 1:
            return higher_dim(arr, shape)
        case 2:
            return array2cube(arr, shape)


def custom_extrap(grid: Sequence, derivative: float|np.ndarray, corner_x: int|float, corner_y: float|np.ndarray) -> np.ndarray:
    """
    Returns an intuitive continuation of the function on the grid using information about the last point.
    Extrapolation bases on function f(x) = exp( (1-x²)/2 ): f' has extrema of ±1 in (-1, 1) and (1, 1).
    Therefore, it scales to complement the spectrum more easily than similar functions.
    """
    if np.all(derivative) == 0: # extrapolation by constant
        return higher_dim(corner_y, grid.size, axis=0)
    else:
        grid = expand_1D_array(grid, corner_y.shape)
        sign = np.sign(derivative)
        return np.exp((1 - (np.abs(derivative) * (grid - corner_x) / corner_y - sign)**2) / 2) * corner_y

def extrap_sd(corner_y: float|np.ndarray, x_arr: np.ndarray):
    """ The exponential growth of uncertainty is completely arbitrary and needs to be investigated """
    return corner_y * 0.05 * (1.01**x_arr - 1)


weights_center_of_mass = 1 - 1 / np.sqrt(2)

def extrapolating(x: np.ndarray, y: np.ndarray, sd: np.ndarray, x_arr: np.ndarray, step: int, avg_steps=20):
    """
    Defines a (multi-dimensional) curve an intuitive continuation on the x_arr, if needed.
    In TCT works for spectra, filter systems and spectral cubes.
    `avg_steps` is a number of corner curve points to be averaged if the curve is not smooth.
    Averaging weights on this range grow linearly closer to the edge (from 0 to 1).
    The exponential growth of uncertainty is completely arbitrary and needs to be investigated.
    """
    obj_shape = y.shape[1:] # (,) for 1D; (n,) for 2D; (w, h) for 3D
    if len(obj_shape) >= 1:
        # currently broken for spectral cubes and "squares"
        is_cube = True
    else:
        is_cube = False
        if sd is None:
            sd = np.zeros_like(y)
            sd_left = sd_right = 0.
        else:
            sd_left = sd[0]
            sd_right = sd[-1]
    if len(x) == 1: # filling with equal-energy spectrum
        x1 = grid(min(x_arr[0], x[0]), max(x_arr[-1], x[0]), step)
        y1 = higher_dim(y[0], x1.size, axis=0)
        if not is_cube:
            sd = extrap_sd(y[0], np.abs(x1 - x[0]))
        x = x1
        y = y1
    else:
        if x[0] > x_arr[0]:
            # Extrapolation to blue
            x1 = np.arange(x_arr[0], x[0], step)
            if np.all(y[0] == 0):
                # Corner point is zero -> no extrapolation needed: most likely it's a filter profile
                y1 = sd1 = np.zeros((x1.size, *obj_shape))
            else:
                y_arr = y[:avg_steps]
                if is_smooth(y_arr):
                    diff = y[1]-y[0]
                    corner_y = y[0]
                else:
                    # Linear weights. Could be more complicated, but there is no need
                    avg_weights = expand_1D_array(np.arange(-avg_steps, 0)[avg_steps-y_arr.shape[0]:], obj_shape)
                    diff = np.average(np.diff(y_arr, axis=0), weights=avg_weights[:-1], axis=0)
                    corner_y = np.average(y_arr, weights=avg_weights, axis=0) - diff * avg_steps * weights_center_of_mass
                y1 = custom_extrap(x1, diff/step, x[0], corner_y)
                if not is_cube:
                    sd1 = sd_left + expand_1D_array(extrap_sd(corner_y, np.arange(x[0]-x_arr[0], 0, -step) - step), obj_shape)
            x = np.append(x1, x)
            y = np.append(y1, y, axis=0)
            if not is_cube:
                sd = np.append(sd1, sd, axis=0)
        if x[-1] < x_arr[-1]:
            # Extrapolation to red
            x1 = np.arange(x[-1], x_arr[-1], step) + step
            if np.all(y[0] == 0):
                # Corner point is zero -> no extrapolation needed: most likely it's a filter profile
                y1 = sd1 = np.zeros((x1.size, *obj_shape))
            else:
                y_arr = y[-avg_steps:]
                if is_smooth(y_arr):
                    diff = y[-1]-y[-2]
                    corner_y = y[-1]
                else:
                    avg_weights = expand_1D_array(np.arange(avg_steps)[:y_arr.shape[0]] + 1, obj_shape)
                    diff = np.average(np.diff(y_arr, axis=0), weights=avg_weights[1:], axis=0)
                    corner_y = np.average(y_arr, weights=avg_weights, axis=0) + diff * avg_steps * weights_center_of_mass
                y1 = custom_extrap(x1, diff/step, x[-1], corner_y)
                if not is_cube:
                    sd1 = sd_right + expand_1D_array(extrap_sd(corner_y, np.arange(0, x_arr[-1]-x[-1], step)), obj_shape)
            x = np.append(x, x1)
            y = np.append(y, y1, axis=0)
            if not is_cube:
                sd = np.append(sd, sd1, axis=0)
    if is_cube:
        sd = None
    else:
        if sd.sum() == 0:
            sd = None
    return x, y, sd


def make_same_ndim(arr1: np.ndarray, arr2: np.ndarray):
    """ Equalizes the arrays dimensions along spatial axes to make it possible to broadcast """
    if (ndim_delta := arr2.ndim - arr1.ndim) != 0:
        if ndim_delta > 0:
            arr1 = arr1.reshape(arr1.shape + (1,)*ndim_delta)
        else:
            arr2 = arr2.reshape(arr2.shape + (1,)*(-ndim_delta))
    return arr1, arr2

def add_br(br1, br2):
    """
    Calculates the value of the sum.
    The input can be a numeric or a (multidimensional) numpy array.
    """
    if isinstance(br1, np.ndarray) and isinstance(br2, np.ndarray):
        br1, br2 = make_same_ndim(br1, br2)
    return br1 + br2

def add_sd(br1, sd1, br2, sd2):
    """
    Calculates the standard deviation of the sum.
    The input can be a numeric or a (multidimensional) numpy array.
    """
    if sd1 is None:
        return sd2
    elif sd2 is None:
        return sd1
    else:
        if isinstance(sd1, np.ndarray) and isinstance(sd2, np.ndarray):
            sd1, sd2 = make_same_ndim(sd1, sd2)
        return np.sqrt(sd1**2 + sd2**2)

def sub_br(br1, br2):
    """
    Calculates the value of the difference.
    The input can be a numeric or a (multidimensional) numpy array.
    """
    if isinstance(br1, np.ndarray) and isinstance(br2, np.ndarray):
        br1, br2 = make_same_ndim(br1, br2)
    return br1 + br2

def sub_sd(br1, sd1, br2, sd2):
    """
    Calculates the standard deviation of the difference.
    The input can be a numeric or a (multidimensional) numpy array.
    """
    return add_sd(br1, sd1, br2, sd2)

def mul_br(br1, br2):
    """
    Calculates the value of the product.
    The input can be a numeric or a (multidimensional) numpy array.
    """
    try:
        # Numeric and same-ndim numpy arrays cases
        return br1 * br2
    except ValueError:
        # Different ndim case
        if isinstance(br1, np.ndarray) and isinstance(br2, np.ndarray) and br2.ndim > br1.ndim:
            br1, br2 = br2, br1
        return (br1.T * br2).T

def mul_sd(br1, sd1, br2, sd2):
    """
    Calculates the standard deviation of the product.
    The input can be a numeric or a (multidimensional) numpy array.
    """
    if sd1 is None and sd2 is None:
        return None
    else:
        if sd1 is None:
            sd1 = np.zeros_like(br1)
        if sd2 is None:
            sd2 = np.zeros_like(br2)
        return np.sqrt(mul_br(br1, sd2)**2 + mul_br(br2, sd1)**2 + mul_br(sd1, sd2)**2)

def div_br(br1, br2):
    """
    Calculates the value of the private.
    The input can be a numeric or a (multidimensional) numpy array.
    """
    try:
        # Numeric and same-ndim numpy arrays cases
        return br1 / br2
    except ValueError:
        # Different ndim case
        if isinstance(br1, np.ndarray) and isinstance(br2, np.ndarray) and br2.ndim > br1.ndim:
            br1, br2 = br2, br1
        return (br1.T / br2).T

def div_sd(br1, sd1, br2, sd2):
    """
    Calculates the standard deviation of the private.
    The input can be a numeric or a (multidimensional) numpy array.
    """
    if sd1 is None and sd2 is None:
        return None
    else:
        if sd1 is None:
            sd1 = np.zeros_like(br1)
        if sd2 is None:
            sd2 = np.zeros_like(br2)
        return div_br(mul_sd(br1, sd1, br2, sd2), br2**2)


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



# ------------ Database Processing Section ------------

def parse_value_sd(data: float|Sequence[float]) -> tuple[float, float|None]:
    """
    Guarantees the output of the value and its standard deviation.

    Supported input types:
    - value
    - [value, sd]
    - [value, +sd1, -sd2]
    - [value, -sd1, +sd2]
    """
    if isinstance(data, int|float):
        # no standard deviation
        return data, None
    elif isinstance(data, Sequence|np.ndarray):
        match len(data):
            case 2:
                # regular standard deviation
                return tuple(data)
            case 3:
                # asymmetric standard deviation
                value, sd1, sd2 = data
                sd = 0.5 * (abs(sd1) + abs(sd2)) # reduced to regular
                return value, sd
    print(f'Invalid data input: {data}. Must be a numeric value or a [value, sd] list. Returning None.')
    return None, None

def parse_value_sd_list(arr: Sequence):
    """ Splits the values and standard deviations into two arrays """
    try:
        arr = np.array(arr, dtype='float') # ValueError here means inhomogeneous shape
    except ValueError:
        # inhomogeneous standard deviation input
        values = []
        for data in arr:
            value, _ = parse_value_sd(data)
            values.append(value)
        return np.array(values, dtype='float'), None
    try:
        # no standard deviation
        if arr.ndim == 0:
            arr = np.atleast_1d(arr)
        elif arr.ndim > 1:
            raise ValueError # means sd is there
        return arr, None
    except ValueError:
        # standard deviation case
        values = []
        sds = []
        for data in arr:
            value, sd = parse_value_sd(data)
            values.append(value)
            sds.append(sd)
        return np.array(values, dtype='float'), np.array(sds, dtype='float')

def repeat_if_value(data: int|float|Sequence, arr_len: int):
    """ If the input consists of a single number, stretches to 1D array """
    arr = np.array(data)
    if arr.ndim == 0:
        # a single number
        return np.repeat(arr, arr_len)
    else:
        return arr

def mag2irradiance(mag: int|float|np.ndarray, zero_point: float = 1.):
    """ Converts magnitudes to irradiance (by default in Vega units) """
    return zero_point * 10**(-0.4 * mag)

def sd_mag2sd_irradiance(sd_mag: int|float|np.ndarray, irradiance: int|float|np.ndarray):
    """
    Converts standard deviation of the magnitude to a irradiance standard deviation.

    The formula is derived from the error propagation equation:
    I(mag) = zero_point ∙ 10^(-0.4 mag)
    sd_I² = (d I / d mag)² ∙ sd_mag²
    I' = zero_point∙(10^(-0.4 mag))' = zero_point∙10^(-0.4 mag)∙ln(10^(-0.4)) = I∙(-0.4) ln(10)
    sd_I = |I'| ∙ sd_mag = 0.4 ln(10) ∙ I ∙ sd_mag
    """
    return 0.4 * np.log(10) * irradiance * sd_mag

def color_index_splitter(index: str):
    """
    Dashes in filter names are allowed in the SVO Filter Profile Service.
    This function should fix all or most of the problems caused.
    """
    try:
        filter1, filter2 = index.split('-')
    except ValueError:
        dotpart1, dotpart2, dotpart3 = index.split('.') # one dot per full filter name
        dashpart1, dashpart2 = dotpart2.split('-', 1)
        filter1 = f'{dotpart1}.{dashpart1}'
        filter2 = f'{dashpart2}.{dotpart3}'
    return filter1, filter2

def color_indices_parser(indices: dict):
    """
    Converts color indices to linear brightness, assuming mag=0 in the first filter.
    Each new color index must refer to a previously specified one.
    Note: The output order may sometimes not be in ascending wavelength order.
    This can be corrected by knowing the filter profiles, which better to do outside the function.

    For standard deviations the error propagation equation is used:
    f(x, y) = x - y
    sd_f² = (df/dx)² sd_x² + (df/dy)² sd_y² = sd_x² + sd_y²
    where x, y are magnitudes and f is a color index.

    Finding standard deviations of a photospectrum built from color indices is an ill-posed problem:
    it's just like with integrating, we loose constant after differentiation (color indices is
    a discrete differential form of a photospectrum).
    For the photospectrum itself, it's not a problem: the solutions dimension is just scaling
    the spectrum on a constant (it's pretty obvious that color indices always lost brightness
    information).
    But the solutions space for their standard deviations is more complex, I found its geometric
    interpretation: since the standard deviations subtracting rule is, in fact, the Pythagorean theorem,
    the solutions space is the same as if you try to build a line of right triangles, for each one
    the next cathetus is linked to a previous cathetus by their square.
    (To draw on the plane you have to use rhombuses of the same area and the same equal sides
    instead of squares.)
    N hypotenuses are standard deviations of color indices, and N+1 different cathetes are the sought
    standard deviations of the photospectrum.
    The whole triangle line possible positions can be described by just one parameter (1D parametric
    space of solutions).
    For simplicity, I will choose the first cathetus (the first sought standard deviation) as
    a variable of this space.
    Such triangles can "collapse" if the previous cathetus is greater than the next hypotenuse!
    I tried to find an analytical solution, but the requirement for the optimal solution I derived
    suggested that about a half of the triangles should be collapsed.

    In the numerical approach I use, some solutions are collapsed (the `try-except` code block),
    but there are a some range of possible solutions too, which one to choose?
    I decided to choose the solution with minimal standard deviation of standard deviations it gives.
    To tighten the solution selection criteria, it can be assumed that the size of the standard deviation
    is inversely proportional to the root of the irradiance (in the Poisson noise approximation).
    So it's better to minimize the differences not between the stds of magnitudes, but between
    the stds of scaled irradiances.
    """
    first_color_index = tuple(indices.keys())[0]
    filter0, _ = color_index_splitter(first_color_index)
    _, sd0 = parse_value_sd(indices[first_color_index])
    # Just photospectrum calculation
    uncertainty_flag = True
    filters = {filter0: 0} # mag=0 for the first point (arbitrarily)
    for key, value in indices.items():
        bluer_filter, redder_filter = color_index_splitter(key)
        mag, sd = parse_value_sd(value)
        if sd is None:
            uncertainty_flag = False
        if bluer_filter in filters:
            filters |= {redder_filter: filters[bluer_filter] - mag}
        else:
            filters |= {bluer_filter: filters[redder_filter] + mag}
    irradiance = mag2irradiance(np.array(tuple(filters.values())))
    filter_names = filters.keys() # name setting before using the variable for sd processing
    sd = None
    # Uncertainty calculation
    if uncertainty_flag:
        shot_noise_factor = np.sqrt(irradiance) # common Poisson noise factor
        sd_of_sd = np.inf
        for sd_assumed in np.linspace(0, sd0, 1001):
            impossible_assumption = False
            # Numerically select the best value of the standard deviation of the first point,
            # on which all other standard deviations clearly depend
            filters = {filter0: sd_assumed}
            for key, value in indices.items():
                bluer_filter, redder_filter = color_index_splitter(key)
                _, index_sd = parse_value_sd(value)
                try:
                    if bluer_filter in filters:
                        filters |= {redder_filter: sqrt(index_sd**2 - filters[bluer_filter]**2)}
                    else:
                        filters |= {bluer_filter: sqrt(index_sd**2 - filters[redder_filter]**2)}
                except ValueError:
                    # This means that the difference under the root is negative
                    # and the initial standard deviation assumption is not possible
                    impossible_assumption = True
                    break
            if not impossible_assumption:
                new_sd = sd_mag2sd_irradiance(np.array(tuple(filters.values())), irradiance)
                # Finding the minimum deviation between sd as solution quality criterion
                # The standard deviations are scaled by the Poisson noise factor
                new_sd_of_sd = np.std(new_sd * shot_noise_factor)
                if new_sd_of_sd < sd_of_sd:
                    sd = new_sd
                    sd_of_sd = new_sd_of_sd
                    continue
                else:
                    # Means that the best values of standard deviations were found
                    # in the last iteration and they started to diverge
                    break
    return filter_names, irradiance, sd



# ------------ Phase Photometry Section ------------


# Macroscopic roughness angle of Hapke 1984 model
# Hapke, B. (1984). Bidirectional reflectance spectroscopy. Icarus, 59(1), 41–59. doi:10.1016/0019-1035(84)90054-x
# https://www.sciencedirect.com/science/article/abs/pii/001910358490054X

# "When Eqs. (57) and (58) for a macroscopically rough surface were inserted into the above equations,
# analytic expressions for the physical albedo and integral phase function could not be obtained.
# Hence, the integration was done numerically for values of θ up to 60°."

_alpha = np.array([0, 2, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180]) / 180 * np.pi
_theta = np.array([0, 10, 20, 30, 40, 50, 60]) / 180 * np.pi
_k = np.array([
    [1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00],
    [1.00, 0.997, 0.991, 0.984, 0.974, 0.961, 0.943],
    [1.00, 0.994, 0.981, 0.965, 0.944, 0.918, 0.881],
    [1.00, 0.991, 0.970, 0.943, 0.909, 0.866, 0.809],
    [1.00, 0.988, 0.957, 0.914, 0.861, 0.797, 0.715],
    [1.00, 0.986, 0.947, 0.892, 0.825, 0.744, 0.644],
    [1.00, 0.984, 0.938, 0.871, 0.789, 0.692, 0.577],
    [1.00, 0.982, 0.926, 0.846, 0.748, 0.635, 0.509],
    [1.00, 0.979, 0.911, 0.814, 0.698, 0.570, 0.438],
    [1.00, 0.974, 0.891, 0.772, 0.637, 0.499, 0.366],
    [1.00, 0.968, 0.864, 0.719, 0.566, 0.423, 0.296],
    [1.00, 0.959, 0.827, 0.654, 0.487, 0.346, 0.231],
    [1.00, 0.946, 0.777, 0.575, 0.403, 0.273, 0.175],
    [1.00, 0.926, 0.708, 0.484, 0.320, 0.208, 0.130],
    [1.00, 0.894, 0.617, 0.386, 0.243, 0.153, 0.0936],
    [1.00, 0.840, 0.503, 0.290, 0.175, 0.107, 0.064],
    [1.00, 0.747, 0.374, 0.201, 0.117, 0.070, 0.041],
    [1.00, 0.590, 0.244, 0.123, 0.069, 0.040, 0.023],
    [1.00, 0.366, 0.127, 0.060, 0.032, 0.018, 0.010],
    [1.00, 0.128, 0.037, 0.016, 0.0085, 0.0047, 0.0026],
    [1.00, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
])

_A, _B = np.meshgrid(_alpha, _theta, indexing='ij')
hapke_k = CloughTocher2DInterpolator(np.column_stack([_A.ravel(), _B.ravel()]), _k.ravel())

def henyey_greenstein(alpha: np.ndarray, b: float, c: float):
    """ Double Henyey-Greenstein (1941) single particle scattering function """
    return (1 - b**2) * ((1 - c) * (1 + 2*b*np.cos(alpha) + b**2)**(-1.5) + c * (1 - 2*b*np.cos(alpha) + b**2)**(-1.5))


# HG1G2 base functions
# https://github.com/milicolazo/Pyedra/blob/master/pyedra/datasets/penttila2016.csv

_alpha = np.array([
    0, 0.025, 0.05, 0.075, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75,
    0.8, 0.85, 0.9, 0.95, 1, 1.25, 1.5, 1.75, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 9, 10,
    11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 33, 36, 39, 42, 45,
    48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 90, 93, 96, 99, 102, 105, 108, 111, 114,
    117, 120, 123, 126, 129, 132, 135, 138, 141, 144, 147, 150
]) / 180 * np.pi

_phi1 = np.array([
    1, 0.99916667, 0.99833333, 0.9975, 0.99666667, 0.995, 0.99333333, 0.99166667, 0.99, 0.98833333,
    0.98666667, 0.985, 0.98333333, 0.98166667, 0.98, 0.97833333, 0.97666667, 0.975, 0.97333333,
    0.97166667, 0.97, 0.96833333, 0.96666667, 0.95833333, 0.95, 0.94166667, 0.93333333, 0.91666667,
    0.9, 0.88333333, 0.86666667, 0.85, 0.83333333, 0.81666667, 0.8, 0.78333333, 0.76666667, 0.75,
    0.7335651, 0.70205874, 0.67230993, 0.64424623, 0.6177952, 0.59288439, 0.56944137, 0.5473937,
    0.52666893, 0.50719463, 0.48889834, 0.47170764, 0.45555008, 0.44035322, 0.42604461, 0.41255183,
    0.39980241, 0.38772394, 0.37624396, 0.36529003, 0.35478972, 0.34467057, 0.33486016, 0.3068662,
    0.28089877, 0.25685779, 0.2346432, 0.21415492, 0.19529288, 0.177957, 0.16204721, 0.14746343,
    0.1341056, 0.1218788, 0.11070881, 0.10052653, 0.09126291, 0.08284886, 0.07521532, 0.06829321,
    0.06201346, 0.056307, 0.05110476, 0.0463475, 0.04201539, 0.03809846, 0.0345867, 0.03147014,
    0.02873879, 0.02638265, 0.02439175, 0.02275609, 0.02146569, 0.02048884, 0.019707, 0.01897989,
    0.01816723, 0.01712876, 0.01572421, 0.01381329, 0.01125575, 0.00791131, 0.0036397
])

_phi2 = np.array([
    1, 0.99975, 0.9995, 0.99925, 0.999, 0.9985, 0.998, 0.9975, 0.997, 0.9965, 0.996, 0.9955, 0.995,
    0.9945, 0.994, 0.9935, 0.993, 0.9925, 0.992, 0.9915, 0.991, 0.9905, 0.99, 0.9875, 0.985, 0.9825,
    0.98, 0.975, 0.97, 0.965, 0.96, 0.955, 0.95, 0.945, 0.94, 0.935, 0.93, 0.925, 0.91993295,
    0.90940957, 0.89839618, 0.88692759, 0.87503862, 0.86276408, 0.85013879, 0.83719757, 0.82397523,
    0.81050658, 0.79682645, 0.78296964, 0.76897098, 0.75486528, 0.74068735, 0.72647201, 0.71225408,
    0.69806837, 0.6839497, 0.66993288, 0.65605272, 0.64234406, 0.62884169, 0.58974571, 0.55271081,
    0.51762803, 0.4843884, 0.45288296, 0.42300275, 0.39463881, 0.36768217, 0.34202387, 0.31755495,
    0.2941793, 0.27185223, 0.25054189, 0.23021646, 0.21084408, 0.19239292, 0.17483114, 0.15812689,
    0.14224835, 0.12716367, 0.11285041, 0.09932372, 0.08660818, 0.07472832, 0.06370871, 0.05357391,
    0.04434847, 0.03605695, 0.02872391, 0.0223739, 0.01701331, 0.0125758, 0.00897685, 0.00613196,
    0.00395661, 0.00236629, 0.00127648, 0.00060269, 0.00026038, 0.00016506
])

_phi3 = np.array([
    1, 0.9980637, 0.99261656, 0.98406203, 0.9728036, 0.94378889, 0.90880018, 0.87106525, 0.83381185,
    0.7996872, 0.76901633, 0.74154373, 0.71701389, 0.69517129, 0.67576042, 0.65852577, 0.64321182,
    0.62956307, 0.61732399, 0.60623909, 0.59605283, 0.58650972, 0.57735424, 0.53374972, 0.49331752,
    0.45592704, 0.42144772, 0.36065328, 0.30965499, 0.26712671, 0.2317423, 0.20228652, 0.17798763,
    0.15818479, 0.14221716, 0.12942389, 0.11914414, 0.11071705, 0.10348178, 0.09076411, 0.07980824,
    0.07025206, 0.06173347, 0.05394627, 0.04680785, 0.04029153, 0.03437061, 0.02901839, 0.02420818,
    0.01991328, 0.01610701, 0.01276361, 0.00986117, 0.00737872, 0.0052953, 0.00358992, 0.00224164,
    0.00122947, 0.00053245, 0.00012962, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
])

hg1g2_phi1 = PchipInterpolator(_alpha, _phi1, extrapolate=True)
hg1g2_phi2 = PchipInterpolator(_alpha, _phi2, extrapolate=True)
hg1g2_phi3 = PchipInterpolator(_alpha, _phi3, extrapolate=True)


# ------------ Color Processing Section ------------

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


# ------------ Other ------------

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
    '\\', # backslash
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

superscript_digits = '⁰¹²³⁴⁵⁶⁷⁸⁹'

def superscript(number: int):
    """ Converts a number to be a superscript string """
    return ''.join([superscript_digits[int(digit)] for digit in str(number)])

subscript_digits = '₀₁₂₃₄₅₆₇₈₉'

def subscript(number: int | str):
    """ Converts a number to be a subscript string """
    return ''.join([subscript_digits[int(digit)] for digit in str(number)])
