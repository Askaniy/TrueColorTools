import PySimpleGUI as sg
import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import plotly.graph_objects as go
import user, cmf, filters
import calculations as calc
import database as db
import strings as tr

lang = user.lang("en") # ReadMe -> FAQ -> Localization


def tag_list():
    tag_set = set(["all"])
    for data in db.objects.values():
        if "tags" in data:
            tag_set.update(data["tags"])
    return list(tag_set)

def obj_list(tag="all"):
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

short_list = ["I", "i", "j", "l", "f", "r", "t", "[", "]", "/", ":", "*", "°", ".", " "]
T3_max_width = 11
def width(line):
    w = 0
    for letter in line:
        if letter in short_list:
            w += 0.5
        elif letter.isupper():
            w += 1.5
        else:
            w += 1
    return w

def recurse(lst):
    w_list = []
    for i in lst:
        w_list.append(width(i))
    if max(w_list) < T3_max_width:
        for i in range(len(w_list)-1):
            if w_list[i]+w_list[i+1] < T3_max_width:
                lst[i] += " " + lst[i+1]
                lst.pop(i+1)
                recurse(lst)
                break
    else:
        for i in range(len(lst)):
            if width(lst[i]) > T3_max_width:
                try:
                    lst[i+1] = lst[i][-1] + lst[i+1]
                except IndexError:
                    lst.append(lst[i][-1])
                finally:
                    lst[i] = lst[i][:-1]
                while width(lst[i]) >= T3_max_width:
                    lst[i+1] = lst[i][-1] + lst[i+1]
                    lst[i] = lst[i][:-1]
                recurse(lst)
                break
    return lst
    
def line_splitter(line):
    w = width(line)
    if w < T3_max_width:
        return [line]
    else:
        return recurse(line.split())

def convert_to_bytes(img):
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

