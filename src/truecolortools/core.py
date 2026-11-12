"""
TrueColorTools-specific data layer on top of AstroColor.

AstroColor owns spectra, filter profiles, photometric models, database
parsing and color processing. This module keeps only the glue that is
specific to TCT:

- configuration of the filter search folders;
- reading TCT spectrum files with TCT extension conventions;
- the `DatabaseEntry` wrapper that adds database metadata (`tags`) and
  file-based albedo spectra to `astrocolor.CelestialObject`;
- small adapters for inputs that AstroColor intentionally does not accept
  (numeric filter identifiers and TCT `ObjectName`).

Everything else should be imported from `astrocolor` directly.
"""

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import astrocolor as ac
import numpy as np
import numpy.typing as npt

import truecolortools.data_import as di
from truecolortools.database import ObjectName

# TCT was designed for the optical-to-mid-infrared range. AstroColor's own
# grid limit is much wider (meters); keeping TCT's 3 μm cap avoids allocating
# tens of thousands of points for far-infrared tails in FITS files.
TCT_MAX_WAVELENGTH_NM = 3000


# AstroColor is the source of truth for filter lookup. TCT keeps downloaded
# profiles and hand-maintained profiles in its working directory.
def configure_filter_paths(base_dir: str | Path | None = None) -> None:
    """
    Points AstroColor at TCT's local filter folders.

    Args:
    - base_dir: project working directory; the current directory by default.
    """
    root = Path.cwd() if base_dir is None else Path(base_dir)
    cached = root / 'cached_filters'
    cached.mkdir(parents=True, exist_ok=True)
    ac.Config.set_cached_filters_folder(cached)
    custom = root / 'custom_filters'
    if custom.is_dir():
        ac.Config.set_custom_filters_folder(custom)


configure_filter_paths()


def _clip_arrays_to_tct_range(
    wavelength_nm: npt.ArrayLike,
    spectral_dist: npt.ArrayLike,
    standard_deviation: npt.ArrayLike | None = None,
) -> tuple[npt.NDArray[np.floating], npt.NDArray[np.floating], npt.NDArray[np.floating] | None]:
    """ Trims parallel wavelength/brightness arrays above TCT's 3 μm limit. """
    nm = np.asarray(wavelength_nm)
    sd = np.asarray(spectral_dist)
    std = None if standard_deviation is None else np.asarray(standard_deviation)
    if nm.size == 0 or float(np.nanmax(nm)) <= TCT_MAX_WAVELENGTH_NM:
        return nm, sd, std
    mask = nm <= TCT_MAX_WAVELENGTH_NM
    nm = nm[mask]
    sd = sd[mask]
    if std is not None:
        std = std[mask]
    return nm, sd, std


def _limit_content_wavelengths(data: dict[str, Any]) -> None:
    """ Applies TCT's wavelength cap to arrays and generated database grids. """
    nm = data.get('wavelength_nm')
    if nm is not None:
        nm_array = np.asarray(nm)
        mask = nm_array <= TCT_MAX_WAVELENGTH_NM
        if not np.all(mask):
            data['wavelength_nm'] = nm_array[mask]
            for key in (
                'spectral_dist', 'uncertainty',
                'sd_geometric', 'std_geometric',
                'sd_spherical', 'std_spherical',
            ):
                values = data.get(key)
                if values is not None and np.shape(values)[:1] == (nm_array.size,):
                    data[key] = np.asarray(values)[mask]
    for key in ('nm_range', 'spectral_slope'):
        grid = data.get(key)
        if isinstance(grid, dict) and float(grid.get('stop', 0)) > TCT_MAX_WAVELENGTH_NM:
            data[key] = {**grid, 'stop': TCT_MAX_WAVELENGTH_NM}


def get_filter(name: str | float) -> ac.Filter:
    """
    Returns a filter profile by SVO FPS identifier or by wavelength in nm.

    AstroColor's `Filter.get()` accepts only SVO identifiers. TCT also allows
    numeric values as monochromatic filters, so that compatibility lives here.
    """
    if isinstance(name, str):
        try:
            wavelength = float(name)
        except ValueError:
            return ac.Filter.get(name)
        return ac.Filter.monochromatic(wavelength)
    return ac.Filter.monochromatic(float(name))


def read_spectrum_file(
    file: str | Path,
    name: object = None,
    is_emission_spectrum: bool = False,
) -> ac.Spectrum:
    """
    Reads a TCT spectrum file into an AstroColor `Spectrum`.

    TCT encodes wavelength and detector conventions in the file extension:
    `A` for angstroms, `U` for micrometers, `J` for energy density per
    frequency and `P` for photon counting. AstroColor has no file IO, so this
    adapter applies those conventions before constructing the object.

    Args:
    - file: path to a text or FITS file.
    - name: object name to attach to the spectrum.
    - is_emission_spectrum: interpret the input rows as spectral lines.
    """
    file = str(file)
    wavelength_nm, spectral_dist, standard_deviation = di.file_reader(file)
    wavelength_nm, spectral_dist, standard_deviation = _clip_arrays_to_tct_range(
        wavelength_nm, spectral_dist, standard_deviation
    )
    if wavelength_nm.size == 0:
        return ac.Spectrum.stub(name=name if name is not None else file)
    spectrum = ac.Spectrum(
        wavelength_nm,
        spectral_dist,
        standard_deviation,
        name=name if name is not None else file,
        is_emission_spectrum=is_emission_spectrum,
    )
    extension = file.split('.')[-1].upper()
    if 'J' in extension:
        spectrum = spectrum.convert_from_energy_spectral_density_per_frequency()
    elif 'P' in extension:
        spectrum = spectrum.convert_from_photon_spectral_density()
    return spectrum


