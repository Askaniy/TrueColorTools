import user, spectra, filters, convert
import strings as tr
import PySimpleGUI as sg
from PIL import Image, ImageDraw
import numpy as np
import io

lang = user.lang() # ReadMe -> FAQ -> How to choose a language?

vis = 3
preview = (256, 128)

sg.LOOK_AND_FEEL_TABLE["MaterialDark"] = {
    'BACKGROUND': '#333333', 'TEXT': '#FFFFFF',
    'INPUT': '#424242', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#86A8FF',
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

def frame(num):
    n = str(num)
    l = [
        [sg.Input(size=(15, 1), disabled=False, disabled_readonly_background_color="#3A3A3A", key="path"+n), sg.FileBrowse(button_text=tr.gui_browse[lang], size=(6, 1), disabled=False, key="browse"+n)],
        [sg.Text(tr.gui_filter[lang], size=(8, 1), text_color="#A3A3A3", key="filterN"+n), sg.InputCombo([], size=(11, 1), disabled=True, enable_events=True, key="filter"+n)],
        [sg.Text(tr.gui_wavelength[lang], size=(14, 1), key="wavelengthN"+n), sg.Input(size=(6, 1), disabled_readonly_background_color="#3A3A3A", disabled=False, enable_events=True, key="wavelength"+n)]
    ]
    return sg.Frame(title=f"{tr.gui_band[lang]} {num+1}", layout=l, visible=num < vis, key="band"+n)

def obj_list():
    global lang
    names = {}
    for name_0 in spectra.objects.keys():
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
            for obj_name, tranlation in tr.names.items():
                if name_1.startswith(obj_name):
                    name_1 = name_1.replace(obj_name, tranlation[lang])
                    break
            name_1 = index + name_1
        names.update({name_1: name_0})
    return names

presets = ["Hubble maps"]
col1 = [
    [sg.Text(tr.gui_input[lang], size=(12, 1), font=("arial", 12), key="title1"), sg.Button(button_text="+", size=(2, 1)), sg.Button(button_text="-", size=(2, 1), disabled=False)],
    [sg.Checkbox(tr.gui_preset[lang], size=(20, 1), enable_events=True, key="preset")],
    [sg.InputCombo(presets, size=(24, 1), enable_events=True, disabled=True, key="template")],
    [sg.Checkbox(tr.gui_single[lang], size=(20, 1), enable_events=True, key="single")],
    [sg.Input(size=(16, 1), disabled=True, disabled_readonly_background_color="#3A3A3A", key="path"), sg.FileBrowse(button_text=tr.gui_browse[lang], size=(6, 1), disabled=True, key="browse")],
    [frame(0)],
    [frame(1)],
    [frame(2)],
    [frame(3)],
    [frame(4)] # just add more frames here
]
col2 = [
    [sg.Text(tr.gui_output[lang], size=(20, 1), font=("arial", 12), key="title2")],
    [sg.Checkbox(tr.gui_gamma[lang], size=(20, 1), key="gamma")],
    [sg.Checkbox("sRGB", size=(20, 1), key="srgb")],
    [sg.Checkbox(tr.gui_system[lang], size=(26, 1), enable_events=True, key="system")],
    [sg.InputCombo(filters.get_sets(), size=(26, 1), enable_events=True, disabled=True, key="filter")],
    [sg.Checkbox(tr.gui_calib[lang], size=(26, 1), enable_events=True, key="calib")],
    [sg.InputCombo(list(obj_list().keys()), size=(26, 1), enable_events=True, disabled=True, key="ref")],
    [sg.T("")],
    [sg.Text(tr.gui_folder[lang])],
    [sg.Input(size=(27, 1), enable_events=True, key="folder"), sg.FolderBrowse(button_text=tr.gui_browse[lang], size=(6, 1), key="browse_folder")],
    [sg.Button(tr.gui_preview[lang], size=(15, 1), disabled=True, key="show"), sg.Button(tr.gui_process[lang], size=(15, 1), disabled=True, key="process")],
    [sg.Image(background_color="black", size=preview, key="preview")]
]
layout = [
    [sg.Column(col1), sg.VSeperator(), sg.Column(col2)],
]
window = sg.Window(tr.gui_name2[lang], layout)

num = len(col1) - 5
while True:
    event, values = window.Read()
    #print(values)

    if event == sg.WIN_CLOSED:
        break

    if event == "preset":
        window["template"].update(disabled=not values["preset"])
    
    if event == "template":
        if values["template"] == "Hubble maps":
            vis = 3
            window["single"].update(True)
            window["browse"].update(disabled=False)
            window["system"].update(True)
            window["filter"].update("Hubble")
            window["filter0"].update("f395n")
            window["filter1"].update("f502n")
            window["filter2"].update("f631n")

    if event == "single":
        window["browse"].update(disabled=not values["single"])
        window["path"].update(disabled=not values["single"])
        for i in range(num):
            window["browse"+str(i)].update(disabled=values["single"])
            window["path"+str(i)].update(disabled=values["single"])
        if values["single"]:
            vis = 3
            for i in range(num):
                window["band"+str(i)].update(visible=False)
            for i in range(3):
                window["band"+str(i)].update(visible=True)

    if event == "system":
        window["filter"].update(disabled=not values["system"])
        for i in range(num):
            window["filter"+str(i)].update(disabled=not values["system"])
            window["wavelength"+str(i)].update(disabled=values["system"])

    if event == "filter":
        for i in range(num):
            window["filter"+str(i)].update(values=filters.get_filters(values["filter"]))

    if event in ["filter"+str(i) for i in range(num)]:
        i = event[-1]
        window["wavelength"+i].update(filters.get_param(values["filter"], values["filter"+i], "L_mean"))

    if event == "calib":
        window["ref"].update(disabled=not values["calib"])

    if event == "folder":
        window["process"].update(disabled=False)
    
    if event == "+":
        window["band"+str(vis)].update(visible=True)
        vis += 1
    
    if event == "-":
        window["band"+str(vis-1)].update(visible=False)
        vis -= 1
    
    window["+"].update(disabled=values["single"] or not 2 <= vis < num)
    window["-"].update(disabled=values["single"] or not 2 < vis <= num)
    for i in range(num):
        window["filterN"+str(i)].update(text_color=("#A3A3A3", "#FFFFFF")[values["system"]])
        window["wavelengthN"+str(i)].update(text_color=("#A3A3A3", "#FFFFFF")[not values["system"]])
    
    input_data = {"gamma": values["gamma"], "srgb": values["srgb"], "nm": []}
    window["show"].update(disabled=False)
    if values["folder"] != "":
        window["process"].update(disabled=False)
    if values["system"]:
        for i in range(vis):
            if bool(values["filter"+str(i)]):
                input_data["nm"].append(filters.get_param(values["filter"], values["filter"+str(i)], "L_mean"))
            else:
                window["show"].update(disabled=True)
                window["process"].update(disabled=True)
                break
    else:
        for i in range(vis):
            if values["wavelength"+str(i)].replace(".", "").isnumeric():
                input_data["nm"].append(float(values["wavelength"+str(i)]))
            else:
                window["show"].update(disabled=True)
                window["process"].update(disabled=True)
                break
    if not all(a > b for a, b in zip(input_data["nm"][1:], input_data["nm"])): # increasing check
        window["show"].update(disabled=True)
        window["process"].update(disabled=True)
    
    if event in ("show", "process"):
        try:
            load = []
            if values["single"]:
                if values["path"] == "":
                    raise ValueError("Path is empty")
                rgb_img = Image.open(values["path"])
                if event == "show":
                    rgb_img = rgb_img.resize(preview, resample=Image.HAMMING)
                if len(rgb_img.getbands()) == 3:
                    r, g, b = rgb_img.split()
                    a = False
                elif len(rgb_img.getbands()) == 4:
                    r, g, b, a = rgb_img.split()
                for i in [b, g, r]:
                    load.append(np.array(i))
            else:
                for i in range(vis):
                    if values["path"+str(i)] == "":
                        raise ValueError(f'Path {i+1} is empty')
                    bw_img = Image.open(values["path"+str(i)])
                    if event == "show":
                        bw_img = bw_img.resize(preview, resample=Image.HAMMING)
                    if len(bw_img.getbands()) != 1:
                        raise TypeError("Band image should be b/w")
                    load.append(np.array(bw_img))
            
            data = np.array(load, dtype="float64")
            l = data.shape[0] # number of maps
            h = data.shape[1] # height of maps
            w = data.shape[2] # width of maps

            if data.max() > 255:
                bit = 16
                depth = 65535
            else:
                bit = 8
                depth = 255
            
            nm = convert.xyz_nm if values["srgb"] else convert.rgb_nm
            img = Image.new("RGB", (w, h), (0, 0, 0))
            draw = ImageDraw.Draw(img)
            counter = 0
            px_num = w*h

            for x in range(w):
                for y in range(h):
                    spectrum = data[:, y, x]
                    if np.sum(spectrum) > 0:
                        curve = convert.DefaultExtrapolator(input_data["nm"], list(spectrum), nm)
                        rgb = convert.to_rgb(curve, mode="albedo", albedo=True, inp_bit=bit, exp_bit=8, gamma=input_data["gamma"])
                        draw.point((x, y), rgb)
                    counter += 1
                    sg.OneLineProgressMeter("Progress", counter, px_num)
            
            #img.show()
            if event == "show":
                window["preview"].update(data=convert_to_bytes(img))
            else:
                img.save(values["folder"]+"/TCT_result.png")
        
        except Exception as e:
            print(e)
    
    if event == "process":
        print(input_data)

window.Close()