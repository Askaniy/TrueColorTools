import io
import PySimpleGUI as sg
import scr.strings as tr
import scr.filters as filters
import scr.data_import as di

sg.LOOK_AND_FEEL_TABLE["MaterialDark"] = {
        'BACKGROUND': '#333333', 'TEXT': '#FFFFFF',
        'INPUT': '#424242', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#424242',
        'BUTTON': ('#FFFFFF', '#007ACC'), 'PROGRESS': ('#000000', '#000000'),
        'BORDER': 0, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
        'ACCENT1': '#FF0266', 'ACCENT2': '#FF5C93', 'ACCENT3': '#C5003C'
    }
sg.ChangeLookAndFeel("MaterialDark")

def convert_to_bytes(img):
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

def frame(num, lang):
    n = str(num)
    l = [
        [sg.Input(size=(18, 1), disabled=False, disabled_readonly_background_color="#3A3A3A", enable_events=True, key="T2_path"+n), sg.FileBrowse(button_text=tr.gui_browse[lang], size=(10, 1), disabled=False, key="T2_browse"+n)],
        [sg.Text(tr.gui_filter[lang], size=(13, 1), text_color="#A3A3A3", key="T2_filterN"+n), sg.InputCombo([], size=(11, 1), disabled=True, enable_events=True, key="T2_filter"+n)],
        [sg.Text(tr.gui_wavelength[lang], size=(13, 1), key="T2_wavelengthN"+n), sg.Input(size=(13, 1), disabled_readonly_background_color="#3A3A3A", disabled=False, enable_events=True, key="T2_wavelength"+n)],
        [sg.Text(tr.gui_exposure[lang], size=(13, 1), key="T2_exposureN"+n), sg.Input("1.0", size=(13, 1), disabled_readonly_background_color="#3A3A3A", disabled=False, key="T2_exposure"+n)]
    ]
    return sg.Frame(f"{tr.gui_band[lang]} {num+1}", l, visible=True, key="T2_band"+n)

