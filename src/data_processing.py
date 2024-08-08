""" Processes the raw data of a database unit into a state from which color can be obtained. """

from typing import Sequence
from traceback import format_exc
from math import sqrt
import numpy as np
from src.core import *
import src.auxiliary as aux
import src.data_import as di


sun_SI = Spectrum.from_file('spectra/files/CALSPEC/sun_reference_stis_002.fits', name='Sun') # W / (m² nm)
sun_in_V = sun_SI @ get_filter('Generic_Bessell.V')
sun_norm = sun_SI.scaled_at(get_filter('Generic_Bessell.V'))
sun_filter = sun_SI.normalize()

vega_SI = Spectrum.from_file('spectra/files/CALSPEC/alpha_lyr_stis_011.fits', name='Vega') # W / (m² nm)
vega_in_V = vega_SI @ get_filter('Generic_Bessell.V')
vega_norm = vega_SI.scaled_at(get_filter('Generic_Bessell.V'))


class NonReflectiveBody:
    """ High-level processing class, specializing on photometry of a physical body with not specified reflectance. """

    def __init__(self, name: ObjectName, tags: Sequence, spectrum: Spectrum):
        """
        Args:
        - `name` (ObjectName): name as an instance of a class that stores its components 
        - `tags` (Sequence): list of categories that specify the physical body
        - `spectrum` (Spectrum): not assumed to be scaled
        """
        self.name = name
        self.tags = tags
        self.spectrum = spectrum
    
    def get_spectrum(self, mode: str):
        """
        Returns the spectrum as the first argument, and the `estimated=False` bool status as the second one.
        Albedo not determined for NonReflectiveBody, so it can't be "estimated", but we need output compatibility with ReflectiveBody.
        """
        if 'star' in self.tags:
            return self.spectrum, False # means it's an emitter and we need to render it
        else:
            return Spectrum(self.name, *Spectrum.stub).to_scope(visible_range), False # means we don't need to render it


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

    def __init__(
            self, name: ObjectName, tags: Sequence,
            geometric: Spectrum = None, spherical: Spectrum = None,
            phase_integral: tuple[float, float] = None
        ):
        """
        Args:
        - `name` (ObjectName): name as an instance of a class that stores its components 
        - `tags` (Sequence): list of categories that specify the physical body
        - `geometric` (Spectrum): represents geometric albedo
        - `spherical` (Spectrum): represents spherical albedo
        - `phase_integral` (tuple[value, sd]): factor of transition from geometric albedo to spherical
        """
        self.name = name
        self.tags = tags
        self.spherical = spherical
        self.geometric = geometric
        self.phase_integral = phase_integral
    
    def get_spectrum(self, mode: str):
        """
        Returns the albedo-scaled spectrum as the first argument, and the `estimated` bool status as the second one.
        `estimated = True` if the albedo was not known and estimated using a theoretical model.
        """
        match mode:
            case 'geometric':
                if self.geometric:
                    return self.geometric, False
                else:
                    sphericalV = self.spherical @ get_filter('Generic_Bessell.V')
                    if self.phase_integral is not None:
                        phase_integral = self.phase_integral[0]
                        geometricV = sphericalV / phase_integral
                        estimated = False
                    else:
                        geometricV = (np.sqrt(0.359**2 + 4 * 0.47 * sphericalV) - 0.359) / (2 * 0.47)
                        estimated = True
                    return self.spherical.scaled_at(get_filter('Generic_Bessell.V'), geometricV), estimated
            case 'spherical':
                if self.spherical:
                    return self.spherical, False
                else:
                    geometricV = self.geometric @ get_filter('Generic_Bessell.V')
                    if self.phase_integral is not None:
                        phase_integral = self.phase_integral[0]
                        estimated = False
                    else:
                        phase_integral = 0.359 + 0.47 * geometricV
                        estimated = True
                    sphericalV = geometricV * phase_integral
                    return self.geometric.scaled_at(get_filter('Generic_Bessell.V'), sphericalV), estimated


