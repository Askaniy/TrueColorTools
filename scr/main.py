import io
import time
import numpy as np
import PySimpleGUI as sg
from PIL import Image, ImageDraw, ImageFont
import plotly.graph_objects as go
import scr.cmf as cmf
import scr.filters as filters
import scr.calculations as calc
import scr.database as db
import scr.strings as tr
import scr.experimental


def tag_list():
    tag_set = set(["all"])
    for data in db.objects.values():
        if "tags" in data:
            tag_set.update(data["tags"])
    return list(tag_set)

def obj_list(tag, lang):
    names = {}
    for name_0, data in db.objects.items():

        flag = True
        if tag != "all":
            if "tags" in data:
                if tag not in data["tags"]:
                    flag = False
            else:
                flag = False
        
        if flag:
            if "|" in name_0:
                name_1 = "{} [{}]".format(*name_0.split("|"))
            else:
                name_1 = name_0
            if lang != "en":
                index = ""
                if name_1[0] == "(":
                    parts = name_1.split(")", 1)
                    index = parts[0] + ") "
                    name_1 = parts[1].strip()
                elif "/" in name_1:
                    parts = name_1.split("/", 1)
                    index = parts[0] + "/"
                    name_1 = parts[1].strip()
                for obj_name, tranlation in tr.names.items():
                    if name_1.startswith(obj_name):
                        name_1 = name_1.replace(obj_name, tranlation[lang])
                        break
                name_1 = index + name_1
            names.update({name_1: name_0})
    return names

def export(rgb):
    lst = []
    mx = 0
    for i in rgb:
        lst.append(str(i))
        l = len(lst[-1])
        if l > mx:
            mx = l
    w = 8 if mx < 8 else mx+1
    return "".join([i.ljust(w) for i in lst])

def denumerized_sources(lst):
    res = []
    for i in range(len(lst)):
       res.append(lst[i].split("]: ")[1])
    return res

def width(line, font):
    return font.getlength(line)

def recurse(lst0, font, maxW, hyphen=True):
    lst = lst0
    w_list = []
    for i in lst:
        w_list.append(width(i, font))
    if max(w_list) < maxW:
        for i in range(len(w_list)-1):
            if w_list[i]+w_list[i+1] < maxW:
                lst[i] += " " + lst[i+1]
                lst.pop(i+1)
                recurse(lst, font, maxW)
                break
    else:
        hyphen_w = width("-", font) if hyphen else 0
        for i in range(len(lst)):
            if width(lst[i], font) > maxW:
                try:
                    lst[i+1] = lst[i][-1] + " " + lst[i+1]
                except IndexError:
                    lst.append(lst[i][-1])
                finally:
                    lst[i] = lst[i][:-1]
                while width(lst[i], font)+hyphen_w > maxW:
                    lst[i+1] = lst[i][-1] + lst[i+1]
                    lst[i] = lst[i][:-1]
                if lst[i][-1] in [" ", ":", "-"]:
                    recurse(lst0, font, maxW, hyphen=False)
                else:
                    lst[i] += "-"
                    recurse(lst, font, maxW)
                break
    return lst

def line_splitter(line, font, maxW):
    w = width(line, font)
    if w < maxW:
        return [line]
    else:
        return recurse(line.split(), font, maxW)

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

