""" Generates and launches a graphical interface that accesses other modules. """

import FreeSimpleGUI as sg
from sigfig import round as sigfig_round
from copy import deepcopy
import src.gui as gui
from src.data_core import Spectrum, get_filter
import src.auxiliary as aux
import src.data_import as di
import src.data_processing as dp
import src.color_processing as cp
import src.image_processing as ip
from src.table_generator import generate_table
import src.plotter as pl
import src.strings as tr


def launch_window(lang: str):

    # Databases declaration, to be filled by the json5 database later
    objectsDB, refsDB = {}, {}
    tagsDB = []
    filtersDB = di.list_filters()

    # Processing configuration
    default_tag = 'featured'
    brMode = 1 # default brightness mode
    bitness = 1
    rounding = 3

    # GUI configuration
    T2_num = 8 # max number of image bands
    T2_vis = T2_num # current number of visible image bands
    circle_r = 100 # radius in pixels of color preview circle
    circle_coord = (circle_r, circle_r+1)
    img_preview_size = (256, 128)
    img_preview_area = img_preview_size[0]*img_preview_size[1]
    text_colors = (gui.muted_color, gui.text_color)

    # Launching the main window
    sg.ChangeLookAndFeel('MaterialDark')
    window0 = sg.Window(
        'TrueColorTools', icon=gui.icon, finalize=True, resizable=True, margins=(0, 0), size=(1000, 640),
        layout=gui.generate_layout(
            (2*circle_r+1, 2*circle_r+1), img_preview_size, text_colors, filtersDB, brMode, bitness, rounding, T2_num, lang
        )
    )
    # Creating the plot window stub
    window1 = None

    T2_logger = gui.create_logger(window0, 'T2_thread')

    # Setting default color preview circle
    T1_preview = window0['T1_graph'].DrawCircle(circle_coord, circle_r, fill_color='black', line_color=None)
    T3_preview = window0['T3_graph'].DrawCircle(circle_coord, circle_r, fill_color='black', line_color=None)

    # Setting plots templates
    light_theme = False
    plot_data = {} # for tabs 1 and 3, both at once
    background_plot = ((cp.r, cp.g, cp.b), (cp.x, cp.y, cp.z)) # for tab 2
    mean_spectrum = [] # for tab 2

    T1_raw_name = T1_spectrum = T3_raw_name = T3_spectrum = None

    def T1_T3_update_plot(fig, fig_canvas_agg, gamma: bool, srgb: bool, albedo: bool, light_theme: bool, lang: str):
        pl.close_figure(fig)
        fig_canvas_agg.get_tk_widget().forget()
        to_plot = deepcopy(plot_data)
        if T1_raw_name:
            to_plot |= {T1_raw_name: T1_spectrum}
        if T3_raw_name:
            to_plot |= {T3_raw_name: T3_spectrum}
        fig = pl.plot_spectra(to_plot, gamma, srgb, albedo, light_theme, lang)
        fig_canvas_agg = pl.draw_figure(window1['W1_canvas'].TKCanvas, fig)
        return fig, fig_canvas_agg
    
    # List of settings events that cause color recalculation
    triggers = ('-gamma-', '-srgb-', '-brMode0-', '-brMode1-', '-brMode2-', '-bitness-', '-rounding-')

    # Window events loop
    while True:
        window, event, values = sg.read_all_windows()

        # Closing one of the windows
        if event == sg.WIN_CLOSED or event == tr.gui_exit[lang]:
            window.close() # for pop-up windows, they're suddenly processed here too
            if window is window0:
                break # closing the main window = exit program
            elif window is window1:
                window1 = None # marking the plot window as closed
        
        # Events with the plot window
        elif event.endswith('plot'):
            if not window1:
                window1 = sg.Window(
                    tr.spectral_plot[lang], gui.generate_plot_layout(lang, light_theme), icon=gui.icon,
                    finalize=True, element_justification='center'
                )
            else:
                pl.close_figure(T1_T3_fig)
                T1_T3_fig_canvas_agg.get_tk_widget().forget()
            to_plot = deepcopy(plot_data)
            if T1_raw_name:
                to_plot |= {T1_raw_name: T1_spectrum}
            if T3_raw_name:
                to_plot |= {T3_raw_name: T3_spectrum}
            T1_T3_fig = pl.plot_spectra(to_plot, values['-gamma-'], values['-srgb-'], brMode, light_theme, lang)
            T1_T3_fig_canvas_agg = pl.draw_figure(window1['W1_canvas'].TKCanvas, T1_T3_fig)
        elif event == 'W1_path':
            T1_T3_fig.savefig(values['W1_path'], dpi=133.4) # 1200x800
        elif event == 'W1_light_theme':
            light_theme = values['W1_light_theme']
            T1_T3_fig, T1_T3_fig_canvas_agg = T1_T3_update_plot(
                T1_T3_fig, T1_T3_fig_canvas_agg, window0.ReturnValuesDictionary['-gamma-'],
                window0.ReturnValuesDictionary['-srgb-'], brMode, light_theme, lang
            )

        # Run-time translation
        elif event in tr.lang_list[lang]:
            for lng, lst in tr.langs.items(): # determine the language
                if event in lst:
                    lang = lng
                    break
            window0 = gui.translate_win0(window0, T2_vis, lang)
            if window1:
                window1 = gui.translate_win1(window1, lang)
                T1_T3_fig, T1_T3_fig_canvas_agg = T1_T3_update_plot(
                    T1_T3_fig, T1_T3_fig_canvas_agg, window0.ReturnValuesDictionary['-gamma-'],
                    window0.ReturnValuesDictionary['-srgb-'], brMode, light_theme, lang
                )
            window['T1_list'].update(values=tuple(aux.obj_names_dict(objectsDB, values['T1_tags'], lang).keys()))
        
        # Only the main window events
        if window is window0:

            # ------------ Global window events ------------
            
            if event == tr.gui_ref[lang]:
                if len(refsDB) == 0:
                    sg.popup(tr.gui_no_data_message[lang], title=event, icon=gui.icon, non_blocking=True)
                else:
                    to_show = ''
                    for key, value in refsDB.items():
                        to_show += f'"{key}": {value[0]}\n'
                        for info in value[1:]:
                            to_show += info + '\n'
                        to_show += '\n'
                    sg.popup_scrolled(to_show, title=event, size=(150, 25), icon=gui.icon, non_blocking=True)
            
            elif event == tr.gui_info[lang]:
                sg.popup(f'{tr.link}\n{tr.auth_info[lang]}', title=event, icon=gui.icon, non_blocking=True)
            
            # Global loading of spectra database, was needed for separate Table tab
            elif event == 'T1_database':
                objectsDB, refsDB = di.import_DBs(['spectra', 'spectra_extras'])
                tagsDB = aux.tag_list(objectsDB)
                namesDB = { # optimize!
                    'en': aux.obj_names_dict(objectsDB, 'ALL', 'en'),
                    'ru': aux.obj_names_dict(objectsDB, 'ALL', 'ru'),
                    'de': aux.obj_names_dict(objectsDB, 'ALL', 'de')
                }
                window['T1_tagsN'].update(visible=True)
                window['T1_tags'].update(default_tag, values=tagsDB, visible=True)
                window['T1_list'].update(values=tuple(aux.obj_names_dict(objectsDB, default_tag, lang).keys()), visible=True)
                window['T1_database'].update(tr.gui_update[lang])
                window['T1_database'].metadata=True # switcher from "Load" to "Update"

            # Brightness mode radio selection
            elif isinstance(event, str) and event.startswith('-brMode'):
                brMode = aux.get_flag_index((values['-brMode0-'], values['-brMode1-'], values['-brMode2-']))
            
            # Checks for empty input
            elif event == '-bitness-':
                try:
                    bitness = int(values['-bitness-'])
                except ValueError:
                    pass
            elif event == '-rounding-':
                try:
                    rounding = int(values['-rounding-'])
                except ValueError:
                    pass
            
            # Checking enabled and disables settings for the new selected tab
            elif event == '-currentTab-':
                is_img_tab = values['-currentTab-'] == 'tab2'
                text_color_is1tab = text_colors[int(values['-currentTab-'] == 'tab1')]
                text_color_not2tab = text_colors[int(not is_img_tab)]
                window['-srgb-'].update(text_color=text_color_not2tab)
                window['-brModeText-'].update(text_color=text_color_is1tab)
                window['-brMode0-'].update(text_color=text_color_is1tab)
                window['-brMode1-'].update(text_color=text_color_is1tab)
                window['-brMode2-'].update(text_color=text_color_is1tab)
                window['-formattingText-'].update(text_color=text_color_not2tab)
                window['-bitnessText-'].update(text_color=text_color_not2tab)
                window['-roundingText-'].update(text_color=text_color_not2tab)
                window['-bitness-'].update(disabled=is_img_tab, text_color=text_color_not2tab)
                window['-rounding-'].update(disabled=is_img_tab, text_color=text_color_not2tab)

            # ------------ Events in the tab "Database viewer" ------------

            if values['-currentTab-'] == 'tab1':

                if (event in triggers or event == 'T1_list' or event == 'T1_filter') and values['T1_list'] != []:
                    T1_name = values['T1_list'][0]
                    T1_raw_name = namesDB[lang][T1_name]

                    # Spectral data import and processing
                    T1_body = dp.database_parser(T1_name, objectsDB[T1_raw_name])
                    T1_albedo = brMode and isinstance(T1_body, dp.ReflectiveBody)

                    # Setting brightness mode
                    match brMode:
                        case 0:
                            T1_spectrum, T1_estimated = T1_body.get_spectrum('chromaticity')
                        case 1:
                            T1_spectrum, T1_estimated = T1_body.get_spectrum('geometric')
                        case 2:
                            T1_spectrum, T1_estimated = T1_body.get_spectrum('spherical')
                    
                    if T1_estimated:
                        window['T1_estimated'].update(tr.gui_estimated[lang])
                    else:
                        window['T1_estimated'].update('')

                    # Color calculation
                    if values['-srgb-']:
                        T1_color = cp.Color.from_spectrum_CIE(T1_spectrum, T1_albedo)
                    else:
                        T1_color = cp.Color.from_spectrum(T1_spectrum, T1_albedo)
                    if values['-gamma-']:
                        T1_color = T1_color.gamma_corrected()
                    T1_rgb = tuple(T1_color.to_bit(bitness).round(rounding))
                    T1_rgb_show = T1_color.to_html()

                    # Output
                    window['T1_graph'].TKCanvas.itemconfig(T1_preview, fill=T1_rgb_show)
                    window['T1_rgb'].update(T1_rgb)
                    window['T1_hex'].update(T1_rgb_show)
                    T1_filter = get_filter(values['T1_filter'])
                    window['T1_convolved'].update(sigfig_round(T1_spectrum.to_scope(T1_filter.nm)@T1_filter, rounding, warn=False))

                    # Dynamical plotting
                    if window1:
                        T1_T3_fig, T1_T3_fig_canvas_agg = T1_T3_update_plot(
                            T1_T3_fig, T1_T3_fig_canvas_agg, window0.ReturnValuesDictionary['-gamma-'],
                            window0.ReturnValuesDictionary['-srgb-'], brMode, light_theme, lang
                        )
                
                elif event == 'T1_tags':
                    window['T1_list'].update(tuple(aux.obj_names_dict(objectsDB, values['T1_tags'], lang).keys()))
                
                elif event == 'T1_pin' and values['T1_list'] != []:
                    plot_data |= {T1_raw_name: T1_spectrum}
                
                elif event == 'T1_unpin':
                    plot_data.pop(T1_raw_name)
                
                elif event == 'T1_export2text':
                    if len(objectsDB) == 0:
                        sg.popup(tr.gui_no_data_message[lang], title=tr.gui_output[lang], icon=gui.icon, non_blocking=True)
                    else:
                        T1_export = '\n' + '\t'.join(tr.gui_col[lang]) + '\n' + '_' * 36
                        for name, raw_name in aux.obj_names_dict(objectsDB, values['T1_tags'], lang).items():
                            T1_body = dp.database_parser(name, objectsDB[raw_name])
                            T1_albedo = brMode and isinstance(T1_body, dp.ReflectiveBody)
                        
                            # Setting brightness mode
                            match brMode:
                                case 0:
                                    T1_spectrum, T1_estimated = T1_body.get_spectrum('chromaticity')
                                case 1:
                                    T1_spectrum, T1_estimated = T1_body.get_spectrum('geometric')
                                case 2:
                                    T1_spectrum, T1_estimated = T1_body.get_spectrum('spherical')

                            # Color calculation
                            if values['-srgb-']:
                                T1_color = cp.Color.from_spectrum_CIE(T1_spectrum, T1_albedo)
                            else:
                                T1_color = cp.Color.from_spectrum(T1_spectrum, T1_albedo)
                            if values['-gamma-']:
                                T1_color = T1_color.gamma_corrected()
                            T1_rgb = tuple(T1_color.to_bit(bitness).round(rounding))

                            # Output
                            T1_export += f'\n{aux.export_colors(T1_rgb)}\t{name}'
                            if T1_estimated:
                                T1_export += f'; {tr.gui_estimated[lang]}'

                        sg.popup_scrolled(
                            T1_export, title=tr.gui_output[lang], size=(100, max(10, min(30, 3+len(objectsDB)))),
                            font=('Consolas', 10), icon=gui.icon, non_blocking=True
                        )
                
                elif event == 'T1_folder':
                    if len(objectsDB) == 0:
                        sg.popup(tr.gui_no_data_message[lang], title=tr.gui_output[lang], icon=gui.icon, non_blocking=True)
                    else:
                        generate_table(objectsDB, values['T1_tags'], brMode, values['-srgb-'], values['-gamma-'], values['T1_folder'], 'png', lang)
            
            # ------------ Events in the tab "Image processing" ------------
            
            elif values['-currentTab-'] == 'tab2':

                # Getting input data mode name
                T2_mode = aux.get_flag_index((values['-typeImage-'], values['-typeImageRGB-'], values['-typeImageCube-']))

                # Setting template for the bandpass frames list
                if T2_mode == 2: # Spectral cube
                    window['T2_frames'].update(visible=False)
                else:
                    window['T2_frames'].update(visible=True)
                    match T2_mode:
                        case 0: # Multiband image
                            T2_vis = T2_num
                        case 1: # RGB image
                            T2_vis = 3
                    for i in range(T2_num):
                        if i < T2_vis:
                            window[f'T2_band{i}'].update(visible=True)
                            window[f'T2_path{i}'].update(visible=values['-typeImage-'])
                            window[f'T2_pathText{i}'].update(visible=values['-typeImage-'])
                            window[f'T2_rgbText{i}'].update(visible=values['-typeImageRGB-'])
                        else:
                            window[f'T2_band{i}'].update(visible=False)
                
                # Setting single file choice
                T2_single_file_flag = T2_mode > 0
                window['T2_step2'].update(visible=not T2_single_file_flag)
                window['T2_path'].update(visible=T2_single_file_flag)
                window['T2_pathText'].update(visible=T2_single_file_flag)
                
                # Getting filters and image paths
                T2_files = []
                T2_filters = []
                T2_formulas = []
                for i in range(T2_vis):
                    T2_filter_name = values[f'T2_filter{i}']
                    if T2_filter_name != '':
                        T2_filter = get_filter(T2_filter_name)
                        T2_filters.append(T2_filter)
                        T2_files.append(values[f'T2_path{i}'])
                        T2_formulas.append(values[f'T2_eval{i}'])
                
                # Image processing
                if isinstance(event, str) and event in ('T2_preview', 'T2_folder'):
                    window.start_thread(
                        lambda: ip.image_parser(
                            image_mode=T2_mode,
                            preview_flag=event=='T2_preview',
                            save_folder=values['T2_folder'],
                            pixels_limit=img_preview_area,
                            single_file=values['T2_path'],
                            files=T2_files,
                            filters=T2_filters,
                            formulas=T2_formulas,
                            gamma_correction=values['-gamma-'],
                            srgb=values['-srgb-'],
                            desun=values['T2_desun'],
                            photons=values['T2_photons'],
                            makebright=values['T2_makebright'],
                            factor=float(values['T2_factor']),
                            enlarge=values['T2_enlarge'],
                            log=T2_logger
                        ),
                        ('T2_thread', 'End of the image processing thread\n')
                    )
                
                # Getting messages from image processing thread
                elif event[0] == 'T2_thread':
                    sg.Print(event[1]) # pop-up printing
                    if values[event] is not None:
                        # Updating preview image and adding mean spectrum to plot
                        preview, mean_spectrum = values[event]
                        window['T2_image'].update(data=ip.convert_to_bytes(preview))
                        mean_spectrum = [mean_spectrum]
                
                # Updating filters profile plot
                if (isinstance(event, str) and event.startswith('T2_filter')) or (event[0] == 'T2_thread' and values[event] is not None) or event in ('-currentTab-', '-srgb-'):
                    try:
                        pl.close_figure(T2_fig)
                        to_plot = [*background_plot[values['-srgb-']], *T2_filters, *mean_spectrum]
                        T2_fig = pl.plot_filters(to_plot, lang)
                    except UnboundLocalError: # means it's the first tab opening
                        T2_fig = pl.plot_filters(background_plot[values['-srgb-']], lang)
                        T2_fig_canvas_agg = pl.draw_figure(window['T2_canvas'].TKCanvas, T2_fig)
                    finally:
                        T2_fig_canvas_agg.get_tk_widget().forget()
                        T2_fig_canvas_agg = pl.draw_figure(window['T2_canvas'].TKCanvas, T2_fig)

            
            # ------------ Events in the tab "Blackbody & Redshifts" ------------
            
            elif values['-currentTab-'] == 'tab3':
                
                if event == 'T3_maxtemp_num':
                    window['T3_slider1'].update(range=(0, int(values['T3_maxtemp_num'])))
                
                elif event == 'T3_pin':
                    plot_data |= {T3_raw_name: T3_spectrum}
                
                elif event == 'T3_unpin':
                    plot_data.pop(T3_raw_name)
                
                else:
                    if event == 'T3_overexposure':
                        window['T3_mag'].update(text_color=text_colors[values['T3_overexposure']])
                        window['T3_slider4'].update(disabled=not values['T3_overexposure'])
                    
                    # Spectral data processing
                    T3_spectrum = Spectrum.from_blackbody_redshift(aux.visible_range, values['T3_slider1'], values['T3_slider2'], values['T3_slider3'])
                    T3_raw_name = T3_spectrum.name
                    if values['T3_overexposure']:
                        T3_spectrum.br /= dp.mag2flux(values['T3_slider4'], dp.vega_in_V) * dp.sun_in_V

                    # Color calculation
                    if values['-srgb-']:
                        T3_color = cp.Color.from_spectrum_CIE(T3_spectrum, albedo=values['T3_overexposure'])
                    else:
                        T3_color = cp.Color.from_spectrum(T3_spectrum, albedo=values['T3_overexposure'])
                    if values['-gamma-']:
                        T3_color = T3_color.gamma_corrected()
                    T3_rgb = tuple(T3_color.to_bit(bitness).round(rounding))
                    T3_rgb_show = T3_color.to_html()
                
                    # Output
                    window['T3_graph'].TKCanvas.itemconfig(T3_preview, fill=T3_rgb_show)
                    window['T3_rgb'].update(T3_rgb)
                    window['T3_hex'].update(T3_rgb_show)

                    # Dynamical plotting
                    if window1:
                        T1_T3_fig, T1_T3_fig_canvas_agg = T1_T3_update_plot(
                            T1_T3_fig, T1_T3_fig_canvas_agg, window0.ReturnValuesDictionary['-gamma-'],
                            window0.ReturnValuesDictionary['-srgb-'], brMode, light_theme, lang
                        )
