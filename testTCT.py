import unittest
from numpy.testing import assert_equal, assert_allclose

from src.core import *
from src.data_processing import database_parser


class TestTCT(unittest.TestCase):

    def setUp(self):
        self.sun = Spectrum.from_file('spectra/files/CALSPEC/sun_reference_stis_002.fits', name='Sun') # W / (m² nm)
        self.vega = Spectrum.from_file('spectra/files/CALSPEC/alpha_lyr_stis_011.fits', name='Vega') # W / (m² nm)
        self.v = get_filter('Generic_Bessell.V')
        self.ubv = FilterSystem.from_list(('Generic_Bessell.U', 'Generic_Bessell.B', 'Generic_Bessell.V'), name='UBV')
    
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
        Spectrum.stub() @ Spectrum.stub()
        Spectrum.stub() @ FilterSystem.stub()
        SpectralCube.stub() @ Spectrum.stub()
        SpectralCube.stub() @ FilterSystem.stub()
        Photospectrum.stub() @ Spectrum.stub()
        Photospectrum.stub() @ FilterSystem.stub()
        PhotospectralCube.stub() @ Spectrum.stub()
        PhotospectralCube.stub() @ FilterSystem.stub()

    def test_convolution(self):
        assert_allclose(self.vega @ self.v, 3.626192e-11, rtol=0.01)
        assert_allclose((self.vega @ self.ubv).br, [4.192070e-11, 6.478653e-11, 3.626192e-11], rtol=0.01)
        assert_allclose(self.vega @ self.v, (self.vega * self.v).integrate(), rtol=0.01)
        assert_allclose((self.vega @ self.ubv).br, (self.vega * self.ubv).integrate(), rtol=0.01)
    
    def test_multiplication(self):
        assert_allclose((self.v * self.vega).mean_nm(), 544.601418, rtol=0.01) # 544.543 in SVO filter service
        assert_allclose((self.ubv * self.vega).mean_nm(), [366.764603, 435.741381, 544.601418], rtol=0.01)
        assert_allclose(self.vega * 2 @ self.v, self.vega @ self.v * 2, rtol=0.01)
        assert_allclose((self.vega * 2 @ self.ubv).br, (self.vega @ self.ubv * 2).br, rtol=0.01)
    
    def test_division(self):
        assert_allclose((self.v / self.vega).mean_nm(), 558.681024, rtol=0.01)
        assert_allclose((self.ubv / self.vega).mean_nm(), [356.283866, 447.589411, 558.681024], rtol=0.01)
        assert_allclose((self.sun / self.sun.nm).mean_nm(), 670.9781529, rtol=0.01)
        assert_allclose((self.ubv / self.ubv.nm).mean_nm(), [359.158258, 438.480057, 548.890305], rtol=0.01)
    
    def test_normalization(self):
        assert_allclose(self.vega @ (self.v * 2).normalize(), self.vega @ self.v, rtol=0.01)
        assert_allclose((self.vega @ (self.ubv * 2).normalize()).br, (self.vega @ self.ubv).br, rtol=0.01)
    
    def test_filter_edges(self):
        self.assertEqual(self.v.br[0], 0.)
        self.assertEqual(self.v.br[-1], 0.)
        extrapolated_v = self.v.to_scope(visible_range)
        self.assertEqual(extrapolated_v.br[0], 0.)
        self.assertEqual(extrapolated_v.br[-1], 0.)
    
    def test_extrapolation_flat_spectrum(self):
        nm = np.arange(500, 701, 5)
        spectrum = Spectrum(nm, np.ones_like(nm))
        assert_equal(spectrum.to_scope(visible_range, crop=True).br, np.ones(visible_range.size))
    
    def test_extrapolation_flat_photospectrum(self):
        photospectrum = Photospectrum(self.ubv, (1, 1, 1), name='test photospectrum')
        assert_equal(photospectrum.to_scope(visible_range, crop=True).br, np.ones(visible_range.size))
    
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


unittest.main()