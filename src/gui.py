""" Responsible for the creation and translation of the graphical interface. """

from typing import Callable
from time import strftime
import PySimpleGUI as sg
import src.strings as tr

# TCT style colors
main_color = '#3884A9' # HSV 199.65° 66.86% 66.27%
#main_color = '#5D9BBA' # HSV 200.00° 50.00% 72.94% (0.5^1/2.2 = 72.974%)
text_color = '#FFFFFF'
muted_color = '#A3A3A3'
highlight_color = '#5A5A5A'
bg_color = '#333333'
inputON_color = '#424242'
inputOFF_color = '#3A3A3A'

# PySimpleGUI custom theme
sg.LOOK_AND_FEEL_TABLE['MaterialDark'] = {
        'BACKGROUND': bg_color, 'TEXT': text_color,
        'INPUT': inputON_color, 'TEXT_INPUT': text_color, 'SCROLL': inputON_color,
        'BUTTON': (text_color, main_color), 'PROGRESS': ('#000000', '#000000'),
        'BORDER': 0, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0
    }

def create_logger(window: sg.Window, key: str) -> Callable:
    """ Creates a function that sends messages to the window main thread """
    def logger(message: str, data=None):
        window.write_event_value((key, f'{strftime("%H:%M:%S")} {message}'), data)
    return logger

