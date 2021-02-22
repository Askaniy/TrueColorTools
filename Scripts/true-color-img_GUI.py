import user, spectra, convert
import translator as tr
import PySimpleGUI as sg

lang = user.lang("en") # ReadMe -> FAQ -> How to choose a language?


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
    [sg.Text(tr.gui_results[lang], size=(12, 1), font=("arial", 12), key="title1")],
    [sg.Image(background_color="black", size=(256, 128), key="preview")],
    [sg.Button(tr.gui_preview[lang], key="show"), sg.Button(tr.gui_process[lang], disabled=True, key="process")],
    [sg.Text("Saving folder"), sg.Input(size=(15, 1), enable_events=True, key="folder"), sg.FileBrowse()],
    [sg.Text("Progress"), sg.ProgressBar(100, orientation="h", size=(16, 25), key="progbar")]
]
layout = [
    [sg.Column(col1), sg.VSeperator(), sg.Column(col2)],
    [sg.Text("")],
    [sg.Text("Image bands", size=(10, 1), font=("arial", 12), key="title2"), sg.Button(button_text="Add", key="add")],
    [
        sg.Column([
            [sg.FileBrowse(disabled=False, key="browse0"), sg.Input(size=(12, 1), disabled=False, disabled_readonly_background_color="#3A3A3A", key="path0")],
            [sg.Text("Filter name"), sg.InputCombo([], size=(7, 1), enable_events=True, disabled=True, key="filter0")],
            [sg.Text("Wavelength (nm)"), sg.Input(size=(5, 1), disabled_readonly_background_color="#3A3A3A", disabled=False, key="wavelength0")]
        ], visible=True, key="band0"),
        sg.Column([
            [sg.FileBrowse(disabled=False, key="browse1"), sg.Input(size=(12, 1), disabled=False, disabled_readonly_background_color="#3A3A3A", key="path1")],
            [sg.Text("Filter name"), sg.InputCombo([], size=(7, 1), enable_events=True, disabled=True, key="filter1")],
            [sg.Text("Wavelength (nm)"), sg.Input(size=(5, 1), disabled_readonly_background_color="#3A3A3A", disabled=False, key="wavelength1")]
        ], visible=True, key="band1"),
        sg.Column([
            [sg.FileBrowse(disabled=False, key="browse2"), sg.Input(size=(12, 1), disabled=False, disabled_readonly_background_color="#3A3A3A", key="path2")],
            [sg.Text("Filter name"), sg.InputCombo([], size=(7, 1), enable_events=True, disabled=True, key="filter2")],
            [sg.Text("Wavelength (nm)"), sg.Input(size=(5, 1), disabled_readonly_background_color="#3A3A3A", disabled=False, key="wavelength2")]
        ], visible=False, key="band2"),
        sg.Column([
            [sg.FileBrowse(disabled=False, key="browse3"), sg.Input(size=(12, 1), disabled=False, disabled_readonly_background_color="#3A3A3A", key="path3")],
            [sg.Text("Filter name"), sg.InputCombo([], size=(7, 1), enable_events=True, disabled=True, key="filter3")],
            [sg.Text("Wavelength (nm)"), sg.Input(size=(5, 1), disabled_readonly_background_color="#3A3A3A", disabled=False, key="wavelength3")]
        ], visible=False, key="band3"),
        sg.Column([
            [sg.FileBrowse(disabled=False, key="browse4"), sg.Input(size=(12, 1), disabled=False, disabled_readonly_background_color="#3A3A3A", key="path4")],
            [sg.Text("Filter name"), sg.InputCombo([], size=(7, 1), enable_events=True, disabled=True, key="filter4")],
            [sg.Text("Wavelength (nm)"), sg.Input(size=(5, 1), disabled_readonly_background_color="#3A3A3A", disabled=False, key="wavelength4")]
        ], visible=False, key="band4")
    ]
]
window = sg.Window("True color image processing tool", layout)

num = len(layout[3])
vis = 2
while True:
    event, values = window.Read()
    print(values)

    if event == sg.WIN_CLOSED:
        break

    if event == "single":
        window["browse"].update(disabled=not values["single"])
        window["path"].update(disabled=not values["single"])
        for i in range(num):
            window["browse"+str(i)].update(disabled=values["single"])
            window["path"+str(i)].update(disabled=values["single"])

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
    
    if event == "add":
        window["band"+str(vis)].update(visible=True)
        vis += 1
        if vis == num:
            window["add"].update(disabled=True)

window.Close()