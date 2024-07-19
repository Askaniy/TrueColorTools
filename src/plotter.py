""" Provides plotting functions. """

from typing import Sequence
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import rc_context
import matplotlib.pyplot as plt
from src.data_core import Spectrum
import src.color_processing as cp
import src.strings as tr
import src.gui as gui

# MatPlotLib custom theme
# https://matplotlib.org/stable/tutorials/introductory/customizing.html
errorbar_capsize = 5 # points
dark_theme = {
    'text.color': gui.text_color, 'axes.labelcolor': gui.text_color,
    'axes.edgecolor': gui.muted_color, 'xtick.color': gui.muted_color, 'ytick.color': gui.muted_color,
    'figure.facecolor': gui.bg_color, 'axes.facecolor': gui.inputON_color,
    'axes.grid': True, 'grid.color': gui.highlight_color, 'errorbar.capsize': errorbar_capsize,
}
light_theme = {
    'text.color': '#000000', 'axes.labelcolor': '#000000',
    'axes.edgecolor': '#5C5C5C', 'xtick.color': '#5C5C5C', 'ytick.color': '#5C5C5C',
    'figure.facecolor': '#FFFFFF', 'axes.facecolor': '#FFFFFF',
    'axes.grid': True, 'grid.color': '#A5A5A5', 'errorbar.capsize': errorbar_capsize,
}
themes = (dark_theme, light_theme)
plt.rcParams |= dark_theme


rgb_muted = ('#904040', '#3c783c', '#5050e0')
background_CMFs = ((cp.r, cp.g, cp.b), (cp.x, cp.y, cp.z))


def close_figure(figure: Figure):
    """ Removes the figure from memory """
    plt.close(figure)

def draw_figure(canvas, figure: Figure):
    """ Places the figure on the canvas that can be displayed """
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def plot_spectra(spectra: Sequence[Spectrum], gamma: bool, srgb: bool, albedo: bool, light_theme: bool, lang: str):
    """ Creates a figure with plotted spectra from the input list and the CMFs used """
    with rc_context(themes[int(light_theme)]):
        fig, ax = plt.subplots(1, 1, figsize=(9, 6), dpi=100)
        ax.set_xlabel(tr.xaxis_text[lang])
        ax.set_ylabel(tr.yaxis_text[lang])
        # Determining the scale for CMFs in the background
        max_y = []
        for spectrum in spectra:
            max_y.append(spectrum.br.max())
        rgb = background_CMFs[srgb]
        k = max(max_y) / rgb[2].br.max() if len(max_y) != 0 else 1
        # Plotting the CMFs
        for i, cmf in enumerate(rgb):
            ax.plot(cmf.nm, cmf.br * k, label=cmf.name(lang), color=rgb_muted[i])
        # Color calculating and plotting
        for spectrum in spectra:
            color = cp.ColorPoint.from_spectral_data(spectrum, albedo, srgb)
            if gamma:
                color = color.gamma_corrected()
            ax.plot(spectrum.nm, spectrum.br, label=spectrum.name(lang), color=color.to_html())
            if spectrum.photospectrum is not None:
                fmt = 'o' if spectrum.photospectrum.sd is None else ''
                ax.errorbar(
                    x=spectrum.photospectrum.mean_wavelengths(), y=spectrum.photospectrum.br,
                    xerr=spectrum.photospectrum.standard_deviations(), yerr=spectrum.photospectrum.sd,
                    fmt=fmt, linestyle='none', color='#7F7F7F'
                )
        ax.legend()
        fig.tight_layout() # moving to subplots() causes UserWarning
        return fig

def plot_filters(filters: Sequence[Spectrum], srgb: bool, lang: str):
    """ Creates a figure with plotted sensitive curves and the CMFs used """
    fig, ax = plt.subplots(1, 1, figsize=(5.25, 1.75), dpi=90)
    ax.set_xlabel(tr.xaxis_text[lang])
    # Determining the scale for CMFs in the background
    max_y = []
    for spectrum in filters:
        max_y.append(spectrum.br.max())
    rgb = background_CMFs[srgb]
    k = max(max_y) / rgb[2].br.max() if len(max_y) != 0 else 1
    # Plotting the CMFs
    for i, cmf in enumerate(rgb):
        ax.plot(cmf.nm, cmf.br * k, label=cmf.name(lang), color=rgb_muted[i])
    # Color calculating and plotting
    for i, spectrum in enumerate(filters):
        color = cp.ColorPoint.from_spectral_data(spectrum, srgb=srgb).gamma_corrected().to_html()
        ax.plot(spectrum.nm, spectrum.br, label=spectrum.name(lang), color=color)
    fig.tight_layout() # moving to subplots() causes UserWarning
    return fig