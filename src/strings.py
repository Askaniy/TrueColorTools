
# Celestial bodies
names = {
    'Vega': {'ru': 'Вега', 'de': 'Wega'},
    'Sun': {'ru': 'Солнце', 'de': 'Sonne'},
    'Mercury': {'ru': 'Меркурий', 'de': 'Merkur'},
    'Venus': {'ru': 'Венера', 'de': 'Venus'},
    'Earth': {'ru': 'Земля', 'de': 'Erde'},
    'Moon': {'ru': 'Луна', 'de': 'Mond'},
    'Mars': {'ru': 'Марс', 'de': 'Mars'},
    'Phobos': {'ru': 'Фобос', 'de': 'Phobos'},
    'Deimos': {'ru': 'Деймос', 'de': 'Deimos'},
    'Jovian irregulars': {'ru': 'Нерег. сп. Юпитера', 'de': 'irreguläre Jupitermonde'},
    'Jupiter': {'ru': 'Юпитер', 'de': 'Jupiter'},
    'Io': {'ru': 'Ио', 'de': 'Io'},
    'Europa': {'ru': 'Европа', 'de': 'Europa'},
    'Ganymede': {'ru': 'Ганимед', 'de': 'Ganymed'},
    'Callisto': {'ru': 'Каллисто', 'de': 'Kallisto'},
    'Saturnian irregulars': {'ru': 'Нерег. сп. Сатурна', 'de': 'irreguläre Saturnmonde'},
    'Saturn': {'ru': 'Сатурн', 'de': 'Saturn'},
    'Rings': {'ru': 'Кольца', 'de': 'Ringe'},
    'Enceladus': {'ru': 'Энцелад', 'de': 'Enceladus'},
    'Tethys': {'ru': 'Тефия', 'de': 'Tethys'},
    'Dione': {'ru': 'Диона', 'de': 'Dione'},
    'Rhea': {'ru': 'Рея', 'de': 'Rhea'},
    'Titania': {'ru': 'Титания', 'de': 'Titania'},
    'Titan': {'ru': 'Титан', 'de': 'Titan'},
    'Uranian irregulars': {'ru': 'Нерег. сп. Урана', 'de': 'irreguläre Uranusmonde'},
    'Uranus': {'ru': 'Уран', 'de': 'Uranus'},
    'Miranda': {'ru': 'Миранда', 'de': 'Miranda'},
    'Ariel': {'ru': 'Ариэль', 'de': 'Ariel'},
    'Umbriel': {'ru': 'Умбриэль', 'de': 'Umbriel'},
    'Oberon': {'ru': 'Оберон', 'de': 'Oberon'},
    'Neptunian irregulars': {'ru': 'Нерег. сп. Нептуна', 'de': 'irreguläre Neptunmonde'},
    'Neptune': {'ru': 'Нептун', 'de': 'Neptun'},
    'Nereid': {'ru': 'Нереида', 'de': 'Nereid'},
    'Triton': {'ru': 'Тритон', 'de': 'Triton'},
    'Halley': {'ru': 'Галлея', 'de': 'Halley'},
    'Ceres': {'ru': 'Церера', 'de': 'Ceres'},
    'Pallas': {'ru': 'Паллада', 'de': 'Pallas'},
    'Juno': {'ru': 'Юнона', 'de': 'Juno'},
    'Vesta': {'ru': 'Веста', 'de': 'Vesta'},
    'Iris': {'ru': 'Ирида', 'de': 'Iris'},
    'Psyche': {'ru': 'Психея', 'de': 'Psyche'},
    'Kalliope': {'ru': 'Каллиопа', 'de': 'Kalliope'},
    'Euphrosyne': {'ru': 'Евфросина', 'de': 'Euphrosyne'},
    'Daphne': {'ru': 'Дафна', 'de': 'Daphne'},
    'Eugenia': {'ru': 'Евгения', 'de': 'Eugenia'},
    'Sylvia': {'ru': 'Сильвия', 'de': 'Sylvia'},
    'Antiope': {'ru': 'Антиопа', 'de': 'Antiope'},
    'Minerva': {'ru': 'Минерва', 'de': 'Minerva'},
    'Camilla': {'ru': 'Камилла', 'de': 'Camilla'},
    'Hermione': {'ru': 'Гермиона', 'de': 'Hermione'},
    'Elektra': {'ru': 'Электра', 'de': 'Elektra'},
    'Kleopatra': {'ru': 'Клеопатра', 'de': 'Kleopatra'},
    'Eros': {'ru': 'Эрос', 'de': 'Eros'},
    'Chiron': {'ru': 'Хирон', 'de': 'Chiron'},
    'Pholus': {'ru': 'Фол', 'de': 'Pholus'},
    'Chariklo': {'ru': 'Харикло', 'de': 'Chariklo'},
    'Varuna': {'ru': 'Варуна', 'de': 'Varuna'},
    'Itokawa': {'ru': 'Итокава', 'de': 'Itokawa'},
    'Quaoar': {'ru': 'Квавар', 'de': 'Quaoar'},
    'Sedna': {'ru': 'Седна', 'de': 'Sedna'},
    'Orcus': {'ru': 'Орк', 'de': 'Orcus'},
    'Vanth': {'ru': 'Вант', 'de': 'Vanth'},
    'Bennu': {'ru': 'Бенну', 'de': 'Bennu'},
    'Pluto': {'ru': 'Плутон', 'de': 'Pluto'},
    'Haumea': {'ru': 'Хаумеа', 'de': 'Haumea'},
    'Eris': {'ru': 'Эрида', 'de': 'Eris'},
    'Makemake': {'ru': 'Макемаке', 'de': 'Makemake'},
    'Arrokoth': {'ru': 'Аррокот', 'de': 'Arrokoth'},
    'Ultima': {'ru': 'Ультима', 'de': 'Ultima'},
    'Thule': {'ru': 'Туле', 'de': 'Thule'},
    'Akasa': {'ru': 'Акаса', 'de': 'Akasa'},
    'ʻOumuamua': {'ru': 'Оумуамуа', 'de': 'ʻOumuamua'},
    'Comets': {'ru': 'Кометы', 'de': 'Kometen'},
    'J. trojans': {'ru': 'Троянцы', 'de': 'J-Trojaner'},
    'Centaurs': {'ru': 'Кентавры', 'de': 'Zentauren'},
    'Plutinos': {'ru': 'Плутино', 'de': 'Plutinos'},
    'Other res.': {'ru': 'Др. рез.', 'de': 'Andere res.'},
    'Cubewano': {'ru': 'Классич.', 'de': 'Cubewano'},
    'SDO': {'ru': 'Рассеянный диск', 'de': 'SDO'},
    'Detached': {'ru': 'Обособл.', 'de': 'Detached'},
    'Class': {'ru': 'Класс', 'de': 'Spektraltyp'}
}

