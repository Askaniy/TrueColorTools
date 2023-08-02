import io
import time
import numpy as np
import PySimpleGUI as sg
from PIL import Image, ImageDraw
import src.core as core
import src.gui as gui
import src.filters as filters
import src.calculations as calc
import src.data_import as di
import src.plotter as pl
import src.strings as tr
import src.table_generator as tg
import src.experimental


def convert_to_bytes(img: Image.Image):
    """ Prepares PIL's image to be displayed in the window """
    bio = io.BytesIO()
    img.save(bio, format='png')
    del img
    return bio.getvalue()

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

def launch_window():
    lang = 'en' # can be translated into German or Russian at runtime
    debug = False
    objectsDB, refsDB = {}, {} # initial loading became too long with separate json5 database files
    tagsDB = []
    default_tag = 'featured'
    filtersDB = di.list_filters()

    circle_r = 100 # radius in pixels of color preview circle
    circle_coord = (circle_r, circle_r+1)
    T2_preview = (256, 128)
    T2_area = T2_preview[0]*T2_preview[1]
    text_colors = (gui.muted_color, gui.text_color)

    sg.ChangeLookAndFeel('MaterialDark')
    window = sg.Window(
        'True Color Tools', gui.generate_layout((2*circle_r+1, 2*circle_r+1), T2_preview, text_colors, filtersDB, lang),
        finalize=True, resizable=True, margins=(0, 0), size=(900, 600))
    T2_vis = 3  # current number of visible image bands
    T2_num = 10 # max number of image bands, ~ len(window['T2_frames'])
    T5_num = 8
    for i in range(T2_vis, T2_num):
        window['T2_band'+str(i)].update(visible=False)

    T1_preview = window['T1_graph'].DrawCircle(circle_coord, circle_r, fill_color='black', line_color=None)
    T4_preview = window['T4_graph'].DrawCircle(circle_coord, circle_r, fill_color='black', line_color=None)

    triggers = ['-gamma-', '-srgb-', '-brMode0-', '-brMode1-', '-interpMode0-', '-interpMode1-', '-bitness-', '-rounding-']
    
    albedoFlag = True # default brightness mode
    interpMode = calc.interp_modes[0] # default interpolation mode
    bitness = int(window['-bitness-'].get())
    rounding = int(window['-rounding-'].get())

    T1_plot_data = []
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
        elif event in ('-interpMode0-', '-interpMode1-'):
            for i in range(2):
                if values[f'-interpMode{i}-']:
                    interpMode = calc.interp_modes[i]
                    break
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

                # Spectral data import and processing
                T1_spectrum = objectsDB[di.obj_dict(objectsDB, 'all', lang)[T1_name]]
                T1_albedo = albedoFlag
                if T1_albedo:
                    try:
                        T1_albedo = T1_spectrum['albedo']
                    except KeyError:
                        T1_albedo = False
                        T1_spectrum |= {'albedo': False}
                T1_spectrum = calc.standardize_photometry(T1_spectrum)
                T1_spectrum |= calc.matching_check(T1_name, T1_spectrum)
                
                # Spectrum interpolation
                try:
                    T1_sun = T1_spectrum['sun']
                except KeyError:
                    T1_sun = False
                T1_curve = calc.polator(T1_spectrum['nm'], T1_spectrum['br'], calc.rgb_nm, T1_albedo, mode=interpMode, desun=T1_sun)
                
                # Color calculation
                T1_spec = core.Spectrum(T1_name, calc.rgb_nm, T1_curve)
                if values['-srgb-']:
                    T1_color = core.Color.from_spectrum(T1_spec, T1_albedo)
                else:
                    T1_color = core.Color.from_spectrum_legacy(T1_spec, T1_albedo)
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
                T1_plot_data.append(T1_spec)
            
            elif event == 'T1_plot':
                pl.plot_spectra(T1_plot_data, values['-gamma-'], values['-srgb-'], albedoFlag, lang)
            
            elif event == 'T1_clear':
                T1_plot_data = []
            
            elif event == 'T1_export':
                T1_export = '\n' + '\t'.join(tr.gui_col[lang]) + '\n' + '_' * 36
                
                # Spectrum processing
                for name, raw_name in di.obj_dict(objectsDB, values['T1_tags'], lang).items():
                    T1_spectrum = objectsDB[raw_name]
                    T1_albedo = albedoFlag
                    if T1_albedo:
                        try:
                            T1_albedo = T1_spectrum['albedo']
                        except KeyError:
                            T1_albedo = False
                            T1_spectrum |= {'albedo': False}
                    T1_spectrum = calc.standardize_photometry(T1_spectrum)
                    T1_spectrum |= calc.matching_check(T1_name, T1_spectrum)
                    
                    # Spectrum interpolation
                    try:
                        T1_sun = T1_spectrum['sun']
                    except KeyError:
                        T1_sun = False
                    T1_curve = calc.polator(T1_spectrum['nm'], T1_spectrum['br'], calc.rgb_nm, T1_albedo, mode=interpMode, desun=T1_sun)

                    # Color calculation
                    T1_spec = core.Spectrum(T1_name, calc.rgb_nm, T1_curve)
                    if values['-srgb-']:
                        T1_color = core.Color.from_spectrum(T1_spec, T1_albedo)
                    else:
                        T1_color = core.Color.from_spectrum_legacy(T1_spec, T1_albedo)
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
                    window['T2_exposure'+str(i)].update(disabled=values['T2_single'])
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
                window['T2_exposureN'+str(i)].update(text_color=text_colors[not values['T2_single']])
            
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

                T2_time = time.monotonic()
                T2_load = []

                if values['T2_single']:
                    T2_rgb_img = Image.open(values['T2_path'])
                    if T2_rgb_img.mode == 'P': # NameError if color is indexed
                        T2_rgb_img = T2_rgb_img.convert('RGB')
                        sg.Print('Note: image converted from "P" (indexed color) mode to "RGB"')
                    if event == 'T2_preview':
                        T2_ratio = T2_rgb_img.width / T2_rgb_img.height
                        T2_rgb_img = T2_rgb_img.resize((int(np.sqrt(T2_area*T2_ratio)), int(np.sqrt(T2_area/T2_ratio))), resample=Image.Resampling.HAMMING)
                    if len(T2_rgb_img.getbands()) == 3:
                        r, g, b = T2_rgb_img.split()
                        a = None
                    elif len(T2_rgb_img.getbands()) == 4:
                        r, g, b, a = T2_rgb_img.split()
                    for i in [b, g, r]:
                        T2_load.append(np.array(i))
                else:
                    T2_exposures = [float(values['T2_exposure'+str(i)]) for i in range(T2_vis)]
                    T2_max_exposure = max(T2_exposures)
                    for i in range(T2_vis):
                        T2_bw_img = Image.open(values['T2_path'+str(i)])
                        if T2_bw_img.mode not in ('L', 'I', 'F'): # image should be b/w
                            sg.Print(f'Note: image of band {i+1} converted from "{T2_bw_img.mode}" mode to "L"')
                            T2_bw_img = T2_bw_img.convert('L')
                        if i == 0:
                            T2_size = T2_bw_img.size
                        else:
                            if T2_size != T2_bw_img.size:
                                sg.Print(f'Note: image of band {i+1} resized from {T2_bw_img.size} to {T2_size}')
                                T2_bw_img = T2_bw_img.resize(T2_size)
                        if event == 'T2_preview':
                            T2_ratio = T2_bw_img.width / T2_bw_img.height
                            T2_bw_img = T2_bw_img.resize((int(np.sqrt(T2_area*T2_ratio)), int(np.sqrt(T2_area/T2_ratio))), resample=Image.Resampling.HAMMING)
                        T2_load.append(np.array(T2_bw_img) / T2_exposures[i] * T2_max_exposure)
                
                T2_data = np.array(T2_load, 'int64')
                T2_l, T2_h, T2_w = T2_data.shape
                
                if values['T2_autoalign']:
                    T2_data = src.experimental.autoalign(T2_data, debug)
                    T2_l, T2_h, T2_w = T2_data.shape
                
                T2_data = T2_data.astype('float32')
                T2_max = T2_data.max()
                if values['T2_makebright']:
                    T2_data *= 65500 / T2_max
                    T2_input_bit = 16
                    T2_input_depth = 65535
                else:
                    T2_input_bit = 16 if T2_max > 255 else 8
                    T2_input_depth = 65535 if T2_max > 255 else 255
                #T2_data = np.clip(T2_data, 0, T2_input_depth)

                T2_img = Image.new('RGB', (T2_w, T2_h), (0, 0, 0))
                T2_draw = ImageDraw.Draw(T2_img)
                T2_counter = 0
                T2_px_num = T2_w*T2_h
                
                #if values['T2_plotpixels']:
                #    T2_fig = go.Figure()
                #    T2_fig.update_layout(title=tr.map_title_text[lang], xaxis_title=tr.xaxis_text[lang], yaxis_title=tr.yaxis_text[lang])

                sg.Print(f'\n{round(time.monotonic() - T2_time, 3)} seconds for loading, autoalign and creating output templates\n')
                sg.Print(f'{time.strftime("%H:%M:%S")} 0%')

                T2_time = time.monotonic()
                T2_get_spectrum_time = 0
                T2_calc_polator_time = 0
                T2_calc_rgb_time = 0
                T2_draw_point_time = 0
                T2_plot_pixels_time = 0
                T2_progress_bar_time = 0

                for x in range(T2_w):
                    for y in range(T2_h):

                        T2_temp_time = time.monotonic_ns()
                        T2_spectrum = T2_data[:, y, x]
                        T2_get_spectrum_time += time.monotonic_ns() - T2_temp_time

                        if np.sum(T2_spectrum) > 0:
                            T2_name = f'({x}; {y})'

                            T2_temp_time = time.monotonic_ns()
                            T2_curve = calc.polator(input_data['nm'], list(T2_spectrum), calc.rgb_nm, mode=interpMode, desun=input_data['desun'])
                            T2_calc_polator_time += time.monotonic_ns() - T2_temp_time

                            T2_temp_time = time.monotonic_ns()
                            T2_rgb = calc.to_rgb(T2_name, T2_curve, albedo=True, inp_bit=T2_input_bit, exp_bit=8, gamma=input_data['gamma'])
                            T2_calc_rgb_time += time.monotonic_ns() - T2_temp_time

                            T2_temp_time = time.monotonic_ns()
                            T2_draw.point((x, y), T2_rgb)
                            T2_draw_point_time += time.monotonic_ns() - T2_temp_time

                            #if values['T2_plotpixels']:
                            #    T2_temp_time = time.monotonic_ns()
                            #    if x % 32 == 0 and y % 32 == 0:
                            #        T2_fig.add_trace(go.Scatter(
                            #            x = calc.rgb_nm,
                            #            y = T2_curve,
                            #            name = T2_name,
                            #            line = dict(color='rgb'+str(T2_rgb), width=2)
                            #            ))
                            #    T2_plot_pixels_time += time.monotonic_ns() - T2_temp_time
                        
                        T2_temp_time = time.monotonic_ns()
                        T2_counter += 1
                        if T2_counter % 2048 == 0:
                            try:
                                sg.Print(f'{time.strftime("%H:%M:%S")} {round(T2_counter/T2_px_num * 100)}%, {round(T2_counter/(time.monotonic()-T2_time))} px/sec')
                            except ZeroDivisionError:
                                sg.Print(f'{time.strftime("%H:%M:%S")} {round(T2_counter/T2_px_num * 100)}% (ZeroDivisionError)')
                        T2_progress_bar_time += time.monotonic_ns() - T2_temp_time
                
                T2_end_time = time.monotonic()
                sg.Print(f'\n{round(T2_end_time - T2_time, 3)} seconds for color processing, where:')
                sg.Print(f'\t{T2_get_spectrum_time / 1e9} for getting spectrum')
                sg.Print(f'\t{T2_calc_polator_time / 1e9} for inter/extrapolating')
                sg.Print(f'\t{T2_calc_rgb_time / 1e9} for color calculating')
                sg.Print(f'\t{T2_draw_point_time / 1e9} for pixel drawing')
                sg.Print(f'\t{T2_plot_pixels_time / 1e9} for adding spectrum to plot')
                sg.Print(f'\t{T2_progress_bar_time / 1e9} for progress bar')
                sg.Print(f'\t{round(T2_end_time-T2_time-(T2_get_spectrum_time+T2_calc_polator_time+T2_calc_rgb_time+T2_draw_point_time+T2_plot_pixels_time+T2_progress_bar_time)/1e9, 3)} for other (time, black-pixel check)')
                
                #if values['T2_plotpixels']:
                #    T2_fig.show()
                if event == 'T2_preview':
                    window['T2_image'].update(data=convert_to_bytes(T2_img))
                else:
                    T2_img.save(f'{values["T2_folder"]}/TCT_{time.strftime("%Y-%m-%d_%H-%M")}.png')
        
        # ------------ Events in the tab "Table" ------------

        elif values['-currentTab-'] == 'tab3':

            window['T3_process'].update(disabled = values['T3_folder']=='' or window['T3_database'].metadata==False)
            
            if event == 'T3_process':
                tg.generate_table(objectsDB, values['T3_tags'], albedoFlag, values['-srgb-'], values['-gamma-'], values['T3_folder'], values['T3_extension'], lang)

        
        # ------------ Events in the tab "Blackbody & Redshifts" ------------
        
        elif values['-currentTab-'] == 'tab4':
            
            if event == 'T4_maxtemp_num':
                window['T4_slider1'].update(range=(0, int(values['T4_maxtemp_num'])))
            
            else:
                if event == 'T4_surfacebr':
                    window['T4_scale'].update(text_color=text_colors[values['T4_surfacebr']])
                    window['T4_slider4'].update(disabled=not values['T4_surfacebr'])
                
                T4_curve = calc.blackbody_redshift(calc.rgb_nm, values['T4_slider1'], values['T4_slider2'], values['T4_slider3'])
                if values['T4_surfacebr']:
                    try:
                        T4_curve /= calc.mag2intensity(values['T4_slider4'])
                    except np.core._exceptions.UFuncTypeError:
                        pass
                T4_name = f'{values["T4_slider1"]} {values["T4_slider2"]} {values["T4_slider3"]}'

                # Color calculation
                T4_spec = core.Spectrum(T4_name, calc.rgb_nm, T4_curve)
                if values['-srgb-']:
                    T4_color = core.Color.from_spectrum(T4_spec)
                else:
                    T4_color = core.Color.from_spectrum_legacy(T4_spec)
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
                        T5_filter = di.import_filter(T5_filter_name)
                        T5_plot_data.append(T5_filter)
                T5_fig.clf()
                T5_fig = pl.plot_filters(T5_plot_data)
                figure_canvas_agg.get_tk_widget().forget()
                figure_canvas_agg = pl.draw_figure(window['T5_canvas'].TKCanvas, T5_fig)

    window.close()