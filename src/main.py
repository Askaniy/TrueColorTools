""" Generates and launches a graphical interface that accesses other modules. """

import FreeSimpleGUI as sg
from sigfig import round as sigfig_round

from src.core import *
import src.gui as gui
import src.auxiliary as aux
import src.database as db
import src.image_processing as ip
from src.table_generator import generate_table
import src.plotter as pl
import src.strings as tr


def launch_window(lang: str):

    # Databases declaration
    database_folders = ('spectra', 'spectra_extras')
    objectsDB, refsDB = {}, {}
    tagsDB = []
    filtersDB = db.list_filters()

    # Processing configuration
    default_tag = 'featured'
    srgb = True   # default color space
    brMax = False # albedo/chromaticity mode switcher
    brGeom = True # default albedo type (True==geometrical, False==spherical)
    bitness = 1
    rounding = 3

    # GUI configuration
    T2_num = 8 # max number of image bands
    T2_vis = T2_num # current number of visible image bands
    circle_r = 100 # radius in pixels of color preview circle
    circle_coord = (circle_r, circle_r+1)
    circle_size = (2*circle_r+1, 2*circle_r+1)
    img_preview_size = (256, 128)
    img_preview_area = img_preview_size[0] * img_preview_size[1]
    text_colors = (gui.muted_color, gui.text_color)
    window0_size = (1120, 640)

    # Plots configuration
    spectra_dpi = 100
    spectra_plot_size = (1000, 500)
    spectra_figsize = (spectra_plot_size[0] / spectra_dpi, spectra_plot_size[1] / spectra_dpi)
    filters_dpi = 90
    filters_plot_size = (500, 200)
    filters_figsize = (filters_plot_size[0] / filters_dpi, filters_plot_size[1] / filters_dpi)

    # Loading the icon
    with open('src/window/icon', 'rb') as file:
        icon = file.read()

    # Loading the window 0 title
    with open('src/window/title.txt', 'rb') as file:
        window0_title = file.readline().decode().strip()

    # Launching the main window
    sg.theme('MaterialDark')
    window0 = sg.Window(
        title=window0_title, size=window0_size, icon=icon, finalize=True, resizable=True, margins=(0, 0),
        layout=gui.generate_layout(
            circle_size, filters_plot_size, img_preview_size, text_colors, filtersDB, srgb, brMax, brGeom, bitness, rounding, T2_num, lang
        )
    )
    # Creating the plot window stub
    window1 = None

    # Connection to the parallel thread of image processing
    T2_logger = gui.create_logger(window0, 'T2_thread')

    # Setting default color preview circle
    T1_preview = window0['T1_graph'].DrawCircle(circle_coord, circle_r, fill_color='black', line_color=None)
    T3_preview = window0['T3_graph'].DrawCircle(circle_coord, circle_r, fill_color='black', line_color=None)

    # Setting plots templates
    light_theme = False
    plot_data = [] # for tabs 1 and 3, both at once
    mean_spectrum = [] # for tab 2

    # Default values to avoid errors
    T1_obj_name = T1_spectrum = T3_obj_name = T3_spectrum = None
    T1_albedo_note = tr.gui_blank_note

    def T1_T3_update_plot(fig, fig_canvas_agg, current_tab, gamma: bool, srgb: bool, albedo: bool, light_theme: bool, lang: str):
        pl.close_figure(fig)
        fig_canvas_agg.get_tk_widget().forget()
        to_plot = deepcopy(plot_data)
        if current_tab == 'tab1' and T1_obj_name and T1_spectrum not in to_plot:
            to_plot.append(T1_spectrum)
        if current_tab == 'tab3' and T3_obj_name and T3_spectrum not in to_plot:
            to_plot.append(T3_spectrum)
        fig = pl.plot_spectra(to_plot, gamma, srgb, albedo, light_theme, lang, spectra_figsize, spectra_dpi)
        fig_canvas_agg = pl.draw_figure(window1['W1_canvas'].TKCanvas, fig)
        return fig, fig_canvas_agg
    
    # List of events that cause color recalculation
    T1_triggers = ('-gamma-', '-srgb-', '-brMax-', '-brMode1-', '-brMode2-', '-bitness-', '-rounding-', 'T1_list', 'T1_filter')
    T3_triggers = ('-gamma-', '-srgb-', '-brMax-', '-bitness-', '-rounding-', 'T3_slider1', 'T3_slider2', 'T3_slider3', 'T3_slider4')

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
        elif isinstance(event, str) and event.endswith('plot'):
            if not window1:
                window1 = sg.Window(
                    tr.spectral_plot[lang], gui.generate_plot_layout(lang, spectra_plot_size, light_theme), icon=icon,
                    finalize=True, element_justification='center'
                )
            else:
                pl.close_figure(T1_T3_fig)
                T1_T3_fig_canvas_agg.get_tk_widget().forget()
            to_plot = deepcopy(plot_data)
            if T1_obj_name and T1_spectrum not in to_plot:
                to_plot.append(T1_spectrum)
            if T3_obj_name and T3_spectrum not in to_plot:
                to_plot.append(T3_spectrum)
            T1_T3_fig = pl.plot_spectra(to_plot, values['-gamma-'], values['-srgb-'], values['-brMax-'],
                                        light_theme, lang, spectra_figsize, spectra_dpi)
            T1_T3_fig_canvas_agg = pl.draw_figure(window1['W1_canvas'].TKCanvas, T1_T3_fig)
        elif event == 'W1_path':
            T1_T3_fig.savefig(values['W1_path'], dpi=133.4) # 1200x800
        elif event == 'W1_light_theme':
            light_theme = values['W1_light_theme']
            T1_T3_fig, T1_T3_fig_canvas_agg = T1_T3_update_plot(
                T1_T3_fig, T1_T3_fig_canvas_agg,
                window0.ReturnValuesDictionary['-currentTab-'],
                window0.ReturnValuesDictionary['-gamma-'],
                window0.ReturnValuesDictionary['-srgb-'],
                window0.ReturnValuesDictionary['-brMax-'],
                light_theme, lang
            )

        # Run-time translation
        elif event in tr.langs.keys():
            lang = tr.langs[event]
            window0 = gui.translate_win0(window0, T1_albedo_note, T2_vis, lang)
            match values['-currentTab-']:
                case 'tab1':
                    if T1_obj_name:
                        window['T1_title2'].update(T1_obj_name.indexed_name(lang))
                    T1_displayed_namesDB = db.obj_names_dict(objectsDB, values['T1_tags'], lang)
                    if T1_obj_name:
                        T1_index = tuple(T1_displayed_namesDB.keys()).index(T1_obj_name(lang))
                        window['T1_list'].update(tuple(T1_displayed_namesDB.keys()), set_to_index=T1_index, scroll_to_index=T1_index)
                    else:
                        window['T1_list'].update(tuple(T1_displayed_namesDB.keys()))
                case 'tab3':
                    if T3_obj_name:
                        window['T3_title2'].update(T3_obj_name.indexed_name(lang))
            if window1:
                window1 = gui.translate_win1(window1, lang)
                T1_T3_fig, T1_T3_fig_canvas_agg = T1_T3_update_plot(
                    T1_T3_fig, T1_T3_fig_canvas_agg,
                    window0.ReturnValuesDictionary['-currentTab-'],
                    window0.ReturnValuesDictionary['-gamma-'],
                    window0.ReturnValuesDictionary['-srgb-'],
                    window0.ReturnValuesDictionary['-brMax-'],
                    light_theme, lang
                )
        
        # Only the main window events
        if window is window0:

            # ------------ Global window events ------------
            
            if event == tr.gui_ref[lang]:
                if len(refsDB) == 0:
                    sg.popup(tr.gui_no_data_message[lang], title=event, icon=icon, non_blocking=True)
                else:
                    to_show = ''
                    for key, value in refsDB.items():
                        to_show += f'"{key}": {value[0]}\n'
                        for info in value[1:]:
                            to_show += info + '\n'
                        to_show += '\n'
                    sg.popup_scrolled(to_show, title=event, size=(150, 25), icon=icon, non_blocking=True)
            
            elif event == tr.gui_info[lang]:
                sg.popup(f'{tr.link}\n{tr.auth_info[lang]}', title=event, icon=icon, non_blocking=True)
            
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
                is1tab = values['-currentTab-'] == 'tab1'
                not2tab = values['-currentTab-'] != 'tab2'
                window['-brMode1-'].update(visible=is1tab)
                window['-brMode2-'].update(visible=is1tab)
                window['-formattingText-'].update(visible=not2tab)
                window['-bitnessText-'].update(visible=not2tab)
                window['-roundingText-'].update(visible=not2tab)
                window['-bitness-'].update(visible=not2tab)
                window['-rounding-'].update(visible=not2tab)

            # ------------ Events in the tab "Database viewer" ------------

            if values['-currentTab-'] == 'tab1':
                
                if event in ('T1_load', 'T1_reload'):
                    # Loading of the spectra database

                    objectsDB, refsDB = db.import_DBs(database_folders)
                    tagsDB = db.tag_list(objectsDB)
                    namesDB = { # TODO: generalize!
                        'en': db.obj_names_dict(objectsDB, 'ALL', 'en'),
                        'ru': db.obj_names_dict(objectsDB, 'ALL', 'ru'),
                        'de': db.obj_names_dict(objectsDB, 'ALL', 'de')
                    }

                    if event == 'T1_load':
                        # Enable database view elements
                        window['T1_header_space'].update(visible=False)
                        window['T1_load'].update(tr.gui_load[lang], visible=False)
                        window['T1_tagsN'].update(visible=True)
                        window['T1_tags'].update(default_tag, values=tagsDB, visible=True)
                        T1_displayed_namesDB = db.obj_names_dict(objectsDB, default_tag, lang)
                        window['T1_list'].update(values=tuple(T1_displayed_namesDB.keys()), visible=True)
                        window['T1_reload'].update(tr.gui_reload[lang], visible=True)
                    else:
                        # Updating tags on reload
                        if values['T1_tags'] in tagsDB:
                            window['T1_tags'].update(values['T1_tags'], values=tagsDB)
                        else:
                            window['T1_tags'].update(default_tag, values=tagsDB)
                            T1_displayed_namesDB = db.obj_names_dict(objectsDB, default_tag, lang)
                            window['T1_list'].update(values=tuple(T1_displayed_namesDB.keys()))

                elif event in T1_triggers and values['T1_list'] != []:

                    # for green Dinkinesh Easter egg
                    last_click_was_Dinkinesh = event == 'T1_list' and T1_spectrum is not None and T1_spectrum.name.name() == 'Dinkinesh'

                    T1_obj_name = namesDB[lang][values['T1_list'][0]]
                    window['T1_title2'].update(T1_obj_name.indexed_name(lang))

                    # Spectral data import and processing
                    T1_body = database_parser(T1_obj_name, objectsDB[T1_obj_name])
                    T1_spectrum, T1_estimated = T1_body.get_spectrum('geometric' if values['-brMode1-'] else 'spherical')
                    
                    # Setting of notes
                    T1_albedo_note = tr.gui_blank_note
                    if not values['-brMax-']:
                        match T1_estimated:
                            case None:
                                if isinstance(T1_body, ReflectingBody):
                                    T1_albedo_note = tr.gui_no_albedo
                            case True:
                                T1_albedo_note = tr.gui_estimated
                    window['T1_albedo_note'].update(T1_albedo_note[lang])

                    # Color calculation
                    T1_maximize_br = values['-brMax-'] or T1_estimated is None
                    T1_color = ColorPoint.from_spectral_data(T1_spectrum, T1_maximize_br, values['-srgb-'])
                    if values['-gamma-']:
                        T1_color = T1_color.gamma_corrected()
                    T1_rgb = tuple(T1_color.to_bit(bitness).round(rounding))
                    T1_rgb_show = T1_color.to_html()

                    # Output
                    window['T1_graph'].TKCanvas.itemconfig(T1_preview, fill=T1_rgb_show)
                    window['T1_rgb'].update(T1_rgb)
                    window['T1_hex'].update(T1_rgb_show)
                    T1_value, T1_sd = T1_spectrum @ get_filter(values['T1_filter'])
                    if T1_sd is None:
                        window['T1_convolved'].update(sigfig_round(T1_value, rounding, warn=False))
                    else:
                        window['T1_convolved'].update(sigfig_round(T1_value, uncertainty=T1_sd, warn=False))


                    # Green Dinkinesh Easter egg (added by request)
                    # There was a bug in TCT v3.3 caused by upper limit of uint16 when squaring nm for AB calibration
                    if last_click_was_Dinkinesh and T1_spectrum.name.name() == 'Dinkinesh':
                        window['T1_graph'].TKCanvas.itemconfig(T1_preview, fill='#7f9000')
                        window['T1_albedo_note'].update('Easter egg! Values below are correct.')

                    # Dynamical plotting
                    if window1:
                        T1_T3_fig, T1_T3_fig_canvas_agg = T1_T3_update_plot(
                            T1_T3_fig, T1_T3_fig_canvas_agg,
                            window0.ReturnValuesDictionary['-currentTab-'],
                            window0.ReturnValuesDictionary['-gamma-'],
                            window0.ReturnValuesDictionary['-srgb-'],
                            window0.ReturnValuesDictionary['-brMax-'],
                            light_theme, lang
                        )
                
                elif event == 'T1_tags':
                    T1_displayed_namesDB = db.obj_names_dict(objectsDB, values['T1_tags'], lang)
                    window['T1_list'].update(tuple(T1_displayed_namesDB.keys()))
                
                elif event == 'T1_pin' and values['T1_list'] != []:
                    if T1_spectrum not in plot_data:
                        plot_data.append(T1_spectrum)
                
                elif event == 'T1_clear':
                    plot_data = []
                    if window1:
                        T1_T3_fig, T1_T3_fig_canvas_agg = T1_T3_update_plot(
                            T1_T3_fig, T1_T3_fig_canvas_agg,
                            window0.ReturnValuesDictionary['-currentTab-'],
                            window0.ReturnValuesDictionary['-gamma-'],
                            window0.ReturnValuesDictionary['-srgb-'],
                            window0.ReturnValuesDictionary['-brMax-'],
                            light_theme, lang
                        )
                
                elif event == 'T1_export2text':
                    if len(objectsDB) == 0:
                        sg.popup(tr.gui_no_data_message[lang], title=tr.gui_output[lang], icon=icon, non_blocking=True)
                    else:
                        T1_export = '\n' + '\t'.join(tr.gui_col[lang]) + '\n' + '_' * 36
                        for obj_name in T1_displayed_namesDB.values():
                            T1_body = database_parser(obj_name, objectsDB[obj_name])
                        
                            # Setting brightness mode
                            T1_spectrum, T1_estimated = T1_body.get_spectrum('geometric' if values['-brMode1-'] else 'spherical')

                            # Color calculation
                            T1_maximize_br = values['-brMax-'] or T1_estimated is None
                            T1_color = ColorPoint.from_spectral_data(T1_spectrum, T1_maximize_br, values['-srgb-'])
                            if values['-gamma-']:
                                T1_color = T1_color.gamma_corrected()
                            T1_rgb = tuple(T1_color.to_bit(bitness).round(rounding))

                            # Output
                            T1_export += f'\n{aux.export_colors(T1_rgb)}\t{obj_name(lang)}'
                            if T1_estimated:
                                T1_export += f'; {tr.gui_estimated[lang]}'

                        sg.popup_scrolled(
                            T1_export, title=tr.gui_output[lang], size=(100, max(10, min(30, 3+len(objectsDB)))),
                            font=('Consolas', 10), icon=icon, non_blocking=True
                        )
                
                elif event == 'T1_folder':
                    if len(objectsDB) == 0:
                        sg.popup(tr.gui_no_data_message[lang], title=tr.gui_output[lang], icon=icon, non_blocking=True)
                    else:
                        generate_table(
                            objectsDB, values['T1_tags'], values['-brMax-'], values['-brMode1-'],
                            values['-srgb-'], values['-gamma-'], values['T1_folder'], 'png', lang
                        )
            
            # ------------ Events in the tab "Image processing" ------------
            
            elif values['-currentTab-'] == 'tab2':

                # Getting input data mode name
                T2_mode = aux.get_flag_index((values['-typeImage-'], values['-typeImageRGB-'], values['-typeImageCube-']))

                if T2_mode == 2:
                    # No visible frames in spectral cube mode
                    window['T2_frames'].update(visible=False)
                else:
                    # The number of visible frames for RGB image (T2_mode==1) is 3,
                    # otherwise all possible frames are displayed
                    window['T2_frames'].update(visible=True)
                    T2_vis = 3 if T2_mode else T2_num
                    # Setting the visibility and elements
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
                            px_lower_limit=img_preview_area,
                            px_upper_limit=int(float(values['T2_chunks']) * 1e6), # megapixels to pixels
                            single_file=values['T2_path'],
                            files=T2_files,
                            filters=T2_filters,
                            formulas=T2_formulas,
                            gamma_correction=values['-gamma-'],
                            srgb=values['-srgb-'],
                            maximize_brightness=values['-brMax-'],
                            desun=values['T2_desun'],
                            photons=values['T2_photons'],
                            factor=float(values['T2_factor']),
                            upscale=values['T2_upscale'],
                            log=T2_logger
                        ),
                        ('T2_thread', 'End of the image processing thread\n')
                    )
                
                # Getting messages from image processing thread
                elif event[0] == 'T2_thread':
                    sg.easy_print(event[1]) # pop-up printing
                    if values[event] is not None:
                        # Updating preview image
                        window['T2_image'].update(data=ip.convert_to_bytes(values[event]))
                
                # Updating filters profile plot
                if (isinstance(event, str) and event.startswith('T2_filter')) or (event[0] == 'T2_thread' and values[event] is not None) or event in ('-currentTab-', '-srgb-'):
                    try:
                        pl.close_figure(T2_fig)
                        T2_to_plot = [*T2_filters, *mean_spectrum]
                        T2_fig = pl.plot_filters(T2_to_plot, values['-srgb-'], lang, filters_figsize, filters_dpi)
                        T2_fig_canvas_agg.get_tk_widget().forget()
                        T2_fig_canvas_agg = pl.draw_figure(window['T2_canvas'].TKCanvas, T2_fig)
                    except UnboundLocalError: # means it's the first tab opening
                        T2_fig = pl.plot_filters((), values['-srgb-'], lang, filters_figsize, filters_dpi)
                        T2_fig_canvas_agg = pl.draw_figure(window['T2_canvas'].TKCanvas, T2_fig)

            
            # ------------ Events in the tab "Blackbody & Redshifts" ------------
            
            elif values['-currentTab-'] == 'tab3':
                
                if event in T3_triggers:
                    if event == '-brMax-':
                        window['T3_mag'].update(text_color=text_colors[not values['-brMax-']])
                        window['T3_slider4'].update(disabled=values['-brMax-'])
                    
                    # Spectral data processing
                    T3_spectrum = Spectrum.from_blackbody_redshift(visible_range, values['T3_slider1'], values['T3_slider2'], values['T3_slider3'])
                    T3_obj_name = T3_spectrum.name
                    window['T3_title2'].update(T3_obj_name.indexed_name(lang))

                    # Mode with "exposure"
                    if not values['-brMax-']:
                        T3_spectrum.br /= aux.mag2irradiance(values['T3_slider4'], vega_in_V) * sun_in_V

                    # Color calculation
                    T3_color = ColorPoint.from_spectral_data(T3_spectrum, values['-brMax-'], values['-srgb-'])
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
                            T1_T3_fig, T1_T3_fig_canvas_agg,
                            window0.ReturnValuesDictionary['-currentTab-'],
                            window0.ReturnValuesDictionary['-gamma-'],
                            window0.ReturnValuesDictionary['-srgb-'],
                            window0.ReturnValuesDictionary['-brMax-'],
                            light_theme, lang
                        )
                
                elif event == 'T3_maxtemp_num':
                    window['T3_slider1'].update(range=(0, int(values['T3_maxtemp_num'])))
                
                elif event == 'T3_pin':
                    if T3_spectrum not in plot_data:
                        plot_data.append(T3_spectrum)
                
                elif event == 'T3_clear':
                    plot_data = []
                    if window1:
                        T1_T3_fig, T1_T3_fig_canvas_agg = T1_T3_update_plot(
                            T1_T3_fig, T1_T3_fig_canvas_agg,
                            window0.ReturnValuesDictionary['-currentTab-'],
                            window0.ReturnValuesDictionary['-gamma-'],
                            window0.ReturnValuesDictionary['-srgb-'],
                            window0.ReturnValuesDictionary['-brMax-'],
                            light_theme, lang
                        )