# Window
ref = {
    'en': 'References',
    'ru': 'Источники',
    'de': 'Quellen'
}
note = {
    'en': 'Notes',
    'ru': 'Примечания',
    'de': 'Anmerkungen'
}
gui_info = {
    'en': 'Info',
    'ru': 'О программе',
    'de': 'Info'
}
link = 'github.com/Askaniy/TrueColorTools'
auth_info = {
    'en': 'Askaniy Anpilogov, 2020-2023',
    'ru': 'Анпилогов Асканий, 2020-2023',
    'de': 'Askaniy Anpilogov, 2020-2023'
}
gui_exit = {
    'en': 'Exit',
    'ru': 'Выход',
    'de': 'Schließen'
}
langs = {
    'en': ['English', 'Английский', 'Englisch'],
    'ru': ['Russian', 'Русский', 'Russisch'],
    'de': ['German', 'Немецкий', 'Deutsch']
}
lang_list = {
    'en': ['Russian', 'German'],
    'ru': ['Английский', 'Немецкий'],
    'de': ['Englisch', 'Russisch']
}
gui_tabs = {
    'en': ['Spectra', 'Images', 'Table', 'Blackbody & Redshifts'],
    'ru': ['Спектры', 'Изображения', 'Таблица', 'АЧТ и красные смещения'],
    'de': ['Spektren', 'Bilder', 'Vergleich', 'Schwarzkörper & Rotverschiebung']
}
gui_menu = {
    'en': [['File', [ref['en'], note['en'], gui_info['en'], gui_exit['en']]], ['Language', lang_list['en']]],
    'ru': [['Файл', [ref['ru'], note['ru'], gui_info['ru'], gui_exit['ru']]], ['Язык', lang_list['ru']]],
    'de': [['Datei', [ref['de'], note['de'], gui_info['de'], gui_exit['de']]], ['Sprache', lang_list['de']]],
}

