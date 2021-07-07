import locale
import ctypes
import inspect
import os
import sys
import config, strings

def lang_check(name):
    for lang, names in strings.langs.items():
        if name.lower() == lang or name.title() in names:
            return lang
    return "en"

def lang(manually=""):
    if manually != "":
        return lang_check(manually)
    elif config.language != "":
        return lang_check(config.language)
    else: # Automatic system language detection
        return lang_check(locale.windows_locale[ctypes.windll.kernel32.GetUserDefaultUILanguage()][:2])

def folder(manually=""):
    if manually != "":
        return manually
    elif config.folder != "":
        return config.folder
    else: # Automatic main folder path detection
        if getattr(sys, "frozen", False): # py2exe, PyInstaller, cx_Freeze
            path = os.path.abspath(sys.executable)
        else:
            path = inspect.getabsfile(folder)
        path = os.path.realpath(path) # follow symlinks
        return os.path.dirname("/".join(path.split("\\")[:-1]))