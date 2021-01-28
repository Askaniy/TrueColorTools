import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.interpolate import Akima1DInterpolator
import translator as tr
import user, spectra, convert


config = {
    "path": user.folder() + "/Tables/",
    "name": "color_table-",
    "lang": user.lang(), # ReadMe -> FAQ -> How to choose a language?
    "srgb": False,
    "gamma": False,
    "albedo": False,
    "author info": False,
    "extension": ".png"
}


# Layout

r = 46 # radius in px
l = len(spectra.objects)
w = 100*(l + 1) if l < 15 else 1600
s = len(spectra.sources)
name_step = 75
objt_size = 18
srce_size = 15
srce_step = 10 + 2 * srce_size
note_size = 16
note_step = 4 + note_size
auth_size = 10
h0 = name_step + 100 * int(np.ceil(l / 15) + 1)
h1 = h0 + s * srce_step
img = Image.new("RGB", (w, h1 + 50), (0, 0, 0))
draw = ImageDraw.Draw(img)
name_font = ImageFont.truetype("arial.ttf", 42)
help_font = ImageFont.truetype("arial.ttf", 18)
narr_font = ImageFont.truetype("ARIALN.TTF", objt_size)
wide_font = ImageFont.truetype("arial.ttf", objt_size)
link_font = ImageFont.truetype("arial.ttf", 12)
srce_font = ImageFont.truetype("arial.ttf", srce_size)
note_font = ImageFont.truetype("arial.ttf", note_size)
auth_font = ImageFont.truetype("arial.ttf", auth_size)
# text brightness formula: br = 255 * (x^(1/2.2))
draw.text((100 - r, 50), tr.name_text[config["lang"]], fill=(255, 255, 255), font=name_font) # x = 1, br = 255
draw.text((100 - r, h0 - 25), tr.source[config["lang"]]+":", fill=(230, 230, 230), font=help_font) # x = 0.8, br = 230
draw.text((w * 2/3, h0 - 25), tr.note[config["lang"]]+":", fill=(230, 230, 230), font=help_font) # x = 0.8, br = 230
if config["author info"]:
    auth_step = 302 if config["lang"] == "ru" else 284
    draw.text((w - auth_step, h1 - auth_size), tr.info[config["lang"]], fill=(136, 136, 136), font=help_font) # x = 0.25, br = 136
for srce_num in range(s): # x = 0.5, br = 186
    draw.multiline_text((100 - r, h1 - srce_step * (s-srce_num)), spectra.sources[srce_num], fill=(186, 186, 186), font=srce_font)
note_num = 0
for note, translation in tr.notes.items(): # x = 0.75, br = 224
    draw.multiline_text((w * 2/3, h0 + note_step * note_num), f'{note} {translation[config["lang"]]}', fill=(224, 224, 224), font=note_font)
    note_num += 1


# Table generator

nm = convert.xyz_nm if config["srgb"] else convert.rgb_nm

n = 0 # object counter
for name, spectrum in spectra.objects.items():
    mode = "albedo" if config["albedo"] else "chromaticity"

    # Spectral data processing
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

    # Object drawing
    center_x = 100 * (1 + n%15)
    center_y = name_step + 100 * int(1 + n/15)
    if "obl" in spectrum:
        b = int(r * (1 - spectrum["obl"]))
        draw.ellipse([center_x-r, center_y-b, center_x+r, center_y+b], fill=rgb)
    else:
        draw.ellipse([center_x-r, center_y-r, center_x+r, center_y+r], fill=rgb)
    
    # Name processing
    if name[0] == "(":
        link_right = True
        index = name.split(")")
        name = index[1].strip()
        draw.text((center_x-40, center_y-22), f"({index[0][1:]})", fill=(0, 0, 0), font=link_font)
    else:
        link_right = False
    if "|" in name:
        link = name.split("|")
        name = link[0].strip()
        ll = len(link[1])
        if link_right:
            shift = 26 - 7*(ll-1)
        else:
            shift = -(6 + 3*(ll-1))
        draw.text((center_x+shift, center_y-22), f"[{link[1]}]", fill=(0, 0, 0), font=link_font)
    if config["lang"] != "en":
        for obj_name, tranlation in tr.names.items():
            if name.startswith(obj_name):
                name = name.replace(obj_name, tranlation[config["lang"]])
                pass
    width = 0
    for letter in name:
        if letter in ["I", "i", "j", "l", "f", "r", "t", "[", "]", "/", ":", "*" ".", " "]:
            width += 0.5
        elif letter.isupper():
            width += 1.5
        else:
            width += 1
    if width < 8:
        draw.text((center_x-40, center_y-(objt_size/2)), name, fill=(0, 0, 0), font=wide_font)
    elif width < 9:
        draw.text((center_x-42, center_y-(objt_size/2)), name, fill=(0, 0, 0), font=wide_font)
    elif width < 10:
        draw.text((center_x-40, center_y-(objt_size/2)), name, fill=(0, 0, 0), font=narr_font)
    elif width < 11:
        draw.text((center_x-42, center_y-(objt_size/2)), name, fill=(0, 0, 0), font=narr_font)
    elif width < 12:
        draw.text((center_x-42, center_y-(objt_size/2)), name.replace(":", "\n    :"), fill=(0, 0, 0), font=narr_font)
    elif width < 13:
        draw.text((center_x-42, center_y-(objt_size/2)), name.replace(":", "\n    :"), fill=(0, 0, 0), font=narr_font)
    else:
        draw.text((center_x-42, center_y-(objt_size/2)), f"{name[:10]}\n    {name[10:]}", fill=(0, 0, 0), font=narr_font)
    n += 1
    print(rgb, name)

save = ""
for key, value in config.items():
    if type(value) == str:
        save += value
    else:
        if value:
            save += f"-{key}"

img.save(save)
img.show()