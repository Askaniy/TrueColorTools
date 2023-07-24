import warnings
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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

def plot_spectra(names: list, objects: list, lang: str):
    title = tr.single_title_text[lang] + names[0] if len(names) == 1 else tr.batch_title_text[lang] + ', '.join(names)
    fig = plt.Figure(figsize=(6, 4), dpi=125)
    ax = fig.add_subplot(111, xlabel=tr.xaxis_text[lang])
    for name, obj in zip(names, objects):
        ax.plot(obj[0], obj[1], color=obj[2], label=name)
    layout = [[sg.Text(title)], [sg.Canvas(key='-canvas-')]]
    window = sg.Window('True Color Tools: Plot', layout, finalize=True, font='arial 18')
    fig_canvas_agg = draw_figure(window['-canvas-'].TKCanvas, fig)
    event, values = window.read()
    window.close()