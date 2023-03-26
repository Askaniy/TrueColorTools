from PIL import Image, ImageDraw, ImageFont
import numpy as np
import scr.cmf as cmf
import scr.calculations as calc
import scr.data_import as di
import scr.strings as tr


def generate_table(objectsDB: dict, refsDB: dict, tag: str, br_mode: str, srgb: bool, gamma: bool, folder: str, extension: str, lang: str) -> None:
    objects = di.obj_dict(objectsDB, tag, lang)
    l = len(objects)

    denumerized_references_list = refsDB
    adapted_references_list = []
    orig_num_list = []
    redirect_list = []

    # Layout
    num = 15 # objects per row
    r = 46 # half a side of a square
    rr = 4 # rounding radius
    ar = r-4 # active space
    if l < 11:
        w = 1200
    elif l < num:
        w = 100*(l + 1)
    else:
        w = 1600
    s = len(denumerized_references_list)
    name_step = 75
    objt_size = 17
    srce_size = 9
    srce_step = 3 * srce_size
    note_size = 16
    note_step = 4 + note_size
    auth_size = 10
    h0 = name_step + 100 * int(np.ceil(l / num) + 1)
    h1 = h0 + s * srce_step
    w0 = 100 - r
    w1 = int(w * 0.618034) # golden ratio
    img = Image.new('RGB', (w, h1 + 50), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    try:
        name_font = ImageFont.truetype('arial.ttf', 40)
        help_font = ImageFont.truetype('arial.ttf', 18)
        objt_font = ImageFont.truetype('ARIALN.TTF', objt_size)
        smll_font = ImageFont.truetype('arial.ttf', 12)
        srce_font = ImageFont.truetype('arial.ttf', srce_size)
        note_font = ImageFont.truetype('arial.ttf', note_size)
    except OSError: # Linux
        name_font = ImageFont.truetype('/usr/share/fonts/truetype/NotoSans-Regular.ttf', 40)
        help_font = ImageFont.truetype('/usr/share/fonts/truetype/NotoSans-Regular.ttf', 18)
        objt_font = ImageFont.truetype('/usr/share/fonts/truetype/NotoSans-Condensed.ttf', objt_size)
        smll_font = ImageFont.truetype('/usr/share/fonts/truetype/NotoSans-Regular.ttf', 12)
        srce_font = ImageFont.truetype('/usr/share/fonts/truetype/NotoSans-Regular.ttf', srce_size)
        note_font = ImageFont.truetype('/usr/share/fonts/truetype/NotoSans-Regular.ttf', note_size)
    # text brightness formula: br = 255 * (x^(1/2.2))
    draw.text((w0, 50), tag.join(tr.name_text[lang]), fill=(255, 255, 255), font=name_font) # x = 1, br = 255
    draw.text((w0, h0 - 25), tr.ref[lang]+':', fill=(230, 230, 230), font=help_font) # x = 0.8, br = 230
    draw.text((w1, h0 - 25), tr.note[lang]+':', fill=(230, 230, 230), font=help_font) # x = 0.8, br = 230
    note_num = 0
    for note, translation in tr.notes.items(): # x = 0.6, br = 202
        draw.multiline_text((w1, h0 + note_step * note_num), f'{note} {translation[lang]}', fill=(202, 202, 202), font=note_font)
        note_num += 1
    info_num = 1
    for info_num, info in enumerate([br_mode, srgb, gamma]): # x = 0.75, br = 224
        draw.multiline_text((w1, h0 + note_step * (note_num + info_num + 1)), f'{tr.info[lang][info_num]}: {info}', fill=(224, 224, 224), font=note_font)
        info_num += 1
    draw.multiline_text((w1, h0 + note_step * (note_num + info_num)), tr.link, fill=(0, 200, 255), font=note_font)
    
    # Table generator

    nm = cmf.xyz_nm if srgb else cmf.rgb_nm

    n = 0 # object counter
    for name, raw_name in objects.items():
        spectrum = objectsDB[raw_name]
        mode = br_mode

        # Spectral data import and processing
        albedo = 0
        if 'albedo' not in spectrum:
            if mode == 'albedo':
                mode = 'chromaticity'
            spectrum |= {'albedo': False}
        elif type(spectrum['albedo']) != bool:
            albedo = spectrum['albedo']
        spectrum = calc.standardize_photometry(spectrum)
        
        # Spectrum interpolation
        sun = False
        if 'sun' in spectrum:
            sun = spectrum['sun']
        curve = calc.polator(spectrum['nm'], spectrum['br'], nm, albedo, desun=sun)

        # Color calculation
        rgb = calc.to_rgb(
            name, curve, mode=mode,
            albedo = spectrum['albedo'] or albedo,
            exp_bit=8, gamma=gamma, srgb=srgb
        )

        # Object drawing
        center_x = 100 * (1 + n%num)
        center_y = name_step + 100 * int(1 + n/num)
        draw.rounded_rectangle((center_x-r, center_y-r, center_x+r, center_y+r), radius=rr, fill=rgb)
        
        text_color = (0, 0, 0) if np.mean(rgb) >= 127 else (255, 255, 255)
        
        if name[0] == '(': # Name processing
            parts = name.split(')', 1)
            name = parts[1].strip()
            draw.text((center_x-ar, center_y-ar), f'({parts[0][1:]})', fill=text_color, font=smll_font)
        elif '/' in name:
            parts = name.split('/', 1)
            name = parts[1].strip()
            draw.text((center_x-ar, center_y-ar), f'{parts[0]}/', fill=text_color, font=smll_font)
        
        if '|' in name:
            name, link = name.split('|')
            name = name.strip()
            new_link = []
            for i in link.split(', '):
                orig_num = int(i)-1 # reference number
                if orig_num in orig_num_list: # it was already numbered
                    new_link.append(str(redirect_list[orig_num_list.index(orig_num)]))
                else:
                    orig_num_list.append(orig_num)
                    srce_num = len(orig_num_list) # its new number
                    redirect_list.append(srce_num)
                    adapted_references_list.append(denumerized_references_list[orig_num])
                    new_link.append(str(srce_num))
                    draw.multiline_text((w0, h1 + (srce_num-1 - s) * srce_step), f'[{srce_num}] {adapted_references_list[-1]}', fill=(186, 186, 186), font=srce_font) # x = 0.5, br = 186
            new_link = f'[{", ".join(new_link)}]'
            draw.text((center_x+ar-width(new_link, smll_font), center_y-ar), new_link, fill=text_color, font=smll_font)
        
        if lang != 'en':
            for obj_name, tranlation in tr.names.items():
                if name.startswith(obj_name):
                    name = name.replace(obj_name, tranlation[lang])
        
        splitted = line_splitter(name, objt_font, ar*2)
        shift = objt_size/2 if len(splitted) == 1 else objt_size
        draw.multiline_text((center_x-ar, center_y-shift), '\n'.join(splitted), fill=text_color, font=objt_font, spacing=5)
        
        n += 1
        # print(export(rgb), name)
    
    file_name = f'TCT-table_{tag}{"_srgb" if srgb else ""}_{mode}{"_gamma-corrected" if gamma else ""}_{lang}.{extension}'
    s2 = len(adapted_references_list)
    h2 = h1 + (s2 - s) * srce_step
    min_limit = h0 + note_step * (note_num + info_num + 1)
    img = img.crop((0, 0, w, h2+50 if h2 > min_limit else min_limit+50))
    img.save(f'{folder}/{file_name}')
    # img.show()
    print('Done, saved as', file_name, '\n')


def width(line, font):
    return font.getlength(line)

def recurse(lst0, font, maxW, hyphen=True):
    lst = lst0
    w_list = []
    for i in lst:
        w_list.append(width(i, font))
    if max(w_list) < maxW:
        for i in range(len(w_list)-1):
            if w_list[i]+w_list[i+1] < maxW:
                lst[i] += ' ' + lst[i+1]
                lst.pop(i+1)
                recurse(lst, font, maxW)
                break
    else:
        hyphen_w = width('-', font) if hyphen else 0
        for i in range(len(lst)):
            if width(lst[i], font) > maxW:
                try:
                    lst[i+1] = lst[i][-1] + ' ' + lst[i+1]
                except IndexError:
                    lst.append(lst[i][-1])
                finally:
                    lst[i] = lst[i][:-1]
                while width(lst[i], font)+hyphen_w > maxW:
                    lst[i+1] = lst[i][-1] + lst[i+1]
                    lst[i] = lst[i][:-1]
                if lst[i][-1] in [' ', ':', '-']:
                    recurse(lst0, font, maxW, hyphen=False)
                else:
                    lst[i] += '-'
                    recurse(lst, font, maxW)
                break
    return lst

def line_splitter(line, font, maxW):
    w = width(line, font)
    if w < maxW:
        return [line]
    else:
        return recurse(line.split(), font, maxW)
