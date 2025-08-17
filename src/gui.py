""" Responsible for the creation and translation of the graphical interface. """

from typing import Callable
from time import strftime
import platform
import FreeSimpleGUI as sg

import src.strings as tr
from src.core import supported_color_spaces, supported_white_points


# TCT style colors
main_color = '#3884A9' # HSV 199.65° 66.86% 66.27%
#main_color = '#5D9BBA' # HSV 200.00° 50.00% 72.94% (0.5^1/2.2 = 72.974%)
text_color = '#FFFFFF'
muted_color = '#A3A3A3'
highlight_color = '#5A5A5A'
bg_color = '#333333'
inputON_color = '#424242'
inputOFF_color = '#3A3A3A'

# FreeSimpleGUI custom theme
sg.LOOK_AND_FEEL_TABLE['MaterialDark'] = {
    'BACKGROUND': bg_color, 'TEXT': text_color,
    'INPUT': inputON_color, 'TEXT_INPUT': text_color, 'SCROLL': inputON_color,
    'BUTTON': (text_color, main_color), 'PROGRESS': ('#000000', '#000000'),
    'BORDER': 0, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0
}

if platform.system() == 'Windows':
    # to display subscript numbers correctly
    sg.set_options(font=('Segoe UI', 10))


def create_logger(window: sg.Window, key: str) -> Callable:
    """ Creates a function that sends messages to the window main thread """
    def logger(message: str, data=None):
        window.write_event_value((key, f'{strftime("%H:%M:%S")} {message}'), data)
    return logger

def generate_plot_layout(lang: str, plot_size: tuple, light_theme: bool):
    """ Window 1 layout generator, the window of plot """
    return [
        [
            sg.Text(tr.spectral_plot[lang], font=('arial', 16), key='W1_title'),
            sg.Push(),
            sg.Checkbox(tr.light_theme[lang], default=light_theme, enable_events=True, key='W1_light_theme'),
            sg.Push(),
            sg.InputText(visible=False, enable_events=True, key='W1_path'),
            sg.FileSaveAs(
                tr.gui_save[lang], initial_folder='..',
                file_types=('PNG {png}', 'PDF {pdf}', 'SVG {svg}'), default_extension='.png', key='W1_save'
            )
        ],
        [sg.Canvas(size=plot_size, key='W1_canvas')],
    ]

def generate_menu_bar(lang: str):
    """ Window 0 menu bar generator """
    return [
        [tr.gui_menu[lang], [tr.gui_ref[lang], tr.gui_info[lang], tr.gui_exit[lang]]],
        [tr.gui_language[lang], tuple(tr.langs.keys())],
    ]

