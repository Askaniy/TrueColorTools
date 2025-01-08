import unittest
from numpy.testing import assert_equal, assert_allclose

from src.core import *
from src.table_generator import ImageFont, line_splitter


class TestTCT(unittest.TestCase):

    def setUp(self):
        self.sun = Spectrum.from_file('spectra/files/CALSPEC/sun_reference_stis_002.fits', name='Sun') # W / (m² nm)
        self.vega = Spectrum.from_file('spectra/files/CALSPEC/alpha_lyr_stis_011.fits', name='Vega') # W / (m² nm)
        self.v = get_filter('Generic_Bessell.V')
        self.ubv = FilterSystem.from_list(('Generic_Bessell.U', 'Generic_Bessell.B', 'Generic_Bessell.V'), name='UBV')
        self.r = get_filter('StilesBurch2deg.r')
        self.rgb = FilterSystem.from_list(('StilesBurch2deg.r', 'StilesBurch2deg.g', 'StilesBurch2deg.b'), name='RGB')
    
    def test_mean_nm(self):
        assert_allclose(self.sun.mean_nm(), 857.052056, rtol=0.01)
        assert_allclose(self.vega.mean_nm(), 504.347403, rtol=0.01)
        assert_allclose(self.v.mean_nm(), 551.204273, rtol=0.01) # 551.210 in SVO filter service
        assert_allclose(self.ubv.mean_nm(), [360.507105, 441.301389, 551.204273], rtol=0.01)

    def test_sd_of_nm(self):
        assert_allclose(self.sun.sd_of_nm(), 468.978657, rtol=0.01)
        assert_allclose(self.vega.sd_of_nm(), 353.430263, rtol=0.01)
        assert_allclose(self.v.sd_of_nm(), 36.354015, rtol=0.01)
        assert_allclose(self.ubv.sd_of_nm(), [21.932217, 35.816641, 36.354015], rtol=0.01)
    
    def test_stub_and_convolution_possibility(self):
        self.assertIsInstance(Spectrum.stub() @ Spectrum.stub(), tuple)
        self.assertIsInstance(Spectrum.stub() @ FilterSystem.stub(), Photospectrum)
        self.assertIsInstance(SpectralSquare.stub() @ Spectrum.stub(), tuple)
        self.assertIsInstance(SpectralSquare.stub() @ FilterSystem.stub(), PhotospectralSquare)
        self.assertIsInstance(SpectralCube.stub() @ Spectrum.stub(), tuple)
        self.assertIsInstance(SpectralCube.stub() @ FilterSystem.stub(), PhotospectralCube)
        self.assertIsInstance(Photospectrum.stub() @ Spectrum.stub(), tuple)
        self.assertIsInstance(Photospectrum.stub() @ FilterSystem.stub(), Photospectrum)
        self.assertIsInstance(PhotospectralSquare.stub() @ Spectrum.stub(), tuple)
        self.assertIsInstance(PhotospectralSquare.stub() @ FilterSystem.stub(), PhotospectralSquare)
        self.assertIsInstance(PhotospectralCube.stub() @ Spectrum.stub(), tuple)
        self.assertIsInstance(PhotospectralCube.stub() @ FilterSystem.stub(), PhotospectralCube)

    def test_convolution(self):
        assert_allclose((self.vega @ self.v)[0], 3.626192e-11, rtol=0.01)
        assert_allclose((self.vega @ self.ubv).br, [4.192070e-11, 6.478653e-11, 3.626192e-11], rtol=0.01)
        assert_allclose((self.vega @ self.v)[0], (self.vega * self.v).integrate(), rtol=0.01)
        assert_allclose((self.vega @ self.ubv).br, (self.vega * self.ubv).integrate(), rtol=0.01)
    
    def test_multiplication(self):
        assert_allclose((self.v * self.vega).mean_nm(), 544.601418, rtol=0.01) # 544.543 in SVO filter service
        assert_allclose((self.ubv * self.vega).mean_nm(), [366.764603, 435.741381, 544.601418], rtol=0.01)
        assert_allclose((self.vega * 2 @ self.v)[0], (self.vega @ self.v)[0] * 2, rtol=0.01)
        assert_allclose((self.vega * 2 @ self.ubv).br, (self.vega @ self.ubv * 2).br, rtol=0.01)
    
    def test_division(self):
        assert_allclose((self.v / self.vega).mean_nm(), 558.681024, rtol=0.01)
        assert_allclose((self.ubv / self.vega).mean_nm(), [356.283866, 447.589411, 558.681024], rtol=0.01)
        assert_allclose((self.sun / self.sun.nm).mean_nm(), 670.9781529, rtol=0.01)
        assert_allclose((self.ubv / self.ubv.nm).mean_nm(), [359.158258, 438.480057, 548.890305], rtol=0.01)
    
    def test_normalization(self):
        assert_allclose((self.vega @ (self.v * 2).normalize())[0], (self.vega @ self.v)[0], rtol=0.01)
        assert_allclose((self.vega @ (self.ubv * 2).normalize()).br, (self.vega @ self.ubv).br, rtol=0.01)
    
    def test_spectrum_from_nm(self):
        spectrum = Spectrum.from_nm(555.5)
        assert_allclose(spectrum.integrate(), 1.0, rtol=1e-10)
        assert_allclose(spectrum.mean_nm(), 555.5, rtol=1e-10)
        spectrum = Spectrum.from_nm(555)
        assert_allclose(spectrum.integrate(), 1.0, rtol=1e-10)
        assert_allclose(spectrum.mean_nm(), 555, rtol=1e-10)
    
    def test_filter_edges(self):
        self.assertEqual(self.v.br[0], 0.)
        self.assertEqual(self.v.br[-1], 0.)
        extrapolated_v = self.v.define_on_range(visible_range)
        self.assertEqual(extrapolated_v.br[0], 0.)
        self.assertEqual(extrapolated_v.br[-1], 0.)
    
    def test_getting_profile_from_filter_system(self):
        v_there_and_back = FilterSystem.from_list([self.v])[0]
        assert_allclose(v_there_and_back.nm, self.v.nm)
        assert_allclose(v_there_and_back.br, self.v.br)
    
    def test_filter_system_getitem(self):
        assert_equal(self.rgb[0].mean_nm(), self.r.mean_nm())
    
    def test_extrapolation_flat_spectrum(self):
        nm = np.arange(500, 701, 5)
        spectrum = Spectrum(nm, np.ones_like(nm))
        assert_equal(spectrum.define_on_range(visible_range, crop=True).br, np.ones(visible_range.size))
    
    def test_extrapolation_flat_photospectrum(self):
        photospectrum = Photospectrum(self.ubv, (1, 1, 1), name='test photospectrum')
        assert_allclose(photospectrum.define_on_range(visible_range, crop=True).br, np.ones(visible_range.size))
    
    def test_sd_parsing(self):
        assert_equal(aux.parse_value_sd(0.202), (0.202, None))
        assert_equal(aux.parse_value_sd([0.202, 0.0665]), (0.202, 0.0665))
        assert_equal(aux.parse_value_sd([0.202, 0.084, 0.049]), (0.202, 0.0665))
        assert_equal(aux.parse_value_sd([0.202, +0.084, -0.049]), (0.202, 0.0665))
    
    def test_name_parsing(self):
        obj_name = ObjectName('HZ43(8) (DA) | CALSPEC')
        assert_equal(obj_name.name(), 'HZ43(8)')
        assert_equal(obj_name.info, 'DA')
        obj_name = ObjectName('HD 101452 (A2/3) | CALSPEC')
        assert_equal(obj_name.name(), 'HD 101452')
        assert_equal(obj_name.info, 'A2/3')
    
    def test_db(self):
        db = {
            'Phoebe (S IX) | Grav2003, Miller2011': {
                'tags': ['featured', 'Solar System/Saturnian system', 'natural satellite/irregular moon'],
                'photometric_system': 'Generic_Bessell',
                'color_indices': {'B-V': 0.63, 'V-R': 0.35, 'V-I': 0.64},
                'calibration_system': 'Vega',
                'sun_is_emitter': True,
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
            body = database_parser(key, value)
    
    def test_line_splitter(self):
        object_font = ImageFont.truetype('src/fonts/FiraSansExtraCondensed-Regular.ttf', 20, layout_engine=ImageFont.Layout.BASIC)
        self.assertEqual(line_splitter('Sun', object_font, 114), ['Sun'])
        self.assertEqual(line_splitter('2MASSW J0746425+200032', object_font, 114), ['2MASSW', 'J0746425+', '+200032'])
        self.assertEqual(line_splitter('Rings of Uranus', object_font, 114), ['Rings of', 'Uranus'])
        self.assertEqual(line_splitter('Gǃkúnǁʼhòmdímà', object_font, 114), ['Gǃkúnǁʼhòmdí-', 'mà'])
        self.assertEqual(line_splitter('Honda–Mrkos–Pajdušáková', object_font, 114), ['Honda–', '–Mrkos–', '–Pajdušáková'])
        self.assertEqual(line_splitter('Churyumov–Gerasimenko', object_font, 114), ['Churyumov–', '–Gerasimenko'])
        self.assertEqual(line_splitter('Чурюмова — Герасименко³⁰', object_font, 114), ['Чурюмова —', 'Герасименко', '³⁰'])
        self.assertEqual(line_splitter('136472', object_font, 32), ['136-', '472'])

unittest.main()