def frame(num):
    n = str(num)
    l = [
        [sg.Input(size=(20, 1), disabled=False, disabled_readonly_background_color="#3A3A3A", key="T2_path"+n), sg.FileBrowse(button_text=tr.gui_browse[lang], size=(10, 1), disabled=False, key="T2_browse"+n)],
        [sg.Text(tr.gui_filter[lang], size=(14, 1), text_color="#A3A3A3", key="T2_filterN"+n), sg.InputCombo([], size=(12, 1), disabled=True, enable_events=True, key="T2_filter"+n)],
        [sg.Text(tr.gui_wavelength[lang], size=(14, 1), key="T2_wavelengthN"+n), sg.Input(size=(14, 1), disabled_readonly_background_color="#3A3A3A", disabled=False, enable_events=True, key="T2_wavelength"+n)]
    ]
    return sg.Frame(f"{tr.gui_band[lang]} {num+1}", l, visible=num < T2_vis, key="T2_band"+n)


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
    [sg.Text(tr.gui_tags[lang], size=(7, 1), key="T1_tagsN"), sg.InputCombo(tag_list(), default_value="featured", size=(16, 1), enable_events=True, key="T1_tags")],
    [sg.Listbox(values=tuple(obj_list(tag="featured").keys()), size=(25, 22), enable_events=True, key="T1_list")]
]
T1_col2 = [
    [sg.Text(tr.gui_settings[lang], size=(16, 1), font=("arial", 12), key="T1_title2")],
    [sg.Checkbox(tr.gui_gamma[lang], size=(16, 1), enable_events=True, default=True, key="T1_gamma")],
    [sg.Checkbox("sRGB", enable_events=True, size=(16, 1), key="T1_srgb")],
    [sg.HorizontalSeparator()],
    [sg.Text(tr.gui_br[lang][0], size=(20, 1), key="T1_br_mode")],
    [sg.Radio(tr.gui_br[lang][1], "T1_rad", size=(15, 1), enable_events=True, default=True, key="T1_br_mode0")],
    [sg.Radio(tr.gui_br[lang][2], "T1_rad", size=(15, 1), enable_events=True, key="T1_br_mode1")],
    [sg.Radio(tr.gui_br[lang][3], "T1_rad", size=(15, 1), enable_events=True, key="T1_br_mode2")],
    [sg.HorizontalSeparator()],
    [sg.Text(tr.gui_phase[lang], size=(20, 1), key="T1_phase")],
    [sg.Slider(range=(-180, 180), default_value=0, resolution=1, orientation="h", size=(18, 16), enable_events=True, key="T1_slider")],
    [sg.HorizontalSeparator()],
    [sg.Text(tr.gui_interp[lang][0], size=(20, 1), key="T1_interp")],
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
T2_col1 = [
    [sg.Text(tr.gui_input[lang], size=(20, 1), font=("arial", 12), key="T2_title1"), sg.Button(button_text="+", size=(2, 1), key="T2_+"), sg.Button(button_text="-", size=(2, 1), disabled=False, key="T2_-")],
    [frame(0)],
    [frame(1)],
    [frame(2)],
    [frame(3)],
    [frame(4)],
    [frame(5)],
    [frame(6)],
    [frame(7)],
    [frame(8)],
    [frame(9)] # just add more frames here
]
T2_col2 = [
    [sg.Text(tr.gui_output[lang], size=(30, 1), font=("arial", 12), key="T2_title2")],
    [sg.Checkbox(tr.gui_gamma[lang], size=(17, 1), key="T2_gamma"),
    sg.Radio(tr.gui_interp[lang][1], "T2_interp", size=(12, 1), enable_events=True, default=True, key="T2_interp0")],
    [sg.Checkbox("sRGB", size=(17, 1), key="T2_srgb"),
    sg.Radio(tr.gui_interp[lang][2], "T2_interp", size=(12, 1), enable_events=True, key="T2_interp1")],
    [sg.HorizontalSeparator()],
    [sg.Checkbox(tr.gui_single[lang], size=(22, 1), enable_events=True, key="T2_single")],
    [sg.Input(size=(32, 1), disabled=True, disabled_readonly_background_color="#3A3A3A", key="T2_path"), sg.FileBrowse(button_text=tr.gui_browse[lang], size=(10, 1), disabled=True, key="T2_browse")],
    [sg.Checkbox(tr.gui_system[lang], size=(26, 1), enable_events=True, key="T2_system")],
    [sg.InputCombo(filters.get_sets(), size=(26, 1), enable_events=True, disabled=True, key="T2_filter")],
    [sg.T("")],
    [sg.Text(tr.gui_folder[lang], size=(22, 1), key="T2_folderN")],
    [sg.Input(size=(32, 1), enable_events=True, key="T2_folder"), sg.FolderBrowse(button_text=tr.gui_browse[lang], size=(10, 1), key="T2_browse_folder")],
    [sg.Button(tr.gui_preview[lang], size=(15, 1), disabled=True, key="T2_show"), sg.Button(tr.gui_process[lang], size=(15, 1), disabled=True, key="T2_process")],
    [sg.Image(background_color="black", size=T2_preview, key="T2_preview")]
]
T2_num = len(T2_col1) - 1

T3_col1 = [
    [sg.Text(tr.gui_settings[lang], size=(20, 1), font=("arial", 12), key="T3_title1")],
    [sg.Text(tr.gui_tags[lang], size=(7, 1), key="T3_tagsN"), sg.InputCombo(tag_list(), default_value="featured", size=(16, 1), enable_events=True, key="T3_tags")],
    [sg.HorizontalSeparator()],
    [sg.Checkbox(tr.gui_gamma[lang], size=(16, 1), enable_events=True, default=True, key="T3_gamma")],
    [sg.Checkbox("sRGB", enable_events=True, size=(16, 1), key="T3_srgb")],
    [sg.HorizontalSeparator()],
    [sg.Text(tr.gui_br[lang][0], size=(18, 1), key="T3_br_mode")],
    [sg.Radio(tr.gui_br[lang][1], "T3_rad", size=(15, 1), enable_events=True, default=True, key="T3_br_mode0")],
    [sg.Radio(tr.gui_br[lang][2], "T3_rad", size=(15, 1), enable_events=True, key="T3_br_mode1")],
    [sg.Radio(tr.gui_br[lang][3], "T3_rad", size=(15, 1), enable_events=True, key="T3_br_mode2")],
    [sg.HorizontalSeparator()],
    [sg.Checkbox(tr.gui_signature[lang], size=(16, 1), enable_events=True, default=False, key="T3_signature")]
]
T3_col2 = [
    [sg.Text(tr.gui_results[lang], size=(30, 1), font=("arial", 12), key="T3_title2")],
    [sg.Text(tr.gui_extension[lang], size=(15, 1), key="T3_ext"), sg.InputCombo(["png", "jpeg"], default_value="png", size=(10, 1), enable_events=True, key="T3_extension")],
    [sg.Text(tr.gui_folder[lang], size=(15, 1), key="T3_folderN"), sg.Input(size=(16, 1), enable_events=True, key="T3_folder"), sg.FolderBrowse(button_text=tr.gui_browse[lang], size=(10, 1), key="T3_browse_folder")],
    [sg.T("")],
    [sg.Button(tr.gui_process[lang], size=(15, 1), disabled=True, key="T3_process")]
]

slider_size = (28, 16)
T4_text_colors = ("#A3A3A3", "#FFFFFF")
T4_col1 = [
    [sg.Text(tr.gui_input[lang], size=(16, 1), font=("arial", 12), key="T4_title1")],
    [sg.Text(tr.gui_temp[lang], size=(15, 1), key="T4_temp"), sg.Slider(range=(0, 20000), default_value=0, resolution=100, orientation="h", size=slider_size, enable_events=True, key="T4_slider1")],
    [sg.Text(tr.gui_velocity[lang], size=(15, 1), key="T4_velocity"), sg.Slider(range=(-1, 1), default_value=0, resolution=0.01, orientation="h", size=slider_size, enable_events=True, key="T4_slider2")],
    [sg.Text(tr.gui_vI[lang], size=(15, 1), key="T4_vI"), sg.Slider(range=(0, 1), default_value=0, resolution=0.01, orientation="h", size=slider_size, enable_events=True, key="T4_slider3")],
    [sg.Text(tr.gui_scale[lang], size=(15, 1), text_color=T4_text_colors[0], key="T4_scale"), sg.Slider(range=(-10, 10), default_value=0, resolution=0.1, orientation="h", size=slider_size, enable_events=True, disabled=True, key="T4_slider4")],
    [sg.T("")],
    [sg.HorizontalSeparator()],
    [sg.Checkbox(tr.gui_irr[lang], size=(20, 1), enable_events=True, default=False, key="T4_irr"),
    sg.Text(tr.gui_maxtemp[lang], size=(12, 1), key="T4_maxtemp"), sg.InputText("20000", size=(8, 1), enable_events=True, key="T4_maxtemp_num")],
    [sg.Checkbox(tr.gui_gamma[lang], size=(20, 1), enable_events=True, default=True, key="T4_gamma"),
    sg.Text(tr.gui_bit[lang], size=(12, 1), key="T4_bit"), sg.InputText("8", size=(4, 1), enable_events=True, key="T4_bit_num")],
    [sg.Checkbox("sRGB", enable_events=True, size=(20, 1), key="T4_srgb"),
    sg.Text(tr.gui_rnd[lang], size=(12, 1), key="T4_rnd"), sg.InputText("3", size=(4, 1), enable_events=True, key="T4_rnd_num")]
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
    [sg.Column(T1_col1), sg.VSeperator(), sg.Column(T1_col2), sg.VSeperator(), sg.Column(T1_col3)]
]
tab2 = [
    [sg.Column(T2_col1), sg.VSeperator(), sg.Column(T2_col2)]
]
tab3 = [
    [sg.Column(T3_col1), sg.VSeperator(), sg.Column(T3_col2)]
]
tab4 = [
    [sg.Column(T4_col1), sg.VSeperator(), sg.Column(T4_col2)]
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

window = sg.Window("True Color Tools", layout)    
window.Finalize()
T1_preview = window["T1_graph"].DrawCircle((48, 46), 42, fill_color="black", line_color="white")
T4_preview = window["T4_graph"].DrawCircle((48, 46), 42, fill_color="black", line_color="white")

T1_fig = go.Figure()
T1_events = ["T1_list", "T1_gamma", "T1_srgb", "T1_br_mode0", "T1_br_mode1", "T1_br_mode2", "T1_interp0", "T1_interp1", "T1_slider", "T1_bit_num", "T1_rnd_num"]
br_modes = ["chromaticity", "albedo 0.5", "albedo"]


# Window events loop

names = []
while True:
    event, values = window.Read()

    # Global window events

    if event in [sg.WIN_CLOSED, tr.gui_exit[lang]]:
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
        window["T1_list"].update(values=tuple(obj_list(tag=values["T1_tags"]).keys()))
        window["T1_br_mode"].update(tr.gui_br[lang][0])
        window["T1_phase"].update(tr.gui_phase[lang])
        window["T1_interp"].update(tr.gui_interp[lang][0])
        window["T1_bit"].update(tr.gui_bit[lang])
        window["T1_rnd"].update(tr.gui_rnd[lang])
        window["T1_colorRGB"].update(tr.gui_rgb[lang])
        window["T1_colorHEX"].update(tr.gui_hex[lang])
        window["T1_add"].update(tr.gui_add[lang])
        window["T1_plot"].update(tr.gui_plot[lang])
        window["T1_export"].update(tr.gui_export[lang])
        window["T2_title1"].update(tr.gui_input[lang])
        window["T2_title2"].update(tr.gui_output[lang])
        #window["T2_single"].update(tr.gui_single[lang])
        window["T2_browse"].update(tr.gui_browse[lang])
        for i in range(T2_num):
            window["T2_browse"+str(i)].update(tr.gui_browse[lang])
            window["T2_filterN"+str(i)].update(tr.gui_filter[lang])
            window["T2_wavelengthN"+str(i)].update(tr.gui_wavelength[lang])
            window["T2_band"+str(i)].update(f"{tr.gui_band[lang]} {i+1}")
        #window["T2_gamma"].update(tr.gui_gamma[lang])
        #window["T2_system"].update(tr.gui_system[lang])
        window["T2_folderN"].update(tr.gui_folder[lang])
        window["T2_browse_folder"].update(tr.gui_browse[lang])
        window["T2_show"].update(tr.gui_preview[lang])
        window["T2_process"].update(tr.gui_process[lang])
        window["T3_title1"].update(tr.gui_settings[lang])
        window["T3_title2"].update(tr.gui_results[lang])
        window["T3_tagsN"].update(tr.gui_tags[lang])
        window["T3_br_mode"].update(tr.gui_br[lang][0])
        #window["T3_signature"].update(tr.gui_signature[lang])
        window["T3_ext"].update(tr.gui_extension[lang])
        window["T3_browse_folder"].update(tr.gui_browse[lang])
        window["T3_folderN"].update(tr.gui_folder[lang])
        window["T3_process"].update(tr.gui_process[lang])
        window["T4_title1"].update(tr.gui_input[lang])
        window["T4_title2"].update(tr.gui_results[lang])
        window["T4_temp"].update(tr.gui_temp[lang])
        window["T4_velocity"].update(tr.gui_velocity[lang])
        window["T4_vI"].update(tr.gui_vI[lang])
        window["T4_scale"].update(tr.gui_scale[lang])
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
        sg.popup("https://github.com/Askaniy/TrueColorTools\n"+tr.auth_info[lang], title=event)
    
    # ------------ Events in the tab "Spectra" ------------

    elif event.startswith("T1"):

        if event in T1_events and values["T1_list"] != []:
            T1_nm = cmf.xyz_nm if values["T1_srgb"] else cmf.rgb_nm
            for i in range(3):
                if values["T1_br_mode"+str(i)]:
                    T1_mode = br_modes[i]

            # Spectral data import and processing
            T1_spectrum = db.objects[obj_list()[values["T1_list"][0]]]
            T1_albedo = 0
            if "albedo" not in T1_spectrum:
                if T1_mode == "albedo":
                    T1_mode = "chromaticity"
                T1_spectrum.update({"albedo": False})
            elif type(T1_spectrum["albedo"]) != bool:
                T1_albedo = T1_spectrum["albedo"]
            T1_spectrum = calc.transform(T1_spectrum)
            
            # Spectrum interpolation
            T1_curve = calc.polator(T1_spectrum["nm"], T1_spectrum["br"], T1_nm, T1_albedo, values["T1_interp1"])
            
            # Color calculation
            try:
                T1_phase = 0 if "star" in T1_spectrum["tags"] else values["T1_slider"]
            except Exception:
                T1_phase = values["T1_slider"]
            T1_rgb = calc.to_rgb(
                T1_curve, mode=T1_mode,
                albedo = T1_spectrum["albedo"] or T1_albedo,
                phase=T1_phase,
                exp_bit=int(values["T1_bit_num"]), 
                gamma=values["T1_gamma"], 
                rnd=int(values["T1_rnd_num"]),
                srgb=values["T1_srgb"]
            )
            T1_rgb_show = calc.to_rgb(
                T1_curve, mode=T1_mode,
                albedo = T1_spectrum["albedo"] or T1_albedo,
                phase=T1_phase,
                gamma=values["T1_gamma"],
                srgb=values["T1_srgb"],
                html=True
            )
            if not np.array_equal(np.absolute(T1_rgb), T1_rgb):
                T1_rgb_show = "#000000"
                print("\n" + tr.error2[lang][0])
                print(tr.error2[lang][1].format(values["T1_list"][0], *T1_rgb) + "\n")
                #break

            # Output
            window["T1_graph"].TKCanvas.itemconfig(T1_preview, fill=T1_rgb_show)
            window["T1_rgb"].update(T1_rgb)
            window["T1_hex"].update(T1_rgb_show)
        
        elif event == "T1_tags":
            window["T1_list"].update(tuple(obj_list(tag=values["T1_tags"]).keys()))
        
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
            for name_1, name_0 in obj_list(tag=values["T1_tags"]).items():
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
                T1_curve = calc.polator(T1_spectrum["nm"], T1_spectrum["br"], T1_nm, T1_albedo, values["T1_interp1"])

                # Color calculation
                T1_rgb = calc.to_rgb(
                    T1_curve, mode=T1_mode,
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
            if values["T2_single"]:
                T2_vis = 3
                for i in range(T2_num):
                    window["T2_band"+str(i)].update(visible=False)
                for i in range(3):
                    window["T2_band"+str(i)].update(visible=True)

        elif event == "T2_system":
            window["T2_filter"].update(disabled=not values["T2_system"])
            for i in range(T2_num):
                window["T2_filter"+str(i)].update(disabled=not values["T2_system"])
                window["T2_wavelength"+str(i)].update(disabled=values["T2_system"])

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
            window["T2_filterN"+str(i)].update(text_color=("#A3A3A3", "#FFFFFF")[values["T2_system"]])
            window["T2_wavelengthN"+str(i)].update(text_color=("#A3A3A3", "#FFFFFF")[not values["T2_system"]])
        
        input_data = {"gamma": values["T2_gamma"], "srgb": values["T2_srgb"], "nm": []}
        window["T2_show"].update(disabled=False)
        if values["T2_folder"] != "":
            window["T2_process"].update(disabled=False)
        if values["T2_system"]:
            for i in range(T2_vis):
                if bool(values["T2_filter"+str(i)]):
                    input_data["nm"].append(filters.get_param(values["T2_filter"], values["T2_filter"+str(i)], "L_mean"))
                else:
                    window["T2_show"].update(disabled=True)
                    window["T2_process"].update(disabled=True)
                    break
        else:
            for i in range(T2_vis):
                if values["T2_wavelength"+str(i)].replace(".", "").isnumeric():
                    input_data["nm"].append(float(values["T2_wavelength"+str(i)]))
                else:
                    window["T2_show"].update(disabled=True)
                    window["T2_process"].update(disabled=True)
                    break
        if not all(a > b for a, b in zip(input_data["nm"][1:], input_data["nm"])): # increasing check
            window["T2_show"].update(disabled=True)
            window["T2_process"].update(disabled=True)
        
        if event in ("T2_show", "T2_process"):
            try:
                load = []
                if values["T2_single"]:
                    if values["T2_path"] == "":
                        raise ValueError("Path is empty")
                    T2_rgb_img = Image.open(values["T2_path"])
                    if event == "T2_show":
                        T2_rgb_img = T2_rgb_img.resize(T2_preview, resample=Image.HAMMING)
                    if len(T2_rgb_img.getbands()) == 3:
                        r, g, b = T2_rgb_img.split()
                        a = False
                    elif len(T2_rgb_img.getbands()) == 4:
                        r, g, b, a = T2_rgb_img.split()
                    for i in [b, g, r]:
                        load.append(np.array(i))
                else:
                    for i in range(T2_vis):
                        if values["T2_path"+str(i)] == "":
                            raise ValueError(f'Path {i+1} is empty')
                        T2_bw_img = Image.open(values["T2_path"+str(i)])
                        if event == "T2_show":
                            T2_bw_img = T2_bw_img.resize(T2_preview, resample=Image.HAMMING)
                        if len(T2_bw_img.getbands()) != 1:
                            raise TypeError("Band image should be b/w")
                        load.append(np.array(T2_bw_img))
                
                T2_data = np.array(load, dtype="float32")
                T2_l = T2_data.shape[0] # number of maps
                T2_h = T2_data.shape[1] # height of maps
                T2_w = T2_data.shape[2] # width of maps
                
                T2_max = T2_data.max()
                if T2_max > 256:
                    T2_bit = 16
                    T2_depth = 65535
                elif T2_max < 2:
                    T2_bit = 0
                    T2_depth = 1
                else:
                    T2_bit = 8
                    T2_depth = 255
                T2_data = np.clip(T2_data, 0, T2_depth)
                
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
                counter = 0
                px_num = T2_w*T2_h
                
                T2_fig = go.Figure()
                T2_fig.update_layout(title=tr.map_title_text[lang], xaxis_title=tr.xaxis_text[lang], yaxis_title=tr.yaxis_text[lang])

                for x in range(T2_w):
                    for y in range(T2_h):
                        T2_spectrum = T2_data[:, y, x]
                        if np.sum(T2_spectrum) > 0:
                            T2_curve = calc.polator(input_data["nm"], list(T2_spectrum), T2_nm, fast=T2_fast)
                            T2_rgb = calc.to_rgb(T2_curve, mode="albedo", albedo=True, inp_bit=T2_bit, exp_bit=8, gamma=input_data["gamma"])
                            T2_draw.point((x, y), T2_rgb)
                            if x % 32 == 0 and y % 32 == 0:
                                T2_fig.add_trace(go.Scatter(
                                    x = T2_nm,
                                    y = T2_curve,
                                    name = px_num,
                                    line = dict(color="rgb"+str(T2_rgb), width=2)
                                    ))
                        counter += 1
                        sg.OneLineProgressMeter("Progress", counter, px_num)
                
                T2_fig.show()
                if event == "T2_show":
                    window["T2_preview"].update(data=convert_to_bytes(T2_img))
                else:
                    T2_img.save(values["T2_folder"]+"/TCT_result.png")
            
            except Exception as e:
                print(e)
    
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
            T3_rr = 5 # rounding radius
            if T3_l < 11:
                T3_w = 1200
            elif T3_l < T3_num:
                T3_w = 100*(T3_l + 1)
            else:
                T3_w = 1600
            T3_s = len(denumerized_sources_list)
            T3_name_step = 75
            T3_objt_size = 18
            T3_srce_size = 9
            T3_srce_step = 7 + 2 * T3_srce_size
            T3_note_size = 16
            T3_note_step = 4 + T3_note_size
            T3_auth_size = 10
            T3_h0 = T3_name_step + 100 * int(np.ceil(T3_l / T3_num) + 1)
            T3_h1 = T3_h0 + T3_s * T3_srce_step
            T3_w0 = 100 - T3_r
            T3_w1 = int(T3_w * 3/5)
            T3_img = Image.new("RGB", (T3_w, T3_h1 + 50), (0, 0, 0))
            T3_draw = ImageDraw.Draw(T3_img)
            T3_name_font = ImageFont.truetype("arial.ttf", 42)
            T3_help_font = ImageFont.truetype("arial.ttf", 18)
            T3_narr_font = ImageFont.truetype("ARIALN.TTF", T3_objt_size)
            T3_wide_font = ImageFont.truetype("arial.ttf", T3_objt_size)
            T3_link_font = ImageFont.truetype("arial.ttf", 12)
            T3_cnsl_font = ImageFont.truetype("consola.ttf", 12)
            T3_srce_font = ImageFont.truetype("arial.ttf", T3_srce_size)
            T3_note_font = ImageFont.truetype("arial.ttf", T3_note_size)
            T3_auth_font = ImageFont.truetype("arial.ttf", T3_auth_size)
            # text brightness formula: br = 255 * (x^(1/2.2))
            T3_draw.text((T3_w0, 50), values["T3_tags"].join(tr.name_text[lang]), fill=(255, 255, 255), font=T3_name_font) # x = 1, br = 255
            T3_draw.text((T3_w0, T3_h0 - 25), tr.source[lang]+":", fill=(230, 230, 230), font=T3_help_font) # x = 0.8, br = 230
            T3_draw.text((T3_w1, T3_h0 - 25), tr.note[lang]+":", fill=(230, 230, 230), font=T3_help_font) # x = 0.8, br = 230
            if values["T3_signature"]:
                T3_auth_step = 302 if lang == "ru" else 284
                T3_draw.text((T3_w - T3_auth_step, T3_h1 - T3_auth_size), tr.auth_info[lang], fill=(136, 136, 136), font=T3_help_font) # x = 0.25, br = 136
            T3_note_num = 0
            for note, translation in tr.notes.items(): # x = 0.6, br = 202
                T3_draw.multiline_text((T3_w1, T3_h0 + T3_note_step * T3_note_num), f'{note} {translation[lang]}', fill=(202, 202, 202), font=T3_note_font)
                T3_note_num += 1
            T3_info_num = 0
            for info_num, info in enumerate([T3_mode0, values["T3_srgb"], values["T3_gamma"]]): # x = 0.75, br = 224
                T3_draw.multiline_text((T3_w1, T3_h0 + T3_note_step * (T3_note_num + info_num + 1)), f'{tr.info[lang][info_num]}: {info}', fill=(224, 224, 224), font=T3_note_font)
                T3_info_num += 1
            
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
                T3_curve = calc.polator(spectrum["nm"], spectrum["br"], T3_nm, T3_albedo)

                # Color calculation
                T3_rgb = calc.to_rgb(
                    T3_curve, mode=T3_mode,
                    albedo = spectrum["albedo"] or T3_albedo,
                    exp_bit=8, gamma=values["T3_gamma"], srgb=values["T3_srgb"]
                )
                if not np.array_equal(np.absolute(T3_rgb), T3_rgb):
                    print("\n" + tr.error2[lang][0])
                    print(tr.error2[lang][1].format(name, *T3_rgb) + "\n")
                    break

                # Object drawing
                center_x = 100 * (1 + T3_n%T3_num)
                center_y = T3_name_step + 100 * int(1 + T3_n/T3_num)
                T3_draw.rounded_rectangle((center_x-T3_r, center_y-T3_r, center_x+T3_r, center_y+T3_r), radius=T3_rr, fill=T3_rgb)
                
                T3_text_color = (0, 0, 0) if np.mean(T3_rgb) >= 127 else (255, 255, 255)
                
                if name[0] == "(": # Name processing
                    parts = name.split(")", 1)
                    name = parts[1].strip()
                    T3_draw.text((center_x-42, center_y-36), f"({parts[0][1:]})", fill=T3_text_color, font=T3_link_font)
                elif "/" in name:
                    parts = name.split("/", 1)
                    name = parts[1].strip()
                    T3_draw.text((center_x-42, center_y-36), f"{parts[0]}/", fill=T3_text_color, font=T3_link_font)
                
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
                    T3_draw.text((center_x+38-7*(len(new_link)-1), center_y-42), new_link, fill=T3_text_color, font=T3_cnsl_font)
                
                if lang != "en":
                    for obj_name, tranlation in tr.names.items():
                        if name.startswith(obj_name):
                            name = name.replace(obj_name, tranlation[lang])
                
                T3_splitted = line_splitter(name)
                shift = T3_objt_size/2 if len(T3_splitted) == 1 else T3_objt_size
                T3_draw.multiline_text((center_x-42, center_y-shift), "\n".join(T3_splitted), fill=T3_text_color, font=T3_narr_font)
                
                T3_n += 1
                # print(export(T3_rgb), name)
            
            T3_s2 = len(adapted_sources_list)
            T3_h2 = T3_h1 + (T3_s2 - T3_s) * T3_srce_step
            T3_min_limit = T3_h0 + T3_note_step * (T3_note_num + info_num + 1)
            T3_img = T3_img.crop((0, 0, T3_w, T3_h2+50 if T3_h2 > T3_min_limit else T3_min_limit+50))
            T3_img.save(f'{values["T3_folder"]}/TCT-table_{values["T3_tags"]}{"_srgb" if values["T3_srgb"] else ""}_{T3_mode}{"_gamma-corrected" if values["T3_gamma"] else ""}_{lang}.{values["T3_extension"]}')
            T3_img.show()
    
    # ------------ Events in the tab "Blackbody & Redshifts" ------------
    
    elif event.startswith("T4"):
        
        if event == "T4_maxtemp_num":
            window["T4_slider1"].update(range=(0, int(values["T4_maxtemp_num"])))
        else:

            if event == "T4_irr":
                window["T4_scale"].update(text_color=T4_text_colors[values["T4_irr"]])
                window["T4_slider4"].update(disabled=not values["T4_irr"])
            
            T4_mode = "albedo" if values["T4_irr"] else "chromaticity"
            T4_nm = cmf.xyz_nm if values["T4_srgb"] else cmf.rgb_nm
            T4_curve = calc.blackbody_redshift(T4_nm, values["T4_slider1"], values["T4_slider2"], values["T4_slider3"])
            if values["T4_irr"]:
                try:
                    T4_curve *= 10**(-values["T4_slider4"])
                except np.core._exceptions.UFuncTypeError:
                    pass
            T4_rgb = calc.to_rgb(
                T4_curve, mode=T4_mode,
                albedo=values["T4_irr"],
                exp_bit=int(values["T4_bit_num"]), 
                gamma=values["T4_gamma"], 
                rnd=int(values["T4_rnd_num"]),
                srgb=values["T4_srgb"]
            )
            T4_rgb_show = calc.to_rgb(
                T4_curve, mode=T4_mode,
                albedo=values["T4_irr"],
                gamma=values["T4_gamma"],
                srgb=values["T4_srgb"],
                html=True
            )
        
            # Output
            window["T4_graph"].TKCanvas.itemconfig(T4_preview, fill=T4_rgb_show)
            window["T4_rgb"].update(T4_rgb)
            window["T4_hex"].update(T4_rgb_show)


window.Close()