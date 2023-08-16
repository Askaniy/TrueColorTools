import io
import time
import numpy as np
import PySimpleGUI as sg
from PIL import Image, ImageDraw
import src.core as core


# This file needs revision


def convert_to_bytes(img: Image.Image):
    """ Prepares PIL's image to be displayed in the window """
    bio = io.BytesIO()
    img.save(bio, format='png')
    del img
    return bio.getvalue()

def preview_size(area, ratio):
    return int(np.sqrt(area*ratio)), int(np.sqrt(area/ratio))

def image_processing(input_data: dict):
    t = time.monotonic()
    load = []

    if input_data['single']:
        rgb_img = Image.open(input_data['path'])
        
        if rgb_img.mode == 'P': # NameError if color is indexed
            rgb_img = rgb_img.convert('RGB')
            sg.Print('Note: image converted from "P" (indexed color) mode to "RGB"')
        if input_data['preview']:
            ratio = rgb_img.width / rgb_img.height
            rgb_img = rgb_img.resize(preview_size(input_data['area'], ratio), resample=Image.Resampling.HAMMING)
        if len(rgb_img.getbands()) == 3:
            r, g, b = rgb_img.split()
            a = None
        elif len(rgb_img.getbands()) == 4:
            r, g, b, a = rgb_img.split()
        for i in [b, g, r]:
            load.append(np.array(i))
    else:
        exposures = input_data['exposures']
        max_exposure = max(exposures)
        for i in range(input_data['vis']):
            bw_img = Image.open(input_data['paths'][i])
            if bw_img.mode not in ('L', 'I', 'F'): # image should be b/w
                sg.Print(f'Note: image of band {i+1} converted from "{bw_img.mode}" mode to "L"')
                bw_img = bw_img.convert('L')
            if i == 0:
                size = bw_img.size
            else:
                if size != bw_img.size:
                    sg.Print(f'Note: image of band {i+1} resized from {bw_img.size} to {size}')
                    bw_img = bw_img.resize(size)
            if input_data['preview']:
                ratio = bw_img.width / bw_img.height
                bw_img = bw_img.resize(preview_size(input_data['area'], ratio), resample=Image.Resampling.HAMMING)
            load.append(np.array(bw_img) / exposures[i] * max_exposure)
    
    data = np.array(load, 'int64')
    l, h, w = data.shape
    
    if input_data['autoalign']:
        data = experimental_autoalign(data, debug=False)
        l, h, w = data.shape
    
    data = data.astype('float32')
    data_max = data.max()
    if input_data['makebright']:
        data *= 65500 / data_max
        input_bit = 16
        input_depth = 65535
    else:
        input_bit = 16 if data_max > 255 else 8
        input_depth = 65535 if data_max > 255 else 255
    #data = np.clip(data, 0, input_depth)

    img = Image.new('RGB', (w, h), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    counter = 0
    px_num = w*h

    sg.Print(f'\n{round(time.monotonic() - t, 3)} seconds for loading, autoalign and creating output templates\n')
    sg.Print(f'{time.strftime("%H:%M:%S")} 0%')

    t = time.monotonic()
    get_spectrum_time = 0
    calc_polator_time = 0
    calc_rgb_time = 0
    draw_point_time = 0
    plot_pixels_time = 0
    progress_bar_time = 0

    for x in range(w):
        for y in range(h):

            temp_time = time.monotonic_ns()
            slice = data[:, y, x]
            get_spectrum_time += time.monotonic_ns() - temp_time

            if np.sum(slice) > 0:
                name = f'({x}; {y})'

                temp_time = time.monotonic_ns() # Spectral data processing
                spectrum = core.Spectrum(name, input_data['nm'], list(slice), scope=core.visible_range)
                if input_data['desun']:
                    spectrum /= core.sun_norm
                calc_polator_time += time.monotonic_ns() - temp_time

                temp_time = time.monotonic_ns() # Color calculation
                if input_data['srgb']:
                    color = core.Color.from_spectrum(spectrum, albedo=True)
                else:
                    color = core.Color.from_spectrum_legacy(spectrum, albedo=True)
                if input_data['gamma']:
                    color = color.gamma_corrected()
                color.rgb /= input_bit
                rgb = tuple(color.to_bit(8).round().astype(int))
                calc_rgb_time += time.monotonic_ns() - temp_time

                temp_time = time.monotonic_ns()
                draw.point((x, y), rgb)
                draw_point_time += time.monotonic_ns() - temp_time

            temp_time = time.monotonic_ns()
            counter += 1
            if counter % 2048 == 0:
                try:
                    sg.Print(f'{time.strftime("%H:%M:%S")} {round(counter/px_num * 100)}%, {round(counter/(time.monotonic()-t))} px/sec')
                except ZeroDivisionError:
                    sg.Print(f'{time.strftime("%H:%M:%S")} {round(counter/px_num * 100)}% (ZeroDivisionError)')
            progress_bar_time += time.monotonic_ns() - temp_time
    
    end_time = time.monotonic()
    sg.Print(f'\n{round(end_time - t, 3)} seconds for color processing, where:')
    sg.Print(f'\t{get_spectrum_time / 1e9} for getting spectrum')
    sg.Print(f'\t{calc_polator_time / 1e9} for inter/extrapolating')
    sg.Print(f'\t{calc_rgb_time / 1e9} for color calculating')
    sg.Print(f'\t{draw_point_time / 1e9} for pixel drawing')
    sg.Print(f'\t{plot_pixels_time / 1e9} for adding spectrum to plot')
    sg.Print(f'\t{progress_bar_time / 1e9} for progress bar')
    sg.Print(f'\t{round(end_time-t-(get_spectrum_time+calc_polator_time+calc_rgb_time+draw_point_time+plot_pixels_time+progress_bar_time)/1e9, 3)} for other (time, black-pixel check)')

    if not input_data['preview']:
        img.save(f'{input_data["save"]}/TCT_{time.strftime("%Y-%m-%d_%H-%M")}.png')

    return img




# Align multiband image

def experimental_autoalign(data: np.ndarray, debug: bool):
    l, h, w = data.shape
    sums_x = []
    sums_y = []
    for layer in data:
        sums_x.append(np.sum(layer, 0))
        sums_y.append(np.sum(layer, 1))
    shifts0_x = relative_shifts(square(sums_x))
    shifts0_y = relative_shifts(square(sums_y))
    if debug:
        print("\nBase", shifts0_x, shifts0_y)
    
    shiftsR_x = []
    shiftsR_y = []
    for i in range(l-1):
        shift_x, shift_y = recursive_shift(square(data[i]), square(data[i+1]), shifts0_x[i], shifts0_y[i], debug)
        shiftsR_x.append(shift_x)
        shiftsR_y.append(shift_y)
    if debug:
        print("\nRecursion", shiftsR_x, shiftsR_y)
    
    #corrections_x = []
    #corrections_y = []
    #for l in range(l-1):
    #    arr0, arr1 = square(data[l]), square(data[l+1])
    #    coord = (0, 0)
    #    min = 1e18
    #    for i in range(-25, 26):
    #        for j in range(-25, 26):
    #            diff = abs(np.sum(np.abs(arr0 - np.roll(arr1, (shifts0_y[l]+j, shifts0_x[l]+i)))))
    #            if diff < min:
    #                min = diff
    #                coord = (i, j)
    #                print(min, coord)
    #    corrections_x.append(coord[0])
    #    corrections_y.append(coord[1])
    #quit()
    #if debug:
    #   print("\nCorrection", corrections_x, corrections_y)
    #shiftsC_x = np.array(shifts0_x) + np.array(corrections_x)
    #shiftsC_y = np.array(shifts0_y) + np.array(corrections_y)
    #if debug:
    #   print("\nCorrected", shiftsC_x, shiftsC_y)
    
    shifts_x = absolute_shifts(shiftsR_x)
    shifts_y = absolute_shifts(shiftsR_y)
    w = w + shifts_x.min()
    h = h + shifts_y.min()
    for i in range(l):
        data[i] = np.roll(data[i], (shifts_y[i], shifts_x[i]))
    data = data[:, :h, :w]
    return data

def square(array: np.ndarray):
    return np.multiply(array, array)
    #return np.clip(array, np.mean(array), None)

def mod_shift(c, size): # 0->size shift to -s/2->s/2
    size05 = int(size/2) # floor rounding
    return (c+size05)%size-size05

def relative_shifts(sums):
    diffs = []
    for i in range(len(sums)-1):
        size = len(sums[i])
        temp_diff_list = []
        for j in range(size):
            diff = np.abs(sums[i] - np.roll(sums[i+1], j))
            temp_diff_list.append(np.sum(diff))
        diffs.append(mod_shift(np.argmin(temp_diff_list), size))
    return diffs

def recursive_shift(img0: np.ndarray, img1: np.ndarray, shift_x, shift_y, debug):
    if debug:
        print("\nstart of recursion with ", shift_x, shift_y)
    diff0 = abs(np.sum(np.abs(img0 - np.roll(img1, (shift_y, shift_x)))))
    diffU = abs(np.sum(np.abs(img0 - np.roll(img1, (shift_y-1, shift_x)))))
    diffD = abs(np.sum(np.abs(img0 - np.roll(img1, (shift_y+1, shift_x)))))
    diffL = abs(np.sum(np.abs(img0 - np.roll(img1, (shift_y, shift_x-1)))))
    diffR = abs(np.sum(np.abs(img0 - np.roll(img1, (shift_y, shift_x+1)))))
    diffUL = abs(np.sum(np.abs(img0 - np.roll(img1, (shift_y-1, shift_x-1)))))
    diffUR = abs(np.sum(np.abs(img0 - np.roll(img1, (shift_y-1, shift_x+1)))))
    diffDL = abs(np.sum(np.abs(img0 - np.roll(img1, (shift_y+1, shift_x-1)))))
    diffDR = abs(np.sum(np.abs(img0 - np.roll(img1, (shift_y+1, shift_x+1)))))
    if debug:
        print(f'{diffUL} {diffU} {diffUR}\n{diffL} {diff0} {diffR}\n{diffDL} {diffD} {diffDR}')
    argmin = np.argmin((diff0, diffU, diffD, diffL, diffR, diffUL, diffUR, diffDL, diffDR))
    if argmin != 0: # box 3x3
        if argmin == 1:
            shift_y -= 1
        elif argmin == 2:
            shift_y += 1
        elif argmin == 3:
            shift_x -= 1
        elif argmin == 4:
            shift_x += 1
        elif argmin == 5:
            shift_x -= 1
            shift_y -= 1
        elif argmin == 6:
            shift_x += 1
            shift_y -= 1
        elif argmin == 7:
            shift_x -= 1
            shift_y += 1
        elif argmin == 8:
            shift_x += 1
            shift_y += 1
        return recursive_shift(img0, img1, shift_x, shift_y, debug)
    else:
        return shift_x, shift_y
    #while True:
    #    if debug:
    #        print("\nstart of recursion with ", shift_x, shift_y)
    #    diffs = []
    #    for i in range(9):
    #        x = i % 3 - 1
    #        y = i // 3 - 1
    #        diff = abs(np.sum(np.abs(img0 - np.roll(img1, (shift_y+y, shift_x+x)))))
    #        diffs.append(diff)
    #    if debug:
    #        for i in range(3):
    #            for j in range(3):
    #                sys.stdout.write(str(diffs[i*3+j]) + " ")
    #            print("")
    #    argmin = np.argmin(diffs)
    #    shift_x += argmin % 3 - 1
    #    shift_y += argmin // 3 - 1
    #    print(argmin)
    #    print(diffs)
    #    if argmin == 4:
    #        break
    #return shift_x, shift_y

def absolute_shifts(diffs):
    p = [0]
    for d in diffs:
        p.append(p[-1]+d)
    return np.array(p) - max(p)