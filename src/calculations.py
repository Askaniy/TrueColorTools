import numpy as np


# Spectrum processing functions

H = 6.626e-34 # Planck constant
C = 299792458 # Speed of light
K = 1.381e-23 # Boltzmann constant
const1 = 2 * np.pi * H * C * C
const2 = H * C / K

def irradiance(nm, t):
    m = nm / 1e9
    return const1 / (m**5 * (np.exp(const2 / m / t) - 1) )

def blackbody_redshift(scope, temperature, velocity, vII):
    if temperature == 0:
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
            br.append(irradiance(nm*doppler*grav, temperature) / 1e9) # per m -> per nm
        else:
            br.append(0)
    return np.array(br)

V = 2.518021002e-8 # 1 Vega in W/m^2, https://arxiv.org/abs/1510.06262

def intensity2mag(e):
    return -2.5 * np.log10(e / V)

def mag2intensity(m):
    return V * 10**(-0.4 * m)


# Pivot wavelengths and ZeroPoints of filter bandpasses
# https://www.stsci.edu/~INS/2010CalWorkshop/pickles.pdf

# HST https://www.stsci.edu/~WFC3/PhotometricCalibration/ZP_calculating_wfc3.html
# https://www.stsci.edu/files/live/sites/www/files/home/hst/instrumentation/legacy/nicmos/_documents/nicmos_ihb_v10_cy17.pdf

filters = {
    'Tycho': {
        'b': {'nm': 419.6, 'zp': -0.108},
        'v': {'nm': 530.5, 'zp': -0.030}
    },
    'Landolt': {
        'u': {'nm': 354.6, 'zp': 0.761},
        'b': {'nm': 432.6, 'zp': -0.103},
        'v': {'nm': 544.5, 'zp': -0.014},
        'r': {'nm': 652.9, 'zp': 0.154},
        'i': {'nm': 810.4, 'zp': 0.405}
    },
    'UBVRI': {
        'u': {'nm': 358.9, 'zp': 0.763},
        'b': {'nm': 437.2, 'zp': -0.116},
        'v': {'nm': 549.3, 'zp': -0.014},
        'r': {'nm': 652.7, 'zp': 0.165},
        'i': {'nm': 789.1, 'zp': 0.368}
    },
    'Stromgren': {
        'us': {'nm': 346.1, 'zp': -0.290},
        'vs': {'nm': 410.7, 'zp': -0.316},
        'bs': {'nm': 467.0, 'zp': -0.181},
        'ys': {'nm': 547.6, 'zp': -0.041}
    },
    'Sloan Air': {
        "u'": {'nm': 355.2, 'zp': -0.033},
        "g'": {'nm': 476.6, 'zp': -0.009},
        "r'": {'nm': 622.6, 'zp': 0.004},
        "i'": {'nm': 759.8, 'zp': 0.008},
        "z'": {'nm': 890.6, 'zp': 0.009}
    },
    'Sloan Vacuum': {
        'u': {'nm': 355.7, 'zp': -0.034},
        'g': {'nm': 470.3, 'zp': -0.002},
        'r': {'nm': 617.6, 'zp': 0.003},
        'i': {'nm': 749.0, 'zp': 0.011},
        'z': {'nm': 889.2, 'zp': 0.007}
    },
    'New Horizons': { # New Horizons SOC to Instrument Pipeline ICD, p.76
        'pan1': {'nm': 651},
        'pan2': {'nm': 651},
        'blue': {'nm': 488},
        'red': {'nm': 612},
        'nir': {'nm': 850},
        'ch4': {'nm': 886}
    },
    'Hubble': {
        'f200lp': {'nm': 197.19, 'zp': 26.931},
        'f218w': {'nm': 222.8, 'zp': 21.278},
        'f225w': {'nm': 237.21, 'zp': 22.43},
        'f275w': {'nm': 270.97, 'zp': 22.677},
        'f280n': {'nm': 283.29, 'zp': 19.516},
        'f300x': {'nm': 282.05, 'zp': 23.565},
        'f336w': {'nm': 335.45, 'zp': 23.527},
        'f343n': {'nm': 343.52, 'zp': 22.754},
        'f350lp': {'nm': 587.39, 'zp': 26.81},
        'f373n': {'nm': 373.02, 'zp': 21.036},
        'f390m': {'nm': 389.72, 'zp': 23.545},
        'f390w': {'nm': 392.37, 'zp': 25.174},
        'f395n': {'nm': 395.52, 'zp': 22.712},
        'f410m': {'nm': 410.9, 'zp': 23.771},
        'f438w': {'nm': 432.62, 'zp': 25.003},
        'f467m': {'nm': 468.26, 'zp': 23.859},
        'f469n': {'nm': 468.81, 'zp': 21.981},
        'f475w': {'nm': 477.31, 'zp': 25.81},
        'f475x': {'nm': 494.07, 'zp': 26.216},
        'f487n': {'nm': 487.14, 'zp': 22.05},
        'f502n': {'nm': 500.96, 'zp': 22.421},
        'f547m': {'nm': 544.75, 'zp': 24.761},
        'f555w': {'nm': 530.84, 'zp': 25.841},
        'f600lp': {'nm': 746.81, 'zp': 25.554},
        'f606w': {'nm': 588.92, 'zp': 26.006},
        'f621m': {'nm': 621.89, 'zp': 24.465},
        'f625w': {'nm': 624.26, 'zp': 25.379},
        'f631n': {'nm': 630.43, 'zp': 21.723},
        'f645n': {'nm': 645.36, 'zp': 22.049},
        'f656n': {'nm': 656.14, 'zp': 19.868},
        'f657n': {'nm': 656.66, 'zp': 22.333},
        'f658n': {'nm': 658.4, 'zp': 20.672},
        'f665n': {'nm': 665.59, 'zp': 22.492},
        'f673n': {'nm': 676.59, 'zp': 22.343},
        'f680n': {'nm': 687.76, 'zp': 23.556},
        'f689m': {'nm': 687.68, 'zp': 24.196},
        'f763m': {'nm': 761.44, 'zp': 23.837},
        'f775w': {'nm': 765.14, 'zp': 24.48},
        'f814w': {'nm': 803.91, 'zp': 24.698},
        'f845m': {'nm': 843.91, 'zp': 23.316},
        'f850lp': {'nm': 917.61, 'zp': 23.326},
        'f953n': {'nm': 953.06, 'zp': 19.803},
        'f090m': {'nm': 900, 'zp': 0},
        'f110w': {'nm': 1100, 'zp': 0},
        'f110m': {'nm': 1100, 'zp': 0},
        'f140w': {'nm': 1400, 'zp': 0},
        'f145m': {'nm': 1450, 'zp': 0},
        'f150w': {'nm': 1500, 'zp': 0},
        'f160w': {'nm': 1600, 'zp': 0},
        'f165m': {'nm': 1700, 'zp': 0},
        'f170m': {'nm': 1700, 'zp': 0},
        'f171m': {'nm': 1715, 'zp': 0},
        'f175w': {'nm': 1750, 'zp': 0},
        'f180m': {'nm': 1800, 'zp': 0},
        'f187w': {'nm': 1875, 'zp': 0},
        'f204m': {'nm': 2040, 'zp': 0},
        'f205w': {'nm': 1900, 'zp': 0},
        'f207m': {'nm': 2100, 'zp': 0},
        'f222m': {'nm': 2300, 'zp': 0},
        'f237m': {'nm': 2375, 'zp': 0},
        'f240m': {'nm': 2400, 'zp': 0}
    }
}