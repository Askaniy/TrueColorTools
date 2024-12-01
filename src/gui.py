""" Responsible for the creation and translation of the graphical interface. """

from typing import Callable
from time import strftime
import FreeSimpleGUI as sg

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

# FreeSimpleGUI custom theme
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

def generate_plot_layout(lang: str, light_theme: bool):
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
        [sg.Canvas(key='W1_canvas')],
    ]

def generate_menu_bar(lang: str):
    """ Window 0 menu bar generator """
    return [
        [tr.gui_menu[lang], [tr.gui_ref[lang], tr.gui_info[lang], tr.gui_exit[lang]]],
        [tr.gui_language[lang], tuple(tr.langs.keys())],
    ]

def generate_layout(
        canvas_size: tuple,
        img_preview_size: tuple,
        text_colors: tuple,
        filtersDB: tuple,
        srgb: bool,
        brMax: bool,
        brGeom: bool,
        bitness: int,
        rounding: int,
        T2_num: int,
        lang: str):
    """ Window 0 layout generator, the main window with tabs """
    title_font = ('arial', 12)
    tags_input_size = 20
    button_size = 30
    browse_size = 10
    slider_size = (1, 15)

    settings_column = sg.Column([
        [sg.T()],
        [sg.Push(), sg.Text(tr.gui_settings[lang], font=title_font, key='-settingsTitle-'), sg.Push()],
        [sg.T()],
        [sg.Checkbox(tr.gui_gamma[lang], enable_events=True, default=True, key='-gamma-', tooltip=tr.gui_gamma_note[lang])],
        [sg.Checkbox('sRGB', enable_events=True, default=srgb, key='-srgb-', tooltip=tr.gui_srgb_note[lang])],
        [sg.T()],
        [sg.Text(tr.gui_brMode[lang], key='-brModeText-')],
        [sg.Checkbox(tr.gui_brMax[lang], enable_events=True, default=brMax, key='-brMax-')],
        [sg.Radio(tr.gui_geom[lang], 'brRadio', enable_events=True, default=brGeom, key='-brMode1-', tooltip=tr.gui_geom_note[lang])],
        [sg.Radio(tr.gui_sphe[lang], 'brRadio', enable_events=True, default=not brGeom, key='-brMode2-', tooltip=tr.gui_sphe_note[lang])],
        [sg.T()],
        [sg.Text(tr.gui_formatting[lang], key='-formattingText-')],
        [
            sg.Text(tr.gui_bit[lang], key='-bitnessText-'),
            sg.InputText(bitness, size=1, disabled_readonly_background_color=inputOFF_color, expand_x=True, enable_events=True, key='-bitness-'),
        ],
        [
            sg.Text(tr.gui_rnd[lang], key='-roundingText-'),
            sg.InputText(rounding, size=1, disabled_readonly_background_color=inputOFF_color, expand_x=True, enable_events=True, key='-rounding-'),
        ],
    ])

    T1_col1 = [
        #[sg.Push(), sg.Text(tr.gui_database[lang], font=title_font, key='T1_title1'), sg.Push()],
        [sg.Push(),sg.Text(key='T1_header_space'), sg.Push()], # Push() is a workaround to make visible=False action work
        [sg.Push(), sg.Button(button_text=tr.gui_load[lang], size=button_size, key='T1_load'), sg.Push()],
        [
            sg.Push(), sg.Text(tr.gui_tags[lang], key='T1_tagsN', visible=False),
            sg.InputCombo([], default_value='', size=tags_input_size, enable_events=True, key='T1_tags', visible=False),
        ],
        [sg.Listbox(values=(), enable_events=True, key='T1_list', visible=False, expand_x=True, expand_y=True)],
        [sg.Button(button_text=tr.gui_reload[lang], size=button_size, key='T1_reload', visible=False)],
    ]
    T1_col2 = [
        [sg.Text(font=title_font, key='T1_title2')],
        [sg.Graph(canvas_size=canvas_size, graph_bottom_left=(0, 0), graph_top_right=canvas_size, background_color=None, key='T1_graph')],
        [sg.T(key='T1_albedo_note')],
        [sg.Text(tr.gui_rgb[lang], key='T1_colorRGB'), sg.Input(size=1, key='T1_rgb', expand_x=True)],
        [sg.Text(tr.gui_hex[lang], key='T1_colorHEX'), sg.Input(size=1, key='T1_hex', expand_x=True)],
        [
            sg.Input(size=1, key='T1_convolved', expand_x=True),
            sg.Text(tr.gui_in_filter[lang], key='T1_in_filter'),
            sg.InputCombo(filtersDB, 'Generic_Bessell.V', enable_events=True, key='T1_filter')
        ],
        [sg.T()],
        [sg.Button(button_text=tr.gui_plot[lang], size=button_size, key='T1_plot')],
        [sg.Button(button_text=tr.gui_pin[lang], size=button_size, key='T1_pin')],
        [sg.Button(button_text=tr.gui_clear[lang], size=button_size, key='T1_clear')],
        [sg.T()],
        [sg.Button(button_text=tr.gui_export2text[lang], size=button_size, key='T1_export2text')],
        [
            sg.Input(enable_events=True, key='T1_folder', visible=False),
            sg.FolderBrowse(
                button_text=tr.gui_export2table[lang], size=button_size,
                initial_folder='..', key='T1_export2table'
            ),
        ],
    ]

    def frame(num: int, filtersDB: tuple, lang: str):
        n = str(num)
        try:
            rgb_text = sg.Text(tr.gui_RGBcolors[lang][num], key='T2_rgbText'+n)
        except IndexError:
            rgb_text = sg.Text(key='T2_rgbText'+n)
        l = [
            [
                sg.Input(enable_events=True, size=1, key='T2_path'+n, expand_x=True, visible=False),
                # size=1 is VERY important to make column be depended on the max length of filter file names
                # Depending on the radio box, FileBrowse or label is displayed below
                sg.FileBrowse(button_text=tr.gui_browse[lang], size=browse_size, key='T2_pathText'+n, visible=False),
                # No need of initial_folder='..' in the FileBrowse to make the path dynamical between the frames
                rgb_text,
            ],
            [
                sg.Text(tr.gui_filter[lang], key='T2_filterText'+n),
                sg.InputCombo(('', *filtersDB), enable_events=True, expand_x=True, key='T2_filter'+n)
            ],
            [
                sg.Text(tr.gui_evaluate[lang], key='T2_evalText'+n, tooltip=tr.gui_evaluate_note[lang]),
                sg.Input('x', size=1, key='T2_eval'+n, expand_x=True)
            ],
        ]
        return sg.Frame(f'{tr.gui_band[lang]} {num+1}', l, key='T2_band'+n)
    
    T2_frames = [[frame(i, filtersDB, lang)] for i in range(T2_num)]
    T2_col1 = [
        #[sg.Push(), sg.Text(tr.gui_input[lang], font=title_font, key='T2_title1'), sg.Push()],
        [sg.Text(tr.gui_step1[lang], key='T2_step1')],
        [sg.Radio(tr.gui_datatype[lang][0], 'DataTypeRadio', enable_events=True, key='-typeImage-', default=True)],
        [sg.Radio(tr.gui_datatype[lang][1], 'DataTypeRadio', enable_events=True, key='-typeImageRGB-')],
        [sg.Radio(tr.gui_datatype[lang][2], 'DataTypeRadio', enable_events=True, key='-typeImageCube-')],
        [
            sg.Text(tr.gui_step2[lang], key='T2_step2'),
            # or image input
            sg.Input(enable_events=True, size=1, key='T2_path', expand_x=True, visible=False),
            sg.FileBrowse(
                button_text=tr.gui_browse[lang], size=browse_size,
                initial_folder='..', key='T2_pathText', visible=False
            ),
        ],
        [sg.Column(T2_frames, scrollable=True, vertical_scroll_only=True, key='T2_frames', expand_x=True, expand_y=True)],
    ]
    T2_col2_1 = [
        [sg.Checkbox(tr.gui_desun[lang], key='T2_desun', tooltip=tr.gui_desun_note[lang])],
        [sg.Checkbox(tr.gui_photons[lang], key='T2_photons', tooltip=tr.gui_photons_note[lang])],
        #[sg.Checkbox(tr.gui_autoalign[lang], key='T2_autoalign')],
    ]
    T2_col2_2 = [
        [sg.Text(tr.gui_factor[lang], key='T2_factorText', tooltip=tr.gui_factor_note[lang]), sg.Input('1', size=1, key='T2_factor', expand_x=True)],
        [sg.Checkbox(tr.gui_upscale[lang], default=False, key='T2_upscale', tooltip=tr.gui_upscale_note[lang])],
    ]
    T2_col2 = [
        #[sg.Push(), sg.Text(tr.gui_output[lang], font=title_font, key='T2_title2'), sg.Push()],
        [sg.Canvas(key='T2_canvas')],
        [
            sg.Column(T2_col2_1, expand_x=True, expand_y=False), sg.VSeperator(),
            sg.Column(T2_col2_2, expand_x=True, expand_y=False)
        ],
        [
            sg.Text(tr.gui_chunks[lang], key='T2_chunksText', tooltip=tr.gui_chunks_note[lang]),
            sg.Input('1', size=1, key='T2_chunks', expand_x=True),
        ],
        [sg.T()],
        [sg.Push(), sg.Image(background_color='black', size=img_preview_size, key='T2_image'), sg.Push()],
        [sg.Push(), sg.Button(tr.gui_preview[lang], size=button_size, key='T2_preview'), sg.Push()],
        [
            sg.Push(),
            sg.Input(enable_events=True, key='T2_folder', visible=False),
            sg.FolderBrowse(
                button_text=tr.gui_process[lang], size=button_size,
                initial_folder='..', key='T2_process'
            ),
            sg.Push(),
        ],
    ]

    T3_col1 = [
        #[sg.Push(), sg.Text(tr.gui_input[lang], font=title_font, key='T3_title1'), sg.Push()],
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
        [sg.T()],
        [
            sg.Text(tr.gui_mag[lang], size=18, text_color=text_colors[0], justification='right', key='T3_mag'),
            sg.Slider(range=(-50, 0), default_value=-26.7, resolution=0.1, orientation='h', size=slider_size, enable_events=True, disabled=True, key='T3_slider4', expand_x=True)
        ],
        [sg.Text(tr.gui_mag_note[lang], key='T3_mag_note')],
    ]
    T3_col2 = [
        [sg.Text(font=title_font, key='T3_title2')],
        [sg.Graph(canvas_size=canvas_size, graph_bottom_left=(0, 0), graph_top_right=canvas_size, background_color=None, key='T3_graph')],
        [sg.T()],
        [sg.Text(tr.gui_rgb[lang], key='T3_colorRGB'), sg.Input(size=1, key='T3_rgb', expand_x=True)],
        [sg.Text(tr.gui_hex[lang], key='T3_colorHEX'), sg.Input(size=1, key='T3_hex', expand_x=True)],
        [sg.T()],
        [sg.Button(button_text=tr.gui_plot[lang], size=button_size, key='T3_plot')],
        [sg.Button(button_text=tr.gui_pin[lang], size=button_size, key='T3_pin')],
        [sg.Button(button_text=tr.gui_clear[lang], size=button_size, key='T3_clear')],
    ]


    tab1 = [
        [
            sg.Column(T1_col1, expand_x=True, expand_y=True, element_justification='center'),
            sg.VSeperator(),
            sg.Column(T1_col2, expand_x=True, expand_y=True, element_justification='center'),
        ]
    ]
    tab2 = [
        [
            sg.Column(T2_col1, expand_x=True, expand_y=True),
            sg.VSeperator(),
            sg.Column(T2_col2, expand_x=True, expand_y=True),
        ]
    ]
    tab3 = [
        [
            sg.Column(T3_col1, expand_x=True, expand_y=True),
            sg.VSeperator(),
            sg.Column(T3_col2, expand_x=True, expand_y=True, element_justification='center'),
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


def translate_win0(window: sg.Window, T2_vis: int, lang: str):
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
    #window['T1_title1'].update(tr.gui_database[lang])
    #window['T1_title2'].update(tr.gui_output[lang])
    window['T1_load'].update(tr.gui_load[lang])
    window['T1_reload'].update(tr.gui_reload[lang])
    window['T1_tagsN'].update(tr.gui_tags[lang])
    if window['T1_albedo_note'].get() != '':
        window['T1_albedo_note'].update(tr.gui_estimated[lang])
    window['T1_colorRGB'].update(tr.gui_rgb[lang])
    window['T1_colorHEX'].update(tr.gui_hex[lang])
    window['T1_in_filter'].update(tr.gui_in_filter[lang])
    window['T1_plot'].update(tr.gui_plot[lang])
    window['T1_pin'].update(tr.gui_pin[lang])
    window['T1_clear'].update(tr.gui_clear[lang])
    window['T1_export2text'].update(tr.gui_export2text[lang])
    window['T1_export2table'].update(tr.gui_export2table[lang])
    #window['T2_title1'].update(tr.gui_input[lang])
    #window['T2_title2'].update(tr.gui_output[lang])
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
        window['T2_evalText'+str(i)].update(tr.gui_evaluate[lang])
    window['T2_desun'].update(text=tr.gui_desun[lang])
    window['T2_photons'].update(text=tr.gui_photons[lang]) #, tooltip=tr.gui_photons_note[lang]) # doesn't work
    #window['T2_autoalign'].update(text=tr.gui_autoalign[lang])
    #window['T2_plotpixels'].update(text=tr.gui_plotpixels[lang])
    window['T2_factorText'].update(tr.gui_factor[lang])
    window['T2_upscale'].update(text=tr.gui_upscale[lang])
    window['T2_chunksText'].update(tr.gui_chunks[lang])
    window['T2_preview'].update(tr.gui_preview[lang])
    window['T2_process'].update(tr.gui_process[lang])
    #window['T3_title1'].update(tr.gui_input[lang])
    #window['T3_title2'].update(tr.gui_output[lang])
    window['T3_temp'].update(tr.gui_temp[lang])
    window['T3_velocity'].update(tr.gui_velocity[lang])
    window['T3_vII'].update(tr.gui_vII[lang])
    window['T3_mag'].update(tr.gui_mag[lang])
    window['T3_mag_note'].update(tr.gui_mag_note[lang])
    window['T3_colorRGB'].update(tr.gui_rgb[lang])
    window['T3_colorHEX'].update(tr.gui_hex[lang])
    window['T3_plot'].update(tr.gui_plot[lang])
    window['T3_pin'].update(tr.gui_pin[lang])
    window['T3_clear'].update(tr.gui_clear[lang])
    return window

def translate_win1(window: sg.Window, lang: str):
    window['W1_title'].update(tr.spectral_plot[lang])
    window['W1_light_theme'].update(text=tr.light_theme[lang])
    window['W1_save'].update(tr.gui_save[lang])
    return window