def generate_layout(objectsDB, T2_preview: tuple, T4_text_colors: tuple, lang: str):
    T1_col1 = [
        [sg.Text(tr.gui_database[lang], size=(16, 1), font=("arial", 12), key="T1_title1")],
        [sg.Text(tr.gui_tags[lang], size=(7, 1), key="T1_tagsN"), sg.InputCombo(di.tag_list(objectsDB), default_value="featured", size=(17, 1), enable_events=True, key="T1_tags")],
        [sg.Listbox(values=tuple(di.obj_dict(objectsDB, "featured", lang).keys()), size=(27, 22), enable_events=True, key="T1_list")]
    ]
    T1_col2 = [
        [sg.Text(tr.gui_settings[lang], size=(16, 1), font=("arial", 12), key="T1_title2")],
        [sg.Checkbox(tr.gui_gamma[lang], size=(16, 1), enable_events=True, default=True, key="T1_gamma")],
        [sg.Checkbox("sRGB", enable_events=True, size=(16, 1), key="T1_srgb")],
        [sg.HorizontalSeparator()],
        [sg.Text(tr.gui_br[lang][0], size=(21, 1), key="T1_br_mode")],
        [sg.Radio(tr.gui_br[lang][1], "T1_rad", size=(15, 1), enable_events=True, default=True, key="T1_br_mode0")],
        [sg.Radio(tr.gui_br[lang][2], "T1_rad", size=(15, 1), enable_events=True, key="T1_br_mode1")],
        [sg.Radio(tr.gui_br[lang][3], "T1_rad", size=(15, 1), enable_events=True, key="T1_br_mode2")],
        [sg.HorizontalSeparator()],
        [sg.Text(tr.gui_phase[lang], size=(21, 1), key="T1_phase")],
        [sg.Slider(range=(-180, 180), default_value=0, resolution=1, orientation="h", size=(18, 16), enable_events=True, key="T1_slider")],
        [sg.HorizontalSeparator()],
        [sg.Text(tr.gui_interp[lang][0], size=(21, 1), key="T1_interp")],
        [sg.Radio(tr.gui_interp[lang][1], "T1_interp", size=(15, 1), enable_events=True, default=True, key="T1_interp0")],
        [sg.Radio(tr.gui_interp[lang][2], "T1_interp", size=(15, 1), enable_events=True, key="T1_interp1")],
        [sg.HorizontalSeparator()],
        [sg.Text(tr.gui_bit[lang], size=(14, 1), key="T1_bit"), sg.InputText("8", size=(4, 1), enable_events=True, key="T1_bit_num")],
        [sg.Text(tr.gui_rnd[lang], size=(14, 1), key="T1_rnd"), sg.InputText("3", size=(4, 1), enable_events=True, key="T1_rnd_num")]
    ]
    T1_col3 = [
        [sg.Text(tr.gui_results[lang], size=(16, 1), font=("arial", 12), key="T1_title3")],
        [sg.Graph(canvas_size=(180, 175), graph_bottom_left=(0, 0), graph_top_right=(100, 100), background_color=None, key="T1_graph")],
        [sg.Text(tr.gui_rgb[lang], size=(12, 1), key="T1_colorRGB")],
        [sg.In(size=(25, 1), key="T1_rgb")],
        [sg.Text(tr.gui_hex[lang], size=(12, 1), key="T1_colorHEX")],
        [sg.In(size=(25, 1), key="T1_hex")],
        [sg.T("")],
        [sg.Button(button_text=tr.gui_add[lang], size=(22, 1), key="T1_add")],
        [sg.Button(button_text=tr.gui_plot[lang], size=(22, 1), key="T1_plot")],
        [sg.Button(button_text=tr.gui_export[lang], size=(22, 1), key="T1_export")]
    ]

    T2_frames = [
        [frame(0, lang)],
        [frame(1, lang)],
        [frame(2, lang)],
        [frame(3, lang)],
        [frame(4, lang)],
        [frame(5, lang)],
        [frame(6, lang)],
        [frame(7, lang)],
        [frame(8, lang)],
        [frame(9, lang)] # just add more frames here
    ]
    T2_col1 = [
        [sg.Text(tr.gui_input[lang], size=(18, 1), font=("arial", 12), key="T2_title1"),
        sg.Button(button_text="+", size=(2, 1), key="T2_+"), sg.Button(button_text="-", size=(2, 1), disabled=False, key="T2_-")],
        [sg.Column(T2_frames, size=(250, 400), scrollable=True, vertical_scroll_only=True, key="T2_frames")]
    ]
    T2_col2 = [
        [sg.Text(tr.gui_output[lang], size=(30, 1), font=("arial", 12), key="T2_title2")],
        [sg.Checkbox(tr.gui_gamma[lang], size=(16, 1), default=True, key="T2_gamma"),
        sg.Radio(tr.gui_interp[lang][1], "T2_interp", size=(12, 1), enable_events=True, default=True, key="T2_interp0")],
        [sg.Checkbox("sRGB", size=(16, 1), key="T2_srgb"),
        sg.Radio(tr.gui_interp[lang][2], "T2_interp", size=(12, 1), enable_events=True, key="T2_interp1")],
        [sg.HorizontalSeparator()],
        [sg.Checkbox(tr.gui_makebright[lang], size=(16, 1), key="T2_makebright"),
        sg.Checkbox(tr.gui_autoalign[lang], size=(16, 1), key="T2_autoalign")],
        [sg.Checkbox(tr.gui_desun[lang], size=(30, 1), key="T2_desun")],
        [sg.Checkbox(tr.gui_single[lang], size=(11, 1), enable_events=True, key="T2_single"),
        sg.Input(size=(14, 1), disabled=True, disabled_readonly_background_color="#3A3A3A", key="T2_path"),
        sg.FileBrowse(button_text=tr.gui_browse[lang], size=(10, 1), disabled=True, key="T2_browse")],
        [sg.Checkbox(tr.gui_filterset[lang], size=(12, 1), enable_events=True, key="T2_filterset"),
        sg.InputCombo(filters.get_sets(), size=(24, 1), enable_events=True, disabled=True, key="T2_filter")],
        [sg.HorizontalSeparator()],
        [sg.Checkbox(tr.gui_plotpixels[lang], size=(30, 1), enable_events=True, key="T2_plotpixels")],
        [sg.Text(tr.gui_folder[lang], size=(14, 1), key="T2_folderN"),
        sg.Input(size=(14, 1), enable_events=True, key="T2_folder"),
        sg.FolderBrowse(button_text=tr.gui_browse[lang], size=(10, 1), key="T2_browse_folder")],
        [sg.Button(tr.gui_preview[lang], size=(19, 1), disabled=True, key="T2_preview"),
        sg.Button(tr.gui_process[lang], size=(19, 1), disabled=True, key="T2_process")],
        [sg.Image(background_color="black", size=T2_preview, key="T2_image")]
    ]

    T3_col1 = [
        [sg.Text(tr.gui_settings[lang], size=(20, 1), font=("arial", 12), key="T3_title1")],
        [sg.Text(tr.gui_tags[lang], size=(7, 1), key="T3_tagsN"), sg.InputCombo(di.tag_list(objectsDB), default_value="featured", size=(16, 1), enable_events=True, key="T3_tags")],
        [sg.HorizontalSeparator()],
        [sg.Checkbox(tr.gui_gamma[lang], size=(16, 1), enable_events=True, default=True, key="T3_gamma")],
        [sg.Checkbox("sRGB", enable_events=True, size=(16, 1), key="T3_srgb")],
        [sg.HorizontalSeparator()],
        [sg.Text(tr.gui_br[lang][0], size=(22, 1), key="T3_br_mode")],
        [sg.Radio(tr.gui_br[lang][1], "T3_rad", size=(15, 1), enable_events=True, default=True, key="T3_br_mode0")],
        [sg.Radio(tr.gui_br[lang][2], "T3_rad", size=(15, 1), enable_events=True, key="T3_br_mode1")],
        [sg.Radio(tr.gui_br[lang][3], "T3_rad", size=(15, 1), enable_events=True, key="T3_br_mode2")]
    ]
    T3_col2 = [
        [sg.Text(tr.gui_results[lang], size=(30, 1), font=("arial", 12), key="T3_title2")],
        [sg.Text(tr.gui_extension[lang], size=(15, 1), key="T3_ext"), sg.InputCombo(["png", "jpeg", "pdf"], default_value="png", size=(10, 1), enable_events=True, key="T3_extension")],
        [sg.Text(tr.gui_folder[lang], size=(15, 1), key="T3_folderN"), sg.Input(size=(22, 1), enable_events=True, key="T3_folder"), sg.FolderBrowse(button_text=tr.gui_browse[lang], size=(10, 1), key="T3_browse_folder")],
        [sg.T("")],
        [sg.Button(tr.gui_process[lang], size=(15, 1), disabled=True, key="T3_process")]
    ]

    slider_size = (30, 15)
    T4_text_colors = ("#A3A3A3", "#FFFFFF")
    T4_col1 = [
        [sg.Text(tr.gui_input[lang], size=(16, 1), font=("arial", 12), key="T4_title1")],
        [sg.Text(tr.gui_temp[lang], size=(16, 1), key="T4_temp"), sg.Slider(range=(0, 20000), default_value=0, resolution=100, orientation="h", size=slider_size, enable_events=True, key="T4_slider1")],
        [sg.Text(tr.gui_velocity[lang], size=(16, 1), key="T4_velocity"), sg.Slider(range=(-1, 1), default_value=0, resolution=0.01, orientation="h", size=slider_size, enable_events=True, key="T4_slider2")],
        [sg.Text(tr.gui_vII[lang], size=(16, 1), key="T4_vII"), sg.Slider(range=(0, 1), default_value=0, resolution=0.01, orientation="h", size=slider_size, enable_events=True, key="T4_slider3")],
        [sg.Text(tr.gui_irr[lang], size=(16, 1), text_color=T4_text_colors[0], key="T4_scale"), sg.Slider(range=(-50, 50), default_value=0, resolution=0.01, orientation="h", size=slider_size, enable_events=True, disabled=True, key="T4_slider4")],
        [sg.T("")],
        [sg.HorizontalSeparator()],
        [sg.Checkbox(tr.gui_surfacebr[lang], size=(23, 1), enable_events=True, default=False, key="T4_surfacebr"),
        sg.Text(tr.gui_maxtemp[lang], size=(14, 1), key="T4_maxtemp"), sg.InputText("20000", size=(8, 1), enable_events=True, key="T4_maxtemp_num")],
        [sg.Checkbox(tr.gui_gamma[lang], size=(23, 1), enable_events=True, default=True, key="T4_gamma"),
        sg.Text(tr.gui_bit[lang], size=(14, 1), key="T4_bit"), sg.InputText("8", size=(4, 1), enable_events=True, key="T4_bit_num")],
        [sg.Checkbox("sRGB", size=(23, 1), enable_events=True, key="T4_srgb"),
        sg.Text(tr.gui_rnd[lang], size=(14, 1), key="T4_rnd"), sg.InputText("3", size=(4, 1), enable_events=True, key="T4_rnd_num")]
    ]
    T4_col2 = [
        [sg.Text(tr.gui_results[lang], size=(16, 1), font=("arial", 12), key="T4_title2")],
        [sg.Graph(canvas_size=(180, 175), graph_bottom_left=(0, 0), graph_top_right=(100, 100), background_color=None, key="T4_graph")],
        [sg.Text(tr.gui_rgb[lang], size=(12, 1), key="T4_colorRGB")],
        [sg.In(size=(25, 1), key="T4_rgb")],
        [sg.Text(tr.gui_hex[lang], size=(12, 1), key="T4_colorHEX")],
        [sg.In(size=(25, 1), key="T4_hex")]
    ]

    tab1 = [
        [sg.vtop(sg.Column(T1_col1)), sg.VSeperator(), sg.vtop(sg.Column(T1_col2)), sg.VSeperator(), sg.vtop(sg.Column(T1_col3))]
    ]
    tab2 = [
        [sg.vtop(sg.Column(T2_col1)), sg.VSeperator(), sg.vtop(sg.Column(T2_col2))]
    ]
    tab3 = [
        [sg.vtop(sg.Column(T3_col1)), sg.VSeperator(), sg.vtop(sg.Column(T3_col2))]
    ]
    tab4 = [
        [sg.vtop(sg.Column(T4_col1)), sg.VSeperator(), sg.vtop(sg.Column(T4_col2))]
    ]
    return [
        [sg.Menu(tr.gui_menu[lang], key="menu")],
        [sg.TabGroup([[
            sg.Tab(tr.gui_tabs[lang][0], tab1, key="tab0"),
            sg.Tab(tr.gui_tabs[lang][1], tab2, key="tab2"),
            sg.Tab(tr.gui_tabs[lang][2], tab3, key="tab3"),
            sg.Tab(tr.gui_tabs[lang][3], tab4, key="tab4")
            ]])
        ]
    ]

