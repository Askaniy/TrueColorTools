import numpy as np
from scipy.interpolate import Akima1DInterpolator
import cmf, database


# Phase curves processing functions

def lambert(phase):
    phi = abs(np.deg2rad(phase))
    return (np.sin(phi) + np.pi * np.cos(phi) - phi * np.cos(phi)) / np.pi # * 2/3 * albedo


# Spectrum processing functions

H = 6.626e-34 # Planck constant
C = 299792458 # Speed of light
K = 1.381e-23 # Boltzmann constant
const1 = 2 * np.pi * H * C * C
const2 = H * C / K

def irradiance(nm, t):
    m = nm / 1e9
    return const1 / (m**5 * (np.exp(const2 / m / t) - 1) )

def blackbody_redshift(scope, tempurature, velocity, vII):
    if tempurature == 0:
        physics = False
    else:
        physics = True
        if velocity == 0:
            doppler = 1
        else:
            if abs(velocity) != 1:
                doppler = np.sqrt((1-velocity) / (1+velocity))
            else:
                physics = False
        if vII == 0:
            grav = 1
        else:
            if vII != 1:
                grav = np.exp(-vII*vII/2)
            else:
                physics = False
    br = []
    for nm in scope:
        if physics:
            br.append(irradiance(nm*doppler*grav, tempurature) / 1e9) # per m -> per nm
        else:
            br.append(0)
    return np.array(br)

def polator(x, y, scope, albedo=0, fast=False):
    mn = scope[0]
    mx = scope[-1]
    extrap = True if x[0] > mn or x[-1] < mx else False
    br = []
    if fast:
        a = y[0] / x[0]
        b = 0
        x.append(x[-1] + 1000)
        y.append(0)
        nm = mn
        flag = False
        for i, ax in enumerate(x):
            while nm <= ax:
                if nm <= mx:
                    br.append(a * nm + b)
                    nm += 5
                else:
                    flag = True
                    break
            if flag:
                break
            else:
                ay = y[i]
                bx = x[i+1]
                by = y[i+1]
                ay_by = ay - by
                ax_bx = ax - bx
                a = ay_by / ax_bx
                b = by - bx * a
    else: # qualitatively
        if not extrap:
            br = Akima1DInterpolator(x, y)(scope)
        else: # if extrapolation is needed
            x = [x[0] - 250] + x + [x[-1] + 1000]
            y = [0] + y + [0]
            interp = Akima1DInterpolator(x, y)
            line = lambda wl: y[1] + (wl - x[1]) * (y[-2] - y[1]) / (x[-2] - x[1])
            for nm in scope:
                if x[1] < nm < x[-2]:
                    br.append(interp(nm))
                else:
                    br.append((line(nm) + interp(nm)) / 2)
    curve = np.clip(br, 0, None)
    if albedo:
        br550 = curve[scope.index(550)]
        curve = curve / br550 * albedo
    return curve

# to do - def gauss(x): return np.exp(- x**2 / 2) / np.sqrt(2 * np.pi)
def get_points(pivots, nm_list, br_list, albedo=0, wide=100, low_res=True):
    r = int(wide/2)
    scopes = []
    if low_res:
        for pivot in pivots:
            scope = polator(nm_list, br_list, range(pivot-r, pivot+r, 5), albedo)
            scopes.append(np.mean(scope))
    else:
        for pivot in pivots:
            scope = []
            for nm, br in zip(nm_list, br_list):
                if nm-r < pivot < nm+r:
                    scope.append(br)
            scopes.append(np.mean(scope))
    return scopes

def from_filters(data):
    nm = []
    for band in data["bands"]:
        name = band.lower()
        for filter, info in filters[data["filters"]].items():
            if filter == name:
                nm.append(info["nm"])
    data.update({"nm": nm})
    return data

def from_indices(data):
    result = {}
    for index, value in data["indices"].items():
        band1, band2 = index.lower().split("-")
        if result == {}:
            result.update({band1: 1.0})
        if band1 in result:
            k = filters[data["filters"]][band1]["zp"] - filters[data["filters"]][band2]["zp"]
            result.update({band2: result[band1] * 10**(0.4*(value + k))})
    nm = []
    br = []
    for band, value in result.items():
        nm.append(filters[data["filters"]][band]["nm"])
        br.append(value / (filters[data["filters"]][band]["nm"]/1e9)**2)
    data.update({"nm": nm, "br": br})
    return data

def from_magnitudes(data, vega):
    if "vega" not in data:
        data.update({"vega": True})
    br = []
    waves = get_points(data["nm"], vega["nm"], vega["br"], low_res=False)
    for ref, mag in zip(waves, data["mag"]):
        br.append(ref * 10**(-0.4*mag) if data["vega"] else 10**(-0.4*mag))
    data.update({"br": br})
    return data

def subtract_sun(spectrum, sun):
    nm = []
    br = []
    interp = Akima1DInterpolator(spectrum["nm"], spectrum["br"])
    for sun_nm, sun_br in zip(sun["nm"], sun["br"]):
        corrected = interp(sun_nm) / sun_br
        if not np.isnan(corrected):
            br.append(corrected)
            nm.append(sun_nm)
    spectrum.update({"nm": nm, "br": br, "sun": False})
    return spectrum

