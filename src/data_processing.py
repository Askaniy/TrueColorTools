""" Processes the raw data of a database unit into a state from which color can be obtained. """

from typing import Sequence
from traceback import format_exc
from copy import deepcopy
import numpy as np
from src.core import Spectrum, Photometry, get_filter, nm_red_limit, resolution
import src.data_import as di


# To calculate color, it is necessary to achieve a definition of the spectrum in the visible range.
# Boundaries have been defined based on the CMF (color matching functions) used, but can be any.
visible_range = np.arange(390, 780, 5) # nm

sun_SI = Spectrum.from_file('Sun', 'spectra/files/CALSPEC/sun_reference_stis_002.fits') # W / (m² nm)
sun_in_V = sun_SI @ get_filter('Generic_Bessell.V')
sun_norm = sun_SI.scaled_at('Generic_Bessell.V')

vega_SI = Spectrum.from_file('Vega', 'spectra/files/CALSPEC/alpha_lyr_stis_011.fits') # W / (m² nm)
vega_in_V = vega_SI @ get_filter('Generic_Bessell.V')
vega_norm = vega_SI.scaled_at('Generic_Bessell.V')

lambdas = np.arange(5, nm_red_limit+1, 5)
equal_frequency_density = Spectrum('AB', lambdas, 1/lambdas**2).scaled_at('Generic_Bessell.V') # f_lambda=f_nu*c/lambda^2
del lambdas


class NonReflectiveBody:
    """ High-level processing class, specializing on photometry of a physical body with not specified reflectance. """

    def __init__(self, name: str, tags: Sequence, spectrum: Spectrum):
        """
        Args:
        - `name` (str): human-readable identification. May include references (separated by "|") and a note (separated by ":")
        - `tags` (Sequence): list of categories that specify the physical body
        - `spectrum` (Spectrum): not assumed to be scaled
        """
        self.name = name
        self.tags = tags
        self.spectrum = spectrum
    
    def get_spectrum(self, mode: str):
        if mode == 'chromaticity' or 'star' in self.tags:
            return self.spectrum # means it's an emitter and we need to render it
        else:
            return Spectrum(self.name, *Spectrum.stub).to_scope(visible_range) # means we don't need to render it


class ReflectiveBody:
    """
    High-level processing class, specializing on reflectance photometry of a physical body.

    Albedo formatting rules:
    1. `geometric_albedo` and `spherical_albedo` can be a boolean type or in [filter/nm, br, sd] format
    2. both values by default `false`
    3. no albedo is specified and "star" in tags → emitter, else black output
    4. one albedo is specified → another one is estimated with the phase integral model

    Phase integral model by Shevchenko et al.: https://ui.adsabs.harvard.edu/abs/2019A%26A...626A..87S/abstract
    q = 0.359 (± 0.005) + 0.47 (± 0.03) p, where `p` is geometric albedo.
    By definition, spherical albedo A is p∙q.
    """

    def __init__(self, name: str, tags: Sequence, geometric: Spectrum = None, spherical: Spectrum = None):
        """
        Args:
        - `name` (str): human-readable identification. May include references (separated by "|") and a note (separated by ":")
        - `tags` (Sequence): list of categories that specify the physical body
        - `geometric` (Spectrum): represents geometric albedo
        - `spherical` (Spectrum): represents spherical albedo
        """
        self.name = name
        self.tags = tags
        self.spherical = spherical
        self.geometric = geometric
    
    def get_spectrum(self, mode: str):
        if mode == 'chromaticity': # chromaticity mode
            if self.geometric:
                return self.geometric # most likely it's original (unscaled) data, so it's a bit better
            else:
                return self.spherical
        elif mode == 'geometric':
            if self.geometric:
                return self.geometric
            else:
                sphericalV = self.spherical @ get_filter('Generic_Bessell.V')
                geometricV = (np.sqrt(0.359**2 + 4 * 0.47 * sphericalV) - 0.359) / (2 * 0.47)
                return self.spherical.scaled_at('Generic_Bessell.V', geometricV)
        else:
            if self.spherical:
                return self.spherical
            else:
                geometricV = self.geometric @ get_filter('Generic_Bessell.V')
                sphericalV = geometricV * (0.395 + 0.47 * geometricV)
                return self.geometric.scaled_at('Generic_Bessell.V', sphericalV)


def number2array(target: int|float|Sequence, size: int):
    """ Makes an array of specified size even if input is a number """
    if isinstance(target, (int, float)):
        return np.full(size, target)
    else:
        return np.array(target)

def mag2flux(mag: int|float|np.ndarray, zero_point: float = 1.):
    """ Converts magnitudes to flux (by default in Vega units) """
    return zero_point * 10**(-0.4 * mag)