# Settings sidebar
gui_settings = {
    'en': 'Settings',
    'ru': 'Параметры',
    'de': 'Einstellungen'
}
gui_gamma = {
    'en': 'gamma correction',
    'ru': 'гамма-коррекция',
    'de': 'Gammakorrektur'
}
gui_br = {
    'en': ['Brightness display mode', 'true albedo', 'chromaticity'],
    'ru': ['Отображение яркости', 'альбедо', 'цветность'],
    'de': ['Helligkeitsmodus', 'Farbe mit Albedo', 'Farbton']
}
gui_interp = {
    'en': ['Interpolator/extrapolator', 'qualitatively', 'fast'],
    'ru': ['Интер/экстраполятор', 'качественно', 'быстро'],
    'de': ['Interpolation/Extrapolation', 'qualitativ', 'schnell']
}
gui_formatting = {
    'en': 'Output formatting',
    'ru': 'Форматирование',
    'de': 'Ausgabeformatierung'
}
gui_bit = {
    'en': 'Color depth (bit)',
    'ru': 'Глубина цвета',
    'de': 'Farbtiefe (bit)'
}
gui_rnd = {
    'en': 'Decimal places',
    'ru': 'Округление',
    'de': 'Dezimalstellen'
}

# Tab 1 - Spectra
gui_database = {
    'en': 'Database',
    'ru': 'База данных',
    'de': 'Datenbank'
}
gui_load = {
    'en': 'Load database',
    'ru': 'Загрузить базу данных',
    'de': 'Datenbank laden'
}
gui_update = {
    'en': 'Update database',
    'ru': 'Обновить базу данных',
    'de': 'Aktualisierung'
}
gui_tags = {
    'en': 'Category',
    'ru': 'Категория',
    'de': 'Kategorie'
}
gui_results = {
    'en': 'Output',
    'ru': 'Результат',
    'de': 'Ergebnisse'
}
gui_rgb = {
    'en': 'RGB color',
    'ru': 'Цвет RGB',
    'de': 'RGB Farbe'
}
gui_hex = {
    'en': 'HEX color',
    'ru': 'Цвет HTML',
    'de': 'HTML Farbe'
}
gui_add = {
    'en': 'Add spectrum to plot',
    'ru': 'Добавить спектр к графику',
    'de': 'Spektrum hinzufügen'
}
gui_plot = {
    'en': 'Plot spectra',
    'ru': 'Построить график спектров',
    'de': 'Spektren plotten'
}
gui_clear = {
    'en': 'Clear plot',
    'ru': 'Очистить график',
    'de': 'Klare Handlung'
}
gui_export = {
    'en': 'Export category colors',
    'ru': 'Экспортировать все цвета',
    'de': 'Farben der Kategorie exp.'
}
gui_save = {
    'en': 'Save',
    'ru': 'Сохранить',
    'de': 'Speichern'
}
gui_col = {
    'en': ['Red', 'Green', 'Blue', '| Object'],
    'ru': ['Красный', 'Зелёный', 'Синий', '| Объект'],
    'de': ['Rot', 'Grün', 'Blau', '| Objekt']
}

# Tab 2 - Images
gui_input = {
    'en': 'Input data',
    'ru': 'Входные данные',
    'de': 'Eingaben'
}
gui_band = {
    'en': 'Band',
    'ru': 'Канал',
    'de': 'Band'
}
gui_browse = {
    'en': 'Browse',
    'ru': 'Обзор',
    'de': 'Durchsuchen'
}
gui_wavelength = {
    'en': 'Wavelength [nm]',
    'ru': 'Длина волны [нм]',
    'de': 'Wellenlänge [nm]'
}
gui_exposure = {
    'en': 'Exposure',
    'ru': 'Экспозиция',
    'de': 'Belichtung'
}
gui_output = {
    'en': 'Processing and output',
    'ru': 'Обработка и вывод',
    'de': 'Verarbeitung und Ausgabe'
}
gui_makebright = {
    'en': 'Maximize brightness',
    'ru': 'Максимизировать яркость',
    'de': 'Maximieren Sie die Helligkeit'
}
gui_autoalign = {
    'en': 'Align bands (β)',
    'ru': 'Совместить (β)',
    'de': 'Ausrichten (β)'
}
gui_desun = {
    'en': 'Subtract the solar spectrum',
    'ru': 'Вычесть солнечный спектр',
    'de': 'Subtrahiere das Sonnenspektrum'
}
gui_plotpixels = {
    'en': 'Plot spectra of some pixels',
    'ru': 'Построить спектры некоторых пикселей',
    'de': 'Zeichnen Sie Spektren einiger Pixel'
}
gui_filterset = {
    'en': 'Camera filter set',
    'ru': 'Набор фильтров',
    'de': 'Kamera Filterset'
}
gui_single = {
    'en': 'Input RGB image',
    'ru': 'Ввод RGB изображения',
    'de': 'RGB-Bild eingeben'
}
gui_folder = {
    'en': 'Save file location',
    'ru': 'Путь сохранения',
    'de': 'Speicherort'
}
gui_preview = {
    'en': 'Show preview',
    'ru': 'Предпросмотр',
    'de': 'Vorschau anzeigen'
}
gui_process = {
    'en': 'Start processing',
    'ru': 'Обработать',
    'de': 'Bild erzeugen'
}

