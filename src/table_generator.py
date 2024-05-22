""" Provides a table generation function, generate_table(). """

from PIL import Image, ImageDraw, ImageFont
from math import floor, ceil, sqrt
import numpy as np
import src.auxiliary as aux
import src.data_processing as dp
import src.color_processing as cp
import src.strings as tr


def generate_table(objectsDB: dict, tag: str, brMode: bool, srgb: bool, gamma: bool, folder: str, extension: str, lang: str):
    """ Creates and saves a table of colored squares for each spectral data unit that has the specified tag """
    objects = aux.obj_dict(objectsDB, tag, lang)
    l = len(objects)
    notes = aux.notes_list(objects.keys())
    notes_flag = bool(notes)

    # Load fonts
    name_size = 36
    object_size = 18
    help_size = 18
    help_step = 5 + help_size
    note_size = 16
    note_step = 4 + note_size
    engine = ImageFont.Layout.BASIC # see https://github.com/python-pillow/Pillow/issues/7765
    name_font = ImageFont.truetype('src/fonts/FiraSans-Bold.ttf', name_size, layout_engine=engine)
    object_font = ImageFont.truetype('src/fonts/FiraSansExtraCondensed-Regular.ttf', object_size, layout_engine=engine)
    help_font = ImageFont.truetype('src/fonts/FiraSansCondensed-Bold.ttf', help_size, layout_engine=engine)
    note_font = ImageFont.truetype('src/fonts/FiraSansCondensed-Regular.ttf', note_size, layout_engine=engine)
    small_font = ImageFont.truetype('src/fonts/FiraSansExtraCondensed-Light.ttf', 13, layout_engine=engine)

    # Layout
    half_square = 58 # half of the grid width
    r = 55 # half of the square width
    rounding_radius = 5 # rounding radius
    r_left= r-3 # active space
    r_right = r-3
    w_border = 8 # pixels of left and right spaces
    h_border = 16 # pixels of top and bottom spaces

    # Selecting the number of columns so that the bottom row is as full as possible
    col_num = sqrt(1.5*l) # strives for a 3:2 aspect ratio
    col_num_option1 = floor(col_num)
    fullness_option1 = fullness(col_num_option1, l)
    col_num_option2 = ceil(col_num)
    fullness_option2 = fullness(col_num_option2, l)
    col_num = (col_num_option1, col_num_option2)[bool(fullness_option1 < fullness_option2)]

    # Calculating grid widths
    min_obj_to_scale = 3 + int(notes_flag) * 2
    objects_per_row = max(min_obj_to_scale, col_num)
    w_table = 2*half_square*objects_per_row
    w = 2*w_border + w_table # image width
    w0 = w_border + half_square - r # using shift width

    # Placing info column
    info_list = (
        f'{l}/{len(objectsDB)} {tr.info_objects[lang]}',
        f'{tr.info_gamma[lang]}: {tr.info_indicator[lang][gamma]}',
        f'{tr.info_sRGB[lang]}: {tr.info_indicator[lang][srgb]}',
        f'{tr.gui_br[lang][0]}: {tr.gui_br[lang][brMode+1]}',
        tr.link,
    )
    info_colors = (      # text brightness formula: br = 255 * (x^(1/2.2))
        (224, 224, 224), # x = 0.75, br = 224
        (224, 224, 224),
        (224, 224, 224),
        (224, 224, 224),
        (0, 200, 255),
    )
    if notes_flag:
        w1 = int(w * 0.618034) # golden ratio for the info column
        w1 = min(w1, w-w0-max(width(info_text, note_font) for info_text in info_list))
    else:
        w1 = w0

    # Support for multiline title
    title_lines = line_splitter(tag.join(tr.table_title[lang]), name_font, w_table)
    title = '\n'.join(title_lines)
    name_size *= len(title_lines)

    # Notes calculations
    notes_per_column = len(info_list)
    if notes_flag:
        notes_numbered = [f'{superscript(note_num+1)} {note}' for note_num, note in enumerate(notes)]
        w_notes = w0 + max(width(note_text, note_font) for note_text in notes_numbered) # notes columns width
        notes_columns_num = (w1 - w0) // w_notes # max possible number of columns
        if notes_per_column * notes_columns_num < len(notes):
            notes_per_column = round(len(notes) // notes_columns_num + 1)

    # Calculating grid hights
    h0 = h_border + name_size
    h1 = h0 + 2*half_square * int(ceil(l / objects_per_row)) + note_step
    h2 = h1 + help_step
    h = h1 + help_step + notes_per_column*note_step + h_border # image hight

    # Calculating squircles positions
    l_range = np.arange(l)
    centers_x = w_border + half_square + 2*half_square * (l_range%objects_per_row)
    centers_y = h0 + half_square + 2*half_square * (l_range/objects_per_row).astype('int')

    # Creating of background of colored squircles
    arr = np.zeros((h, w, 3))
    squircle = np.repeat(np.expand_dims(generate_squircle(r, rounding_radius), axis=2), repeats=3, axis=2)
    squircle_contour = np.repeat(np.expand_dims(generate_squircle_contour(r, rounding_radius, 1), axis=2), repeats=3, axis=2) * 0.25
    is_estimated = np.empty(l, dtype='bool')
    is_white_text = np.empty(l, dtype='bool')

    for n, raw_name in enumerate(objects.values()):

        # Spectral data import and processing
        body = dp.database_parser(raw_name, objectsDB[raw_name])
        albedo = brMode and isinstance(body, dp.ReflectiveBody)

        # Setting brightness mode
        match brMode:
            case 0:
                spectrum, estimated = body.get_spectrum('chromaticity')
            case 1:
                spectrum, estimated = body.get_spectrum('geometric')
            case 2:
                spectrum, estimated = body.get_spectrum('spherical')
        is_estimated[n] = estimated
        
        # Color calculation
        if srgb:
            color = cp.Color.from_spectrum_CIE(spectrum, albedo)
        else:
            color = cp.Color.from_spectrum(spectrum, albedo)
        if gamma:
            color = color.gamma_corrected()
        is_white_text[n] = color.grayscale() > 0.5

        # Rounded square. For just square use `object_template = color.rgb`
        object_template = color.rgb * squircle if np.any(color.rgb) else squircle_contour

        # Placing object template into the image template
        center_x = centers_x[n]
        center_y = centers_y[n]
        arr[center_y-r:center_y+r, center_x-r:center_x+r, :] = object_template

    # Creating of image template
    img = Image.fromarray(np.clip(np.round(arr*255), 0, 255).astype('int8'), 'RGB')
    draw = ImageDraw.Draw(img)
    draw.multiline_text(
        xy=(int(w/2), int(h0/2)), text=title, fill=(255, 255, 255),
        font=name_font, anchor='mm', align='center', spacing=0
    )

    # Notes writing
    if notes_flag:
        draw.text((w0, h1), tr.notes_label[lang], fill=(230, 230, 230), font=help_font, anchor='la') # x = 0.8, br = 230
        for note_num, note_text in enumerate(notes_numbered): # x = 0.5, br = 186
            draw.text(
                xy=(w0 + w_notes * (note_num // notes_per_column), h2 + note_step * (note_num % notes_per_column)),
                text=note_text, fill=(186, 186, 186), font=note_font, anchor='la'
            )
    
    # Info writing
    draw.text((w1, h1), tr.info_label[lang], fill=(230, 230, 230), font=help_font, anchor='la') # x = 0.8, br = 230
    for info_num, (info_text, info_color) in enumerate(zip(info_list, info_colors)):
        draw.text(
            xy=(w1, h2+note_step*info_num), text=info_text, fill=info_color, font=note_font, anchor='la'
        )
    
    # Labeling the template
    for n, name in enumerate(objects.keys()):
        center_x = centers_x[n]
        center_y = centers_y[n]

        text_color = (0, 0, 0) if is_white_text[n] else (255, 255, 255)

        if is_estimated[n]:
            draw.text((center_x+r_left, center_y+r_left), tr.table_estimated[lang], text_color, small_font, anchor='rs', align='right')
        
        # Name processing
        workaround_shift = 3 # it is not possible to use "lt" and "rt" anchors for multiline text https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html
        
        ref_len = 0 # to avoid intersections with indices in the left corner
        if '[' in name:
            parts = name.split('[', 1)
            name = parts[0].strip()
            ref = parts[1][:-1]
            if ',' in ref:
                # checking multiple references, no more than 3 are supported!
                refs = [i.strip() for i in ref.split(',', 2)]
                ref = '\n'.join(refs) 
                ref_len = width(refs[0], small_font)
            elif len(ref) > 4 and (year := ref[-4:]).isnumeric() and (ref[-5].isalpha() or ref[-5] in separators) and (author_len := width(author := ref[:-4].strip(), small_font)) > width(year, small_font):
                # checking for a year in the reference name to print it on the second line
                ref = f'{author}\n{year}'
                ref_len = author_len
            else:
                ref_len = width(ref, small_font)
            draw.multiline_text((center_x+r_left, center_y-r_left-workaround_shift), ref, fill=text_color, font=small_font, anchor='ra', align='right', spacing=0)
        
        if name[0] == '(':
            parts = name.split(')', 1)
            name = parts[1].strip()
            index = parts[0][1:].strip()
            if '+' in index:
                index = index.replace('+', '\n+')
            else:
                free_space = r_left + r_right - ref_len - 3
                index = '\n'.join(line_splitter(index, small_font, free_space))
            draw.multiline_text((center_x-r_left, center_y-r_left-workaround_shift), f'{index}', fill=text_color, font=small_font, anchor='la', align='left', spacing=0)
        elif '/' in name:
            parts = name.split('/', 1)
            name = parts[1].strip()
            draw.text((center_x-r_left, center_y-r_left-workaround_shift), f'{parts[0]}/', fill=text_color, font=small_font)
        
        if notes_flag and ':' in name:
            parts = name.split(':', 1)
            name = parts[0].strip()
            note = parts[1].strip()
            name += superscript(notes.index(note) + 1)

        splitted = line_splitter(name, object_font, r_left+r_right)
        shift = object_size/2 if len(splitted) == 1 else object_size
        draw.multiline_text((center_x-r_left, center_y-shift), '\n'.join(splitted), fill=text_color, font=object_font, spacing=1)
    
    file_name = f'TCT_{tag}_gamma{("OFF", "ON")[gamma]}_srgb{("OFF", "ON")[srgb]}_albedo{("OFF", "GEOM", "SPHER")[brMode]}_{lang}.{extension}'
    img.save(f'{folder}/{file_name}')
    print(f'Color table saved as {file_name}\n')

def fullness(width: int, total_width: int):
    """ Column determination criterion """
    remainder = width % total_width
    return remainder / total_width if remainder != 0 else 1

def generate_squircle(semiaxis: int, rounding_radius: float, factor: int = 10):
    """
    Generates antialiased squircle using the formula from
    https://math.stackexchange.com/questions/1649714/whats-the-equation-for-a-rectircle-perfect-rounded-corner-rectangle-without-s
    Antialiasing is achieved by scaling by the `factor` and then downsampling.
    """
    axis = 2 * semiaxis
    semiaxis_ = semiaxis * factor
    y, x = np.ogrid[-semiaxis_:semiaxis_, -semiaxis_:semiaxis_]
    exponent = axis / rounding_radius
    mask = np.abs(x+0.5)**exponent + np.abs(y+0.5)**exponent <= semiaxis_**exponent
    return mask.astype('float').reshape(axis, factor, axis, factor).mean(axis=(1,3)) # downsampled

def generate_squircle_contour(semiaxis: int, rounding_radius: float, width: int, factor: int = 10):
    """ Generates antialiased squircle contour """
    outer_squircle = generate_squircle(semiaxis, rounding_radius, factor)
    inner_squircle = generate_squircle(semiaxis-width, rounding_radius / semiaxis * (semiaxis - width), factor)
    reversed_width = 2 * semiaxis - width
    outer_squircle[width:reversed_width, width:reversed_width] -= inner_squircle
    return outer_squircle

def superscript(number: int):
    """ Converts a number to be a superscript string """
    return ''.join(['⁰¹²³⁴⁵⁶⁷⁸⁹'[int(digit)] for digit in str(number)]) 

#def spacing_year(line: str):
#    """ Adds space between author and year in a reference name """
#    if line[-4:].isnumeric() and line[-5].isalpha():
#        line = f'{line[:-4]} {line[-4:]}'
#    return line

def width(line: str, font: ImageFont.FreeTypeFont):
    """ Alias for measuring line width in pixels """
    return font.getlength(line)

def line_splitter(line: str, font: ImageFont.FreeTypeFont, maxW: int) -> list[str]:
    """ Performs an adaptive line break at the specified width in pixels """
    if width(line, font) < maxW:
        return [line]
    else:
        return recursive_split(line.split(), font, maxW)

separators = (' ', ':', '+', '-')

def recursive_split(lst0: list, font: ImageFont.FreeTypeFont, maxW: int, hyphen=True):
    """ A function that recursively splits and joins the list of strings to match `maxW` """
    words_widths = [width(word, font) for word in lst0]
    lst = lst0
    if max(words_widths) < maxW:
        # Attempt to combine words
        for i in range(len(words_widths)-1):
            combination = f'{lst[i]} {lst[i+1]}'
            if width(combination, font) < maxW:
                lst[i] = combination
                lst.pop(i+1)
                recursive_split(lst, font, maxW)
                break
    else:
        # Attempt to hyphenate the word
        hyphen_width = width('-', font) if hyphen else 0
        for i in range(len(lst)):
            if width(lst[i], font) > maxW:
                # Check for a separator not on the edge
                for separator in separators:
                    if separator in lst[i][1:-2]:
                        part0, part1 = lst[i].split(separator, 1)
                        lst[i] = f'{part0}-'
                        try:
                            lst[i+1] = f'{separator}{part1} {lst[i+1]}'
                        except IndexError:
                            lst.append(f'{separator}{part1}')
                        recursive_split(lst, font, maxW)
                        break
                else:
                    # Move one letter per iteration
                    try:
                        lst[i+1] = f'{lst[i][-1]} {lst[i+1]}'
                    except IndexError:
                        lst.append(lst[i][-1])
                    finally:
                        lst[i] = lst[i][:-1]
                        while width(lst[i], font)+hyphen_width > maxW:
                            lst[i+1] = lst[i][-1] + lst[i+1]
                            lst[i] = lst[i][:-1]
                    if len(lst[i]) > 1:
                        if lst[i][-1] in separators:
                            recursive_split(lst0, font, maxW, hyphen=False)
                        else:
                            lst[i] += '-'
                            recursive_split(lst, font, maxW)
                    else:
                        lst[i+1] = lst[i] + lst[i+1]
                        lst[i] = ''
                    break
    return lst