def blackbody_spectrum(
    wavelength_nm: npt.ArrayLike,
    temperature: float,
    velocity: float = 0.0,
    vII: float = 0.0,
) -> ac.Spectrum:
    """
    Returns a Planck spectrum with optional Doppler and gravitational redshift.

    This is a thin adapter over `astrocolor.BlackBodyModel`; the name is
    converted to `ObjectName` because TCT's GUI translates object names.
    """
    spectrum = ac.get_spectrometry(
        ac.BlackBodyModel(temperature, velocity, vII),
        wavelength_nm,
        strictly=True,
    )
    if isinstance(spectrum, ac.Spectrum):
        spectrum.name = ObjectName(str(spectrum.name))
    return spectrum


# Solar normalization used by the "multiply by the Sun" GUI mode.
sun_norm = ac.scale_to_match_value(
    ac.sun_calspec,
    ac.Filter.get('Generic/Bessell.V'),
)


class DatabaseEntry:
    """
    A single TCT database record, backed by `astrocolor.CelestialObject`.

    The wrapper adds the two pieces of metadata that AstroColor deliberately
    leaves to the database layer:

    - `tags`: the categorization strings used by the GUI and table generator;
    - `file`, `file_geometric`, `file_spherical`: paths to spectra stored
      outside JSON5. They are read into `spectral_dist`, `sd_geometric` and
      `sd_spherical` respectively before the AstroColor object is created.

    Attributes:
    - `name` (ObjectName): parsed object name.
    - `tags` (list[str]): database tags.
    - `celestial_object` (ac.CelestialObject): parsed physical object.
    """

    def __init__(self, name: object, content: Mapping[str, Any]) -> None:
        """
        Args:
        - name: TCT object name, `ObjectName` or a raw string.
        - content: a value from the JSON5 spectra database.
        """
        self.name = ObjectName.as_ObjectName(name)
        self.tags: list[str] = list(content.get('tags', []))
        self.celestial_object = ac.CelestialObject(
            name=self.name,
            **self._expand_content(content),
        )

    @staticmethod
    def _expand_content(content: Mapping[str, Any]) -> dict[str, Any]:
        """ Expands TCT-only metadata and file keys into AstroColor arguments. """
        data = dict(content)
        data.pop('tags', None)

        file = data.pop('file', None)
        if file:
            # `is_emission_spectrum` is applied while reading the file, so it
            # must not be applied a second time by CelestialObject.
            is_emission = bool(data.pop('is_emission_spectrum', False))
            if is_emission:
                # Emission-line files must still be rendered as emissive.
                data['is_emissive'] = True
            spectrum = read_spectrum_file(
                file,
                name=file,
                is_emission_spectrum=is_emission,
            )
            data['wavelength_nm'] = spectrum.wavelength_nm
            data['spectral_dist'] = spectrum.spectral_dist
            if spectrum.standard_deviation is not None:
                data['uncertainty'] = spectrum.standard_deviation

        for file_key, value_key, std_key in (
            ('file_geometric', 'sd_geometric', 'std_geometric'),
            ('file_spherical', 'sd_spherical', 'std_spherical'),
        ):
            file = data.pop(file_key, None)
            if not file:
                continue
            spectrum = read_spectrum_file(file, name=file)
            data[value_key] = spectrum.spectral_dist
            if std_key not in data and spectrum.standard_deviation is not None:
                data[std_key] = spectrum.standard_deviation
            # A standalone albedo file also defines the spectral grid when
            # the entry has no primary spectrum or filter list of its own.
            if not any(
                key in data
                for key in ('wavelength_nm', 'nm_range', 'spectral_slope', 'filters', 'color_indices')
            ):
                data['wavelength_nm'] = spectrum.wavelength_nm

        _limit_content_wavelengths(data)
        return data

    @property
    def is_emissive(self) -> bool:
        """ Whether the object is rendered without albedo scaling. """
        return self.celestial_object.is_emissive

    def get_spectrum(
        self,
        albedo_type: str | None = None,
    ) -> tuple[ac.Spectrum | ac.Photospectrum, bool | None]:
        """
        Returns the requested albedo spectrum and its estimation status.

        This is a convenience alias for `CelestialObject.get_spectral_data()`.
        """
        return self.celestial_object.get_spectral_data(albedo_type)  # pyright: ignore[reportArgumentType]

    def __repr__(self) -> str:
        return f'DatabaseEntry(name={self.name!r}, tags={self.tags!r})'
