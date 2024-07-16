""" Provides a table generation function, generate_table(). """
from PIL import Image, ImageDraw, ImageFont
from time import strftime
from math import floor, ceil, sqrt
import numpy as np
from src.auxiliary import normalize_string
import src.database as db
import src.data_processing as dp
import src.color_processing as cp
import src.strings as tr


def generate_table(objectsDB: dict, tag: str, brMode: bool, srgb: bool, gamma: bool, folder: str, extension: str, lang: str):
    """ Creates and saves a table of colored squares for each spectral data unit that has the specified tag """
    displayed_namesDB = db.obj_names_list(objectsDB, tag)
    l = len(displayed_namesDB)
    notes = db.notes_list(displayed_namesDB, lang)
    notes_flag = bool(notes)
    tag = tag.split('/')[-1] # then only the last category is used

    # Load fonts
    name_size = 36
    object_size = 20
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
    border_space = 20
    tiny_space = 2
    rounding_radius = 5
    half_square = 61 # half of the grid width
    r_square = half_square - tiny_space # half of the square width
    r_active = r_square - tiny_space # half of area, available for text

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
    w = 2*tiny_space + w_table # total image width
    w0 = tiny_space + border_space

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

    # Multiline title
    title_lines = line_splitter(tag.join(tr.table_title[lang]), name_font, w_table-2*border_space)
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
    h0 = border_space + name_size
    h1 = h0 + 2*half_square * int(ceil(l / objects_per_row)) + border_space//2
    h2 = h1 + help_step
    h = h1 + help_step + notes_per_column*note_step + border_space//2 # total image hight

    # Calculating squircles positions
    l_range = np.arange(l)
    centers_x = tiny_space + half_square + 2*half_square * (l_range%objects_per_row)
    centers_y = h0 + half_square + 2*half_square * (l_range/objects_per_row).astype('int')

    # Creating of background of colored squircles
    arr = np.zeros((h, w, 3))
    squircle = np.repeat(np.expand_dims(generate_squircle(r_square, rounding_radius), axis=2), repeats=3, axis=2)
    squircle_contour = np.repeat(np.expand_dims(generate_squircle_contour(r_square, rounding_radius, 1), axis=2), repeats=3, axis=2) * 0.25
    is_estimated = np.empty(l, dtype='bool')
    is_white_text = np.empty(l, dtype='bool')

    for n, obj_name in enumerate(displayed_namesDB):

        # Spectral data import and processing
        body = dp.database_parser(obj_name, objectsDB[obj_name])
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

        # Rounded square. For just a square, use `object_template = color.rgb`
        object_template = color.rgb * squircle if np.any(color.rgb) else squircle_contour

        # Placing object template into the image template
        center_x = centers_x[n]
        center_y = centers_y[n]
        arr[center_y-r_square:center_y+r_square, center_x-r_square:center_x+r_square, :] = object_template

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
    for n, obj_name in enumerate(displayed_namesDB):
        center_x = centers_x[n]
        center_y = centers_y[n]

        text_color = (0, 0, 0) if is_white_text[n] else (255, 255, 255)

        if is_estimated[n]:
            draw.text((center_x+r_active, center_y+r_active), tr.table_estimated[lang], text_color, small_font, anchor='rs', align='right')
        
        name = obj_name.name(lang)

        workaround_shift = 3
        # (it is not possible to use "lt" and "rt" anchors for multiline text
        # https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html)

        ref_len = 0 # to avoid intersections with indices in the left corner
        if obj_name.reference:
            ref = obj_name.reference
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
            draw.multiline_text((center_x+r_active, center_y-r_active-workaround_shift), ref, fill=text_color, font=small_font, anchor='ra', align='right', spacing=0)
        
        if obj_name.index or obj_name.info:
            index = '\n'.join(filter(None, (obj_name.index, obj_name.info)))
            if '+' in index:
                index = index.replace('+', '\n+')
            else:
                free_space = 2*r_active - ref_len - tiny_space
                index = '\n'.join(line_splitter(index, small_font, free_space))
            draw.multiline_text((center_x-r_active, center_y-r_active-workaround_shift), f'{index}', fill=text_color, font=small_font, anchor='la', align='left', spacing=0)
        
        if notes_flag and (note := obj_name.note(lang)):
            name += superscript(notes.index(note) + 1)

        splitted = line_splitter(name, object_font, 2*r_active)
        shift = object_size/2 if len(splitted) == 1 else object_size
        draw.multiline_text((center_x-r_active, center_y-shift), '\n'.join(splitted), fill=text_color, font=object_font, spacing=1)
    
    file_name = f'TCT_{strftime("%Y-%m-%d_%H-%M-%S")}_{normalize_string(tag)}.{extension}'
    img.save(f'{folder}/{file_name}')
    print(f'Color table saved as {file_name}')

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

separators = (' ', ':', '+', '-', '–', '—', '/')

def combine_words(word0: str, word1: str):
    """ Joining or rejoining lines of text """
    if (last_symbol := word0[-1]) == word1[0] and last_symbol in separators:
        combination = f'{word0}{word1[1:]}'
    else:
        combination = f'{word0} {word1}'
    return combination

def recursive_split(lst0: list, font: ImageFont.FreeTypeFont, maxW: int):
    """ A function that recursively splits and joins the list of strings to match `maxW` """
    words_widths = tuple(width(word, font) for word in lst0)
    lst = lst0
    if max(words_widths) > maxW:
        # Attempt to hyphenate the word
        for i in range(len(lst)):
            lst[i] = lst[i].strip()
            if width(lst[i], font) > maxW:
                # Check for a separator not on the edge
                for separator in separators:
                    if separator in (inner := lst[i][1:-1]):
                        part0, part1 = inner.split(separator, 1)
                        part1 += lst[i][-1]
                        lst[i] = f'{lst[i][0]}{part0}{separator}'.strip()
                        part1 = f'{separator}{part1}'.strip()
                        try:
                            lst[i+1] = combine_words(part1, lst[i+1])
                        except IndexError:
                            lst.append(part1)
                        recursive_split(lst, font, maxW)
                        break
                else:
                    # Move one letter per iteration
                    if (last_symbol := lst[i][-1]) in separators:
                        letter = lst[i][-2]
                        lst[i] = lst[i][:-2] + last_symbol
                    else:
                        letter = last_symbol + ' '
                        lst[i] = lst[i][:-1] + '-'
                    try:
                        lst[i+1] = f'{letter}{lst[i+1]}'
                    except IndexError:
                        lst.append(letter)
                    recursive_split(lst, font, maxW)
                break
    else:
        # Attempt to combine words
        for i in range(len(words_widths)-1):
            combination = combine_words(lst[i], lst[i+1])
            if width(combination, font) < maxW:
                lst[i] = combination
                lst.pop(i+1)
                recursive_split(lst, font, maxW)
                break
    return lst