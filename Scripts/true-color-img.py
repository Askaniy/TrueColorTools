import sys
import time
import numpy as np
import plotly.graph_objects as go
from PIL import Image, ImageDraw
import spectra, convert
start_time = time.time()

def k(lat_planetographic, obl=0):
    if obl == 0:
        lat = lat_planetographic
        return np.cos(lat) / np.sqrt(1 - (np.cos(lat))**2)
    else:
        lat_planetocentric = np.arctan((1 - obl)**2 * np.tan(lat_planetographic))
        return (1 - obl) * np.cos(lat_planetocentric) / np.sqrt(1 - (np.cos(lat_planetocentric))**2 * (2*obl - obl**2))


info = {
    "path": "X:/Documents/Astronomy/Creating/Bodies/Dwarf planets/2 Pluto-Charon/0 Pluto/v4/TCT/",
    "img": ["1K_nh_pluto_band4_BLUE.png", "1K_nh_pluto_band3_RED.png", "1K_nh_pluto_band2_NIR.png"],
    "filters": "New Horizons",
    "bands": ["Blue", "Red", "NIR"],
    "ref": "(134340) Pluto|6",
    "br": [0.473, 0.627, 0.747], # Characteristics of Pluto’s haze and surface from an analytic radiative transfer model, p.16
    "calib": False,
    "srgb": False,
    "gamma": False,
    "albedo": False,
    "name": "TCT result " + time.strftime("%Y-%m-%d %H-%M"),
    "extension": ".png"
}
n = 50 # number of calibration cycles


if "filters" in info and "bands" in info:
    info = convert.from_filters(info) # replacement of filters for their wavelengths
bands = info["nm"]
nm = convert.xyz_nm if info["srgb"] else convert.rgb_nm


# Loading images into an array

load = []
if type(info["img"]) is str:
    base = Image.open(info["path"] + info["img"])
    if len(base.getbands()) == 3:
        r, g, b = base.split()
        a = False
    elif len(base.getbands()) == 4:
        r, g, b, a = base.split() # alpha need to be used
    for i in [b, g, r]:
        load.append(np.array(i))
elif type(info["img"]) is list:
    for i in info["img"]:
        bw = Image.open(info["path"] + i)
        if len(bw.getbands()) != 1:
            sys.exit("Wrong format")
        load.append(np.array(bw))
else:
    sys.exit("Wrong format")

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
calib = [[[], []] for _ in range(l)] # [[[], []]]*l is very bad!


# Calibration of maps by spectrum

if info["calib"]:
    if "br" in info:
        br = np.array(info["br"])
        obl = 0
    elif "ref" in info:
        ref = convert.transform(spectra.objects[info["ref"]])
        albedo = ref["albedo"] if "albedo" in ref else 0
        br = convert.get_points(bands, ref["nm"], ref["br"], albedo)
        obl = ref["obl"] if "obl" in ref else 0
    for u in range(n): # calibration cycles
        for y in range(h):
            for layer in range(l):
                if np.sum(data[layer][y]) != 0:
                    calib[layer][0].append(np.sum(data[layer][y]) / np.count_nonzero(data[layer][y]))
                    calib[layer][1].append(k(np.pi * (0.5 - (y + 0.5) / h), obl))
        for layer in range(l):
            avg = np.average(calib[layer][0], weights=calib[layer][1])
            color = depth * br[layer]
            data[layer] = data[layer] * color / avg


# Creating templates for the resulting image and figure

img = Image.new("RGB", (w, h), (0, 0, 0))
draw = ImageDraw.Draw(img)

fig = go.Figure()
fig.update_layout(title=info["name"], xaxis_title="Wavelength [nm]", yaxis_title="Reflectivity")


px = 0 # pixel counter
pr = 1 # percent counter
n = 100 / (w * h)
for x in range(w):
    for y in range(h):
        spectrum = data[:, y, x]
        if np.sum(spectrum) > 0:
            curve = convert.DefaultExtrapolator(bands, list(spectrum), nm)
            rgb = convert.to_rgb(curve, mode="albedo", inp_bit=bit, exp_bit=8, gamma=info["gamma"])
            draw.point((x, y), rgb)
        px += 1
        if px * n > pr:
            print(f'{pr} %')
            pr += 1
            fig.add_trace(go.Scatter(
                x = nm,
                y = curve,
                name = px,
                line = dict(color="rgb"+str(rgb), width=2)
                ))

img.save(info["path"] + info["name"].replace(" ", "_") + info["extension"])
print(f'100 %, it took {round((time.time() - start_time)/60, 5)} min')
fig.show()
img.show()