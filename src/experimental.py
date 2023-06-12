import numpy as np


# Phase curves processing functions

def lambert(phase: float):
    phi = abs(np.deg2rad(phase))
    return (np.sin(phi) + np.pi * np.cos(phi) - phi * np.cos(phi)) / np.pi # * 2/3 * albedo


# Align mustispectral image bands

def autoalign(data: np.ndarray, debug: bool):
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