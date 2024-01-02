from pathlib import Path
from traceback import format_exc
from json5 import load as json5load
from astropy.io import fits
from astropy.table import Table
import astropy.units as u
import numpy as np
import src.strings as tr


# Support of filters database provided by Filter Profile Service
# http://svo2.cab.inta-csic.es/svo/theory/fps3/index.php

def list_filters():
    """ Returns list of file names were found in the filters folder """
    files = sorted(Path('filters').glob('*.*'))
    return tuple(file.stem for file in files)

def find_filter(name: str):
    """ Returns the qualified file name with the required filter profile """
    return str(next(Path('filters').glob(f'{name}.*')))


supported_extensions = ('txt', 'dat', 'fits', 'fit')

def file_reader(file: str) -> tuple:
    """
    Gets the file path within the TCT main folder (text or FITS) and returns the spectrum points (nm, br, sd).
    The internal measurement standards are nanometers and energy spectral density ("energy counter").
    For FITS files it will try to determine them from internal data.
    You can also forcefully specify the data type through letters in the file extension (.txt for example):
    - .txtN for nanometers, .txtA for angstroms, .txtU for micrometers;
    - .txtE for energy counters, .txtP for photon counters.
    """
    extension = file.split('.')[-1].lower()
    type_info = extension
    for ext in supported_extensions:
        type_info = type_info.removeprefix(ext)
    if extension.startswith('fit'):
        nm, br, sd = fits_reader(file, type_info)
    else:
        nm, br, sd = txt_reader(file, type_info)
    if 'p' in type_info:
        br /= nm # multiplying by scaled photon energy E=hc/λ
    return nm, br, sd

def txt_reader(file: str, type_info: str) -> tuple:
    """ Imports spectral data from a text file """
    if 'a' in type_info:
        to_nm_factor = 0.1
    elif 'u' in type_info:
        to_nm_factor = 1000
    else:
        to_nm_factor = 1
    with open(file, 'rt', encoding='UTF-8') as f:
        data = np.loadtxt(f).transpose()
        nm = data[0]
        br = data[1]
        try:
            sd = data[3]
        except IndexError:
            sd = np.zeros_like(br)
    return nm*to_nm_factor, br, sd

def fits_reader(file: str, type_info: str):
    """ Imports spectral data from a FITS file in standards of CALSPEC, VizeR, UVES, BAAVSS, etc """
    if 'n' in type_info:
        to_nm_factor = 1
    elif 'a' in type_info:
        to_nm_factor = 0.1
    elif 'u' in type_info:
        to_nm_factor = 1000
    else:
        to_nm_factor = 0 # not stated
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
            if not to_nm_factor:
                to_nm_factor = 0.1 if columns[x_id].unit in angstroms else 1
            y = (y_column * str2unit(columns[y_id].unit)).to(flux_density_SI)
        except IndexError:
            header = hdul[0].header # but sometimes they are in the primary HDU, like in BAAVSS
            #header_printer(header)
            x_column = header['CRVAL1'] + header['CDELT1']*(np.arange(header['NAXIS1'])-1)
            if not to_nm_factor:
                to_nm_factor = 0.1 if header['CUNIT1'] in angstroms else 1
            y = list(Table(hdul[0].data)[0])
    x = x_column * to_nm_factor
    y = np.array(y)
    return x, y, np.zeros_like(y) # TODO: add support for standard deviation

angstroms = ('A', 'ANGSTROM', 'ANGSTROMS')

# Units of spectral flux density by wavelength and frequency
flam = u.def_unit('FLAM', (u.erg / u.s) / (u.cm**2 * u.AA))
#FNU = u.def_unit('fnu', (u.erg / u.s) / (u.cm**2 * u.Hz))
flux_density_SI = u.def_unit('W / (m² nm)', u.W / u.m**2 / u.nm)

def str2unit(string: str):
    """ Simple unit parser for FITS files """
    string = string.upper()
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
