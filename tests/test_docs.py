# TP-DOC / TP-STRUCT / TP-DOMAIN-02 (packaging, structure, about identity)
from __future__ import print_function, unicode_literals

import ast
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
        stage_text = (ROOT / "src" / "VideoSpeed" / "file_stage.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("def main(", ship_text)
        self.assertIn("class Cli", ship_text)
        self.assertIn("def promote_file(", stage_text)
        self.assertIn("shutil.move", stage_text)

    def test_tp_domain_02_about_version_honest(self):
        """TP-DOMAIN-02: about/version identity fields honest."""
        import VideoSpeed
        from VideoSpeed import cli

        self.assertEqual(cli.Cli.APP_NAME, "VideoSpeed")
        self.assertEqual(cli.Cli.CONSOLE_NAME, "video-speed")
        self.assertEqual(cli.Cli._PKG_VERSION, VideoSpeed.__version__)

    def test_tp_doc_02_version_match_is_suite_not_import(self):
        """TP-DOC-02: version equality is a suite check, not an import raise."""
        import VideoSpeed
        from VideoSpeed import cli

        self.assertEqual(cli.Cli._PKG_VERSION, VideoSpeed.__version__)
        ship = (ROOT / "src" / "VideoSpeed" / "cli.py").read_text(encoding="utf-8")
        self.assertNotIn(
            'raise RuntimeError("package version SSOT mismatch")',
            ship,
        )

    def test_tp_style_01_constants_live_on_cli(self):
        """TP-STYLE-01: identity, verbs, and bounds are class Cli attributes."""
        import VideoSpeed
        from VideoSpeed import cli
        from VideoSpeed.cli import Cli

        names = (
            "_PKG_VERSION",
            "APP_NAME",
            "CONSOLE_NAME",
            "PRODUCT_VERBS",
            "LIFECYCLE_VERBS",
            "AUTHOR_NAME",
            "HOMEPAGE",
            "LAST_UPDATE",
            "DOWNLOAD_URL",
            "BASIC_USAGE",
            "RATIO_MIN",
            "RATIO_MAX",
        )
        missing = object()
        for name in names:
            self.assertIs(getattr(cli, name, missing), missing, name)
            self.assertTrue(hasattr(Cli, name), name)
        self.assertEqual(Cli.APP_NAME, "VideoSpeed")
        self.assertEqual(Cli.CONSOLE_NAME, "video-speed")
        self.assertEqual(Cli.DOWNLOAD_URL, "")
        self.assertEqual(Cli.RATIO_MIN, 20.0)
        self.assertEqual(Cli.RATIO_MAX, 200.0)
        self.assertIn("edit", Cli.PRODUCT_VERBS)
        self.assertIn("self-update", Cli.LIFECYCLE_VERBS)
        self.assertEqual(Cli._PKG_VERSION, VideoSpeed.__version__)

        ship = (ROOT / "src" / "VideoSpeed" / "cli.py").read_text(encoding="utf-8")
        tree = ast.parse(ship)
        module_targets = []
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        module_targets.append(target.id)
        for name in names:
            self.assertNotIn(name, module_targets)
        classes = [
            node for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == "Cli"
        ]
        self.assertEqual(len(classes), 1)
        class_targets = []
        for node in classes[0].body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        class_targets.append(target.id)
        for name in names:
            self.assertIn(name, class_targets)
        host = (ROOT / "src" / "VideoSpeed" / "check_system.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("from .cli import", host)
        self.assertNotIn(
            'raise RuntimeError("package version SSOT mismatch")',
            ship,
        )

    def test_tp_style_02_attribute_access_by_name(self):
        """TP-STYLE-02: ship modules and the suite do not read or write the class mapping."""
        token = "__" + "dict__"
        roots = (ROOT / "src" / "VideoSpeed", ROOT / "tests")
        for folder in roots:
            for path in folder.rglob("*.py"):
                text = path.read_text(encoding="utf-8")
                self.assertNotIn(token, text, str(path))


if __name__ == "__main__":
    unittest.main()