def sd_mag2sd_flux(sd_mag: int|float|np.ndarray, flux: int|float|np.ndarray):
    """
    Converts standard deviation of the magnitude to a flux standard deviation.

    The formula is derived from the error propagation equation:
    I(mag) = zero_point ∙ 10^(-0.4 mag)
    sd_I² = (d I / d mag)² ∙ sd_mag²
    I' = zero_point∙(10^(-0.4 mag))' = zero_point∙10^(-0.4 mag)∙ln(10^(-0.4)) = I∙(-0.4) ln(10)
    sd_I = |I'| ∙ sd_mag = 0.4 ln(10) ∙ I ∙ sd_mag
    """
    return 0.4 * np.log(10) * flux * sd_mag

def color_index_splitter(index: str):
    """
    Dashes in filter names are allowed in the SVO Filter Profile Service.
    This function should fix all or most of the problems caused.
    """
    try:
        filter1, filter2 = index.split('-')
    except ValueError:
        dotpart1, dotpart2, dotpart3 = index.split('.') # one dot per full filter name
        dashpart1, dashpart2 = dotpart2.split('-', 1)
        filter1 = f'{dotpart1}.{dashpart1}'
        filter2 = f'{dashpart2}.{dotpart3}'
    return filter1, filter2

def color_indices_parser(indices: dict, sd: Sequence = None):
    """
    Converts color indices to linear brightness, assuming mag=0 in the first filter.
    Each new color index must refer to a previously specified one.
    Note: The output order may sometimes not be in ascending wavelength order.
    This can be corrected by knowing the filter profiles, which better to do outside the function.

    For standard deviations the error propagation equation is used:
    f(x, y) = x - y
    sd_f² = (df/dx)² sd_x² + (df/dy)² sd_y² = sd_x² + sd_y²
    where x, y are magnitudes and f is a color index.

    If all the data points have the same uncertainty (x == y):
    sd_y = sd_f / sqrt(2)

    Else, we assume that the first two data points have equal uncertainty
    to begin the iterative calculation of standard deviations:
    sd_y = sqrt(sd_f² - sd_x²)
    """
    indices = deepcopy(indices) # else it would pop one index per calling
    first_color_index = tuple(indices.keys())[0]
    filter0, filter1 = color_index_splitter(first_color_index)
    # Working with stub if standard deviations are not known to simplify the code
    sd_ = iter(sd if sd is not None else np.ones(len(indices)))
    sd0 = next(sd_)/np.sqrt(2)
    filters = {
        filter0: (0, sd0), # assuming mag=0 for the first point
        filter1: (-indices.pop(first_color_index), sd0) # and the same standard deviation for the first two points
    }
    for key, value in indices.items():
        bluer_filter, redder_filter = color_index_splitter(key)
        if bluer_filter in filters:
            current_sd = np.sqrt(next(sd_)**2 - filters[bluer_filter][1]**2)
            filters |= {redder_filter: (filters[bluer_filter][0] - value, current_sd)}
        else:
            current_sd = np.sqrt(next(sd_)**2 - filters[redder_filter][1]**2)
            filters |= {bluer_filter: (filters[redder_filter][0] + value, current_sd)}
    flux, sd_flux = np.array(tuple(filters.values())).transpose()
    flux = mag2flux(flux)
    sd_flux = sd_mag2sd_flux(sd_flux, flux) if sd is not None else None
    return filters.keys(), flux, sd_flux

def spectral_data2visible_spectrum(
        name: str, nm: Sequence[int|float], filters: Sequence[str], br: Sequence,
        sd: Sequence = None, calib: str = None, sun: bool = False
    ) -> Spectrum:
    """
    Decides whether we are dealing with photometry or continuous spectrum
    and guarantees the completeness of the spectrum in the visible range.
    """
    if len(nm) > 0:
        spectral_data = Spectrum.from_array(name, nm, br, sd)
    elif len(filters) > 0:
        spectral_data = Photometry.from_list(name, filters, br, sd)
    else:
        print(f'# Note for the database object "{name}"')
        print(f'- No wavelength data. Spectrum stub object was created.')
        spectral_data = Spectrum(name, *Spectrum.stub)
    match calib:
        case 'vega':
            spectral_data *= vega_norm
        case 'ab':
            spectral_data *= equal_frequency_density
        case _:
            pass
    if sun:
        spectral_data /= sun_norm
    return spectral_data.to_scope(visible_range)

