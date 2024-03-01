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
        [sg.Text(tr.gui_factor[lang], key='T2_factorText'), sg.Input('1', size=1, key='T2_factor', expand_x=True)]
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