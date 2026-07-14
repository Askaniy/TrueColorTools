import unittest
import numpy as np

import src.core as core
import src.auxiliary as aux
from src.table_generator import ImageFont, line_splitter


class TestTCT(unittest.TestCase):

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