def translate(window: sg.Window, T2_num: int, lang: str):
    window["menu"].update(tr.gui_menu[lang])
    #window["tab0"].update(title=tr.gui_tabs[lang][0])
    #window["tab1"].update(title=tr.gui_tabs[lang][1])
    #window["tab2"].update(title=tr.gui_tabs[lang][2])
    window["T1_title1"].update(tr.gui_database[lang])
    window["T1_title2"].update(tr.gui_settings[lang])
    window["T1_title3"].update(tr.gui_results[lang])
    window["T1_tagsN"].update(tr.gui_tags[lang])
    window["T1_gamma"].update(text=tr.gui_gamma[lang])
    window["T1_br_mode"].update(tr.gui_br[lang][0])
    window["T1_br_mode0"].update(text=tr.gui_br[lang][1])
    window["T1_br_mode1"].update(text=tr.gui_br[lang][2])
    window["T1_br_mode2"].update(text=tr.gui_br[lang][3])
    window["T1_phase"].update(tr.gui_phase[lang])
    window["T1_interp"].update(tr.gui_interp[lang][0])
    window["T1_interp0"].update(text=tr.gui_interp[lang][1])
    window["T1_interp1"].update(text=tr.gui_interp[lang][2])
    window["T1_bit"].update(tr.gui_bit[lang])
    window["T1_rnd"].update(tr.gui_rnd[lang])
    window["T1_colorRGB"].update(tr.gui_rgb[lang])
    window["T1_colorHEX"].update(tr.gui_hex[lang])
    window["T1_add"].update(tr.gui_add[lang])
    window["T1_plot"].update(tr.gui_plot[lang])
    window["T1_export"].update(tr.gui_export[lang])
    window["T2_title1"].update(tr.gui_input[lang])
    window["T2_title2"].update(tr.gui_output[lang])
    for i in range(T2_num):
        window["T2_band"+str(i)].update(f"{tr.gui_band[lang]} {i+1}")
        window["T2_browse"+str(i)].update(tr.gui_browse[lang])
        window["T2_filterN"+str(i)].update(tr.gui_filter[lang])
        window["T2_wavelengthN"+str(i)].update(tr.gui_wavelength[lang])
        window["T2_exposureN"+str(i)].update(tr.gui_exposure[lang])
    window["T2_gamma"].update(text=tr.gui_gamma[lang])
    window["T2_interp0"].update(text=tr.gui_interp[lang][1])
    window["T2_interp1"].update(text=tr.gui_interp[lang][2])
    window["T2_makebright"].update(text=tr.gui_makebright[lang])
    window["T2_autoalign"].update(text=tr.gui_autoalign[lang])
    window["T2_desun"].update(text=tr.gui_desun[lang])
    window["T2_single"].update(text=tr.gui_single[lang])
    window["T2_browse"].update(tr.gui_browse[lang])
    window["T2_filterset"].update(text=tr.gui_filterset[lang])
    window["T2_folderN"].update(tr.gui_folder[lang])
    window["T2_browse_folder"].update(tr.gui_browse[lang])
    window["T2_plotpixels"].update(text=tr.gui_plotpixels[lang])
    window["T2_preview"].update(tr.gui_preview[lang])
    window["T2_process"].update(tr.gui_process[lang])
    window["T3_title1"].update(tr.gui_settings[lang])
    window["T3_title2"].update(tr.gui_results[lang])
    window["T3_tagsN"].update(tr.gui_tags[lang])
    window["T3_gamma"].update(text=tr.gui_gamma[lang])
    window["T3_br_mode"].update(tr.gui_br[lang][0])
    window["T3_br_mode0"].update(text=tr.gui_br[lang][1])
    window["T3_br_mode1"].update(text=tr.gui_br[lang][2])
    window["T3_br_mode2"].update(text=tr.gui_br[lang][3])
    window["T3_ext"].update(tr.gui_extension[lang])
    window["T3_browse_folder"].update(tr.gui_browse[lang])
    window["T3_folderN"].update(tr.gui_folder[lang])
    window["T3_process"].update(tr.gui_process[lang])
    window["T4_title1"].update(tr.gui_input[lang])
    window["T4_title2"].update(tr.gui_results[lang])
    window["T4_temp"].update(tr.gui_temp[lang])
    window["T4_velocity"].update(tr.gui_velocity[lang])
    window["T4_vII"].update(tr.gui_vII[lang])
    window["T4_scale"].update(tr.gui_irr[lang])
    window["T4_surfacebr"].update(text=tr.gui_surfacebr[lang])
    window["T4_gamma"].update(text=tr.gui_gamma[lang])
    window["T4_maxtemp"].update(tr.gui_maxtemp[lang])
    window["T4_bit"].update(tr.gui_bit[lang])
    window["T4_rnd"].update(tr.gui_rnd[lang])
    window["T4_colorRGB"].update(tr.gui_rgb[lang])
    window["T4_colorHEX"].update(tr.gui_hex[lang])
    return window