def generate_layout(canvas_size: tuple, img_preview_size: tuple, text_colors: tuple, filtersDB: tuple, bitness: int, rounding: int, T2_num: int, lang: str):
    title_font = ('arial', 12)
    tags_input_size = 20
    button_size = 24
    browse_size = 10
    slider_size = (1, 15)

    settings_column = sg.Column([
        [sg.Push(), sg.Text(tr.gui_settings[lang], font=title_font, key='-settingsTitle-'), sg.Push()],
        [sg.T('')],
        [sg.Checkbox(tr.gui_gamma[lang], enable_events=True, default=True, key='-gamma-')],
        [sg.Checkbox('sRGB', enable_events=True, key='-srgb-')],
        [sg.T('')],
        [sg.Push(), sg.Text(tr.gui_br[lang][0], key='-brModeText-'), sg.Push()],
        [sg.Radio(tr.gui_br[lang][1], 'brRadio', enable_events=True, default=False, key='-brMode0-')],
        [sg.Radio(tr.gui_br[lang][2], 'brRadio', enable_events=True, default=True, key='-brMode1-')],
        [sg.Radio(tr.gui_br[lang][3], 'brRadio', enable_events=True, default=False, key='-brMode2-')],
        [sg.T('')],
        [sg.Push(), sg.Text(tr.gui_formatting[lang], key='-formattingText-'), sg.Push()],
        [
            sg.Text(tr.gui_bit[lang], key='-bitnessText-'),
            sg.InputText(bitness, size=1, disabled_readonly_background_color=inputOFF_color, expand_x=True, enable_events=True, key='-bitness-')
        ],
        [
            sg.Text(tr.gui_rnd[lang], key='-roundingText-'),
            sg.InputText(rounding, size=1, disabled_readonly_background_color=inputOFF_color, expand_x=True, enable_events=True, key='-rounding-')
        ]
    ])

    T1_col1 = [
        [sg.Push(), sg.Text(tr.gui_database[lang], font=title_font, key='T1_title1'), sg.Push()],
        [sg.Push(), sg.Button(button_text=tr.gui_load[lang], size=button_size, key='T1_database', metadata=False), sg.Push()],
        [
            sg.Push(), sg.Text(tr.gui_tags[lang], key='T1_tagsN', visible=False),
            sg.InputCombo([], default_value='', size=tags_input_size, enable_events=True, key='T1_tags', visible=False)
        ],
        [sg.Listbox(values=(), enable_events=True, key='T1_list', visible=False, expand_x=True, expand_y=True)]
    ]
    T1_col2 = [
        [sg.Push(), sg.Text(tr.gui_results[lang], font=title_font, key='T1_title2'), sg.Push()],
        [sg.Push(), sg.Graph(canvas_size=canvas_size, graph_bottom_left=(0, 0), graph_top_right=canvas_size, background_color=None, key='T1_graph'), sg.Push()],
        [sg.Push(), sg.T('', key='T1_estimated'), sg.Push()],
        [sg.Text(tr.gui_rgb[lang], key='T1_colorRGB'), sg.Input(size=1, key='T1_rgb', expand_x=True)],
        [sg.Text(tr.gui_hex[lang], key='T1_colorHEX'), sg.Input(size=1, key='T1_hex', expand_x=True)],
        [
            sg.Input(size=1, key='T1_convolved', expand_x=True),
            sg.Text(tr.gui_in_filter[lang], key='T1_in_filter'),
            sg.InputCombo(filtersDB, 'Generic_Bessell.V', enable_events=True, key='T1_filter')
        ],
        [sg.T('')],
        [sg.Push(), sg.Button(button_text=tr.gui_add[lang], size=button_size, key='T1_add'), sg.Push()],
        [sg.Push(), sg.Button(button_text=tr.gui_plot[lang], size=button_size, key='T1_plot'), sg.Push()],
        [sg.Push(), sg.Button(button_text=tr.gui_clear[lang], size=button_size, key='T1_clear'), sg.Push()],
        [sg.T('')],
        [sg.Push(), sg.Button(button_text=tr.gui_export2text[lang], size=button_size, key='T1_export2text'), sg.Push()],
        [
            sg.Push(), sg.Input(enable_events=True, key='T1_folder', visible=False),
            sg.FolderBrowse(button_text=tr.gui_export2table[lang], size=button_size, key='T1_export2table'), sg.Push()
        ]
    ]

    def frame(num: int, filtersDB: tuple, lang: str):
        n = str(num)
        try:
            rgb_text = sg.Text(tr.gui_RGBcolors[lang][num], key='T2_rgbText'+n)
        except IndexError:
            rgb_text = sg.Text('', key='T2_rgbText'+n)
        l = [
            [
                sg.Input(enable_events=True, size=1, key='T2_path'+n, expand_x=True, visible=False),
                # size=1 is VERY important! Now column depends on max length of filter file names
                sg.FileBrowse(button_text=tr.gui_browse[lang], size=10, key='T2_pathText'+n, visible=False),
                # or label of RGB image bands, depends on radio box
                rgb_text
            ],
            [
                sg.Text(tr.gui_filter[lang], key='T2_filterText'+n),
                sg.InputCombo(('', *filtersDB), enable_events=True, expand_x=True, key='T2_filter'+n)
            ],
            [
                sg.Text(tr.gui_factor[lang], key='T2_factorText'+n),
                sg.Input('1', size=1, key='T2_factor'+n, expand_x=True)
            ]
        ]
        return sg.Frame(f'{tr.gui_band[lang]} {num+1}', l, key='T2_band'+n)
    
    T2_frames = [[frame(i, filtersDB, lang)] for i in range(T2_num)]
    T2_col1 = [
        [sg.Push(), sg.Text(tr.gui_input[lang], font=title_font, key='T2_title1'), sg.Push()],
        [sg.Text(tr.gui_step1[lang], key='T2_step1')],
        [sg.Radio(tr.gui_datatype[lang][0], 'DataTypeRadio', enable_events=True, key='-typeImage-', default=True)],
        [sg.Radio(tr.gui_datatype[lang][1], 'DataTypeRadio', enable_events=True, key='-typeImageRGB-')],
        [sg.Radio(tr.gui_datatype[lang][2], 'DataTypeRadio', enable_events=True, key='-typeImageCube-')],
        [
            sg.Text(tr.gui_step2[lang], key='T2_step2'),
            # or image input
            sg.Input(enable_events=True, size=1, key='T2_path', expand_x=True, visible=False),
            sg.FileBrowse(button_text=tr.gui_browse[lang], size=10, key='T2_pathText', visible=False),
        ],
        [sg.Column(T2_frames, scrollable=True, vertical_scroll_only=True, key='T2_frames', expand_x=True, expand_y=True)]
    ]
    T2_col2_1 = [
        [sg.Checkbox(tr.gui_desun[lang], key='T2_desun')],
        [sg.Checkbox(tr.gui_photons[lang], key='T2_photons')],
        #[sg.Checkbox(tr.gui_autoalign[lang], key='T2_autoalign')],
    ]
    T2_col2_2 = [
        [sg.Checkbox(tr.gui_makebright[lang], key='T2_makebright')],
        [sg.Text(tr.gui_factor[lang], key='T2_factorText'), sg.Input('1', size=1, key='T2_factor', expand_x=True)],
        [sg.Checkbox(tr.gui_enlarge[lang], True, key='T2_enlarge')],
    ]
    T2_col2 = [
        [sg.Push(), sg.Text(tr.gui_results[lang], font=title_font, key='T2_title2'), sg.Push()],
        [sg.Canvas(key='T2_canvas')],
        [
            sg.Column(T2_col2_1, expand_x=True, expand_y=False), sg.VSeperator(),
            sg.Column(T2_col2_2, expand_x=True, expand_y=False)
        ],
        [sg.T('')],
        [sg.Push(), sg.Image(background_color='black', size=img_preview_size, key='T2_image'), sg.Push()],
        [sg.Push(), sg.Button(tr.gui_preview[lang], size=button_size, key='T2_preview'), sg.Push()],
        [sg.Push(), sg.Input(enable_events=True, key='T2_folder', visible=False), sg.FolderBrowse(tr.gui_process[lang], size=button_size, key='T2_process'), sg.Push()]
    ]

    T3_col1 = [
        [sg.Push(), sg.Text(tr.gui_input[lang], font=title_font, key='T3_title1'), sg.Push()],
        [sg.Push(), sg.Text('max ='), sg.InputText('20000', size=8, enable_events=True, key='T3_maxtemp_num'), sg.Text('K')],
        [
            sg.Text(tr.gui_temp[lang], justification='right', size=18, key='T3_temp'),
            sg.Slider(range=(0, 20000), default_value=0, resolution=100, orientation='h', size=slider_size, enable_events=True, key='T3_slider1', expand_x=True)
        ],
        [
            sg.Text(tr.gui_velocity[lang], justification='right', size=18, key='T3_velocity'),
            sg.Slider(range=(-1, 1), default_value=0, resolution=0.01, orientation='h', size=slider_size, enable_events=True, key='T3_slider2', expand_x=True)
        ],
        [
            sg.Text(tr.gui_vII[lang], size=18, justification='right', key='T3_vII'),
            sg.Slider(range=(0, 1), default_value=0, resolution=0.01, orientation='h', size=slider_size, enable_events=True, key='T3_slider3', expand_x=True)
        ],
        [sg.T('')],
        [sg.Checkbox(tr.gui_overexposure[lang], enable_events=True, default=False, key='T3_overexposure')],
        [
            sg.Text(tr.gui_mag[lang], size=18, text_color=text_colors[0], justification='right', key='T3_mag'),
            sg.Slider(range=(-50, 0), default_value=-26.7, resolution=0.1, orientation='h', size=slider_size, enable_events=True, disabled=True, key='T3_slider4', expand_x=True)
        ],
        [sg.Text(tr.gui_explanation[lang], key='T3_explanation')]
    ]
    T3_col2 = [
        [sg.Push(), sg.Text(tr.gui_results[lang], font=title_font, key='T3_title2'), sg.Push()],
        [sg.Push(), sg.Graph(canvas_size=canvas_size, graph_bottom_left=(0, 0), graph_top_right=canvas_size, background_color=None, key='T3_graph'), sg.Push()],
        [sg.T('')],
        [sg.Text(tr.gui_rgb[lang], key='T3_colorRGB'), sg.Input(size=1, key='T3_rgb', expand_x=True)],
        [sg.Text(tr.gui_hex[lang], key='T3_colorHEX'), sg.Input(size=1, key='T3_hex', expand_x=True)],
        [sg.T('')],
        [sg.Push(), sg.Button(button_text=tr.gui_add[lang], size=button_size, key='T3_add'), sg.Push()],
        [sg.Push(), sg.Button(button_text=tr.gui_plot[lang], size=button_size, key='T3_plot'), sg.Push()],
        [sg.Push(), sg.Button(button_text=tr.gui_clear[lang], size=button_size, key='T3_clear'), sg.Push()]
    ]


    tab1 = [
        [
            sg.Column(T1_col1, expand_x=True, expand_y=True), sg.VSeperator(),
            sg.Column(T1_col2, expand_x=True, expand_y=True)
        ]
    ]
    tab2 = [
        [
            sg.Column(T2_col1, expand_x=True, expand_y=True), sg.VSeperator(),
            sg.Column(T2_col2, expand_x=True, expand_y=True)
        ]
    ]
    tab3 = [
        [
            sg.Column(T3_col1, expand_x=True, expand_y=True), sg.VSeperator(),
            sg.Column(T3_col2, expand_x=True, expand_y=True)
        ]
    ]
    tabs = sg.TabGroup([[
            sg.Tab(tr.gui_tabs[lang][0], tab1, key='tab1'),
            sg.Tab(tr.gui_tabs[lang][1], tab2, key='tab2'),
            sg.Tab(tr.gui_tabs[lang][2], tab3, key='tab3')
    ]], expand_x=True, expand_y=True, enable_events=True, key='-currentTab-')
    return [
        [sg.Menu(tr.gui_menu[lang], key='menu')],
        [sg.vtop(settings_column), tabs]
    ]


