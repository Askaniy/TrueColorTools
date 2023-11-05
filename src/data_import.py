from pathlib import Path
from traceback import format_exc
from json5 import load as json5load
from astropy.io import fits
from astropy.table import Table
import astropy.units as u
import numpy as np
import src.strings as tr


# FITS spectrum reader

# Units of spectral flux density by wavelength and frequency
flam = u.def_unit('FLAM', (u.erg / u.s) / (u.cm**2 * u.AA))
#FNU = u.def_unit('fnu', (u.erg / u.s) / (u.cm**2 * u.Hz))
flux_density_SI = u.def_unit('W / (m² nm)', u.W / u.m**2 / u.nm)

def str2unit(string: str, axis: str):
    """ Simple unit parser for FITS files """
    string = string.upper()
    if axis == 'x':
        if string in ('A', 'ANGSTROM', 'ANGSTROMS'):
            unit = u.AA
        else:
            unit = u.nm
    else:
        if string == 'FLAM':
            unit = flam
        elif string == '10**(-16)erg.cm**(-2).s**(-1).angstrom**(-1)':
            unit = 10e-16 * flam # used in UVES data example
        else:
            unit = flux_density_SI
    return unit

x_names = {'WAVELENGTH', 'WAVE', 'LAMBDA'}
y_names = {'FLUX'}

def search_column(names: list[str], axis: str):
    """ Returns the index of the FITS column of interest """
    names = [name.upper() for name in names]
    names_set = set(names)
    if axis == 'x':
        candidates = names_set & x_names
    else:
        candidates = names_set & y_names
    try:
        return names.index(list(candidates)[0])
    except IndexError:
        return 0 if axis == 'x' else 1 # by default the first column is wavelength, the second is flux

def header_printer(header):
    """ Wrap lines for readable output to the console """
    n = 80
    print([header[i:i+n]+'\n' for i in range(0, len(header), n)])

def fits_reader(file: str):
    """ Imports spectrum data from FITS file in standards of CALSPEC, VizeR, UVES, BAAVSS, etc """
    with fits.open(file) as hdul:
        #hdul.info()
        try:
            columns = hdul[1].columns # most likely the second HDU contains data
            #print(columns.names)
            #print(columns.units)
            tbl = Table(hdul[1].data)
            x_id = search_column(columns.names, 'x')
            y_id = search_column(columns.names, 'y')
            x_column = tbl[columns[x_id].name]
            y_column = tbl[columns[y_id].name]
            if len(x_column.shape) > 1:
                x_column = x_column[0]
            if len(y_column.shape) > 1:
                y_column = y_column[0]
            x = x_column * str2unit(columns[x_id].unit, 'x')
            y = y_column * str2unit(columns[y_id].unit, 'y')
            return x.to(u.nm), y.to(flux_density_SI)
        except IndexError:
            header = hdul[0].header # but sometimes they are in the primary HDU, like in BAAVSS
            #header_printer(header)
            x_column = header['CRVAL1'] + header['CDELT1']*(np.arange(header['NAXIS1'])-1)
            x = x_column * str2unit(header['CUNIT1'], 'x')
            y = list(Table(hdul[0].data)[0])
            return x.to(u.nm), y

def txt_reader(file: str):
    """ Imports spectrum data from a simple text file. Wavelength only in angstroms """
    with open(file, 'rt', encoding='UTF-8') as f:
        angstrom, response = np.loadtxt(f).transpose()
    return angstrom/10, response


# Support of filters database provided by Filter Profile Service
# http://svo2.cab.inta-csic.es/svo/theory/fps3/index.php

def list_filters():
    """ Returns list of file names were found in the filters folder """
    files = sorted(Path('filters').glob('*.dat'))
    return tuple(file.stem for file in files)


# Support of database extension via JSON5 files

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
    files = sorted(Path(folder).glob('**/*.json5'))
    for file in files:
        with open(file, 'rt', encoding='UTF-8') as f:
            try:
                content = json5load(f)
                for key, value in content.items():
                    if type(value) == list:
                        refs |= {key: value}
                    else:
                        objects |= {key: value}
            except ValueError:
                print(f'Error in JSON5 syntax of file "{file.name}", its upload was cancelled.')
                print(f'More precisely, {format_exc(limit=0)}')
    return objects, refs


# Front-end view on spectra database

def obj_dict(database: dict, tag: str, lang: str):
    """ Maps front-end spectrum names allowed by the tag to names in the database """
    names = {}
    for raw_name, obj_data in database.items():
        if tag == '_all_':
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
                    if new_name.startswith(obj_name) or obj_name in new_name.split():
                        new_name = new_name.replace(obj_name, translation[lang])
                        break
                new_name = index + new_name
            new_name = new_name if source == '' else f'{new_name} [{source}]'
            names |= {new_name: raw_name}
    return names

def tag_list(database: dict):
    """ Generates a list of tags found in the spectra database """
    tag_set = set(['_all_'])
    for obj_data in database.values():
        if 'tags' in obj_data:
            tag_set.update(obj_data['tags'])
    return sorted(tag_set)