def transform(spectrum):
    if "filters" in spectrum:
        if "bands" in spectrum:
            spectrum = from_filters(spectrum) # replacement of filters for their wavelengths
        elif "indices" in spectrum:
            spectrum = from_indices(spectrum) # spectrum from color indices
        spectrum.pop("filters")
    if "mag" in spectrum:
        spectrum = from_magnitudes(spectrum, database.objects["Vega|1"]) # spectrum from magnitudes
        spectrum.pop("mag")
    if "sun" in spectrum:
        if spectrum["sun"]:
            spectrum = subtract_sun(spectrum, database.objects["Sun|1"]) # subtract solar spectrum
    return spectrum


# Color processing functions

xyz_from_xy = lambda x, y: np.array((x, y, 1-x-y))

def xyz_to_sRGB(xyz):
    # https://scipython.com/blog/converting-a-spectrum-to-a-colour/
    r = xyz_from_xy(0.64, 0.33)
    g = xyz_from_xy(0.30, 0.60)
    b = xyz_from_xy(0.15, 0.06)
    white = xyz_from_xy(0.3127, 0.3291) # D65
    M = np.vstack((r, g, b)).T
    MI = np.linalg.inv(M)
    wscale = MI.dot(white)
    T = MI / wscale[:, np.newaxis]
    rgb = T.dot(xyz)
    if np.any(rgb < 0): # We're not in the sRGB gamut: approximate by desaturating
        w = - np.min(rgb)
        rgb += w
    return rgb

gamma_correction = np.vectorize(lambda grayscale: grayscale * 12.92 if grayscale < 0.0031308 else 1.055 * grayscale**(1.0/2.4) - 0.055)
rounder = np.vectorize(lambda grayscale, d_places: int(round(grayscale)) if d_places == 0 else round(grayscale, d_places))
def to_bit(color, bit): return color * (2**bit - 1)
def to_html(color): return "#{:02x}{:02x}{:02x}".format(*rounder(to_bit(color, 8), 0))

def to_rgb(spectrum, mode="chromaticity", inp_bit=None, exp_bit=None, rnd=0, albedo=False, phase=0, gamma=False, srgb=False, html=False):
    if inp_bit:
        spectrum /= (2**inp_bit - 1)
    if srgb:
        xyz = np.sum(spectrum[:, np.newaxis] * cmf.xyz, axis=0)
        rgb = xyz_to_sRGB(xyz)
        rgb = rgb / rgb[1] * spectrum[38] # xyz cmf is not normalized, so result was overexposed; spectrum[38] is 550 nm
    else:
        rgb = np.sum(spectrum[:, np.newaxis] * cmf.rgb, axis=0)
    if mode == "albedo 0.5":
        if rgb[1] != 0:
            rgb /= 2 * rgb[1]
    elif mode == "albedo" and albedo:
        if html:
            rgb = np.clip(rgb, 0, 1)
    else: # "chromaticity" and when albedo == False
        mx = np.max(rgb)
        if mx != 0:
            rgb /= mx
    if phase != 0:
        rgb *= lambert(phase)
    if gamma:
        rgb = gamma_correction(rgb)
    if rgb.min() < 0:
        # print(f'Negative RGB values were clipped: {rgb}')
        rgb = np.clip(rgb, 0, None)
    if html:
        return to_html(rgb)
    else:
        return tuple(rounder(rgb if not exp_bit else to_bit(rgb, exp_bit), rnd))


# Pivot wavelengths and ZeroPoints of filter bandpasses
# https://www.stsci.edu/~INS/2010CalWorkshop/pickles.pdf

# HST https://www.stsci.edu/~WFC3/PhotometricCalibration/ZP_calculating_wfc3.html
# https://www.stsci.edu/files/live/sites/www/files/home/hst/instrumentation/legacy/nicmos/_documents/nicmos_ihb_v10_cy17.pdf

