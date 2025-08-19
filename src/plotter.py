""" Provides plotting functions. """

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import rc_context
import matplotlib.pyplot as plt

from src.core import *
from src.core import _TrueColorToolsObject, FilterSystem, ColorSystem
import src.strings as tr
import src.gui as gui

# MatPlotLib custom theme
# https://matplotlib.org/stable/tutorials/introductory/customizing.html
errorbar_capsize = 3 # points
errorbar_color = '#7F7F7F' # exactly gray
dark_theme = {
    'text.color': gui.text_color, 'axes.labelcolor': gui.text_color,
    'axes.edgecolor': gui.muted_color, 'axes.grid': True, 'grid.color': gui.highlight_color,
    'xtick.color': gui.muted_color, 'ytick.color': gui.muted_color,
    'figure.facecolor': gui.bg_color, 'axes.facecolor': gui.inputON_color,
    'errorbar.capsize': errorbar_capsize
}
light_theme = {
    'text.color': '#000000', 'axes.labelcolor': '#000000',
    'axes.edgecolor': '#5C5C5C', 'axes.grid': True, 'grid.color': '#A5A5A5',
    'xtick.color': '#5C5C5C', 'ytick.color': '#5C5C5C',
    'figure.facecolor': '#FFFFFF', 'axes.facecolor': '#FFFFFF',
    'errorbar.capsize': errorbar_capsize
}
themes = (dark_theme, light_theme)
plt.rcParams |= dark_theme

rgb_muted = ('#904040', '#3c783c', '#5050e0')
cmfs = FilterSystem.from_list(('StilesBurch2deg.r', 'StilesBurch2deg.g', 'StilesBurch2deg.b'), name='RGB')

def close_figure(figure: Figure):
    """ Removes the figure from memory """
    plt.close(figure)

def draw_figure(canvas, figure: Figure):
    """ Places the figure on the canvas that can be displayed """
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def plot_spectra(
        spectra: Sequence[_TrueColorToolsObject], color_system: ColorSystem,
        gamma_correction: bool, maximize_brightness: bool,
        light_theme: bool, lang: str, figsize: tuple, dpi: int
    ):
    """ Creates a figure with plotted spectra from the input list and the CMFs used """
    with rc_context(themes[int(light_theme)]):
        fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)
        ax.set_xlabel(tr.xaxis_text[lang])
        ax.set_ylabel(tr.yaxis_text[lang])
        # Determining the scale for CMFs in the background
        max_y = []
        for spectrum in spectra:
            max_y.append(spectrum.br.max())
        k = max(max_y) / cmfs[2].br.max() if len(max_y) != 0 else 1
        # Plotting the CMFs
        for i, cmf in enumerate(cmfs):
            ax.plot(cmf.nm, cmf.br * k, label=cmf.name(lang), color=rgb_muted[i])
        # Color calculating and plotting
        for photospectrum_or_spectrum in spectra:
            color = ColorPoint.from_spectral_data(photospectrum_or_spectrum, color_system)
            color.gamma_correction = gamma_correction
            color.maximize_brightness = maximize_brightness
            spectrum: Spectrum = photospectrum_or_spectrum.define_on_range(visible_range)
            ax.plot(spectrum.nm, spectrum.br, label=spectrum.name(lang), color=color.to_html())
            if spectrum.photospectrum is not None:
                ax.errorbar(
                    x=spectrum.photospectrum.filter_system.mean_nm(), y=spectrum.photospectrum.br,
                    xerr=spectrum.photospectrum.filter_system.sd_of_nm(), yerr=spectrum.photospectrum.sd,
                    fmt='o', color=errorbar_color
                )
            if spectrum.sd is not None:
                # 1σ confidence band
                y_lim = ax.get_ylim()
                ax.fill_between(
                    spectrum.nm, spectrum.br-spectrum.sd, spectrum.br+spectrum.sd,
                    color=errorbar_color, alpha=0.25
                )
                ax.set_ylim(y_lim)
        ax.legend()
        fig.tight_layout() # moving to subplots() causes UserWarning
        return fig

def plot_filters(filters: Sequence[Spectrum], color_system: ColorSystem, lang: str, figsize: tuple, dpi: int):
    """ Creates a figure with plotted sensitive curves and the CMFs used """
    fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)
    ax.set_xlabel(tr.xaxis_text[lang])
    # Determining the scale for CMFs in the background
    max_y = []
    for spectrum in filters:
        max_y.append(spectrum.br.max())
    k = max(max_y) / cmfs[2].br.max() if len(max_y) != 0 else 1
    # Plotting the CMFs
    for i, cmf in enumerate(cmfs):
        ax.plot(cmf.nm, cmf.br * k, label=cmf.name(lang), color=rgb_muted[i])
    # Color calculating and plotting
    for i, spectrum in enumerate(filters):
        color = ColorPoint.from_spectral_data(spectrum, color_system)
        color.gamma_correction = True
        color.maximize_brightness = True
        ax.plot(spectrum.nm, spectrum.br, label=spectrum.name(lang), color=color.to_html())
    fig.tight_layout() # moving to subplots() causes UserWarning
    return fig
