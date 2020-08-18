import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import Akima1DInterpolator, PchipInterpolator, CubicSpline
import translator as tr
import spectra, convert
import PySimpleGUI as sg
sg.theme("DarkGrey6")
lang = "en"

def obj_list():
    global lang
    names = {}
    for name_0 in spectra.objects.keys():
        if "|" in name_0:
            name_1 = "{} [{}]".format(*name_0.split("|"))
        else:
            name_1 = name_0
        if lang != "en":
            for obj_name, tranlation in tr.names.items():
                if name_1.startswith(obj_name):
                    name_1 = name_1.replace(obj_name, tranlation[lang])
                    break
        names.update({name_1: name_0})
    return names

col1 = [
    [sg.Text(tr.columns[lang][0], size=(16, 1), font=("arial", 12), key="col0")],
    [sg.Listbox(values=tuple(obj_list().keys()), size=(20, 20), enable_events=True, key="list")]
]
col2 = [
    [sg.Text(tr.columns[lang][1], size=(16, 1), font=("arial", 12), key="col1")],
    [sg.Checkbox(tr.gui_gamma[lang], size=(16, 1), default=True, key="gamma")],
    [sg.Checkbox("sRGB", size=(16, 1), key="srgb")],
    [sg.Text(tr.gui_br[lang][0]+":", size=(18, 1), key="br0")],
    [sg.Radio(tr.gui_br[lang][1], "rad", size=(15, 1), default=True, key="br1")], # Cannot be translated 
    [sg.Radio(tr.gui_br[lang][2], "rad", size=(15, 1), key="br2")],               # due to parameter update issues
    [sg.Radio(tr.gui_br[lang][3], "rad", size=(15, 1), key="br3")],               # in sg.Radio and sg.Checkbox
    [sg.Text(tr.gui_interp[lang][0]+":", size=(18, 1), key="interp0")],
    [sg.Radio(tr.gui_interp[lang][1], "interp", size=(8, 1), default=True, key="interp1")],
    [sg.Radio(tr.gui_interp[lang][2], "interp", size=(6, 1), key="interp2"), sg.Radio(tr.gui_interp[lang][3], "interp", size=(6, 1), key="interp3")],
    [sg.Text(tr.gui_bit[lang]+":", size=(12, 1), key="bit"), sg.InputText("8", size=(4, 1), key="bit_num")],
    [sg.Text(tr.gui_rnd[lang]+":", size=(12, 1), key="rnd"), sg.InputText("3", size=(4, 1), key="rnd_num")],
    [sg.Button(button_text=tr.gui_apply[lang], key="apply")]
]
col3 = [
    [sg.Text(tr.columns[lang][2], size=(16, 1), font=("arial", 12), key="col2")],
    [sg.Graph(canvas_size=(180, 165), graph_bottom_left=(0, 0), graph_top_right=(100, 100), background_color=None, key="graph")],
    [sg.Text(tr.gui_rgb[lang]+":", size=(8, 1), key="colorRGB")],
    [sg.In(size=(26, 1), key="rgb")],
    [sg.Text(tr.gui_hex[lang]+":", size=(8, 1), key="colorHEX"), sg.In(size=(8, 1), key="hex")],
    [sg.Text("_" * 32, size=(22, 1))],
    [sg.Button(button_text=tr.gui_add[lang], key="add")],
    [sg.Button(button_text=tr.gui_plot[lang], key="plot")]
]
layout = [
    [sg.Menu(tr.gui_menu[lang], key="menu")],
    [sg.Column(col1), sg.VSeperator(), sg.Column(col2), sg.VSeperator(), sg.Column(col3)]
]
window = sg.Window("Color calculator", layout)
window.Finalize()
graph = window["graph"]
preview = graph.DrawCircle((52, 50), 46, fill_color="black", line_color="white")

