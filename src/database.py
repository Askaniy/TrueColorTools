"""
Support of the database of JSON5 files and filters profiles.
Describes the object name data storage class.
"""

from collections.abc import Sequence
from functools import cache
from pathlib import Path
from traceback import format_exc

from json5 import load as json5load

import src.auxiliary as aux
import src.strings as tr


class ObjectName:
    """
    Class to work with a (celestial object) name.
    It parses the original string (raw_name) and stores the components:
    - index
    - name(lang)
    - note(lang)
    - info(lang)
    - reference
    """

    unnamed_count = 0 # class attribute to track the number of unnamed objects

    def __init__(self, raw_input: str = ''):
        """
        Initializes the ObjectName with name parsing.
        The template is `(index) name: note (info) | reference`.
        If no name is specified, a numbered unnamed object will be created.
        """
        self.index = self.reference = ''
        self._note_raw = self._note_en = ''
        self._info_raw = self._info_en = ''
        if raw_input == '':
            ObjectName.unnamed_count += 1
            self.raw_input = ObjectName.unnamed_count
            self._name_raw = self._name_en = f'Unnamed object {ObjectName.unnamed_count}'
        else:
            self.raw_input = raw_input
            name = raw_input.replace('~', ' ')
            # A tilde, as in LaTeX, denotes a (narrow) non-breaking space.
            # It is recommended to use it as a number group separator instead of a period or comma.
            if '|' in name:
                name, reference = name.split('|')
                name = name.strip()
                self.reference = reference.strip()
            if name[0] == '(': # minor body index or something else
                index, name = name.split(')', 1)
                self.index = self.formatting_provisional_designation(index[1:].strip())
            if name[-1] == ')': # stellar spectral type or something else
                info, name = name[::-1].split('(', 1) # getting the last bracket
                name = name[::-1] # reversing back
                self._info_raw = info[::-1].split(')', 1)[0].strip()
                self._info_en = self.formatting_provisional_designation(self._info_raw)
            if ':' in name: # note
                name, note = name.split(':', 1)
                self._note_raw = note.strip()
                self._note_en = self.formatting_provisional_designation(self._note_raw)
            # the last check because "/" may encounter in info or notes:
            if '/' in name and name[name.index('/') - 1] in ('P', 'C', 'I'): # comet name
                index, name = name.split('/', 1)
                self.index = index.strip() + '/'
            self._name_raw = name.strip()
            self._name_en = self.formatting_provisional_designation(self._name_raw)

    def name(self, lang: str = 'en') -> str:
        """ Returns the name in the specified language """
        return self._name_en if lang == 'en' else self.translate(self._name_en, tr.names, lang)

    def note(self, lang: str = 'en') -> str:
        """ Returns the note in the specified language """
        if self._note_en:
            return self._note_en if lang == 'en' else self.translate(self._note_en, tr.notes, lang)
        else:
            return ''

    def info(self, lang: str = 'en') -> str:
        """ Returns the info in the specified language """
        if self._info_en:
            return self._info_en if lang == 'en' else self.translate(self._info_en, tr.names, lang)
        else:
            return ''

    def indexed_name(self, lang: str = 'en') -> str:
        """ Returns the name with the index in the specified language """
        name = self.name(lang)
        if self.index:
            if self.index[-1] == '/':
                # a comet with a number prefix
                name = f'{self.index}{name}'
            elif '/' in self.index:
                # a comet without a number prefix
                name = f'{self.index} ({name})'
            elif name[:4].isnumeric():
                # index of an unnamed asteroid
                name = f'({self.index}) {name}'
            else:
                name = f'{self.index} {name}'
        return name

    @cache
    def __call__(self, lang: str = 'en') -> str:
        """ Returns a string composed of the available attributes """
        name = self.indexed_name(lang)
        if self._note_en:
            name = f'{name}: {self.note(lang)}'
        if self._info_en:
            name = f'{name} ({self.info(lang)})'
        if self.reference:
            name = f'{name} [{self.reference}]'
        return name

    @staticmethod
    def formatting_provisional_designation(string: str):
        """
        Checks if the string contains a provisional designation and subscripts the last number
        (of previous letter alphabetic cycles).

        See https://www.minorplanetcenter.net/iau/info/DesDoc.html
        """
        words = string.split()
        if len(words) > 1:
            for i, word in enumerate(words):
                if i+1 != len(words) and word[-4:].isnumeric() and word[-4:-2] in ('19', '20'):
                    letters = words[i+1]
                    if 2 < len(letters) < 7 and letters[:2].isalpha() and letters[2:].isnumeric():
                        words[i+1] = letters[:2] + aux.subscript(letters[2:])
        return ' '.join(words)

    @staticmethod
    def translate(target: str, translations: dict[str, dict[str, str]], lang: str) -> str:
        """ Searches part of the target string to be translated and replaces it with translation """
        for original, translation in translations.items():
            if target.startswith(original) or target.endswith(original) or original in target.split():
                if lang in translation:
                    target = target.replace(original, translation[lang])
                break
        return target

    @staticmethod
    def as_ObjectName(name):
        """ Guaranteed to return an object of the given class, even if the input may have already been one """
        if isinstance(name, ObjectName):
            return name
        elif name is None:
            return ObjectName('')
        else:
            return ObjectName(name)

    def __hash__(self) -> int:
        """ Returns the hash value based on the object's raw input """
        return hash(self.raw_input)

    def __eq__(self, other) -> bool:
        """ Checks equality with another ObjectName instance """
        if isinstance(other, ObjectName):
            return self.raw_input == other.raw_input
        return False

    def __str__(self) -> str:
        return self()

    def __repr__(self) -> str:
        output = 'ObjectName('
        if self.index:
            output += f'index={self.index}, '
        if self._name_en:
            output += f'name={self._name_en}, '
        if self._note_en:
            output += f'note={self._note_en}, '
        if self._info_en:
            output += f'info={self._info_en}, '
        if self.reference:
            output += f'reference={self.reference}, '
        return output[:-2] + ')'


