import numpy as np


# Phase curves processing functions

def lambert(phase: float):
    phi = abs(np.deg2rad(phase))
    return (np.sin(phi) + np.pi * np.cos(phi) - phi * np.cos(phi)) / np.pi # * 2/3 * albedo


# Magnitudes processing functions

V = 2.518021002e-8 # 1 Vega in W/m^2, https://arxiv.org/abs/1510.06262

def mag2intensity(m: int|float|np.ndarray):
    return V * 10**(-0.4 * m)

#def intensity2mag(e):
#    return -2.5 * np.log10(e / V)


# Linear extrapolation

def line_generator(x1, y1, x2, y2):
    return np.vectorize(lambda wl: y1 + (wl - x1) * (y2 - y1) / (x2 - x1))

def custom_interp(x1: np.ndarray, x0: np.ndarray, y0: np.ndarray, k=4):
    """ Unsuccessful generalization of the interpolation algorithm """
    step = x0[1] - x0[0]
    y1 = []
    counter = 0
    for x in x1:
        if x <= x0[0] or x >= x0[-1]: # extrapolation is not supported
            y1.append(0.)
        else:
            t = x - x0[counter]
            while t > step:
                counter += 1
                t = x - x0[counter]
            xi = t / step
            l = y0[counter]
            try:
                ll = y0[counter-1]
            except IndexError:
                ll = l
            r = y0[counter+1]
            try:
                rr = y0[counter+2]
            except IndexError:
                rr = r
            m = (l+r)/2
            y = m + (xi*(rr-ll) + m - rr) / k
            y1.append(y)
    return y1