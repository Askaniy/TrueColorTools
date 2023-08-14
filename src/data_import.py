from pathlib import Path
from astropy.io import fits
from astropy.table import Table
import astropy.units as u
import json5
import traceback
import numpy as np
import src.strings as tr


# Units of spectral flux density by wavelength and frequency
flam = u.def_unit('flam', (u.erg / u.s) / (u.cm**2 * u.AA))
#FNU = u.def_unit('fnu', (u.erg / u.s) / (u.cm**2 * u.Hz))
flux_density_SI = u.def_unit('W / (m² nm)', u.W / u.m**2 / u.nm)

def str2unit(string: str, br: bool):
    """ Simple unit parser for FITS files """
    string = string.lower()
    if br: # spectral flux density
        if string == 'flam':
            unit = flam
        else:
            unit = flux_density_SI
    else:
        if string in ('a', 'angstroms'):
            unit = u.AA
        else:
            unit = u.nm
    return unit


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

def txt_reader(file: str):
    """ Imports spectrum data from a simple text file. Wavelength only in angstroms """
    with open(file) as f:
        angstrom, response = np.loadtxt(f).transpose()
    return angstrom/10, response

def fits_reader(file: str):
    """ Imports spectrum data from FITS file in standards of CALSPEC, VizeR, etc """
    with fits.open(file) as hdul:
        #hdul.info()
        columns = hdul[1].columns # most likely the second HDU contains data
        tbl = Table(hdul[1].data)
        x = tbl[columns[0].name] * str2unit(columns[0].unit, br=False)
        y = tbl[columns[1].name] * str2unit(columns[1].unit, br=True)
    return x.to(u.nm), y.to(flux_density_SI)

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
            if '|' in raw_name:
                new_name, source = raw_name.split('|', -1)
            else:
                new_name, source = raw_name, ''
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
                    if new_name.startswith(obj_name) or new_name.endswith(obj_name):
                        new_name = new_name.replace(obj_name, translation[lang])
                        break
                new_name = index + new_name
            new_name = new_name if source == '' else f'{new_name} [{source}]'
            names |= {new_name: raw_name}
    return names

def tag_list(database: dict):
    """ Generates a list of tags found in the spectra database """
    tag_set = set(['all'])
    for obj_data in database.values():
        if 'tags' in obj_data:
            tag_set.update(obj_data['tags'])
    return sorted(tag_set)