""" Responsible for converting measurement data into a working form. """

# Disabling warnings about supplier non-compliance with FITS unit storage standards
from collections.abc import Sequence
from typing import Any, cast
from warnings import filterwarnings

import astropy.units as u
import numpy as np
import numpy.typing as npt
from astropy.io import fits
from astropy.table import Table

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

type SpectrumArrays = tuple[
    npt.NDArray[Any],
    npt.NDArray[Any],
    npt.NDArray[Any] | None,
]

def file_reader(file: str) -> SpectrumArrays:
    """
    Gets the file path within the TCT main folder (text or FITS) and returns the spectrum points (nm, br, std).
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
        nm, br, std = fits_reader(file, type_info)
    else:
        nm, br, std = txt_reader(file, type_info)
    return nm, br, std

def txt_reader(file: str, type_info: str) -> SpectrumArrays:
    """ Imports spectral data from a text file """
    if 'a' in type_info:
        to_nm_factor = 0.1
    elif 'u' in type_info:
        to_nm_factor = 1000
    else:
        to_nm_factor = 1
    with open(file, 'rt', encoding='UTF-8') as f:
        data = np.asarray(np.loadtxt(f)).transpose()
        if data.ndim != 2 or data.shape[0] < 2:
            raise ValueError(f'Expected at least two columns in "{file}"')
        nm = data[0]
        br = data[1]
        std: npt.NDArray[Any] | None = data[2] if data.shape[0] >= 3 else None
        if data.shape[0] >= 4 and 1 in data[3]:
            # SMASS error indication in the 4th column
            mask = data[3] == 1
            nm = nm[mask]
            br = br[mask]
            if std is not None:
                std = std[mask]
    return nm*to_nm_factor, br, std

def fits_reader(file: str, type_info: str) -> SpectrumArrays:
    """ Imports spectral data from a FITS file in standards of CALSPEC, VizeR, UVES, BAAVSS, etc """
    if 'n' in type_info:
        wl_unit: u.UnitBase | None = u.nm
    elif 'a' in type_info:
        wl_unit = u.Angstrom
    elif 'u' in type_info:
        wl_unit = u.micron
    else:
        wl_unit = None
    std: Any = None
    with fits.open(file) as hdul:
        if len(hdul) >= 2 and len(columns := cast(Any, hdul[1]).columns) >= 2:
            # Most likely the second HDU contains data
            hdu = cast(Any, hdul[1])
            tbl = Table(hdu.data)
            # Getting wavelength data
            wl_id = search_column(list(columns.names), 'wl')
            wl: Any = tbl[columns[wl_id].name]
            if wl.ndim > 1:
                wl = wl[0]
            # Getting flux data
            br_id = search_column(list(columns.names), 'br')
            br: Any = tbl[columns[br_id].name]
            match br.ndim:
                case 2:
                    br = br[0]
                case 3:
                    br = br.transpose((0, 2, 1)) # like spectral cube?!
            # Standard deviation getting attempt
            std_id: int | None = None
            if len(columns) > 2:
                std_id = search_column(list(columns.names), 'std')
                std = tbl[columns[std_id].name]
                if len(std.shape) > 1:
                    std = std[0]
            # Standardization of units of measurement
            if wl_unit is None:
                wl_unit = u.Unit(columns[wl_id].unit)
            nm = (wl * wl_unit).to(u.nm)
            br = (br * u.Unit(columns[br_id].unit)).to(flux_density_SI)
            if std is not None and std_id is not None:
                std = (std * u.Unit(columns[std_id].unit)).to(flux_density_SI)
        else:
            try:
                # BAAVSS store wavelength info only in primary HDU
                header = cast(Any, hdul[0]).header
                wl = header['CRVAL1'] + header['CDELT1']*(np.arange(header['NAXIS1'])-1)
                if wl_unit is None:
                    wl_unit = u.Unit(header['CUNIT1'])
                nm = (wl * wl_unit).to(u.nm)
                br = list(cast(Any, Table(cast(Any, hdul[0]).data))[0])
            except KeyError:
                # IRAF-formatted "multispec" is not supported, there were attempts
                data = cast(Any, hdul[0]).data
                nm = data[0] * 0.1
                br = data[1]
    nm_array: npt.NDArray[Any] = np.array(nm)
    br_array: npt.NDArray[Any] = np.array(br)
    std_array: npt.NDArray[Any] | None = None
    if std is not None:
        std_array = np.array(std)
    return nm_array, br_array, std_array

def search_column(names: Sequence[str], target: str) -> int:
    """ Returns the index of the FITS column of interest """
    names = [name.lower() for name in names]
    names_set = set(names)
    candidates: set[str] = set()
    match target:
        case 'wl':
            candidates = names_set & {'wavelength', 'wave', 'lambda'}
        case 'br':
            candidates = names_set & {'flux', 'sci'}
        case 'std':
            candidates = names_set & {'syserror'}
    try:
        return names.index(next(iter(candidates)))
    except (IndexError, StopIteration):
        match target:
            case 'wl':
                return 0 # by default the first column is wavelength
            case 'br':
                return 1 # the second is flux
            case 'std':
                return 2 # the third is standard deviation
            case _:
                return 0
