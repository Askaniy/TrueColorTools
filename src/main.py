import traceback
import PySimpleGUI as sg
import src.core as core
import src.gui as gui
import src.filters as filters
import src.data_import as di
import src.image as im
import src.plotter as pl
import src.strings as tr
import src.table_generator as tg


def launch_window():
    lang = 'en' # can be translated into German or Russian at runtime
    objectsDB, refsDB = {}, {} # initial loading became too long with separate json5 database files
    tagsDB = []
    default_tag = 'featured'
    filtersDB = di.list_filters()

    circle_r = 100 # radius in pixels of color preview circle
    circle_coord = (circle_r, circle_r+1)
    T2_preview_size = (256, 128)
    T2_preview_area = T2_preview_size[0]*T2_preview_size[1]
    text_colors = (gui.muted_color, gui.text_color)

    sg.ChangeLookAndFeel('MaterialDark')
    window = sg.Window(
        'True Color Tools', gui.generate_layout((2*circle_r+1, 2*circle_r+1), T2_preview_size, text_colors, filtersDB, lang),
        finalize=True, resizable=True, margins=(0, 0), size=(900, 600))
    T2_vis = 3  # current number of visible image bands
    T2_num = 10 # max number of image bands, ~ len(window['T2_frames'])
    T5_num = 8
    for i in range(T2_vis, T2_num):
        window['T2_band'+str(i)].update(visible=False)

    T1_preview = window['T1_graph'].DrawCircle(circle_coord, circle_r, fill_color='black', line_color=None)
    T4_preview = window['T4_graph'].DrawCircle(circle_coord, circle_r, fill_color='black', line_color=None)

    triggers = ['-gamma-', '-srgb-', '-brMode0-', '-brMode1-', '-interpMode0-', '-interpMode1-', '-bitness-', '-rounding-']
    
    albedoFlag = False # default brightness mode
    #oldInterpFlag = True # default interpolation mode
    bitness = int(window['-bitness-'].get())
    rounding = int(window['-rounding-'].get())

    plot_data = [] # of the tabs 1 and 4
    T5_plot_data = [core.r, core.g, core.b]
    T5_fig = pl.plot_filters(T5_plot_data)
    figure_canvas_agg = pl.draw_figure(window['T5_canvas'].TKCanvas, T5_fig)
    

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
            is_color_circle = int(values['-currentTab-'] in ('tab1', 'tab4'))
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
            window = gui.translate(window, T2_num, T5_num, lang)
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
        
        elif event.endswith('database'): # global loading of spectra database
            objectsDB, refsDB = di.import_DBs(['spectra']) # ['spectra', 'extras']
            tagsDB = di.tag_list(objectsDB)
            window['T1_tagsN'].update(visible=True)
            window['T1_tags'].update(default_tag, values=tagsDB, visible=True)
            window['T3_tagsN'].update(text_color=text_colors[1])
            window['T3_tags'].update(default_tag, values=tagsDB, disabled=False)
            window['T1_list'].update(values=tuple(di.obj_dict(objectsDB, default_tag, lang).keys()), visible=True)
            window['T1_database'].metadata=True
            window['T1_database'].update(tr.gui_update[lang])
            window['T3_database'].metadata=True
            window['T3_database'].update(tr.gui_update[lang])

        # ------------ Events in the tab "Spectra" ------------

        if values['-currentTab-'] == 'tab1':

            if (event in triggers or event == 'T1_list') and values['T1_list'] != []:
                T1_name = values['T1_list'][0]
                T1_raw_name = di.obj_dict(objectsDB, 'all', lang)[T1_name]

                # Spectral data import and processing
                T1_photometry = core.Photometry(T1_name, objectsDB[T1_raw_name])
                T1_spectrum = core.Spectrum.from_photometry(T1_photometry, core.visible_range)
                if T1_photometry.sun:
                    T1_spectrum /= core.sun_norm
                if albedoFlag:
                    if isinstance(T1_photometry.albedo, float):
                        T1_spectrum = T1_spectrum.scaled_to_albedo(T1_photometry.albedo, core.bessell_V)
                
                # Color calculation
                if values['-srgb-']:
                    T1_color = core.Color.from_spectrum(T1_spectrum, albedoFlag and T1_photometry.albedo)
                else:
                    T1_color = core.Color.from_spectrum_legacy(T1_spectrum, albedoFlag and T1_photometry.albedo)
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
                pl.plot_spectra(plot_data, values['-gamma-'], values['-srgb-'], albedoFlag, lang)
            
            elif event == 'T1_clear':
                plot_data = []
            
            elif event == 'T1_export':
                T1_export = '\n' + '\t'.join(tr.gui_col[lang]) + '\n' + '_' * 36
                
                for name, raw_name in di.obj_dict(objectsDB, values['T1_tags'], lang).items():

                    # Spectral data import and processing
                    T1_photometry = core.Photometry(name, objectsDB[raw_name])
                    T1_spectrum = core.Spectrum.from_photometry(T1_photometry, core.visible_range)
                    if T1_photometry.sun:
                        T1_spectrum /= core.sun_norm
                    if albedoFlag:
                        if isinstance(T1_photometry.albedo, float):
                            T1_spectrum = T1_spectrum.scaled_to_albedo(T1_photometry.albedo, core.bessell_V)
                    
                    # Color calculation
                    if values['-srgb-']:
                        T1_color = core.Color.from_spectrum(T1_spectrum, albedoFlag and T1_photometry.albedo)
                    else:
                        T1_color = core.Color.from_spectrum_legacy(T1_spectrum, albedoFlag and T1_photometry.albedo)
                    if values['-gamma-']:
                        T1_color = T1_color.gamma_corrected()
                    T1_rgb = tuple(T1_color.to_bit(bitness).round(rounding))

                    # Output
                    T1_export += f'\n{export_colors(T1_rgb)}\t{name}'

                sg.popup_scrolled(T1_export, title=tr.gui_results[lang], size=(72, 32), font=('Consolas', 10))
        
        # ------------ Events in the tab "Images" ------------

        elif values['-currentTab-'] == 'tab2':

            if event == 'T2_single':
                window['T2_browse'].update(disabled=not values['T2_single'])
                window['T2_path'].update(disabled=not values['T2_single'])
                for i in range(T2_num):
                    window['T2_browse'+str(i)].update(disabled=values['T2_single'])
                    window['T2_path'+str(i)].update(disabled=values['T2_single'])
                if values['T2_single']:
                    T2_vis = 3
                    for i in range(T2_num):
                        window['T2_band'+str(i)].update(visible=False)
                    for i in range(3):
                        window['T2_band'+str(i)].update(visible=True)

            elif event == 'T2_filterset':
                window['T2_filter'].update(disabled=not values['T2_filterset'])
                for i in range(T2_num):
                    window['T2_filter'+str(i)].update(disabled=not values['T2_filterset'])
                    window['T2_wavelength'+str(i)].update(disabled=values['T2_filterset'])

            elif event == 'T2_filter':
                for i in range(T2_num):
                    window['T2_filter'+str(i)].update(values=filters.get_filters(values['T2_filter']))

            elif event in ['T2_filter'+str(i) for i in range(T2_num)]:
                i = event[-1]
                window['T2_wavelength'+i].update(filters.get_param(values['T2_filter'], values['T2_filter'+i], 'L_mean'))

            elif event == 'T2_folder':
                window['T2_process'].update(disabled=False)
            
            elif event == 'T2_+':
                window['T2_band'+str(T2_vis)].update(visible=True)
                T2_vis += 1
            
            elif event == 'T2_-':
                window['T2_band'+str(T2_vis-1)].update(visible=False)
                T2_vis -= 1
            
            window['T2_+'].update(disabled=values['T2_single'] or not 2 <= T2_vis < T2_num)
            window['T2_-'].update(disabled=values['T2_single'] or not 2 < T2_vis <= T2_num)
            for i in range(T2_num):
                window['T2_filterN'+str(i)].update(text_color=text_colors[values['T2_filterset']])
                window['T2_wavelengthN'+str(i)].update(text_color=text_colors[not values['T2_filterset']])
            
            input_data = {'gamma': values['-gamma-'], 'srgb': values['-srgb-'], 'desun': values['T2_desun'], 'nm': []}
            
            T2_preview_status = True
            if values['T2_single']:
                if values['T2_path'] == '':
                    T2_preview_status = False
            else:
                for i in range(T2_vis):
                    if values['T2_path'+str(i)] == '':
                        T2_preview_status = False
                        break
            if values['T2_filterset']:
                for i in range(T2_vis):
                    if values['T2_filter'+str(i)]:
                        try:
                            input_data['nm'].append(filters.get_param(values['T2_filter'], values['T2_filter'+str(i)], 'L_mean'))
                        except KeyError:
                            window['T2_filter'+str(i)].update([])
                    else:
                        T2_preview_status = False
                        break
            else:
                for i in range(T2_vis):
                    if values['T2_wavelength'+str(i)].replace('.', '').isnumeric():
                        input_data['nm'].append(float(values['T2_wavelength'+str(i)]))
                    else:
                        T2_preview_status = False
                        break
            if not all(a > b for a, b in zip(input_data['nm'][1:], input_data['nm'])): # check for increasing
                T2_preview_status = False
            window['T2_preview'].update(disabled=not T2_preview_status)
            window['T2_process'].update(disabled=not T2_preview_status) if values['T2_folder'] != '' else window['T2_process'].update(disabled=True)
            
            if event in ('T2_preview', 'T2_process'):
                try:
                    input_data |= {
                        'vis': T2_vis,
                        'single': values['T2_single'],
                        'makebright': values['T2_makebright'],
                        'autoalign': values['T2_autoalign'],
                        'path': values['T2_path'],
                        'paths': [values['T2_path'+str(i)] for i in range(T2_vis)],
                        'exposures': [float(values['T2_exposure'+str(i)]) for i in range(T2_vis)],
                        'save': values['T2_folder'],
                        'preview': event=='T2_preview',
                        'area': T2_preview_area
                    }
                    T2_img = im.image_processing(input_data)
                    
                    if event == 'T2_preview':
                        window['T2_image'].update(data=im.convert_to_bytes(T2_img))
                except Exception:
                    sg.Print(traceback.format_exc(limit=0))
        
        # ------------ Events in the tab "Table" ------------

        elif values['-currentTab-'] == 'tab3':

            window['T3_process'].update(disabled = values['T3_folder']=='' or window['T3_database'].metadata==False)
            
            if event == 'T3_process':
                tg.generate_table(objectsDB, values['T3_tags'], albedoFlag, values['-srgb-'], values['-gamma-'], values['T3_folder'], values['T3_extension'], lang)
        
        # ------------ Events in the tab "Blackbody & Redshifts" ------------
        
        elif values['-currentTab-'] == 'tab4':
            
            if event == 'T4_maxtemp_num':
                window['T4_slider1'].update(range=(0, int(values['T4_maxtemp_num'])))

            elif event == 'T4_add':
                plot_data.append(T4_spectrum)
            
            elif event == 'T4_plot':
                pl.plot_spectra(plot_data, values['-gamma-'], values['-srgb-'], albedoFlag, lang)
            
            elif event == 'T4_clear':
                plot_data = []
            
            else:
                if event == 'T4_overexposure':
                    window['T4_mag'].update(text_color=text_colors[values['T4_overexposure']])
                    window['T4_slider4'].update(disabled=not values['T4_overexposure'])
                
                # Spectral data processing
                T4_spectrum = core.Spectrum.from_blackbody_redshift(core.visible_range, values['T4_slider1'], values['T4_slider2'], values['T4_slider3'])
                if values['T4_overexposure']:
                    T4_spectrum.br /= core.mag2irradiance(values['T4_slider4'], core.vega_in_V) * core.sun_in_V

                # Color calculation
                if values['-srgb-']:
                    T4_color = core.Color.from_spectrum(T4_spectrum, albedo=values['T4_overexposure'])
                else:
                    T4_color = core.Color.from_spectrum_legacy(T4_spectrum, albedo=values['T4_overexposure'])
                if values['-gamma-']:
                    T4_color = T4_color.gamma_corrected()
                T4_rgb = tuple(T4_color.to_bit(bitness).round(rounding))
                T4_rgb_show = T4_color.to_html()
            
                # Output
                window['T4_graph'].TKCanvas.itemconfig(T4_preview, fill=T4_rgb_show)
                window['T4_rgb'].update(T4_rgb)
                window['T4_hex'].update(T4_rgb_show)
        
        # ------------ Events in the tab "WIP" ------------
        
        elif values['-currentTab-'] == 'tab5':
            T5_image_flag = values['-typeImage-']

            if event in ('-typeSpectrum-', '-typeImage-'):
                for i in range(T5_num):
                    window['T5_path'+str(i)].update(visible=T5_image_flag)
                    window['T5_pathText'+str(i)].update(visible=T5_image_flag)
                    window['T5_brText'+str(i)].update(visible=not T5_image_flag)
                    window['T5_br'+str(i)].update(visible=not T5_image_flag)
            
            elif event.startswith('T5_filter') or event == '-srgb-':
                if values['-srgb-']:
                    T5_plot_data = [core.x, core.y, core.z]
                else:
                    T5_plot_data = [core.r, core.g, core.b]
                for i in range(T5_num):
                    T5_filter_name = values['T5_filter'+str(i)]
                    if T5_filter_name != '':
                        T5_filter = core.Spectrum.from_filter(T5_filter_name)
                        T5_plot_data.append(T5_filter)
                T5_fig.clf()
                T5_fig = pl.plot_filters(T5_plot_data)
                figure_canvas_agg.get_tk_widget().forget()
                figure_canvas_agg = pl.draw_figure(window['T5_canvas'].TKCanvas, T5_fig)

    window.close()


def export_colors(rgb: tuple):
    """ Generated formatted string of colors """
    lst = []
    mx = 0
    for i in rgb:
        lst.append(str(i))
        l = len(lst[-1])
        if l > mx:
            mx = l
    w = 8 if mx < 8 else mx+1
    return ''.join([i.ljust(w) for i in lst])