def parse_value_sd(data: float|Sequence[float]):
    """ Guarantees the output of the value and its sd for variable input """
    if isinstance(data, Sequence) and len(data) == 2:
        value, sd = data
    elif isinstance(data, (int, float)):
        value = data
        sd = None
    else:
        print(f'Invalid data input: {data}. Must be a numeric value or a [value, sd] list. Returning None.')
        value = sd = None
    return value, sd

def number2array(target: int|float|Sequence, size: int):
    """ Makes an array of specified size even if input is a number """
    if isinstance(target, (int, float)):
        return np.full(size, target)
    else:
        return np.array(target)

def mag2irradiance(mag: int|float|np.ndarray, zero_point: float = 1.):
    """ Converts magnitudes to irradiance (by default in Vega units) """
    return zero_point * 10**(-0.4 * mag)

def sd_mag2sd_irradiance(sd_mag: int|float|np.ndarray, irradiance: int|float|np.ndarray):
    """
    Converts standard deviation of the magnitude to a irradiance standard deviation.

    The formula is derived from the error propagation equation:
    I(mag) = zero_point ∙ 10^(-0.4 mag)
    sd_I² = (d I / d mag)² ∙ sd_mag²
    I' = zero_point∙(10^(-0.4 mag))' = zero_point∙10^(-0.4 mag)∙ln(10^(-0.4)) = I∙(-0.4) ln(10)
    sd_I = |I'| ∙ sd_mag = 0.4 ln(10) ∙ I ∙ sd_mag
    """
    return 0.4 * np.log(10) * irradiance * sd_mag

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

def color_indices_parser(indices: dict):
    """
    Converts color indices to linear brightness, assuming mag=0 in the first filter.
    Each new color index must refer to a previously specified one.
    Note: The output order may sometimes not be in ascending wavelength order.
    This can be corrected by knowing the filter profiles, which better to do outside the function.

    For standard deviations the error propagation equation is used:
    f(x, y) = x - y
    sd_f² = (df/dx)² sd_x² + (df/dy)² sd_y² = sd_x² + sd_y²
    where x, y are magnitudes and f is a color index.

    Finding standard deviations of a photospectrum built from color indices is an ill-posed problem:
    it's just like with integrating, we loose constant after differentiation (color indices is
    a discrete differential form of a photospectrum).
    For the photospectrum itself, it's not a problem: the solutions dimension is just scaling
    the spectrum on a constant (it's pretty obvious that color indices always lost brightness
    information).
    But the solutions space for their standard deviations is more complex, I found its geometric
    interpretation: since the standard deviations subtracting rule is, in fact, the Pythagorean theorem,
    the solutions space is the same as if you try to build a line of right triangles, for each one
    the next cathetus is linked to a previous cathetus by their square.
    N hypotenuses are standard deviations of color indices, and N+1 different cathetes are the sought
    standard deviations of the photospectrum.
    The whole triangle line possible positions can be described by just one parameter (1D parametric
    space of solutions).
    For simplicity, I will choose the first cathetus (the first sought standard deviation) as
    a variable of this space.
    Such triangles can "collapse" if the previous cathetus is greater than the next hypotenuse!
    I tried to find an analytical solution, but the requirement for the optimal solution I derived
    suggested that about a half of the triangles should be collapsed.

    In the numerical approach I use, some solutions are collapsed (the `try-except` code block),
    but there are a some range of possible solutions too, which one to choose?
    I decided to choose the solution with minimal standard deviation of standard deviations it gives.
    To tighten the solution selection criteria, it can be assumed that the size of the standard deviation
    is inversely proportional to the root of the irradiance (in the Poisson noise approximation).
    So it's better to minimize the differences not between the stds of magnitudes, but between
    the stds of scaled irradiances.
    """
    first_color_index = tuple(indices.keys())[0]
    filter0, _ = color_index_splitter(first_color_index)
    _, sd0 = parse_value_sd(indices[first_color_index])
    # Just photospectrum calculation
    uncertainty_flag = False
    filters = {filter0: 0} # mag=0 for the first point (arbitrarily)
    for key, value in indices.items():
        bluer_filter, redder_filter = color_index_splitter(key)
        mag, sd = parse_value_sd(value)
        if sd is not None:
            uncertainty_flag = True
        if bluer_filter in filters:
            filters |= {redder_filter: filters[bluer_filter] - mag}
        else:
            filters |= {bluer_filter: filters[redder_filter] + mag}
    irradiance = mag2irradiance(np.array(tuple(filters.values())))
    sd = np.zeros_like(irradiance)
    # Uncertainty calculation
    if uncertainty_flag:
        shot_noise_factor = np.sqrt(irradiance) # common Poisson noise factor
        old_sd_of_sd = np.inf
        for sd_assumed in np.linspace(0, sd0, 1001):
            impossible_assumption = False
            # Numerically select the best value of the standard deviation of the first point,
            # on which all other standard deviations clearly depend
            filters = {filter0: sd_assumed}
            for key, value in indices.items():
                bluer_filter, redder_filter = color_index_splitter(key)
                _, sd = parse_value_sd(value)
                try:
                    if bluer_filter in filters:
                        filters |= {redder_filter: sqrt(sd**2 - filters[bluer_filter]**2)}
                    else:
                        filters |= {bluer_filter: sqrt(sd**2 - filters[redder_filter]**2)}
                except ValueError:
                    # This means that the difference under the root is negative
                    # and the initial standard deviation assumption is not possible
                    impossible_assumption = True
                    break
            if not impossible_assumption:
                new_sd = sd_mag2sd_irradiance(np.array(tuple(filters.values())), irradiance)
                # Finding the minimum deviation between sd as solution quality criterion
                # The standard deviations are scaled by the Poisson noise factor
                new_sd_of_sd = np.std(new_sd * shot_noise_factor)
                if new_sd_of_sd < old_sd_of_sd:
                    old_sd = new_sd
                    old_sd_of_sd = new_sd_of_sd
                    continue
                else:
                    # Means that the best values of standard deviations were found
                    # in the last iteration and they started to diverge
                    sd = old_sd
                    break
    return filters.keys(), irradiance, sd

