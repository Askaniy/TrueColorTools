""" Responsible for converting measurement data into a working form. """

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
u.add_enabled_aliases({'flam': flam})
u.add_enabled_aliases({'ANGSTROMS': u.Angstrom})
u.add_enabled_aliases({'angstroms': u.Angstrom})
flux_density_SI = u.W / u.m**2 / u.nm


supported_extensions = ('txt', 'dat', 'fits', 'fit')

def file_reader(file: str) -> tuple[np.ndarray]:
    """
    Gets the file path within the TCT main folder (text or FITS) and returns the spectrum points (nm, br, sd).
    The internal measurement standards are nanometers and energy spectral density ("energy counter").
    For FITS files, it will try to determine the wavelength unit from internal data.
    You can also forcefully specify the data type through letters in the file extension (.txt for example):
    - .txtN for nanometers, .txtA for angstroms, .txtU for micrometers;
    - .txtE for energy counters per wavelength, .txtJ for energy counters per frequency, .txtP for photon counters.
    """
    extension = file.split('.')[-1].lower()
    type_info = extension
    for ext in supported_extensions:
        type_info = type_info.removeprefix(ext)
    if extension.startswith('fit'):
        nm, br, sd = fits_reader(file, type_info)
    else:
        nm, br, sd = txt_reader(file, type_info)
    return nm, br, sd

def txt_reader(file: str, type_info: str) -> tuple[np.ndarray]:
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
        sd = data[2] if data.shape[0] >= 3 else None
        if data.shape[0] >= 4 and 1 in data[3]:
            # SMASS error indication in the 4th column
            mask = data[3] == 1
            nm = nm[mask]
            br = br[mask]
            sd = sd[mask]
    return nm*to_nm_factor, br, sd

def fits_reader(file: str, type_info: str) -> tuple[np.ndarray]:
    """ Imports spectral data from a FITS file in standards of CALSPEC, VizeR, UVES, BAAVSS, etc """
    if 'n' in type_info:
        wl_unit = u.nm
    elif 'a' in type_info:
        wl_unit = u.Angstrom
    elif 'u' in type_info:
        wl_unit = u.micron
    else:
        wl_unit = None
    sd = None
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
            if wl.ndim > 1:
                wl = wl[0]
            # Getting flux data
            br_id = search_column(columns.names, 'br')
            br = tbl[columns[br_id].name]
            match br.ndim:
                case 2:
                    br = br[0]
                case 3:
                    br = br.transpose((0, 2, 1)) # like spectral cube?!
            # Standard deviation getting attempt
            if len(columns) > 2:
                sd_id = search_column(columns.names, 'sd')
                sd = tbl[columns[sd_id].name]
                if len(sd.shape) > 1:
                    sd = sd[0]
            # Standardization of units of measurement
            if wl_unit is None:
                wl_unit = u.Unit(columns[wl_id].unit)
            nm = (wl * wl_unit).to(u.nm)
            br = (br * u.Unit(columns[br_id].unit)).to(flux_density_SI)
            if sd is not None:
                sd = (sd * u.Unit(columns[sd_id].unit)).to(flux_density_SI)
        else:
            try:
                # BAAVSS store wavelength info only in primary HDU
                header = hdul[0].header
                wl = header['CRVAL1'] + header['CDELT1']*(np.arange(header['NAXIS1'])-1)
                if wl_unit is None:
                    wl_unit = u.Unit(header['CUNIT1'])
                nm = (wl * wl_unit).to(u.nm)
                br = list(Table(hdul[0].data)[0])
            except KeyError:
                # IRAF-formatted "multispec" is not supported, there were attempts
                nm = hdul[0].data[0] * 0.1
                br = hdul[0].data[1]
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
            candidates = names_set & {'flux', 'sci'}
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
