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
    'en': 'Askaniy Anpilogov, 2020-2026',
    'ru': 'Асканий Анпилогов, 2020-2026',
    'de': 'Askaniy Anpilogov, 2020-2026'
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
gui_color_space = {
    'en': 'Color space',
    'ru': 'Цветовое пространство',
    'de': 'Farbraum'
}
gui_color_space_tooltip = {
    'en': 'Color space defines color range, encodes the technical capabilities of the display',
    'ru': 'Цветовое пространство определяет диапазон цветов, кодирует технические возможности дисплея',
    'de': 'Der Farbraum definiert den Farbbereich und kodiert die technischen Möglichkeiten des Bildschirms'
}
gui_chromatic_adaptation = {
    'en': 'Chromatic adaptation',
    'ru': 'Хроматическая адаптация',
    'de': 'Chromatische Anpassung'
}
gui_chromatic_adaptation_tooltip = {
    'en': 'Assigns white to the selected white point, calibrates by the sensitivity of the cones',
    'ru': 'Назначает белой выбранную точку белого, калибруя по чувствительности колбочек',
    'de': 'Weist dem ausgewählten Weißpunkt Weiß zu, kalibriert nach der Empfindlichkeit der Zapfen'
}
gui_gamma_correction = {
    'en': 'Gamma correction',
    'ru': 'Гамма-коррекция',
    'de': 'Gammakorrektur'
}
gui_gamma_correction_tooltip = {
    'en': 'Gamma correction models the nonlinearity of the human eye’s perception of luminance',
    'ru': 'Гамма-коррекция моделирует нелинейность восприятия яркости человеческим глазом',
    'de': 'Die Gammakorrektur modelliert die Nichtlinearität der Helligkeitswahrnehmung durch das menschliche Auge'
}
#gui_brightness = {
#    'en': 'Brightness',
#    'ru': 'Яркость',
#    'de': 'Helligkeit'
#}
gui_maximize = {
    'en': 'Maximize brightness',
    'ru': 'Максимизировать яркость',
    'de': 'Helligkeit maximieren'
}
gui_scale_factor = {
    'en': 'Scale factor',
    'ru': 'Умножить на',
    'de': 'Helligkeitsfaktor'
}
gui_scale_factor_tooltip = {
    'en': 'Multiplies the values of the output by a constant',
    'ru': 'Умножает значения вывода на константу',
    'de': 'Multipliziert die Werte der Ausgabe mit einer Konstante'
}
gui_albedo_mode = {
    'en': 'Albedo mode',
    'ru': 'Режим альбедо',
    'de': 'Albedo-Modus'
}
gui_geom = {
    'en': 'geometric albedo',
    'ru': 'геом. альбедо',
    'de': 'geometrische Albedo'
}
gui_geom_tooltip = {
    'en': 'Flux ratio to the Lambertian disk flux with the same cross-sectional area at a phase angle of 0°',
    'ru': 'Отношение потока к потоку ламбертового диска с той же площадью сечения при фазовом угле 0°',
    'de': 'Flussverhältnis zum Lambertschen Strahler mit gleicher Querschnittsfläche bei einem Phasenwinkel von 0°'
}
gui_sphe = {
    'en': 'spherical albedo',
    'ru': 'сфер. альбедо',
    'de': 'sphärische Albedo'
}
gui_sphe_tooltip = {
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
gui_tag_filter = {
    'en': 'Filter by category',
    'ru': 'Фильтр по категории',
    'de': 'Nach Kategorie filtern'
}
gui_search = {
    'en': 'Global search',
    'ru': 'Глобальный поиск',
    'de': 'Globale Suche'
}
gui_blank_note = {
    'en': '',
    'ru': '',
    'de': ''
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

# Color table
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
table_brightness_mode = {
    'en': 'Brightness mode',
    'ru': 'Режим яркости',
    'de': 'Helligkeitsmodus'
}
table_chromaticity = {
    'en': 'chromaticity',
    'ru': 'цветность',
    'de': 'Farbton'
}
table_scale_factor = {
    'en': 'Brightness scale factor',
    'ru': 'Множитель яркости',
    'de': 'Helligkeitsfaktor'
}
table_notes = {
    'en': 'Notes',
    'ru': 'Примечания',
    'de': 'Anmerkungen'
}
table_info = {
    'en': 'Info',
    'ru': 'Информация',
    'de': 'Info'
}
table_objects_number = {
    'en': 'objects displayed',
    'ru': 'объектов показано',
    'de': 'Objekte werden angezeigt'
}
table_bool_indicator = {
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
gui_filter_or_nm = {
    'en': 'Filter or nm',
    'ru': 'Фильтр или нм',
    'de': 'Filter oder nm'
}
gui_evaluate = {
    'en': 'Evaluate',
    'ru': 'Выполнить',
    'de': 'Auswerten von'
}
gui_evaluate_tooltip = {
    'en': 'Apply a function to the brightness values (x), written in Python syntax',
    'ru': 'Применить функцию к значениям яркости (x), используется синтаксис Python',
    'de': 'Wende Funktion auf Helligkeitswerte (x) an, in Python Syntax geschrieben'
}
gui_desun = {
    'en': 'Divide by Solar spectrum',
    'ru': 'Делить на спектр Солнца',
    'de': 'Division durch Sonnenspektrum'
}
gui_desun_tooltip = {
    'en': 'Removes the reflected color of the Sun, leaves the radiance factor (I/F)',
    'ru': 'Убирает отражённый цвет Солнца, оставляет отражательную способность (I/F)',
    'de': 'Entfernt die reflektierte Farbe der Sonne und belässt den Strahlungsfaktor (I/F)'
}
gui_photons = {
    'en': 'Photon counter',
    'ru': 'Счётчик фотонов',
    'de': 'Photonenzähler'
}
gui_photons_tooltip = {
    'en': 'Converts the photon spectral density of the input data into the desired energy density',
    'ru': 'Переводит спектральную плотность фотонов входных данных в требуемую энергетическую',
    'de': 'Wandelt die Photonenspektraldichte der Eingangsdaten in die gewünschte Energiedichte um'
}
#gui_autoalign = {
#    'en': 'Align image bands (β)',
#    'ru': 'Совместить изображения (β)',
#    'de': 'Bildbänder ausrichten (β)'
#}
gui_upscale = {
    'en': 'Upscale small images',
    'ru': 'Увеличить небольшие изображения',
    'de': 'Kleine Bilder vergrößern'
}
gui_upscale_tooltip = {
    'en': 'Multiplies width and height by integer times to the preview size (no interpolation)',
    'ru': 'Умножает ширину и высоту в целое число раз до размера превью (без интерполяции)',
    'de': 'Multipliziert Breite und Höhe mit ganzzahligen Werten auf die Vorschaugröße (keine Interpolation)'
}
gui_chunks = {
    'en': 'Maximum chunk size (in megapixels)',
    'ru': 'Макс. размер фрагмента (в мегапикселях)',
    'de': 'Maximale Chunkgröße (in Megapixeln)'
}
gui_chunks_tooltip = {
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
gui_exposure_settings = {
    'en': 'Exposure settings',
    'ru': 'Настройки экспозиции',
    'de': 'Belichtungseinstellungen'
}
gui_radiance = {
    'en': 'Radiance of surface in V band:',
    'ru': 'Поверхностная яркость в фильтре V:',
    'de': 'Strahlungsdichte der Oberfläche im V-Band:'
}
gui_overexposure_limit = {
    'en': 'Clipping level (overexposure):',
    'ru': 'Уровень клиппинга (переэкспозиция):',
    'de': 'Clipping-Grenze (Überbelichtung):'
}
gui_dimension = {
    'en': 'W/(m²·sr)',
    'ru': 'Вт/(м²·ср)',
    'de': 'W/(m²·sr)'
}

# Plots
spectral_plot = {
    'en': 'Energy spectral density / albedo',
    'ru': 'Спектральная плотность энергии / альбедо',
    'de': 'Spektrale Energiedichte / Albedo'
}
limit_to_vis = {
    'en': 'Limit to visible range',
    'ru': 'Только видимый диапазон',
    'de': 'Sichtbarer Spektralbereich' # Auf sichtbaren Spektralbereich begrenzen
}
normalize = {
    'en': 'Normalize at 550 nm',
    'ru': 'Нормализовать по 550 нм',
    'de': 'Normalisieren bei 550 nm'
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
    'nm': {'ru': 'нм'},
    # Part of the name to indicate moon status
    'Moon of': {'ru': 'Спутник', 'de': 'Mond von'},
    'Satellite of': {'ru': 'Спутник', 'de': 'Satellit von'},
    # Constellations
    'Andromedae': {'ru': 'Андромеды'},
    #'Antliae': {'ru': ''},
    #'Apodis': {'ru': ''},
    #'Aquarii': {'ru': ''},
    #'Aquilae': {'ru': ''},
    #'Arae': {'ru': ''},
    #'Arietis': {'ru': ''},
    #'Aurigae': {'ru': ''},
    'Boötis': {'ru': 'Волопаса'},
    #'Caeli': {'ru': ''},
    #'Camelopardalis': {'ru': ''},
    'Cancri': {'ru': 'Рака'},
    #'Canum Venaticorum': {'ru': ''},
    #'Canis Majoris': {'ru': ''},
    #'Canis Minoris': {'ru': ''},
    #'Capricorni': {'ru': ''},
    #'Carinae': {'ru': ''},
    #'Cassiopeiae': {'ru': ''},
    'Centauri': {'ru': 'Центавра'},
    #'Cephei': {'ru': ''},
    'Ceti': {'ru': 'Кита'},
    #'Chamaeleontis': {'ru': ''},
    #'Circini': {'ru': ''},
    'Columbae': {'ru': 'Голубя'},
    'Comae Berenices': {'ru': 'Волос Вероники'},
    #'Coronae Australis': {'ru': ''},
    #'Coronae Borealis': {'ru': ''},
    #'Corvi': {'ru': ''},
    #'Crateris': {'ru': ''},
    #'Crucis': {'ru': ''},
    'Cygni': {'ru': 'Лебедя'},
    #'Delphini': {'ru': ''},
    'Doradus': {'ru': 'Золотой Рыбы'},
    #'Draconis': {'ru': ''},
    #'Equulei': {'ru': ''},
    #'Eridani': {'ru': ''},
    #'Fornacis': {'ru': ''},
    #'Geminorum': {'ru': ''},
    #'Gruis': {'ru': ''},
    #'Herculis': {'ru': ''},
    #'Horologii': {'ru': ''},
    #'Hydrae': {'ru': ''},
    #'Hydri': {'ru': ''},
    #'Indi': {'ru': ''},
    'Lacertae': {'ru': 'Ящерицы'},
    #'Leonis': {'ru': ''},
    #'Leonis Minoris': {'ru': ''},
    'Leporis': {'ru': 'Зайца'},
    #'Librae': {'ru': ''},
    #'Lupi': {'ru': ''},
    #'Lyncis': {'ru': ''},
    #'Lyrae': {'ru': ''},
    #'Mensae': {'ru': ''},
    'Microscopii': {'ru': 'Микроскопа'},
    #'Monocerotis': {'ru': ''},
    #'Muscae': {'ru': ''},
    #'Normae': {'ru': ''},
    #'Octantis': {'ru': ''},
    #'Ophiuchi': {'ru': ''},
    'Orionis': {'ru': 'Ориона'},
    #'Pavonis': {'ru': ''},
    'Pegasi': {'ru': 'Пегаса'},
    #'Persei': {'ru': ''},
    #'Phoenicis': {'ru': ''},
    #'Pictoris': {'ru': ''},
    #'Piscium': {'ru': ''},
    #'Piscis Austrini': {'ru': ''},
    #'Puppis': {'ru': ''},
    #'Pyxidis': {'ru': ''},
    #'Reticuli': {'ru': ''},
    #'Sagittae': {'ru': ''},
    #'Sagittarii': {'ru': ''},
    'Scorpii': {'ru': 'Скорпиона'},
    #'Sculptoris': {'ru': ''},
    #'Scuti': {'ru': ''},
    #'Serpentis': {'ru': ''},
    #'Sextantis': {'ru': ''},
    #'Tauri': {'ru': ''},
    #'Telescopii': {'ru': ''},
    #'Trianguli': {'ru': ''},
    #'Trianguli Australis': {'ru': ''},
    #'Tucanae': {'ru': ''},
    #'Ursae Majoris': {'ru': ''},
    #'Ursae Minoris': {'ru': ''},
    #'Velorum': {'ru': ''},
    'Virginis': {'ru': 'Девы'},
    #'Volantis': {'ru': ''},
    #'Vulpeculae': {'ru': ''},
    # Stars
    'Adhara': {'ru': 'Адара'},
    'Alchiba': {'ru': 'Альхиба'},
    'Alkaid': {'ru': 'Алькаид'},
    'Alphard': {'ru': 'Альфард'},
    'Alsephina': {'ru': 'Альсефина'},
    'Altair': {'ru': 'Альтаир'},
    'Alsafi': {'ru': 'Альсафи'},
    'Ankaa': {'ru': 'Анкаа'},
    'Arcturus': {'ru': 'Арктур', 'de': 'Arkturus'},
    'Avior': {'ru': 'Авиор'},
    'Barnard’s Star': {'ru': 'Звезда Барнарда', 'de': 'Barnards Stern'},
    'Bellatrix': {'ru': 'Беллатрикс'},
    'Betelgeuse': {'ru': 'Бетельгейзе', 'de': 'Beteigeuze'},
    'Canopus': {'ru': 'Канопус'},
    'Crab Pulsar': {'ru': 'Пульсар в Крабе', 'de': 'Krebspulsar'},
    'Debris disk of AU Microscopii': {'ru': 'Осколочный диск AU Микроскопа', 'de': 'Trümmerscheibe von AU Microscopii'},
    'Gacrux': {'ru': 'Гакрукс'},
    'Geminga': {'ru': 'Геминга'},
    'Gliese': {'ru': 'Глизе'},
    'Miaplacidus': {'ru': 'Миаплацидус'},
    'Mimosa': {'ru': 'Мимоза'},
    'Mira': {'ru': 'Мира'},
    'Mirzam': {'ru': 'Мирцам', 'de': 'Murzim'},
    'Procyon': {'ru': 'Процион', 'de': 'Prokyon'},
    'Proxima Centauri': {'ru': 'Проксима Центавра'},
    'Ran': {'ru': 'Ран'},
    'Rigel': {'ru': 'Ригель'},
    'Sceptrum': {'ru': 'Скип'},
    'Sirius': {'ru': 'Сириус'},
    'Suhail': {'ru': 'Сухайль'},
    'Titawin': {'ru': 'Титавин'},
    'van Maanen 2': {'ru': 'ван Маанен 2'},
    'Vega': {'ru': 'Вега', 'de': 'Wega'},
    'Vela Pulsar': {'ru': 'Пульсар в Парусах', 'de': 'Vela-Pulsar'},
    'Wezen': {'ru': 'Везен'},
    'Yildun': {'ru': 'Йильдун'},
    # Star types
    'Wolf-Rayet stars': {'ru': 'Звёзды Вольфа — Райе', 'de': 'Wolf-Rayet-Sterne'},
    'White dwarfs': {'ru': 'Белые карлики', 'de': 'Weiße Zwerge'},
    # Solar system
    'Sun': {'ru': 'Солнце', 'de': 'Sonne'},
    'Mercury': {'ru': 'Меркурий', 'de': 'Merkur'},
    'Venus': {'ru': 'Венера'},
    'Surface of Venus': {'ru': 'Поверхность Венеры', 'de': 'Oberfläche der Venus'},
    'Clouds of Venus': {'ru': 'Облака Венеры', 'de': 'Wolken der Venus'},
    'Sky of Venus': {'ru': 'Небо Венеры', 'de': 'Himmel der Venus'},
    'Earth': {'ru': 'Земля', 'de': 'Erde'},
    'Surface of Earth': {'ru': 'Поверхность Земли', 'de': 'Oberfläche der Erde'},
    'Clouds of Earth': {'ru': 'Облака Земли', 'de': 'Wolken der Erde'},
    'Oceans of Earth': {'ru': 'Океаны Земли', 'de': 'Ozeane der Erde'},
    'Caribbean Sea': {'ru': 'Карибское море', 'de': 'Karibisches Meer'},
    'Moon': {'ru': 'Луна', 'de': 'Mond'},
    'Guang Han Gong': {'ru': 'Гуанханьгун'},
    'Mars': {'ru': 'Марс'},
    'Sky of Mars': {'ru': 'Небо Марса', 'de': 'Himmel vom Mars'},
    'Olympus Mons': {'ru': 'Олимп'},
    'Valles Marineris': {'ru': 'Долины Маринер'},
    'Phobos': {'ru': 'Фобос'},
    'Deimos': {'ru': 'Деймос'},
    # Jovian system
    'Jupiter': {'ru': 'Юпитер'},
    'Great Red Spot': {'ru': 'Большое красное пятно', 'de': 'Großer Roter Fleck'},
    'Rings of Jupiter': {'ru': 'Кольца Юпитера', 'de': 'Jupiterringe'},
    'Main ring': {'ru': 'Главное кольцо', 'de': 'Hauptring'},
    'Amalthea': {'ru': 'Амальтея'},
    'Thebe': {'ru': 'Фива'},
    'Io': {'ru': 'Ио'},
    'Europa': {'ru': 'Европа'},
    'Ganymede': {'ru': 'Ганимед', 'de': 'Ganymed'},
    'Callisto': {'ru': 'Каллисто', 'de': 'Kallisto'},
    # Jovian irregulars
    'Himalia': {'ru': 'Гималия'},
    'Elara': {'ru': 'Элара'},
    'Pasiphae': {'ru': 'Пасифе'},
    'Sinope': {'ru': 'Синопе'},
    'Lysithea': {'ru': 'Лиситея'},
    'Carme': {'ru': 'Карме'},
    'Ananke': {'ru': 'Ананке'},
    'Leda': {'ru': 'Леда'},
    'Callirrhoe': {'ru': 'Каллирое'},
    'Themisto': {'ru': 'Фемисто'},
    'Megaclite': {'ru': 'Мегаклите'},
    'Taygete': {'ru': 'Тайгете'},
    'Chaldene': {'ru': 'Халдене'},
    'Harpalyke': {'ru': 'Гарпалике'},
    'Kalyke': {'ru': 'Калике'},
    'Iocaste': {'ru': 'Иокасте'},
    'Erinome': {'ru': 'Эриноме'},
    'Isonoe': {'ru': 'Исоное'},
    'Praxidike': {'ru': 'Праксидике'},
    'Autonoe': {'ru': 'Автоное'},
    'Thyone': {'ru': 'Тионе'},
    'Hermippe': {'ru': 'Гермиппе'},
    'Eukelade': {'ru': 'Эвкеладе'},
    'Cyllene': {'ru': 'Киллене'},
    # Saturnian system
    'Saturn': {'ru': 'Сатурн'},
    'Aurorae of Saturn': {'ru': 'Полярные сияния Сатурна', 'de': 'Saturn-Auroräen'},
    'Rings of Saturn': {'ru': 'Кольца Сатурна', 'de': 'Saturnringe'},
    'D ring': {'ru': 'Кольцо D', 'de': 'D-Ring'},
    'D72 ringlet': {'ru': 'Кольцо D72', 'de': 'D72-Ring'},
    'D73 ringlet': {'ru': 'Кольцо D73', 'de': 'D73-Ring'},
    'C ring': {'ru': 'Кольцо C', 'de': 'C-Ring'},
    'B ring': {'ru': 'Кольцо B', 'de': 'B-Ring'},
    'Cassini Division': {'ru': 'Деление Кассини', 'de': 'Cassinische Teilung'},
    'A ring': {'ru': 'Кольцо A', 'de': 'A-Ring'},
    'F ring': {'ru': 'Кольцо F', 'de': 'F-Ring'},
    'G ring': {'ru': 'Кольцо G', 'de': 'G-Ring'},
    'E ring': {'ru': 'Кольцо E', 'de': 'E-Ring'},
    'Pan': {'ru': 'Пан'},
    'Daphnis': {'ru': 'Дафнис'},
    'Atlas': {'ru': 'Атлас'},
    'Prometheus': {'ru': 'Прометей'},
    'Pandora': {'ru': 'Пандора'},
    'Janus': {'ru': 'Янус'},
    'Epimetheus': {'ru': 'Эпиметей'},
    'Aegaeon': {'ru': 'Эгеон'},
    'Mimas': {'ru': 'Мимас'},
    'Methone': {'ru': 'Мефона'},
    'Pallene': {'ru': 'Паллена'},
    'Enceladus': {'ru': 'Энцелад'},
    'Tethys': {'ru': 'Тефия'},
    'Telesto': {'ru': 'Телесто'},
    'Calypso': {'ru': 'Калипсо'},
    'Dione': {'ru': 'Диона'},
    'Helene': {'ru': 'Елена'},
    'Polydeuces': {'ru': 'Полидевк'},
    'Rhea': {'ru': 'Рея'},
    'Titan': {'ru': 'Титан'},
    'Surface of Titan': {'ru': 'Поверхность Титана', 'de': 'Oberfläche von Titan'},
    'Shangri-La': {'ru': 'Шангри-Ла'},
    'Hyperion': {'ru': 'Гиперион'},
    'Iapetus': {'ru': 'Япет'},
    # Saturnian irregulars
    'Phoebe': {'ru': 'Феба'},
    'Ymir': {'ru': 'Имир'},
    'Paaliaq': {'ru': 'Палиак'},
    'Tarvos': {'ru': 'Тарвос'},
    'Ijiraq': {'ru': 'Иджирак'},
    'Suttungr': {'ru': 'Суттунг'},
    'Kiviuq': {'ru': 'Кивиок'},
    'Mundilfari': {'ru': 'Мундильфари'},
    'Albiorix': {'ru': 'Альбиорикс'},
    'Skathi': {'ru': 'Скади'},
    'Erriapus': {'ru': 'Эррипо'},
    'Siarnaq': {'ru': 'Сиарнак'},
    'Thrymr': {'ru': 'Трюм'},
    'Narvi': {'ru': 'Нарви'},
    'Aegir': {'ru': 'Эгир'},
    'Bebhionn': {'ru': 'Бефинд'},
    'Bergelmir': {'ru': 'Бергельмир'},
    'Bestla': {'ru': 'Бестла'},
    'Fornjot': {'ru': 'Форньот'},
    'Hyrrokkin': {'ru': 'Гирроккин'},
    'Kari': {'ru': 'Кари'},
    'Tarqeq': {'ru': 'Таркек'},
    # Uranian system
    'Uranus': {'ru': 'Уран'},
    'Rings of Uranus': {'ru': 'Кольца Урана', 'de': 'Uranusringe'},
    'α and β rings': {'ru': 'Кольца α и β', 'de': 'α- und β-Ringe'},
    'α ring': {'ru': 'Кольцо α', 'de': 'α-Ring'},
    'β ring': {'ru': 'Кольцо β', 'de': 'β-Ring'},
    'η, γ, and δ rings': {'ru': 'Кольца η, γ и δ', 'de': 'η-, γ- und δ-Ringe'},
    'η ring': {'ru': 'Кольцо η', 'de': 'η-Ring'},
    'γ ring': {'ru': 'Кольцо γ', 'de': 'γ-Ring'},
    'δ ring': {'ru': 'Кольцо δ', 'de': 'δ-Ring'},
    'ε ring': {'ru': 'Кольцо ε', 'de': 'ε-Ring'},
    'Portia': {'ru': 'Порция'},
    'Portia group': {'ru': 'Группа Порции', 'de': 'Portia-Gruppe'},
    'Puck': {'ru': 'Пак'},
    'Miranda': {'ru': 'Миранда'},
    'Ariel': {'ru': 'Ариэль'},
    'Umbriel': {'ru': 'Умбриэль'},
    'Titania': {'ru': 'Титания'},
    'Oberon': {'ru': 'Оберон'},
    # Uranian irregulars
    'Caliban': {'ru': 'Калибан'},
    'Sycorax': {'ru': 'Сикоракса'},
    'Prospero': {'ru': 'Просперо'},
    'Setebos': {'ru': 'Сетебос'},
    'Stephano': {'ru': 'Стефано'},
    'Trinculo': {'ru': 'Тринкуло'},
    # Neptunian system
    'Neptune': {'ru': 'Нептун', 'de': 'Neptun'},
    'Northern Dark Spot': {'ru': 'Северное тёмное пятно', 'de': 'Nördlicher Dunkler Fleck'},
    'Naiad': {'ru': 'Наяда'},
    'Thalassa': {'ru': 'Таласса'},
    'Despina': {'ru': 'Деспина'},
    'Galatea': {'ru': 'Галатея'},
    'Larissa': {'ru': 'Ларисса'},
    'Proteus': {'ru': 'Протей'},
    'Neptunian inner satellites': {'ru': 'Внутренние спутники Нептуна', 'de': 'Innere Satelliten des Neptun'},
    'Triton': {'ru': 'Тритон'},
    'Nereid': {'ru': 'Нереида'},
    # Neptunian irregulars
    'Halimede': {'ru': 'Галимеда'},
    'Neso': {'ru': 'Несо'},
    # Minor bodies
    'Ceres': {'ru': 'Церера'},
    'Ahuna Mons': {'ru': 'Горы Ахуна'},
    'Cerealia Facula': {'ru': 'Факула Цереалий'},
    'Haulani Crater': {'ru': 'Кратер Хаулани'},
    'Vinalia Faculae': {'ru': 'Факулы Виналий'},
    'Yalode Crater': {'ru': 'Кратер Ялоде'},
    'Pallas': {'ru': 'Паллада'},
    'Juno': {'ru': 'Юнона'},
    'Vesta': {'ru': 'Веста'},
    'Iris': {'ru': 'Ирида'},
    'Metis': {'ru': 'Метида'},
    'Hygiea': {'ru': 'Гигея'},
    'Egeria': {'ru': 'Эгерия'},
    'Eunomia': {'ru': 'Эвномия'},
    'Psyche': {'ru': 'Психея'},
    'Fortuna': {'ru': 'Фортуна'},
    'Lutetia': {'ru': 'Лютеция'},
    'Kalliope': {'ru': 'Каллиопа'},
    'Themis': {'ru': 'Фемида'},
    'Amphitrite': {'ru': 'Амфитрита'},
    'Euphrosyne': {'ru': 'Евфросина'},
    'Daphne': {'ru': 'Дафна'},
    'Eugenia': {'ru': 'Евгения'},
    'Petit-Prince': {'ru': 'Маленький принц'},
    'Doris': {'ru': 'Дорида'},
    # 50
    #'Europa': {'ru': 'Европа'}, # duplicate
    'Cybele': {'ru': 'Кибела'},
    'Sylvia': {'ru': 'Сильвия'},
    'Romulus': {'ru': 'Ромул'},
    'Remus': {'ru': 'Рем'},
    'Thisbe': {'ru': 'Фисба'},
    'Antiope': {'ru': 'Антиопа'},
    'Minerva': {'ru': 'Минерва'},
    'Aegis': {'ru': 'Эгида'},
    'Aurora': {'ru': 'Аврора'},
    # 100
    'Camilla': {'ru': 'Камилла'},
    'Hermione': {'ru': 'Гермиона'},
    'Elektra': {'ru': 'Электра'},
    'Pompeja': {'ru': 'Помпея'},
    'Kleopatra': {'ru': 'Клеопатра'},
    'Ida': {'ru': 'Ида'},
    'Dactyl': {'ru': 'Дактиль'},
    'Mathilde': {'ru': 'Матильда'},
    'Justitia': {'ru': 'Юстиция'},
    'Eros': {'ru': 'Эрос'},
    'Patientia': {'ru': 'Пациенция'},
    'Griseldis': {'ru': 'Гризельда'},
    # 500
    'Davida': {'ru': 'Давида'},
    'Achilles': {'ru': 'Ахиллес'},
    'Scheila': {'ru': 'Шейла'},
    'Patroclus-Menoetius': {'ru': 'Патрокл-Менетий'},
    'Chimaera': {'ru': 'Химера'},
    'Hektor': {'ru': 'Гектор'},
    'Nestor': {'ru': 'Нестор'},
    'Interamnia': {'ru': 'Интерамния'},
    'Ani': {'ru': 'Ани'},
    'Priamus': {'ru': 'Приам'},
    'Agamemnon': {'ru': 'Агамемнон'},
    'Hidalgo': {'ru': 'Идальго'},
    'Gaspra': {'ru': 'Гаспра'},
    # 1000
    'Ganymed': {'ru': 'Ганимед'},
    'Odysseus': {'ru': 'Одиссей'},
    'Äneas': {'ru': 'Эней'},
    'Anchises': {'ru': 'Анхис'},
    'Troilus': {'ru': 'Троил'},
    'Celestia': {'ru': 'Селестия'},
    'Ajax': {'ru': 'Аякс'},
    'Diomedes': {'ru': 'Диомед'},
    'Antilochus': {'ru': 'Антилох'},
    'Geographos': {'ru': 'Географ'},
    'Menelaus': {'ru': 'Менелай'},
    'Telamon': {'ru': 'Теламон'},
    'Deiphobus': {'ru': 'Деифоб'},
    'Glaukos': {'ru': 'Главк'},
    'Astyanax': {'ru': 'Астианакт'},
    'Helenos': {'ru': 'Гелен'},
    'Agenor': {'ru': 'Агенор'},
    'Chiron': {'ru': 'Хирон'},
    'Bacchus': {'ru': 'Бахус'},
    'Antenor': {'ru': 'Антенор'},
    'Hephaistos': {'ru': 'Гефест'},
    'Sarpedon': {'ru': 'Сарпедон'},
    'Phereclos': {'ru': 'Ферекл'},
    'Masursky': {'ru': 'Мазурский'},
    'Šteins': {'ru': 'Штейнс'},
    'Phaethon': {'ru': 'Фаэтон'},
    'Paris': {'ru': 'Парис'},
    'Mentor': {'ru': 'Ментор'},
    'Eurybates': {'ru': 'Эврибат'},
    'Don Quixote': {'ru': 'Дон Кихот'},
    'Thestor': {'ru': 'Тестор'},
    'Toutatis': {'ru': 'Таутатис'},
    'Ennomos': {'ru': 'Энном'},
    'Castalia': {'ru': 'Касталия'},
    'Sergestus': {'ru': 'Сергест'},
    'Munroe': {'ru': 'Манро'},
    # 5000
    'Ilioneus': {'ru': 'Илионей'},
    'Pholus': {'ru': 'Фол'},
    'Cloanthus': {'ru': 'Клоант'},
    'Annefrank': {'ru': 'Аннафранк'},
    'Gault': {'ru': 'Голт'},
    'Golevka': {'ru': 'Голевка'},
    'Leitus': {'ru': 'Лейтус'},
    'Tithonus': {'ru': 'Титон'},
    'Nessus': {'ru': 'Несс'},
    'Hypsenor': {'ru': 'Гипсенор'},
    'Asbolus': {'ru': 'Асбол'},
    'Othryoneus': {'ru': 'Офрионей'},
    'Erichthonios': {'ru': 'Эрихтоний'},
    'Eurymachos': {'ru': 'Эвримах'},
    'Braille': {'ru': 'Брайль'},
    # 10 000
    'Chariklo': {'ru': 'Харикло'},
    'Rings of Chariklo': {'ru': 'Кольца Харикло', 'de': 'Ringe der Chariklo'},
    'Westerwald': {'ru': 'Вестервальд'},
    'Hylonome': {'ru': 'Хилонома'},
    'Leucus': {'ru': 'Левк'},
    'Ascanios': {'ru': 'Асканий'},
    'Rockox': {'ru': 'Рококс'},
    'Antiphos': {'ru': 'Антифос'},
    'Polymele': {'ru': 'Полимела'},
    'Hypeirochus': {'ru': 'Гиперох'},
    'Albion': {'ru': 'Алебион'},
    'Arawn': {'ru': 'Араун'},
    'Pyraechmes': {'ru': 'Пирехм'},
    'Thymbraeus': {'ru': 'Фимбрей'},
    'Zarex': {'ru': 'Зарекс'},
    'Dardanos': {'ru': 'Дардан'},
    'Demoleon': {'ru': 'Демолеон'},
    'Chaos': {'ru': 'Хаос'},
    'Varuna': {'ru': 'Варуна'},
    'Dioretsa': {'ru': 'Диоретса'},
    'Orus': {'ru': 'Орус'},
    'Epicles': {'ru': 'Эпикл'},
    'Ousha': {'ru': 'Оуша'}, # not confirmed (reads as o'sha)
    'Dorippe': {'ru': 'Дориппе'},
    'Thasos': {'ru': 'Тасос'},
    'Belova': {'ru': 'Белова'},
    'Itokawa': {'ru': 'Итокава'},
    'Binns': {'ru': 'Биннс'},
    'Ixion': {'ru': 'Иксион'},
    'Hippokoon': {'ru': 'Гиппокоон'},
    'Elatus': {'ru': 'Элат'},
    'Thereus': {'ru': 'Терей'},
    'Scottmanley': {'ru': 'Скоттмэнли'},
    'Rhadamanthus': {'ru': 'Радамант'},
    'Huya': {'ru': 'Гуйя'},
    'Kipkeino': {'ru': 'Кипкейно'},
    'Typhon': {'ru': 'Тифон'},
    'Echidna': {'ru': 'Ехидна'},
    'Lempo–Hiisi': {'ru': 'Лемпо–Хийси'},
    'Pelion': {'ru': 'Пелион'},
    # 50 000
    'Quaoar': {'ru': 'Квавар'},
    'Donaldjohanson': {'ru': 'Дональдджохансон'},
    'Okyrhoe': {'ru': 'Окироя'},
    'Cyllarus': {'ru': 'Киллар'},
    'Deucallion': {'ru': 'Девкалион'},
    'Bienor': {'ru': 'Биенор'},
    'Aya': {'ru': 'Айа'},
    'Amycus': {'ru': 'Амик'},
    'Uni': {'ru': 'Уни'}, # has moon Tinia (Тиния)
    'Logos': {'ru': 'Логос'},
    'Moza': {'ru': 'Моза'}, # not confirmed
    'Echeclus': {'ru': 'Эхекл'},
    'Ceto': {'ru': 'Кето'},
    'Phorcys': {'ru': 'Форкий'},
    'Didymos': {'ru': 'Дидим'},
    'Moshup': {'ru': 'Мошуп'},
    'Borasisi': {'ru': 'Борасизи'},
    'Pabu': {'ru': 'Пабу'},
    'Sila–Nunam': {'ru': 'Сила–Нунам'},
    'Crantor': {'ru': 'Крантор'},
    'Teharonhiawako': {'ru': 'Таронхайавагон'},
    'Sawiskera': {'ru': 'Тавискарон'},
    'Sedna': {'ru': 'Седна'},
    'Orcus': {'ru': 'Орк'},
    'Vanth': {'ru': 'Вант'},
    'Goibniu': {'ru': 'Гоибниу'},
    'Torifune': {'ru': 'Торифуне'},
    'Apophis': {'ru': 'Апофис'},
    # 100 000
    'Bennu': {'ru': 'Бенну'},
    'Salacia': {'ru': 'Салация'},
    'Actaea': {'ru': 'Актея'},
    'Aphidas': {'ru': 'Афида'},
    'Pluto': {'ru': 'Плутон'},
    'Baret Montes': {'ru': 'Горы Барре'},
    'Belton Regio': {'ru': 'Область Белтона'},
    'Lowell Regio': {'ru': 'Область Лоуэлла'},
    'Sputnik Planitia': {'ru': 'Равнина Спутник'},
    'Viking Terra': {'ru': 'Земля Викинг'},
    'Charon': {'ru': 'Харон'},
    'Mordor Macula': {'ru': 'Макула Мордор'},
    'Nix': {'ru': 'Никта'},
    'Gleti Crater': {'ru': 'Кратер Глети'},
    'Hydra': {'ru': 'Гидра'},
    'Haumea': {'ru': 'Хаумеа'},
    'Dark Red Spot': {'ru': 'Тёмное красное пятно', 'de': 'Dunkelroter Fleck'},
    'Ring of Haumea': {'ru': 'Кольцо Хаумеа', 'de': 'Ring der Haumea'},
    'Hiʻiaka': {'ru': 'Хииака'},
    'Namaka': {'ru': 'Намака'},
    'Eris': {'ru': 'Эрида'},
    'Makemake': {'ru': 'Макемаке'},
    'Rumina': {'ru': 'Румина'},
    'Ritona': {'ru': 'Ритона'},
    'Altjira': {'ru': 'Алтьира'},
    'Dinkinesh': {'ru': 'Динкинеш'},
    'Ryugu': {'ru': 'Рюгу'},
    'Cardea': {'ru': 'Кардея'},
    'Varda': {'ru': 'Варда'},
    'Ilmarë': {'ru': 'Ильмарэ'},
    'Achlys': {'ru': 'Ахлис'},
    'Gonggong': {'ru': 'Гунгун'},
    'Xiangliu': {'ru': 'Сянлю'},
    'Gǃkúnǁʼhòmdímà': {'ru': 'Гкъкунлъ’хомдима'},
    'Gǃòʼé ǃHú': {'ru': 'Гкъо’э Къху'},
    'Máni': {'ru': 'Мани'},
    'Mors–Somnus': {'ru': 'Мор–Сомн'},
    'Mors': {'ru': 'Мор'},
    'Somnus': {'ru': 'Сомн'},
    'Rhiphonos': {'ru': 'Рифон'}, # no official ru translation
    'Manwë': {'ru': 'Манвэ'},
    'Thorondor': {'ru': 'Торондор'},
    'Otrera': {'ru': 'Отрера'},
    'Clete': {'ru': 'Клета'},
    'Kamo‘oalewa': {'ru': 'Камоалева'},
    'ǂKá̦gára': {'ru': 'Кагара'}, # no official ru translation
    'Dziewanna': {'ru': 'Девана'},
    'Alicanto': {'ru': 'Аликанто'},
    # 500 000
    'Arrokoth': {'ru': 'Аррокот'},
    'Wenu Lobus': {'ru': 'Доля Уэну'},
    'Weeyo Lobus': {'ru': 'Доля Уээйо'},
    'Akasa Collum': {'ru': 'Шея Акаса'},
    'Zoozve': {'ru': 'Зоозве'},
    'Chiminigagua': {'ru': 'Чиминигагуа'},
    '’Ayló’chaxnim': {'ru': 'Айло́тчахним'}, # no official ru translation
    # Comets and interstellar objects
    'ʻOumuamua': {'ru': 'Оумуамуа'},
    # Comet discovery sites
    'CINEOS': {},
    'NEAT': {},
    'PanSTARRS': {},
    'LONEOS': {},
    'LINEAR': {},
    'WISE': {},
    'Spacewatch': {},
    'Palomar': {},
    'Lemmon': {},
    'Tenagra': {'ru': 'Тенагра'},
    'La Sagra': {'ru': 'Ла-Сагра'},
    'Catalina': {'ru': 'Каталина'},
    'Siding Spring': {'ru': 'Сайдинг Спринг'},
    # Comet discoverers
    'Arend': {'ru': 'Арена'},
    'Arend–Rigaux': {'ru': 'Арена — Риго'},
    'd’Arrest': {'ru': 'д’Арре'},
    'Ashbrook–Jackson': {'ru': 'Ашбрука — Джексона'},
    'Bernardinelli–Bernstein': {'ru': 'Бернардинелли — Бернштейна'},
    'Boattini': {'ru': 'Боаттини'},
    'Borrelly': {'ru': 'Борелли'}, # in ru with one "r"
    'Borisov': {'ru': 'Борисова'},
    'Churyumov–Gerasimenko': {'ru': 'Чурюмова — Герасименко', 'de': 'Tschurjumow-Gerassimenko'},
    'Elst–Pizarro': {'ru': 'Эльст — Писарро'},
    'Encke': {'ru': 'Энке'},
    'Faye': {'ru': 'Фая'},
    'Forbes': {'ru': 'Форбса'},
    'Garradd': {'ru': 'Гаррадда'},
    'Giacobini–Zinner': {'ru': 'Джакобини — Циннера'},
    'Gibbs': {'ru': 'Гиббса'},
    'Gleason': {'ru': 'Глисона'},
    'Hale–Bopp': {'ru': 'Хейла — Боппа'},
    'Halley': {'ru': 'Галлея'},
    'Hartley': {'ru': 'Хартли'},
    'Hill': {'ru': 'Хилла'},
    'Holmes': {'ru': 'Холмса'},
    'Honda–Mrkos–Pajdušáková': {'ru': 'Хонда — Мркоса — Пайдушаковой'},
    'Kearns–Kwee': {'ru': 'Кирнса — Гуи'},
    'Kopff': {'ru': 'Копффа'},
    'Kowalski': {'ru': 'Ковальски'},
    'Kowal': {'ru': 'Коваля'},
    'Kowal–Mrkos': {'ru': 'Коваля — Мркоса'},
    'Larsen': {'ru': 'Ларсена'},
    'Leonard': {'ru': 'Леонарда'},
    'Lovejoy': {'ru': 'Лавджоя'},
    'Machholz': {'ru': 'Макхольца'},
    'McNaught': {'ru': 'Макнота'},
    'Neujmin': {'ru': 'Неуймина'},
    'Oterma': {'ru': 'Отерма'},
    'Pons–Brooks': {'ru': 'Понса — Брукса'},
    'Pons–Winnecke': {'ru': 'Понса — Виннеке'},
    'Read': {'ru': 'Рида'},
    'Russell': {'ru': 'Рассела'},
    'Sanguin': {'ru': 'Сангина'},
    'Schuster': {'ru': 'Шустера'},
    'Schwartz': {'ru': 'Шварца'},
    'Schwassmann–Wachmann': {'ru': 'Швассмана — Вахмана'},
    'Shoemaker–Holt': {'ru': 'Шумейкеров — Хольта'},
    'Shoemaker–Levy': {'ru': 'Шумейкеров — Леви'},
    'Skiff': {'ru': 'Скиффа'},
    'Tempel': {'ru': 'Темпеля'},
    'Tempel–Tuttle': {'ru': 'Темпеля — Туттля'},
    'Tsuchinshan–ATLAS': {'ru': 'Цзыцзиньшань — ATLAS'},
    'Tuttle': {'ru': 'Туттля'},
    'Whipple': {'ru': 'Уиппла'},
    'Wild': {'ru': 'Вильда'},
    'Wilson–Harrington': {'ru': 'Вильсон — Харрингтон'},
    'Wirtanen': {'ru': 'Виртанена'},
    'Wiseman–Skiff': {'ru': 'Уайзмана — Скиффа'},
    'Wolf': {'ru': 'Вольфа'},
    # Classes
    'Class': {'ru': 'Класс', 'de': 'Klasse'},
    'Spectral type': {'ru': 'Спектральный класс', 'de': 'Spektraltyp'},
    'A-type': {'ru': 'Класс A', 'de': 'A-Klasse'},
    'B-type': {'ru': 'Класс B', 'de': 'B-Klasse'},
    'C-type': {'ru': 'Класс C', 'de': 'C-Klasse'},
    'Cb-type': {'ru': 'Класс Cb', 'de': 'Cb-Klasse'},
    'Cg-type': {'ru': 'Класс Cg', 'de': 'Cg-Klasse'},
    'Cgh-type': {'ru': 'Класс Cgh', 'de': 'Cgh-Klasse'},
    'Ch-type': {'ru': 'Класс Ch', 'de': 'Ch-Klasse'},
    'D-type': {'ru': 'Класс D', 'de': 'D-Klasse'},
    'DP-type': {'ru': 'Класс DP', 'de': 'DP-Klasse'},
    'E-type': {'ru': 'Класс E', 'de': 'E-Klasse'},
    'K-type': {'ru': 'Класс K', 'de': 'K-Klasse'},
    'L-type': {'ru': 'Класс L', 'de': 'L-Klasse'},
    'Ld-type': {'ru': 'Класс Ld', 'de': 'Ld-Klasse'},
    'M-type': {'ru': 'Класс M', 'de': 'M-Klasse'},
    'O-type': {'ru': 'Класс O', 'de': 'O-Klasse'},
    'P-type': {'ru': 'Класс P', 'de': 'P-Klasse'},
    'PD-type': {'ru': 'Класс PD', 'de': 'PD-Klasse'},
    'Q-type': {'ru': 'Класс Q', 'de': 'Q-Klasse'},
    'R-type': {'ru': 'Класс R', 'de': 'R-Klasse'},
    'S-type': {'ru': 'Класс S', 'de': 'S-Klasse'},
    'Sa-type': {'ru': 'Класс Sa', 'de': 'Sa-Klasse'},
    'Sk-type': {'ru': 'Класс Sk', 'de': 'Sk-Klasse'},
    'Sl-type': {'ru': 'Класс Sl', 'de': 'Sl-Klasse'},
    'Sq-type': {'ru': 'Класс Sq', 'de': 'Sq-Klasse'},
    'Sr-type': {'ru': 'Класс Sr', 'de': 'Sr-Klasse'},
    'Sv-type': {'ru': 'Класс Sv', 'de': 'Sv-Klasse'},
    'Sw-type': {'ru': 'Класс Sw', 'de': 'Sw-Klasse'},
    'T-type': {'ru': 'Класс T', 'de': 'T-Klasse'},
    'V-type': {'ru': 'Класс V', 'de': 'V-Klasse'},
    'Z-type': {'ru': 'Класс Z', 'de': 'Z-Klasse'},
    'X-type': {'ru': 'Класс X', 'de': 'X-Klasse'},
    'Xc-type': {'ru': 'Класс Xc', 'de': 'Xc-Klasse'},
    'Xe-type': {'ru': 'Класс Xe', 'de': 'Xe-Klasse'},
    'Xk-type': {'ru': 'Класс Xk', 'de': 'Xk-Klasse'},
    'Xn-type': {'ru': 'Класс Xn', 'de': 'Xn-Klasse'},
    'Jovian irregulars': {'ru': 'Нерегулярные спутники Юпитера', 'de': 'irreguläre Jupitermonde'},
    'Jupiter trojans': {'ru': 'Троянцы Юпитера', 'de': 'Jupiter-Trojaner'},
    'Saturnian irregulars': {'ru': 'Нерегулярные спутники Сатурна', 'de': 'irreguläre Saturnmonde'},
    'Uranian irregulars': {'ru': 'Нерегулярные спутники Урана', 'de': 'irreguläre Uranusmonde'},
    'Neptunian irregulars': {'ru': 'Нерегулярные спутники Нептуна', 'de': 'irreguläre Neptunmonde'},
    'Neptune trojans': {'ru': 'Троянцы Нептуна', 'de': 'Neptun-Trojaner'},
    'Comets': {'ru': 'Кометы', 'de': 'Kometen'},
    'Damocloids': {'ru': 'Дамоклоиды', 'de': 'Damocloiden'},
    'Centaurs': {'ru': 'Кентавры', 'de': 'Zentauren'},
    'Plutinos': {'ru': 'Плутино', 'de': 'Plutinos'},
    'Other resonances': {'ru': 'Другие резонансы', 'de': 'Andere Resonanzen'},
    'Haumea family': {'ru': 'Семейство Хаумеа', 'de': 'Haumea-Familie'},
    'Cubewano': {'ru': 'Кьюбивано', 'de': 'Cubewano'},
    'SDO': {'ru': 'Рассеянный диск', 'de': 'SDO'},
    'Detached objects': {'ru': 'Обособл. ТНО', 'de': 'Detached Objects'},
    # Deep sky objects
    'Galaxy bulges': {'ru': 'Ядра галактик', 'de': 'Galaxienbulge'},
    'Elliptical galaxies': {'ru': 'Эллиптические галактики', 'de': 'Elliptische Galaxien'},
    'Spiral galaxies': {'ru': 'Спиральные галактики', 'de': 'Spiralgalaxien'},
    'Starburst galaxies with': {'ru': 'Галактики со вспышкой зв. образ.', 'de': 'Sternburstgalaxien mit'}, # "with 0.39 < E(B-V) < 0.50" for example
    'Quasars': {'ru': 'Квазары', 'de': 'Quasare'},
    'Galactic cirri': {'ru': 'Галактические циррусы', 'de': 'Galaktische Cirri'},
    'Envelope of CW Leonis': {'ru': 'Оболочка CW Льва', 'de': 'Hülle von CW Leonis'},
    'Planetary nebula': {'ru': 'Планетарная туманность', 'de': 'Planetarischer Nebel'},
    'Nova, nebular phase': {'ru': 'Новая, фаза туманности', 'de': 'Nova, nebulöse Phase'},
    # Materials
    'Soil at Venera 13 landing site': {'ru': 'Грунт на месте посадки Венеры-13', 'de': 'Boden am Landeplatz von Venera 13'},
    'Rocks at Venera 13 landing site': {'ru': 'Камни на месте посадки Венеры-13', 'de': 'Felsen am Landeplatz von Venera 13'},
    'Bright red drift at Pathfinder landing site': {'ru': 'Ярко-красный нанос на м. посадки Pathfinder', 'de': 'Hellroter Drift am Pathfinder-Landeplatz'},
    'Bright rock at Pathfinder landing site': {'ru': 'Яркий камень на месте посадки Pathfinder', 'de': 'Heller Fels am Pathfinder-Landeplatz'},
    'Dark rock at Pathfinder landing site': {'ru': 'Тёмный камень на м. посадки Pathfinder', 'de': 'Dunkler Fels am Pathfinder-Landeplatz'},
    'Pink rock at Pathfinder landing site': {'ru': 'Розовый камень на м. посадки Pathfinder', 'de': 'Rosa Fels am Pathfinder-Landeplatz'},
    'Rock at Pathfinder landing site': {'ru': 'Камень на месте посадки Pathfinder', 'de': 'Fels am Pathfinder-Landeplatz'},
    'Bright soil at Pathfinder landing site': {'ru': 'Яркий грунт на месте посадки Pathfinder', 'de': 'Heller Boden am Pathfinder-Landeplatz'},
    'Dark soil at Pathfinder landing site': {'ru': 'Тёмный грунт на месте посадки Pathfinder', 'de': 'Dunkler Boden am Pathfinder-Landeplatz'},
    'Disturbed soil at Pathfinder landing site': {'ru': 'След на грунте от Pathfinder', 'de': 'Gestörter Boden am Pathfinder-Landeplatz'},
    'Lamb-like soil at Pathfinder landing site': {'ru': 'Смешанный грунт на м. посадки Pathfinder', 'de': 'Gemischter Boden am Pathfinder-Landeplatz'},
    'Soil at Pathfinder landing site': {'ru': 'Грунт на месте посадки Pathfinder', 'de': 'Boden am Pathfinder-Landeplatz'},
    'Ice at Phoenix landing site': {'ru': 'Лёд на месте посадки Phoenix', 'de': 'Eis am Phoenix-Landeplatz'},
    'Soil at Phoenix landing site': {'ru': 'Грунт на месте посадки Phoenix', 'de': 'Boden am Phoenix-Landeplatz'},
    'Martian dust, 130 nm': {'ru': 'Пыль, 130 нм', 'de': 'Marsstaub, 130 nm'},
    'Martian dust, 165 nm': {'ru': 'Пыль, 165 нм', 'de': 'Marsstaub, 165 nm'},
    'Martian dust, 180 nm': {'ru': 'Пыль, 180 нм', 'de': 'Marsstaub, 180 nm'},
    'Martian snow, 100 μm': {'ru': 'Снег, 100 мкм', 'de': 'Mars-Schnee, 100 μm'},
    'Martian snow, 100 μm and 0.01% dust': {'ru': 'Марсианский снег, 100 мкм и 0,01% пыли', 'de': 'Mars-Schnee, 100 μm und 0,01% Staub'},
    'Martian snow, 100 μm and 0.1% dust': {'ru': 'Марсианский снег, 100 мкм и 0,1% пыли', 'de': 'Mars-Schnee, 100 μm und 0,1% Staub'},
    'Martian snow, 100 μm and 1% dust': {'ru': 'Марсианский снег, 100 мкм и 1% пыли', 'de': 'Mars-Schnee, 100 μm und 1% Staub'},
    'Martian snow, 100 μm and 10% dust': {'ru': 'Марсианский снег, 100 мкм и 10% пыли', 'de': 'Mars-Schnee, 100 μm und 10% Staub'},
    'Martian snow, 350 μm': {'ru': 'Марсианский снег, 350 мкм', 'de': 'Mars-Schnee, 350 μm'},
    'Martian snow, 350 μm and 0.015% dust': {'ru': 'Марсианский снег, 350 мкм и 0,015% пыли', 'de': 'Mars-Schnee, 350 μm und 0,015% Staub'},
    'Martian snow, 500 μm': {'ru': 'Марсианский снег, 500 мкм', 'de': 'Mars-Schnee, 500 μm'},
    'Martian snow, 500 μm and 0.01% dust': {'ru': 'Марсианский снег, 500 мкм и 0,01% пыли', 'de': 'Mars-Schnee, 500 μm und 0,01% Staub'},
    'Martian snow, 500 μm and 0.1% dust': {'ru': 'Марсианский снег, 500 мкм и 0,1% пыли', 'de': 'Mars-Schnee, 500 μm und 0,1% Staub'},
    'Martian snow, 500 μm and 1% dust': {'ru': 'Марсианский снег, 500 мкм и 1% пыли', 'de': 'Mars-Schnee, 500 μm und 1% Staub'},
    'Martian snow, 500 μm and 10% dust': {'ru': 'Марсианский снег, 500 мкм и 10% пыли', 'de': 'Mars-Schnee, 500 μm und 10% Staub'},
    'Martian firn, 2500 μm': {'ru': 'Марсианский фирн, 2500 мкм', 'de': 'Mars-Firn, 2500 μm'},
    'Martian firn, 2500 μm and 0.01% dust': {'ru': 'Марсианский фирн, 2500 мкм и 0,01% пыли', 'de': 'Mars-Firn, 2500 μm und 0,01% Staub'},
    'Martian firn, 2500 μm and 0.1% dust': {'ru': 'Марсианский фирн, 2500 мкм и 0,1% пыли', 'de': 'Mars-Firn, 2500 μm und 0,1% Staub'},
    'Martian firn, 2500 μm and 1% dust': {'ru': 'Марсианский фирн, 2500 мкм и 1% пыли', 'de': 'Mars-Firn, 2500 μm und 1% Staub'},
    'Martian firn, 2500 μm and 10% dust': {'ru': 'Марсианский фирн, 2500 мкм и 10% пыли', 'de': 'Mars-Firn, 2500 μm und 10% Staub'},
    'Martian glacier, 14000 μm': {'ru': 'Марсианский ледник, 14000 мкм', 'de': 'Mars-Gletschereis, 14000 μm'},
    'Martian glacier, 14000 μm and 0.01% dust': {'ru': 'Марсианский ледник 14000 мкм и 0,01% пыли', 'de': 'Mars-Gletschereis, 14000 μm und 0,01% Staub'},
    'Martian glacier, 14000 μm and 0.1% dust': {'ru': 'Марсианский ледник, 14000 мкм и 0,1% пыли', 'de': 'Mars-Gletschereis, 14000 μm und 0,1% Staub'},
    'Martian glacier, 14000 μm and 1% dust': {'ru': 'Марсианский ледник, 14000 мкм и 1% пыли', 'de': 'Mars-Gletschereis, 14000 μm und 1% Staub'},
    'Martian glacier, 14000 μm and 10% dust': {'ru': 'Марсианский ледник, 14000 мкм и 10% пыли', 'de': 'Mars-Gletschereis, 14000 μm und 10% Staub'},
    'Solid methane': {'ru': 'Твёрдый метан', 'de': 'Festes Methan'},
    'Liquid methane': {'ru': 'Жидкий метан', 'de': 'Flüssiges Methan'},
    # Other
    'Equal-energy spectrum': {'ru': 'Плоский спектр', 'de': 'Homogenes Energiespektrum'}
}

# Sort in key length descending order to prevent nested word errors
names = dict(sorted(names.items(), key=lambda x: len(x[0]), reverse=True))


# Notes localization
notes = {
    'km': {'ru': 'км'},
    'Spectrum': {'ru': 'Спектр', 'de': 'Sprektrum'},
    'Photometry': {'ru': 'Фотометрия', 'de': 'Fotometrie'},
    'Synthetic spectrum': {'ru': 'Синтетический спектр', 'de': 'Synthetisches Sprektrum'},
    'Composite spectrum': {'ru': 'Композитный спектр', 'de': 'Zusammengesetztes Spektrum'},
    'With companion': {'ru': 'С компаньоном', 'de': 'Mit Begleiter'},
    'With interstellar dust extinction': {'ru': 'С межзвёздным поглощением пылью', 'de': 'Mit Extinktion durch interstellaren Staub'},
    'Surface': {'ru': 'Поверхность', 'de': 'Oberfläche'},
    'Phase angle': {'ru': 'Фазовый угол', 'de': 'Phasenwinkel'},
    'Maximum': {'ru': 'Максимум'},
    'Minimum': {'ru': 'Минимум'},
    'Bright spots': {'ru': 'Яркие пятна', 'de': 'Helle Flecken'},
    'Bright areas': {'ru': 'Яркие участки', 'de': 'Helle Regionen'},
    'Dark areas': {'ru': 'Тёмные участки', 'de': 'Dunkle Regionen'},
    'Dark boulder terrain': {'ru': 'Тёмные валуны', 'de': 'Terrain dunkler Felsbrocken'},
    'Red impact crater': {'ru': 'Красный кратер', 'de': 'Roter Einschlagkrater'},
    # 'Red blotch': {'ru': 'Красное пятно', 'de': 'Roter Fleck'}, # Gleti on Nix
    'Unresolved photometry': {'ru': 'Неразрешённая фотометрия', 'de': 'Unaufgelöste Photometrie'}, # Dark Red Spot on Haumea
    '25% of maximum cross-section': {'ru': '25% от максимального поперечного сечения', 'de': '25% des maximalen Querschnitts'},
    'Bright polar cap': {'ru': 'Яркая полярная шапка', 'de': 'Helle Polkappe'},
    'Dark polar cap': {'ru': 'Тёмная полярная шапка', 'de': 'Dunkle Polkappe'},
    'Polar region': {'ru': 'Полярный регион', 'de': 'Polargebiet'},
    'Frost band': {'ru': 'Полоса мерзлоты', 'de': 'Frost-Band'},
    'Anomalous scattering region': {'ru': 'Регион с аномальным рассеянием', 'de': 'Anomale Streuungsregion'},
    'Near side': {'ru': 'Видимая сторона', 'de': 'Erdzugewandte Seite'},
    'Far side': {'ru': 'Обратная сторона', 'de': 'Erdabgewandte Seite'},
    'Leading side': {'ru': 'Ведущая сторона', 'de': 'Führende Seite'},
    'Trailing side': {'ru': 'Ведомая сторона', 'de': 'Folgende Seite'},
    'Leading hemisphere': {'ru': 'Ведущее полушарие', 'de': 'Führende Hemisphäre'},
    'Trailing hemisphere': {'ru': 'Ведомое полушарие', 'de': 'Folgende Hemisphäre'},
    'Northwest midplane': {'ru': 'Северно-западная полуплоскость', 'de': 'Nordwestliche Mittelebene'},
    'Southeast midplane': {'ru': 'Южно-восточная полуплоскость', 'de': 'Südöstliche Mittelebene'},
    'Northern part': {'ru': 'Северная часть', 'de': 'Nördlicher Teil'},
    'Eastern part': {'ru': 'Восточная часть', 'de': 'Östlicher Teil'},
    'West': {'ru': 'к западу', 'de': 'West'},
    'East': {'ru': 'к востоку', 'de': 'Ost'},
    'Red': {'ru': 'Красные', 'de': 'Rote'},
    'Less-red': {'ru': 'Менее красные', 'de': 'Weniger rote'},
    'Gray': {'ru': 'Серые', 'de': 'Graue'},
    'Active': {'ru': 'Активные', 'de': 'Aktive'},
    'Inactive': {'ru': 'Неактивные', 'de': 'Inaktive'},
    'Greek camp': {'ru': 'Греки', 'de': 'Griechisches Lager'},
    'Trojan camp': {'ru': 'Троянцы', 'de': 'Trojanisches Lager'},
    'Jupiter family': {'ru': 'Семейства Юпитера', 'de': 'Jupiter Familie'},
    'Jupiter family, active': {'ru': 'Семейства Юпитера, активные', 'de': 'Jupiter Familie, aktive'},
    'Short-period': {'ru': 'Короткопериодические', 'de': 'Kurzperiodisch'},
    'Long-period': {'ru': 'Долгопериодические', 'de': 'Langperiodisch'},
    'Long-period, active': {'ru': 'Долгопериодические, активные', 'de': 'Langperiodisch, aktive'},
    'Hot, inner objects': {'ru': 'Тёплые, внутренние объекты', 'de': 'Heiße, innere Objekte'},
    'Cold, outer objects': {'ru': 'Холодные, внешние объекты', 'de': 'Kalte, äußere Objekte'},
    'Weighted mean': {'ru': 'Взвешенное среднее', 'de': 'Gewichteter Durchschnitt'},
    'Upper limit albedo': {'ru': 'Верхний предел альбедо', 'de': 'Obergrenze Albedo'},
    'Near the aphelion': {'ru': 'Вблизи афелия', 'de': 'In der Nähe des Aphels'},
    'Venera 9': {'ru': 'Венера-9'},
    'Venera 10': {'ru': 'Венера-10'},
    'Venera 11': {'ru': 'Венера-11'},
    'Venera 13': {'ru': 'Венера-13'},
    'Venera 14': {'ru': 'Венера-14'},
    'Archean': {'ru': 'Архей', 'de': 'Archaikum'},
    'Proterozoic': {'ru': 'Протерозой', 'de': 'Proterozoikum'},
    'Deserted land': {'ru': 'Безрастительная земля', 'de': 'Vegetationslose Fläche'},
    'Vegetated land': {'ru': 'Растительный покров', 'de': 'Bewachsene Fläche'},
    'Highlands': {'ru': 'Материки', 'de': 'Hochland'},
    'Maria': {'ru': 'Моря', 'de': 'Maria'},
    "Chang'e-3 Landing Site": {'ru': 'Место посадки Чанъэ-3', 'de': "Chang'e-3 Landestelle"},
    'Fragment 73P-C': {'ru': 'Фрагмент 73P-C', 'de': 'Fragment 73P-C'},
    'Nucleus': {'ru': 'Ядро', 'de': 'Kern'},
    'Tail': {'ru': 'Хвост', 'de': 'Schweif'},
    'Coma': {'ru': 'Кома', 'de': 'Koma'},
    'Inner coma': {'ru': 'Внутренняя кома', 'de': 'Innere Koma'},
    'Outer coma': {'ru': 'Внешняя кома', 'de': 'Äußere Koma'},
    'Extended coma': {'ru': 'Расширенная кома', 'de': 'Erweiterte Koma'},
    'Coma particles dominated': {'ru': 'Преобладают частицы комы', 'de': 'Koma-Teilchen dominieren'},
    'Dust ejecta': {'ru': 'Пылевой выброс', 'de': 'Staubexplosionen'},
    'Pre-outburst': {'ru': 'Перед выбросом', 'de': 'Vor dem Ausbruch'},
    'Post-outburst': {'ru': 'После выброса', 'de': 'Nach dem Ausbruch'},
    'High aurora': {'ru': 'Высотные сияния', 'de': 'Hohe Aurora'},
    'Brightest aurora': {'ru': 'Ярчайшие сияния', 'de': 'Hellste Aurora'},
    'Deep aurora': {'ru': 'Глубокие сияния', 'de': 'Tiefe Aurora'},
    'Knot': {'ru': 'Узел', 'de': 'Knoten'},
    'Amorphous water ice': {'ru': 'Аморфный водяной лед', 'de': 'Amorphes Wassereis'},
    'Crystallized water ice': {'ru': 'Кристаллизованный водяной лед', 'de': 'Kristallisiertes Wassereis'},
    'Porous grains model': {'ru': 'Модель полых зёрен', 'de': 'Poröse Körner-Modell'},
    'Compact grains model': {'ru': 'Модель компактных зёрен', 'de': 'Kompakte Körner-Modell'},
    'Pyroxene': {'ru': 'Пироксен'},
    'Solid methane': {'ru': 'Твёрдый метан', 'de': 'Festes Methan'},
    'Liquid methane': {'ru': 'Жидкий метан', 'de': 'Flüssiges Methan'},
    'Nitrogen type': {'ru': 'Азотный тип', 'de': 'WN-Typ'}, # Wolf-Rayet stars
    'Carbon type': {'ru': 'Углеродный тип', 'de': 'WC-Typ'},
    'Hydrogen emission lines dominating': {'ru': 'Доминирование эмиссионных линий водорода', 'de': 'Wasserstoff-Emissionslinien dominieren'},
    'Strong forbidden emission lines': {'ru': 'Сильные запрещённые эмиссионные линии', 'de': 'Starke verbotene Emissionslinien'},
    'January': {'ru': 'Январь', 'de': 'Januar'},
    'February': {'ru': 'Февраль', 'de': 'Februar'},
    'March': {'ru': 'Март', 'de': 'März'},
    'April': {'ru': 'Апрель', 'de': 'April'},
    'May': {'ru': 'Май', 'de': 'Mai'},
    'June': {'ru': 'Июнь', 'de': 'Juni'},
    'July': {'ru': 'Июль', 'de': 'Juli'},
    'August': {'ru': 'Август', 'de': 'August'},
    'September': {'ru': 'Сентябрь', 'de': 'September'},
    'October': {'ru': 'Октябрь', 'de': 'Oktober'},
    'November': {'ru': 'Ноябрь', 'de': 'November'},
    'December': {'ru': 'Декабрь', 'de': 'Dezember'},
}

# Sort in key length descending order to prevent nested word errors
notes = dict(sorted(notes.items(), key=lambda x: len(x[0]), reverse=True))
