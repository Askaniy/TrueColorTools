import PySimpleGUI as sg
import io
import numpy as np
from scipy.interpolate import Akima1DInterpolator, PchipInterpolator, CubicSpline
from PIL import Image, ImageDraw
import plotly.graph_objects as go
import user, spectra, filters, convert
import strings as tr

lang = user.lang() # ReadMe -> FAQ -> How to choose a language?


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

def frame(num):
    n = str(num)
    l = [
        [sg.Input(size=(21, 1), disabled=False, disabled_readonly_background_color="#3A3A3A", key="T2_path"+n), sg.FileBrowse(button_text=tr.gui_browse[lang], size=(6, 1), disabled=False, key="T2_browse"+n)],
        [sg.Text(tr.gui_filter[lang], size=(8, 1), text_color="#A3A3A3", key="T2_filterN"+n), sg.InputCombo([], size=(17, 1), disabled=True, enable_events=True, key="T2_filter"+n)],
        [sg.Text(tr.gui_wavelength[lang], size=(14, 1), key="T2_wavelengthN"+n), sg.Input(size=(12, 1), disabled_readonly_background_color="#3A3A3A", disabled=False, enable_events=True, key="T2_wavelength"+n)]
    ]
    return sg.Frame(f"{tr.gui_band[lang]} {num+1}", l, visible=num < T2_vis, key="T2_band"+n)

def convert_to_bytes(img):
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()


sg.LOOK_AND_FEEL_TABLE["MaterialDark"] = {
    'BACKGROUND': '#333333', 'TEXT': '#FFFFFF',
    'INPUT': '#424242', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#86A8FF',
    'BUTTON': ('#FFFFFF', '#007ACC'), 'PROGRESS': ('#000000', '#000000'),
    'BORDER': 0, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
    'ACCENT1': '#FF0266', 'ACCENT2': '#FF5C93', 'ACCENT3': '#C5003C'
}
sg.ChangeLookAndFeel("MaterialDark")

T1_col1 = [
    [sg.Text(tr.gui_database[lang], size=(16, 1), font=("arial", 12), key="T1_title0")],
    [sg.Text(tr.gui_tags[lang], size=(7, 1), key="T1_tagsN"), sg.InputCombo([], size=(12, 1), enable_events=True, disabled=True, key="T1_tags")],
    [sg.Listbox(values=tuple(obj_list().keys()), size=(22, 22), enable_events=True, key="T1_list")]
]
T1_col2 = [
    [sg.Text(tr.gui_settings[lang], size=(16, 1), font=("arial", 12), key="T1_title1")],
    [sg.Checkbox(tr.gui_gamma[lang], size=(16, 1), enable_events=True, default=True, key="T1_gamma")],
    [sg.Checkbox("sRGB", enable_events=True, size=(16, 1), key="T1_srgb")],
    [sg.HorizontalSeparator()],
    [sg.Text(tr.gui_br[lang][0], size=(18, 1), key="T1_br_mode")],
    [sg.Radio(tr.gui_br[lang][1], "T1_rad", size=(15, 1), enable_events=True, default=True, key="T1_br_mode0")],
    [sg.Radio(tr.gui_br[lang][2], "T1_rad", size=(15, 1), enable_events=True, key="T1_br_mode1")],
    [sg.Radio(tr.gui_br[lang][3], "T1_rad", size=(15, 1), enable_events=True, key="T1_br_mode2")],
    [sg.HorizontalSeparator()],
    [sg.Text(tr.gui_interp[lang][0], size=(18, 1), key="T1_interp")],
    [sg.Radio(tr.gui_interp[lang][1], "T1_interp", size=(15, 1), enable_events=True, default=True, key="T1_interp0")],
    [sg.Radio(tr.gui_interp[lang][2], "T1_interp", size=(6, 1), enable_events=True, key="T1_interp1"),
    sg.Radio(tr.gui_interp[lang][3], "T1_interp", size=(6, 1), enable_events=True, key="T1_interp2")],
    [sg.HorizontalSeparator()],
    [sg.Text(tr.gui_bit[lang], size=(12, 1), key="T1_bit"), sg.InputText("8", size=(4, 1), enable_events=True, key="T1_bit_num")],
    [sg.Text(tr.gui_rnd[lang], size=(12, 1), key="T1_rnd"), sg.InputText("3", size=(4, 1), enable_events=True, key="T1_rnd_num")]
]
T1_col3 = [
    [sg.Text(tr.gui_results[lang], size=(16, 1), font=("arial", 12), key="T1_title2")],
    [sg.Graph(canvas_size=(180, 175), graph_bottom_left=(0, 0), graph_top_right=(100, 100), background_color=None, key="T1_graph")],
    [sg.Text(tr.gui_rgb[lang], size=(8, 1), key="T1_colorRGB")],
    [sg.In(size=(25, 1), key="T1_rgb")],
    [sg.Text(tr.gui_hex[lang], size=(8, 1), key="T1_colorHEX")],
    [sg.In(size=(25, 1), key="T1_hex")],
    [sg.T("")],
    [sg.Button(button_text=tr.gui_add[lang], size=(22, 1), key="T1_add")],
    [sg.Button(button_text=tr.gui_plot[lang], size=(22, 1), key="T1_plot")],
    [sg.Button(button_text=tr.gui_export[lang], size=(22, 1), key="T1_export")]
]

