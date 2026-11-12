""" Tests for TCT's thin adapters over AstroColor. """

from pathlib import Path

import astrocolor as ac
import numpy as np
import pytest

from truecolortools import core
from truecolortools.database import ObjectName


def test_filter_paths_are_configured():
    assert ac.Config.get_cached_filters_folder() == Path.cwd() / 'cached_filters'
    assert ac.Config.get_custom_filters_folder() == Path.cwd() / 'custom_filters'


def test_get_filter_by_identifier():
    v_filter = core.get_filter('Generic/Bessell.V')
    assert isinstance(v_filter, ac.Filter)
    assert v_filter.spectral_dist[0] == 0
    assert v_filter.spectral_dist[-1] == 0
    np.testing.assert_allclose(v_filter.integrate(), 1.0)


def test_get_filter_by_wavelength():
    for wavelength in (555, 555.5):
        monochromatic = core.get_filter(wavelength)
        assert isinstance(monochromatic, ac.Filter)
        np.testing.assert_allclose(monochromatic.integrate(), 1.0, rtol=1e-12)
        np.testing.assert_allclose(monochromatic.mean_nm(), wavelength, rtol=1e-12)


def test_read_spectrum_file(tmp_path: Path):
    file = tmp_path / 'spectrum.txt'
    file.write_text('500 1\n505 2\n510 3\n', encoding='UTF-8')
    spectrum = core.read_spectrum_file(file)
    assert spectrum.wavelength_nm[0] == 500
    assert spectrum.wavelength_nm[-1] == 510
    np.testing.assert_allclose(spectrum.spectral_dist, [1, 2, 3])


def test_read_spectrum_file_angstroms(tmp_path: Path):
    file = tmp_path / 'spectrum.txtA'
    file.write_text('5000 1\n5050 2\n5100 3\n', encoding='UTF-8')
    spectrum = core.read_spectrum_file(file)
    assert spectrum.wavelength_nm[0] == 500
    assert spectrum.wavelength_nm[-1] == 510


def test_wavelength_cap(tmp_path: Path):
    file = tmp_path / 'spectrum.txt'
    file.write_text('500 1\n1000 2\n3000 3\n4000 4\n', encoding='UTF-8')
    spectrum = core.read_spectrum_file(file)
    assert spectrum.wavelength_nm[-1] <= core.TCT_MAX_WAVELENGTH_NM
    assert spectrum.wavelength_nm[-1] == core.TCT_MAX_WAVELENGTH_NM


def test_blackbody_spectrum():
    spectrum = core.blackbody_spectrum(ac.visible_range, 5800)
    assert isinstance(spectrum, ac.Spectrum)
    assert isinstance(spectrum.name, ObjectName)
    assert spectrum.spectral_dist.max() > 0
    assert abs(float(spectrum.mean_nm()) - 500) < 100

    cold = core.blackbody_spectrum(ac.visible_range, 0)
    assert np.all(cold.spectral_dist == 0)


@pytest.mark.parametrize('temperature,velocity,vII', [(5800, 0, 0), (5800, 0.1, 0), (5800, 0, 0.1)])
def test_blackbody_redshift_shapes(temperature: float, velocity: float, vII: float):
    spectrum = core.blackbody_spectrum(ac.visible_range, temperature, velocity, vII)
    assert spectrum.spectral_size == ac.visible_range.size
    assert np.all(np.isfinite(spectrum.spectral_dist))
