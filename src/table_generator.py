from PIL import Image, ImageDraw, ImageFont
import numpy as np
import src.cmf as cmf
import src.calculations as calc
import src.data_import as di
import src.strings as tr


def generate_table(objectsDB: dict, tag: str, br_mode: str, srgb: bool, gamma: bool, folder: str, extension: str, lang: str):
    """Creates and saves a table of colored squares for each spectrum with the specified tag"""
    objects = di.obj_dict(objectsDB, tag, lang)
    l = len(objects)

    # Layout
    half_square = 50 # half of square width
    r = 46 # half a side of a square
    rr = 4 # rounding radius
    ar = r-4 # active space
    br = r-2 # ...is higher for the right side of the square
    w_border = 50 # pixels of left and right spaces
    h_border = 50 # pixels of top and bottom spaces

    max_obj_per_raw = 14
    min_obj_to_scale = 8
    objects_per_raw = min(max(l, min_obj_to_scale), max_obj_per_raw)
    w_table = 2*half_square*objects_per_raw
    w = 2*w_border + w_table # calculate image width

    name_size = 42
    objt_size = 17
    help_size = 17
    help_step = 5 + help_size
    note_size = 16
    note_step = 4 + note_size

    # Load fonts
    name_font = ImageFont.truetype('fonts/NotoSans-DisplayCondensedSemiBold.ttf', name_size)
    objt_font = ImageFont.truetype('fonts/NotoSans-DisplayExtraCondensed.ttf', objt_size)
    help_font = ImageFont.truetype('fonts/NotoSans-DisplayCondensedSemiBold.ttf', help_size)
    note_font = ImageFont.truetype('fonts/NotoSans-DisplayCondensed.ttf', note_size)
    smll_font = ImageFont.truetype('fonts/NotoSans-DisplayCondensed.ttf', 12)

    # Support for multiline title
    title_lines = line_splitter(tag.join(tr.name_text[lang]), name_font, w_table)
    title = '\n'.join(title_lines)
    name_size *= len(title_lines)

    # Guide grid
    h0 = h_border + name_size
    h1 = h0 + 2*half_square * int(np.ceil(l / objects_per_raw)) + note_step
    h2 = h1 + help_step
    h = h1 + help_step + 4*note_step + h_border # calculate image width
    w0 = w_border + half_square - r
    w1 = 2*w0 + max([width(f'{note} {text[lang]}', note_font) for note, text in list(tr.notes.items())[:4]]) # second column depends on the width of the first
    w2 = int(w * 0.618034) # golden ratio

    # Create image template
    img = Image.new('RGB', (w, h), (0, 0, 0))
    draw = ImageDraw.Draw(img)                                                              # text brightness formula: br = 255 * (x^(1/2.2))
    draw.multiline_text((int(w/2), int(h0/2)), title, fill=(255, 255, 255), font=name_font, anchor='mm', align='center', spacing=0)
    draw.text((w0, h1), tr.legend[lang], fill=(230, 230, 230), font=help_font, anchor='la') # x = 0.8, br = 230
    draw.text((w2, h1), tr.note[lang], fill=(230, 230, 230), font=help_font, anchor='la')   # x = 0.8, br = 230
    note_num = 0
    for note, text in tr.notes.items(): # x = 0.6, br = 202
        draw.text((w0 if note_num < 4 else w1, h2 + note_step*(note_num%4)), f'{note} {text[lang]}', fill=(202, 202, 202), font=note_font, anchor='la')
        note_num += 1
    for info_num, info in enumerate([br_mode, srgb, gamma]): # x = 0.75, br = 224
        draw.text((w2, h2 + note_step*info_num), f'{tr.info[lang][info_num]}: {info}', fill=(224, 224, 224), font=note_font, anchor='la')
    draw.text((w2, h2 + note_step*(1+info_num)), tr.link, fill=(0, 200, 255), font=note_font, anchor='la')
    
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
        spectrum |= calc.matching_check(name, spectrum)
        
        # Spectrum interpolation
        try:
            sun = spectrum['sun']
        except KeyError:
            sun = False
        curve = calc.polator(spectrum['nm'], spectrum['br'], nm, albedo, desun=sun)

        # Color calculation
        rgb = calc.to_rgb(
            name, curve, mode=mode,
            albedo = spectrum['albedo'] or albedo,
            exp_bit=8, gamma=gamma, srgb=srgb
        )

        # Object drawing
        center_x = w_border + half_square + 2*half_square * (n%objects_per_raw)
        center_y = h0 + half_square + 2*half_square * int(n/objects_per_raw)
        draw.rounded_rectangle((center_x-r, center_y-r, center_x+r, center_y+r), radius=rr, fill=rgb)
        
        text_color = (0, 0, 0) if np.mean(rgb) >= 127 else (255, 255, 255)
        
        # Name processing
        if name[0] == '(':
            parts = name.split(')', 1)
            name = parts[1].strip()
            draw.text((center_x-ar, center_y-ar), f'({parts[0][1:]})', fill=text_color, font=smll_font)
        elif '/' in name:
            parts = name.split('/', 1)
            name = parts[1].strip()
            draw.text((center_x-ar, center_y-ar), f'{parts[0]}/', fill=text_color, font=smll_font)
        
        if '[' in name:
            parts = name.split('[', -1)
            name = parts[0].strip()
            ref = parts[1][:-1]
            if ',' in ref: # check for several references, no more than 3 supported
                ref = '\n'.join([spacing_year(i.strip()) for i in ref.split(',', 2)]) 
            elif ref[-4:].isnumeric() and (ref[-5].isalpha() or ref[-5]==''): # check for the year in the reference name to print it on the second line
                author = ref[:-4].strip()
                year = ref[-4:]
                if width(author, smll_font) > width(year, smll_font):
                    ref = f'{author}\n{year}'
                else:
                    ref = spacing_year(ref)
            draw.multiline_text((center_x+ar, center_y-ar), ref, fill=text_color, font=smll_font, anchor='ra', align='right', spacing=0)
        
        splitted = line_splitter(name, objt_font, ar+br)
        shift = objt_size/2 if len(splitted) == 1 else objt_size
        draw.multiline_text((center_x-ar, center_y-shift), '\n'.join(splitted), fill=text_color, font=objt_font, spacing=0)
        n += 1
    
    file_name = f'TCT-table_{tag}{"_srgb" if srgb else ""}_{mode}{"_gamma-corrected" if gamma else ""}_{lang}.{extension}'
    img.save(f'{folder}/{file_name}')
    print(f'Color table saved as {file_name}\n')


