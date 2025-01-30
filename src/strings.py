""" Localization file, contains almost all the strings used """


# Menu bar
gui_menu = {
    'en': 'Menu',
    'ru': 'Меню',
    'de': 'Menü'
}
gui_ref = {
    'en': 'References',
    'ru': 'Источники',
    'de': 'Quellen'
}
gui_info = {
    'en': 'Info',
    'ru': 'О программе',
    'de': 'Info'
}
link = 'github.com/Askaniy/TrueColorTools'
auth_info = {
    'en': 'Askaniy Anpilogov, 2020-2024',
    'ru': 'Анпилогов Асканий, 2020-2024',
    'de': 'Askaniy Anpilogov, 2020-2024'
}
gui_exit = {
    'en': 'Exit',
    'ru': 'Выход',
    'de': 'Schließen'
}
gui_language = {
    'en': 'Language',
    'ru': 'Язык',
    'de': 'Sprache'
}
langs = {
    'English': 'en',
    'Русский': 'ru',
    'Deutsch': 'de'
}
gui_no_data_message = {
    'en': 'You need to load the database to get this data.',
    'ru': 'Вам нужно загрузить базу данных для получения этих данных.',
    'de': 'Sie müssen die Datenbank laden, um diese Daten abzurufen.'
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
gui_gamma_note = {
    'en': 'Takes into account the non-linearity of brightness perception of the human eye',
    'ru': 'Учитывает нелинейность восприятия яркости человеческого глаза',
    'de': 'Berücksichtigt die Nichtlinearität der Helligkeitswahrnehmung des menschlichen Auges'
}
gui_srgb_note = {
    'en': 'CIE sRGB color space with Illuminant E',
    'ru': 'Цветовое пространство CIE sRGB с осветителем E',
    'de': 'CIE sRGB-Farbraum mit Normlicht E'
}
gui_brMode = {
    'en': 'Brightness mode',
    'ru': 'Режим яркости',
    'de': 'Helligkeitsmodus'
}
gui_brMax = {
    'en': 'maximize',
    'ru': 'максимизировать',
    'de': 'maximieren'
}
gui_chromaticity = {
    'en': 'chromaticity',
    'ru': 'цветность',
    'de': 'Farbton'
}
gui_geom = {
    'en': 'geometric albedo',
    'ru': 'геом. альбедо',
    'de': 'geometrische Albedo'
}
gui_geom_note = {
    'en': 'Flux ratio to the Lambertian disk flux with the same cross-sectional area at a phase angle of 0°',
    'ru': 'Отношение потока к потоку ламбертового диска с той же площадью сечения при фазовом угле 0°',
    'de': 'Flussverhältnis zum Lambertschen Strahler mit gleicher Querschnittsfläche bei einem Phasenwinkel von 0°'
}
gui_sphe = {
    'en': 'spherical albedo',
    'ru': 'сфер. альбедо',
    'de': 'sphärische Albedo'
}
gui_sphe_note = {
    'en': 'Ratio of scattered light to incident light in all directions',
    'ru': 'Отношение рассеянного света к падающему по всем направлением',
    'de': 'Verhältnis von gestreutem zu einfallendem Licht über alle Richtungen'
}
#gui_interp = {
#    'en': ['Interpolator/extrapolator', 'old', 'new'],
#    'ru': ['Интер/экстраполятор', 'старый', 'новый'],
#    'de': ['Interpolation/Extrapolation', 'alt', 'neu']
#}
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

#gui_input = {
#    'en': 'Input data',
#    'ru': 'Входные данные',
#    'de': 'Eingaben'
#}
gui_output = {
    'en': 'Output',
    'ru': 'Результат',
    'de': 'Ergebnisse'
}
gui_tabs = {
    'en': ['Database viewer', 'Image processing', 'Blackbody & Redshifts'],
    'ru': ['Просмотр базы спектров', 'Обработка изображений', 'АЧТ и красные смещения'],
    'de': ['Datenbank-Viewer', 'Bildverarbeitung', 'Schwarzkörper & Rotverschiebung']
}

# Tab 1 - Database viewer
#gui_database = {
#    'en': 'Database',
#    'ru': 'База данных',
#    'de': 'Datenbank'
#}
gui_load = {
    'en': 'Load the database',
    'ru': 'Загрузить базу данных',
    'de': 'Datenbank laden'
}
gui_reload = {
    'en': 'Reload the database',
    'ru': 'Перезагрузить базу данных',
    'de': 'Aktualisieren'
}
gui_tags = {
    'en': 'Category',
    'ru': 'Категория',
    'de': 'Kategorie'
}
gui_no_albedo = {
    'en': 'Note: No albedo data.',
    'ru': 'Прим.: Нет данных об альбедо.',
    'de': 'Hinweis: Keine Albedodaten.'
}
gui_estimated = {
    'en': 'Note: The albedo is estimated.',
    'ru': 'Прим.: Данное альбедо — теор. оценка.',
    'de': 'Hinweis: Die Albedo ist eine Schätzung.'
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
gui_in_filter = {
    'en': 'in filter',
    'ru': 'в фильтре',
    'de': 'im Filter'
}
gui_plot = {
    'en': 'Show the plot',
    'ru': 'Показать график',
    'de': 'Diagramm anzeigen'
}
gui_pin = {
    'en': 'Pin the spectrum',
    'ru': 'Закрепить спектр',
    'de': 'Aktuelles Spektrum beibehalten'
}
#gui_unpin = {
#    'en': 'Unpin the spectrum plot',
#    'ru': 'Открепить график спектра',
#    'de': 'Freigabe des Spektrumsdiagramms'
#}
gui_clear = {
    'en': 'Clear the plot',
    'ru': 'Очистить график',
    'de': 'Plot löschen'
}
gui_export2text = {
    'en': 'Export category to text',
    'ru': 'Экспортировать в текст',
    'de': 'Kategorie als Text exportieren'
}
gui_export2table = {
    'en': 'Export category to table',
    'ru': 'Экспортировать в таблицу',
    'de': 'Kategorie als Tabelle exportieren'
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
table_title = {
    'en': ['The “', '” category color table'],
    'ru': ['Таблица цветов для категории «', '»'],
    'de': ['Farbtabelle der Kategory „', '“']
}
table_no_albedo = {
    'en': 'no albedo',
    'ru': 'нет альбедо',
    'de': 'keine Albedo'
}
table_estimated = {
    'en': 'estimated albedo',
    'ru': 'оценка альбедо',
    'de': 'geschätzte Albedo'
}
legend = {
    'en': 'Legend',
    'ru': 'Легенда',
    'de': 'Legende'
}
notes_label = {
    'en': 'Notes',
    'ru': 'Примечания',
    'de': 'Anmerkungen'
}
info_label = {
    'en': 'Info',
    'ru': 'Информация',
    'de': 'Info'
}
info_objects = {
    'en': 'objects displayed',
    'ru': 'объектов показано',
    'de': 'Objekte werden angezeigt'
}
info_srgb = {
    'en': 'sRGB color space',
    'ru': 'Пространство sRGB',
    'de': 'sRGB-Farbraum'
}
info_gamma = {
    'en': 'Gamma correction',
    'ru': 'Гамма-коррекция',
    'de': 'Gammakorrektur'
}
info_indicator = {
    'en': ('off', 'on'),
    'ru': ('выкл', 'вкл'),
    'de': ('Inaktiv', 'Aktiv')
}

# Tab 2 - Image processing
gui_step1 = {
    'en': 'Choose the input data type',
    'ru': 'Выберите формат вводимых данных',
    'de': 'Eingabe-Datentyp auswählen'
}
gui_datatype = {
    'en': ['Multiband image', 'RGB image', 'Spectral cube'],
    'ru': ['Многоканальное изображение', 'RGB изображение', 'Спектральный куб'],
    'de': ['Multiband Aufnahme', 'RGB-Bild', 'Spektralwürfel']
}
gui_RGBcolors = {
    'en': ['Blue channel', 'Green channel', 'Red channel'],
    'ru': ['Синий канал', 'Зелёный канал', 'Красный канал'],
    'de': ['Blauer Kanal', 'Grüner Kanal', 'Roter Kanal'],
}
gui_step2 = {
    'en': 'Match several filters with data',
    'ru': 'Соотнесите фильтры с данными',
    'de': 'Mehrere Filter an Daten anpassen'
}
gui_browse = {
    'en': 'Browse',
    'ru': 'Обзор',
    'de': 'Durchsuchen'
}
gui_band = {
    'en': 'Band',
    'ru': 'Канал',
    'de': 'Band'
}
gui_filter = {
    'en': 'Filter or nm',
    'ru': 'Фильтр или нм',
    'de': 'Filter oder nm'
}
gui_evaluate = {
    'en': 'Evaluate',
    'ru': 'Выполнить',
    'de': 'Auswerten von'
}
gui_evaluate_note = {
    'en': 'Apply a function to the brightness values (x), written in Python syntax',
    'ru': 'Применить функцию к значениям яркости (x), используется синтаксис Python',
    'de': 'Wende Funktion auf Helligkeitswerte (x) an, in Python Syntax geschrieben'
}
#gui_brightness = {
#    'en': 'Brightness',
#    'ru': 'Яркость',
#    'de': 'Helligkeit'
#}
gui_desun = {
    'en': 'Divide by Solar spectrum',
    'ru': 'Делить на спектр Солнца',
    'de': 'Division durch Sonnenspektrum'
}
gui_desun_note = {
    'en': 'Removes the reflected color of the Sun, leaves the radiance factor (I/F)',
    'ru': 'Убирает отражённый цвет Солнца, оставляет отражательную способность (I/F)',
    'de': 'Entfernt die reflektierte Farbe der Sonne und belässt den Strahlungsfaktor (I/F)'
}
gui_photons = {
    'en': 'Photon counter',
    'ru': 'Счётчик фотонов',
    'de': 'Photonenzähler'
}
gui_photons_note = {
    'en': 'Converts the photon spectral density of the input data into the desired energy density',
    'ru': 'Переводит спектральную плотность фотонов входных данных в требуемую энергетическую',
    'de': 'Wandelt die Photonenspektraldichte der Eingangsdaten in die gewünschte Energiedichte um'
}
#gui_autoalign = {
#    'en': 'Align image bands (β)',
#    'ru': 'Совместить изображения (β)',
#    'de': 'Bildbänder ausrichten (β)'
#}
gui_factor = {
    'en': 'Brightness factor',
    'ru': 'Множитель яркости',
    'de': 'Helligkeitsfaktor'
}
gui_factor_note = {
    'en': 'Multiplies the values of the (reconstructed) spectral cube by a constant',
    'ru': 'Умножает значения (реконструированного) спектрального куба на константу',
    'de': 'Multipliziert die Werte des (rekonstruierten) Spektralwürfels mit einer Konstante'
}
gui_upscale = {
    'en': 'Upscale small images',
    'ru': 'Увеличить небольшие изображения',
    'de': 'Kleine Bilder vergrößern'
}
gui_upscale_note = {
    'en': 'Multiplies width and height by integer times to the preview size (no interpolation)',
    'ru': 'Умножает ширину и высоту в целое число раз до размера превью (без интерполяции)',
    'de': 'Multipliziert Breite und Höhe mit ganzzahligen Werten auf die Vorschaugröße (keine Interpolation)'
}
gui_chunks = {
    'en': 'Maximum chunk size (in megapixels)',
    'ru': 'Макс. размер фрагмента (в мегапикселях)',
    'de': 'Maximale Chunkgröße (in Megapixeln)'
}
gui_chunks_note = {
    'en': 'Prevents RAM overflow; value to optimize based on Task Manager readings',
    'ru': 'Предотвращает переполнение ОЗУ; число оптимизировать по показаниям Диспетчера задач',
    'de': 'Verhindert RAM-Überlauf; optimiert den Wert anhand der Messwerte des Task-Managers'
}
gui_preview = {
    'en': 'Show preview',
    'ru': 'Предпросмотр',
    'de': 'Vorschau anzeigen'
}
gui_process = {
    'en': 'Start processing',
    'ru': 'Обработать',
    'de': 'Bild generieren'
}


# Tab 3 - Blackbody & Redshifts
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
gui_mag = {
    'en': 'App. magnitude*',
    'ru': 'Вид. зв. величина*',
    'de': 'scheinb. Helligkeit*'
}
gui_mag_note = {
    'en': '* if the Solar disk in the sky is replaced by this blackbody sphere',
    'ru': '* если диск Солнца на небе заменить данной чёрнотельной сферой',
    'de': '* wenn die Sonne am Taghimmel durch einen Schwarzkörper ersetzt würde'
}

# Plots
spectral_plot = {
    'en': 'Energy spectral density or albedo, resp.',
    'ru': 'Спектральная плотность энергии или альбедо, соотв.',
    'de': 'Spektrale Energiedichte bzw. Albedo'
}
light_theme = {
    'en': 'Light theme',
    'ru': 'Светлая тема',
    'de': 'Heller Modus'
}
xaxis_text = {
    'en': 'Wavelength, nm',
    'ru': 'Длина волны, нм',
    'de': 'Wellenlänge, nm'
}
yaxis_text = {
    'en': 'Spectral density',
    'ru': 'Спектральная плотность',
    'de': 'Spektraldichte'
}


# Objects localization
names = {
    # Component of a generic Black Body spectrum name
    'BB with': {'ru': 'АЧТ с', 'de': 'SK mit'},
    # Component of a generic single-point spectrum name
    'nm': {'ru': 'нм', 'de': 'nm'},
    # Constellations
    'Andromedae': {'ru': 'Андромеды', 'de': 'Andromedae'},
    #'Antliae': {'ru': '', 'de': 'Antliae'},
    #'Apodis': {'ru': '', 'de': 'Apodis'},
    #'Aquarii': {'ru': '', 'de': 'Aquarii'},
    #'Aquilae': {'ru': '', 'de': 'Aquilae'},
    #'Arae': {'ru': '', 'de': 'Arae'},
    #'Arietis': {'ru': '', 'de': 'Arietis'},
    #'Aurigae': {'ru': '', 'de': 'Aurigae'},
    'Boötis': {'ru': 'Волопаса', 'de': 'Boötis'},
    #'Caeli': {'ru': '', 'de': 'Caeli'},
    #'Camelopardalis': {'ru': '', 'de': 'Camelopardalis'},
    'Cancri': {'ru': 'Рака', 'de': 'Cancri'},
    #'Canum Venaticorum': {'ru': '', 'de': 'Canum Venaticorum'},
    #'Canis Majoris': {'ru': '', 'de': 'Canis Majoris'},
    #'Canis Minoris': {'ru': '', 'de': 'Canis Minoris'},
    #'Capricorni': {'ru': '', 'de': 'Capricorni'},
    #'Carinae': {'ru': '', 'de': 'Carinae'},
    #'Cassiopeiae': {'ru': '', 'de': 'Cassiopeiae'},
    'Centauri': {'ru': 'Центавра', 'de': 'Centauri'},
    #'Cephei': {'ru': '', 'de': 'Cephei'},
    'Ceti': {'ru': 'Кита', 'de': 'Ceti'},
    #'Chamaeleontis': {'ru': '', 'de': 'Chamaeleontis'},
    #'Circini': {'ru': '', 'de': 'Circini'},
    'Columbae': {'ru': 'Голубя', 'de': 'Columbae'},
    'Comae Berenices': {'ru': 'Волос Вероники', 'de': 'Comae Berenices'},
    #'Coronae Australis': {'ru': '', 'de': 'Coronae Australis'},
    #'Coronae Borealis': {'ru': '', 'de': 'Coronae Borealis'},
    #'Corvi': {'ru': '', 'de': 'Corvi'},
    #'Crateris': {'ru': '', 'de': 'Crateris'},
    #'Crucis': {'ru': '', 'de': 'Crucis'},
    'Cygni': {'ru': 'Лебедя', 'de': 'Cygni'},
    #'Delphini': {'ru': '', 'de': 'Delphini'},
    'Doradus': {'ru': 'Золотой Рыбы', 'de': 'Doradus'},
    #'Draconis': {'ru': '', 'de': 'Draconis'},
    #'Equulei': {'ru': '', 'de': 'Equulei'},
    #'Eridani': {'ru': '', 'de': 'Eridani'},
    #'Fornacis': {'ru': '', 'de': 'Fornacis'},
    #'Geminorum': {'ru': '', 'de': 'Geminorum'},
    #'Gruis': {'ru': '', 'de': 'Gruis'},
    #'Herculis': {'ru': '', 'de': 'Herculis'},
    #'Horologii': {'ru': '', 'de': 'Horologii'},
    #'Hydrae': {'ru': '', 'de': 'Hydrae'},
    #'Hydri': {'ru': '', 'de': 'Hydri'},
    #'Indi': {'ru': '', 'de': 'Indi'},
    'Lacertae': {'ru': 'Ящерицы', 'de': 'Lacertae'},
    #'Leonis': {'ru': '', 'de': 'Leonis'},
    #'Leonis Minoris': {'ru': '', 'de': 'Leonis Minoris'},
    'Leporis': {'ru': 'Зайца', 'de': 'Leporis'},
    #'Librae': {'ru': '', 'de': 'Librae'},
    #'Lupi': {'ru': '', 'de': 'Lupi'},
    #'Lyncis': {'ru': '', 'de': 'Lyncis'},
    #'Lyrae': {'ru': '', 'de': 'Lyrae'},
    #'Mensae': {'ru': '', 'de': 'Mensae'},
    #'Microscopii': {'ru': '', 'de': 'Microscopii'},
    #'Monocerotis': {'ru': '', 'de': 'Monocerotis'},
    #'Muscae': {'ru': '', 'de': 'Muscae'},
    #'Normae': {'ru': '', 'de': 'Normae'},
    #'Octantis': {'ru': '', 'de': 'Octantis'},
    #'Ophiuchi': {'ru': '', 'de': 'Ophiuchi'},
    'Orionis': {'ru': 'Ориона', 'de': 'Orionis'},
    #'Pavonis': {'ru': '', 'de': 'Pavonis'},
    'Pegasi': {'ru': 'Пегаса', 'de': 'Pegasi'},
    #'Persei': {'ru': '', 'de': 'Persei'},
    #'Phoenicis': {'ru': '', 'de': 'Phoenicis'},
    #'Pictoris': {'ru': '', 'de': 'Pictoris'},
    #'Piscium': {'ru': '', 'de': 'Piscium'},
    #'Piscis Austrini': {'ru': '', 'de': 'Piscis Austrini'},
    #'Puppis': {'ru': '', 'de': 'Puppis'},
    #'Pyxidis': {'ru': '', 'de': 'Pyxidis'},
    #'Reticuli': {'ru': '', 'de': 'Reticuli'},
    #'Sagittae': {'ru': '', 'de': 'Sagittae'},
    #'Sagittarii': {'ru': '', 'de': 'Sagittarii'},
    'Scorpii': {'ru': 'Скорпиона', 'de': 'Scorpii'},
    #'Sculptoris': {'ru': '', 'de': 'Sculptoris'},
    #'Scuti': {'ru': '', 'de': 'Scuti'},
    #'Serpentis': {'ru': '', 'de': 'Serpentis'},
    #'Sextantis': {'ru': '', 'de': 'Sextantis'},
    #'Tauri': {'ru': '', 'de': 'Tauri'},
    #'Telescopii': {'ru': '', 'de': 'Telescopii'},
    #'Trianguli': {'ru': '', 'de': 'Trianguli'},
    #'Trianguli Australis': {'ru': '', 'de': 'Trianguli Australis'},
    #'Tucanae': {'ru': '', 'de': 'Tucanae'},
    #'Ursae Majoris': {'ru': '', 'de': 'Ursae Majoris'},
    #'Ursae Minoris': {'ru': '', 'de': 'Ursae Minoris'},
    #'Velorum': {'ru': '', 'de': 'Velorum'},
    'Virginis': {'ru': 'Девы', 'de': 'Virginis'},
    #'Volantis': {'ru': '', 'de': 'Volantis'},
    #'Vulpeculae': {'ru': '', 'de': 'Vulpeculae'},
    # Stars
    'Gliese': {'ru': 'Глизе', 'de': 'Gliese'},
    'Mimosa': {'ru': 'Мимоза', 'de': 'Mimosa'},
    'Mirzam': {'ru': 'Мирцам', 'de': 'Murzim'},
    'Adhara': {'ru': 'Адара', 'de': 'Adhara'},
    'Bellatrix': {'ru': 'Беллатрикс', 'de': 'Bellatrix'},
    'Rigel': {'ru': 'Ригель', 'de': 'Rigel'},
    'Vega': {'ru': 'Вега', 'de': 'Wega'},
    'Alsephina': {'ru': 'Альсефина', 'de': 'Alsephina'},
    'Miaplacidus': {'ru': 'Миаплацидус', 'de': 'Miaplacidus'},
    'Canopus': {'ru': 'Канопус', 'de': 'Canopus'},
    'Alchiba': {'ru': 'Альхиба', 'de': 'Alchiba'},
    'Procyon': {'ru': 'Процион', 'de': 'Prokyon'},
    'Wezen': {'ru': 'Везен', 'de': 'Wezen'},
    'Ankaa': {'ru': 'Анкаа', 'de': 'Ankaa'},
    'Alsafi': {'ru': 'Альсафи', 'de': 'Alsafi'},
    'Ran': {'ru': 'Ран', 'de': 'Ran'},
    'Alphard': {'ru': 'Альфард', 'de': 'Alphard'},
    'Avior': {'ru': 'Авиор', 'de': 'Avior'},
    'Suhail': {'ru': 'Сухайль', 'de': 'Suhail'},
    'Betelgeuse': {'ru': 'Бетельгейзе', 'de': 'Beteigeuze'},
    'Gacrux': {'ru': 'Гакрукс', 'de': 'Gacrux'},
    'Proxima Centauri': {'ru': 'Проксима Центавра', 'de': 'Proxima Centauri'},
    'Vela pulsar': {'ru': 'Пульсар в Парусах', 'de': 'Vela-Pulsar'},
    # Stars from the CALSPEC add-on
    'Alkaid': {'ru': 'Алькаид', 'de': 'Alkaid'},
    'Yildun': {'ru': 'Йильдун', 'de': 'Yildun'},
    'Sirius': {'ru': 'Сириус', 'de': 'Sirius'},
    # Solar system
    'Sun': {'ru': 'Солнце', 'de': 'Sonne'},
    'Mercury': {'ru': 'Меркурий', 'de': 'Merkur'},
    'Venus': {'ru': 'Венера', 'de': 'Venus'},
    'Earth': {'ru': 'Земля', 'de': 'Erde'},
    'Caribbean Sea': {'ru': 'Карибское море', 'de': 'Karibisches Meer'},
    'Moon': {'ru': 'Луна', 'de': 'Mond'},
    'Mars': {'ru': 'Марс', 'de': 'Mars'},
    'Phobos': {'ru': 'Фобос', 'de': 'Phobos'},
    'Deimos': {'ru': 'Деймос', 'de': 'Deimos'},
    # Jovian system
    'Jupiter': {'ru': 'Юпитер', 'de': 'Jupiter'},
    'Amalthea': {'ru': 'Амальтея', 'de': 'Amalthea'},
    'Thebe': {'ru': 'Фива', 'de': 'Thebe'},
    'Io': {'ru': 'Ио', 'de': 'Io'},
    'Europa': {'ru': 'Европа', 'de': 'Europa'},
    'Ganymede': {'ru': 'Ганимед', 'de': 'Ganymed'},
    'Callisto': {'ru': 'Каллисто', 'de': 'Kallisto'},
    # Jovian irregulars
    'Himalia': {'ru': 'Гималия', 'de': 'Himalia'},
    'Elara': {'ru': 'Элара', 'de': 'Elara'},
    'Pasiphae': {'ru': 'Пасифе', 'de': 'Pasiphae'},
    'Sinope': {'ru': 'Синопе', 'de': 'Sinope'},
    'Lysithea': {'ru': 'Лиситея', 'de': 'Lysithea'},
    'Carme': {'ru': 'Карме', 'de': 'Carme'},
    'Ananke': {'ru': 'Ананке', 'de': 'Ananke'},
    'Leda': {'ru': 'Леда', 'de': 'Leda'},
    'Callirrhoe': {'ru': 'Каллирое', 'de': 'Callirrhoe'},
    'Themisto': {'ru': 'Фемисто', 'de': 'Themisto'},
    'Megaclite': {'ru': 'Мегаклите', 'de': 'Megaclite'},
    'Taygete': {'ru': 'Тайгете', 'de': 'Taygete'},
    'Chaldene': {'ru': 'Халдене', 'de': 'Chaldene'},
    'Harpalyke': {'ru': 'Гарпалике', 'de': 'Harpalyke'},
    'Kalyke': {'ru': 'Калике', 'de': 'Kalyke'},
    'Iocaste': {'ru': 'Иокасте', 'de': 'Iocaste'},
    'Erinome': {'ru': 'Эриноме', 'de': 'Erinome'},
    'Isonoe': {'ru': 'Исоное', 'de': 'Isonoe'},
    'Praxidike': {'ru': 'Праксидике', 'de': 'Praxidike'},
    'Autonoe': {'ru': 'Автоное', 'de': 'Autonoe'},
    'Thyone': {'ru': 'Тионе', 'de': 'Thyone'},
    'Hermippe': {'ru': 'Гермиппе', 'de': 'Hermippe'},
    'Eukelade': {'ru': 'Эвкеладе', 'de': 'Eukelade'},
    'Cyllene': {'ru': 'Киллене', 'de': 'Cyllene'},
    # Saturnian system
    'Saturn': {'ru': 'Сатурн', 'de': 'Saturn'},
    'Rings of Saturn': {'ru': 'Кольца Сатурна', 'de': 'Saturnringe'},
    'Pan': {'ru': 'Пан', 'de': 'Pan'},
    'Daphnis': {'ru': 'Дафнис', 'de': 'Daphnis'},
    'Atlas': {'ru': 'Атлас', 'de': 'Atlas'},
    'Prometheus': {'ru': 'Прометей', 'de': 'Prometheus'},
    'Pandora': {'ru': 'Пандора', 'de': 'Pandora'},
    'Janus': {'ru': 'Янус', 'de': 'Janus'},
    'Epimetheus': {'ru': 'Эпиметей', 'de': 'Epimetheus'},
    'Aegaeon': {'ru': 'Эгеон', 'de': 'Aegaeon'},
    'Mimas': {'ru': 'Мимас', 'de': 'Mimas'},
    'Methone': {'ru': 'Мефона', 'de': 'Methone'},
    'Pallene': {'ru': 'Паллена', 'de': 'Pallene'},
    'Enceladus': {'ru': 'Энцелад', 'de': 'Enceladus'},
    'Tethys': {'ru': 'Тефия', 'de': 'Tethys'},
    'Telesto': {'ru': 'Телесто', 'de': 'Telesto'},
    'Calypso': {'ru': 'Калипсо', 'de': 'Calypso'},
    'Dione': {'ru': 'Диона', 'de': 'Dione'},
    'Helene': {'ru': 'Елена', 'de': 'Helene'},
    'Polydeuces': {'ru': 'Полидевк', 'de': 'Polydeuces'},
    'Rhea': {'ru': 'Рея', 'de': 'Rhea'},
    'Titan': {'ru': 'Титан', 'de': 'Titan'},
    'Hyperion': {'ru': 'Гиперион', 'de': 'Hyperion'},
    'Iapetus': {'ru': 'Япет', 'de': 'Iapetus'},
    # Saturnian irregulars
    'Phoebe': {'ru': 'Феба', 'de': 'Phoebe'},
    'Ymir': {'ru': 'Имир', 'de': 'Ymir'},
    'Paaliaq': {'ru': 'Палиак', 'de': 'Paaliaq'},
    'Tarvos': {'ru': 'Тарвос', 'de': 'Tarvos'},
    'Ijiraq': {'ru': 'Иджирак', 'de': 'Ijiraq'},
    'Suttungr': {'ru': 'Суттунг', 'de': 'Suttungr'},
    'Kiviuq': {'ru': 'Кивиок', 'de': 'Kiviuq'},
    'Mundilfari': {'ru': 'Мундильфари', 'de': 'Mundilfari'},
    'Albiorix': {'ru': 'Альбиорикс', 'de': 'Albiorix'},
    'Skathi': {'ru': 'Скади', 'de': 'Skathi'},
    'Erriapus': {'ru': 'Эррипо', 'de': 'Erriapus'},
    'Siarnaq': {'ru': 'Сиарнак', 'de': 'Siarnaq'},
    'Thrymr': {'ru': 'Трюм', 'de': 'Thrymr'},
    'Narvi': {'ru': 'Нарви', 'de': 'Narvi'},
    'Aegir': {'ru': 'Эгир', 'de': 'Aegir'},
    'Bebhionn': {'ru': 'Бефинд', 'de': 'Bebhionn'},
    'Bergelmir': {'ru': 'Бергельмир', 'de': 'Bergelmir'},
    'Bestla': {'ru': 'Бестла', 'de': 'Bestla'},
    'Fornjot': {'ru': 'Форньот', 'de': 'Fornjot'},
    'Hyrrokkin': {'ru': 'Гирроккин', 'de': 'Hyrrokkin'},
    'Kari': {'ru': 'Кари', 'de': 'Kari'},
    'Tarqeq': {'ru': 'Таркек', 'de': 'Tarqeq'},
    # Uranian system
    'Uranus': {'ru': 'Уран', 'de': 'Uranus'},
    'Rings of Uranus': {'ru': 'Кольца Урана', 'de': 'Uranusringe'},
    'Portia': {'ru': 'Порция', 'de': 'Portia'},
    'Portia group': {'ru': 'Группа Порции', 'de': 'Portia-Gruppe'},
    'Puck': {'ru': 'Пак', 'de': 'Puck'},
    'Miranda': {'ru': 'Миранда', 'de': 'Miranda'},
    'Ariel': {'ru': 'Ариэль', 'de': 'Ariel'},
    'Umbriel': {'ru': 'Умбриэль', 'de': 'Umbriel'},
    'Titania': {'ru': 'Титания', 'de': 'Titania'},
    'Oberon': {'ru': 'Оберон', 'de': 'Oberon'},
    # Uranian irregulars
    'Caliban': {'ru': 'Калибан', 'de': 'Caliban'},
    'Sycorax': {'ru': 'Сикоракса', 'de': 'Sycorax'},
    'Prospero': {'ru': 'Просперо', 'de': 'Prospero'},
    'Setebos': {'ru': 'Сетебос', 'de': 'Setebos'},
    'Stephano': {'ru': 'Стефано', 'de': 'Stephano'},
    'Trinculo': {'ru': 'Тринкуло', 'de': 'Trinculo'},
    # Neptunian system
    'Neptune': {'ru': 'Нептун', 'de': 'Neptun'},
    'Larissa': {'ru': 'Ларисса', 'de': 'Larissa'},
    'Proteus': {'ru': 'Протей', 'de': 'Proteus'},
    'Nereid': {'ru': 'Нереида', 'de': 'Nereid'},
    'Triton': {'ru': 'Тритон', 'de': 'Triton'},
    # Neptunian irregulars
    'Halimede': {'ru': 'Галимеда', 'de': 'Halimede'},
    'Neso': {'ru': 'Несо', 'de': 'Neso'},
    # Minor bodies
    'Ceres': {'ru': 'Церера', 'de': 'Ceres'},
    'Pallas': {'ru': 'Паллада', 'de': 'Pallas'},
    'Juno': {'ru': 'Юнона', 'de': 'Juno'},
    'Vesta': {'ru': 'Веста', 'de': 'Vesta'},
    'Iris': {'ru': 'Ирида', 'de': 'Iris'},
    'Metis': {'ru': 'Метида', 'de': 'Metis'},
    'Hygiea': {'ru': 'Гигея', 'de': 'Hygiea'},
    'Egeria': {'ru': 'Эгерия', 'de': 'Egeria'},
    'Eunomia': {'ru': 'Эвномия', 'de': 'Eunomia'},
    'Psyche': {'ru': 'Психея', 'de': 'Psyche'},
    'Fortuna': {'ru': 'Фортуна', 'de': 'Fortuna'},
    'Lutetia': {'ru': 'Лютеция', 'de': 'Lutetia'},
    'Kalliope': {'ru': 'Каллиопа', 'de': 'Kalliope'},
    'Themis': {'ru': 'Фемида', 'de': 'Themis'},
    'Amphitrite': {'ru': 'Амфитрита', 'de': 'Amphitrite'},
    'Euphrosyne': {'ru': 'Евфросина', 'de': 'Euphrosyne'},
    'Daphne': {'ru': 'Дафна', 'de': 'Daphne'},
    'Eugenia': {'ru': 'Евгения', 'de': 'Eugenia'},
    'Doris': {'ru': 'Дорида', 'de': 'Doris'},
    # 50
    'Europa': {'ru': 'Европа', 'de': 'Europa'},
    'Cybele': {'ru': 'Кибела', 'de': 'Cybele'},
    'Sylvia': {'ru': 'Сильвия', 'de': 'Sylvia'},
    'Thisbe': {'ru': 'Фисба', 'de': 'Thisbe'},
    'Antiope': {'ru': 'Антиопа', 'de': 'Antiope'},
    'Minerva': {'ru': 'Минерва', 'de': 'Minerva'},
    'Aurora': {'ru': 'Аврора', 'de': 'Aurora'},
    # 100
    'Camilla': {'ru': 'Камилла', 'de': 'Camilla'},
    'Hermione': {'ru': 'Гермиона', 'de': 'Hermione'},
    'Elektra': {'ru': 'Электра', 'de': 'Elektra'},
    'Kleopatra': {'ru': 'Клеопатра', 'de': 'Kleopatra'},
    'Ida': {'ru': 'Ида', 'de': 'Ida'},
    'Dactyl': {'ru': 'Дактиль', 'de': 'Dactyl'},
    'Mathilde': {'ru': 'Матильда', 'de': 'Mathilde'},
    'Justitia': {'ru': 'Юстиция', 'de': 'Justitia'},
    'Eros': {'ru': 'Эрос', 'de': 'Eros'},
    # 500
    'Davida': {'ru': 'Давида', 'de': 'Davida'},
    'Achilles': {'ru': 'Ахиллес', 'de': 'Achilles'},
    'Scheila': {'ru': 'Шейла', 'de': 'Scheila'},
    'Patroclus-Menoetius': {'ru': 'Патрокл-Менетий', 'de': 'Patroclus-Menoetius'},
    'Chimaera': {'ru': 'Химера', 'de': 'Chimaera'},
    'Hektor': {'ru': 'Гектор', 'de': 'Hektor'},
    'Nestor': {'ru': 'Нестор', 'de': 'Nestor'},
    'Interamnia': {'ru': 'Интерамния', 'de': 'Interamnia'},
    'Ani': {'ru': 'Ани', 'de': 'Ani'},
    'Priamus': {'ru': 'Приам', 'de': 'Priamus'},
    'Agamemnon': {'ru': 'Агамемнон', 'de': 'Agamemnon'},
    'Hidalgo': {'ru': 'Идальго', 'de': 'Hidalgo'},
    'Gaspra': {'ru': 'Гаспра', 'de': 'Gaspra'},
    # 1000
    'Ganymed': {'ru': 'Ганимед', 'de': 'Ganymed'},
    'Odysseus': {'ru': 'Одиссей', 'de': 'Odysseus'},
    'Äneas': {'ru': 'Эней', 'de': 'Äneas'},
    'Anchises': {'ru': 'Анхис', 'de': 'Anchises'},
    'Troilus': {'ru': 'Троил', 'de': 'Troilus'},
    'Celestia': {'ru': 'Селестия', 'de': 'Celestia'},
    'Ajax': {'ru': 'Аякс', 'de': 'Ajax'},
    'Diomedes': {'ru': 'Диомед', 'de': 'Diomedes'},
    'Antilochus': {'ru': 'Антилох', 'de': 'Antilochus'},
    'Geographos': {'ru': 'Географ', 'de': 'Geographos'},
    'Menelaus': {'ru': 'Менелай', 'de': 'Menelaus'},
    'Telamon': {'ru': 'Теламон', 'de': 'Telamon'},
    'Deiphobus': {'ru': 'Деифоб', 'de': 'Deiphobus'},
    'Glaukos': {'ru': 'Главк', 'de': 'Glaukos'},
    'Astyanax': {'ru': 'Астианакт', 'de': 'Astyanax'},
    'Helenos': {'ru': 'Гелен', 'de': 'Helenos'},
    'Agenor': {'ru': 'Агенор', 'de': 'Agenor'},
    'Chiron': {'ru': 'Хирон', 'de': 'Chiron'},
    'Bacchus': {'ru': 'Бахус', 'de': 'Bacchus'},
    'Sarpedon': {'ru': 'Сарпедон', 'de': 'Sarpedon'},
    'Phereclos': {'ru': 'Ферекл', 'de': 'Phereclos'},
    'Masursky': {'ru': 'Мазурский', 'de': 'Masursky'},
    'Šteins': {'ru': 'Штейнс', 'de': 'Šteins'},
    'Phaethon': {'ru': 'Фаэтон', 'de': 'Phaethon'},
    'Paris': {'ru': 'Парис', 'de': 'Paris'},
    'Mentor': {'ru': 'Ментор', 'de': 'Mentor'},
    'Eurybates': {'ru': 'Эврибат', 'de': 'Eurybates'},
    'Wilson–Harrington': {'ru': 'Вильсон — Харрингтон', 'de': 'Wilson–Harrington'},
    'Thestor': {'ru': 'Тестор', 'de': 'Thestor'},
    'Toutatis': {'ru': 'Таутатис', 'de': 'Toutatis'},
    'Ennomos': {'ru': 'Энном', 'de': 'Ennomos'},
    'Sergestus': {'ru': 'Сергест', 'de': 'Sergestus'},
    # 5000
    'Ilioneus': {'ru': 'Илионей', 'de': 'Ilioneus'},
    'Pholus': {'ru': 'Фол', 'de': 'Pholus'},
    'Cloanthus': {'ru': 'Клоант', 'de': 'Cloanthus'},
    'Annefrank': {'ru': 'Аннафранк', 'de': 'Annefrank'},
    'Gault': {'ru': 'Голт', 'de': 'Gault'},
    'Golevka': {'ru': 'Голевка', 'de': 'Golevka'},
    'Leitus': {'ru': 'Лейтус', 'de': 'Leitus'},
    'Tithonus': {'ru': 'Титон', 'de': 'Tithonus'},
    'Nessus': {'ru': 'Несс', 'de': 'Nessus'},
    'Hypsenor': {'ru': 'Гипсенор', 'de': 'Hypsenor'},
    'Elst–Pizarro': {'ru': 'Эльст — Писарро', 'de': 'Elst–Pizarro'},
    'Asbolus': {'ru': 'Асбол', 'de': 'Asbolus'},
    'Othryoneus': {'ru': 'Офрионей', 'de': 'Othryoneus'},
    'Erichthonios': {'ru': 'Эрихтоний', 'de': 'Erichthonios'},
    'Eurymachos': {'ru': 'Эвримах', 'de': 'Eurymachos'},
    'Braille': {'ru': 'Брайль', 'de': 'Braille'},
    # 10 000
    'Chariklo': {'ru': 'Харикло', 'de': 'Chariklo'},
    'Westerwald': {'ru': 'Вестервальд', 'de': 'Westerwald'},
    'Hylonome': {'ru': 'Хилонома', 'de': 'Hylonome'},
    'Leucus': {'ru': 'Левк', 'de': 'Leucus'},
    'Ascanios': {'ru': 'Асканий', 'de': 'Ascanios'},
    'Rockox': {'ru': 'Рококс', 'de': 'Rockox'},
    'Antiphos': {'ru': 'Антифос', 'de': 'Antiphos'},
    'Polymele': {'ru': 'Полимела', 'de': 'Polymele'},
    'Albion': {'ru': 'Алебион', 'de': 'Albion'},
    'Arawn': {'ru': 'Араун', 'de': 'Arawn'},
    'Thymbraeus': {'ru': 'Фимбрей', 'de': 'Thymbraeus'},
    'Zarex': {'ru': 'Зарекс', 'de': 'Zarex'},
    'Dardanos': {'ru': 'Дардан', 'de': 'Dardanos'},
    'Demoleon': {'ru': 'Демолеон', 'de': 'Demoleon'},
    'Chaos': {'ru': 'Хаос', 'de': 'Chaos'},
    'Varuna': {'ru': 'Варуна', 'de': 'Varuna'},
    'Dioretsa': {'ru': 'Диоретса', 'de': 'Dioretsa'},
    'Orus': {'ru': 'Орус', 'de': 'Orus'},
    'Epicles': {'ru': 'Эпикл', 'de': 'Epicles'},
    'Dorippe': {'ru': 'Дориппе', 'de': 'Dorippe'},
    'Thasos': {'ru': 'Тасос', 'de': 'Thasos'},
    'Belova': {'ru': 'Белова', 'de': 'Belova'},
    'Itokawa': {'ru': 'Итокава', 'de': 'Itokawa'},
    'Binns': {'ru': 'Биннс', 'de': 'Binns'},
    'Ixion': {'ru': 'Иксион', 'de': 'Ixion'},
    'Hippokoon': {'ru': 'Гиппокоон', 'de': 'Hippokoon'},
    'Elatus': {'ru': 'Элат', 'de': 'Elatus'},
    'Thereus': {'ru': 'Терей', 'de': 'Thereus'},
    'Rhadamanthus': {'ru': 'Радамант', 'de': 'Rhadamanthus'},
    'Huya': {'ru': 'Гуйя', 'de': 'Huya'},
    'Kipkeino': {'ru': 'Кипкейно', 'de': 'Kipkeino'},
    'Typhon': {'ru': 'Тифон', 'de': 'Typhon'},
    'Echidna': {'ru': 'Ехидна', 'de': 'Echidna'},
    'Lempo': {'ru': 'Лемпо', 'de': 'Lempo'},
    'Pelion': {'ru': 'Пелион', 'de': 'Pelion'},
    # 50 000
    'Quaoar': {'ru': 'Квавар', 'de': 'Quaoar'},
    'Donaldjohanson': {'ru': 'Дональдджохансон', 'de': 'Donaldjohanson'},
    'Okyrhoe': {'ru': 'Окироя', 'de': 'Okyrhoe'},
    'Cyllarus': {'ru': 'Киллар', 'de': 'Cyllarus'},
    'Deucallion': {'ru': 'Девкалион', 'de': 'Deucallion'},
    'Bienor': {'ru': 'Биенор', 'de': 'Bienor'},
    'Amycus': {'ru': 'Амик', 'de': 'Amycus'},
    'Logos': {'ru': 'Логос', 'de': 'Logos'},
    'Echeclus': {'ru': 'Эхекл', 'de': 'Echeclus'},
    'Ceto': {'ru': 'Кето', 'de': 'Ceto'},
    'Didymos': {'ru': 'Дидим', 'de': 'Didymos'},
    'Moshup': {'ru': 'Мошуп', 'de': 'Moshup'},
    'Borasisi': {'ru': 'Борасизи', 'de': 'Borasisi'},
    'Sila-Nunam': {'ru': 'Сила-Нунам', 'de': 'Sila-Nunam'},
    'Crantor': {'ru': 'Крантор', 'de': 'Crantor'},
    'Teharonhiawako': {'ru': 'Таронхайавагон', 'de': 'Teharonhiawako'},
    'Sawiskera': {'ru': 'Тавискарон', 'de': 'Sawiskera'},
    'Sedna': {'ru': 'Седна', 'de': 'Sedna'},
    'Orcus': {'ru': 'Орк', 'de': 'Orcus'},
    'Torifune': {'ru': 'Торифуне', 'de': 'Torifune'},
    'Apophis': {'ru': 'Апофис', 'de': 'Apophis'},
    'Vanth': {'ru': 'Вант', 'de': 'Vanth'},
    # 100 000
    'Bennu': {'ru': 'Бенну', 'de': 'Bennu'},
    'Salacia': {'ru': 'Салация', 'de': 'Salacia'},
    'Actaea': {'ru': 'Актея', 'de': 'Actaea'},
    'Aphidas': {'ru': 'Афида', 'de': 'Aphidas'},
    'Pluto': {'ru': 'Плутон', 'de': 'Pluto'},
    'Charon': {'ru': 'Харон', 'de': 'Charon'},
    'Nix': {'ru': 'Никта', 'de': 'Nix'},
    'Hydra': {'ru': 'Гидра', 'de': 'Hydra'},
    'Haumea': {'ru': 'Хаумеа', 'de': 'Haumea'},
    'Hi‘iaka': {'ru': 'Хииака', 'de': 'Hi‘iaka'},
    'Namaka': {'ru': 'Намака', 'de': 'Namaka'},
    'Eris': {'ru': 'Эрида', 'de': 'Eris'},
    'Makemake': {'ru': 'Макемаке', 'de': 'Makemake'},
    'Dinkinesh': {'ru': 'Динкинеш', 'de': 'Dinkinesh'},
    'Ryugu': {'ru': 'Рюгу', 'de': 'Ryugu'},
    'Cardea': {'ru': 'Кардея', 'de': 'Cardea'},
    'Varda': {'ru': 'Варда', 'de': 'Varda'},
    'Ilmarë': {'ru': 'Ильмарэ', 'de': 'Ilmarë'},
    'Gonggong': {'ru': 'Гунгун', 'de': 'Gonggong'},
    'Xiangliu': {'ru': 'Сянлю', 'de': 'Xiangliu'},
    'Gǃkúnǁʼhòmdímà': {'ru': 'Гкъкунлъ’хомдима', 'de': 'Gǃkúnǁʼhòmdímà'},
    'Gǃòʼé ǃHú': {'ru': 'Гкъо’э Къху', 'de': 'Gǃòʼé ǃHú'},
    'Mors-Somnus': {'ru': 'Мор-Сомн', 'de': 'Mors-Somnus'},
    'Rhiphonos': {'ru': 'Рифон', 'de': 'Rhiphonos'}, # no official ru translation
    'Otrera': {'ru': 'Отрера', 'de': 'Otrera'},
    'Clete': {'ru': 'Клета', 'de': 'Clete'},
    'Kamo‘oalewa': {'ru': 'Камоалева', 'de': 'Kamo‘oalewa'},
    'ǂKá̦gára': {'ru': 'Кагара', 'de': 'ǂKá̦gára'}, # no official ru translation
    'Alicanto': {'ru': 'Аликанто', 'de': 'Alicanto'},
    # 500 000
    'Arrokoth': {'ru': 'Аррокот', 'de': 'Arrokoth'},
    'Zoozve': {'ru': 'Зоозве', 'de': 'Zoozve'},
    'Dziewanna': {'ru': 'Девана', 'de': 'Dziewanna'},
    'Halley': {'ru': 'Галлея', 'de': 'Halley'},
    'Encke': {'ru': 'Энке', 'de': 'Encke'},
    'dArrest': {'ru': 'д’Арре', 'de': 'dArrest'},
    'Pons–Winnecke': {'ru': 'Понса — Виннеке', 'de': 'Pons–Winnecke'},
    'Tuttle': {'ru': 'Туттля', 'de': 'Tuttle'},
    'Tempel': {'ru': 'Темпеля', 'de': 'Tempel'},
    'Wolf': {'ru': 'Вольфа', 'de': 'Wolf'},
    'Giacobini–Zinner': {'ru': 'Джакобини — Циннера', 'de': 'Giacobini–Zinner'},
    'Kopff': {'ru': 'Копффа', 'de': 'Kopff'},
    'Forbes': {'ru': 'Форбса', 'de': 'Forbes'},
    'Oterma': {'ru': 'Отерма', 'de': 'Oterma'},
    'Honda–Mrkos–Pajdušáková': {'ru': 'Хонда — Мркоса — Пайдушаковой', 'de': 'Honda–Mrkos–Pajdušáková'},
    'Ashbrook–Jackson': {'ru': 'Ашбрука — Джексона', 'de': 'Ashbrook–Jackson'},
    'Arend–Rigaux': {'ru': 'Арена — Риго', 'de': 'Arend–Rigaux'},
    'Arend': {'ru': 'Арена', 'de': 'Arend'},
    'Tempel–Tuttle': {'ru': 'Темпеля — Туттля', 'de': 'Tempel–Tuttle'},
    'Kearns–Kwee': {'ru': 'Кирнса — Гуи', 'de': 'Kearns–Kwee'},
    'Wild': {'ru': 'Вильда', 'de': 'Wild'},
    'Churyumov–Gerasimenko': {'ru': 'Чурюмова — Герасименко', 'de': 'Tschurjumow-Gerassimenko'},
    'Sanguin': {'ru': 'Сангина', 'de': 'Sanguin'},
    'Hartley': {'ru': 'Хартли', 'de': 'Hartley'},
    'Schuster': {'ru': 'Шустера', 'de': 'Schuster'},
    'Wiseman–Skiff': {'ru': 'Уайзмана — Скиффа', 'de': 'Wiseman–Skiff'},
    'Kowal–Mrkos': {'ru': 'Коваля — Мркоса', 'de': 'Kowal–Mrkos'},
    'Siding Spring': {'ru': 'Сайдинг Спринг', 'de': 'Siding Spring'},
    'Read': {'ru': 'Рида', 'de': 'Read'},
    'Gibbs': {'ru': 'Гиббса', 'de': 'Gibbs'},
    'Hale–Bopp': {'ru': 'Хейла — Боппа', 'de': 'Hale–Bopp'},
    'Skiff': {'ru': 'Скиффа', 'de': 'Skiff'},
    'Loneos': {'ru': '', 'de': 'Loneos'},
    'Gleason': {'ru': 'Глисона', 'de': 'Gleason'},
    'Boattini': {'ru': 'Боаттини', 'de': 'Boattini'},
    'McNaught': {'ru': 'Макнота', 'de': 'McNaught'},
    'Catalina': {'ru': 'Каталина', 'de': 'Catalina'},
    'Hill': {'ru': 'Хилла', 'de': 'Hill'},
    'Kowalski': {'ru': 'Ковальски', 'de': 'Kowalski'},
    'Schwartz': {'ru': 'Шварца', 'de': 'Schwartz'},
    'Borisov': {'ru': 'Борисова', 'de': 'Borisov'},
    'Bernardinelli-Berstein': {'ru': 'Бернардинелли — Бернштейна', 'de': 'Bernardinelli-Berstein'},
    'ʻOumuamua': {'ru': 'Оумуамуа', 'de': 'ʻOumuamua'},
    # Classes
    'Class': {'ru': 'Класс', 'de': 'Klasse'},
    'Spectral type': {'ru': 'Спектральный класс', 'de': 'Spektraltyp'},
    'Jovian irregulars': {'ru': 'Нерегулярные спутники Юпитера', 'de': 'irreguläre Jupitermonde'},
    'Saturnian irregulars': {'ru': 'Нерегулярные спутники Сатурна', 'de': 'irreguläre Saturnmonde'},
    'Uranian irregulars': {'ru': 'Нерегулярные спутники Урана', 'de': 'irreguläre Uranusmonde'},
    'Neptunian irregulars': {'ru': 'Нерегулярные спутники Нептуна', 'de': 'irreguläre Neptunmonde'},
    'Comets': {'ru': 'Кометы', 'de': 'Kometen'},
    'Jupiter trojans': {'ru': 'Троянцы Юпитера', 'de': 'Jupiter-Trojaner'},
    'Centaurs': {'ru': 'Кентавры', 'de': 'Zentauren'},
    'Plutinos': {'ru': 'Плутино', 'de': 'Plutinos'},
    'Other resonances': {'ru': 'Другие резонансы', 'de': 'Andere Resonanzen'},
    'Cubewano': {'ru': 'Кьюбивано', 'de': 'Cubewano'},
    'SDO': {'ru': 'Рассеянный диск', 'de': 'SDO'},
    'Detached objects': {'ru': 'Обособл. ТНО', 'de': 'Detached Objects'},
    # Others
    'Equal-energy spectrum': {'ru': 'Плоский спектр', 'de': 'Homogenes Energiespektrum'}
}

# Sort in key length descending order to prevent nested word errors
names = dict(sorted(names.items(), key=lambda x: len(x[0]), reverse=True))


# Notes localization
notes = {
    'Synthetic spectrum': {'ru': 'Синтетический спектр', 'de': 'Synthetisches Sprektrum'},
    'Surface': {'ru': 'Поверхность', 'de': 'Oberfläche'},
    'Bright areas': {'ru': 'Яркие участки', 'de': 'Helle Regionen'},
    'Dark areas': {'ru': 'Тёмные участки', 'de': 'Dunkle Regionen'},
    'Dark boulder terrain': {'ru': 'Тёмные валуны', 'de': 'Terrain dunkler Felsbrocken'},
    'Near side': {'ru': 'Видимая сторона', 'de': 'Erdzugewandte Seite'},
    'Far side': {'ru': 'Обратная сторона', 'de': 'Erdabgewandte Seite'},
    'Leading side': {'ru': 'Ведущая сторона', 'de': 'Führende Seite'},
    'Trailing side': {'ru': 'Ведомая сторона', 'de': 'Folgende Seite'},
    'Leading hemisphere': {'ru': 'Ведущее полушарие', 'de': 'Führende Hemisphäre'},
    'Trailing hemisphere': {'ru': 'Ведомое полушарие', 'de': 'Folgende Hemisphäre'},
    'Surface, phase angle': {'ru': 'Поверхность, фазовый угол', 'de': 'Oberfläche, Phasenwinkel'},
    'West': {'ru': 'к западу', 'de': 'West'},
    'East': {'ru': 'к востоку', 'de': 'Ost'},
    'Long-period': {'ru': 'Долгопериодические', 'de': 'Langperiodisch'},
    'Short-period': {'ru': 'Короткопериодические', 'de': 'Kurzperiodisch'},
    'Hot, inner objects': {'ru': 'Тёплые, внутренние объекты', 'de': 'Heiße, innere Objekte'},
    'Cold, outer objects': {'ru': 'Холодные, внешние объекты', 'de': 'Kalte, äußere Objekte'},
    'Weighted mean': {'ru': 'Взвешенное среднее', 'de': 'Gewichteter Durchschnitt'},
    'Coma particles dominated': {'ru': 'Преобладают частицы комы', 'de': 'Koma-Teilchen dominieren'},
    'Upper limit albedo': {'ru': 'Верхний предел альбедо', 'de': 'Obergrenze Albedo'},
    'Active': {'ru': 'Активные', 'de': 'Aktive'},
    'Inactive': {'ru': 'Неактивные', 'de': 'Inaktive'},
    'Gray': {'ru': 'Серые', 'de': 'Graue'},
    'Red': {'ru': 'Красные', 'de': 'Rote'},
    'Archean': {'ru': 'Архей', 'de': 'Archaikum'},
    'Proterozoic': {'ru': 'Протерозой', 'de': 'Proterozoikum'},
    "Chang'e-3 Landing Site": {'ru': 'Место посадки Чанъэ-3', 'de': "Chang'e-3 Landestelle"},
    'Belton Regio': {'ru': 'Область Белтона', 'de': 'Belton Regio'},
    'Lowell Regio': {'ru': 'Область Лоуэлла', 'de': 'Lowell Regio'},
    'Wenu Lobus': {'ru': 'Доля Уэну', 'de': 'Wenu Lobus'},
    'Weeyo Lobus': {'ru': 'Доля Уээйо', 'de': 'Weeyo Lobus'},
    'Akasa Linea': {'ru': 'Линия Акаса', 'de': 'Akasa Linea'},
    'Near the aphelion': {'ru': 'Вблизи афелия', 'de': 'In der Nähe des Aphels'},
}

# Sort in key length descending order to prevent nested word errors
notes = dict(sorted(notes.items(), key=lambda x: len(x[0]), reverse=True))
