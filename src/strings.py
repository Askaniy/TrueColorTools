""" Localization file, contains almost all the strings used """

# Window
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
    'en': ['Database viewer', 'Image processing', 'Blackbody & Redshifts'],
    'ru': ['Просмотр базы спектров', 'Обработка изображений', 'АЧТ и красные смещения'],
    'de': ['Datenbank-Viewer', 'Bildverarbeitung', 'Schwarzkörper & Rotverschiebung']
}
gui_menu = {
    'en': [['File', [gui_ref['en'], gui_info['en'], gui_exit['en']]], ['Language', lang_list['en']]],
    'ru': [['Файл', [gui_ref['ru'], gui_info['ru'], gui_exit['ru']]], ['Язык', lang_list['ru']]],
    'de': [['Datei', [gui_ref['de'], gui_info['de'], gui_exit['de']]], ['Sprache', lang_list['de']]],
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
gui_br = {
    'en': ['Brightness mode', 'chromaticity', 'geometric albedo', 'spherical albedo'],
    'ru': ['Режим яркости', 'цветность', 'геом. альбедо', 'сфер. альбедо'],
    'de': ['Helligkeitsmodus', 'Farbton', 'geometrische Albedo', 'sphärische Albedo']
}
gui_interp = {
    'en': ['Interpolator/extrapolator', 'old', 'new'],
    'ru': ['Интер/экстраполятор', 'старый', 'новый'],
    'de': ['Interpolation/Extrapolation', 'alt', 'neu']
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
gui_estimated = {
    'en': 'Note: The albedo is estimated.',
    'ru': 'Прим.: Данное альбедо — теор. оценка',
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
    'de': 'Zeigen Sie das Diagramm'
}
gui_pin = {
    'en': 'Pin the spectrum',
    'ru': 'Закрепить спектр',
    'de': 'Das Spektrum festhalten'
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
    'de': 'Kategorie in Text exportieren'
}
gui_export2table = {
    'en': 'Export category to table',
    'ru': 'Экспортировать в таблицу',
    'de': 'Kategorie in Tabelle exportieren'
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
    'de': ['Farbtafel der Kategory „', '“']
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
info_sRGB = {
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
#gui_brightness = {
#    'en': 'Brightness',
#    'ru': 'Яркость',
#    'de': 'Helligkeit'
#}
gui_desun = {
    'en': 'Remove Sun as emitter',
    'ru': 'Убрать отражённый спектр Солнца',
    'de': 'Sonne als Emitter entfernen'
}
gui_photons = {
    'en': 'Photon spectral density',
    'ru': 'Спектральная плотность фотонов',
    'de': 'Photonensprektraldichte'
}
#gui_autoalign = {
#    'en': 'Align image bands (β)',
#    'ru': 'Совместить изображения (β)',
#    'de': 'Bildbänder ausrichten (β)'
#}
gui_makebright = {
    'en': 'Maximize brightness',
    'ru': 'Максимизировать яркость',
    'de': 'Helligkeit maximieren'
}
gui_factor = {
    'en': 'Brightness factor',
    'ru': 'Множитель яркости',
    'de': 'Helligkeitsfaktor'
}
gui_enlarge = {
    'en': 'Enlarge small images',
    'ru': 'Увеличить небольшие изображения',
    'de': 'Kleine Bilder vergrößern'
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
gui_overexposure = {
    'en': 'Adjust overexposure limit',
    'ru': 'Регулировать предел переэкспонирования',
    'de': 'Überbelichtungslimit anpassen'
}
gui_mag = {
    'en': 'App. magnitude*',
    'ru': 'Вид. зв. величина*',
    'de': 'scheinb. Helligkeit*'
}
gui_explanation = {
    'en': '* if the Solar disk in the sky is replaced by this blackbody sphere',
    'ru': '* если диск Солнца на небе заменить данной чёрнотельной сферой',
    'de': '* wenn die Sonne am Taghimmel durch einen Schwarzkörper ersetzt würde'
}

# Plots
spectral_plot = {
    'en': 'Spectral energy density plot',
    'ru': 'График спектральной плотности энергии',
    'de': 'Spektralenergiedichte'
}
light_theme = {
    'en': 'Light theme',
    'ru': 'Светлая тема',
    'de': 'Thema Licht'
}
xaxis_text = {
    'en': 'Wavelength, nm',
    'ru': 'Длина волны, нм',
    'de': 'Wellenlänge, nm'
}
yaxis_text = {
    'en': 'Spectral energy density',
    'ru': 'Спектральная плотность энергии',
    'de': 'Spektralenergiedichte'
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
    'Rings of Saturn': {'ru': 'Кольца Сатурна', 'de': 'Ringe des Saturn'},
    'Mimas': {'ru': 'Мимас', 'de': 'Mimas'},
    'Enceladus': {'ru': 'Энцелад', 'de': 'Enceladus'},
    'Tethys': {'ru': 'Тефия', 'de': 'Tethys'},
    'Dione': {'ru': 'Диона', 'de': 'Dione'},
    'Rhea': {'ru': 'Рея', 'de': 'Rhea'},
    'Titania': {'ru': 'Титания', 'de': 'Titania'},
    'Titan': {'ru': 'Титан', 'de': 'Titan'},
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
    'Rings of Uranus': {'ru': 'Кольца Урана', 'de': 'Ringe des Uranus'},
    'Portia group': {'ru': 'Группа Порции', 'de': 'Portia-Gruppe'},
    'Puck': {'ru': 'Пак', 'de': 'Puck'},
    'Miranda': {'ru': 'Миранда', 'de': 'Miranda'},
    'Ariel': {'ru': 'Ариэль', 'de': 'Ariel'},
    'Umbriel': {'ru': 'Умбриэль', 'de': 'Umbriel'},
    'Oberon': {'ru': 'Оберон', 'de': 'Oberon'},
    # Uranian irregulars
    'Caliban': {'ru': 'Калибан', 'de': 'Caliban'},
    'Sycorax': {'ru': 'Сикоракса', 'de': 'Sycorax'},
    'Prospero': {'ru': 'Просперо', 'de': 'Prospero'},
    'Setebos': {'ru': 'Сетебос', 'de': 'Setebos'},
    'Stephano': {'ru': 'Стефано', 'de': 'Stephano'},
    # Neptunian system
    'Neptune': {'ru': 'Нептун', 'de': 'Neptun'},
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
    'Europa': {'ru': 'Европа', 'de': 'Europa'},
    'Cybele': {'ru': 'Кибела', 'de': 'Cybele'},
    'Sylvia': {'ru': 'Сильвия', 'de': 'Sylvia'},
    'Thisbe': {'ru': 'Фисба', 'de': 'Thisbe'},
    'Antiope': {'ru': 'Антиопа', 'de': 'Antiope'},
    'Minerva': {'ru': 'Минерва', 'de': 'Minerva'},
    'Aurora': {'ru': 'Аврора', 'de': 'Aurora'},
    'Camilla': {'ru': 'Камилла', 'de': 'Camilla'},
    'Hermione': {'ru': 'Гермиона', 'de': 'Hermione'},
    'Elektra': {'ru': 'Электра', 'de': 'Elektra'},
    'Kleopatra': {'ru': 'Клеопатра', 'de': 'Kleopatra'},
    'Ida': {'ru': 'Ида', 'de': 'Ida'},
    'Dactyl': {'ru': 'Дактиль', 'de': 'Dactyl'},
    'Mathilde': {'ru': 'Матильда', 'de': 'Mathilde'},
    'Justitia': {'ru': 'Юстиция', 'de': 'Justitia'},
    'Eros': {'ru': 'Эрос', 'de': 'Eros'},
    'Davida': {'ru': 'Давида', 'de': 'Davida'},
    'Patroclus-Menoetius': {'ru': 'Патрокл-Менетий', 'de': 'Patroclus-Menoetius'},
    'Interamnia': {'ru': 'Интерамния', 'de': 'Interamnia'},
    'Hidalgo': {'ru': 'Идальго', 'de': 'Hidalgo'},
    'Gaspra': {'ru': 'Гаспра', 'de': 'Gaspra'},
    'Ganymed': {'ru': 'Ганимед', 'de': 'Ganymed'},
    'Celestia': {'ru': 'Селестия', 'de': 'Celestia'},
    'Geographos': {'ru': 'Географ', 'de': 'Geographos'},
    'Chiron': {'ru': 'Хирон', 'de': 'Chiron'},
    'Bacchus': {'ru': 'Бахус', 'de': 'Bacchus'},
    'Šteins': {'ru': 'Штейнс', 'de': 'Šteins'},
    'Phaethon': {'ru': 'Фаэтон', 'de': 'Phaethon'},
    'Eurybates': {'ru': 'Эврибат', 'de': 'Eurybates'},
    'Toutatis': {'ru': 'Таутатис', 'de': 'Toutatis'},
    'Pholus': {'ru': 'Фол', 'de': 'Pholus'},
    'Golevka': {'ru': 'Голевка', 'de': 'Golevka'},
    'Braille': {'ru': 'Брайль', 'de': 'Braille'},
    'Chariklo': {'ru': 'Харикло', 'de': 'Chariklo'},
    'Leucus': {'ru': 'Левк', 'de': 'Leucus'},
    'Polymele': {'ru': 'Полимела', 'de': 'Polymele'},
    'Varuna': {'ru': 'Варуна', 'de': 'Varuna'},
    'Orus': {'ru': 'Орус', 'de': 'Orus'},
    'Itokawa': {'ru': 'Итокава', 'de': 'Itokawa'},
    'Ixion': {'ru': 'Иксион', 'de': 'Ixion'},
    'Huya': {'ru': 'Гуйя', 'de': 'Huya'},
    'Lempo': {'ru': 'Лемпо', 'de': 'Lempo'},
    'Quaoar': {'ru': 'Квавар', 'de': 'Quaoar'},
    'Didymos': {'ru': 'Дидим', 'de': 'Didymos'},
    'Sedna': {'ru': 'Седна', 'de': 'Sedna'},
    'Orcus': {'ru': 'Орк', 'de': 'Orcus'},
    'Vanth': {'ru': 'Вант', 'de': 'Vanth'},
    'Bennu': {'ru': 'Бенну', 'de': 'Bennu'},
    'Salacia': {'ru': 'Салация', 'de': 'Salacia'},
    'Pluto': {'ru': 'Плутон', 'de': 'Pluto'},
    'Charon': {'ru': 'Харон', 'de': 'Charon'},
    'Haumea': {'ru': 'Хаумеа', 'de': 'Haumea'},
    'Eris': {'ru': 'Эрида', 'de': 'Eris'},
    'Makemake': {'ru': 'Макемаке', 'de': 'Makemake'},
    'Dinkinesh': {'ru': 'Динкинеш', 'de': 'Dinkinesh'},
    'Ryugu': {'ru': 'Рюгу', 'de': 'Ryugu'},
    'Varda': {'ru': 'Варда', 'de': 'Varda'},
    'Ilmarë': {'ru': 'Ильмарэ', 'de': 'Ilmarë'},
    'Gonggong': {'ru': 'Гунгун', 'de': 'Gonggong'},
    'Xiangliu': {'ru': 'Сянлю', 'de': 'Xiangliu'},
    'Gǃkúnǁʼhòmdímà': {'ru': 'Гкъкунлъ’хомдима', 'de': 'Gǃkúnǁʼhòmdímà'},
    'Gǃòʼé ǃHú': {'ru': 'Гкъо’э Къху', 'de': 'Gǃòʼé ǃHú'},
    'Arrokoth': {'ru': 'Аррокот', 'de': 'Arrokoth'},
    'Halley': {'ru': 'Галлея', 'de': 'Halley'},
    'Churyumov–Gerasimenko': {'ru': 'Чурюмова — Герасименко', 'de': 'Churyumov-Gerasimenko'},
    'Hartley': {'ru': 'Хартли', 'de': 'Hartley'},
    'Hale–Bopp': {'ru': 'Хейла — Боппа', 'de': 'Hale–Bopp'},
    'ʻOumuamua': {'ru': 'Оумуамуа', 'de': 'ʻOumuamua'},
    # Classes
    'Class': {'ru': 'Класс', 'de': 'Spektraltyp'},
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
    'Surface, phase angle': {'ru': 'Поверхность, фазовый угол', 'de': 'Oberfläche, Phasenwinkel'},
    'Surface': {'ru': 'Поверхность', 'de': 'Oberfläche'},
    'Bright areas': {'ru': 'Яркие участки', 'de': 'Helle Regionen'},
    'Dark areas': {'ru': 'Тёмные участки', 'de': 'Dunkle Regionen'},
    'Dark boulder terrain': {'ru': 'Тёмные валуны', 'de': 'Terrain dunkler Felsbrocken'},
    'Near side': {'ru': 'Видимая сторона', 'de': 'Erdzugewandte Seite'},
    'Far side': {'ru': 'Обратная сторона', 'de': 'Erdabgewandte Seite'},
    'Leading hemisphere': {'ru': 'Ведущее полушарие', 'de': 'Führende Hemisphäre'},
    'Trailing hemisphere': {'ru': 'Ведомое полушарие', 'de': 'Folgende Hemisphäre'},
    'Leading side': {'ru': 'Ведущая сторона', 'de': 'Führende Seite'},
    'Trailing side': {'ru': 'Ведомая сторона', 'de': 'Folgende Seite'},
    'Long-period': {'ru': 'Долгопериодические', 'de': 'Langperiodisch'},
    'Short-period': {'ru': 'Короткопериодические', 'de': 'Kurzperiodisch'},
    'Hot, inner objects': {'ru': 'Тёплые, внутренние объекты', 'de': 'Heiße, innere Objekte'},
    'Cold, outer objects': {'ru': 'Холодные, внешние объекты', 'de': 'Kalte, äußere Objekte'},
    'Weighted mean': {'ru': 'Взвешенное среднее', 'de': 'Gewichteter Durchschnitt'},
    'Archean': {'ru': 'Архей', 'de': 'Archaikum'},
    'Proterozoic': {'ru': 'Протерозой', 'de': 'Proterozoikum'},
    "Chang'e-3 Landing Site": {'ru': 'Место посадки Чанъэ-3', 'de': "Chang'e-3 Landestelle"},
    'Wenu Lobus': {'ru': 'Доля Уэну', 'de': 'Wenu Lobus'},
    'Weeyo Lobus': {'ru': 'Доля Уээйо', 'de': 'Weeyo Lobus'},
    'Akasa Linea': {'ru': 'Линия Акаса', 'de': 'Akasa Linea'},
}

# Sort in key length descending order to prevent nested word errors
notes = dict(sorted(notes.items(), key=lambda x: len(x[0]), reverse=True))