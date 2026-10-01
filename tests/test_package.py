# TP-PKG — packaging / import (requirement-python-packaging, L-IMPORT-01)
from __future__ import print_function, unicode_literals

import compileall
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


class TestPackage(unittest.TestCase):
    def test_tp_pkg_01_import_without_cv2(self):
        """TP-PKG-01: import VideoSpeed without OpenCV; __version__ readable."""
        import VideoSpeed

        self.assertTrue(hasattr(VideoSpeed, "__version__"))
        self.assertRegex(VideoSpeed.__version__, r"^\d+\.\d+\.\d+")
        self.assertIsNone(sys.modules.get("cv2"))

    def test_tp_pkg_02_pyproject_version_matches(self):
        """TP-PKG-02 / TP-VER-01: triple joins to __version__ and pyproject."""
        import VideoSpeed

        joined = "{0}.{1}.{2}".format(
            VideoSpeed.MAJOR_VERSION,
            VideoSpeed.MINOR_VERSION,
            VideoSpeed.PATCH_VERSION,
        )
        self.assertEqual(VideoSpeed.__version__, joined)
        text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('version = "{}"'.format(VideoSpeed.__version__), text)
        cli = (SRC / "VideoSpeed" / "cli.py").read_text(encoding="utf-8")
        self.assertNotIn("MAJOR_VERSION =", cli)
        self.assertNotIn('_PKG_VERSION = "1.0.6"', cli)

    def test_tp_pkg_03_console_script_target(self):
        """TP-PKG-03: console script video-speed → VideoSpeed.cli:main."""
        text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn("video-speed = \"VideoSpeed.cli:main\"", text)

    def test_tp_pkg_04_py_compile(self):
        """TP-PKG-04: package modules compile."""
        pkg = SRC / "VideoSpeed"
        ok = compileall.compile_dir(str(pkg), quiet=1)
        self.assertTrue(ok)


if __name__ == "__main__":
    unittest.main()
