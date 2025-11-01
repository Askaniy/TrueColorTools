""" Generates and launches a graphical interface that accesses other modules. """

import FreeSimpleGUI as sg
from sigfig import round as sigfig_round
from copy import deepcopy
from time import strftime
import numpy as np

from src.core import Spectrum, ReflectingBody, ColorSystem, ColorPoint, FilterNotFoundError, \
    visible_range, sun_in_V, get_filter, database_parser
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
    namesDB = {}
    tagsDB = []
    filtersDB: tuple[str, ...] = db.list_filters()

    # Processing configuration
    default_tag = 'featured'
    default_color_space = 'sRGB'
    default_white_point = 'Illuminant E'
    color_system = ColorSystem(default_color_space, default_white_point)
    default_gamma_correction = True
    brMax = False # albedo/chromaticity mode switcher
    brGeom = True # default albedo type (True==geometrical, False==spherical)
    bitness = 1
    rounding = 3

    # GUI configuration
    tab2_num = 8 # max number of image bands
    tab2_vis = 3 # current number of visible image bands
    tab2_mode = 1 # default mode of the Tab 2 input data
    circle_r = 100 # radius in pixels of color preview circle
    circle_coord = (circle_r, circle_r+1)
    circle_size = (2*circle_r+1, 2*circle_r+1)
    img_preview_size = (256, 128)
    img_preview_area = img_preview_size[0] * img_preview_size[1]
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
            circle_size, filters_plot_size, img_preview_size, filtersDB,
            default_color_space, default_white_point, default_gamma_correction,
            brMax, brGeom, bitness, rounding, tab2_num, lang
        )
    )
    # Creating the plot window stub
    window1 = None

    # Connection to the parallel thread of image processing
    tab2_logger = gui.create_logger(window0, 'tab2_thread')

    # Setting default color preview circle
    tab1_preview = window0['tab1_graph'].DrawCircle(circle_coord, circle_r, fill_color='black', line_color=None)
    tab3_preview = window0['tab3_graph'].DrawCircle(circle_coord, circle_r, fill_color='black', line_color=None)

    # Setting plots templates
    limit_to_vis = False
    normalize_at_550nm = False
    light_theme = False
    pinned_spectra_and_colors = {} # for tabs 1 and 3, both at once
    mean_spectrum = [] # for tab 2

    # Default values to avoid errors
    tab1_obj_name = tab1_html = tab1_spectrum = None
    tab1_albedo_note = tr.gui_blank_note
    tab2_preview = None
    tab2_filters = []
    tab2_filters_checklist = np.zeros(tab2_num, dtype='bool')
    tab2_filters_were_updated = False
    tab3_obj_name = tab3_html = tab3_spectrum = None

    def tab1_tab3_update_plot(fig, fig_canvas_agg, current_tab, limit_to_vis, normalize_at_550nm, light_theme: bool, lang: str):
        pl.close_figure(fig)
        fig_canvas_agg.get_tk_widget().forget()
        dict_to_plot = deepcopy(pinned_spectra_and_colors)
        if current_tab == 'tab1' and tab1_obj_name and tab1_spectrum not in dict_to_plot:
            dict_to_plot |= {tab1_spectrum: tab1_html}
        if current_tab == 'tab3' and tab3_obj_name and tab3_spectrum not in dict_to_plot:
            dict_to_plot |= {tab3_spectrum: tab3_html}
        fig = pl.plot_spectra(dict_to_plot, limit_to_vis, normalize_at_550nm, light_theme, lang, spectra_figsize, spectra_dpi)
        fig_canvas_agg = pl.draw_figure(window1['W1_canvas'].TKCanvas, fig)
        return fig, fig_canvas_agg

    # List of events that cause tab1_body / tab3_spectrum recalculation
    tab1_recalc_body_events = ('tab1_list', 'tab1_(re)load')
    tab3_recalc_spectrum_events = ('tab3_slider1', 'tab3_slider2', 'tab3_slider3')

    # List of events that cause color recalculation
    tab1_recalc_color_events = ('-AlbedoMode1-', '-AlbedoMode2-', 'tab1_list', 'tab1_(re)load')
    tab3_recalc_color_events = ('tab3_slider1', 'tab3_slider2', 'tab3_slider3')

    # List of events that cause GUI output update
    tab1_update_gui_events = (
        '-ColorSpace-', '-WhitePoint-', '-GammaCorrection-', '-MaximizeBrightness-', '-ScaleFactor-',
        '-AlbedoMode1-', '-AlbedoMode2-', '-bitness-', '-rounding-', 'tab1_list', 'tab1_(re)load', '-currentTab-'
    )
    tab2_update_gui_events = (
        '-ColorSpace-', '-WhitePoint-', '-GammaCorrection-', '-MaximizeBrightness-', '-ScaleFactor-', '-currentTab-'
    )
    tab3_update_gui_events = (
        '-ColorSpace-', '-WhitePoint-', '-GammaCorrection-', '-MaximizeBrightness-', '-ScaleFactor-',
        '-bitness-', '-rounding-', 'tab3_slider1', 'tab3_slider2', 'tab3_slider3', '-currentTab-'
    )

    # GUI first loading flags
    tab1_loaded = False
    tab2_opened = False

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
                    tr.spectral_plot[lang], gui.generate_plot_layout(lang, spectra_plot_size, limit_to_vis, normalize_at_550nm, light_theme), icon=icon,
                    finalize=True, element_justification='center'
                )
            else:
                pl.close_figure(tab1_tab3_fig)
                tab1_tab3_fig_canvas_agg.get_tk_widget().forget()
            dict_to_plot = deepcopy(pinned_spectra_and_colors)
            if tab1_obj_name and tab1_spectrum not in dict_to_plot.keys():
                dict_to_plot |= {tab1_spectrum: tab1_html}
            if tab3_obj_name and tab3_spectrum not in dict_to_plot.keys():
                dict_to_plot |= {tab3_spectrum: tab3_html}
            tab1_tab3_fig = pl.plot_spectra(dict_to_plot, limit_to_vis, normalize_at_550nm, light_theme, lang, spectra_figsize, spectra_dpi)
            tab1_tab3_fig_canvas_agg = pl.draw_figure(window1['W1_canvas'].TKCanvas, tab1_tab3_fig)
        elif event == 'W1_path':
            tab1_tab3_fig.savefig(values['W1_path'], dpi=133.4) # 1200x800
        elif event in ('W1_limit_to_vis', 'W1_normalize', 'W1_light_theme'):
            limit_to_vis = values['W1_limit_to_vis']
            normalize_at_550nm = values['W1_normalize']
            light_theme = values['W1_light_theme']
            tab1_tab3_fig, tab1_tab3_fig_canvas_agg = tab1_tab3_update_plot(
                tab1_tab3_fig, tab1_tab3_fig_canvas_agg,
                window0.ReturnValuesDictionary['-currentTab-'],
                limit_to_vis, normalize_at_550nm, light_theme, lang
            )

        # Run-time translation
        elif event in tr.langs.keys():
            lang = tr.langs[event]
            window0 = gui.translate_win0(window0, tab1_loaded, tab1_albedo_note, tab2_vis, lang)
            match values['-currentTab-']:
                case 'tab1':
                    if tab1_obj_name:
                        window['tab1_title2'].update(tab1_obj_name.indexed_name(lang))
                    tab1_displayed_namesDB = db.obj_names_dict(objectsDB, values['tab1_tag_filter'], values['tab1_searched'], lang)
                    tab1_displayed_names_tuple = tuple(tab1_displayed_namesDB.keys())
                    if tab1_obj_name and values['tab1_searched'] == '':
                        # object name could be not on the list during global search (ValueError) or if no object selected (TypeError)
                        tab1_index = tab1_displayed_names_tuple.index(tab1_obj_name(lang))
                        window['tab1_list'].update(tab1_displayed_names_tuple, set_to_index=tab1_index, scroll_to_index=tab1_index)
                    else:
                        window['tab1_list'].update(tab1_displayed_names_tuple)
                case 'tab3':
                    if tab3_obj_name:
                        window['tab3_title2'].update(tab3_obj_name.indexed_name(lang))
            if window1:
                window1 = gui.translate_win1(window1, lang)
                tab1_tab3_fig, tab1_tab3_fig_canvas_agg = tab1_tab3_update_plot(
                    tab1_tab3_fig, tab1_tab3_fig_canvas_agg,
                    window0.ReturnValuesDictionary['-currentTab-'],
                    limit_to_vis, normalize_at_550nm, light_theme, lang
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

            elif event == '-ColorSpace-' or event == '-WhitePoint-':
                # Update color system
                color_system = ColorSystem(values['-ColorSpace-'], values['-WhitePoint-'])

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
                window['-AlbedoModeText-'].update(visible=is1tab)
                window['-AlbedoMode1-'].update(visible=is1tab)
                window['-AlbedoMode2-'].update(visible=is1tab)
                window['-formattingText-'].update(visible=not2tab)
                window['-bitnessText-'].update(visible=not2tab)
                window['-roundingText-'].update(visible=not2tab)
                window['-bitness-'].update(visible=not2tab)
                window['-rounding-'].update(visible=not2tab)

            # ------------ Events in the tab "Database viewer" ------------

            if values['-currentTab-'] == 'tab1':

                if event == 'tab1_(re)load':

                    # Loading of the spectra database
                    objectsDB, refsDB = db.import_DBs(database_folders)
                    tagsDB = db.tag_list(objectsDB)
                    for l in tr.langs.values():
                        namesDB |= {l: db.obj_names_dict(objectsDB, tag='ALL', searched='', lang=l)}

                    if not tab1_loaded:
                        # Setting the default tag on the first loading
                        tab1_tag = default_tag
                        window['tab1_(re)load'].update(tr.gui_reload[lang])
                    else:
                        # Handle the case of a non-existing tag after reloading
                        tab1_tag = values['tab1_tag_filter']
                        if tab1_tag not in tagsDB:
                            tab1_tag = default_tag

                    window['tab1_tag_filter'].update(tab1_tag, values=tagsDB)
                    tab1_displayed_namesDB = db.obj_names_dict(objectsDB, tab1_tag, values['tab1_searched'], lang)
                    tab1_displayed_names_tuple = tuple(tab1_displayed_namesDB.keys())
                    if tab1_loaded and tab1_obj_name and tab1_obj_name(lang) in tab1_displayed_names_tuple:
                        tab1_index = tab1_displayed_names_tuple.index(tab1_obj_name(lang))
                        window['tab1_list'].update(values=tab1_displayed_names_tuple, set_to_index=tab1_index, scroll_to_index=tab1_index)
                    else:
                        window['tab1_list'].update(values=tab1_displayed_names_tuple)

                    tab1_loaded = True

                if values['tab1_list'] != []:
                    # (Check for the availability of the selected object)
                    # For optimization purposes, the cases when some calculations are not required are separated

                    if event in tab1_recalc_body_events:

                        # Getting ObjectName and updating title
                        try:
                            tab1_obj_name = namesDB[lang][values['tab1_list'][0]]
                        except KeyError:
                            continue
                        window['tab1_title2'].update(tab1_obj_name.indexed_name(lang))

                        # Spectral data import and processing
                        tab1_body = database_parser(tab1_obj_name, objectsDB[tab1_obj_name])

                    if event in tab1_recalc_color_events:

                        # Apply albedo mode to calculated spectrum
                        tab1_spectrum, tab1_estimated = tab1_body.get_spectrum('geometric' if values['-AlbedoMode1-'] else 'spherical')

                        # Color calculation
                        tab1_color_xyz = ColorPoint.from_spectral_data(tab1_spectrum)

                    if event in tab1_update_gui_events:

                        # Color postprocessing
                        tab1_color_rgb = tab1_color_xyz.to_color_system(color_system)
                        tab1_color_rgb.gamma_correction = values['-GammaCorrection-']
                        tab1_color_rgb.maximize_brightness = values['-MaximizeBrightness-'] or tab1_estimated is None
                        tab1_color_rgb.scale_factor = values['-ScaleFactor-']
                        tab1_html = tab1_color_rgb.to_html()

                        # Output
                        window['tab1_graph'].TKCanvas.itemconfig(tab1_preview, fill=tab1_html)
                        window['tab1_rgb'].update(tuple(tab1_color_rgb.to_bit(bitness).round(rounding)))
                        window['tab1_hex'].update(tab1_html)
                        tab1_value, tab1_sd = tab1_spectrum @ get_filter(values['tab1_in_filter'])
                        if tab1_sd is None:
                            window['tab1_convolved'].update(sigfig_round(tab1_value, rounding, warn=False))
                        else:
                            window['tab1_convolved'].update(sigfig_round(tab1_value, uncertainty=tab1_sd, warn=False))

                        # Setting of notes
                        tab1_albedo_note = tr.gui_blank_note
                        if not values['-MaximizeBrightness-']:
                            match tab1_estimated:
                                case None:
                                    if isinstance(tab1_body, ReflectingBody):
                                        tab1_albedo_note = tr.gui_no_albedo
                                case True:
                                    tab1_albedo_note = tr.gui_estimated
                        window['tab1_albedo_note'].update(tab1_albedo_note[lang])

                        # Dynamical plotting
                        if window1:
                            tab1_tab3_fig, tab1_tab3_fig_canvas_agg = tab1_tab3_update_plot(
                                tab1_tab3_fig, tab1_tab3_fig_canvas_agg,
                                window0.ReturnValuesDictionary['-currentTab-'],
                                limit_to_vis, normalize_at_550nm, light_theme, lang
                            )

                if event in ('tab1_tag_filter', 'tab1_searched'):
                    tab1_displayed_namesDB = db.obj_names_dict(objectsDB, values['tab1_tag_filter'], values['tab1_searched'], lang)
                    window['tab1_list'].update(tuple(tab1_displayed_namesDB.keys()))

                elif event == 'tab1_pin' and values['tab1_list'] != []:
                    if tab1_spectrum not in pinned_spectra_and_colors.keys():
                        pinned_spectra_and_colors |= {tab1_spectrum: tab1_html}

                elif event == 'tab1_clear':
                    pinned_spectra_and_colors = {}
                    if window1:
                        tab1_tab3_fig, tab1_tab3_fig_canvas_agg = tab1_tab3_update_plot(
                            tab1_tab3_fig, tab1_tab3_fig_canvas_agg,
                            window0.ReturnValuesDictionary['-currentTab-'],
                            limit_to_vis, normalize_at_550nm, light_theme, lang
                        )

                elif event == 'tab1_export2text':
                    if len(objectsDB) == 0:
                        sg.popup(tr.gui_no_data_message[lang], title=tr.gui_output[lang], icon=icon, non_blocking=True)
                    else:
                        tab1_export = '\n' + '\t'.join(tr.gui_col[lang]) + '\n' + '_' * 36
                        for obj_name in tab1_displayed_namesDB.values():
                            body = database_parser(obj_name, objectsDB[obj_name])

                            # Setting brightness mode
                            spectrum, estimated = body.get_spectrum('geometric' if values['-AlbedoMode1-'] else 'spherical')

                            # Color calculation
                            color = ColorPoint.from_spectral_data(spectrum).to_color_system(color_system)
                            color.maximize_brightness = values['-MaximizeBrightness-'] or estimated is None
                            color.gamma_correction = values['-GammaCorrection-']
                            rgb = tuple(color.to_bit(bitness).round(rounding))

                            # Output
                            tab1_export += f'\n{aux.export_colors(rgb)}\t{obj_name(lang)}'
                            if estimated:
                                tab1_export += f'; {tr.gui_estimated[lang]}'

                        sg.popup_scrolled(
                            tab1_export, title=tr.gui_output[lang], size=(100, max(10, min(30, 3+len(objectsDB)))),
                            font=('Consolas', 10), icon=icon, non_blocking=True
                        )

                elif event == 'tab1_folder':
                    if len(objectsDB) == 0:
                        sg.popup(tr.gui_no_data_message[lang], title=tr.gui_output[lang], icon=icon, non_blocking=True)
                    else:
                        generate_table(
                            objectsDB, values['tab1_tag_filter'], color_system, values['-GammaCorrection-'], values['-MaximizeBrightness-'],
                            values['-ScaleFactor-'], values['-AlbedoMode1-'], values['tab1_folder'], 'png', lang
                        )

            # ------------ Events in the tab "Image processing" ------------

            elif values['-currentTab-'] == 'tab2':

                if isinstance(event, str):

                    if event in ('-typeImage-', '-typeImageRGB-', '-typeImageCube-'):

                        # Getting input data mode name
                        tab2_mode = aux.get_flag_index((values['-typeImage-'], values['-typeImageRGB-'], values['-typeImageCube-']))

                        # Setting the visibility and elements
                        if tab2_mode == 2:
                            # No visible frames in spectral cube mode
                            window['tab2_frames'].update(visible=False)
                        else:
                            # The number of visible frames for RGB image (tab2_mode==1) is 3,
                            # otherwise all possible frames are displayed
                            window['tab2_frames'].update(visible=True)
                            tab2_vis = 3 if tab2_mode else tab2_num
                            for i in range(tab2_num):
                                if i < tab2_vis:
                                    window[f'tab2_band{i}'].update(visible=True)
                                    window[f'tab2_path{i}'].update(visible=values['-typeImage-'])
                                    window[f'tab2_pathText{i}'].update(visible=values['-typeImage-'])
                                    window[f'tab2_rgbText{i}'].update(visible=values['-typeImageRGB-'])
                                else:
                                    window[f'tab2_band{i}'].update(visible=False)

                        # Setting single file choice
                        tab2_single_file_flag = tab2_mode > 0
                        window['tab2_step2'].update(visible=not tab2_single_file_flag)
                        window['tab2_path'].update(visible=tab2_single_file_flag)
                        window['tab2_pathText'].update(visible=tab2_single_file_flag)

                    elif event.startswith('tab2_filter'):
                        # Updates the list of filters and generates the checklist of valid inputs
                        tab2_filters_old = tab2_filters
                        tab2_filters = []
                        tab2_filters_checklist_old = tab2_filters_checklist
                        tab2_filters_checklist = np.zeros(tab2_num, dtype='bool')
                        for i in range(tab2_vis):
                            tab2_filter_name = values[f'tab2_filter{i}']
                            if len(tab2_filter_name) > 2:
                                # Starting with an input length of 3 because:
                                # - Assuming that no filter names are so short
                                # - The wavelength input is always more than three digits
                                try:
                                    tab2_filter = get_filter(tab2_filter_name)
                                    tab2_filters.append(tab2_filter)
                                    tab2_filters_checklist[i] = True
                                except FilterNotFoundError:
                                    pass
                        # To not update the plot when the input is less than three digits or causes an error
                        tab2_filters_were_updated = not (
                            np.array_equal(tab2_filters_checklist_old, tab2_filters_checklist) and tab2_filters_old == tab2_filters
                        )

                    # Image processing
                    elif event in ('tab2_preview_button', 'tab2_folder'):
                        # Reading files and formulas to evaluate
                        tab2_files = []
                        tab2_formulas = []
                        for i in range(tab2_vis):
                            if tab2_filters_checklist[i]:
                                tab2_files.append(values[f'tab2_path{i}'])
                                tab2_formulas.append(values[f'tab2_eval{i}'])
                        # Starting the image processing thread
                        _ = window.start_thread(
                            lambda: ip.image_parser(
                                image_mode=tab2_mode,
                                preview_flag=event=='tab2_preview_button',
                                px_lower_limit=img_preview_area,
                                px_upper_limit=int(float(values['tab2_chunks']) * 1e6), # megapixels to pixels
                                single_file=values['tab2_path'],
                                files=tab2_files,
                                filters=tab2_filters,
                                formulas=tab2_formulas,
                                desun=values['tab2_desun'],
                                photons=values['tab2_photons'],
                                upscale=values['tab2_upscale'],
                                log=tab2_logger
                            ),
                            ('tab2_thread', 'End of the image processing thread\n')
                        )

                    # Updating preview image
                    elif tab2_preview is not None and event in tab2_update_gui_events:
                        tab2_preview_rgb = tab2_preview.to_color_system(color_system)
                        tab2_preview_rgb.gamma_correction = values['-GammaCorrection-']
                        tab2_preview_rgb.maximize_brightness = values['-MaximizeBrightness-']
                        tab2_preview_rgb.scale_factor = values['-ScaleFactor-']
                        window['tab2_preview'].update(data=tab2_preview_rgb.to_bytes())

                # Getting messages from the image processing thread
                elif event[0] == 'tab2_thread':
                    sg.easy_print(event[1]) # pop-up printing
                    if values[event] is not None:
                        tab2_img = values[event]
                        tab2_img.gamma_correction = values['-GammaCorrection-']
                        tab2_img.maximize_brightness = values['-MaximizeBrightness-']
                        tab2_img.scale_factor = values['-ScaleFactor-']
                        if event[1].endswith('Sending the preview to the main thread'):
                            tab2_preview = tab2_img
                        else:
                            tab2_preview = tab2_img.downscale(img_preview_area)
                            tab2_img.to_color_system(color_system).to_pillow_image().save(f'{values["tab2_folder"]}/TCT_{strftime("%Y-%m-%d_%H-%M-%S")}.png')
                        tab2_preview_rgb = tab2_preview.to_color_system(color_system)
                        window['tab2_preview'].update(data=tab2_preview_rgb.to_bytes())

                # Updating filters profile plot
                if event in ('-currentTab-', '-ColorSpace-', '-WhitePoint-') or tab2_filters_were_updated:
                    if not tab2_opened:
                        # The first tab opening
                        tab2_fig = pl.plot_filters((), color_system, lang, filters_figsize, filters_dpi)
                        tab2_opened = True
                    else:
                        pl.close_figure(tab2_fig)
                        tab2_dict_to_plot = [*tab2_filters, *mean_spectrum]
                        tab2_fig = pl.plot_filters(tab2_dict_to_plot, color_system, lang, filters_figsize, filters_dpi)
                        tab2_fig_canvas_agg.get_tk_widget().forget()
                    tab2_fig_canvas_agg = pl.draw_figure(window['tab2_canvas'].TKCanvas, tab2_fig)
                    tab2_filters_were_updated = False


            # ------------ Events in the tab "Blackbody & Redshifts" ------------

            elif values['-currentTab-'] == 'tab3':

                if event in tab3_recalc_spectrum_events:

                    # Spectral data processing and updating title
                    tab3_spectrum = Spectrum.from_blackbody_redshift(visible_range, values['tab3_slider1'], values['tab3_slider2'], values['tab3_slider3'])
                    tab3_spectrum /= sun_in_V
                    tab3_obj_name = tab3_spectrum.name
                    window['tab3_title2'].update(tab3_obj_name.indexed_name(lang))

                if event in tab3_recalc_color_events:

                    # Color calculation
                    tab3_color_xyz = ColorPoint.from_spectral_data(tab3_spectrum)

                if event in tab3_update_gui_events and tab3_obj_name is not None:

                    # Color postprocessing
                    tab3_color_rgb = tab3_color_xyz.to_color_system(color_system)
                    tab3_color_rgb.gamma_correction = values['-GammaCorrection-']
                    tab3_color_rgb.maximize_brightness = values['-MaximizeBrightness-']
                    tab3_color_rgb.scale_factor = values['-ScaleFactor-']
                    tab3_html = tab3_color_rgb.to_html()

                    # Output
                    window['tab3_graph'].TKCanvas.itemconfig(tab3_preview, fill=tab3_html)
                    window['tab3_rgb'].update(tuple(tab3_color_rgb.to_bit(bitness).round(rounding)))
                    window['tab3_hex'].update(tab3_html)

                    # Dynamical plotting
                    if window1:
                        tab1_tab3_fig, tab1_tab3_fig_canvas_agg = tab1_tab3_update_plot(
                            tab1_tab3_fig, tab1_tab3_fig_canvas_agg,
                            window0.ReturnValuesDictionary['-currentTab-'],
                            limit_to_vis, normalize_at_550nm, light_theme, lang
                        )

                elif event == 'tab3_maxtemp_num':
                    window['tab3_slider1'].update(range=(0, int(values['tab3_maxtemp_num'])))

                elif event == 'tab3_pin':
                    if tab3_spectrum not in pinned_spectra_and_colors.keys():
                        pinned_spectra_and_colors |= {tab3_spectrum: tab3_html}

                elif event == 'tab3_clear':
                    pinned_spectra_and_colors = {}
                    if window1:
                        tab1_tab3_fig, tab1_tab3_fig_canvas_agg = tab1_tab3_update_plot(
                            tab1_tab3_fig, tab1_tab3_fig_canvas_agg,
                            window0.ReturnValuesDictionary['-currentTab-'],
                            limit_to_vis, normalize_at_550nm, light_theme, lang
                        )