# Importing files

def import_DBs(folders: Sequence[str]):
    """ Returns databases of objects and references were found in the given folders """
    objectsDB = {}
    refsDB = {}
    for folder in folders:
        additional_data = import_folder(folder)
        objectsDB |= additional_data[0]
        refsDB |= additional_data[1]
    return objectsDB, refsDB

def import_folder(folder: str):
    """ Returns objects and references were found in the given folder """
    objects = {}
    refs = {}
    files = sorted(Path(folder).glob('**/*.json5'))
    for file in files:
        with open(file, 'rt', encoding='UTF-8') as f:
            try:
                content = json5load(f)
                for key, value in content.items():
                    if type(value) == list:
                        refs |= {key: value}
                    else:
                        objects |= {ObjectName(key): value}
            except ValueError:
                print(f'Error in JSON5 syntax of file "{file.name}", its upload was cancelled.')
                print(f'More precisely, {format_exc(limit=0)}')
    return objects, refs


# Imported database iterators

def is_tag_in_obj(tag: str, obj_data: dict) -> bool:
    """ Search for a tag in a list that handles subcategories """
    if 'tags' in obj_data:
        tag_set = set(tag.split('/'))
        for obj_tag in obj_data['tags']:
            if tag_set.issubset(obj_tag.split('/')):
                return True
    return False

def obj_names_dict(database: dict[ObjectName, dict], tag: str, searched: str, lang: str) -> dict[str, ObjectName]:
    """ Matches the front-end names with the ObjectName for the selected tag """
    names = {}
    if searched == '':
        for obj_name, obj_data in database.items():
            if tag == 'ALL' or is_tag_in_obj(tag, obj_data):
                names |= {obj_name(lang): obj_name}
    else:
        # "Search engine"
        searched = searched.lower()
        for obj_name in database:
            # 1, 2. Search within English name and subscript numbers of provisional designation
            # 3, 4. Search within translated indexed name and additional information
            if searched in obj_name._name_raw.lower() or \
               searched in obj_name._info_raw.lower() or \
               searched in obj_name.indexed_name(lang).lower() or \
               searched in obj_name.info(lang).lower():
                # It fits
                names |= {obj_name(lang): obj_name}
    return names

# TODO: delete this function, and give `tab1_displayed_namesDB` to `generate_table()` instead of tag
def obj_names_list(database: dict[ObjectName, dict], tag: str) -> list[ObjectName]:
    """ Lists the names of eligible objects for color table """
    names = []
    for obj_name, obj_data in database.items():
        if tag == 'ALL' or is_tag_in_obj(tag, obj_data):
            names.append(obj_name)
    return names

def tag_list(database: dict[ObjectName, dict]) -> list[str]:
    """
    Generates a list of tags found in the spectra database.
    Tags can be written as `A/B/C`, which reads as {A, A/B, A/B/C}.
    """
    tag_set = {'ALL'}
    for obj_data in database.values():
        if 'tags' in obj_data:
            for tag in obj_data['tags']:
                tag_set.add(tag)
                if '/' in tag:
                    supertags = []
                    while '/' in tag:
                        supertag, tag = tag.split('/', 1)
                        supertags.append(supertag)
                        tag_set.add('/'.join(supertags))
    return sorted(tag_set)

def notes_list(obj_names: list[ObjectName], lang: str) -> list[str]:
    """ Generates a list of notes found in the spectra database """
    notes = []
    for obj_name in obj_names:
        note = obj_name.note(lang)
        if note and note not in notes:
            notes.append(note)
    return notes


# Support of the filters database provided by Filter Profile Service
# http://svo2.cab.inta-csic.es/svo/theory/fps3/index.php

def list_filters() -> tuple[str, ...]:
    """ Returns list of file names were found in the filters folder """
    files = sorted(Path('filters').glob('*.*'))
    return tuple(file.stem for file in files)
