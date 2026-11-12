""" Tests for color-table layout and text fitting. """

from pathlib import Path

import astrocolor as ac
from PIL import ImageFont

import truecolortools.database as db
from truecolortools.database import ObjectName
from truecolortools.table_generator import FONT_DIR, generate_table, line_splitter


def test_line_splitter():
    object_font = ImageFont.truetype(
        str(FONT_DIR / 'FiraSansExtraCondensed-Regular.ttf'),
        20,
        layout_engine=ImageFont.Layout.BASIC,
    )
    assert line_splitter('Sun', object_font, 114) == ['Sun']
    assert line_splitter('2MASSW J0746425+200032', object_font, 114) == ['2MASSW', 'J0746425+', '+200032']
    assert line_splitter('Rings of Uranus', object_font, 114) == ['Rings of', 'Uranus']
    assert line_splitter('Gǃkúnǁʼhòmdímà', object_font, 114) == ['Gǃkúnǁʼhòmdí-', 'mà']
    assert line_splitter('Honda–Mrkos–Pajdušáková', object_font, 114) == ['Honda–', '–Mrkos–', '–Pajdušáková']
    assert line_splitter('Churyumov–Gerasimenko', object_font, 114) == ['Churyumov–', '–Gerasimenko']
    assert line_splitter('Churyumov–Gerasimenko³⁰', object_font, 114) == ['Churyumov–', '–Gerasimenk-', 'o³⁰']
    assert line_splitter('Чурюмова — Герасименко³⁰', object_font, 114) == ['Чурюмова —', 'Герасименко', '³⁰']
    assert line_splitter('Tschurjumow-Gerassimenko³⁰', object_font, 114) == ['Tschurjumow-', '-Gerassimenk-', 'o³⁰']
    assert line_splitter('Бернардинелли — Бернштейна', object_font, 114) == ['Бернардинел-', 'ли —', 'Бернштейна']
    assert line_splitter('136472', object_font, 32) == ['136-', '472']


def test_generate_table(tmp_path: Path):
    content = {
        ObjectName('Test object'): {
            'tags': ['featured'],
            'wavelength_nm': [500, 505, 510, 515],
            'spectral_dist': [1, 2, 3, 2],
            'is_albedo': True,
        }
    }
    generate_table(
        objectsDB=content,
        tag='featured',
        color_system=ac.ColorSystem('sRGB', 'Illuminant E'),
        gamma_correction=True,
        maximize_brightness=False,
        scale_factor=1,
        geom_albedo=True,
        sun_multiply=False,
        folder=str(tmp_path),
        extension='png',
        lang='en',
    )
    files = list(tmp_path.glob('TCT_*.png'))
    assert len(files) == 1
    assert files[0].stat().st_size > 0


def test_database_import(tmp_path: Path):
    file = tmp_path / 'db.json5'
    file.write_text(
        """
        {
            'Ref': ['Source', 'https://example.org'],
            'Object': {tags: ['featured', 'group/sub'], spectral_dist: [1], wavelength_nm: [500]},
        }
        """,
        encoding='UTF-8',
    )
    objects, references = db.import_folder(str(tmp_path))
    assert len(objects) == 1
    assert 'Ref' in references
    assert db.tag_list(objects) == ['ALL', 'featured', 'group', 'group/sub']