def generate_layout(
        circle_size: tuple,
        filters_plot_size: tuple,
        img_preview_size: tuple,
        text_colors: tuple,
        filtersDB: tuple,
        color_space: str,
        white_point: str,
        gamma: bool,
        brMax: bool,
        brGeom: bool,
        bitness: int,
        rounding: int,
        tab2_num: int,
        lang: str):
    """ Window 0 layout generator, the main window with tabs """
    title_font = (sg.DEFAULT_FONT[0], 12)
    tags_input_size = 20
    button_size = 30
    browse_size = 10
    slider_size = (1, 15)

    settings_column = sg.Column([
        [sg.T()],
        [sg.Push(), sg.Text(tr.gui_settings[lang], font=title_font, key='-settingsTitle-'), sg.Push()],
        [sg.T()],
        [sg.Text('Color space', key='-ColorSpaceText-', tooltip=tr.gui_color_space_tooltip[lang])],
        [
            sg.Combo(
                tuple(supported_color_spaces.keys()), default_value=color_space, readonly=True,
                expand_x=True, enable_events=True, key='-ColorSpace-', tooltip=tr.gui_color_space_tooltip[lang]
            )
        ],
        [sg.Text('White point', key='-WhitePointText-', tooltip=tr.gui_white_point_tooltip[lang])],
        [
            sg.Combo(
                tuple(supported_white_points.keys()), default_value=white_point, readonly=True,
                expand_x=True, enable_events=True, key='-WhitePoint-', tooltip=tr.gui_white_point_tooltip[lang]
            )
        ],
        [sg.T()],
        [sg.Checkbox(tr.gui_gamma[lang], default=gamma, enable_events=True, key='-gamma-', tooltip=tr.gui_gamma_tooltip[lang])],
        [sg.T()],
        [sg.Text(tr.gui_brMode[lang], key='-brModeText-')],
        [sg.Checkbox(tr.gui_brMax[lang], enable_events=True, default=brMax, key='-brMax-')],
        [sg.Radio(tr.gui_geom[lang], 'brRadio', enable_events=True, default=brGeom, key='-brMode1-', tooltip=tr.gui_geom_tooltip[lang])],
        [sg.Radio(tr.gui_sphe[lang], 'brRadio', enable_events=True, default=not brGeom, key='-brMode2-', tooltip=tr.gui_sphe_tooltip[lang])],
        [sg.T()],
        [sg.Text(tr.gui_formatting[lang], key='-formattingText-')],
        [
            sg.Text(tr.gui_bit[lang], key='-bitnessText-'),
            sg.InputText(
                str(bitness), size=1, disabled_readonly_background_color=inputOFF_color,
                expand_x=True, enable_events=True, key='-bitness-'
            ),
        ],
        [
            sg.Text(tr.gui_rnd[lang], key='-roundingText-'),
            sg.InputText(
                str(rounding), size=1, disabled_readonly_background_color=inputOFF_color,
                expand_x=True, enable_events=True, key='-rounding-'
            ),
        ],
    ])

    tab1_col1 = [
        #[sg.Push(), sg.Text(tr.gui_database[lang], font=title_font, key='tab1_title1'), sg.Push()],,
        [
            sg.Text(tr.gui_tag_filter[lang], key='tab1_tag_filterN'),
            sg.Combo([], default_value='', size=tags_input_size, readonly=True, expand_x=True, enable_events=True, key='tab1_tag_filter'),
        ],
        [
            sg.Text(tr.gui_search[lang], key='tab1_searchN'),
            sg.InputText('', size=1, disabled_readonly_background_color=inputOFF_color, expand_x=True, enable_events=True, key='tab1_searched'),
        ],
        [sg.Listbox(values=(), enable_events=True, key='tab1_list', expand_x=True, expand_y=True)],
        [sg.Button(button_text=tr.gui_load[lang], size=button_size, key='tab1_(re)load')],
    ]
    tab1_col2 = [
        [sg.Text(font=title_font, key='tab1_title2')],
        [sg.Graph(canvas_size=circle_size, graph_bottom_left=(0, 0), graph_top_right=circle_size, background_color=None, key='tab1_graph')],
        [sg.T(key='tab1_albedo_note')],
        [sg.Text(tr.gui_rgb[lang], key='tab1_colorRGB'), sg.Input(size=1, key='tab1_rgb', expand_x=True)],
        [sg.Text(tr.gui_hex[lang], key='tab1_colorHEX'), sg.Input(size=1, key='tab1_hex', expand_x=True)],
        [
            sg.Input(size=1, key='tab1_convolved', expand_x=True),
            sg.Text(tr.gui_in_filter[lang], key='tab1_in_filterN'),
            sg.InputCombo(filtersDB, 'Generic_Bessell.V', enable_events=True, key='tab1_in_filter')
        ],
        [sg.T()],
        [sg.Button(button_text=tr.gui_plot[lang], size=button_size, key='tab1_plot')],
        [sg.Button(button_text=tr.gui_pin[lang], size=button_size, key='tab1_pin')],
        [sg.Button(button_text=tr.gui_clear[lang], size=button_size, key='tab1_clear')],
        [sg.T()],
        [sg.Button(button_text=tr.gui_export2text[lang], size=button_size, key='tab1_export2text')],
        [
            sg.Input(enable_events=True, key='tab1_folder', visible=False),
            sg.FolderBrowse(
                button_text=tr.gui_export2table[lang], size=button_size,
                initial_folder='..', key='tab1_export2table'
            ),
        ],
    ]

    def frame(num: int, filtersDB: tuple, lang: str):
        n = str(num)
        try:
            rgb_text = sg.Text(tr.gui_RGBcolors[lang][num], key='tab2_rgbText'+n)
        except IndexError:
            rgb_text = sg.Text(key='tab2_rgbText'+n)
        l = [
            [
                sg.Input(enable_events=True, size=1, key='tab2_path'+n, expand_x=True, visible=False),
                # size=1 is VERY important to make column be depended on the max length of filter file names
                # Depending on the radio box, FileBrowse or label is displayed below
                sg.FileBrowse(button_text=tr.gui_browse[lang], size=browse_size, key='tab2_pathText'+n, visible=False),
                # No need of initial_folder='..' in the FileBrowse to make the path dynamical between the frames
                rgb_text,
            ],
            [
                sg.Text(tr.gui_tag_filter[lang], key='tab2_filterText'+n),
                sg.InputCombo(('', *filtersDB), enable_events=True, expand_x=True, key='tab2_filter'+n)
            ],
            [
                sg.Text(tr.gui_evaluate[lang], key='tab2_evalText'+n, tooltip=tr.gui_evaluate_tooltip[lang]),
                sg.Input('x', size=1, key='tab2_eval'+n, expand_x=True)
            ],
        ]
        return sg.Frame(f'{tr.gui_band[lang]} {num+1}', l, key='tab2_band'+n)

    tab2_frames = [[frame(i, filtersDB, lang)] for i in range(tab2_num)]
    tab2_col1 = [
        #[sg.Push(), sg.Text(tr.gui_input[lang], font=title_font, key='tab2_title1'), sg.Push()],
        [sg.Text(tr.gui_step1[lang], key='tab2_step1')],
        [sg.Radio(tr.gui_datatype[lang][0], 'DataTypeRadio', enable_events=True, key='-typeImage-', default=True)],
        [sg.Radio(tr.gui_datatype[lang][1], 'DataTypeRadio', enable_events=True, key='-typeImageRGB-')],
        [sg.Radio(tr.gui_datatype[lang][2], 'DataTypeRadio', enable_events=True, key='-typeImageCube-')],
        [
            sg.Text(tr.gui_step2[lang], key='tab2_step2'),
            # or image input
            sg.Input(enable_events=True, size=1, key='tab2_path', expand_x=True, visible=False),
            sg.FileBrowse(
                button_text=tr.gui_browse[lang], size=browse_size,
                initial_folder='..', key='tab2_pathText', visible=False
            ),
        ],
        [sg.Column(tab2_frames, scrollable=True, vertical_scroll_only=True, key='tab2_frames', expand_x=True, expand_y=True)],
    ]
    tab2_col2_1 = [
        [sg.Checkbox(tr.gui_desun[lang], key='tab2_desun', tooltip=tr.gui_desun_tooltip[lang])],
        [sg.Checkbox(tr.gui_photons[lang], key='tab2_photons', tooltip=tr.gui_photons_tooltip[lang])],
        #[sg.Checkbox(tr.gui_autoalign[lang], key='tab2_autoalign')],
    ]
    tab2_col2_2 = [
        [sg.Text(tr.gui_factor[lang], key='tab2_factorText', tooltip=tr.gui_factor_tooltip[lang]), sg.Input('1', size=1, key='tab2_factor', expand_x=True)],
        [sg.Checkbox(tr.gui_upscale[lang], default=False, key='tab2_upscale', tooltip=tr.gui_upscale_tooltip[lang])],
    ]
    tab2_col2 = [
        #[sg.Push(), sg.Text(tr.gui_output[lang], font=title_font, key='tab2_title2'), sg.Push()],
        [sg.Canvas(size=filters_plot_size, key='tab2_canvas')],
        [
            sg.Column(tab2_col2_1, expand_x=True, expand_y=False), sg.VSeperator(),
            sg.Column(tab2_col2_2, expand_x=True, expand_y=False)
        ],
        [
            sg.Text(tr.gui_chunks[lang], key='tab2_chunksText', tooltip=tr.gui_chunks_tooltip[lang]),
            sg.Input('1', size=1, key='tab2_chunks', expand_x=True),
        ],
        [sg.T()],
        [sg.Push(), sg.Image(background_color='black', size=img_preview_size, key='tab2_image'), sg.Push()],
        [sg.Push(), sg.Button(tr.gui_preview[lang], size=button_size, key='tab2_preview'), sg.Push()],
        [
            sg.Push(),
            sg.Input(enable_events=True, key='tab2_folder', visible=False),
            sg.FolderBrowse(
                button_text=tr.gui_process[lang], size=button_size,
                initial_folder='..', key='tab2_process'
            ),
            sg.Push(),
        ],
    ]

    tab3_col1 = [
        #[sg.Push(), sg.Text(tr.gui_input[lang], font=title_font, key='tab3_title1'), sg.Push()],
        [sg.Push(), sg.Text('max ='), sg.InputText('20000', size=8, enable_events=True, key='tab3_maxtemp_num'), sg.Text('K')],
        [
            sg.Text(tr.gui_temp[lang], justification='right', size=18, key='tab3_temp'),
            sg.Slider(range=(0, 20000), default_value=0, resolution=100, orientation='h', size=slider_size, enable_events=True, key='tab3_slider1', expand_x=True)
        ],
        [
            sg.Text(tr.gui_velocity[lang], justification='right', size=18, key='tab3_velocity'),
            sg.Slider(range=(-1, 1), default_value=0, resolution=0.01, orientation='h', size=slider_size, enable_events=True, key='tab3_slider2', expand_x=True)
        ],
        [
            sg.Text(tr.gui_vII[lang], size=18, justification='right', key='tab3_vII'),
            sg.Slider(range=(0, 1), default_value=0, resolution=0.01, orientation='h', size=slider_size, enable_events=True, key='tab3_slider3', expand_x=True)
        ],
        [sg.T()],
        [
            sg.Text(tr.gui_mag[lang], size=18, text_color=text_colors[not brMax], justification='right', key='tab3_mag'),
            sg.Slider(range=(-50, 0), default_value=-26.7, resolution=0.1, orientation='h', size=slider_size, enable_events=True, disabled=brMax, key='tab3_slider4', expand_x=True)
        ],
        [sg.Text(tr.gui_mag_note[lang], key='tab3_mag_note')],
    ]
    tab3_col2 = [
        [sg.Text(font=title_font, key='tab3_title2')],
        [sg.Graph(canvas_size=circle_size, graph_bottom_left=(0, 0), graph_top_right=circle_size, background_color=None, key='tab3_graph')],
        [sg.T()],
        [sg.Text(tr.gui_rgb[lang], key='tab3_colorRGB'), sg.Input(size=1, key='tab3_rgb', expand_x=True)],
        [sg.Text(tr.gui_hex[lang], key='tab3_colorHEX'), sg.Input(size=1, key='tab3_hex', expand_x=True)],
        [sg.T()],
        [sg.Button(button_text=tr.gui_plot[lang], size=button_size, key='tab3_plot')],
        [sg.Button(button_text=tr.gui_pin[lang], size=button_size, key='tab3_pin')],
        [sg.Button(button_text=tr.gui_clear[lang], size=button_size, key='tab3_clear')],
    ]


    tab1 = [
        [
            sg.Column(tab1_col1, expand_x=True, expand_y=True, element_justification='center'),
            sg.VSeperator(),
            sg.Column(tab1_col2, expand_x=True, expand_y=True, element_justification='center'),
        ]
    ]
    tab2 = [
        [
            sg.Column(tab2_col1, expand_x=True, expand_y=True),
            sg.VSeperator(),
            sg.Column(tab2_col2, expand_x=True, expand_y=True),
        ]
    ]
    tab3 = [
        [
            sg.Column(tab3_col1, expand_x=True, expand_y=True),
            sg.VSeperator(),
            sg.Column(tab3_col2, expand_x=True, expand_y=True, element_justification='center'),
        ]
    ]
    tabs = sg.TabGroup([[
            sg.Tab(tr.gui_tabs[lang][0], tab1, key='tab1'),
            sg.Tab(tr.gui_tabs[lang][1], tab2, key='tab2'),
            sg.Tab(tr.gui_tabs[lang][2], tab3, key='tab3')
    ]], expand_x=True, expand_y=True, enable_events=True, key='-currentTab-')
    return [
        [sg.Menu(generate_menu_bar(lang), key='menu')],
        [sg.vtop(settings_column), tabs]
    ]


