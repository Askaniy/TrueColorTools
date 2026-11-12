""" Provides plotting functions. """

from collections.abc import Mapping, Sequence
from typing import Any, cast

import astrocolor as ac
import matplotlib.pyplot as plt
from cycler import cycler
from matplotlib import rc_context
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import truecolortools.strings as tr
from truecolortools import gui

# MatPlotLib custom theme
# https://matplotlib.org/stable/tutorials/introductory/customizing.html
errorbar_capsize = 3 # points
errorbar_color = '#7F7F7F' # exactly gray
rgb_muted = ('#904040', '#3c783c', '#5050e0')
rgb_cycler = cycler(color=rgb_muted)
dark_theme = {
    'text.color': gui.text_color, 'axes.labelcolor': gui.text_color,
    'axes.edgecolor': gui.muted_color, 'axes.grid': True, 'grid.color': gui.highlight_color,
    'xtick.color': gui.muted_color, 'ytick.color': gui.muted_color,
    'figure.facecolor': gui.bg_color, 'axes.facecolor': gui.inputON_color,
    'errorbar.capsize': errorbar_capsize, 'axes.prop_cycle': rgb_cycler
}
light_theme = {
    'text.color': '#000000', 'axes.labelcolor': '#000000',
    'axes.edgecolor': '#5C5C5C', 'axes.grid': True, 'grid.color': '#A5A5A5',
    'xtick.color': '#5C5C5C', 'ytick.color': '#5C5C5C',
    'figure.facecolor': '#FFFFFF', 'axes.facecolor': '#FFFFFF',
    'errorbar.capsize': errorbar_capsize, 'axes.prop_cycle': rgb_cycler
}
themes = (dark_theme, light_theme)
plt.rcParams |= dark_theme


def _display_name(name: object, lang: str) -> str:
    """ Returns a translated name for ObjectName and a plain string otherwise. """
    return str(name(lang)) if callable(name) else str(name)


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
        dict_to_plot: Mapping[ac.Spectrum | ac.Photospectrum, str],
        limit_to_vis: bool,
        normalize_at_550nm: bool,
        light_theme: bool,
        lang: str,
        figsize: tuple[float, float],
        dpi: int
    ):
    """ Creates a figure with plotted spectra from the input list """
    with rc_context(cast(Any, themes[int(light_theme)])):
        fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)
        ax.set_xlabel(tr.xaxis_text[lang])
        ax.set_ylabel(tr.yaxis_text[lang])
        not_empty = bool(dict_to_plot)
        spectra: list[Any] = []
        # Determining the scale for CMFs in the background
        if not_empty:
            max_y = []
            for spectrum in dict_to_plot:
                resolved = ac.get_spectrometry(
                    spectrum, ac.visible_range, strictly=limit_to_vis
                )
                resolved = cast(ac.Spectrum, resolved)
                if normalize_at_550nm:
                    resolved = cast(ac.Spectrum, ac.scale_to_match_value(resolved, 550))
                spectra.append(resolved)
                max_y.append(resolved.spectral_dist.max())
            k = max(max_y) / ac.xyz_cmf[2].spectral_dist.max()
        else:
            k = 1
        # Plotting the CMFs
        for i, cmf in enumerate(ac.xyz_cmf):
            ax.plot(cmf.wavelength_nm, cmf.spectral_dist * k, color=rgb_muted[i])
        # Plotting the spectra
        if not_empty:
            for spectrum, color in zip(spectra, dict_to_plot.values()):
                ax.plot(
                    spectrum.wavelength_nm,
                    spectrum.spectral_dist,
                    label=_display_name(spectrum.name, lang),
                    color=color,
                )
                photospectral_obj = getattr(spectrum, 'photospectral_obj', None)
                if photospectral_obj is not None:
                    ax.errorbar(
                        x=photospectral_obj.filter_set.mean_nm(),
                        y=photospectral_obj.spectral_dist,
                        xerr=photospectral_obj.filter_set.std_of_nm(),
                        yerr=photospectral_obj.standard_deviation,
                        fmt='o', color=errorbar_color
                    )
                if spectrum.standard_deviation is not None:
                    # 1σ confidence band
                    y_limit = ax.get_ylim()
                    ax.fill_between(
                        spectrum.wavelength_nm,
                        spectrum.spectral_dist - spectrum.standard_deviation,
                        spectrum.spectral_dist + spectrum.standard_deviation,
                        color=errorbar_color, alpha=0.25
                    )
                    ax.set_ylim(y_limit)
            ax.legend()
        # Forcefully clip the X-axis range (required for photospectrum objects)
        if limit_to_vis:
            ax.set_xlim(ac.visible_range[0], ac.visible_range[-1])
        fig.tight_layout()
        return fig


def plot_filters(filters: Sequence[ac.Filter], color_system: ac.ColorSystem, lang: str, figsize: tuple[float, float], dpi: int):
    """
    Creates a figure with plotted filter profiles and the color matching functions.
    The curves are normalized by their maximum value.
    """
    fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)
    ax.set_xlabel(tr.xaxis_text[lang])
    # Plotting the CMFs
    ax.plot(ac.xyz_cmf.wavelength_nm, ac.xyz_cmf.spectral_dist / ac.xyz_cmf.spectral_dist.max(axis=0))
    # Color calculating and plotting
    for profile in filters:
        color = ac.ColorPoint.from_spectral_data(profile).to_color_system(color_system)
        settings = ac.DisplaySettings(
            color_system=color_system,
            gamma_correction=True,
            maximize_brightness=True,
        )
        ax.plot(
            profile.wavelength_nm,
            profile.spectral_dist / profile.spectral_dist.max(),
            label=_display_name(profile.name, lang),
            color=color.to_html(settings),
        )
    fig.tight_layout()
    return fig