fig = go.Figure()
names = []
while True:
    event, values = window.Read()
    print(event, values)
    if event in [sg.WIN_CLOSED, tr.gui_exit[lang]]:
        break
    elif event in tr.lang_list[lang]:
        for lng, lst in tr.langs.items():
            if event in lst:
                lang = lng
                break
        window["menu"].update(tr.gui_menu[lang])
        for i in range(3):
            window["col"+str(i)].update(tr.columns[lang][i])
        window["list"].update(values=tuple(obj_list().keys()))
        window["br0"].update(tr.gui_br[lang][0]+":")
        window["interp0"].update(tr.gui_interp[lang][0]+":")
        window["bit"].update(tr.gui_bit[lang]+":")
        window["rnd"].update(tr.gui_rnd[lang]+":")
        window["apply"].update(tr.gui_apply[lang])
        window["colorRGB"].update(tr.gui_rgb[lang]+":")
        window["colorHEX"].update(tr.gui_hex[lang]+":")
        window["add"].update(tr.gui_add[lang])
        window["plot"].update(tr.gui_plot[lang])
    elif event == tr.source[lang]:
        sg.popup("\n\n".join(spectra.sources), title=event, line_width=120)
    elif event == tr.note[lang]:
        notes = []
        for note, translation in tr.notes.items():
            notes.append(f"{note} {translation[lang]}")
        sg.popup("\n".join(notes), title=event)
    elif event == tr.gui_info[lang]:
        sg.popup(tr.info[lang], title=event)
    elif event == "list" or event == "apply" and values["list"] != []:
        for i in range(1, 4):
            if values["br"+str(i)]:
                mode = str(i)
        spectrum = spectra.objects[obj_list()[values["list"][0]]]
        if "filters" in spectrum:
            spectrum = convert.to_spectrum(spectrum)
        albedo = None
        if mode == "3":
            if "albedo" not in spectrum:
                mode = "1"
            elif type(spectrum["albedo"]) == bool:
                if spectrum["albedo"]:
                    pass
                else:
                    mode = "1"
            else:
                albedo = spectrum["albedo"]
        if values["srgb"]:
            nm = convert.xyz_nm
        else:
            nm = convert.rgb_nm
        if values["interp1"]:
            if spectrum["nm"][0] > nm[0] or spectrum["nm"][-1] < nm[-1]:
                interp = PchipInterpolator(spectrum["nm"], spectrum["br"], extrapolate=True)
            else:
                interp = Akima1DInterpolator(spectrum["nm"], spectrum["br"])
        elif values["interp2"]:
            interp = PchipInterpolator(spectrum["nm"], spectrum["br"], extrapolate=True)
        elif values["interp3"]:
            interp = CubicSpline(spectrum["nm"], spectrum["br"], extrapolate=True)
        rgb = convert.to_rgb(
            interp(nm), 
            mode=mode, albedo=albedo, 
            exp_bit=int(values["bit_num"]), 
            gamma=values["gamma"], 
            rnd=int(values["rnd_num"]),
            srgb=values["srgb"]
        )
        rgb_show = convert.to_rgb(
            interp(nm),
            mode=mode, albedo=albedo,
            gamma=values["gamma"],
            srgb=values["srgb"],
            html=True
        )
        graph.TKCanvas.itemconfig(preview, fill=rgb_show)
        window["rgb"].update(rgb)
        window["hex"].update(rgb_show)
    elif event == "add" and values["list"] != []:
        names.append(values["list"][0])
        fig.add_trace(go.Scatter(
            x = nm,
            y = interp(nm)/interp(550),
            name = values["list"][0],
            line = dict(color=rgb_show, width=4)
            ))
    elif event == "plot":
        if len(names) == 1:
            title_text = tr.single_title_text[lang] + names[0]
        else:
            title_text = tr.batch_title_text[lang] + ", ".join(names)
        fig.update_layout(title=title_text, xaxis_title=tr.xaxis_text[lang], yaxis_title=tr.yaxis_text[lang])
        fig.show()
window.Close()