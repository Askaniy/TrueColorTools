"""
Small presentation helpers with no computational dependencies.

Numerical and spectral helpers formerly collected here now live in
AstroColor. TCT keeps only the formatting utilities used by the GUI and the
color-table renderer.
"""

from collections.abc import Sequence

import numpy as np


def export_colors(rgb: tuple) -> str:
    """ Generates formatted string of colors """
    lst = []
    mx = 0
    for i in rgb:
        lst.append(str(i))
        mx = max(mx, len(lst[-1]))
    w = 8 if mx < 8 else mx + 1
    return ''.join([i.ljust(w) for i in lst])

def get_flag_index(flags: tuple) -> int:
    """ Returns index of active radio button """
    for index, flag in enumerate(flags):
        if flag:
            return index
    return 0


def higher_dim(arr: Sequence | float, times: int, axis: int = 1):
    """ Gets the array and repeats it along a new dimension """
    return np.repeat(np.expand_dims(arr, axis=axis), times, axis=axis)


def extended_log10(value: float | np.floating) -> float:
    """ Returns log10(value), with 0 mapped to 0 instead of minus infinity """
    return np.log10(value) if value != 0 else 0.


illegal_chars = (
    '#',  # pound
    '%',  # percent
    '&',  # ampersand
    '{',  # left curly bracket
    '}',  # right curly bracket
    '\\', # backslash
    '<',  # left angle bracket
    '>',  # right angle bracket
    '*',  # asterisk
    '?',  # question mark
    '/',  # forward slash
    ' ',  # blank spaces
    '$',  # dollar sign
    '!',  # exclamation point
    "'",  # single quotes
    '"',  # double quotes
    ':',  # colon
    '@',  # at sign
    '+',  # plus sign
    '`',  # backtick
    '|',  # pipe
    '=',  # equal sign
)


def normalize_string(string: str) -> str:
    """ Removes characters invalid for file names """
    result = ''
    for char in string:
        if char not in illegal_chars:
            result += char
    return result


superscript_digits = '⁰¹²³⁴⁵⁶⁷⁸⁹'

def superscript(number: int | str) -> str:
    """ Converts a number to a superscript string """
    return ''.join([superscript_digits[int(digit)] for digit in str(number)])


subscript_digits = '₀₁₂₃₄₅₆₇₈₉'

def subscript(number: int | str) -> str:
    """ Converts a number to a subscript string """
    return ''.join([subscript_digits[int(digit)] for digit in str(number)])


subscript_signs = {
    '+': '', #'⁺',
    '-': '⁻'
}

def exponential_notation(value: float) -> str:
    """ Converts a number to a string in exponential notation """
    mantissa, exponent = f'{value:.2E}'.split('E')
    sign = subscript_signs[exponent[0]]
    exponent = superscript(int(exponent[1:]))
    return f'{mantissa} ⋅ 10{sign}{exponent}'
