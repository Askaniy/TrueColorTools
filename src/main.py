""" Generates and launches a graphical interface that accesses other modules. """

import PySimpleGUI as sg
from sigfig import round as sigfig_round
import src.gui as gui
from src.core import Spectrum, get_filter
import src.data_import as di
import src.data_processing as dp
import src.color_processing as cp
from src.table_generator import generate_table
import src.image as im
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
    plot_data = [] # of the tabs 1 and 3
    T2_first_time = True
    
    # List of settings events that cause color recalculation
    triggers = ('-gamma-', '-srgb-', '-brMode0-', '-brMode1-', '-brMode2-', '-bitness-', '-rounding-')

    # Window events loop
    while True:
        event, values = window.read()

        # Independent window events

        if event == sg.WIN_CLOSED or event == tr.gui_exit[lang]:
            break
        # Radio selection
        elif event.startswith('-brMode'):
            brMode = get_flag_index((values['-brMode0-'], values['-brMode1-'], values['-brMode2-']))
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
            is_color_circle = int(values['-currentTab-'] in ('tab1', 'tab3'))
            window['-formattingText-'].update(text_color=text_colors[is_color_circle])
            window['-bitnessText-'].update(text_color=text_colors[is_color_circle])
            window['-roundingText-'].update(text_color=text_colors[is_color_circle])
            window['-bitness-'].update(disabled=not is_color_circle)
            window['-rounding-'].update(disabled=not is_color_circle)

        # Global window events

        if event in tr.lang_list[lang]:
            for lng, lst in tr.langs.items(): # determine language to translate
                if event in lst:
                    lang = lng
                    break
            window = gui.translate(window, T2_num, lang)
            window['T1_list'].update(values=tuple(di.obj_dict(objectsDB, values['T1_tags'], lang).keys()))
        
        elif event == tr.gui_ref[lang]:
            to_show = ''
            for key, value in refsDB.items():
                to_show += f'"{key}": {value[0]}\n'
                for info in value[1:]:
                    to_show += info + '\n'
                to_show += '\n'
            sg.popup_scrolled(to_show, title=event, size=(150, 25))
        
        elif event == tr.gui_info[lang]:
            sg.popup(f'{tr.link}\n{tr.auth_info[lang]}', title=event)
        
        elif event == 'T1_database': # global loading of spectra database, was needed for separate Table tab
            objectsDB, refsDB = di.import_DBs(['spectra', 'spectra_extras'])
            tagsDB = di.tag_list(objectsDB)
            window['T1_tagsN'].update(visible=True)
            window['T1_tags'].update(default_tag, values=tagsDB, visible=True)
            window['T1_list'].update(values=tuple(di.obj_dict(objectsDB, default_tag, lang).keys()), visible=True)
            window['T1_database'].update(tr.gui_update[lang])
            window['T1_database'].metadata=True # switcher from "Load" to "Update"

        # ------------ Events in the tab "Database viewer" ------------

        if values['-currentTab-'] == 'tab1':

            if (event in triggers or event == 'T1_list' or event == 'T1_filter') and values['T1_list'] != []:
                T1_name = values['T1_list'][0]
                T1_raw_name = di.obj_dict(objectsDB, '_all_', lang)[T1_name]

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
                window['T1_list'].update(tuple(di.obj_dict(objectsDB, values['T1_tags'], lang).keys()))
            
            elif event == 'T1_add' and values['T1_list'] != []:
                plot_data.append(T1_spectrum)
            
            elif event == 'T1_plot':
                pl.plot_spectra(plot_data, values['-gamma-'], values['-srgb-'], brMode and T1_albedo, lang)
            
            elif event == 'T1_clear':
                plot_data = []
            
            elif event == 'T1_export2text':
                T1_export = '\n' + '\t'.join(tr.gui_col[lang]) + '\n' + '_' * 36
                
                for name, raw_name in di.obj_dict(objectsDB, values['T1_tags'], lang).items():
                    T1_body = dp.database_parser(name, objectsDB[raw_name])
                    T1_albedo = brMode and isinstance(T1_body, dp.ReflectiveBody)
                
                    # Setting brightness mode
                    match brMode:
                        case 0:
                            T1_spectrum, _ = T1_body.get_spectrum('chromaticity')
                        case 1:
                            T1_spectrum, _ = T1_body.get_spectrum('geometric')
                        case 2:
                            T1_spectrum, _ = T1_body.get_spectrum('spherical')

                    # Color calculation
                    if values['-srgb-']:
                        T1_color = cp.Color.from_spectrum_CIE(T1_spectrum, T1_albedo)
                    else:
                        T1_color = cp.Color.from_spectrum(T1_spectrum, T1_albedo)
                    if values['-gamma-']:
                        T1_color = T1_color.gamma_corrected()
                    T1_rgb = tuple(T1_color.to_bit(bitness).round(rounding))

                    # Output
                    T1_export += f'\n{export_colors(T1_rgb)}\t{name}'

                sg.popup_scrolled(T1_export, title=tr.gui_results[lang], size=(72, 32), font=('Consolas', 10))
            
            elif event == 'T1_folder':
                generate_table(objectsDB, values['T1_tags'], brMode, values['-srgb-'], values['-gamma-'], values['T1_folder'], 'png', lang)
        
        # ------------ Events in the tab "Multiband processing" ------------
        
        elif values['-currentTab-'] == 'tab2':
            if T2_first_time:
                if values['-srgb-']:
                    T2_plot_data = [cp.x, cp.y, cp.z]
                else:
                    T2_plot_data = [cp.r, cp.g, cp.b]
                T2_fig = pl.plot_filters(T2_plot_data)
                figure_canvas_agg = pl.draw_figure(window['T2_canvas'].TKCanvas, T2_fig)
                T2_first_time = False

            # Getting input data mode name
            T2_mode = tr.gui_datatype['en'][get_flag_index(
                (values['-typeSpectrum-'], values['-typeImage-'], values['-typeImageRGB-'], values['-typeImageCube-']))]

            # Setting template for the band list
            # BUG in PySimpleGUI: after translating, bands where visible=False become visible.
            for i in range(T2_num):
                window['T2_band'+str(i)].update(visible=False)
                window['T2_path'+str(i)].update(visible=values['-typeImage-'])
                window['T2_pathText'+str(i)].update(visible=values['-typeImage-'])
                window['T2_brText'+str(i)].update(visible=values['-typeSpectrum-'])
                window['T2_br'+str(i)].update(visible=values['-typeSpectrum-'])
                window['T2_bgrText'+str(i)].update(visible=values['-typeImageRGB-'])
            match event:
                case '-typeImageRGB-':
                    T2_vis = 3
                case '-typeImageCube-':
                    T2_vis = 0
                case _:
                    T2_vis = T2_num
            for i in range(T2_vis):
                window['T2_band'+str(i)].update(visible=True)
            
            # Setting single file choice
            T2_single_file = values['-typeImageRGB-'] or values['-typeImageCube-']
            window['T2_step2'].update(visible=not T2_single_file)
            window['T2_path'].update(visible=T2_single_file)
            window['T2_pathText'].update(visible=T2_single_file)
            
            if event.startswith('T2_filter') or event == '-srgb-':
                if values['-srgb-']:
                    T2_plot_data = [cp.x, cp.y, cp.z]
                else:
                    T2_plot_data = [cp.r, cp.g, cp.b]
                for i in range(T2_num):
                    T2_filter_name = values['T2_filter'+str(i)]
                    if T2_filter_name != '':
                        T2_filter = get_filter(T2_filter_name)
                        T2_plot_data.append(T2_filter)
                T2_fig.clf()
                T2_fig = pl.plot_filters(T2_plot_data)
                figure_canvas_agg.get_tk_widget().forget()
                figure_canvas_agg = pl.draw_figure(window['T2_canvas'].TKCanvas, T2_fig)

        
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
                T3_spectrum = Spectrum.from_blackbody_redshift(dp.visible_range, values['T3_slider1'], values['T3_slider2'], values['T3_slider3'])
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


def export_colors(rgb: tuple):
    """ Generates formatted string of colors """
    lst = []
    mx = 0
    for i in rgb:
        lst.append(str(i))
        l = len(lst[-1])
        if l > mx:
            mx = l
    w = 8 if mx < 8 else mx+1
    return ''.join([i.ljust(w) for i in lst])

def get_flag_index(flags: tuple):
    """ Returns index of active radio button """
    for index, flag in enumerate(flags):
        if flag:
            return index