def translate_win0(window: sg.Window, tab1_loaded: bool, tab1_albedo_note: dict, tab2_vis: int, lang: str):
    window['menu'].update(generate_menu_bar(lang))
    window['tab1'].update(title=tr.gui_tabs[lang][0])
    window['tab2'].update(title=tr.gui_tabs[lang][1])
    window['tab3'].update(title=tr.gui_tabs[lang][2])
    window['-settingsTitle-'].update(tr.gui_settings[lang])
    window['-gamma-'].update(text=tr.gui_gamma[lang])
    window['-brModeText-'].update(tr.gui_brMode[lang])
    window['-brMax-'].update(text=tr.gui_brMax[lang])
    window['-brMode1-'].update(text=tr.gui_geom[lang])
    window['-brMode2-'].update(text=tr.gui_sphe[lang])
    window['-formattingText-'].update(tr.gui_formatting[lang])
    window['-bitnessText-'].update(tr.gui_bit[lang])
    window['-roundingText-'].update(tr.gui_rnd[lang])
    #window['tab1_title1'].update(tr.gui_database[lang])
    #window['tab1_title2'].update(tr.gui_output[lang])
    window['tab1_tag_filterN'].update(tr.gui_tag_filter[lang])
    window['tab1_searchN'].update(tr.gui_search[lang])
    window['tab1_(re)load'].update(tr.gui_reload[lang] if tab1_loaded else tr.gui_load[lang])
    window['tab1_albedo_note'].update(tab1_albedo_note[lang])
    window['tab1_colorRGB'].update(tr.gui_rgb[lang])
    window['tab1_colorHEX'].update(tr.gui_hex[lang])
    window['tab1_in_filterN'].update(tr.gui_in_filter[lang])
    window['tab1_plot'].update(tr.gui_plot[lang])
    window['tab1_pin'].update(tr.gui_pin[lang])
    window['tab1_clear'].update(tr.gui_clear[lang])
    window['tab1_export2text'].update(tr.gui_export2text[lang])
    window['tab1_export2table'].update(tr.gui_export2table[lang])
    #window['tab2_title1'].update(tr.gui_input[lang])
    #window['tab2_title2'].update(tr.gui_output[lang])
    window['tab2_step1'].update(tr.gui_step1[lang])
    window['-typeImage-'].update(text=tr.gui_datatype[lang][0])
    window['-typeImageRGB-'].update(text=tr.gui_datatype[lang][1])
    window['-typeImageCube-'].update(text=tr.gui_datatype[lang][2])
    window['tab2_rgbText0'].update(tr.gui_RGBcolors[lang][0])
    window['tab2_rgbText1'].update(tr.gui_RGBcolors[lang][1])
    window['tab2_rgbText2'].update(tr.gui_RGBcolors[lang][2])
    window['tab2_step2'].update(tr.gui_step2[lang])
    window['tab2_pathText'].update(tr.gui_browse[lang])
    for i in range(tab2_vis):
        window['tab2_band'+str(i)].update(f'{tr.gui_band[lang]} {i+1}')
        window['tab2_filterText'+str(i)].update(tr.gui_filter_or_nm[lang])
        window['tab2_pathText'+str(i)].update(tr.gui_browse[lang])
        window['tab2_evalText'+str(i)].update(tr.gui_evaluate[lang])
    window['tab2_desun'].update(text=tr.gui_desun[lang])
    window['tab2_photons'].update(text=tr.gui_photons[lang]) #, tooltip=tr.gui_photons_tooltip[lang]) # doesn't work
    #window['tab2_autoalign'].update(text=tr.gui_autoalign[lang])
    #window['tab2_plotpixels'].update(text=tr.gui_plotpixels[lang])
    window['tab2_factorText'].update(tr.gui_factor[lang])
    window['tab2_upscale'].update(text=tr.gui_upscale[lang])
    window['tab2_chunksText'].update(tr.gui_chunks[lang])
    window['tab2_preview'].update(tr.gui_preview[lang])
    window['tab2_process'].update(tr.gui_process[lang])
    #window['tab3_title1'].update(tr.gui_input[lang])
    #window['tab3_title2'].update(tr.gui_output[lang])
    window['tab3_temp'].update(tr.gui_temp[lang])
    window['tab3_velocity'].update(tr.gui_velocity[lang])
    window['tab3_vII'].update(tr.gui_vII[lang])
    window['tab3_mag'].update(tr.gui_mag[lang])
    window['tab3_mag_note'].update(tr.gui_mag_note[lang])
    window['tab3_colorRGB'].update(tr.gui_rgb[lang])
    window['tab3_colorHEX'].update(tr.gui_hex[lang])
    window['tab3_plot'].update(tr.gui_plot[lang])
    window['tab3_pin'].update(tr.gui_pin[lang])
    window['tab3_clear'].update(tr.gui_clear[lang])
    return window

def translate_win1(window: sg.Window, lang: str):
    window['W1_title'].update(tr.spectral_plot[lang])
    window['W1_light_theme'].update(text=tr.light_theme[lang])
    window['W1_save'].update(tr.gui_save[lang])
    return window
