import numpy as np
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageShow
from scipy.interpolate import Akima1DInterpolator, PchipInterpolator
import spectra, convert


path = spectra.folder + "/Maps"
request = "Jupiter 2019a"


# Loading images into an array

data = []
bands = []
calib = []
for band, name in spectra.maps[request][1]:
    data.append(np.array(Image.open(f"{path}/{request}/{name}").convert("L")))
    bands.append(band)
    calib.append([[], []])
data = np.array(data, dtype="float64")
l = data.shape[0] # number of maps
h = data.shape[1] # height of maps
w = data.shape[2] # width of maps

nm = convert.rgb_nm
pchip = False
if bands[0] > nm[0] or bands[-1] < nm[-1]:
    pchip = True


# Calibration of maps by spectrum

body = spectra.objects[spectra.maps[request][0]]
if bands[0] < nm[0] or bands[-1] > nm[-1]:
    body_spectrum = PchipInterpolator(body["nm"], body["br"], extrapolate=True)
else:
    body_spectrum = Akima1DInterpolator(body["nm"], body["br"])

for _ in range(42):
    for y in range(h):
        lat = np.pi * (0.5 - (y + 0.5) / h)
        lat = np.arctan((1 - body["obl"])**2 * np.tan(lat)) # from planetographic lat to planetocentric lat
        k = (1 - body["obl"]) * np.cos(lat) / np.sqrt(1 - (np.cos(lat))**2 * (2*body["obl"] - body["obl"]**2)) # planetocentric formula
        for layer in range(l):
            if np.sum(data[layer][y]) != 0:
                calib[layer][0].append(np.sum(data[layer][y]) / np.count_nonzero(data[layer][y]))
                calib[layer][1].append(k)
    for layer in range(l):
        avg = np.average(calib[layer][0], weights=calib[layer][1])
        color = 127.5 * body_spectrum(bands[layer]) / body_spectrum(550)
        data[layer] = data[layer] * color / avg

for layer in calib:
    print(np.average(layer[0], weights=layer[1]))


# Creating templates for the resulting image and figure

img = Image.new("RGB", (w, h), (0, 0, 0))
draw = ImageDraw.Draw(img)

fig = go.Figure()
fig.update_layout(title=request, xaxis_title="Wavelength [nm]", yaxis_title="Reflectivity")


n = 0
for x in range(w):
    for y in range(h):
        spectrum = data[:, y, x]
        n += 1
        if pchip:
            interp = PchipInterpolator(bands, spectrum, extrapolate=True)
        else:
            interp = Akima1DInterpolator(bands, spectrum)
        rgb = convert.to_rgb(interp(nm), mode="albedo", inp_bit=8, exp_bit=8)
        draw.point((x, y), rgb)
        if n % 1000 == 0:
            print(rgb)
            fig.add_trace(go.Scatter(
                x = nm,
                y = interp(nm),
                name = n,
                line = dict(color="rgb"+str(rgb), width=2)
                ))


img.save(f"{path}/{request}.png")
img.show()
#fig.show()