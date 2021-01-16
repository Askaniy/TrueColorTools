
names = {
    "Vega": {"ru": "Вега", "de": ""},
    "Sun": {"ru": "Солнце", "de": ""},
    "Mercury": {"ru": "Меркурий", "de": ""},
    "Venus": {"ru": "Венера", "de": ""},
    "Earth": {"ru": "Земля", "de": ""},
    "Moon": {"ru": "Луна", "de": ""},
    "Mars": {"ru": "Марс", "de": ""},
    "Jupiter": {"ru": "Юпитер", "de": ""},
    "Io": {"ru": "Ио", "de": ""},
    "Europa": {"ru": "Европа", "de": ""},
    "Ganymede": {"ru": "Ганимед", "de": ""},
    "Callisto": {"ru": "Каллисто", "de": ""},
    "Saturn": {"ru": "Сатурн", "de": ""},
    "Rings": {"ru": "Кольца", "de": ""},
    "Rhea": {"ru": "Рея", "de": ""},
    "Titan": {"ru": "Титан", "de": ""},
    "Uranus": {"ru": "Уран", "de": ""},
    "Neptune": {"ru": "Нептун", "de": ""},
    "Pluto": {"ru": "Плутон", "de": ""},
    "Eris": {"ru": "Эрида", "de": ""},
    "Makemake": {"ru": "Макемаке", "de": ""},
    "Eros": {"ru": "Эрос", "de": ""},
    "Itokawa": {"ru": "Итокава", "de": ""},
    "Comets": {"ru": "Кометы", "de": ""},
    "J. trojans": {"ru": "Троянцы", "de": ""},
    "Centaurs": {"ru": "Кентавры", "de": ""},
    "Plutinos": {"ru": "Плутино", "de": ""},
    "Other res.": {"ru": "Др. рез.", "de": ""},
    "Classic": {"ru": "Классич.", "de": ""},
    "Scattered": {"ru": "Рассеянный диск", "de": ""},
    "Detached": {"ru": "Обособл.", "de": ""},
    "Class": {"ru": "Класс", "de": ""},
}

notes = {
    "B:": {"en": "bright regions", "ru": "яркие участки", "de": ""},
    "D:": {"en": "dark regions", "ru": "тёмные участки", "de": ""},
    "L:": {"en": "leading hemisphere", "ru": "ведущее полушарие", "de": ""},
    "T:": {"en": "trailing hemisphere", "ru": "ведомое полушарие", "de": ""},
    "LP:": {"en": "long-period", "ru": "долгопериодические", "de": ""},
    "SP:": {"en": "short-period", "ru": "короткопериодические", "de": ""},
    "H:": {"en": "hot, inner objects", "ru": "тёплые, внутренние объекты", "de": ""},
    "C:": {"en": "cold, outer objects", "ru": "холодные, внешние объекты", "de": ""},
    #"*": {"en": "from color indices", "ru": "из показателей цвета", "de": ""}
}

source = {
    "en": "Sources",
    "ru": "Источники",
    "de": ""
}
note = {
    "en": "Notes",
    "ru": "Примечания",
    "de": ""
}
info = {
    "en": "Anpilogov Askaniy, 2020-2021",
    "ru": "Анпилогов Асканий, 2020-2021",
    "de": ""
}

langs = {
    "en": ["English", "Английский"],
    "ru": ["Russian", "Русский"],
    "de": ["German", "Немецкий"]
}
lang_list = {
    "en": ["Russian", "German"],
    "ru": ["Английский", "Немецкий"],
    "de": [""]
}
gui_name = {
    "en": "True color calculator",
    "ru": "Калькулятор истинных цветов",
    "de": ""
}
gui_info = {
    "en": "Info",
    "ru": "О программе",
    "de": ""
}
gui_exit = {
    "en": "Exit",
    "ru": "Выход",
    "de": ""
}
gui_menu = {
    "en": [["File", [source["en"], note["en"], gui_info["en"], gui_exit["en"]]], ["Language", lang_list["en"]]],
    "ru": [["Файл", [source["ru"], note["ru"], gui_info["ru"], gui_exit["ru"]]], ["Язык", lang_list["ru"]]],
    "de": [["", ["", "", "", ""]], ["", lang_list["de"]]]
}
columns = {
    "en": ["Spectra", "Parameters", "Results"],
    "ru": ["Спектры", "Параметры", "Результат"],
    "de": [""]
}
gui_add = {
    "en": "Add spectrum to plot",
    "ru": "Добавить спектр к графику",
    "de": ""
}
gui_plot = {
    "en": "Plot added spectra",
    "ru": "Построить график спектров",
    "de": ""
}
gui_export = {
    "en": "Export all colors to console",
    "ru": "Экспортировать все цвета",
    "de": ""
}
gui_col = {
    "en": ["Red", "Green", "Blue", "Names"],
    "ru": ["Красный", "Зелёный", "Синий", "Названия"],
    "de": [""]
}
gui_gamma = {
    "en": "gamma correction",
    "ru": "гамма-коррекция",
    "de": ""
}
gui_br = {
    "en": ["Brightness display mode", "chromaticity", "normalization", "albedo"],
    "ru": ["Отображение яркости", "цветность", "нормализация", "альбедо"],
    "de": [""]
}
gui_interp = {
    "en": ["Interpolator/extrapolator", "default", "pchip", "cubic"],
    "ru": ["Интер/экстраполятор", "по умолчанию", "pchip", "кубич."],
    "de": [""]
}
gui_bit = {
    "en": "Color (bit) depth",
    "ru": "Битность цвета",
    "de": ""
}
gui_rnd = {
    "en": "Decimal places",
    "ru": "Округление",
    "de": ""
}
gui_apply = {
    "en": "Apply",
    "ru": "Применить",
    "de": ""
}
gui_rgb = {
    "en": "RGB color",
    "ru": "Цвет RGB",
    "de": ""
}
gui_hex = {
    "en": "HEX color",
    "ru": "Цвет HEX",
    "de": ""
}

name_text = {
    "en": "Colors of celestial bodies from spectra",
    "ru": "Цвета небесных тел, полученные из спектров",
    "de": ""
}

single_title_text = {
    "en": "Spectrum and color of ",
    "ru": "Спектр и цвет объекта ",
    "de": ""
}
batch_title_text = {
    "en": "Spectra and colors of ",
    "ru": "Спектр и цвет следующих объектов: ",
    "de": ""
}
table_title_text = {
    "en": "Spectra and colors of celestial bodies",
    "ru": "Спектры и цвета космических объектов",
    "de": ""
}
xaxis_text = {
    "en": "Wavelength [nm]",
    "ru": "Длина волны [нм]",
    "de": ""
}
yaxis_text = {
    "en": "Reflectivity",
    "ru": "Отражательная способность",
    "de": ""
}

error1 = {
    "en": ["Error 1: mismatch in the number of coordinates to create a spectrum.", "Object name: {}\nWavelength values: {}\nBrightness values: {}"],
    "ru": ["Ошибка 1: несовпадение количества координат для построения спектра.", "Название объекта: {}\nЗначений длин волн: {}\nЗначений яркости: {}"],
    "de": [""]
}

error2 = {
    "en": ["Error 2: value of one of the color bands is negative.", "Object name: {}\nR: {}\nG: {}\nB: {}"],
    "ru": ["Ошибка 2: яркость одного из цветов получилась отрицательной.", "Название объекта: {}\nR: {}\nG: {}\nB: {}"],
    "de": [""]
}