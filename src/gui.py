import PySimpleGUI as sg
import src.strings as tr
import src.filters as filters

# TCT style colors
main_color = '#108BB4'
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

def generate_layout(canvas_size: tuple, T2_preview: tuple, text_colors: tuple, filtersDB: list, lang: str):
    title_font = ('arial', 12)
    tags_input_size = 20
    button_size = 22
    browse_size = 10
    slider_size = (1, 15)

    settings_column = sg.Column([
        [sg.Push(), sg.Text(tr.gui_settings[lang], font=title_font, key='-settingsTitle-'), sg.Push()],
        [sg.T('')],
        [sg.Checkbox(tr.gui_gamma[lang], enable_events=True, default=True, key='-gamma-')],
        [sg.Checkbox('sRGB', enable_events=True, key='-srgb-')],
        [sg.T('')],
        [sg.Push(), sg.Text(tr.gui_br[lang][0], key='-brModeText-'), sg.Push()],
        [sg.Radio(tr.gui_br[lang][1], 'brRadio', enable_events=True, key='-brMode0-')],
        [sg.Radio(tr.gui_br[lang][2], 'brRadio', enable_events=True, default=True, key='-brMode1-')],
        #[sg.HorizontalSeparator()],
        #[sg.Text(tr.gui_phase[lang], key='-phaseText-')],
        #[sg.Slider(range=(-180, 180), default_value=0, resolution=1, orientation='h', size=(18, 16), enable_events=True, key='-phase-')],
        [sg.T('')],
        [sg.Push(), sg.Text(tr.gui_interp[lang][0], key='-interpModeText-'), sg.Push()],
        [sg.Radio(tr.gui_interp[lang][1], 'interpRadio', enable_events=True, default=True, key='-interpMode0-')],
        [sg.Radio(tr.gui_interp[lang][2], 'interpRadio', enable_events=True, key='-interpMode1-')],
        [sg.T('')],
        [sg.Push(), sg.Text(tr.gui_formatting[lang], key='-formattingText-'), sg.Push()],
        [
            sg.Text(tr.gui_bit[lang], key='-bitnessText-'),
            sg.InputText('1', size=1, disabled_readonly_background_color=inputOFF_color, expand_x=True, enable_events=True, key='-bitness-')
        ],
        [
            sg.Text(tr.gui_rnd[lang], key='-roundingText-'),
            sg.InputText('3', size=1, disabled_readonly_background_color=inputOFF_color, expand_x=True, enable_events=True, key='-rounding-')
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
        [sg.T('')],
        [sg.Text(tr.gui_rgb[lang], key='T1_colorRGB'), sg.Input(size=1, key='T1_rgb', expand_x=True)],
        [sg.Text(tr.gui_hex[lang], key='T1_colorHEX'), sg.Input(size=1, key='T1_hex', expand_x=True)],
        [sg.T('')],
        [sg.Push(), sg.Button(button_text=tr.gui_add[lang], size=button_size, key='T1_add'), sg.Push()],
        [sg.Push(), sg.Button(button_text=tr.gui_plot[lang], size=button_size, key='T1_plot'), sg.Push()],
        [sg.Push(), sg.Button(button_text=tr.gui_clear[lang], size=button_size, key='T1_clear'), sg.Push()],
        [sg.T('')],
        [sg.Push(), sg.Button(button_text=tr.gui_export[lang], size=button_size, key='T1_export'), sg.Push()]
    ]

    def frame(num: int, inputOFF_color: str, lang: str):
        n = str(num)
        l = [
            [         # sets frame width
                sg.Input(size=20, disabled=False, disabled_readonly_background_color=inputOFF_color, enable_events=True, key='T2_path'+n, expand_x=True),
                sg.FileBrowse(button_text=tr.gui_browse[lang], size=10, disabled=False, key='T2_browse'+n)
            ],
            [
                sg.Text(tr.gui_filter[lang], text_color=muted_color, key='T2_filterN'+n),
                sg.InputCombo([], disabled=True, enable_events=True, key='T2_filter'+n, expand_x=True)
            ],
            [
                sg.Text(tr.gui_wavelength[lang], key='T2_wavelengthN'+n),
                sg.Input(size=1, disabled_readonly_background_color=inputOFF_color, disabled=False, enable_events=True, key='T2_wavelength'+n, expand_x=True)
            ],
            [
                sg.Text(tr.gui_exposure[lang], key='T2_exposureN'+n),
                sg.Input('1.0', size=1, disabled_readonly_background_color=inputOFF_color, disabled=False, key='T2_exposure'+n, expand_x=True)
            ]
        ]
        return sg.Frame(f'{tr.gui_band[lang]} {num+1}', l, visible=True, key='T2_band'+n)

    T2_frames = [
        [frame(0, inputOFF_color, lang)],
        [frame(1, inputOFF_color, lang)],
        [frame(2, inputOFF_color, lang)],
        [frame(3, inputOFF_color, lang)],
        [frame(4, inputOFF_color, lang)],
        [frame(5, inputOFF_color, lang)],
        [frame(6, inputOFF_color, lang)],
        [frame(7, inputOFF_color, lang)],
        [frame(8, inputOFF_color, lang)],
        [frame(9, inputOFF_color, lang)] # just add more frames here
    ]
    T2_col1 = [
        [
            sg.Push(), sg.Text(tr.gui_input[lang], font=title_font, key='T2_title1'),
            sg.Button(button_text='+', key='T2_+'), sg.Button(button_text='−', key='T2_-'), sg.Push()
        ],
        [sg.Column(T2_frames, scrollable=True, vertical_scroll_only=True, key='T2_frames', expand_x=True, expand_y=True)]
    ]
    T2_col2 = [
        [sg.Push(), sg.Text(tr.gui_output[lang], font=title_font, key='T2_title2'), sg.Push()],
        [sg.Checkbox(tr.gui_makebright[lang], key='T2_makebright')],
        [sg.Checkbox(tr.gui_autoalign[lang], key='T2_autoalign')],
        [sg.Checkbox(tr.gui_desun[lang], key='T2_desun')],
        [sg.Checkbox(tr.gui_plotpixels[lang], enable_events=True, key='T2_plotpixels')],
        [
            sg.Checkbox(tr.gui_filterset[lang], enable_events=True, key='T2_filterset'),
            sg.InputCombo(filters.get_sets(), enable_events=True, disabled=True, key='T2_filter', expand_x=True)
        ],
        [
            sg.Checkbox(tr.gui_single[lang], enable_events=True, key='T2_single'),
            sg.Input(size=1, disabled=True, disabled_readonly_background_color=inputOFF_color, key='T2_path', expand_x=True),
            sg.FileBrowse(button_text=tr.gui_browse[lang], size=browse_size, disabled=True, key='T2_browse')
        ],
        [
            sg.Text(tr.gui_folder[lang], key='T2_folderN'),
            sg.Input(size=1, enable_events=True, key='T2_folder', expand_x=True),
            sg.FolderBrowse(button_text=tr.gui_browse[lang], size=browse_size, key='T2_browse_folder')
        ],
        [sg.T('')],
        [
            sg.Push(), sg.Button(tr.gui_preview[lang], size=button_size, disabled=True, key='T2_preview'),
            sg.Button(tr.gui_process[lang], size=button_size, disabled=True, key='T2_process'), sg.Push()
        ],
        [sg.Push(), sg.Image(background_color='black', size=T2_preview, key='T2_image'), sg.Push()]
    ]

    tab3 = [
        [
            sg.Text(tr.gui_folder[lang], key='T3_folderN'),
            sg.Input(size=1, enable_events=True, key='T3_folder', expand_x=True),
            sg.FolderBrowse(button_text=tr.gui_browse[lang], size=browse_size, key='T3_browse_folder')
        ],
        [
            sg.Push(),
            sg.Column([
                [sg.Push(), sg.Button(button_text=tr.gui_load[lang], size=button_size, key='T3_database', metadata=False), sg.Push()],
                [
                    sg.Push(), sg.Text(tr.gui_tags[lang], text_color=muted_color, key='T3_tagsN'),
                    sg.InputCombo([], default_value='', size=tags_input_size, enable_events=True, disabled=True, key='T3_tags'), sg.Push()
                ]
            ]),
            sg.Push(),
            sg.Column([
                [
                    sg.Push(), sg.Text(tr.gui_extension[lang], key='T3_ext'),
                    sg.InputCombo(['png', 'jpeg', 'pdf'], default_value='png', enable_events=True, key='T3_extension'), sg.Push()
                ],
                [sg.Push(), sg.Button(tr.gui_process[lang], size=button_size, disabled=True, key='T3_process'), sg.Push()]
            ]),
            sg.Push()
        ]
    ]

    T4_col1 = [
        [sg.Push(), sg.Text(tr.gui_input[lang], font=title_font, key='T4_title1'), sg.Push()],
        [sg.Push(), sg.Text('max ='), sg.InputText('20000', size=8, enable_events=True, key='T4_maxtemp_num'), sg.Text('K')],
        [
            sg.Text(tr.gui_temp[lang], justification='right', size=18, key='T4_temp'),
            sg.Slider(range=(0, 20000), default_value=0, resolution=100, orientation='h', size=slider_size, enable_events=True, key='T4_slider1', expand_x=True)
        ],
        [
            sg.Text(tr.gui_velocity[lang], justification='right', size=18, key='T4_velocity'),
            sg.Slider(range=(-1, 1), default_value=0, resolution=0.01, orientation='h', size=slider_size, enable_events=True, key='T4_slider2', expand_x=True)
        ],
        [
            sg.Text(tr.gui_vII[lang], size=18, justification='right', key='T4_vII'),
            sg.Slider(range=(0, 1), default_value=0, resolution=0.01, orientation='h', size=slider_size, enable_events=True, key='T4_slider3', expand_x=True)
        ],
        [sg.T('')],
        [sg.Checkbox(tr.gui_overexposure[lang], enable_events=True, default=False, key='T4_overexposure')],
        [
            sg.Text(tr.gui_mag[lang], size=18, text_color=text_colors[0], justification='right', key='T4_mag'),
            sg.Slider(range=(-100, 0), default_value=-26.7, resolution=0.1, orientation='h', size=slider_size, enable_events=True, disabled=True, key='T4_slider4', expand_x=True)
        ],
        [sg.Text(tr.gui_explanation[lang], key='T4_explanation')]
    ]
    T4_col2 = [
        [sg.Push(), sg.Text(tr.gui_results[lang], font=title_font, key='T4_title2'), sg.Push()],
        [sg.Push(), sg.Graph(canvas_size=canvas_size, graph_bottom_left=(0, 0), graph_top_right=canvas_size, background_color=None, key='T4_graph'), sg.Push()],
        [sg.T('')],
        [sg.Text(tr.gui_rgb[lang], key='T4_colorRGB'), sg.Input(size=1, key='T4_rgb', expand_x=True)],
        [sg.Text(tr.gui_hex[lang], key='T4_colorHEX'), sg.Input(size=1, key='T4_hex', expand_x=True)],
        [sg.T('')],
        [sg.Push(), sg.Button(button_text=tr.gui_add[lang], size=button_size, key='T4_add'), sg.Push()],
        [sg.Push(), sg.Button(button_text=tr.gui_plot[lang], size=button_size, key='T4_plot'), sg.Push()],
        [sg.Push(), sg.Button(button_text=tr.gui_clear[lang], size=button_size, key='T4_clear'), sg.Push()],
    ]

    def frame_new(num: int, filtersDB: list, lang: str):
        n = str(num)
        l = [
            [
                sg.Text(tr.gui_filter[lang], key='T5_filterText'+n),
                sg.InputCombo(filtersDB, enable_events=True, expand_x=True, key='T5_filter'+n)
            ],
            [   # Every moment displays brightness input
                sg.Text(tr.gui_brightness[lang], key='T5_brText'+n),
                sg.Input(size=1, enable_events=True, key='T5_br'+n, expand_x=True),
                # or image input, depends on radio box
                sg.Input(enable_events=True, size=1, key='T5_path'+n, expand_x=True, visible=False),
                sg.FileBrowse(button_text=tr.gui_browse[lang], size=10, key='T5_pathText'+n, visible=False)
            ]   # size=1 is VERY important! Now column depends on max length of filter file names
        ]
        return sg.Frame(f'{tr.gui_band[lang]} {num+1}', l, key='T5_band'+n)
    
    T5_frames = [
        [frame_new(0, filtersDB, lang)],
        [frame_new(1, filtersDB, lang)],
        [frame_new(2, filtersDB, lang)],
        [frame_new(3, filtersDB, lang)],
        [frame_new(4, filtersDB, lang)],
        [frame_new(5, filtersDB, lang)],
        [frame_new(6, filtersDB, lang)],
        [frame_new(7, filtersDB, lang)] # just add more frames here
    ]
    T5_col1 = [
        [sg.Push(), sg.Text(tr.gui_input[lang], font=title_font, key='T5_title1'), sg.Push()],
        [sg.Text(tr.gui_step1[lang], key='T5_step1')],
        [sg.Radio(tr.gui_spectrum[lang], 'DataTypeRadio', enable_events=True, default=True, key='-typeSpectrum-')],
        [sg.Radio(tr.gui_image[lang], 'DataTypeRadio', enable_events=True, key='-typeImage-')],
        [sg.Text(tr.gui_step2[lang], key='T5_step2')],
        [sg.Column(T5_frames, scrollable=True, vertical_scroll_only=True, key='T5_frames', expand_y=True)]
    ]
    T5_col2 = [
        [sg.Push(), sg.Text(tr.gui_results[lang], font=title_font, key='T5_title2'), sg.Push()],
        [sg.Canvas(key='T5_canvas')]
    ]

    tab1 = [
        [
            sg.Column(T1_col1, expand_x=True, expand_y=True), sg.VSeperator(),
            sg.Column(T1_col2, expand_x=True, expand_y=True)
        ]
    ]
    tab2 = [
        [
            sg.Column(T2_col1), sg.VSeperator(),
            sg.Column(T2_col2, expand_x=True, expand_y=True)
        ]
    ]
    tab4 = [
        [
            sg.Column(T4_col1, expand_x=True, expand_y=True), sg.VSeperator(),
            sg.Column(T4_col2, expand_x=True, expand_y=True)
        ]
    ]
    tab5 = [
        [
            sg.Column(T5_col1, expand_x=True, expand_y=True), sg.VSeperator(),
            sg.Column(T5_col2, expand_x=True, expand_y=True)
        ]
    ]
    tabs = sg.TabGroup([[
            sg.Tab(tr.gui_tabs[lang][0], tab1, key='tab1'),
            sg.Tab(tr.gui_tabs[lang][1], tab2, key='tab2'),
            sg.Tab(tr.gui_tabs[lang][2], tab3, key='tab3'),
            sg.Tab(tr.gui_tabs[lang][3], tab4, key='tab4'),
            sg.Tab('WIP', tab5, key='tab5')
    ]], expand_x=True, expand_y=True, enable_events=True, key='-currentTab-')
    return [
        [sg.Menu(tr.gui_menu[lang], key='menu')],
        [sg.vtop(settings_column), tabs]
    ]


def translate(window: sg.Window, T2_num: int, T5_num: int, lang: str):
    window['menu'].update(tr.gui_menu[lang])
    window['tab1'].update(title=tr.gui_tabs[lang][0])
    window['tab2'].update(title=tr.gui_tabs[lang][1])
    window['tab3'].update(title=tr.gui_tabs[lang][2])
    window['tab4'].update(title=tr.gui_tabs[lang][3])
    window['T1_title1'].update(tr.gui_database[lang])
    window['-settingsTitle-'].update(tr.gui_settings[lang])
    window['T1_title2'].update(tr.gui_results[lang])
    window['T1_database'].update(tr.gui_update[lang] if window['T1_database'].metadata else tr.gui_load[lang])
    window['T1_tagsN'].update(tr.gui_tags[lang])
    window['-gamma-'].update(text=tr.gui_gamma[lang])
    window['-brModeText-'].update(tr.gui_br[lang][0])
    window['-brMode0-'].update(text=tr.gui_br[lang][1])
    window['-brMode1-'].update(text=tr.gui_br[lang][2])
    window['-interpModeText-'].update(tr.gui_interp[lang][0])
    window['-interpMode0-'].update(text=tr.gui_interp[lang][1])
    window['-interpMode1-'].update(text=tr.gui_interp[lang][2])
    window['-formattingText-'].update(tr.gui_formatting[lang])
    window['-bitnessText-'].update(tr.gui_bit[lang])
    window['-roundingText-'].update(tr.gui_rnd[lang])
    window['T1_colorRGB'].update(tr.gui_rgb[lang])
    window['T1_colorHEX'].update(tr.gui_hex[lang])
    window['T1_add'].update(tr.gui_add[lang])
    window['T1_plot'].update(tr.gui_plot[lang])
    window['T1_clear'].update(tr.gui_clear[lang])
    window['T1_export'].update(tr.gui_export[lang])
    window['T2_title1'].update(tr.gui_input[lang])
    window['T2_title2'].update(tr.gui_output[lang])
    for i in range(T2_num):
        window['T2_band'+str(i)].update(f'{tr.gui_band[lang]} {i+1}')
        window['T2_browse'+str(i)].update(tr.gui_browse[lang])
        window['T2_filterN'+str(i)].update(tr.gui_filter[lang])
        window['T2_wavelengthN'+str(i)].update(tr.gui_wavelength[lang])
        window['T2_exposureN'+str(i)].update(tr.gui_exposure[lang])
    window['T2_makebright'].update(text=tr.gui_makebright[lang])
    window['T2_autoalign'].update(text=tr.gui_autoalign[lang])
    window['T2_desun'].update(text=tr.gui_desun[lang])
    window['T2_plotpixels'].update(text=tr.gui_plotpixels[lang])
    window['T2_filterset'].update(text=tr.gui_filterset[lang])
    window['T2_single'].update(text=tr.gui_single[lang])
    window['T2_browse'].update(tr.gui_browse[lang])
    window['T2_folderN'].update(tr.gui_folder[lang])
    window['T2_browse_folder'].update(tr.gui_browse[lang])
    window['T2_preview'].update(tr.gui_preview[lang])
    window['T2_process'].update(tr.gui_process[lang])
    window['T3_browse_folder'].update(tr.gui_browse[lang])
    window['T3_folderN'].update(tr.gui_folder[lang])
    window['T3_database'].update(tr.gui_update[lang] if window['T3_database'].metadata else tr.gui_load[lang])
    window['T3_tagsN'].update(tr.gui_tags[lang])
    window['T3_ext'].update(tr.gui_extension[lang])
    window['T3_process'].update(tr.gui_process[lang])
    window['T4_title1'].update(tr.gui_input[lang])
    window['T4_title2'].update(tr.gui_results[lang])
    window['T4_temp'].update(tr.gui_temp[lang])
    window['T4_velocity'].update(tr.gui_velocity[lang])
    window['T4_vII'].update(tr.gui_vII[lang])
    window['T4_mag'].update(tr.gui_mag[lang])
    window['T4_overexposure'].update(text=tr.gui_overexposure[lang])
    window['T4_explanation'].update(tr.gui_explanation[lang])
    window['T4_colorRGB'].update(tr.gui_rgb[lang])
    window['T4_colorHEX'].update(tr.gui_hex[lang])
    window['T4_add'].update(tr.gui_add[lang])
    window['T4_plot'].update(tr.gui_plot[lang])
    window['T4_clear'].update(tr.gui_clear[lang])
    window['T5_title1'].update(tr.gui_input[lang])
    window['T5_title2'].update(tr.gui_results[lang])
    window['T5_step1'].update(tr.gui_step1[lang])
    window['T5_step2'].update(tr.gui_step2[lang])
    for i in range(T5_num):
        window['T5_band'+str(i)].update(f'{tr.gui_band[lang]} {i+1}')
        window['T5_filterText'+str(i)].update(tr.gui_filter[lang])
        window['T5_brText'+str(i)].update(tr.gui_brightness[lang])
        window['T5_pathText'+str(i)].update(tr.gui_browse[lang])
    window['-typeSpectrum-'].update(text=tr.gui_spectrum[lang])
    window['-typeImage-'].update(text=tr.gui_image[lang])
    return window