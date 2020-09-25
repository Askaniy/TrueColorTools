import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import Akima1DInterpolator
import translator as tr
import config, spectra, convert


config = {
    "lang": config.lang(),
    "srgb": False,
    "gamma": True,
    "albedo": True
}


objects = ["Jupiter|5", "Saturn|5", "Uranus|5", "Neptune|5", "Titan|5"] #["Sun|1", "Vega|1"]


fig = go.Figure()

names = []
for request in objects:
    # Parameter recognition
    if config["srgb"]:
        nm = convert.xyz_nm
    else:
        nm = convert.rgb_nm
    albedo = None
    # Spectrum processing
    spectrum = spectra.objects[request]
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
    if "filters" in spectrum:
        spectrum = convert.from_indeces(spectrum) # spectrum from color indices
    if "sun" in spectrum:
        if spectrum["sun"]:
            spectrum = convert.subtract_sun(spectrum, spectra.objects["Sun|1"]) # subtract solar spectrum
    try:
        interp = Akima1DInterpolator(spectrum["nm"], spectrum["br"])
    except ValueError:
        print("\n" + tr.error1[config["lang"]][0])
        print(tr.error1[config["lang"]][1].format(name, len(spectrum["nm"]), len(spectrum["br"])) + "\n")
        break
    if spectrum["nm"][0] > nm[0] or spectrum["nm"][-1] < nm[-1]:
        curve = convert.AskaniyExtrapolator(spectrum["nm"], spectrum["br"], nm)
    else:
        curve = interp(nm)
    rgb = convert.to_rgb(curve, mode=mode, albedo=albedo, exp_bit=8, gamma=config["gamma"], srgb=config["srgb"])
    if not np.array_equal(np.absolute(rgb), rgb):
        print("\n" + tr.error2[config["lang"]][0])
        print(tr.error2[config["lang"]][1].format(name, *rgb) + "\n")
        break
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
        y = curve,
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