def phase_function2phase_integral(name: str, params: dict):
    """ Determines phase integral from the phase function """
    phase_integral = phase_integral_sd = None
    match name:
        case 'HG':
            g, g_sd = parse_value_sd(params['G'])
            phase_integral = 0.290 + 0.684 * g
            if g_sd is not None:
                phase_integral_sd = 0.827 * g_sd # 0.827 ≈ sqrt(0.684)
        case 'HG1G2':
            g1, g1_sd = parse_value_sd(params['G_1'])
            g2, g2_sd = parse_value_sd(params['G_2'])
            phase_integral = 0.009082 + 0.4061 * g1 + 0.8092 * g2
            if g1_sd is not None and g2_sd is not None:
                phase_integral_sd = np.sqrt(0.4061 * g1_sd + 0.8092 * g2_sd)
        case _:
            print(f'Phase function with name {name} is not supported.')
    return phase_integral, phase_integral_sd

def spectral_data2visible_spectrum(
        name: ObjectName, nm: Sequence[int|float], filters: Sequence[str], br: Sequence,
        sd: Sequence = None, calib: str = None, sun: bool = False
    ) -> Spectrum:
    """
    Decides whether we are dealing with photospectrum or continuous spectrum
    and guarantees the completeness of the spectrum in the visible range.
    """
    if len(nm) > 0:
        spectral_data = Spectrum.from_array(nm, br, sd, name=name)
    elif len(filters) > 0:
        spectral_data = Photospectrum(FilterSystem.from_list(filters), br, sd, name=name)
    else:
        print(f'# Note for the database object "{name.raw_name}"')
        print(f'- No wavelength data. Spectrum stub object was created.')
        spectral_data = Spectrum(name, *Spectrum.stub)
    match calib:
        case 'vega':
            spectral_data *= vega_norm
        case 'ab':
            spectral_data = spectral_data.convert_from_frequency_spectral_density()
        case _:
            pass
    if sun:
        spectral_data /= sun_norm
    return spectral_data.to_scope(visible_range)

