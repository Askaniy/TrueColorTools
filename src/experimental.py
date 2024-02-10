""" Provides incomplete or unnecessary functionality. """

import numpy as np



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



# Align multiband image

def experimental_autoalign(data: np.ndarray, debug: bool):
    l, h, w = data.shape
    sums_x = []
    sums_y = []
    for layer in data:
        sums_x.append(np.sum(layer, 0))
        sums_y.append(np.sum(layer, 1))
    shifts0_x = relative_shifts(square(sums_x))
    shifts0_y = relative_shifts(square(sums_y))
    if debug:
        print('\nBase', shifts0_x, shifts0_y)
    
    shiftsR_x = []
    shiftsR_y = []
    for i in range(l-1):
        shift_x, shift_y = recursive_shift(square(data[i]), square(data[i+1]), shifts0_x[i], shifts0_y[i], debug)
        shiftsR_x.append(shift_x)
        shiftsR_y.append(shift_y)
    if debug:
        print('\nRecursion', shiftsR_x, shiftsR_y)
    
    #corrections_x = []
    #corrections_y = []
    #for l in range(l-1):
    #    arr0, arr1 = square(data[l]), square(data[l+1])
    #    coord = (0, 0)
    #    min = 1e18
    #    for i in range(-25, 26):
    #        for j in range(-25, 26):
    #            diff = abs(np.sum(np.abs(arr0 - np.roll(arr1, (shifts0_y[l]+j, shifts0_x[l]+i)))))
    #            if diff < min:
    #                min = diff
    #                coord = (i, j)
    #                print(min, coord)
    #    corrections_x.append(coord[0])
    #    corrections_y.append(coord[1])
    #quit()
    #if debug:
    #   print('\nCorrection', corrections_x, corrections_y)
    #shiftsC_x = np.array(shifts0_x) + np.array(corrections_x)
    #shiftsC_y = np.array(shifts0_y) + np.array(corrections_y)
    #if debug:
    #   print('\nCorrected', shiftsC_x, shiftsC_y)
    
    shifts_x = absolute_shifts(shiftsR_x)
    shifts_y = absolute_shifts(shiftsR_y)
    w = w + shifts_x.min()
    h = h + shifts_y.min()
    for i in range(l):
        data[i] = np.roll(data[i], (shifts_y[i], shifts_x[i]))
    data = data[:, :h, :w]
    return data

def square(array: np.ndarray):
    return np.multiply(array, array)
    #return np.clip(array, np.mean(array), None)

def mod_shift(c, size): # 0->size shift to -s/2->s/2
    size05 = int(size/2) # floor rounding
    return (c+size05)%size-size05

def relative_shifts(sums):
    diffs = []
    for i in range(len(sums)-1):
        size = len(sums[i])
        temp_diff_list = []
        for j in range(size):
            diff = np.abs(sums[i] - np.roll(sums[i+1], j))
            temp_diff_list.append(np.sum(diff))
        diffs.append(mod_shift(np.argmin(temp_diff_list), size))
    return diffs