def spacing_year(line: str):
    """Adds space between author and year in a reference name"""
    if line[-4:].isnumeric() and line[-5].isalpha():
        line = f'{line[:-4]} {line[-4:]}'
    return line

def width(line: str, font: ImageFont.FreeTypeFont):
    """Alias for measuring line width in pixels"""
    return font.getlength(line)

def hight(line: str, font: ImageFont.FreeTypeFont):
    """Alias for measuring line width in pixels"""
    return font.get

def line_splitter(line: str, font: ImageFont.FreeTypeFont, maxW: int):
    """Performs an adaptive line break at the specified width in pixels"""
    if width(line, font) < maxW:
        return [line]
    else:
        return recursive_split(line.split(), font, maxW)

def recursive_split(lst0: list, font: ImageFont.FreeTypeFont, maxW: int, hyphen=True):
    lst = lst0
    w_list = []
    for i in lst:
        w_list.append(width(i, font))
    if max(w_list) < maxW:
        for i in range(len(w_list)-1):
            if w_list[i]+w_list[i+1] < maxW:
                lst[i] += ' ' + lst[i+1]
                lst.pop(i+1)
                recursive_split(lst, font, maxW)
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
                    recursive_split(lst0, font, maxW, hyphen=False)
                else:
                    lst[i] += '-'
                    recursive_split(lst, font, maxW)
                break
    return lst