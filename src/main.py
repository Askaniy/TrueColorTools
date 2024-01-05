import PySimpleGUI as sg
import src.core as core
import src.gui as gui
import src.data_import as di
import src.image as im
import src.plotter as pl
import src.strings as tr
import src.table_generator as tg


def launch_window(lang: str):

    # Databases declaration, to be filled by the json5 database later
    objectsDB, refsDB = {}, {}
    tagsDB = []
    filtersDB = di.list_filters()

    # Processing configuration
    default_tag = 'featured'
    albedoFlag = True # default brightness mode
    #oldInterpFlag = True # default interpolation mode
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
        'TrueColorTools', finalize=True, resizable=True, margins=(0, 0), size=(900, 640),
        layout=gui.generate_layout(
            (2*circle_r+1, 2*circle_r+1), img_preview_size, text_colors, filtersDB, albedoFlag, bitness, rounding, T2_num, lang
            )
        )

    # Setting default color preview circle
    T1_preview = window['T1_graph'].DrawCircle(circle_coord, circle_r, fill_color='black', line_color=None)
    T3_preview = window['T3_graph'].DrawCircle(circle_coord, circle_r, fill_color='black', line_color=None)

    # Setting plots templates
    plot_data = [] # of the tabs 1 and 3
    T2_first_time = True
    
    # List of events that cause color recalculation
    triggers = ('-gamma-', '-srgb-', '-brMode0-', '-brMode1-', '-interpMode0-', '-interpMode1-', '-bitness-', '-rounding-')

    # Window events loop
    while True:
        event, values = window.read()

        # Independent window events

        if event == sg.WIN_CLOSED or event == tr.gui_exit[lang]:
            break
        # Radio selection
        elif event in ('-brMode0-', '-brMode1-'):
            albedoFlag = values['-brMode0-']
        #elif event in ('-interpMode0-', '-interpMode1-'):
        #    oldInterpFlag = values['-interpMode0-']
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
        
        elif event == tr.ref[lang]:
            to_show = ''
            for key, value in refsDB.items():
                to_show += f'"{key}": {value[0]}\n'
                for info in value[1:]:
                    to_show += info + '\n'
                to_show += '\n'
            sg.popup_scrolled(to_show, title=event, size=(150, 25))
        
        elif event == tr.note[lang]:
            notes = []
            for note, translation in tr.notes.items():
                notes.append(f'{note} {translation[lang]}')
            sg.popup('\n'.join(notes), title=event)
        
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

            if (event in triggers or event == 'T1_list') and values['T1_list'] != []:
                T1_name = values['T1_list'][0]
                T1_raw_name = di.obj_dict(objectsDB, '_all_', lang)[T1_name]
                T1_object_unit = objectsDB[T1_raw_name]
                T1_albedo = ('albedo' in T1_object_unit and T1_object_unit['albedo']) or 'scale' in T1_object_unit

                # Spectral data import and processing
                T1_spectrum = core.from_database(T1_name, T1_object_unit).to_scope(core.visible_range)
                if albedoFlag and 'scale' in T1_object_unit:
                    T1_spectrum = T1_spectrum.scaled(*T1_object_unit['scale'])
                
                # Color calculation
                if values['-srgb-']:
                    T1_color = core.Color.from_spectrum(T1_spectrum, albedoFlag and T1_albedo)
                else:
                    T1_color = core.Color.from_spectrum_legacy(T1_spectrum, albedoFlag and T1_albedo)
                if values['-gamma-']:
                    T1_color = T1_color.gamma_corrected()
                T1_rgb = tuple(T1_color.to_bit(bitness).round(rounding))
                T1_rgb_show = T1_color.to_html()

                # Output
                window['T1_graph'].TKCanvas.itemconfig(T1_preview, fill=T1_rgb_show)
                window['T1_rgb'].update(T1_rgb)
                window['T1_hex'].update(T1_rgb_show)
            
            elif event == 'T1_tags':
                window['T1_list'].update(tuple(di.obj_dict(objectsDB, values['T1_tags'], lang).keys()))
            
            elif event == 'T1_add' and values['T1_list'] != []:
                plot_data.append(T1_spectrum)
            
            elif event == 'T1_plot':
                pl.plot_spectra(plot_data, values['-gamma-'], values['-srgb-'], albedoFlag and T1_albedo, lang)
            
            elif event == 'T1_clear':
                plot_data = []
            
            elif event == 'T1_export2text':
                T1_export = '\n' + '\t'.join(tr.gui_col[lang]) + '\n' + '_' * 36
                
                for name, raw_name in di.obj_dict(objectsDB, values['T1_tags'], lang).items():
                    T1_object_unit = objectsDB[raw_name]
                    T1_albedo = ('albedo' in T1_object_unit and T1_object_unit['albedo']) or 'scale' in T1_object_unit

                    # Spectral data import and processing
                    T1_spectrum = core.from_database(name, T1_object_unit).to_scope(core.visible_range)
                    if albedoFlag and 'scale' in T1_object_unit:
                        T1_spectrum = T1_spectrum.scaled(*T1_object_unit['scale'])
                    
                    # Color calculation
                    if values['-srgb-']:
                        T1_color = core.Color.from_spectrum(T1_spectrum, albedoFlag and T1_albedo)
                    else:
                        T1_color = core.Color.from_spectrum_legacy(T1_spectrum, albedoFlag and T1_albedo)
                    if values['-gamma-']:
                        T1_color = T1_color.gamma_corrected()
                    T1_rgb = tuple(T1_color.to_bit(bitness).round(rounding))

                    # Output
                    T1_export += f'\n{export_colors(T1_rgb)}\t{name}'

                sg.popup_scrolled(T1_export, title=tr.gui_results[lang], size=(72, 32), font=('Consolas', 10))
            
            elif event == 'T1_folder':
                tg.generate_table(objectsDB, values['T1_tags'], albedoFlag, values['-srgb-'], values['-gamma-'], values['T1_folder'], 'png', lang)
        
        # ------------ Events in the tab "Multiband processing" ------------
        
        elif values['-currentTab-'] == 'tab2':
            if T2_first_time:
                if values['-srgb-']:
                    T2_plot_data = [core.x, core.y, core.z]
                else:
                    T2_plot_data = [core.r, core.g, core.b]
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
                    T2_plot_data = [core.x, core.y, core.z]
                else:
                    T2_plot_data = [core.r, core.g, core.b]
                for i in range(T2_num):
                    T2_filter_name = values['T2_filter'+str(i)]
                    if T2_filter_name != '':
                        T2_filter = core.get_filter(T2_filter_name)
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
                pl.plot_spectra(plot_data, values['-gamma-'], values['-srgb-'], albedoFlag, lang)
            
            elif event == 'T3_clear':
                plot_data = []
            
            else:
                if event == 'T3_overexposure':
                    window['T3_mag'].update(text_color=text_colors[values['T3_overexposure']])
                    window['T3_slider4'].update(disabled=not values['T3_overexposure'])
                
                # Spectral data processing
                T3_spectrum = core.Spectrum.from_blackbody_redshift(core.visible_range, values['T3_slider1'], values['T3_slider2'], values['T3_slider3'])
                if values['T3_overexposure']:
                    T3_spectrum.br /= core.mag2irradiance(values['T3_slider4'], core.vega_in_V) * core.sun_in_V

                # Color calculation
                if values['-srgb-']:
                    T3_color = core.Color.from_spectrum(T3_spectrum, albedo=values['T3_overexposure'])
                else:
                    T3_color = core.Color.from_spectrum_legacy(T3_spectrum, albedo=values['T3_overexposure'])
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