def recursive_shift(img0: np.ndarray, img1: np.ndarray, shift_x, shift_y, debug):
    if debug:
        print('\nstart of recursion with ', shift_x, shift_y)
    diff0 = abs(np.sum(np.abs(img0 - np.roll(img1, (shift_y, shift_x)))))
    diffU = abs(np.sum(np.abs(img0 - np.roll(img1, (shift_y-1, shift_x)))))
    diffD = abs(np.sum(np.abs(img0 - np.roll(img1, (shift_y+1, shift_x)))))
    diffL = abs(np.sum(np.abs(img0 - np.roll(img1, (shift_y, shift_x-1)))))
    diffR = abs(np.sum(np.abs(img0 - np.roll(img1, (shift_y, shift_x+1)))))
    diffUL = abs(np.sum(np.abs(img0 - np.roll(img1, (shift_y-1, shift_x-1)))))
    diffUR = abs(np.sum(np.abs(img0 - np.roll(img1, (shift_y-1, shift_x+1)))))
    diffDL = abs(np.sum(np.abs(img0 - np.roll(img1, (shift_y+1, shift_x-1)))))
    diffDR = abs(np.sum(np.abs(img0 - np.roll(img1, (shift_y+1, shift_x+1)))))
    if debug:
        print(f'{diffUL} {diffU} {diffUR}\n{diffL} {diff0} {diffR}\n{diffDL} {diffD} {diffDR}')
    argmin = np.argmin((diff0, diffU, diffD, diffL, diffR, diffUL, diffUR, diffDL, diffDR))
    if argmin != 0: # box 3x3
        if argmin == 1:
            shift_y -= 1
        elif argmin == 2:
            shift_y += 1
        elif argmin == 3:
            shift_x -= 1
        elif argmin == 4:
            shift_x += 1
        elif argmin == 5:
            shift_x -= 1
            shift_y -= 1
        elif argmin == 6:
            shift_x += 1
            shift_y -= 1
        elif argmin == 7:
            shift_x -= 1
            shift_y += 1
        elif argmin == 8:
            shift_x += 1
            shift_y += 1
        return recursive_shift(img0, img1, shift_x, shift_y, debug)
    else:
        return shift_x, shift_y
    #while True:
    #    if debug:
    #        print("\nstart of recursion with ", shift_x, shift_y)
    #    diffs = []
    #    for i in range(9):
    #        x = i % 3 - 1
    #        y = i // 3 - 1
    #        diff = abs(np.sum(np.abs(img0 - np.roll(img1, (shift_y+y, shift_x+x)))))
    #        diffs.append(diff)
    #    if debug:
    #        for i in range(3):
    #            for j in range(3):
    #                sys.stdout.write(str(diffs[i*3+j]) + " ")
    #            print("")
    #    argmin = np.argmin(diffs)
    #    shift_x += argmin % 3 - 1
    #    shift_y += argmin // 3 - 1
    #    print(argmin)
    #    print(diffs)
    #    if argmin == 4:
    #        break
    #return shift_x, shift_y

def absolute_shifts(diffs):
    p = [0]
    for d in diffs:
        p.append(p[-1]+d)
    return np.array(p) - max(p)



# Phase curves processing functions
#def lambert(phase: float):
#    phi = abs(np.deg2rad(phase))
#    return (np.sin(phi) + np.pi * np.cos(phi) - phi * np.cos(phi)) / np.pi # * 2/3 * albedo


# Linear extrapolation
#def line_generator(x1, y1, x2, y2):
#    return np.vectorize(lambda wl: y1 + (wl - x1) * (y2 - y1) / (x2 - x1))



# Magnitudes processing functions

#V = 2.518021002e-8 # 1 Vega in W/m^2, https://arxiv.org/abs/1510.06262

#def mag2intensity(m: int|float|np.ndarray):
#    return V * 10**(-0.4 * m)

#def intensity2mag(e):
#    return -2.5 * np.log10(e / V)



#def averaging(x0: Sequence, y0: np.ndarray, x1: Sequence, step: int|float):
#    """ Returns spectrum brightness values with decreased resolution """
#    semistep = step * 0.5
#    y1 = [np.mean(y0[np.where(x0 < x1[0]+semistep)])]
#    for x in x1[1:-1]:
#        flag = np.where((x-semistep < x0) & (x0 < x+semistep))
#        if flag[0].size == 0: # the spectrum is no longer dense enough to be averaged down to 5 nm
#            y = y1[-1] # lengthening the last recorded brightness is the simplest solution
#        else:
#            y = np.mean(y0[flag]) # average the brightness around X points
#        y1.append(y)
#    y1.append(np.mean(y0[np.where(x0 > x1[-1]-semistep)]))
#    return np.array(y1)




#def expand(array, axis, repeat):
#    return np.repeat(np.expand_dims(array, axis=axis), repeat, axis=axis)

