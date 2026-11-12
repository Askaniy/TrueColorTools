""" Tests for the TCT database layer and DatabaseEntry. """

import json5
import numpy as np
import pytest

from truecolortools import core
from truecolortools.database import ObjectName


def test_object_name_parsing():
    obj_name = ObjectName('HZ43(8) (DA) | CALSPEC')
    assert obj_name.name() == 'HZ43(8)'
    assert obj_name.info() == 'DA'

    obj_name = ObjectName('HD 101452 (A2/3) | CALSPEC')
    assert obj_name.name() == 'HD 101452'
    assert obj_name.info() == 'A2/3'

    obj_name = ObjectName('(C/1900 AA1) 2099 AA9999')
    assert obj_name() == 'C/1900 AA₁ (2099 AA₉₉₉₉)'


def test_object_name_translation():
    assert ObjectName('Iocaste').name('ru') == 'Иокасте'
    assert ObjectName('PanSTARRS').name('ru') == 'PanSTARRS'


def test_database_entry_continuous_spectrum():
    content = {
        'tags': ['test', 'minor body'],
        'wavelength_nm': [500, 505, 510, 515],
        'spectral_dist': [1, 2, 3, 2],
        'geometric_albedo': ['Generic/Bessell.V', [0.5, 0.01]],
        'spherical_albedo': ['Generic/Bessell.V', 0.2],
    }
    entry = core.DatabaseEntry(ObjectName('Test object'), content)
    assert entry.name == ObjectName('Test object')
    assert entry.tags == ['test', 'minor body']
    assert not entry.is_emissive

    geometric = entry.celestial_object.spectral_data_geometric
    spherical = entry.celestial_object.spectral_data_spherical
    unscaled = entry.celestial_object.spectral_data_unscaled
    assert geometric is not None
    assert spherical is not None
    assert unscaled is not None
    spectrum, estimated = entry.get_spectrum('geometric')
    assert spectrum is geometric
    assert estimated is False
    assert entry.get_spectrum('spherical')[0] is spherical
    assert entry.get_spectrum(None)[0] is unscaled


def test_database_entry_file_expansion(tmp_path):
    file = tmp_path / 'spectrum.txt'
    file.write_text('500 1\n505 2\n510 3\n', encoding='UTF-8')
    entry = core.DatabaseEntry(
        'File object',
        {'tags': ['file'], 'file': str(file)},
    )
    assert entry.tags == ['file']
    assert entry.celestial_object.spectral_data_unscaled is not None
    np.testing.assert_allclose(
        entry.celestial_object.spectral_data_unscaled.spectral_dist,
        [1, 2, 3],
    )


def test_database_entry_geometric_and_spherical_files(tmp_path):
    geometric_file = tmp_path / 'geometric.txt'
    geometric_file.write_text('500 0.1\n505 0.2\n510 0.3\n', encoding='UTF-8')
    spherical_file = tmp_path / 'spherical.txt'
    spherical_file.write_text('500 0.05\n505 0.1\n510 0.15\n', encoding='UTF-8')
    entry = core.DatabaseEntry(
        'Two albedos',
        {
            'tags': ['file'],
            'wavelength_nm': [500, 505, 510],
            'file_geometric': str(geometric_file),
            'file_spherical': str(spherical_file),
        },
    )
    geometric = entry.celestial_object.spectral_data_geometric
    spherical = entry.celestial_object.spectral_data_spherical
    assert geometric is not None
    assert spherical is not None
    np.testing.assert_allclose(geometric.spectral_dist, [0.1, 0.2, 0.3])
    np.testing.assert_allclose(spherical.spectral_dist, [0.05, 0.1, 0.15])


def test_expand_content_maps_file_keys(tmp_path):
    primary = tmp_path / 'primary.txt'
    primary.write_text('500 1\n505 2\n510 3\n', encoding='UTF-8')
    geometric = tmp_path / 'geometric.txt'
    geometric.write_text('500 0.1\n505 0.2\n510 0.3\n', encoding='UTF-8')
    spherical = tmp_path / 'spherical.txt'
    spherical.write_text('500 0.05\n505 0.1\n510 0.15\n', encoding='UTF-8')

    expanded = core.DatabaseEntry._expand_content({  # pyright: ignore[reportPrivateUsage]
        'tags': ['discarded'],
        'file': str(primary),
        'file_geometric': str(geometric),
        'file_spherical': str(spherical),
    })

    assert 'tags' not in expanded
    assert 'file' not in expanded
    assert 'file_geometric' not in expanded
    assert 'file_spherical' not in expanded
    assert 'spectral_dist' in expanded
    assert 'sd_geometric' in expanded
    assert 'sd_spherical' in expanded
    np.testing.assert_allclose(expanded['spectral_dist'], [1, 2, 3])
    np.testing.assert_allclose(expanded['sd_geometric'], [0.1, 0.2, 0.3])
    np.testing.assert_allclose(expanded['sd_spherical'], [0.05, 0.1, 0.15])


def test_database_entry_emission_file_is_not_applied_twice(tmp_path):
    file = tmp_path / 'lines.txt'
    file.write_text('500 1\n600 2\n', encoding='UTF-8')
    entry = core.DatabaseEntry(
        'Emission lines',
        {
            'tags': ['emission'],
            'file': str(file),
            'is_emission_spectrum': True,
        },
    )
    assert entry.is_emissive
    spectrum = entry.get_spectrum(None)[0]
    assert spectrum.wavelength_nm[0] < 500
    assert spectrum.wavelength_nm[-1] > 600
    assert spectrum.spectral_dist.max() > 0


@pytest.mark.parametrize(
    ('database_file', 'object_name'),
    [
        ('spectra/01_stars.json5', 'Vega (A0 V) | CALSPEC'),
        ('spectra/02_solar_system.json5', 'Phoebe (S IX) | Grav2003, Miller2011'),
        ('spectra/02_solar_system.json5', 'Venus: Synthetic spectrum | VPL, Mallama2017a'),
    ],
)
def test_real_database_entries(database_file: str, object_name: str):
    with open(database_file, encoding='UTF-8') as file:
        content = json5.load(file)[object_name]
    entry = core.DatabaseEntry(ObjectName(object_name), content)
    spectrum, _ = entry.get_spectrum('geometric')
    assert spectrum.spectral_size > 0
    assert np.all(np.isfinite(spectrum.spectral_dist))
