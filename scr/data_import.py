from pathlib import Path
from json5 import load
import spectra.core_database as db
import scr.strings as tr


# Support of database extension via json5 files

def import_core_objs() -> dict:
    return db.objects

def import_core_refs() -> dict:
    return db.refs

def import_folder(folder: str) -> tuple:
    objects = {}
    refs = {}
    if Path.cwd().name == 'TrueColorTools':
        for file in Path(folder).iterdir():
            if file.suffix == '.json5' and not file.is_dir():
                with open(file) as f:
                    for key, value in load(f).items():
                        if type(value) == list:
                            refs |= {key: value}
                        else:
                            objects |= {key: value}
    else:
        print(f'Failed to import {folder=}. Please try to launch from "/TrueColorTools" directory.')
    return objects, refs


# Front-end view on spectra database

def obj_dict(database: dict, tag: str, lang: str) -> dict:
    """Maps front-end spectrum names allowed by the tag to names in the database"""
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
                if new_name[0] == '(': # minor body indices parsing
                    parts = new_name.split(')', 1)
                    index = parts[0] + ') '
                    new_name = parts[1].strip()
                elif '/' in new_name: # comet names parsing
                    parts = new_name.split('/', 1)
                    index = parts[0] + '/'
                    new_name = parts[1].strip()
                for obj_name, tranlation in tr.names.items():
                    if new_name.startswith(obj_name):
                        new_name = new_name.replace(obj_name, tranlation[lang])
                        break
                new_name = index + new_name
            names |= {new_name: raw_name}
    return names

def tag_list(database: dict) -> list:
    """Generates a list of tags found in the spectra database"""
    tag_set = set(['all'])
    for obj_data in database.values():
        if 'tags' in obj_data:
            tag_set.update(obj_data['tags'])
    return list(tag_set)