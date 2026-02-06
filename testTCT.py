import unittest
import numpy as np

import src.core as core
import src.auxiliary as aux
from src.table_generator import ImageFont, line_splitter


class TestTCT(unittest.TestCase):

    def setUp(self):
        self.sun = core.Spectrum.from_file('spectra/files/CALSPEC/sun_reference_stis_002.fits', name='Sun') # W / (m² nm)
        self.vega = core.Spectrum.from_file('spectra/files/CALSPEC/alpha_lyr_stis_011.fits', name='Vega') # W / (m² nm)
        self.v = core.get_filter('Generic_Bessell.V')
        self.ubv = core.FilterSystem.from_list(('Generic_Bessell.U', 'Generic_Bessell.B', 'Generic_Bessell.V'), name='UBV')
        self.r = core.get_filter('StilesBurch2deg.r')
        self.rgb = core.FilterSystem.from_list(('StilesBurch2deg.r', 'StilesBurch2deg.g', 'StilesBurch2deg.b'), name='RGB')

    def test_mean_nm(self):
        np.testing.assert_allclose(self.sun.mean_nm(), 857.052056, rtol=0.01)
        np.testing.assert_allclose(self.vega.mean_nm(), 510.428463, rtol=0.01)
        np.testing.assert_allclose(self.v.mean_nm(), 551.204273, rtol=0.01) # 551.210 in SVO Filter Profile Service
        np.testing.assert_allclose(self.ubv.mean_nm(), [360.507105, 441.301389, 551.204273], rtol=0.01)

    def test_sd_of_nm(self):
        np.testing.assert_allclose(self.sun.sd_of_nm(), 468.978657, rtol=0.01)
        np.testing.assert_allclose(self.vega.sd_of_nm(), 353.430263, rtol=0.01)
        np.testing.assert_allclose(self.v.sd_of_nm(), 36.354015, rtol=0.01)
        np.testing.assert_allclose(self.ubv.sd_of_nm(), [21.932217, 35.816641, 36.354015], rtol=0.01)

    def test_stub_and_convolution_possibility(self):
        self.assertIsInstance(core.Spectrum.stub() @ core.Spectrum.stub(), tuple)
        self.assertIsInstance(core.Spectrum.stub() @ core.FilterSystem.stub(), core.Photospectrum)
        self.assertIsInstance(core.SpectralSquare.stub() @ core.Spectrum.stub(), tuple)
        self.assertIsInstance(core.SpectralSquare.stub() @ core.FilterSystem.stub(), core.PhotospectralSquare)
        self.assertIsInstance(core.SpectralCube.stub() @ core.Spectrum.stub(), tuple)
        self.assertIsInstance(core.SpectralCube.stub() @ core.FilterSystem.stub(), core.PhotospectralCube)
        self.assertIsInstance(core.Photospectrum.stub() @ core.Spectrum.stub(), tuple)
        self.assertIsInstance(core.Photospectrum.stub() @ core.FilterSystem.stub(), core.Photospectrum)
        self.assertIsInstance(core.PhotospectralSquare.stub() @ core.Spectrum.stub(), tuple)
        self.assertIsInstance(core.PhotospectralSquare.stub() @ core.FilterSystem.stub(), core.PhotospectralSquare)
        self.assertIsInstance(core.PhotospectralCube.stub() @ core.Spectrum.stub(), tuple)
        self.assertIsInstance(core.PhotospectralCube.stub() @ core.FilterSystem.stub(), core.PhotospectralCube)

    def test_convolution(self):
        np.testing.assert_allclose((self.vega @ self.v)[0], (self.vega * self.v).integrate(), rtol=0.01)
        np.testing.assert_allclose((self.vega @ self.ubv).br, (self.vega * self.ubv).integrate(), rtol=0.01)

    def test_vega_system_zero_points(self):
        # 0.25% agreement with SVO Filter Profile Service calculations:
        np.testing.assert_allclose((self.vega @ self.v)[0], 3.62708e-11, rtol=0.0025)
        # 3.5% agreement with SVO Filter Profile Service calculations:
        np.testing.assert_allclose((self.vega @ self.ubv).br, [3.96526e-11, 6.13268e-11, 3.62708e-11], rtol=0.035)

    def test_addition(self):
        np.testing.assert_allclose((self.vega + self.vega).br, (self.vega * 2).br, rtol=0.01)

    def test_multiplication(self):
        np.testing.assert_allclose((self.v * self.vega).mean_nm(), 544.601418, rtol=0.01) # 544.543 in SVO Filter Profile Service
        np.testing.assert_allclose((self.ubv * self.vega).mean_nm(), [366.764603, 435.741381, 544.601418], rtol=0.01)
        np.testing.assert_allclose((self.vega * 2 @ self.v)[0], (self.vega @ self.v)[0] * 2, rtol=0.01)
        np.testing.assert_allclose((self.vega * 2 @ self.ubv).br, (self.vega @ self.ubv * 2).br, rtol=0.01)

    def test_division(self):
        np.testing.assert_allclose((self.v / self.vega).mean_nm(), 558.681024, rtol=0.01)
        np.testing.assert_allclose((self.ubv / self.vega).mean_nm(), [356.283866, 447.589411, 558.681024], rtol=0.01)
        np.testing.assert_allclose((self.sun / self.sun.nm).mean_nm(), 670.9781529, rtol=0.01)
        np.testing.assert_allclose((self.ubv / self.ubv.nm).mean_nm(), [359.158258, 438.480057, 548.890305], rtol=0.01)

    def test_normalization(self):
        np.testing.assert_allclose((self.vega @ (self.v * 2).normalize())[0], (self.vega @ self.v)[0], rtol=0.01)
        np.testing.assert_allclose((self.vega @ (self.ubv * 2).normalize()).br, (self.vega @ self.ubv).br, rtol=0.01)

    def test_spectrum_from_nm(self):
        spectrum = core.Spectrum.from_nm(555.5)
        np.testing.assert_allclose(spectrum.integrate(), 1.0, rtol=1e-10)
        np.testing.assert_allclose(spectrum.mean_nm(), 555.5, rtol=1e-10)
        spectrum = core.Spectrum.from_nm(555)
        np.testing.assert_allclose(spectrum.integrate(), 1.0, rtol=1e-10)
        np.testing.assert_allclose(spectrum.mean_nm(), 555, rtol=1e-10)

    def test_filter_edges(self):
        self.assertEqual(self.v.br[0], 0.)
        self.assertEqual(self.v.br[-1], 0.)
        extrapolated_v = self.v.define_on_range(core.visible_range)
        self.assertEqual(extrapolated_v.br[0], 0.)
        self.assertEqual(extrapolated_v.br[-1], 0.)

    def test_getting_profile_from_filter_system(self):
        v_there_and_back = core.FilterSystem.from_list([self.v])[0]
        np.testing.assert_allclose(v_there_and_back.nm, self.v.nm)
        np.testing.assert_allclose(v_there_and_back.br, self.v.br)

    def test_filter_system_getitem(self):
        np.testing.assert_equal(self.rgb[0].mean_nm(), self.r.mean_nm())

    def test_extrapolation_flat_spectrum(self):
        nm = np.arange(500, 701, 5)
        spectrum = core.Spectrum(nm, np.ones_like(nm))
        np.testing.assert_equal(spectrum.define_on_range(core.visible_range, crop=True).br, np.ones(core.visible_range.size))

    def test_extrapolation_flat_photospectrum(self):
        photospectrum = core.Photospectrum(self.ubv, (1, 1, 1), name='test photospectrum')
        np.testing.assert_allclose(photospectrum.define_on_range(core.visible_range, crop=True).br, np.ones(core.visible_range.size))

    def test_sd_parsing(self):
        np.testing.assert_equal(aux.parse_value_sd(0.202), (0.202, None))
        np.testing.assert_equal(aux.parse_value_sd([0.202, 0.0665]), (0.202, 0.0665))
        np.testing.assert_equal(aux.parse_value_sd([0.202, 0.084, 0.049]), (0.202, 0.0665))
        np.testing.assert_equal(aux.parse_value_sd([0.202, +0.084, -0.049]), (0.202, 0.0665))

    def test_phase_coeffitient(self):
        model = core.PhaseCoefficient({'beta': [0.032, 0.001]})
        # testing phase function input
        np.testing.assert_equal(model.phase_function(0), 1)
        np.testing.assert_equal(model.phase_function([0, 0]), 1)
        # test on Phobos from https://www.sciencedirect.com/science/article/abs/pii/0019103576901548
        np.testing.assert_allclose(model.phase_integral, (0.52, 0.03), rtol=0.2)
        # test of the phase function numerical integration
        step = 0.01 # radians
        alpha = np.arange(0, np.pi, step)
        np.testing.assert_allclose(model.phase_integral[0], 2*aux.integrate(model.phase_function(alpha)*np.sin(alpha), step, precisely=True), rtol=0.001)

    def test_exponentials(self):
        model = core.Exponentials({'A_1': 0.0539, 'mu_1': 50, 'A_2': 0.0465, 'mu_2': 5.615, 'A_3': 0.1145, 'mu_3': 0.6135})
        # testing phase function input
        np.testing.assert_equal(model.phase_function(0), 1)
        np.testing.assert_equal(model.phase_function([0, 0]), 1)
        # test of the phase function numerical integration
        step = 0.01 # radians
        alpha = np.arange(0, np.pi, step)
        np.testing.assert_allclose(model.phase_integral[0], 2*aux.integrate(model.phase_function(alpha)*np.sin(alpha), step, precisely=True), rtol=0.001)

    def test_HG(self):
        model = core.HG({'H': [10.87, 0.01], 'G': [0.42, 0.06]})
        # testing phase function input
        np.testing.assert_equal(model.phase_function(0), 1)
        np.testing.assert_equal(model.phase_function([0, 0]), 1)
        # test of the phase function numerical integration
        step = 0.01 # radians
        alpha = np.arange(0, np.pi, step)
        np.testing.assert_allclose(model.phase_integral[0], 2*aux.integrate(model.phase_function(alpha)*np.sin(alpha), step, precisely=True), rtol=0.1) # too high inaccuracy?

    def test_HG1G2(self):
        model = core.HG1G2({'G_1': [0.400906, +0.584725, -0.691005], 'G_2': [0.241104, +0.49603, -0.421077]})
        # testing phase function input
        np.testing.assert_equal(model.phase_function(0), 1)
        np.testing.assert_equal(model.phase_function([0, 0]), 1)
        # test of the phase function numerical integration
        step = 0.01 # radians
        alpha = np.arange(0, np.pi, step)
        np.testing.assert_allclose(model.phase_integral[0], 2*aux.integrate(model.phase_function(alpha)*np.sin(alpha), step, precisely=True), rtol=0.01)

    def test_hapke(self):
        model = core.Hapke({'w': 0.958, 'bo': 0.34, 'h': 0.0065, 'b': -0.599, 'c': 0.723, 'theta': 29})
        # testing phase function input
        np.testing.assert_equal(model.phase_function(0), 1)
        np.testing.assert_equal(model.phase_function([0, 0]), 1)
        # test of the phase function numerical integration
        step = 0.01 # radians
        alpha = np.arange(0, np.pi, step)
        np.testing.assert_allclose(model.phase_integral[0], 2*aux.integrate(model.phase_function(alpha)*np.sin(alpha), step, precisely=True), rtol=0.001)

    def test_color_system_reversibility(self):
        srgb = core.ColorSystem('sRGB')
        xyz = core.ColorSystem('CIE 1931 XYZ')
        color0 = core.ColorObject.from_spectral_data(self.sun) # XYZ
        color1 = color0.to_color_system(srgb)
        color2 = color1.to_color_system(xyz)
        np.testing.assert_allclose(color0.to_array(), color2.to_array(), rtol=1e-13)

    def test_adaptation_white_point(self):
        rgb = core.ColorSystem('CIE 1931 RGB')
        rgb_ = core.ColorSystem('CIE 1931 RGB', adaptation_white_point='Illuminant E')
        color0 = core.ColorObject.from_spectral_data(self.sun) # XYZ
        color1 = color0.to_color_system(rgb)
        color2 = color1.to_color_system(rgb_)
        np.testing.assert_allclose(color1.to_array(), color2.to_array(), rtol=1e-13)

    def test_name_parsing(self):
        obj_name = core.ObjectName('HZ43(8) (DA) | CALSPEC')
        np.testing.assert_equal(obj_name.name(), 'HZ43(8)')
        np.testing.assert_equal(obj_name.info(), 'DA')
        obj_name = core.ObjectName('HD 101452 (A2/3) | CALSPEC')
        np.testing.assert_equal(obj_name.name(), 'HD 101452')
        np.testing.assert_equal(obj_name.info(), 'A2/3')
        obj_name = core.ObjectName('(C/1900 AA1) 2099 AA9999')
        np.testing.assert_equal(obj_name(), 'C/1900 AA₁ (2099 AA₉₉₉₉)')

    def test_name_translation(self):
        np.testing.assert_equal(core.ObjectName('Iocaste').name('ru'), 'Иокасте') # not "Иоcaste"
        np.testing.assert_equal(core.ObjectName('PanSTARRS').name('ru'), 'PanSTARRS') # not "ПанSTARRS"

    def test_db(self):
        db = {
            'Phoebe (S IX) | Grav2003, Miller2011': {
                'tags': ['featured', 'Solar System/Saturnian system', 'natural satellite/irregular moon'],
                'photometric_system': 'Generic_Bessell',
                'color_indices': {'B-V': 0.63, 'V-R': 0.35, 'V-I': 0.64},
                'calibration_system': 'Vega',
                'is_reflecting_sunlight': True,
                'geometric_albedo': ['Generic_Bessell.V', [0.0857, 0.0022]],
                'spherical_albedo': ['Generic_Bessell.V', [0.0267, 0.0083]],
            },
            'Nereid (N II) | Schaefer2000, Kiss2016, Thomas1991': {
                'tags': ['featured', 'Solar System/Neptunian system', 'natural satellite/irregular moon'],
                'photometric_system': 'Generic_Bessell',
                'filters': ['U', 'B', 'V', 'R', 'I'],
                'br': [0.90, 0.93, 1, 1.13, 0.99],
                'geometric_albedo': ['Generic_Bessell.V', [0.24, 0.02]],
                'phase_integral': 0.5,
            },
        }
        for key, value in db.items():
            body = core.database_parser(key, value)

    def test_line_splitter(self):
        object_font = ImageFont.truetype('src/fonts/FiraSansExtraCondensed-Regular.ttf', 20, layout_engine=ImageFont.Layout.BASIC)
        self.assertEqual(line_splitter('Sun', object_font, 114), ['Sun'])
        self.assertEqual(line_splitter('2MASSW J0746425+200032', object_font, 114), ['2MASSW', 'J0746425+', '+200032'])
        self.assertEqual(line_splitter('Rings of Uranus', object_font, 114), ['Rings of', 'Uranus'])
        self.assertEqual(line_splitter('Gǃkúnǁʼhòmdímà', object_font, 114), ['Gǃkúnǁʼhòmdí-', 'mà'])
        self.assertEqual(line_splitter('Honda–Mrkos–Pajdušáková', object_font, 114), ['Honda–', '–Mrkos–', '–Pajdušáková'])
        self.assertEqual(line_splitter('Churyumov–Gerasimenko', object_font, 114), ['Churyumov–', '–Gerasimenko'])
        self.assertEqual(line_splitter('Churyumov–Gerasimenko³⁰', object_font, 114), ['Churyumov–', '–Gerasimenk-', 'o³⁰'])
        self.assertEqual(line_splitter('Чурюмова — Герасименко³⁰', object_font, 114), ['Чурюмова —', 'Герасименко', '³⁰'])
        self.assertEqual(line_splitter('Tschurjumow-Gerassimenko³⁰', object_font, 114), ['Tschurjumow-', '-Gerassimenk-', 'o³⁰'])
        self.assertEqual(line_splitter('Бернардинелли — Бернштейна', object_font, 114), ['Бернардинел-', 'ли —', 'Бернштейна'])
        # ("Бернардинелл-" doesn't fit the square)
        self.assertEqual(line_splitter('136472', object_font, 32), ['136-', '472'])

unittest.main()
