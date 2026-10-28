import pytest

from manimlib.utils.tex_file_writing import LatexError
from manimlib.utils.tex_file_writing import check_svg_glyph_defs

GOOD_SVG = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs><path id="g0-1" d="M 1 0 L 2 3 Z"/></defs>
<g><use xlink:href="#g0-1" x="0" y="6"/></g>
</svg>"""

BROKEN_SVG = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs/>
<g><use xlink:href="#g0-1" x="0" y="6"/></g>
</svg>"""

NO_GLYPHS_SVG = """<svg xmlns="http://www.w3.org/2000/svg"><defs/></svg>"""


def test_svg_with_defined_glyphs_passes():
    check_svg_glyph_defs(GOOD_SVG)


def test_svg_without_glyph_references_passes():
    check_svg_glyph_defs(NO_GLYPHS_SVG)


def test_svg_with_undefined_glyph_raises():
    with pytest.raises(LatexError, match="g0-1") as exc_info:
        check_svg_glyph_defs(BROKEN_SVG)
    assert "cm-super" in str(exc_info.value)
    assert "lmodern" in str(exc_info.value)


def test_svg_with_partially_undefined_glyphs_raises():
    svg = GOOD_SVG.replace(
        '<use xlink:href="#g0-1" x="0" y="6"/>',
        '<use xlink:href="#g0-1" x="0" y="6"/><use xlink:href="#g0-2" x="1" y="6"/>',
    )
    with pytest.raises(LatexError, match="g0-2"):
        check_svg_glyph_defs(svg)
