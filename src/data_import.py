from pathlib import Path
import json5
import traceback
import numpy as np
import src.core as core
import src.strings as tr


# Support of filters database provided by Filter Profile Service
# http://svo2.cab.inta-csic.es/svo/theory/fps3/index.php

def list_filters():
    """ Returns list of file names were found in the filters folder """
    filters = []
    try:
        for file in Path('filters').iterdir():
            if file.suffix == '.dat' and not file.is_dir():
                filters.append(file.stem)
    except FileNotFoundError:
        print(f'The database in folder "filters" was not found and will not be loaded.')
        print(f'More precisely, {traceback.format_exc(limit=0)}')
    return sorted(filters)


# Support of database extension via json5 files

def import_DBs(folders: list):
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
    try:
        for file in sorted(Path(folder).iterdir()):
            if file.suffix == '.json5' and not file.is_dir():
                with open(file) as f:
                    try:
                        content = json5.load(f)
                        for key, value in content.items():
                            if type(value) == list:
                                refs |= {key: value}
                            else:
                                objects |= {key: value}
                    except ValueError:
                        print(f'Error in JSON5 syntax of file "{file.name}", its upload was cancelled.')
                        print(f'More precisely, {traceback.format_exc(limit=0)}')
    except FileNotFoundError:
        print(f'The database in folder "{folder}" was not found and will not be loaded.')
        print(f'More precisely, {traceback.format_exc(limit=0)}')
    return objects, refs


# Front-end view on spectra database

def obj_dict(database: dict, tag: str, lang: str):
    """ Maps front-end spectrum names allowed by the tag to names in the database """
    names = {}
    for raw_name, obj_data in database.items():
        if tag == 'all':
            flag = True
        else:
            try:
                flag = tag in obj_data['tags']
            except KeyError:
                flag = False
        if flag:
            new_name = '{} [{}]'.format(*raw_name.split('|')) if '|' in raw_name else raw_name
            if lang != 'en': # parsing and translating
                index = ''
                if new_name[0] == '(': # minor body index or stellar spectral type parsing
                    parts = new_name.split(')', 1)
                    index = parts[0] + ') '
                    new_name = parts[1].strip()
                elif '/' in new_name: # comet name parsing
                    parts = new_name.split('/', 1)
                    index = parts[0] + '/'
                    new_name = parts[1].strip()
                for obj_name, translation in tr.names.items():
                    if new_name.startswith(obj_name):
                        new_name = new_name.replace(obj_name, translation[lang])
                        break
                new_name = index + new_name
            names |= {new_name: raw_name}
    return names

def tag_list(database: dict):
    """ Generates a list of tags found in the spectra database """
    tag_set = set(['all'])
    for obj_data in database.values():
        if 'tags' in obj_data:
            tag_set.update(obj_data['tags'])
    return sorted(tag_set)