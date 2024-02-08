""" Generates and launches a graphical interface that accesses other modules. """

import PySimpleGUI as sg
from sigfig import round as sigfig_round
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
    brMode = True # default brightness mode
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

    # Launching window
    sg.ChangeLookAndFeel('MaterialDark')
    window = sg.Window(
        'TrueColorTools', finalize=True, resizable=True, margins=(0, 0), size=(1000, 640),
        layout=gui.generate_layout(
            (2*circle_r+1, 2*circle_r+1), img_preview_size, text_colors, filtersDB, bitness, rounding, T2_num, lang
        )
    )

    # Setting default color preview circle
    T1_preview = window['T1_graph'].DrawCircle(circle_coord, circle_r, fill_color='black', line_color=None)
    T3_preview = window['T3_graph'].DrawCircle(circle_coord, circle_r, fill_color='black', line_color=None)

    # Setting plots templates
    plot_data = [] # for tabs 1 and 3, both at once
    background_plot = ((cp.r, cp.g, cp.b), (cp.x, cp.y, cp.z)) # for tab 2
    
    # List of settings events that cause color recalculation
    triggers = ('-gamma-', '-srgb-', '-brMode0-', '-brMode1-', '-brMode2-', '-bitness-', '-rounding-')

    # Window events loop
    while True:
        event, values = window.read()

        # Independent window events

        if event == sg.WIN_CLOSED or event == tr.gui_exit[lang]:
            break
        # Radio selection
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
        # (allows other tab checks to happen)
        elif event == '-currentTab-':
            not_img_tab = int(not values['-currentTab-'] == 'tab2')
            text_color = text_colors[not_img_tab]
            window['-brModeText-'].update(text_color=text_color)
            window['-brMode0-'].update(text_color=text_color)
            window['-brMode1-'].update(text_color=text_color)
            window['-brMode2-'].update(text_color=text_color)
            window['-formattingText-'].update(text_color=text_color)
            window['-bitnessText-'].update(text_color=text_color)
            window['-roundingText-'].update(text_color=text_color)
            window['-bitness-'].update(disabled=not not_img_tab, text_color=text_color)
            window['-rounding-'].update(disabled=not not_img_tab, text_color=text_color)

        # Global window events

        if event in tr.lang_list[lang]:
            for lng, lst in tr.langs.items(): # determine language to translate
                if event in lst:
                    lang = lng
                    break
            window = gui.translate(window, T2_vis, lang)
            window['T1_list'].update(values=tuple(aux.obj_dict(objectsDB, values['T1_tags'], lang).keys()))
        
        elif event == tr.gui_ref[lang]:
            to_show = ''
            for key, value in refsDB.items():
                to_show += f'"{key}": {value[0]}\n'
                for info in value[1:]:
                    to_show += info + '\n'
                to_show += '\n'
            sg.popup_scrolled(to_show, title=event, size=(150, 25), non_blocking=True)
        
        elif event == tr.gui_info[lang]:
            sg.popup(f'{tr.link}\n{tr.auth_info[lang]}', title=event, non_blocking=True)
        
        elif event == 'T1_database': # global loading of spectra database, was needed for separate Table tab
            objectsDB, refsDB = di.import_DBs(['spectra', 'spectra_extras'])
            tagsDB = aux.tag_list(objectsDB)
            window['T1_tagsN'].update(visible=True)
            window['T1_tags'].update(default_tag, values=tagsDB, visible=True)
            window['T1_list'].update(values=tuple(aux.obj_dict(objectsDB, default_tag, lang).keys()), visible=True)
            window['T1_database'].update(tr.gui_update[lang])
            window['T1_database'].metadata=True # switcher from "Load" to "Update"

        # ------------ Events in the tab "Database viewer" ------------

        if values['-currentTab-'] == 'tab1':

            if (event in triggers or event == 'T1_list' or event == 'T1_filter') and values['T1_list'] != []:
                T1_name = values['T1_list'][0]
                T1_raw_name = aux.obj_dict(objectsDB, '_all_', lang)[T1_name]

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
            
            elif event == 'T1_tags':
                window['T1_list'].update(tuple(aux.obj_dict(objectsDB, values['T1_tags'], lang).keys()))
            
            elif event == 'T1_add' and values['T1_list'] != []:
                plot_data.append(T1_spectrum)
            
            elif event == 'T1_plot':
                pl.plot_spectra(plot_data, values['-gamma-'], values['-srgb-'], brMode, lang)
            
            elif event == 'T1_clear':
                plot_data = []
            
            elif event == 'T1_export2text':
                T1_export = '\n' + '\t'.join(tr.gui_col[lang]) + '\n' + '_' * 36
                
                for name, raw_name in aux.obj_dict(objectsDB, values['T1_tags'], lang).items():
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

                sg.popup_scrolled(T1_export, title=tr.gui_results[lang], size=(120, 40), font=('Consolas', 10), non_blocking=True)
            
            elif event == 'T1_folder':
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
            T2_filters = []
            T2_files = []
            for i in range(T2_vis):
                T2_filter_name = values[f'T2_filter{i}']
                if T2_filter_name != '':
                    T2_filter = get_filter(T2_filter_name)
                    T2_filters.append(T2_filter)
                    T2_files.append(values[f'T2_path{i}'])
            
            # Updating filters profile plot
            if (isinstance(event, str) and event.startswith('T2_filter')) or event in ('-currentTab-', '-srgb-'):
                try:
                    pl.close_figure(T2_fig)
                    T2_fig = pl.plot_filters([*background_plot[values['-srgb-']], *T2_filters], lang)
                except UnboundLocalError: # means it's the first tab opening
                    T2_fig = pl.plot_filters(background_plot[values['-srgb-']], lang)
                    figure_canvas_agg = pl.draw_figure(window['T2_canvas'].TKCanvas, T2_fig)
                finally:
                    figure_canvas_agg.get_tk_widget().forget()
                    figure_canvas_agg = pl.draw_figure(window['T2_canvas'].TKCanvas, T2_fig)
            
            # Image processing
            elif isinstance(event, str) and event in ('T2_preview', 'T2_folder'):
                window.start_thread(
                    lambda: ip.image_parser(
                        window, T2_mode, values['T2_folder'], img_preview_area, T2_filters, T2_files, values['T2_path'],
                        values['-gamma-'], values['-srgb-'], values['T2_makebright'], values['T2_desun'], float(values['T2_exposure'])
                    ),
                    ('T2_thread', 'End of the image processing thread.\n')
                )
                window['T2_folder'].update('') # preview mode is detected by this value
            
            # Getting messages from image processing thread
            elif event[0] == 'T2_thread':
                sg.Print(event[1]) # pop-up printing
                if values[event] is not None:
                    # Updating preview
                    window['T2_image'].update(data=ip.convert_to_bytes(values[event]))

        
        # ------------ Events in the tab "Blackbody & Redshifts" ------------
        
        elif values['-currentTab-'] == 'tab3':
            
            if event == 'T3_maxtemp_num':
                window['T3_slider1'].update(range=(0, int(values['T3_maxtemp_num'])))

            elif event == 'T3_add':
                plot_data.append(T3_spectrum)
            
            elif event == 'T3_plot':
                pl.plot_spectra(plot_data, values['-gamma-'], values['-srgb-'], brMode, lang)
            
            elif event == 'T3_clear':
                plot_data = []
            
            else:
                if event == 'T3_overexposure':
                    window['T3_mag'].update(text_color=text_colors[values['T3_overexposure']])
                    window['T3_slider4'].update(disabled=not values['T3_overexposure'])
                
                # Spectral data processing
                T3_spectrum = Spectrum.from_blackbody_redshift(aux.visible_range, values['T3_slider1'], values['T3_slider2'], values['T3_slider3'])
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

    window.close()