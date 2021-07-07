import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import Akima1DInterpolator
import strings as tr
import user, spectra, convert


config = {
    "lang": user.lang(), # ReadMe -> FAQ -> How to choose a language?
    "srgb": False,
    "gamma": False,
    "albedo": False
}


objects = ["Jupiter|5", "Saturn|5", "Uranus|5", "Neptune|5", "Titan|5"]
# objects = ["Sun|1", "Vega|1"]


fig = go.Figure()
nm = convert.xyz_nm if config["srgb"] else convert.rgb_nm

names = []
for request in objects:
    mode = "albedo" if config["albedo"] else "chromaticity"

    # Spectral data processing
    spectrum = spectra.objects[request]
    albedo = 0
    if "albedo" not in spectrum:
        if config["albedo"]:
            mode = "chromaticity"
        spectrum.update({"albedo": False})
    elif type(spectrum["albedo"]) != bool:
        albedo = spectrum["albedo"]
    spectrum = convert.transform(spectrum)
    
    # Spectrum interpolation
    try:
        interp = Akima1DInterpolator(spectrum["nm"], spectrum["br"])
    except ValueError:
        print("\n" + tr.error1[config["lang"]][0])
        print(tr.error1[config["lang"]][1].format(name, len(spectrum["nm"]), len(spectrum["br"])) + "\n")
        break
    if spectrum["nm"][0] > nm[0] or spectrum["nm"][-1] < nm[-1]:
        curve = convert.DefaultExtrapolator(spectrum["nm"], spectrum["br"], nm, albedo)
    else:
        curve = interp(nm) / interp(550) * albedo if albedo else interp(nm)
    curve = np.clip(curve, 0, None)

    # Color calculation
    rgb = convert.to_rgb(
        curve, mode=mode,
        albedo = spectrum["albedo"] or albedo,
        exp_bit=8, gamma=config["gamma"], srgb=config["srgb"]
    )
    if not np.array_equal(np.absolute(rgb), rgb):
        print("\n" + tr.error2[config["lang"]][0])
        print(tr.error2[config["lang"]][1].format(name, *rgb) + "\n")
        break
    if "|" in request:
        name = "{} [{}]".format(*request.split("|"))
    else:
        name = request
    
    # Output
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
    print(rgb, name)

if len(objects) == 1:
    title_text = tr.single_title_text[config["lang"]] + name
else:
    title_text = tr.batch_title_text[config["lang"]] + ", ".join(names)
fig.update_layout(title=title_text, xaxis_title=tr.xaxis_text[config["lang"]], yaxis_title=tr.yaxis_text[config["lang"]])
fig.show()