filters = {
    "Tycho": {
        "b": {"nm": 419.6, "zp": -0.108},
        "v": {"nm": 530.5, "zp": -0.030}
    },
    "Landolt": {
        "u": {"nm": 354.6, "zp": 0.761},
        "b": {"nm": 432.6, "zp": -0.103},
        "v": {"nm": 544.5, "zp": -0.014},
        "r": {"nm": 652.9, "zp": 0.154},
        "i": {"nm": 810.4, "zp": 0.405}
    },
    "UBVRI": {
        "u": {"nm": 358.9, "zp": 0.763},
        "b": {"nm": 437.2, "zp": -0.116},
        "v": {"nm": 549.3, "zp": -0.014},
        "r": {"nm": 652.7, "zp": 0.165},
        "i": {"nm": 789.1, "zp": 0.368}
    },
    "Stromgren": {
        "us": {"nm": 346.1, "zp": -0.290},
        "vs": {"nm": 410.7, "zp": -0.316},
        "bs": {"nm": 467.0, "zp": -0.181},
        "ys": {"nm": 547.6, "zp": -0.041}
    },
    "Sloan Air": {
        "u'": {"nm": 355.2, "zp": -0.033},
        "g'": {"nm": 476.6, "zp": -0.009},
        "r'": {"nm": 622.6, "zp": 0.004},
        "i'": {"nm": 759.8, "zp": 0.008},
        "z'": {"nm": 890.6, "zp": 0.009}
    },
    "Sloan Vacuum": {
        "u": {"nm": 355.7, "zp": -0.034},
        "g": {"nm": 470.3, "zp": -0.002},
        "r": {"nm": 617.6, "zp": 0.003},
        "i": {"nm": 749.0, "zp": 0.011},
        "z": {"nm": 889.2, "zp": 0.007}
    },
    "New Horizons": { # New Horizons SOC to Instrument Pipeline ICD, p.76
        "pan1": {"nm": 651},
        "pan2": {"nm": 651},
        "blue": {"nm": 488},
        "red": {"nm": 612},
        "nir": {"nm": 850},
        "ch4": {"nm": 886}
    },
    "Hubble": {
        "f200lp": {"nm": 197.19, "zp": 26.931},
        "f218w": {"nm": 222.8, "zp": 21.278},
        "f225w": {"nm": 237.21, "zp": 22.43},
        "f275w": {"nm": 270.97, "zp": 22.677},
        "f280n": {"nm": 283.29, "zp": 19.516},
        "f300x": {"nm": 282.05, "zp": 23.565},
        "f336w": {"nm": 335.45, "zp": 23.527},
        "f343n": {"nm": 343.52, "zp": 22.754},
        "f350lp": {"nm": 587.39, "zp": 26.81},
        "f373n": {"nm": 373.02, "zp": 21.036},
        "f390m": {"nm": 389.72, "zp": 23.545},
        "f390w": {"nm": 392.37, "zp": 25.174},
        "f395n": {"nm": 395.52, "zp": 22.712},
        "f410m": {"nm": 410.9, "zp": 23.771},
        "f438w": {"nm": 432.62, "zp": 25.003},
        "f467m": {"nm": 468.26, "zp": 23.859},
        "f469n": {"nm": 468.81, "zp": 21.981},
        "f475w": {"nm": 477.31, "zp": 25.81},
        "f475x": {"nm": 494.07, "zp": 26.216},
        "f487n": {"nm": 487.14, "zp": 22.05},
        "f502n": {"nm": 500.96, "zp": 22.421},
        "f547m": {"nm": 544.75, "zp": 24.761},
        "f555w": {"nm": 530.84, "zp": 25.841},
        "f600lp": {"nm": 746.81, "zp": 25.554},
        "f606w": {"nm": 588.92, "zp": 26.006},
        "f621m": {"nm": 621.89, "zp": 24.465},
        "f625w": {"nm": 624.26, "zp": 25.379},
        "f631n": {"nm": 630.43, "zp": 21.723},
        "f645n": {"nm": 645.36, "zp": 22.049},
        "f656n": {"nm": 656.14, "zp": 19.868},
        "f657n": {"nm": 656.66, "zp": 22.333},
        "f658n": {"nm": 658.4, "zp": 20.672},
        "f665n": {"nm": 665.59, "zp": 22.492},
        "f673n": {"nm": 676.59, "zp": 22.343},
        "f680n": {"nm": 687.76, "zp": 23.556},
        "f689m": {"nm": 687.68, "zp": 24.196},
        "f763m": {"nm": 761.44, "zp": 23.837},
        "f775w": {"nm": 765.14, "zp": 24.48},
        "f814w": {"nm": 803.91, "zp": 24.698},
        "f845m": {"nm": 843.91, "zp": 23.316},
        "f850lp": {"nm": 917.61, "zp": 23.326},
        "f953n": {"nm": 953.06, "zp": 19.803},
        "f090m": {"nm": 900, "zp": 0},
        "f110w": {"nm": 1100, "zp": 0},
        "f110m": {"nm": 1100, "zp": 0},
        "f140w": {"nm": 1400, "zp": 0},
        "f145m": {"nm": 1450, "zp": 0},
        "f150w": {"nm": 1500, "zp": 0},
        "f160w": {"nm": 1600, "zp": 0},
        "f165m": {"nm": 1700, "zp": 0},
        "f170m": {"nm": 1700, "zp": 0},
        "f171m": {"nm": 1715, "zp": 0},
        "f175w": {"nm": 1750, "zp": 0},
        "f180m": {"nm": 1800, "zp": 0},
        "f187w": {"nm": 1875, "zp": 0},
        "f204m": {"nm": 2040, "zp": 0},
        "f205w": {"nm": 1900, "zp": 0},
        "f207m": {"nm": 2100, "zp": 0},
        "f222m": {"nm": 2300, "zp": 0},
        "f237m": {"nm": 2375, "zp": 0},
        "f240m": {"nm": 2400, "zp": 0}
    }
}