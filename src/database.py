"""
Support of the database of JSON5 files and filters profiles.
Describes the object name data storage class.
"""

from typing import Sequence
from json5 import load as json5load
from pathlib import Path
from traceback import format_exc

from src.core import ObjectName


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
        searched = searched.lower()
        for obj_name in database.keys():
            if searched in obj_name.indexed_name(lang).lower() or searched in obj_name.info(lang).lower():
                names |= {obj_name(lang): obj_name}
    return names

# TODO: delete this funtion, and give `tab1_displayed_namesDB` to `generate_table()` instead of tag
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