def launch_window(lang, debug):
    sg.LOOK_AND_FEEL_TABLE["MaterialDark"] = {
        'BACKGROUND': '#333333', 'TEXT': '#FFFFFF',
        'INPUT': '#424242', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#424242',
        'BUTTON': ('#FFFFFF', '#007ACC'), 'PROGRESS': ('#000000', '#000000'),
        'BORDER': 0, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
        'ACCENT1': '#FF0266', 'ACCENT2': '#FF5C93', 'ACCENT3': '#C5003C'
    }
    sg.ChangeLookAndFeel("MaterialDark")

    T1_col1 = [
        [sg.Text(tr.gui_database[lang], size=(16, 1), font=("arial", 12), key="T1_title1")],
        [sg.Text(tr.gui_tags[lang], size=(7, 1), key="T1_tagsN"), sg.InputCombo(tag_list(), default_value="featured", size=(17, 1), enable_events=True, key="T1_tags")],
        [sg.Listbox(values=tuple(obj_list("featured", lang).keys()), size=(27, 22), enable_events=True, key="T1_list")]
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

    T2_vis = 3
    T2_preview = (256, 128)
    T2_area = T2_preview[0]*T2_preview[1]
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
    T2_num = len(T2_frames)
    T2_col1 = [
        [sg.Text(tr.gui_input[lang], size=(18, 1), font=("arial", 12), key="T2_title1"),
        sg.Button(button_text="+", size=(2, 1), key="T2_+"), sg.Button(button_text="-", size=(2, 1), disabled=False, key="T2_-")],
        [sg.Column(T2_frames, size=(250, 400), scrollable=True, vertical_scroll_only=True)]
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
        [sg.Text(tr.gui_tags[lang], size=(7, 1), key="T3_tagsN"), sg.InputCombo(tag_list(), default_value="featured", size=(16, 1), enable_events=True, key="T3_tags")],
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

    layout = [
        [sg.Menu(tr.gui_menu[lang], key="menu")],
        [sg.TabGroup([[
            sg.Tab(tr.gui_tabs[lang][0], tab1, key="tab0"),
            sg.Tab(tr.gui_tabs[lang][1], tab2, key="tab2"),
            sg.Tab(tr.gui_tabs[lang][2], tab3, key="tab3"),
            sg.Tab(tr.gui_tabs[lang][3], tab4, key="tab4")
            ]])
        ]
    ]

    window = sg.Window("True Color Tools", layout, finalize=True)
    T1_preview = window["T1_graph"].DrawCircle((48, 46), 42, fill_color="black", line_color="white")
    T4_preview = window["T4_graph"].DrawCircle((48, 46), 42, fill_color="black", line_color="white")

    T1_fig = go.Figure()
    T1_events = ["T1_list", "T1_gamma", "T1_srgb", "T1_br_mode0", "T1_br_mode1", "T1_br_mode2", "T1_interp0", "T1_interp1", "T1_slider", "T1_bit_num", "T1_rnd_num"]
    br_modes = ["chromaticity", "albedo 0.5", "albedo"]

    for i in range(T2_vis, T2_num):
        window["T2_band"+str(i)].update(visible=False)


    # Window events loop

    names = []
    while True:
        event, values = window.Read()

        # Global window events

        if event == sg.WIN_CLOSED or event == tr.gui_exit[lang]:
            break

        elif event in tr.lang_list[lang]:
            for lng, lst in tr.langs.items():
                if event in lst:
                    lang = lng
                    break
            window["menu"].update(tr.gui_menu[lang])
            #window["tab0"].update(title=tr.gui_tabs[lang][0])
            #window["tab1"].update(title=tr.gui_tabs[lang][1])
            #window["tab2"].update(title=tr.gui_tabs[lang][2])
            window["T1_title1"].update(tr.gui_database[lang])
            window["T1_title2"].update(tr.gui_settings[lang])
            window["T1_title3"].update(tr.gui_results[lang])
            window["T1_tagsN"].update(tr.gui_tags[lang])
            window["T1_list"].update(values=tuple(obj_list(values["T1_tags"], lang).keys()))
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
        
        elif event == tr.source[lang]:
            sg.popup_scrolled("\n\n".join(db.sources), title=event, size=(100, 20))
        
        elif event == tr.note[lang]:
            notes = []
            for note, translation in tr.notes.items():
                notes.append(f"{note} {translation[lang]}")
            sg.popup("\n".join(notes), title=event)
        
        elif event == tr.gui_info[lang]:
            sg.popup(f'{tr.link}\n{tr.auth_info[lang]}', title=event)
        
        # ------------ Events in the tab "Spectra" ------------

        elif event.startswith("T1"):

            if event in T1_events and values["T1_list"] != []:
                T1_name = values["T1_list"][0]
                T1_nm = cmf.xyz_nm if values["T1_srgb"] else cmf.rgb_nm
                for i in range(3):
                    if values["T1_br_mode"+str(i)]:
                        T1_mode = br_modes[i]

                # Spectral data import and processing
                T1_spectrum = db.objects[obj_list("all", lang)[T1_name]]
                T1_albedo = 0
                if "albedo" not in T1_spectrum:
                    if T1_mode == "albedo":
                        T1_mode = "chromaticity"
                    T1_spectrum.update({"albedo": False})
                elif type(T1_spectrum["albedo"]) != bool:
                    T1_albedo = T1_spectrum["albedo"]
                T1_spectrum = calc.transform(T1_spectrum)
                
                # Spectrum interpolation
                T1_sun = False
                if "sun" in T1_spectrum:
                    T1_sun = T1_spectrum["sun"]
                T1_curve = calc.polator(T1_spectrum["nm"], T1_spectrum["br"], T1_nm, T1_albedo, values["T1_interp1"], desun=T1_sun)
                
                # Color calculation
                try:
                    T1_phase = 0 if "star" in T1_spectrum["tags"] else values["T1_slider"]
                except Exception:
                    T1_phase = values["T1_slider"]
                T1_rgb = calc.to_rgb(
                    T1_name, T1_curve, mode=T1_mode,
                    albedo = T1_spectrum["albedo"] or T1_albedo,
                    phase=T1_phase,
                    exp_bit=int(values["T1_bit_num"]), 
                    gamma=values["T1_gamma"], 
                    rnd=int(values["T1_rnd_num"]),
                    srgb=values["T1_srgb"]
                )
                T1_rgb_show = calc.to_rgb(
                    T1_name, T1_curve, mode=T1_mode,
                    albedo = T1_spectrum["albedo"] or T1_albedo,
                    phase=T1_phase,
                    gamma=values["T1_gamma"],
                    srgb=values["T1_srgb"],
                    html=True
                )

                # Output
                window["T1_graph"].TKCanvas.itemconfig(T1_preview, fill=T1_rgb_show)
                window["T1_rgb"].update(T1_rgb)
                window["T1_hex"].update(T1_rgb_show)
            
            elif event == "T1_tags":
                window["T1_list"].update(tuple(obj_list(values["T1_tags"], lang).keys()))
            
            elif event == "T1_add" and values["T1_list"] != []:
                names.append(values["T1_list"][0])
                T1_fig.add_trace(go.Scatter(
                    x = T1_nm,
                    y = T1_curve,
                    name = values["T1_list"][0],
                    line = dict(color=T1_rgb_show, width=4)
                    ))
            
            elif event == "T1_plot":
                if len(names) == 1:
                    T1_title_text = tr.single_title_text[lang] + names[0]
                else:
                    T1_title_text = tr.batch_title_text[lang] + ", ".join(names)
                T1_fig.update_layout(title=T1_title_text, xaxis_title=tr.xaxis_text[lang], yaxis_title=tr.yaxis_text[lang])
                T1_fig.show()
            
            elif event == "T1_export":
                T1_export = "\n" + "\t".join(tr.gui_col[lang]) + "\n" + "_" * 36
                T1_nm = cmf.xyz_nm if values["T1_srgb"] else cmf.rgb_nm
                
                # Spectrum processing
                for name_1, name_0 in obj_list(values["T1_tags"], lang).items():
                    T1_spectrum = db.objects[name_0]
                    for i in range(3):
                        if values["T1_br_mode"+str(i)]:
                            T1_mode = br_modes[i]
                    T1_albedo = 0
                    if "albedo" not in T1_spectrum:
                        if T1_mode == "albedo":
                            T1_mode = "chromaticity"
                        T1_spectrum.update({"albedo": False})
                    elif type(T1_spectrum["albedo"]) != bool:
                        T1_albedo = T1_spectrum["albedo"]
                    T1_spectrum = calc.transform(T1_spectrum)
                    
                    # Spectrum interpolation
                    T1_sun = False
                    if "sun" in T1_spectrum:
                        T1_sun = T1_spectrum["sun"]
                    T1_curve = calc.polator(T1_spectrum["nm"], T1_spectrum["br"], T1_nm, T1_albedo, values["T1_interp1"], desun=T1_sun)

                    # Color calculation
                    T1_rgb = calc.to_rgb(
                        name_0, T1_curve, mode=T1_mode,
                        albedo = T1_spectrum["albedo"] or T1_albedo,
                        exp_bit=int(values["T1_bit_num"]), 
                        gamma=values["T1_gamma"], 
                        rnd=int(values["T1_rnd_num"]),
                        srgb=values["T1_srgb"]
                    )

                    # Output
                    T1_export += "\n" + export(T1_rgb) + "\t" + name_1

                sg.popup_scrolled(T1_export, title=tr.gui_results[lang], size=(72, 32), font=("Consolas", 10))
        
        # ------------ Events in the tab "Images" ------------

        elif event.startswith("T2"):

            if event == "T2_single":
                window["T2_browse"].update(disabled=not values["T2_single"])
                window["T2_path"].update(disabled=not values["T2_single"])
                for i in range(T2_num):
                    window["T2_browse"+str(i)].update(disabled=values["T2_single"])
                    window["T2_path"+str(i)].update(disabled=values["T2_single"])
                    window["T2_exposure"+str(i)].update(disabled=values["T2_single"])
                if values["T2_single"]:
                    T2_vis = 3
                    for i in range(T2_num):
                        window["T2_band"+str(i)].update(visible=False)
                    for i in range(3):
                        window["T2_band"+str(i)].update(visible=True)

            elif event == "T2_filterset":
                window["T2_filter"].update(disabled=not values["T2_filterset"])
                for i in range(T2_num):
                    window["T2_filter"+str(i)].update(disabled=not values["T2_filterset"])
                    window["T2_wavelength"+str(i)].update(disabled=values["T2_filterset"])

            elif event == "T2_filter":
                for i in range(T2_num):
                    window["T2_filter"+str(i)].update(values=filters.get_filters(values["T2_filter"]))

            elif event in ["T2_filter"+str(i) for i in range(T2_num)]:
                i = event[-1]
                window["T2_wavelength"+i].update(filters.get_param(values["T2_filter"], values["T2_filter"+i], "L_mean"))

            elif event == "T2_folder":
                window["T2_process"].update(disabled=False)
            
            elif event == "T2_+":
                window["T2_band"+str(T2_vis)].update(visible=True)
                T2_vis += 1
            
            elif event == "T2_-":
                window["T2_band"+str(T2_vis-1)].update(visible=False)
                T2_vis -= 1
            
            window["T2_+"].update(disabled=values["T2_single"] or not 2 <= T2_vis < T2_num)
            window["T2_-"].update(disabled=values["T2_single"] or not 2 < T2_vis <= T2_num)
            for i in range(T2_num):
                window["T2_filterN"+str(i)].update(text_color=("#A3A3A3", "#FFFFFF")[values["T2_filterset"]])
                window["T2_wavelengthN"+str(i)].update(text_color=("#A3A3A3", "#FFFFFF")[not values["T2_filterset"]])
                window["T2_exposureN"+str(i)].update(text_color=("#A3A3A3", "#FFFFFF")[not values["T2_single"]])
            
            input_data = {"gamma": values["T2_gamma"], "srgb": values["T2_srgb"], "desun": values["T2_desun"], "nm": []}
            
            T2_preview_status = True
            if values["T2_single"]:
                if values["T2_path"] == "":
                    T2_preview_status = False
            else:
                for i in range(T2_vis):
                    if values["T2_path"+str(i)] == "":
                        T2_preview_status = False
                        break
            if values["T2_filterset"]:
                for i in range(T2_vis):
                    if values["T2_filter"+str(i)]:
                        try:
                            input_data["nm"].append(filters.get_param(values["T2_filter"], values["T2_filter"+str(i)], "L_mean"))
                        except KeyError:
                            window["T2_filter"+str(i)].update([])
                    else:
                        T2_preview_status = False
                        break
            else:
                for i in range(T2_vis):
                    if values["T2_wavelength"+str(i)].replace(".", "").isnumeric():
                        input_data["nm"].append(float(values["T2_wavelength"+str(i)]))
                    else:
                        T2_preview_status = False
                        break
            if not all(a > b for a, b in zip(input_data["nm"][1:], input_data["nm"])): # increasing check
                T2_preview_status = False
            window["T2_preview"].update(disabled=not T2_preview_status)
            window["T2_process"].update(disabled=not T2_preview_status) if values["T2_folder"] != "" else window["T2_process"].update(disabled=True)
            
            if event in ("T2_preview", "T2_process"):

                T2_time = time.monotonic()
                T2_load = []

                if values["T2_single"]:
                    T2_rgb_img = Image.open(values["T2_path"])
                    if T2_rgb_img.mode == "P": # NameError if color is indexed
                        T2_rgb_img = T2_rgb_img.convert("RGB")
                        sg.Print('Note: image converted from "P" (indexed color) mode to "RGB"')
                    if event == "T2_preview":
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
                    T2_exposures = [float(values["T2_exposure"+str(i)]) for i in range(T2_vis)]
                    T2_max_exposure = max(T2_exposures)
                    for i in range(T2_vis):
                        T2_bw_img = Image.open(values["T2_path"+str(i)])
                        if T2_bw_img.mode not in ("L", "I", "F"): # image should be b/w
                            sg.Print(f'Note: image of band {i+1} converted from "{T2_bw_img.mode}" mode to "L"')
                            T2_bw_img = T2_bw_img.convert("L")
                        if i == 0:
                            T2_size = T2_bw_img.size
                        else:
                            if T2_size != T2_bw_img.size:
                                sg.Print(f'Note: image of band {i+1} resized from {T2_bw_img.size} to {T2_size}')
                                T2_bw_img = T2_bw_img.resize(T2_size)
                        if event == "T2_preview":
                            T2_ratio = T2_bw_img.width / T2_bw_img.height
                            T2_bw_img = T2_bw_img.resize((int(np.sqrt(T2_area*T2_ratio)), int(np.sqrt(T2_area/T2_ratio))), resample=Image.Resampling.HAMMING)
                        T2_load.append(np.array(T2_bw_img) / T2_exposures[i] * T2_max_exposure)
                
                T2_data = np.array(T2_load, "int64")
                T2_l, T2_h, T2_w = T2_data.shape
                
                if values["T2_autoalign"]:
                    T2_data = scr.experimental.autoalign(T2_data, debug)
                    
                T2_data = T2_data.astype("float32")
                T2_max = T2_data.max()
                if values["T2_makebright"]:
                    T2_data *= 65500 / T2_max
                    T2_input_bit = 16
                    T2_input_depth = 65535
                else:
                    T2_input_bit = 16 if T2_max > 255 else 8
                    T2_input_depth = 65535 if T2_max > 255 else 255
                #T2_data = np.clip(T2_data, 0, T2_input_depth)
                
                # Calibration of maps by spectrum (legacy)
                #if info["calib"]:
                #    if "br" in info:
                #        br = np.array(info["br"])
                #        obl = 0
                #    elif "ref" in info:
                #        ref = calc.transform(db.objects[info["ref"]])
                #        albedo = ref["albedo"] if "albedo" in ref else 0
                #        br = calc.get_points(bands, ref["nm"], ref["br"], albedo)
                #        obl = ref["obl"] if "obl" in ref else 0
                #    for u in range(n): # calibration cycles
                #        for y in range(h):
                #            for layer in range(l):
                #                if np.sum(data[layer][y]) != 0:
                #                    calib[layer][0].append(np.sum(data[layer][y]) / np.count_nonzero(data[layer][y]))
                #                    calib[layer][1].append(k(np.pi * (0.5 - (y + 0.5) / h), obl))
                #        for layer in range(l):
                #            avg = np.average(calib[layer][0], weights=calib[layer][1])
                #            color = depth * br[layer]
                #            data[layer] = data[layer] * color / avg

                T2_fast = True if values["T2_interp1"] else False
                T2_nm = cmf.xyz_nm if input_data["srgb"] else cmf.rgb_nm
                T2_img = Image.new("RGB", (T2_w, T2_h), (0, 0, 0))
                T2_draw = ImageDraw.Draw(T2_img)
                T2_counter = 0
                T2_px_num = T2_w*T2_h
                
                if values["T2_plotpixels"]:
                    T2_fig = go.Figure()
                    T2_fig.update_layout(title=tr.map_title_text[lang], xaxis_title=tr.xaxis_text[lang], yaxis_title=tr.yaxis_text[lang])

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
                            T2_curve = calc.polator(input_data["nm"], list(T2_spectrum), T2_nm, fast=T2_fast, desun=input_data["desun"])
                            T2_calc_polator_time += time.monotonic_ns() - T2_temp_time

                            T2_temp_time = time.monotonic_ns()
                            T2_rgb = calc.to_rgb(T2_name, T2_curve, mode="albedo", albedo=True, inp_bit=T2_input_bit, exp_bit=8, gamma=input_data["gamma"])
                            T2_calc_rgb_time += time.monotonic_ns() - T2_temp_time

                            T2_temp_time = time.monotonic_ns()
                            T2_draw.point((x, y), T2_rgb)
                            T2_draw_point_time += time.monotonic_ns() - T2_temp_time

                            if values["T2_plotpixels"]:
                                T2_temp_time = time.monotonic_ns()
                                if x % 32 == 0 and y % 32 == 0:
                                    T2_fig.add_trace(go.Scatter(
                                        x = T2_nm,
                                        y = T2_curve,
                                        name = T2_name,
                                        line = dict(color="rgb"+str(T2_rgb), width=2)
                                        ))
                                T2_plot_pixels_time += time.monotonic_ns() - T2_temp_time
                        
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
                sg.Print(f'\t{round(T2_end_time-T2_time-(T2_get_spectrum_time+T2_calc_polator_time+T2_calc_rgb_time+T2_draw_point_time+T2_plot_pixels_time+T2_progress_bar_time)/1e9, 3)} sec for other (time, black-pixel check)')
                
                if values["T2_plotpixels"]:
                    T2_fig.show()
                if event == "T2_preview":
                    window["T2_image"].update(data=convert_to_bytes(T2_img))
                else:
                    T2_img.save(f'{values["T2_folder"]}/TCT_{time.strftime("%Y-%m-%d_%H-%M")}.png')
            
                #except Exception as e:
                #    print(e)
        
        # ------------ Events in the tab "Table" ------------

        elif event.startswith("T3"):
            
            if values["T3_folder"] != "":
                window["T3_process"].update(disabled=False)

            if event == "T3_process":

                # Database preprocessing
                if values["T3_tags"] == "all":
                    T3_data = db.objects
                    T3_l = len(T3_data)
                else:
                    T3_data = {}
                    T3_l = 0
                    for name, spectrum in db.objects.items():
                        if "tags" in spectrum:
                            if values["T3_tags"] in spectrum["tags"]:
                                T3_data.update({name: spectrum})
                                T3_l += 1
                for i in range(3):
                    if values["T3_br_mode"+str(i)]:
                        T3_mode0 = br_modes[i]
                
                denumerized_sources_list = denumerized_sources(db.sources)
                adapted_sources_list = []
                orig_num_list = []
                redirect_list = []

                # Layout
                T3_num = 15 # objects per row
                T3_r = 46 # half a side of a square
                T3_rr = 4 # rounding radius
                T3_ar = T3_r-4 # active space
                if T3_l < 11:
                    T3_w = 1200
                elif T3_l < T3_num:
                    T3_w = 100*(T3_l + 1)
                else:
                    T3_w = 1600
                T3_s = len(denumerized_sources_list)
                T3_name_step = 75
                T3_objt_size = 17
                T3_srce_size = 9
                T3_srce_step = 3 * T3_srce_size
                T3_note_size = 16
                T3_note_step = 4 + T3_note_size
                T3_auth_size = 10
                T3_h0 = T3_name_step + 100 * int(np.ceil(T3_l / T3_num) + 1)
                T3_h1 = T3_h0 + T3_s * T3_srce_step
                T3_w0 = 100 - T3_r
                T3_w1 = int(T3_w * 0.618034) # golden ratio
                T3_img = Image.new("RGB", (T3_w, T3_h1 + 50), (0, 0, 0))
                T3_draw = ImageDraw.Draw(T3_img)
                try:
                    T3_name_font = ImageFont.truetype("arial.ttf", 40)
                    T3_help_font = ImageFont.truetype("arial.ttf", 18)
                    T3_objt_font = ImageFont.truetype("ARIALN.TTF", T3_objt_size)
                    T3_smll_font = ImageFont.truetype("arial.ttf", 12)
                    T3_srce_font = ImageFont.truetype("arial.ttf", T3_srce_size)
                    T3_note_font = ImageFont.truetype("arial.ttf", T3_note_size)
                except OSError: # Linux
                    T3_name_font = ImageFont.truetype("/usr/share/fonts/truetype/NotoSans-Regular.ttf", 40)
                    T3_help_font = ImageFont.truetype("/usr/share/fonts/truetype/NotoSans-Regular.ttf", 18)
                    T3_objt_font = ImageFont.truetype("/usr/share/fonts/truetype/NotoSans-Condensed.ttf", T3_objt_size)
                    T3_smll_font = ImageFont.truetype("/usr/share/fonts/truetype/NotoSans-Regular.ttf", 12)
                    T3_srce_font = ImageFont.truetype("/usr/share/fonts/truetype/NotoSans-Regular.ttf", T3_srce_size)
                    T3_note_font = ImageFont.truetype("/usr/share/fonts/truetype/NotoSans-Regular.ttf", T3_note_size)
                # text brightness formula: br = 255 * (x^(1/2.2))
                T3_draw.text((T3_w0, 50), values["T3_tags"].join(tr.name_text[lang]), fill=(255, 255, 255), font=T3_name_font) # x = 1, br = 255
                T3_draw.text((T3_w0, T3_h0 - 25), tr.source[lang]+":", fill=(230, 230, 230), font=T3_help_font) # x = 0.8, br = 230
                T3_draw.text((T3_w1, T3_h0 - 25), tr.note[lang]+":", fill=(230, 230, 230), font=T3_help_font) # x = 0.8, br = 230
                T3_note_num = 0
                for note, translation in tr.notes.items(): # x = 0.6, br = 202
                    T3_draw.multiline_text((T3_w1, T3_h0 + T3_note_step * T3_note_num), f'{note} {translation[lang]}', fill=(202, 202, 202), font=T3_note_font)
                    T3_note_num += 1
                T3_info_num = 1
                for info_num, info in enumerate([T3_mode0, values["T3_srgb"], values["T3_gamma"]]): # x = 0.75, br = 224
                    T3_draw.multiline_text((T3_w1, T3_h0 + T3_note_step * (T3_note_num + info_num + 1)), f'{tr.info[lang][info_num]}: {info}', fill=(224, 224, 224), font=T3_note_font)
                    T3_info_num += 1
                T3_draw.multiline_text((T3_w1, T3_h0 + T3_note_step * (T3_note_num + T3_info_num)), tr.link, fill=(0, 200, 255), font=T3_note_font)
                
                # Table generator

                T3_nm = cmf.xyz_nm if values["T3_srgb"] else cmf.rgb_nm
            
                T3_n = 0 # object counter
                for name, spectrum in T3_data.items():
                    T3_mode = T3_mode0

                    # Spectral data import and processing
                    T3_albedo = 0
                    if "albedo" not in spectrum:
                        if T3_mode == "albedo":
                            T3_mode = "chromaticity"
                        spectrum.update({"albedo": False})
                    elif type(spectrum["albedo"]) != bool:
                        T3_albedo = spectrum["albedo"]
                    spectrum = calc.transform(spectrum)
                    
                    # Spectrum interpolation
                    T3_sun = False
                    if "sun" in spectrum:
                        T3_sun = spectrum["sun"]
                    T3_curve = calc.polator(spectrum["nm"], spectrum["br"], T3_nm, T3_albedo, desun=T3_sun)

                    # Color calculation
                    T3_rgb = calc.to_rgb(
                        name, T3_curve, mode=T3_mode,
                        albedo = spectrum["albedo"] or T3_albedo,
                        exp_bit=8, gamma=values["T3_gamma"], srgb=values["T3_srgb"]
                    )

                    # Object drawing
                    center_x = 100 * (1 + T3_n%T3_num)
                    center_y = T3_name_step + 100 * int(1 + T3_n/T3_num)
                    T3_draw.rounded_rectangle((center_x-T3_r, center_y-T3_r, center_x+T3_r, center_y+T3_r), radius=T3_rr, fill=T3_rgb)
                    
                    T3_text_color = (0, 0, 0) if np.mean(T3_rgb) >= 127 else (255, 255, 255)
                    
                    if name[0] == "(": # Name processing
                        parts = name.split(")", 1)
                        name = parts[1].strip()
                        T3_draw.text((center_x-T3_ar, center_y-T3_ar), f"({parts[0][1:]})", fill=T3_text_color, font=T3_smll_font)
                    elif "/" in name:
                        parts = name.split("/", 1)
                        name = parts[1].strip()
                        T3_draw.text((center_x-T3_ar, center_y-T3_ar), f"{parts[0]}/", fill=T3_text_color, font=T3_smll_font)
                    
                    if "|" in name:
                        name, link = name.split("|")
                        name = name.strip()
                        new_link = []
                        for i in link.split(", "):
                            orig_num = int(i)-1 # source number
                            if orig_num in orig_num_list: # it was already numbered
                                new_link.append(str(redirect_list[orig_num_list.index(orig_num)]))
                            else:
                                orig_num_list.append(orig_num)
                                srce_num = len(orig_num_list) # its new number
                                redirect_list.append(srce_num)
                                adapted_sources_list.append(denumerized_sources_list[orig_num])
                                new_link.append(str(srce_num))
                                T3_draw.multiline_text((T3_w0, T3_h1 + (srce_num-1 - T3_s) * T3_srce_step), f'[{srce_num}] {adapted_sources_list[-1]}', fill=(186, 186, 186), font=T3_srce_font) # x = 0.5, br = 186
                        new_link = f'[{", ".join(new_link)}]'
                        T3_draw.text((center_x+T3_ar-width(new_link, T3_smll_font), center_y-T3_ar), new_link, fill=T3_text_color, font=T3_smll_font)
                    
                    if lang != "en":
                        for obj_name, tranlation in tr.names.items():
                            if name.startswith(obj_name):
                                name = name.replace(obj_name, tranlation[lang])
                    
                    T3_splitted = line_splitter(name, T3_objt_font, T3_ar*2)
                    shift = T3_objt_size/2 if len(T3_splitted) == 1 else T3_objt_size
                    T3_draw.multiline_text((center_x-T3_ar, center_y-shift), "\n".join(T3_splitted), fill=T3_text_color, font=T3_objt_font, spacing=5)
                    
                    T3_n += 1
                    # print(export(T3_rgb), name)
                
                T3_file_name = f'TCT-table_{values["T3_tags"]}{"_srgb" if values["T3_srgb"] else ""}_{T3_mode}{"_gamma-corrected" if values["T3_gamma"] else ""}_{lang}.{values["T3_extension"]}'
                T3_s2 = len(adapted_sources_list)
                T3_h2 = T3_h1 + (T3_s2 - T3_s) * T3_srce_step
                T3_min_limit = T3_h0 + T3_note_step * (T3_note_num + T3_info_num + 1)
                T3_img = T3_img.crop((0, 0, T3_w, T3_h2+50 if T3_h2 > T3_min_limit else T3_min_limit+50))
                T3_img.save(f'{values["T3_folder"]}/{T3_file_name}')
                # T3_img.show()
                print("Done, saved as", T3_file_name, "\n")
        
        # ------------ Events in the tab "Blackbody & Redshifts" ------------
        
        elif event.startswith("T4"):
            
            if event == "T4_maxtemp_num":
                window["T4_slider1"].update(range=(0, int(values["T4_maxtemp_num"])))
            
            else:
                if event == "T4_surfacebr":
                    window["T4_scale"].update(text_color=T4_text_colors[values["T4_surfacebr"]])
                    window["T4_slider4"].update(disabled=not values["T4_surfacebr"])
                
                T4_mode = "albedo" if values["T4_surfacebr"] else "chromaticity"
                T4_nm = cmf.xyz_nm if values["T4_srgb"] else cmf.rgb_nm
                T4_curve = calc.blackbody_redshift(T4_nm, values["T4_slider1"], values["T4_slider2"], values["T4_slider3"])
                if values["T4_surfacebr"]:
                    try:
                        T4_curve /= calc.mag2intensity(values["T4_slider4"])
                    except np.core._exceptions.UFuncTypeError:
                        pass
                T4_name = f'{values["T4_slider1"]} {values["T4_slider2"]} {values["T4_slider3"]}'
                T4_rgb = calc.to_rgb(
                    T4_name, T4_curve, mode=T4_mode,
                    albedo=values["T4_surfacebr"],
                    exp_bit=int(values["T4_bit_num"]),
                    gamma=values["T4_gamma"],
                    rnd=int(values["T4_rnd_num"]),
                    srgb=values["T4_srgb"]
                )
                T4_rgb_show = calc.to_rgb(
                    T4_name, T4_curve, mode=T4_mode,
                    albedo=values["T4_surfacebr"],
                    gamma=values["T4_gamma"],
                    srgb=values["T4_srgb"],
                    html=True
                )
            
                # Output
                window["T4_graph"].TKCanvas.itemconfig(T4_preview, fill=T4_rgb_show)
                window["T4_rgb"].update(T4_rgb)
                window["T4_hex"].update(T4_rgb_show)

    window.close()