T2_vis = 3
T2_preview = (256, 128)
T2_presets = ["Hubble maps"]
T2_col1 = [
    [sg.Text(tr.gui_input[lang], size=(17, 1), font=("arial", 12), key="T2_title1"), sg.Button(button_text="+", size=(2, 1), key="T2_+"), sg.Button(button_text="-", size=(2, 1), disabled=False, key="T2_-")],
    [sg.Checkbox(tr.gui_preset[lang], size=(22, 1), enable_events=True, key="T2_preset")],
    [sg.InputCombo(T2_presets, size=(29, 1), enable_events=True, disabled=True, key="T2_template")],
    [sg.Checkbox(tr.gui_single[lang], size=(22, 1), enable_events=True, key="T2_single")],
    [sg.Input(size=(22, 1), disabled=True, disabled_readonly_background_color="#3A3A3A", key="T2_path"), sg.FileBrowse(button_text=tr.gui_browse[lang], size=(6, 1), disabled=True, key="T2_browse")],
    [frame(0)],
    [frame(1)],
    [frame(2)],
    [frame(3)],
    [frame(4)] # just add more frames here
]
T2_col2 = [
    [sg.Text(tr.gui_output[lang], size=(20, 1), font=("arial", 12), key="T2_title2")],
    [sg.Checkbox(tr.gui_gamma[lang], size=(20, 1), key="T2_gamma")],
    [sg.Checkbox("sRGB", size=(20, 1), key="T2_srgb")],
    [sg.HorizontalSeparator()],
    [sg.Checkbox(tr.gui_system[lang], size=(26, 1), enable_events=True, key="T2_system")],
    [sg.InputCombo(filters.get_sets(), size=(26, 1), enable_events=True, disabled=True, key="T2_filter")],
    [sg.Checkbox(tr.gui_calib[lang], size=(26, 1), enable_events=True, key="T2_calib")],
    [sg.InputCombo(list(obj_list().keys()), size=(26, 1), enable_events=True, disabled=True, key="T2_ref")],
    [sg.T("")],
    [sg.Text(tr.gui_folder[lang], key="T2_folderN")],
    [sg.Input(size=(27, 1), enable_events=True, key="T2_folder"), sg.FolderBrowse(button_text=tr.gui_browse[lang], size=(6, 1), key="T2_browse_folder")],
    [sg.Button(tr.gui_preview[lang], size=(15, 1), disabled=True, key="T2_show"), sg.Button(tr.gui_process[lang], size=(15, 1), disabled=True, key="T2_process")],
    [sg.Image(background_color="black", size=T2_preview, key="T2_preview")]
]
T2_num = len(T2_col1) - 5

