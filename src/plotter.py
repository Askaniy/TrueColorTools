import warnings
from typing import TypeVar, Iterable, Tuple
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import src.core as core
import src.strings as tr
import src.gui as gui

# Filling empty space on a plot
warnings.simplefilter('ignore', UserWarning)
plt.rcParams['figure.autolayout'] = True

# MatPlotLib custom theme
# https://matplotlib.org/stable/tutorials/introductory/customizing.html
plt.rcParams |= {
    'text.color': gui.text_color, 'axes.labelcolor': gui.text_color,
    'axes.edgecolor': gui.muted_color, 'xtick.color': gui.muted_color, 'ytick.color': gui.muted_color,
    'figure.facecolor': gui.bg_color, 'axes.facecolor': gui.inputON_color,
    'axes.grid': True, 'grid.color': gui.highlight_color
    }

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def plot_spectra(objects: Iterable, lang: str):
    """ Creates a separate window with plotted spectra from the input list """
    fig = plt.Figure(figsize=(9, 6), dpi=100)
    ax = fig.add_subplot(111, xlabel=tr.xaxis_text[lang])
    for obj in objects:
        ax.plot(obj[0], obj[1], label=obj[2], color=obj[3])
    if len(objects) > 0:
        ax.legend()
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
    fig = plt.Figure(figsize=(5, 2), dpi=90)
    ax = fig.add_subplot(111)
    nm_min = 400
    nm_max = 700
    br_max = 0
    for obj in filters:
        if obj.nm[0] < nm_min: # not pythonic, but fast
            nm_min = obj.nm[0]
        if obj.nm[-1] > nm_max:
            nm_max = obj.nm[-1]
        max_y = max(obj.br)
        if max_y > br_max:
            br_max = max_y
    if br_max == 0:
        br_max = 1
    rgb_muted = ('#804040', '#3c783c', '#5050a0')
    for i, obj in enumerate(filters):
        if i < 3: # the first three spectra are scaled sensitivity curves
            br = obj.br*br_max
            color = rgb_muted[i]
        else:
            br = obj.br
            color = core.Color.from_spectrum_legacy(obj).to_html()
        ax.plot(obj.nm, br, label=obj.name, color=color)
    ax.set_xlim(nm_min, nm_max)
    return fig