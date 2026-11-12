"""End-to-end checks of the AstroColor/TCT boundary."""

from pathlib import Path

import astrocolor as ac
import numpy as np

import truecolortools.image_processing as ip
import truecolortools.plotter as pl
from truecolortools import core, gui
from truecolortools.main import compose_plot_data


def test_spectral_objects_are_hashable():
    spectrum = ac.sun_calspec
    photometry = ac.Photospectrum(ac.FilterSet.get('Generic/Bessell.V'), [1.])
    assert hash(spectrum) == hash(ac.sun_calspec)
    assert hash(photometry) == hash(ac.Photospectrum(ac.FilterSet.get('Generic/Bessell.V'), [1.]))
    pinned = {spectrum: '#ffffff', photometry: '#000000'}
    assert spectrum in pinned
    assert photometry in pinned


def test_photometry_uses_astrocolor():
    v_filter = core.get_filter('Generic/Bessell.V')
    value, _ = ac.get_photometry(ac.sun_calspec, v_filter)
    assert value > 0
    np.testing.assert_allclose(
        value,
        ac.get_photometry(ac.sun_calspec * 2, v_filter)[0] / 2,
    )


def test_spectrometry_of_flat_spectrum():
    wavelength_nm = np.arange(500, 701, 5)
    spectrum = ac.Spectrum(wavelength_nm, np.ones_like(wavelength_nm))
    reconstructed = ac.get_spectrometry(spectrum, ac.visible_range, strictly=True)
    assert reconstructed.wavelength_nm[0] == ac.visible_range[0]
    assert reconstructed.wavelength_nm[-1] == ac.visible_range[-1]
    np.testing.assert_allclose(reconstructed.spectral_dist, 1.0)


def test_color_pipeline():
    color = ac.ColorPoint.from_spectral_data(ac.sun_calspec)
    srgb = ac.ColorSystem('sRGB', 'Illuminant E')
    converted = color.to_color_system(srgb)
    settings = ac.DisplaySettings(
        color_system=srgb,
        gamma_correction=True,
        maximize_brightness=True,
    )
    rendered = converted.render(settings)
    assert rendered.shape == (3,)
    assert np.all(rendered >= 0)
    assert np.all(rendered <= 1)
    assert converted.to_html(settings).startswith('#')


def test_color_image_png_bytes():
    image = ac.ColorImage(np.ones((3, 4, 5)), color_system=ac.xyz_color_system)
    settings = ac.DisplaySettings(
        color_system=ac.xyz_color_system,
        gamma_correction=False,
        maximize_brightness=False,
    )
    data = ip.color_image_to_bytes(image, settings)
    assert data.startswith(b'\x89PNG\r\n\x1a\n')


def test_plot_spectra(tmp_path: Path):
    spectrum = ac.sun_calspec
    fig = pl.plot_spectra(
        {spectrum: '#ffffff'}, False, False, False, 'en', (3, 2), 70
    )
    path = tmp_path / 'spectra.png'
    fig.savefig(path)
    assert path.stat().st_size > 0
    pl.close_figure(fig)


def test_plot_filters():
    filters = [core.get_filter('Generic/Bessell.V'), core.get_filter('Generic/Bessell.B')]
    fig = pl.plot_filters(
        filters,
        ac.ColorSystem('sRGB', 'Illuminant E'),
        'en',
        (3, 2),
        70,
    )
    assert len(fig.axes) == 1
    pl.close_figure(fig)


def test_blackbody_is_not_plotted_as_pinned_on_other_tab():
    database_spectrum = ac.sun_calspec
    blackbody = core.blackbody_spectrum(ac.visible_range, 3000)
    tab1_item = (database_spectrum, '#111111')
    tab3_item = (blackbody, '#222222')

    on_tab1 = compose_plot_data({}, True, 'tab1', tab1_item, tab3_item)
    assert database_spectrum in on_tab1
    assert blackbody not in on_tab1

    on_tab3 = compose_plot_data({}, True, 'tab3', tab1_item, tab3_item)
    assert blackbody in on_tab3
    assert database_spectrum not in on_tab3

    cleared = compose_plot_data({}, False, 'tab3', tab1_item, tab3_item)
    assert cleared == {}

    pinned = compose_plot_data({blackbody: '#222222'}, False, 'tab1', tab1_item, tab3_item)
    assert pinned == {blackbody: '#222222'}


def test_gui_layout_smoke():
    layout = gui.generate_layout(
        circle_size=(201, 201),
        filters_plot_size=(500, 200),
        img_preview_size=(256, 128),
        filtersDB=('Generic/Bessell.V',),
        tab3_overexposure_limit=3e5,
        color_space='sRGB',
        white_point='Illuminant E',
        gamma=True,
        brMax=False,
        brGeom=True,
        bit_depth=1,
        rounding=3,
        tab2_num=8,
        lang='en',
    )
    assert isinstance(layout, list)
    assert layout