T3_col1 = [
    [sg.Text(tr.gui_settings[lang], size=(20, 1), font=("arial", 12), key="T3_title1")],
    [sg.Text(tr.gui_tags[lang], size=(7, 1), key="T3_tagsN"), sg.InputCombo([], size=(14, 1), enable_events=True, disabled=True, key="T3_tags")],
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
    [sg.Text(tr.gui_extension[lang], size=(17, 1), key="ext"), sg.InputCombo([".png", ".jpeg"], default_value=".png", size=(22, 1), enable_events=True, key="T3_extension")],
    [sg.Text(tr.gui_folder[lang], size=(17, 1), key="T3_folderN"), sg.Input(size=(16, 1), enable_events=True, key="T3_folder"), sg.FolderBrowse(button_text=tr.gui_browse[lang], size=(6, 1), key="T3_browse_folder")],
    [sg.T("")],
    [sg.Button(tr.gui_process[lang], size=(15, 1), disabled=True, key="T3_process")]
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

layout = [
    [sg.Menu(tr.gui_menu[lang], key="menu")],
    [sg.TabGroup([[sg.Tab(tr.gui_tabs[lang][0], tab1, key="tab0"), sg.Tab(tr.gui_tabs[lang][1], tab2, key="tab2"), sg.Tab(tr.gui_tabs[lang][2], tab3, key="tab3")]])]
]

window = sg.Window("True Color Tools", layout)    
window.Finalize()
graph = window["T1_graph"]
T1_preview = graph.DrawCircle((48, 46), 42, fill_color="black", line_color="white")

T1_fig = go.Figure()
T1_events = ["T1_list", "T1_gamma", "T1_srgb", "T1_br_mode0", "T1_br_mode1", "T1_br_mode2", "T1_interp0", "T1_interp1", "T1_interp2", "T1_bit_num", "T1_rnd_num"]
br_modes = ["chromaticity", "normalization", "albedo"]

names = []
while True:
    event, values = window.Read()

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
        window["T1_title0"].update(tr.gui_database[lang])
        window["T1_title1"].update(tr.gui_settings[lang])
        window["T1_title2"].update(tr.gui_results[lang])
        window["T1_tagsN"].update(tr.gui_tags[lang])
        window["T1_list"].update(values=tuple(obj_list().keys()))
        window["T1_br_mode"].update(tr.gui_br[lang][0])
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
        #window["T2_preset"].update(tr.gui_preset[lang])
        #window["T2_single"].update(tr.gui_single[lang])
        window["T2_browse"].update(tr.gui_browse[lang])
        for i in range(T2_num):
            window["T2_browse"+str(i)].update(tr.gui_browse[lang])
            window["T2_filterN"+str(i)].update(tr.gui_filter[lang])
            window["T2_wavelengthN"+str(i)].update(tr.gui_wavelength[lang])
            window["T2_band"+str(i)].update(f"{tr.gui_band[lang]} {i+1}")
        #window["T2_gamma"].update(tr.gui_gamma[lang])
        #window["T2_system"].update(tr.gui_system[lang])
        #window["T2_calib"].update(tr.gui_calib[lang])
        window["T2_folderN"].update(tr.gui_folder[lang])
        window["T2_browse_folder"].update(tr.gui_browse[lang])
        window["T2_show"].update(tr.gui_preview[lang])
        window["T2_process"].update(tr.gui_process[lang])
        window["T3_title1"].update(tr.gui_settings[lang])
        window["T3_title2"].update(tr.gui_results[lang])
        window["T3_tagsN"].update(tr.gui_tags[lang])
        window["T3_br_mode"].update(tr.gui_br[lang][0])
        #window["T3_signature"].update(tr.gui_signature[lang])
        window["ext"].update(tr.gui_extension[lang])
        window["T3_folderN"].update(tr.gui_folder[lang])
        window["T3_process"].update(tr.gui_process[lang])
    
    elif event == tr.source[lang]:
        sg.popup("\n\n".join(spectra.sources), title=event, line_width=120, location=(16, 25))
    
    elif event == tr.note[lang]:
        notes = []
        for note, translation in tr.notes.items():
            notes.append(f"{note} {translation[lang]}")
        sg.popup("\n".join(notes), title=event)
    
    elif event == tr.gui_info[lang]:
        sg.popup(tr.auth_info[lang], title=event)
    
    elif event.startswith("T1"):
        if event in T1_events and values["T1_list"] != []:
            nm = convert.xyz_nm if values["T1_srgb"] else convert.rgb_nm
            for i in range(3):
                if values["T1_br_mode"+str(i)]:
                    mode = br_modes[i]

            # Spectral data import and processing
            spectrum = spectra.objects[obj_list()[values["T1_list"][0]]]
            albedo = 0
            if "albedo" not in spectrum:
                if mode == "albedo":
                    mode = "chromaticity"
                spectrum.update({"albedo": False})
            elif type(spectrum["albedo"]) != bool:
                albedo = spectrum["albedo"]
            spectrum = convert.transform(spectrum)
            
            # Spectrum interpolation
            try:
                interp = Akima1DInterpolator(spectrum["nm"], spectrum["br"])
            except ValueError:
                print("\n" + tr.error1[lang][0])
                print(tr.error1[lang][1].format(values["T1_list"][0], len(spectrum["nm"]), len(spectrum["br"])) + "\n")
                break
            if spectrum["nm"][0] > nm[0] or spectrum["nm"][-1] < nm[-1]:
                if values["T1_interp0"]:
                    curve = convert.DefaultExtrapolator(spectrum["nm"], spectrum["br"], nm, albedo)
                elif values["T1_interp1"]:
                    extrap = PchipInterpolator(spectrum["nm"], spectrum["br"], extrapolate=True)
                    curve = extrap(nm) / extrap(550) * albedo if albedo else extrap(nm)
                elif values["T1_interp2"]:
                    extrap = CubicSpline(spectrum["nm"], spectrum["br"], extrapolate=True)
                    curve = extrap(nm) / extrap(550) * albedo if albedo else extrap(nm)
            else:
                curve = interp(nm) / interp(550) * albedo if albedo else interp(nm)
            curve = np.clip(curve, 0, None)
            
            # Color calculation
            rgb = convert.to_rgb(
                curve, mode=mode,
                albedo = spectrum["albedo"] or albedo,
                exp_bit=int(values["T1_bit_num"]), 
                gamma=values["T1_gamma"], 
                rnd=int(values["T1_rnd_num"]),
                srgb=values["T1_srgb"]
            )
            rgb_show = convert.to_rgb(
                curve, mode=mode,
                albedo = spectrum["albedo"] or albedo,
                gamma=values["T1_gamma"],
                srgb=values["T1_srgb"],
                html=True
            )
            if not np.array_equal(np.absolute(rgb), rgb):
                rgb_show = "#000000"
                print("\n" + tr.error2[lang][0])
                print(tr.error2[lang][1].format(values["T1_list"][0], *rgb) + "\n")
                #break

            # Output
            try:
                graph.TKCanvas.itemconfig(T1_preview, fill=rgb_show)
            except Exception as e:
                graph.TKCanvas.itemconfig(T1_preview, fill="#000000")
                print(e)
            window["T1_rgb"].update(rgb)
            window["T1_hex"].update(rgb_show)
        
        elif event == "T1_add" and values["T1_list"] != []:
            names.append(values["T1_list"][0])
            T1_fig.add_trace(go.Scatter(
                x = nm,
                y = curve,
                name = values["T1_list"][0],
                line = dict(color=rgb_show, width=4)
                ))
        
        elif event == "T1_plot":
            if len(names) == 1:
                title_text = tr.single_title_text[lang] + names[0]
            else:
                title_text = tr.batch_title_text[lang] + ", ".join(names)
            T1_fig.update_layout(title=title_text, xaxis_title=tr.xaxis_text[lang], yaxis_title=tr.yaxis_text[lang])
            T1_fig.show()
        
        elif event == "T1_export":
            print("\n" + "\t".join(tr.gui_col[lang]) + "\n" + "_" * 36)
            nm = convert.xyz_nm if values["T1_srgb"] else convert.rgb_nm
            
            # Spectrum processing
            for name_1, name_0 in obj_list().items():
                spectrum = spectra.objects[name_0]
                for i in range(3):
                    if values["T1_br_mode"+str(i)]:
                        mode = br_modes[i]
                albedo = 0
                if "albedo" not in spectrum:
                    if mode == "albedo":
                        mode = "chromaticity"
                    spectrum.update({"albedo": False})
                elif type(spectrum["albedo"]) != bool:
                    albedo = spectrum["albedo"]
                spectrum = convert.transform(spectrum)
                
                # Spectrum interpolation
                try:
                    interp = Akima1DInterpolator(spectrum["nm"], spectrum["br"])
                except ValueError:
                    print("\n" + tr.error1[lang][0])
                    print(tr.error1[lang][1].format(values["list"][0], len(spectrum["nm"]), len(spectrum["br"])) + "\n")
                    break
                if spectrum["nm"][0] > nm[0] or spectrum["nm"][-1] < nm[-1]:
                    if values["T1_interp0"]:
                        curve = convert.DefaultExtrapolator(spectrum["nm"], spectrum["br"], nm, albedo)
                    elif values["T1_interp1"]:
                        extrap = PchipInterpolator(spectrum["nm"], spectrum["br"], extrapolate=True)
                        curve = extrap(nm) / extrap(550) * albedo if albedo else extrap(nm)
                    elif values["T1_interp2"]:
                        extrap = CubicSpline(spectrum["nm"], spectrum["br"], extrapolate=True)
                        curve = extrap(nm) / extrap(550) * albedo if albedo else extrap(nm)
                else:
                    curve = interp(nm) / interp(550) * albedo if albedo else interp(nm)
                curve = np.clip(curve, 0, None)

                # Color calculation
                rgb = convert.to_rgb(
                    curve, mode=mode,
                    albedo = spectrum["albedo"] or albedo,
                    exp_bit=int(values["T1_bit_num"]), 
                    gamma=values["T1_gamma"], 
                    rnd=int(values["T1_rnd_num"]),
                    srgb=values["T1_srgb"]
                )

                # Output
                print("\t".join([str(i) for i in rgb]) + "\t" + name_1)
    
    elif event.startswith("T2"):
        if event == "T2_preset":
            window["T2_template"].update(disabled=not values["T2_preset"])
        
        elif event == "template":
            if values["T2_template"] == "Hubble maps":
                T2_vis = 3
                window["T2_single"].update(True)
                window["T2_browse"].update(disabled=False)
                window["T2_system"].update(True)
                window["T2_filter"].update("Hubble")
                window["T2_filter0"].update("f395n")
                window["T2_filter1"].update("f502n")
                window["T2_filter2"].update("f631n")

        elif event == "single":
            window["T2_browse"].update(disabled=not values["T2_single"])
            window["T2_path"].update(disabled=not values["T2_single"])
            for i in range(T2_num):
                window["bT2_rowse"+str(i)].update(disabled=values["T2_single"])
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

        elif event == "T2_calib":
            window["T2_ref"].update(disabled=not values["T2_calib"])

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
                    rgb_img = Image.open(values["T2_path"])
                    if event == "show":
                        rgb_img = rgb_img.resize(T2_preview, resample=Image.HAMMING)
                    if len(rgb_img.getbands()) == 3:
                        r, g, b = rgb_img.split()
                        a = False
                    elif len(rgb_img.getbands()) == 4:
                        r, g, b, a = rgb_img.split()
                    for i in [b, g, r]:
                        load.append(np.array(i))
                else:
                    for i in range(T2_vis):
                        if values["T2_path"+str(i)] == "":
                            raise ValueError(f'Path {i+1} is empty')
                        bw_img = Image.open(values["T2_path"+str(i)])
                        if event == "show":
                            bw_img = bw_img.resize(T2_preview, resample=Image.HAMMING)
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
                
                nm = convert.xyz_nm if input_data["srgb"] else convert.rgb_nm
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
                if event == "T2_show":
                    window["T2_preview"].update(data=convert_to_bytes(img))
                else:
                    img.save(values["T2_folder"]+"/TCT_result.png")
            
            except Exception as e:
                print(e)

window.Close()