# Tab 3 - Table
gui_extension = {
    'en': 'File format',
    'ru': 'Расширение файла',
    'de': 'Dateiformat'
}
name_text = {
    'en': ['Colors calculated from spectra for the "', '" category'],
    'ru': ['Цвета, вычисленные по спектрам для категории «', '»'],
    'de': ['Farben von Himmelskörpen aus Spektren der "', '" Kategorie']
}
legend = {
    'en': 'Legend',
    'ru': 'Легенда',
    'de': 'Legende'
}
notes = {
    'B:': {'en': 'bright regions', 'ru': 'яркие участки', 'de': 'helle Regionen'},
    'D:': {'en': 'dark regions', 'ru': 'тёмные участки', 'de': 'dunkle Regionen'},
    'L:': {'en': 'leading hemisphere', 'ru': 'ведущее полушарие', 'de': 'führende Hemisphäre'},
    'T:': {'en': 'trailing hemisphere', 'ru': 'ведомое полушарие', 'de': 'folgende Hemisphäre'},
    'LP:': {'en': 'long-period', 'ru': 'долгопериодические', 'de': 'langperiodisch'},
    'SP:': {'en': 'short-period', 'ru': 'короткопериодические', 'de': 'kurzperiodisch'},
    'H:': {'en': 'hot, inner objects', 'ru': 'тёплые, внутренние объекты', 'de': 'heiße, innere Objekte'},
    'C:': {'en': 'cold, outer objects', 'ru': 'холодные, внешние объекты', 'de': 'kalte, äußere Objekte'}
}
info = {
    'en': ['Brightness mode', 'sRGB color space', 'Gamma correction'],
    'ru': ['Режим яркости', 'Пространство sRGB', 'Гамма-коррекция'],
    'de': ['Helligkeitsmodus', 'sRGB-Farbraum', 'Gammakorrektur']
}

# Tab 4 - Blackbody & Redshifts
gui_temp = {
    'en': 'Temperature [K]',
    'ru': 'Температура [K]',
    'de': 'Temperatur [K]'
}
gui_velocity = {
    'en': 'Velocity [c]',
    'ru': 'Скорость [c]',
    'de': 'Geschwindigkeit [c]'
}
gui_vII = {
    'en': 'Escape vel. [c]',
    'ru': 'II косм. ск. [c]',
    'de': 'Fluchtgeschw. [c]'
}
gui_irr = {
    'en': 'Irradiance [mag/nm]',
    'ru': 'Излуч. [зв. вел/нм]',
    'de': 'Bestrahlung [mag/nm]'
}
gui_surfacebr = {
    'en': 'Scale irradiance at λ=550 nm (lock exposure)',
    'ru': 'Регулировка яркости на λ=550 nm (задать экспозицию)',
    'de': 'Bestrahlungsstärke bei 550 nm skalieren (konstante Belichtung)'
}

# Tab 5 - WIP
gui_step1 = {
    'en': '1. Choose input data type',
    'ru': '1. Выберите формат вводимых данных',
    'de': '1. Eingabe-Datentyp auswählen'
}
gui_spectrum = {
    'en': 'Multiband spectrum',
    'ru': 'Многоканальный спектр',
    'de': 'Multiband Spektrum'
}
gui_image = {
    'en': 'Multiband image',
    'ru': 'Многоканальное изображение',
    'de': 'Multiband Aufnahme'
}
gui_step2 = {
    'en': '2. Match several filters with data',
    'ru': '2. Соотнесите фильтры с данными',
    'de': '2. Mehrere Filter an Daten anpassen'
}
gui_filter = {
    'en': 'Filter',
    'ru': 'Фильтр',
    'de': 'Filter'
}
gui_brightness = {
    'en': 'Brightness',
    'ru': 'Яркость',
    'de': 'Helligkeit'
}

# Plots
spectral_plot = {
    'en': 'Spectral plot',
    'ru': 'Спектральная диаграмма',
    'de': 'Spektraldiagramm'
}
#map_title_text = {
#    'en': 'Spectrum and color of some pixels of the map',
#    'ru': 'Спектр и цвет некоторых пикселей карты',
#    'de': 'Spektren und Farben einiger Pixel der Karte'
#}
xaxis_text = {
    'en': 'Wavelength [nm]',
    'ru': 'Длина волны [нм]',
    'de': 'Wellenlänge [nm]'
}
yaxis_text = {
    'en': 'Reflectivity',
    'ru': 'Отражательная способность',
    'de': 'Reflektivität'
}