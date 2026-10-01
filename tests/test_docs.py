# TP-DOC / TP-STRUCT / TP-DOMAIN-02 (packaging, structure, about identity)
from __future__ import print_function, unicode_literals

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


class TestDocsStruct(unittest.TestCase):
    def test_tp_doc_01_readme_version_matches_package(self):
        """TP-DOC-01: README version badge matches package version."""
        import VideoSpeed

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        badge = "Version-{}".format(VideoSpeed.__version__)
        self.assertIn(badge, readme)
        self.assertIn("video-speed --file", readme)
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn("ChronicleLogger>=1.3.1", pyproject)
        self.assertNotIn("py-tui", pyproject)

    def test_tp_struct_01_ship_ssot_is_package_cli(self):
        """TP-STRUCT-01: ship SSOT is src/VideoSpeed/cli.py, not bootstrap-old."""
        ship = ROOT / "src" / "VideoSpeed" / "cli.py"
        archive = ROOT / "src" / "VideoSpeed" / "cli.bootstrap-old.py"
        self.assertTrue(ship.is_file())
        self.assertTrue(archive.is_file())
        ship_text = ship.read_text(encoding="utf-8")
        self.assertIn("def main(", ship_text)
        self.assertIn("promote_file", ship_text)
        self.assertIn("shutil.move", ship_text)

    def test_tp_domain_02_about_version_honest(self):
        """TP-DOMAIN-02: about/version identity fields honest."""
        import VideoSpeed
        from VideoSpeed import cli

        self.assertEqual(cli.APP_NAME, "VideoSpeed")
        self.assertEqual(cli.CONSOLE_NAME, "video-speed")
        self.assertEqual(cli._PKG_VERSION, VideoSpeed.__version__)

    def test_tp_doc_02_version_match_is_suite_not_import(self):
        """TP-DOC-02: version equality is a suite check, not an import raise."""
        import VideoSpeed
        from VideoSpeed import cli

        self.assertEqual(cli._PKG_VERSION, VideoSpeed.__version__)
        ship = (ROOT / "src" / "VideoSpeed" / "cli.py").read_text(encoding="utf-8")
        self.assertNotIn(
            'raise RuntimeError("package version SSOT mismatch")',
            ship,
        )


if __name__ == "__main__":
    unittest.main()
