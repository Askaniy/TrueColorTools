""" Provides a table generation function, generate_table(). """

from PIL import Image, ImageDraw, ImageFont
from math import ceil, sqrt
import src.data_import as di
import src.data_processing as dp
import src.color_processing as cp
import src.strings as tr


def generate_table(objectsDB: dict, tag: str, brMode: bool, srgb: bool, gamma: bool, folder: str, extension: str, lang: str):
    """ Creates and saves a table of colored squares for each spectral data unit that has the specified tag """
    objects = di.obj_dict(objectsDB, tag, lang)
    l = len(objects)

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
    rounding_radius = 8 # rounding radius
    r_left= r-3 # active space
    r_right = r-3
    w_border = 8 # pixels of left and right spaces
    h_border = 16 # pixels of top and bottom spaces

    # Calculating grid widths
    min_obj_to_scale = 6
    objects_per_raw = min(max(l, min_obj_to_scale), ceil(sqrt(1.5*l))) # strives for a 3:2 aspect ratio
    w_table = 2*half_square*objects_per_raw
    w = 2*w_border + w_table # image width
    w0 = w_border + half_square - r # using shift width
    w1 = int(w * 0.618034) # golden ratio for the info column

    # Support for multiline title
    title_lines = line_splitter(tag.join(tr.table_title[lang]), name_font, w_table)
    title = '\n'.join(title_lines)
    name_size *= len(title_lines)

    # Notes calculations
    notes_per_column = 4 # number of info lines
    notes = di.notes_list(objects.keys()) # not in the main cycle because may influence on the template
    notes_flag = bool(notes)
    if notes_flag:
        notes_numbered = [f'{superscript(note_num+1)} {note}' for note_num, note in enumerate(notes)]
        w_notes = w0 + max(width(note_text, note_font) for note_text in notes_numbered) # notes columns width
        notes_columns_num = (w1 - w0) // w_notes # max possible number of columns
        if notes_per_column * notes_columns_num < len(notes):
            notes_per_column = round(len(notes) // notes_columns_num + 1)

    # Calculating grid hights
    h0 = h_border + name_size
    h1 = h0 + 2*half_square * int(ceil(l / objects_per_raw)) + note_step
    h2 = h1 + help_step
    h = h1 + help_step + notes_per_column*note_step + h_border # image hight

    # Create image template
    img = Image.new('RGB', (w, h), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.multiline_text( # text brightness formula: br = 255 * (x^(1/2.2))
        xy=(int(w/2), int(h0/2)), text=title, fill=(255, 255, 255),
        font=name_font, anchor='mm', align='center', spacing=0
    )

    # Notes writing
    if notes_flag:
        draw.text((w0, h1), tr.notes_label[lang], fill=(230, 230, 230), font=help_font, anchor='la') # x = 0.8, br = 230
        for note_num, note in enumerate(notes): # x = 0.5, br = 186
            draw.text(
                xy=(w0 + w_notes * (note_num // notes_per_column), h2 + note_step * (note_num % notes_per_column)),
                text=notes_numbered[note_num], fill=(186, 186, 186), font=note_font, anchor='la'
            )
    
    # Info writing
    draw.text((w1, h1), tr.info_label[lang], fill=(230, 230, 230), font=help_font, anchor='la') # x = 0.8, br = 230
    draw.text(
        xy=(w1, h2), text=f'{tr.info_gamma[lang]}: {tr.info_indicator[lang][gamma]}',
        fill=(224, 224, 224), font=note_font, anchor='la' # x = 0.75, br = 224
    )
    draw.text(
        xy=(w1, h2+note_step), text=f'{tr.info_sRGB[lang]}: {tr.info_indicator[lang][srgb]}',
        fill=(224, 224, 224), font=note_font, anchor='la' # x = 0.75, br = 224
    )
    draw.text(
        xy=(w1, h2+note_step*2), text=f'{tr.gui_br[lang][0]}: {tr.gui_br[lang][brMode+1]}',
        fill=(224, 224, 224), font=note_font, anchor='la' # x = 0.75, br = 224
    )
    draw.text((w1, h2+note_step*3), tr.link, fill=(0, 200, 255), font=note_font, anchor='la')
    
    # Table generator
    n = 0 # object counter
    for name, raw_name in objects.items():

        # Spectral data import and processing
        body = dp.database_parser(name, objectsDB[raw_name])
        albedo = brMode and isinstance(body, dp.ReflectiveBody)

        # Setting brightness mode
        match brMode:
            case 0:
                spectrum = body.get_spectrum('chromaticity')
            case 1:
                spectrum = body.get_spectrum('geometric')
            case 2:
                spectrum = body.get_spectrum('spherical')
        
        # Color calculation
        if srgb:
            color = cp.Color.from_spectrum_CIE(spectrum, albedo)
        else:
            color = cp.Color.from_spectrum(spectrum, albedo)
        if gamma:
            color = color.gamma_corrected()
        rgb = color.to_bit(8)
        rgb_show = color.to_html()

        # Object drawing
        center_x = w_border + half_square + 2*half_square * (n%objects_per_raw)
        center_y = h0 + half_square + 2*half_square * int(n/objects_per_raw)
        #draw.rounded_rectangle((center_x-r, center_y-r, center_x+r, center_y+r), rounding_radius, rgb_show)
        draw_rounded_square((center_x, center_y), r, rounding_radius, rgb_show, img, 4)
        
        text_color = (0, 0, 0) if rgb.mean() >= 127 else (255, 255, 255)
        
        # Name processing
        workaround_shift = 3 # it is not possible to use "lt" and "rt" anchors for multiline text https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html
        
        ref_len = 0 # to avoid intersections with indices in the left corner
        if '[' in name:
            parts = name.split('[', 1)
            name = parts[0].strip()
            ref = parts[1][:-1]
            if ',' in ref: # check for several references, no more than 3 supported
                refs = [i.strip() for i in ref.split(',', 2)]
                ref = '\n'.join(refs) 
                ref_len = width(refs[0], small_font)
            elif ref[-4:].isnumeric() and (ref[-5].isalpha() or ref[-5] in separators): # check for the year in the reference name to print it on the second line
                author = ref[:-4].strip()
                year = ref[-4:]
                if width(author, small_font) > width(year, small_font):
                    ref = f'{author}\n{year}'
                    ref_len = width(author, small_font)
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
        n += 1
    
    file_name = f'TCT_{lang}_{tag}_gamma{("OFF", "ON")[gamma]}_srgb{("OFF", "ON")[srgb]}_albedo{("OFF", "GEOM", "SPHER")[brMode]}.{extension}'
    img.save(f'{folder}/{file_name}')
    print(f'Color table saved as {file_name}\n')

def draw_rounded_square(xy: tuple[float, float], half_size: int, radius: float, fill: str, img: Image.Image, factor: int):
    """
    Workaround for drawing rounded squares with anti-aliasing.
    See https://github.com/python-pillow/Pillow/issues/5577
    """
    temp_size = half_size * factor
    temp_img = Image.new('RGB', (temp_size, temp_size), (0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    temp_draw.rounded_rectangle((0, 0, temp_size, temp_size), radius*factor/2, fill)
    size = half_size * 2
    temp_img = temp_img.resize((size+1, size+1))
    img.paste(temp_img, (xy[0]-half_size, xy[1]-half_size))

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