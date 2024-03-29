""" Responsible for converting measurement data into a working form. """

from pathlib import Path
from traceback import format_exc
from json5 import load as json5load
from astropy.io import fits
from astropy.table import Table
import astropy.units as u
import numpy as np

# Disabling warnings about supplier non-compliance with FITS unit storage standards
from warnings import filterwarnings
filterwarnings(action='ignore', category=u.UnitsWarning, append=True)


# Units of spectral flux density by wavelength and frequency
flam = u.def_unit('FLAM', (u.erg / u.s) / (u.cm**2 * u.AA))
fnu = u.def_unit('FNU', (u.erg / u.s) / (u.cm**2 * u.Hz))
u.add_enabled_units((flam, fnu))
u.add_enabled_aliases({'ANGSTROMS': u.Angstrom})
flux_density_SI = u.W / u.m**2 / u.nm


# Support of filters database provided by Filter Profile Service
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


supported_extensions = ('txt', 'dat', 'fits', 'fit')

def file_reader(file: str) -> tuple[np.ndarray, None]:
    """
    Gets the file path within the TCT main folder (text or FITS) and returns the spectrum points (nm, br, sd).
    The internal measurement standards are nanometers and energy spectral density ("energy counter").
    For FITS files, it will try to determine the wavelength unit from internal data.
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

def txt_reader(file: str, type_info: str) -> tuple[np.ndarray, None]:
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
            sd = data[2]
        except IndexError:
            sd = None
    return nm*to_nm_factor, br, sd

def fits_reader(file: str, type_info: str) -> tuple[np.ndarray, None]:
    """ Imports spectral data from a FITS file in standards of CALSPEC, VizeR, UVES, BAAVSS, etc """
    if 'n' in type_info:
        wl_unit = u.nm
    elif 'a' in type_info:
        wl_unit = u.Angstrom
    elif 'u' in type_info:
        wl_unit = u.micron
    else:
        wl_unit = None
    with fits.open(file) as hdul:
        #hdul.info()
        #print(repr(hdul[0].header))
        if len(hdul) >= 2 and len(columns := hdul[1].columns) >= 2: # most likely the second HDU contains data
            #print(columns.names)
            #print(columns.units)
            tbl = Table(hdul[1].data)
            # Getting wavelength data
            wl_id = search_column(columns.names, 'wl')
            wl = tbl[columns[wl_id].name]
            if len(wl.shape) > 1:
                wl = wl[0]
            # Getting flux data
            br_id = search_column(columns.names, 'br')
            br = tbl[columns[br_id].name]
            if len(br.shape) > 1:
                br = br[0]
            # Standard deviation getting attempt
            if len(columns) > 2:
                sd_id = search_column(columns.names, 'sd')
                sd = tbl[columns[sd_id].name]
                if len(sd.shape) > 1:
                    sd = sd[0]
            else:
                sd = None
            # Standardization of units of measurement
            if wl_unit is None:
                wl_unit = u.Unit(columns[wl_id].unit)
            nm = (wl * wl_unit).to(u.nm)
            br = (br * u.Unit(columns[br_id].unit)).to(flux_density_SI)
            if sd is not None:
                sd = (sd * u.Unit(columns[sd_id].unit)).to(flux_density_SI)
        else:
            header = hdul[0].header # but sometimes they are in the primary HDU, like in BAAVSS
            wl = header['CRVAL1'] + header['CDELT1']*(np.arange(header['NAXIS1'])-1)
            if wl_unit is None:
                wl_unit = u.Unit(header['CUNIT1'])
            nm = (wl * wl_unit).to(u.nm)
            br = list(Table(hdul[0].data)[0])
    nm = np.array(nm)
    br = np.array(br)
    if sd is not None:
        sd = np.array(sd)
    return nm, br, sd

def search_column(names: list[str], target: str):
    """ Returns the index of the FITS column of interest """
    names = [name.lower() for name in names]
    names_set = set(names)
    match target:
        case 'wl':
            candidates = names_set & {'wavelength', 'wave', 'lambda'}
        case 'br':
            candidates = names_set & {'flux'}
        case 'sd':
            candidates = names_set & {'syserror'}
    try:
        return names.index(list(candidates)[0])
    except IndexError:
        match target:
            case 'wl':
                return 0 # by default the first column is wavelength
            case 'br':
                return 1 # the second is flux
            case 'sd':
                return 2 # the third is standard deviation


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
