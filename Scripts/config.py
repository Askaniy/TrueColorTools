import locale
import ctypes
import inspect
import os
import sys
import translator as tr

def lang(manually=""):
    if manually == "": # Automatic system language detection
        return locale.windows_locale[ctypes.windll.kernel32.GetUserDefaultUILanguage()][:2]
    else:
        for lang, names in tr.langs.items():
            if manually == lang or manually in names:
                return lang

def folder(manually="", follow_symlinks=True):
    if manually == "": # Automatic main folder path detection (by jfs)
        if getattr(sys, "frozen", False): # py2exe, PyInstaller, cx_Freeze
            path = os.path.abspath(sys.executable)
        else:
            path = inspect.getabsfile(folder)
        if follow_symlinks:
            path = os.path.realpath(path)
        return os.path.dirname("/".join(path.split("\\")[:-1]))
    else:
        return lang