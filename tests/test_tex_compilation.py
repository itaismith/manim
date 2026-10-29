import importlib.util
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch
from diskcache import Cache

if importlib.util.find_spec("manimpango") is None:
    sys.modules["manimpango"] = types.ModuleType("manimpango")

from manimlib import Tex
from manimlib.config import manim_config
from manimlib.mobject.svg.tex_mobject import get_tex_mob_scale_factor
from manimlib.utils.tex_file_writing import LatexError, full_tex_to_svg, latex_to_svg


class TestTexCompilation(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.latex_cache = patch.object(manim_config.directories, "latex_cache", self.temp_dir.name)
        self.latex_cache.start()
        self.addCleanup(self.latex_cache.stop)
        disk_cache = Cache(str(Path(self.temp_dir.name) / "cache"))
        self.addCleanup(disk_cache.close)
        self.cache = patch("manimlib.utils.cache._cache", disk_cache)
        self.cache.start()
        self.addCleanup(self.cache.stop)
        latex_to_svg.cache_clear()
        get_tex_mob_scale_factor.cache_clear()
        self.addCleanup(latex_to_svg.cache_clear)
        self.addCleanup(get_tex_mob_scale_factor.cache_clear)

    def test_failed_compilation_after_success(self):
        Tex("0")
        self.assertTrue((Path(self.temp_dir.name) / "working.dvi").exists())
        with self.assertRaisesRegex(LatexError, "Undefined control sequence"):
            Tex(r"\badcommand{x}")

    def test_empty_tex(self):
        Tex("")

    def test_failed_compilation_without_log(self):
        dvi_path = Path(self.temp_dir.name) / "working.dvi"
        dvi_path.write_bytes(b"stale")
        with patch("manimlib.utils.tex_file_writing.subprocess.run") as run:
            run.return_value.returncode = 1
            with self.assertRaisesRegex(LatexError, "LaTeX compilation failed"):
                full_tex_to_svg("bad input")
            self.assertEqual(run.call_count, 1)


if __name__ == "__main__":
    unittest.main()
