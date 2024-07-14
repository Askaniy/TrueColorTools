"""
Support of the database of JSON5 files and filters profiles.
Describes the object name data storage class.
"""

from typing import Sequence
from json5 import load as json5load
from pathlib import Path
from functools import lru_cache
from traceback import format_exc
import src.strings as tr


class ObjectName:
    """
    Class to work with a (celestial object) name.
    It parses the original string (raw_name) and stores the components:
    - index
    - name(lang)
    - note(lang)
    - info
    - reference
    """

    def __init__(self, name: str):
        """
        Initializes the ObjectName with name parsing.
        The template is `(index) name: note (info) | reference`.
        """
        self.raw_name = name
        self.index = self._note_en = self.info = self.reference = None
        if '|' in name:
            name, reference = name.split('|')
            self.reference = reference.strip()
        if name[0] == '(': # minor body index or something else
            index, name = name.split(')', 1)
            self.index = index[1:].strip()
        elif '/' in name: # comet name
            index, name = name.split('/', 1)
            self.index = index.strip() + '/'
        if '(' in name: # stellar spectral type or something else
            name, info = name.split('(', 1)
            self.info = info.split(')', 1)[0].strip()
        if ':' in name:
            name, note = name.split(':', 1)
            self._note_en = note.strip()
        self._name_en = name.strip()
    
    def name(self, lang: str = 'en'):
        """ Returns the name in the specified language """
        return self._name_en if lang == 'en' else self.translate(self._name_en, tr.names, lang)
    
    def note(self, lang: str = 'en'):
        """ Returns the note in the specified language """
        if self._note_en:
            return self._note_en if lang == 'en' else self.translate(self._note_en, tr.notes, lang)
        else:
            return None
    
    def indexed_name(self, lang: str = 'en'):
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

    @lru_cache(maxsize=None)
    def __call__(self, lang: str = 'en') -> str:
        """ Returns a string composed of the available attributes """
        name = self.indexed_name(lang)
        if self._note_en:
            name = f'{name}: {self.note(lang)}'
        if self.info:
            name = f'{name} ({self.info})'
        if self.reference:
            name = f'{name} [{self.reference}]'
        return name
    
    @staticmethod
    def translate(target: str, translations: dict[str, dict[str, str]], lang: str) -> str:
        """ Searches part of the target string to be translated and replaces it with translation """
        for original, translation in translations.items():
            if target.startswith(original) or target.endswith(original) or original in target.split():
                target = target.replace(original, translation[lang])
                break
        return target

    @staticmethod
    def convert_if_needed(input):
        """ Guaranteed to return an object of the given class, even if the input may have already been one """
        return input if isinstance(input, ObjectName) else ObjectName(input)

    def __hash__(self):
        """ Returns the hash value of the object """
        return hash(self.raw_name)

    def __eq__(self, other):
        """ Checks equality with another ObjectName instance """
        if isinstance(other, ObjectName):
            return self.raw_name == other.raw_name
        return False


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

def is_tag_in_obj(tag: str, obj_tags: Sequence[str]) -> bool:
    """ Search for a tag in a list that handles subcategories """
    tag = set(tag.split('/'))
    for obj_tag in obj_tags:
        if tag.issubset(obj_tag.split('/')):
            return True
    return False

def obj_names_dict(database: dict[ObjectName, dict[str]], tag: str, lang: str) -> dict[str, ObjectName]:
    """ Matches the front-end names with the ObjectName for the selected tag """
    names = {}
    for obj_name, obj_data in database.items():
        if tag == 'ALL' or is_tag_in_obj(tag, obj_data['tags']):
            names |= {obj_name(lang): obj_name}
    return names

def obj_names_list(database: dict[ObjectName, dict[str]], tag: str) -> list[ObjectName]:
    """ Lists the names of eligible objects """
    names = []
    for obj_name, obj_data in database.items():
        if tag == 'ALL' or is_tag_in_obj(tag, obj_data['tags']):
            names.append(obj_name)
    return names

def tag_list(database: dict[ObjectName, dict[str]]) -> list[str]:
    """
    Generates a list of tags found in the spectra database.
    Tags can be written as `A/B/C`, which reads as {A, A/B, A/B/C}.
    """
    tag_set = set(['ALL'])
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

def list_filters():
    """ Returns list of file names were found in the filters folder """
    files = sorted(Path('filters').glob('*.*'))
    return tuple(file.stem for file in files)

class FilterNotFoundError(Exception):
    pass

def find_filter(name: str):
    """ Returns the qualified file name with the required filter profile """
    try:
        return str(next(Path('filters').glob(f'{name}.*')))
    except StopIteration:
        raise FilterNotFoundError