""" Provides a table generation function, generate_table(). """
from PIL import Image, ImageDraw, ImageFont
from time import strftime
from math import floor, ceil, sqrt
import numpy as np

from src.core import *
import src.database as db
import src.strings as tr


def generate_table(
        objectsDB: dict, tag: str, color_system: ColorSystem, gamma_correction: bool, maximize_brightness: bool,
        scale_factor: float, geom_albedo: bool, folder: str, extension: str, lang: str
    ):
    """ Creates and saves a table of colored squares for each spectral data unit that has the specified tag """
    displayed_namesDB = db.obj_names_list(objectsDB, tag)
    l = len(displayed_namesDB)
    notes = db.notes_list(displayed_namesDB, lang)
    notes_flag = bool(notes)
    tag = tag.split('/')[-1] # then only the last category is used
    try:
        scale_factor = max(0, float(scale_factor))
    except ValueError:
        scale_factor = 1

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
    ref_maxW = 1.5 * r_active # the limit reference width is 3/4 of the active space

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

    # Constructing and placing info column
    brMode = tr.table_chromaticity if maximize_brightness else (tr.gui_geom if geom_albedo else tr.gui_sphe)
    chromatic_adaptation = color_system.white_point_name if color_system.white_point_name else tr.table_bool_indicator[lang][0]
    info_list = [
        f'{l}/{len(objectsDB)} {tr.table_objects_number[lang]}',
        f'{tr.gui_color_space[lang]}: {color_system.color_space_name}',
        f'{tr.gui_chromatic_adaptation[lang]}: {chromatic_adaptation}',
        f'{tr.gui_gamma_correction[lang]}: {tr.table_bool_indicator[lang][gamma_correction]}',
        f'{tr.table_brightness_mode[lang]}: {brMode[lang]}'
    ]
    if scale_factor != 1:
        info_list.append(f'{tr.table_scale_factor[lang]}: {scale_factor}')
    info_list.append(tr.link)
    notes_per_column = len(info_list)

    # text brightness formula: br = 255 * (x^(1/2.2))
    # here x = 0.75, br = 224
    info_colors = [(224, 224, 224)] * notes_per_column
    info_colors[-1] = (0, 200, 255) # the link
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
    if notes_flag:
        notes_numbered = [f'{aux.superscript(note_num+1)} {note}' for note_num, note in enumerate(notes)]
        w_notes = w0 + max(width(note_text, note_font) for note_text in notes_numbered) # notes columns width
        notes_columns_num = (w1 - w0) // w_notes # max possible number of columns
        if notes_per_column * notes_columns_num < len(notes):
            notes_per_column = round(len(notes) // notes_columns_num + 1)

    # Calculating grid heights
    h0 = border_space + name_size
    h1 = h0 + 2*half_square * int(ceil(l / objects_per_row)) + border_space//2
    h2 = h1 + help_step
    h = h1 + help_step + notes_per_column*note_step + border_space//2 # total image height

    # Calculating squircles positions
    l_range = np.arange(l)
    centers_x = tiny_space + half_square + 2*half_square * (l_range%objects_per_row)
    centers_y = h0 + half_square + 2*half_square * (l_range/objects_per_row).astype('int')

    # Creating of background of colored squircles
    arr = np.zeros((h, w, 3))
    shapes = (
        aux.higher_dim(generate_squircle_contour(r_square+1, rounding_radius, 2), times=3, axis=2),
        aux.higher_dim(generate_squircle(r_square, rounding_radius), times=3, axis=2)
    )
    text_colors = (
        (0, 0, 0),
        (255, 255, 255)
    )
    is_white_text = np.empty(l, dtype='bool')
    object_notes = []

    for n, obj_name in enumerate(displayed_namesDB):

        # Spectral data import and processing
        body = database_parser(obj_name, objectsDB[obj_name])
        spectrum, estimated = body.get_spectrum('geometric' if geom_albedo else 'spherical')

        # Color calculation
        color = ColorPoint.from_spectral_data(spectrum).to_color_system(color_system)
        color.gamma_correction = gamma_correction
        color.maximize_brightness = maximize_brightness or estimated is None
        color.scale_factor = scale_factor
        color_array = color.to_array()

        # Setting of notes and shape
        is_filled = True
        if maximize_brightness or isinstance(body, EmittingBody):
            object_notes.append(None)
        else:
            match estimated:
                case True:
                    object_notes.append(tr.table_estimated[lang])
                case False:
                    object_notes.append(None)
                case None:
                    is_filled = False
                    object_notes.append(tr.table_no_albedo[lang])

        # Setting object and text colors
        if np.any(color_array):
            grayscale = color_array.mean()
            # color.grayscale() luminance doesn't work well for red and blue objects
            if is_filled:
                object_color = color_array
                is_white_text[n] = grayscale < 0.5
            else:
                object_color = color_array / grayscale / 3
                is_white_text[n] = True
        else:
            # error handling
            object_color = 1/3
            is_white_text[n] = True

        # Placing object template into the image template
        center_x = centers_x[n]
        center_y = centers_y[n]
        r_sq = r_square if is_filled else r_square+1
        arr[center_y-r_sq:center_y+r_sq, center_x-r_sq:center_x+r_sq, :] = shapes[is_filled] * object_color

    # Creating of image template
    img = Image.fromarray(np.clip(np.round(arr*255), 0, 255).astype('uint8'))
    draw = ImageDraw.Draw(img)
    draw.multiline_text(
        xy=(int(w/2), int(h0/2)), text=title, fill=(255, 255, 255),
        font=name_font, anchor='mm', align='center', spacing=0
    )

    # Notes writing
    if notes_flag:
        draw.text((w0, h1), tr.table_notes[lang], fill=(230, 230, 230), font=help_font, anchor='la') # x = 0.8, br = 230
        for note_num, note_text in enumerate(notes_numbered): # x = 0.5, br = 186
            draw.text(
                xy=(w0 + w_notes * (note_num // notes_per_column), h2 + note_step * (note_num % notes_per_column)),
                text=note_text, fill=(186, 186, 186), font=note_font, anchor='la'
            )

    # Info writing
    draw.text((w1, h1), tr.table_info[lang], fill=(230, 230, 230), font=help_font, anchor='la') # x = 0.8, br = 230
    for info_num, (info_text, info_color) in enumerate(zip(info_list, info_colors)):
        draw.text(
            xy=(w1, h2+note_step*info_num), text=info_text, fill=info_color, font=note_font, anchor='la'
        )

    # Labeling the template
    for n, obj_name in enumerate(displayed_namesDB):
        center_x = centers_x[n]
        center_y = centers_y[n]

        text_color = text_colors[int(is_white_text[n])]

        if (object_note := object_notes[n]) is not None:
            draw.text((center_x+r_active, center_y+r_active), object_note, text_color, small_font, anchor='rs', align='right')

        name = obj_name.name(lang)

        workaround_shift = 3
        # (it is not possible to use "lt" and "rt" anchors for multiline text
        # https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html)

        ref_len = 0 # to avoid intersections with indices in the left corner
        if obj_name.reference:
            ref = obj_name.reference
            if ',' in ref:
                # checking multiple references, no more than 3 are supported!
                refs = [check_ref(i, small_font, ref_maxW) for i in ref.split(',', 2)]
                ref = '\n'.join(refs)
                ref_len = width(refs[0], small_font)
            elif len(ref) > 4 and (year := ref[-4:]).isnumeric() and (ref[-5].isalpha() or ref[-5] in separators) and (author_len := width(author := check_ref(ref[:-4], small_font, ref_maxW), small_font)) > width(year, small_font):
                # checking for a year in the reference name to print it on the second line
                ref = f'{author}\n{year}'
                ref_len = author_len
            else:
                ref = check_ref(ref, small_font, ref_maxW)
                ref_len = width(ref, small_font)
            draw.multiline_text((center_x+r_active, center_y-r_active-workaround_shift), ref, fill=text_color, font=small_font, anchor='ra', align='right', spacing=0)

        if obj_name.index or obj_name.info:
            index = '\n'.join(filter(None, (obj_name.index, obj_name.info(lang))))
            if '+' in index:
                index = index.replace('+', '\n+')
            else:
                free_space = 2*r_active - ref_len - tiny_space
                try:
                    index = '\n'.join(line_splitter(index, small_font, free_space))
                except RecursionError:
                    # the case of wide reference name (on the first line)
                    index = '\n' + '\n'.join(line_splitter(index, small_font, r_active))
            draw.multiline_text((center_x-r_active, center_y-r_active-workaround_shift), f'{index}', fill=text_color, font=small_font, anchor='la', align='left', spacing=0)

        if notes_flag and (note := obj_name.note(lang)):
            name += aux.superscript(notes.index(note) + 1)

        splitted = line_splitter(name, object_font, 2*r_active)
        match len(splitted):
            case 1:
                shift = 0.5 * object_size
            case 4:
                shift = object_size + workaround_shift # not related, just works to move up the line a bit
            case _:
                shift = object_size
        draw.multiline_text((center_x-r_active, center_y-shift), '\n'.join(splitted), fill=text_color, font=object_font, spacing=1)

    file_name = f'TCT_{strftime("%Y-%m-%d_%H-%M-%S")}_{aux.normalize_string(tag)}.{extension}'
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

separators = (' ', ':', '+', '-', '–', '—', '/')

def width(line: str, font: ImageFont.FreeTypeFont):
    """ Alias for measuring line width in pixels """
    return font.getlength(line)

def check_ref(ref: str, font: ImageFont.FreeTypeFont, maxW: int):
    """ Shortens the reference name if it exceeds the maximum width """
    ref = ref.strip()
    if len(ref) > 4 and (year := ref[-4:]).isnumeric() and (ref[-5].isalpha() or ref[-5] in separators):
        ref = ref[:-4].strip()
        maxW -= width(year, font)
    else:
        year = ''
    if width(ref, font) > maxW:
        while width(ref+'…', font) > maxW:
            ref = ref[:-1]
        ref = ref + '…'
    return ref + year

def line_splitter(line: str, font: ImageFont.FreeTypeFont, maxW: int) -> list[str]:
    """ Performs an adaptive line break at the specified width in pixels """
    if width(line, font) < maxW:
        return [line]
    else:
        return splitter_postprocessing(recursive_split(line.split(), font, maxW))

def combine_words(word0: str, word1: str):
    """ Joining or rejoining lines of text """
    if (last_symbol := word0[-1]) == word1[0] and last_symbol in separators:
        combination = f'{word0}{word1[1:]}'
    else:
        combination = f'{word0} {word1}'
    return combination

def get_numeric_end(word: str):
    """ Returns the number contained at the end of the string """
    number = ''
    for i in range(len(word), 0, -1):
        if word[i-1].isnumeric():
            number = word[i-1:]
        else:
            break
    return number

def recursive_split(lst: list, font: ImageFont.FreeTypeFont, maxW: int):
    """ A function that recursively splits and joins the list of strings to match `maxW` """
    words_widths = tuple(width(word, font) for word in lst)
    if len(lst) > 10:
        # Prevent recursion infinite loop, there can be no more than a few lines
        raise RecursionError(f'{lst} is unexpectedly long')
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
                    # Moving a letter or a number per iteration
                    if (last_symbol := lst[i][-1]) in separators:
                        # don't hyphenate if already hyphenated
                        to_move = lst[i][-2]
                        lst[i] = lst[i][:-2] + last_symbol
                    elif (numeric_end := get_numeric_end(lst[i])) != '' and numeric_end != lst[i]:
                        # it's not good to split numbers, so attempt to get it all
                        to_move = numeric_end
                        lst[i] = lst[i][:-len(numeric_end)] + '-'
                    else:
                        # hyphenate the current line
                        to_move = last_symbol + ' '
                        lst[i] = lst[i][:-1] + '-'
                    try:
                        # adding to the next line
                        lst[i+1] = f'{to_move}{lst[i+1]}'
                    except IndexError:
                        # creating a new line
                        lst.append(to_move.strip())
                    lst = recursive_split(lst, font, maxW)
                break
    else:
        # Attempt to combine words
        for i in range(len(words_widths)-1):
            combination = combine_words(lst[i], lst[i+1])
            if width(combination, font) < maxW:
                lst[i] = combination
                lst.pop(i+1)
                lst = recursive_split(lst, font, maxW)
                break
    return lst

def splitter_postprocessing(lst: list):
    """ Removes hyphenation marks before footnotes """
    for i in range(1, len(lst)):
        if lst[i-1][-1] in separators and lst[i][0] in aux.superscript_digits:
            lst[i-1] = lst[i-1][:-1].strip()
    return lst
