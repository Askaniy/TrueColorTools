from typing import TypeVar, Iterable, Tuple
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import src.core as core
import src.strings as tr
import src.gui as gui

# MatPlotLib custom theme
# https://matplotlib.org/stable/tutorials/introductory/customizing.html
plt.rcParams |= {
    'text.color': gui.text_color, 'axes.labelcolor': gui.text_color,
    'axes.edgecolor': gui.muted_color, 'xtick.color': gui.muted_color, 'ytick.color': gui.muted_color,
    'figure.facecolor': gui.bg_color, 'axes.facecolor': gui.inputON_color,
    'axes.grid': True, 'grid.color': gui.highlight_color
    }

rgb_muted = ('#904040', '#3c783c', '#5050e0')

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def plot_spectra(objects: Iterable[core.Spectrum], gamma, srgb, albedo, lang: str):
    """ Opens a separate window with plotted spectra from the input list """
    fig, ax = plt.subplots(1, 1, figsize=(9, 6), dpi=100)
    ax.set_xlabel(tr.xaxis_text[lang])
    # determining the scale for CMFs in the background
    max_y = []
    for spectrum in objects:
        max_y.append(spectrum.br.max())
    rgb = (core.x, core.y, core.z) if srgb else (core.r, core.g, core.b)
    k = max(max_y) / rgb[2].br.max() if len(max_y) != 0 else 1
    # adding CMFs on the background
    for i, spectrum in enumerate(rgb):
        ax.plot(spectrum.nm, spectrum.br*k, label=spectrum.name, color=rgb_muted[i])
    # color calculating and plotting
    for spectrum in objects:
        if srgb:
            color = core.Color.from_spectrum(spectrum, albedo)
        else:
            color = core.Color.from_spectrum_legacy(spectrum, albedo)
        if gamma:
            color = color.gamma_corrected()
        ax.plot(spectrum.nm, spectrum.br, label=spectrum.name, color=color.to_html())
    ax.legend()
    fig.tight_layout()
    # creating and opening the window
    title = tr.spectral_plot[lang]
    layout = [
        [sg.Text(title, font=('arial', 16)), sg.Push(), sg.InputText(visible=False, enable_events=True, key='-path-'),
         sg.FileSaveAs(tr.gui_save[lang], file_types=('PNG {png}', 'PDF {pdf}', 'SVG {svg}'), default_extension='.png')],
        [sg.Canvas(key='-canvas-')]
    ]
    window = sg.Window(title, layout, finalize=True, element_justification='center')
    draw_figure(window['-canvas-'].TKCanvas, fig)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == '-path-':
            path = values['-path-']
            fig.savefig(path, dpi=133.4) # 1200x800
    window.close()

def plot_filters(filters: Iterable[core.Spectrum]):
    """ Creates a figure with plotted sensitive curves and CMFs """
    fig, ax = plt.subplots(1, 1, figsize=(5, 1.5), dpi=90)
    # determining the scale for CMFs in the background
    max_y = []
    for spectrum in filters[3:]:
        max_y.append(spectrum.br.max())
    k = max(max_y) / filters[2].br.max() if len(max_y) != 0 else 1
    # color calculating and plotting
    for i, spectrum in enumerate(filters):
        if i < 3: # the first three spectra are scaled sensitivity curves
            br = spectrum.br*k
            color = rgb_muted[i]
        else:
            br = spectrum.br
            color = core.Color.from_spectrum_legacy(spectrum).gamma_corrected().to_html()
        ax.plot(spectrum.nm, br, label=spectrum.name, color=color)
    fig.tight_layout()
    return fig