#def spectral_downscaling(nm0: Sequence, br0: np.ndarray, nm1: Sequence, step: int|float):
#    """
#    Edition of spectral_downscaling that uses no loops, but up to 4D arrays.
#    Requires >>15 Gb of RAM for images, just crashed.
#    And slower for 1D spectra than the original
#    """
#    # Obtaining a graph of standard deviations for a Gaussian
#    nm_diff = np.diff(nm0)
#    nm_mid = (nm0[1:] + nm0[:-1]) * 0.5
#    sd_local = gaussian_convolution(nm_mid, nm_diff, nm1, step*2) # 1D
#    # Convolution with Gaussian of variable standard deviation
#    nm0_plane = expand(nm0, 1, len(nm1)) # 2D
#    nm1_plane = expand(nm1, 0, len(nm0)) # 2D
#    sd = gaussian_width(sd_local, step) # 1D
#    factor = expand(-0.5 / sd**2, 0, len(nm0)) # 2D
#    gaussian = np.exp(factor*(nm0_plane - nm1_plane)**2) # 2D
#    br0 = expand(br0, -1, len(nm1)) # 2D for spectra or 4D for cubes
#    br1 = np.average(br0, weights=br0 * gaussian, axis=0) # 1D for spectra or 3D for cubes
#    return br1
#





# Attempt to import spectral cubes with spectral-cube library, unsuccessful
# 1. Can't read files of HST STIS due to WCS errors
# 2. Requires scipy and a lot of other libraries
# 3. Crooked code design

# Disabling warnings about supplier non-compliance with FITS unit storage standards and spectral-cube warnings
#from spectral_cube.utils import WCSWarning, ExperimentalImplementationWarning
#filterwarnings(action='ignore', category=u.UnitsWarning, append=True)
#filterwarnings(action='ignore', category=ExperimentalImplementationWarning, append=True)
#filterwarnings(action='ignore', category=WCSWarning, append=True)

#def do_nothing():
#    """
#    Workaround the spectral-cube library requirement for the progress bar update function.
#    Progress bar by default (provided by AstroPy) cannot work in a thread.
#    """
#    pass

#def cube_reader(file: str) -> tuple[str, np.ndarray, np.ndarray]:
#    """ Imports a spectral cube from the FITS file and down scaling spatial resolutions to the specified one. """
#    # See https://gist.github.com/keflavich/37a2705fb4add9a2491caf2dfa195efd
#
#    cube = SpectralCube.read(file, hdu=1).with_spectral_unit(u.nm)
#    print(cube) # general info
#
#    # Getting target wavelength range
#    nm = aux.grid(*cube.spectral_extrema.value, aux.resolution)
#    flag = np.where(nm < aux.nm_red_limit + aux.resolution) # with reserve to be averaged
#    nm = nm[flag]
#
#    # Spectral smoothing and down scaling
#    current_resolution = aux.get_resolution(cube.spectral_axis.value)
#    sd = aux.gaussian_width(current_resolution, aux.resolution) / current_resolution
#    print('Beginning spectral smoothing')
#    cube = cube.spectral_smooth(Gaussian1DKernel(sd)) # parallel execution doesn't work
#    print('Beginning spectral down scaling')
#    cube = cube.spectral_interpolate(nm * u.nm, suppress_smooth_warning=True, update_function=do_nothing)
#
#    # Spatial smoothing and down scaling
#    if isinstance(pixels_number, int):
#        smooth_factor = int(cube.shape[1] * cube.shape[2] / pixels_number)
#        print('Beginning spatial smoothing')
#        cube = cube.spatial_smooth(Gaussian2DKernel(smooth_factor))
#        print('Beginning spatial down scaling')
#        cube = cube[:,::smooth_factor,::smooth_factor]
#    
#    return Path(file).name, nm, np.array(cube).transpose((0, 2, 1))



# Legacy data_core.py multiresolution spectrum processing
# Code of summer 2023. Simplified in November 2023.

#resolutions = (5, 10, 20, 40, 80, 160) # nm
#def standardize_resolution(input: int):
#    """ Redirects the step size to one of the valid values """
#    res = resolutions[-1] # max possible step
#    for i in range(1, len(resolutions)):
#        if input < resolutions[i]:
#            res = resolutions[i-1] # accuracy is always in reserve
#            break
#    return res

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