def database_parser(name: ObjectName, content: dict) -> NonReflectiveBody | ReflectiveBody:
    """
    Depending on the contents of the object read from the database, returns a class that has `get_spectrum()` method

    Supported input keys of a database unit:
    - `nm` (list): list of wavelengths in nanometers
    - `br` (list): same-size list of "brightness" in energy density units (not a photon counter)
    - `mag` (list): same-size list of magnitudes
    - `sd` (list/number): same-size list of standard deviations or a general value
    - `nm_range` (dict): `start`, `stop`, `step` keys defining a wavelength range
    - `slope` (dict): `start`, `stop`, `power` keys defining a spectrum from spectrophotometric gradient
    - `file` (str): path to a text or FITS file, recommended placing in `spectra` or `spectra_extras` folder
    - `filters` (list): list of filter names (see `filters` folder), can be mixed with nm values if needed
    - `color_indices` (list): dictionary of color indices, formatted `{'filter1-filter2': [br, (sd)]], …}`
    - `photometric_system` (str): a way to bracket the name of the photometric system
    - `calibration_system` (str): `Vega` or `AB` filters zero points calibration, `ST` is assumed by default
    - `albedo` (bool/list): indicates data as albedo scaled or tells how to do it with `[filter/nm, [br, (sd)]]`
    - `geometric_albedo` (bool/list): indicator of geometric/normal albedo data or how to scale to it
    - `spherical_albedo` (bool/list): indicator of spherical albedo data or how to scale to it
    - `bond_albedo` (number): sets spherical albedo scale using known solar spectrum
    - `phase_integral` (number/list): factor of transition from geometric albedo to spherical (sd is optional)
    - `phase_function` (list): function name and its parameters to compute phase integral (sd is optional)
    - `br_geometric`, `br_spherical` (list): specifying unique spectra for different albedos
    - `sd_geometric`, `sd_spherical` (list/number): corresponding standard deviations or a general value
    - `sun_is_emitter` (bool): `true` to remove the reflected solar spectrum
    - `tags` (list): strings categorizing the spectrum
    """
    br = []
    sd = None
    nm = [] # Spectrum object indicator
    filters = [] # Photospectrum object indicator
    if 'file' in content:
        try:
            nm, br, sd = di.file_reader(content['file'])
        except Exception:
            nm, br, sd = Spectrum.stub
            print(f'# Note for the Spectrum object "{name.raw_name}"')
            print(f'- Something unexpected happened during external file reading. The data was replaced by a stub.')
            print(f'- More precisely, {format_exc(limit=0).strip()}')
    else:
        # Brightness reading
        if 'br' in content:
            br = content['br']
            if 'sd' in content:
                sd = number2array(content['sd'], len(br))
        elif 'mag' in content:
            br = mag2irradiance(np.array(content['mag']))
            if 'sd' in content:
                sd = number2array(content['sd'], len(br))
                sd = sd_mag2sd_irradiance(sd, br)
        # Spectrum reading
        if 'nm' in content:
            nm = content['nm']
        elif 'nm_range' in content:
            nm_range = content['nm_range']
            nm = np.arange(nm_range['start'], nm_range['stop']+1, nm_range['step'])
        elif 'slope' in content:
            slope = content['slope']
            nm = np.arange(slope['start'], slope['stop']+1, aux.resolution)
            br = (nm / nm[0])**slope['power']
        # Photospectrum reading
        elif 'filters' in content:
            filters = content['filters']
        elif 'color_indices' in content:
            filters, br, sd = color_indices_parser(content['color_indices'])
        if 'photometric_system' in content:
            # regular filter if name is string, else "delta-filter" (wavelength)
            filters = [f'{content["photometric_system"]}.{short_name}' if isinstance(short_name, str) else short_name for short_name in filters]
    calib = content['calibration_system'].lower() if 'calibration_system' in content else None
    sun = 'sun_is_emitter' in content and content['sun_is_emitter']
    geometric = spherical = None
    if len(br) == 0:
        if 'br_geometric' in content:
            br_geom = content['br_geometric']
            sd_geom = number2array(content['sd_geometric'], len(br_geom)) if 'sd_geometric' in content else None
            geometric = spectral_data2visible_spectrum(name, nm, filters, br_geom, sd_geom, calib, sun)
            if 'spherical_albedo' in content:
                where, how = content['spherical_albedo']
                spherical = geometric.scaled_at(where, *parse_value_sd(how))
            elif 'bond_albedo' in content:
                spherical = geometric.scaled_at(sun_filter, *parse_value_sd(content['bond_albedo']))
        if 'br_spherical' in content:
            br_sphe = content['br_spherical']
            sd_sphe = number2array(content['sd_spherical'], len(br_sphe)) if 'sd_spherical' in content else None
            spherical = spectral_data2visible_spectrum(name, nm, filters, br_sphe, sd_sphe, calib, sun)
            if 'geometric_albedo' in content:
                where, how = content['geometric_albedo']
                geometric = spherical.scaled_at(where, *parse_value_sd(how))
        if geometric is None and spherical is None:
            print(f'# Note for the database object "{name.raw_name}"')
            print(f'- No brightness data. Spectrum stub object was created.')
            spectrum = Spectrum(name, *Spectrum.stub).to_scope(visible_range)
    else:
        spectrum = spectral_data2visible_spectrum(name, nm, filters, br, sd, calib, sun)
        # Non-specific albedo parsing
        if 'albedo' in content:
            if isinstance(content['albedo'], bool) and content['albedo']:
                geometric = spherical = spectrum
            elif isinstance(content['albedo'], Sequence):
                where, how = content['albedo']
                geometric = spherical = spectrum.scaled_at(where, *parse_value_sd(how))
            else:
                print(f'# Note for the database object "{name.raw_name}"')
                print(f'- Invalid albedo value: {content["albedo"]}. Must be boolean or [filter/nm, [br, (sd)]].')
        # Geometric albedo parsing
        if 'geometric_albedo' in content:
            if isinstance(content['geometric_albedo'], bool) and content['geometric_albedo']:
                geometric = spectrum
            elif isinstance(content['geometric_albedo'], Sequence):
                where, how = content['geometric_albedo']
                geometric = spectrum.scaled_at(where, *parse_value_sd(how))
            else:
                print(f'# Note for the database object "{name.raw_name}"')
                print(f'- Invalid geometric albedo value: {content["geometric_albedo"]}. Must be boolean or [filter/nm, [br, (sd)]].')
        # Spherical albedo parsing
        if 'spherical_albedo' in content:
            if isinstance(content['spherical_albedo'], bool) and content['spherical_albedo']:
                spherical = spectrum
            elif isinstance(content['spherical_albedo'], Sequence):
                where, how = content['spherical_albedo']
                spherical = spectrum.scaled_at(where, *parse_value_sd(how))
            else:
                print(f'# Note for the database object "{name.raw_name}"')
                print(f'- Invalid spherical albedo value: {content["spherical_albedo"]}. Must be boolean or [filter/nm, [br, (sd)]].')
        elif 'bond_albedo' in content:
            spherical = spectrum.scaled_at(sun_filter, *parse_value_sd(content['bond_albedo']))
    tags = set()
    if 'tags' in content:
        for tag in content['tags']:
            tags |= set(tag.split('/'))
    if geometric or spherical:
        phase_integral = phase_integral_sd = None
        if 'phase_integral' in content:
            phase_integral, phase_integral_sd = parse_value_sd(content['phase_integral'])
        elif 'phase_function' in content:
            phase_func = content['phase_function']
            if isinstance(phase_func, Sequence) and len(phase_func) == 2 and isinstance(phase_func[0], str) and isinstance(phase_func[1], dict):
                phase_func, params = content['phase_function']
                phase_integral, phase_integral_sd = phase_function2phase_integral(phase_func, params)
            else:
                print(f'# Note for the database object "{name.raw_name}"')
                print(f'- Invalid phase function value: {content["phase_function"]}. Must be in the form ["name", {{param1: value1, ...}}]')
        if phase_integral is not None:
            phase_integral = (phase_integral, phase_integral_sd)
        return ReflectiveBody(name, tags, geometric, spherical, phase_integral)
    else:
        return NonReflectiveBody(name, tags, spectrum)