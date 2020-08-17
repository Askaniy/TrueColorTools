import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import Akima1DInterpolator, PchipInterpolator
import translator as tr
import spectra, convert


config = {
    "lang": "en",
    "srgb": False,
    "gamma": True,
    "albedo": True
}


objects = ["Jupiter|5", "Saturn|5", "Uranus|5", "Neptune|5", "Titan|5"] #["Sun|1", "Vega|1"] #["Pluto|6", "Pluto|9"]


fig = go.Figure()

names = []
for request in objects:
    spectrum = spectra.objects[request]
    if "filters" in spectrum:
        spectrum = convert.to_spectrum(spectrum)
    if config["srgb"]:
        nm = convert.xyz_nm
    else:
        nm = convert.rgb_nm
    if spectrum["nm"][0] > nm[0] or spectrum["nm"][-1] < nm[-1]:
        interp = PchipInterpolator(spectrum["nm"], spectrum["br"], extrapolate=True)
    else:
        interp = Akima1DInterpolator(spectrum["nm"], spectrum["br"])
    albedo = None
    if config["albedo"]:
        if "albedo" not in spectrum:
            mode = "chromaticity"
        elif type(spectrum["albedo"]) == bool:
            if spectrum["albedo"]:
                mode = "albedo"
            else:
                mode = "chromaticity"
        else:
            mode = "albedo"
            albedo = spectrum["albedo"]
    else:
        mode = "chromaticity"
    rgb = convert.to_rgb(interp(nm), mode=mode, albedo=albedo, exp_bit=8, gamma=config["gamma"], srgb=config["srgb"])
    if "|" in request:
        name = "{} [{}]".format(*request.split("|"))
    else:
        name = request
    if config["lang"] != "en":
        for obj_name, tranlation in tr.names.items():
            if name.startswith(obj_name):
                name = name.replace(obj_name, tranlation[config["lang"]])
                break
    names.append(name)
    fig.add_trace(go.Scatter(
        x = nm,
        y = interp(nm),
        name = name,
        line = dict(color="rgb"+str(rgb), width=4)
        ))
    print(rgb)

if len(objects) == 1:
    title_text = tr.single_title_text[config["lang"]] + name
else:
    title_text = tr.batch_title_text[config["lang"]] + ", ".join(names)
fig.update_layout(title=title_text, xaxis_title=tr.xaxis_text[config["lang"]], yaxis_title=tr.yaxis_text[config["lang"]])
fig.show()