def database_parser(name: str, content: dict) -> NonReflectiveBody | ReflectiveBody:
    """
    Depending on the contents of the object read from the database, returns a class that has `get_spectrum()` method

    Supported input keys of a database unit:
    - `nm` (list): list of wavelengths in nanometers
    - `br` (list): same-size list of "brightness", flux in units of energy (not a photon counter)
    - `mag` (list): same-size list of magnitudes
    - `sd` (list/number): same-size list of standard deviations or a general value
    - `nm_range` (dict): `start`, `stop`, `step` keys defining a wavelength range
    - `slope` (dict): `start`, `stop`, `power` keys defining a spectrum from spectrophotometric gradient
    - `file` (str): path to a text or FITS file, recommended placing in `spectra` or `spectra_extras` folder
    - `filters` (list): list of filter names that can be found in the `filters` folder
    - `indices` (list): dictionary of color indices, formatted `{'filter1-filter2': *float*, ...}`
    - `system` (str): a way to bracket the name of the photometric system
    - `calib` (str): `Vega` or `AB` filters zero points calibration, `ST` is assumed by default
    - `albedo` (bool/list): indicates data as albedo scaled or tells how to do it with `[filter/nm, br, (sd)]`
    - `geometric_albedo` (bool/list): indicator of geometric/normal albedo data or how to scale to it
    - `spherical_albedo` (bool/list): indicator of spherical albedo data or how to scale to it
    - `br_geometric`, `br_spherical` (list): specifying unique spectra for different albedos
    - `sd_geometric`, `sd_spherical` (list/number): corresponding standard deviations or a general value
    - `sun` (bool): `true` to remove Sun as emitter
    - `tags` (list): strings, categorizes a spectrum
    """
    br = []
    sd = None
    nm = [] # Spectrum object indicator
    filters = [] # Photometry object indicator
    if 'file' in content:
        try:
            nm, br, sd = di.file_reader(content['file'])
        except Exception:
            nm, br, sd = Spectrum.stub
            print(f'# Note for the Spectrum object "{name}"')
            print(f'- Something unexpected happened during external file reading. The data was replaced by a stub.')
            print(f'- More precisely, {format_exc(limit=0).strip()}')
    else:
        # Brightness reading
        if 'br' in content:
            br = content['br']
            if 'sd' in content:
                sd = number2array(content['sd'], len(br))
        elif 'mag' in content:
            br = mag2flux(np.array(content['mag']))
            if 'sd' in content:
                sd = number2array(content['sd'], len(br))
                sd = sd_mag2sd_flux(sd, br)
        # Spectrum reading
        if 'nm' in content:
            nm = content['nm']
        elif 'nm_range' in content:
            nm_range = content['nm_range']
            nm = np.arange(nm_range['start'], nm_range['stop']+1, nm_range['step'])
        elif 'slope' in content:
            slope = content['slope']
            nm = np.arange(slope['start'], slope['stop']+1, resolution)
            br = (nm / nm[0])**slope['power']
        # Photometry reading
        elif 'filters' in content:
            filters = content['filters']
        elif 'indices' in content:
            if 'sd' in content:
                sd = number2array(content['sd'], len(content['indices']))
            filters, br, sd = color_indices_parser(content['indices'], sd)
        if 'system' in content:
            filters = [f'{content["system"]}.{short_name}' for short_name in filters]
    geometric = None
    spherical = None
    calib = content['calib'].lower() if 'calib' in content else None
    sun = 'sun' in content and content['sun']
    if len(br) == 0:
        if 'br_geometric' in content or 'br_spherical' in content:
            if 'br_geometric' in content:
                br = content['br_geometric']
                sd = number2array(content['sd_geometric'], len(br)) if 'sd_geometric' in content else None
                geometric = spectral_data2visible_spectrum(name, nm, filters, br, sd, calib, sun)
            if 'br_spherical' in content:
                br = content['br_spherical']
                sd = number2array(content['sd_spherical'], len(br)) if 'sd_spherical' in content else None
                spherical = spectral_data2visible_spectrum(name, nm, filters, br, sd, calib, sun)
        else:
            print(f'# Note for the database object "{name}"')
            print(f'- No brightness data. Spectrum stub object was created.')
            spectrum = Spectrum(name, *Spectrum.stub).to_scope(visible_range)
    else:
        spectrum = spectral_data2visible_spectrum(name, nm, filters, br, sd, calib, sun)
        # Non-specific albedo parsing
        if 'albedo' in content:
            if isinstance(content['albedo'], bool):
                geometric = spherical = spectrum
            elif isinstance(content['albedo'], list):
                geometric = spherical = spectrum.scaled_at(*content['albedo'])
            else:
                print(f'# Note for the database object "{name}"')
                print(f'- Invalid albedo value: {content["albedo"]}. Must be boolean or [filter/nm, br, (sd)].')
        # Geometric albedo parsing
        if 'geometric_albedo' in content:
            if isinstance(content['geometric_albedo'], bool):
                geometric = spectrum
            elif isinstance(content['geometric_albedo'], list):
                geometric = spectrum.scaled_at(*content['geometric_albedo'])
            else:
                print(f'# Note for the database object "{name}"')
                print(f'- Invalid geometric albedo value: {content["geometric_albedo"]}. Must be boolean or [filter/nm, br, (sd)].')
        # Spherical albedo parsing
        if 'spherical_albedo' in content:
            if isinstance(content['spherical_albedo'], bool):
                spherical = spectrum
            elif isinstance(content['spherical_albedo'], list):
                spherical = spectrum.scaled_at(*content['spherical_albedo'])
            else:
                print(f'# Note for the database object "{name}"')
                print(f'- Invalid spherical albedo value: {content["spherical_albedo"]}. Must be boolean or [filter/nm, br, (sd)].')
    tags = []
    if 'tags' in content:
        tags = content['tags']
    if geometric or spherical:
        return ReflectiveBody(name, tags, geometric, spherical)
    else:
        return NonReflectiveBody(name, tags, spectrum)