def translate(window: sg.Window, T2_vis: int, lang: str):
    window['menu'].update(tr.gui_menu[lang])
    window['tab1'].update(title=tr.gui_tabs[lang][0])
    window['tab2'].update(title=tr.gui_tabs[lang][1])
    window['tab3'].update(title=tr.gui_tabs[lang][2])
    window['T1_title1'].update(tr.gui_database[lang])
    window['-settingsTitle-'].update(tr.gui_settings[lang])
    window['T1_title2'].update(tr.gui_results[lang])
    window['T1_database'].update(tr.gui_update[lang] if window['T1_database'].metadata else tr.gui_load[lang])
    window['T1_tagsN'].update(tr.gui_tags[lang])
    window['-gamma-'].update(text=tr.gui_gamma[lang])
    window['-brModeText-'].update(tr.gui_br[lang][0])
    window['-brMode0-'].update(text=tr.gui_br[lang][1])
    window['-brMode1-'].update(text=tr.gui_br[lang][2])
    window['-brMode2-'].update(text=tr.gui_br[lang][3])
    window['-formattingText-'].update(tr.gui_formatting[lang])
    window['-bitnessText-'].update(tr.gui_bit[lang])
    window['-roundingText-'].update(tr.gui_rnd[lang])
    if window['T1_estimated'].get() != '':
        window['T1_estimated'].update(tr.gui_estimated[lang])
    window['T1_colorRGB'].update(tr.gui_rgb[lang])
    window['T1_colorHEX'].update(tr.gui_hex[lang])
    window['T1_in_filter'].update(tr.gui_in_filter[lang])
    window['T1_add'].update(tr.gui_add[lang])
    window['T1_plot'].update(tr.gui_plot[lang])
    window['T1_clear'].update(tr.gui_clear[lang])
    window['T1_export2text'].update(tr.gui_export2text[lang])
    window['T1_export2table'].update(tr.gui_export2table[lang])
    window['T2_title1'].update(tr.gui_input[lang])
    window['T2_title2'].update(tr.gui_results[lang])
    window['T2_step1'].update(tr.gui_step1[lang])
    window['-typeImage-'].update(text=tr.gui_datatype[lang][0])
    window['-typeImageRGB-'].update(text=tr.gui_datatype[lang][1])
    window['-typeImageCube-'].update(text=tr.gui_datatype[lang][2])
    window['T2_rgbText0'].update(tr.gui_RGBcolors[lang][0])
    window['T2_rgbText1'].update(tr.gui_RGBcolors[lang][1])
    window['T2_rgbText2'].update(tr.gui_RGBcolors[lang][2])
    window['T2_step2'].update(tr.gui_step2[lang])
    window['T2_pathText'].update(tr.gui_browse[lang])
    for i in range(T2_vis):
        window['T2_band'+str(i)].update(f'{tr.gui_band[lang]} {i+1}')
        window['T2_filterText'+str(i)].update(tr.gui_filter[lang])
        window['T2_pathText'+str(i)].update(tr.gui_browse[lang])
        window['T2_factorText'+str(i)].update(tr.gui_factor[lang])
    window['T2_desun'].update(text=tr.gui_desun[lang])
    window['T2_photons'].update(text=tr.gui_photons[lang])
    #window['T2_autoalign'].update(text=tr.gui_autoalign[lang])
    #window['T2_plotpixels'].update(text=tr.gui_plotpixels[lang])
    window['T2_makebright'].update(text=tr.gui_makebright[lang])
    window['T2_factorText'].update(tr.gui_factor[lang])
    window['T2_enlarge'].update(text=tr.gui_enlarge[lang])
    window['T2_preview'].update(tr.gui_preview[lang])
    window['T2_process'].update(tr.gui_process[lang])
    window['T3_title1'].update(tr.gui_input[lang])
    window['T3_title2'].update(tr.gui_results[lang])
    window['T3_temp'].update(tr.gui_temp[lang])
    window['T3_velocity'].update(tr.gui_velocity[lang])
    window['T3_vII'].update(tr.gui_vII[lang])
    window['T3_mag'].update(tr.gui_mag[lang])
    window['T3_overexposure'].update(text=tr.gui_overexposure[lang])
    window['T3_explanation'].update(tr.gui_explanation[lang])
    window['T3_colorRGB'].update(tr.gui_rgb[lang])
    window['T3_colorHEX'].update(tr.gui_hex[lang])
    window['T3_add'].update(tr.gui_add[lang])
    window['T3_plot'].update(tr.gui_plot[lang])
    window['T3_clear'].update(tr.gui_clear[lang])
    return window

icon = b'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'