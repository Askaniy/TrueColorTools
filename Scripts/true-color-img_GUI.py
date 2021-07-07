import user, spectra, convert
import strings as tr
import PySimpleGUI as sg

lang = user.lang("en") # ReadMe -> FAQ -> How to choose a language?

vis = 2
def frame(num):
    n = str(num)
    l = [
        [sg.FileBrowse(disabled=False, key="browse"+n), sg.Input(size=(12, 1), disabled=False, disabled_readonly_background_color="#3A3A3A", key="path"+n)],
        [sg.Text("Filter name", text_color="#A3A3A3", key="filterN"+n), sg.InputCombo([], size=(7, 1), disabled=True, enable_events=True, key="filter"+n)],
        [sg.Text("Wavelength (nm)", key="wavelengthN"+n), sg.Input(size=(5, 1), disabled_readonly_background_color="#3A3A3A", disabled=False, enable_events=True, key="wavelength"+n)]
    ]
    return sg.Frame(title=f"Band {num+1}", layout=l, visible=num < vis, key="band"+n)

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


sg.LOOK_AND_FEEL_TABLE["MaterialDark"] = {
    'BACKGROUND': '#333333', 'TEXT': '#FFFFFF',
    'INPUT': '#424242', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#86A8FF',
    'BUTTON': ('#FFFFFF', '#007ACC'), 'PROGRESS': ('#000000', '#000000'),
    'BORDER': 0, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
    'ACCENT1': '#FF0266', 'ACCENT2': '#FF5C93', 'ACCENT3': '#C5003C'
}
sg.ChangeLookAndFeel("MaterialDark")

col1 = [
    [sg.Text(tr.gui_settings[lang], size=(24, 1), font=("arial", 12), key="title0")],
    [sg.Checkbox("Gamma correction", size=(20, 1), key="gamma")],
    [sg.Checkbox("sRGB", size=(20, 1), key="srgb")],
    [sg.Checkbox("Single 3-band image mode", size=(20, 1), enable_events=True, key="single")],
    [sg.Input(size=(20, 1), disabled=True, disabled_readonly_background_color="#3A3A3A", key="path"), sg.FileBrowse(disabled=True, key="browse")],
    [sg.Checkbox("Filters preset", size=(24, 1), enable_events=True, key="preset")],
    [sg.InputCombo(list(convert.filters.keys()), size=(24, 1), enable_events=True, disabled=True, key="filter")],
    [sg.Checkbox("Reference body calibration", size=(20, 1), enable_events=True, key="calib")],
    [sg.InputCombo(list(obj_list().keys()), size=(24, 1), enable_events=True, disabled=True, key="ref")],
]
col2 = [
    [sg.Text("Image bands", size=(10, 1), font=("arial", 12), key="title2"), sg.Button(button_text="+", size=(2, 1)), sg.Button(button_text="-", size=(2, 1), disabled=True)],
    [frame(0)],
    [frame(1)],
    [frame(2)],
    [frame(3)],
    [frame(4)]
]
col3 = [
    [sg.Text(tr.gui_results[lang], size=(12, 1), font=("arial", 12), key="title1")],
    [sg.Image(background_color="black", size=(256, 128), key="preview")],
    [sg.Button(tr.gui_preview[lang], disabled=True, key="show"), sg.Button(tr.gui_process[lang], disabled=True, key="process")],
    [sg.Text("Saving folder"), sg.Input(size=(15, 1), enable_events=True, key="folder"), sg.FileBrowse()],
    [sg.Text("Progress"), sg.ProgressBar(100, orientation="h", size=(16, 25), key="progbar")]
]
layout = [
    [sg.Column(col1), sg.VSeperator(), sg.Column(col2), sg.VSeperator(), sg.Column(col3)],
]
window = sg.Window("True color image processing tool", layout)

num = len(col2) - 1
while True:
    event, values = window.Read()
    #print(values)

    if event == sg.WIN_CLOSED:
        break

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

    if event == "preset":
        window["filter"].update(disabled=not values["preset"])
        for i in range(num):
            window["filter"+str(i)].update(disabled=not values["preset"])
            window["wavelength"+str(i)].update(disabled=values["preset"])

    if event == "filter":
        for i in range(num):
            window["filter"+str(i)].update(values=list(convert.filters[values["filter"]].keys()))

    if event in ["filter"+str(i) for i in range(num)]:
        i = event[-1]
        window["wavelength"+i].update(convert.filters[values["filter"]][values["filter"+i]]["nm"])

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
        window["filterN"+str(i)].update(text_color=("#A3A3A3", "#FFFFFF")[values["preset"]])
        window["wavelengthN"+str(i)].update(text_color=("#A3A3A3", "#FFFFFF")[not values["preset"]])
    
    input_data = {"gamma": values["gamma"], "srgb": values["srgb"], "nm": []}
    window["show"].update(disabled=False)
    window["process"].update(disabled=False)
    if values["preset"]:
        for i in range(vis):
            if bool(values["filter"+str(i)]):
                input_data["nm"].append(convert.filters[values["filter"]][values["filter"+str(i)]]["nm"])
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
    
    if event == "process":
        print(input_data)

window.Close()