# TP-DEP — pip dependency floors (requirement-python-dependency-management)
from __future__ import print_function, unicode_literals

import importlib.metadata as metadata
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CV_SPEC = "opencv-python-headless>=5.0.0.93"
LOG_SPEC = "ChronicleLogger>=1.3.1"
LAW = ROOT / "docs/requirements/requirement-python-dependency-management.md"


def _numeric_prefix(version):
    parts = []
    for piece in version.split("."):
        digits = ""
        for ch in piece:
            if ch.isdigit():
                digits += ch
            else:
                break
        if not digits:
            break
        parts.append(int(digits))
    return tuple(parts)


def _at_least(version, floor):
    got = _numeric_prefix(version)
    width = max(len(got), len(floor))
    got = got + (0,) * (width - len(got))
    floor = floor + (0,) * (width - len(floor))
    return got >= floor


class TestDependencies(unittest.TestCase):
    def _deps(self):
        data = tomllib.loads((ROOT / "pyproject.toml").read_bytes().decode("utf-8"))
        return list(data["project"]["dependencies"])

    def test_tp_dep_01_version_specifiers(self):
        """TP-DEP-01: runtime deps are present and versioned."""
        deps = self._deps()
        self.assertEqual(deps, [CV_SPEC, LOG_SPEC])
        joined = " ".join(deps)
        self.assertNotIn("py-tui", joined)
        self.assertNotIn("py_tui", joined)
        for spec in deps:
            self.assertRegex(spec, r"(==|>=|<=|~=|!=|>|<)")

    def test_tp_dep_02_headless_opencv_only(self):
        """TP-DEP-02: vision wheel is headless; GUI opencv-python is absent."""
        names = []
        for spec in self._deps():
            name = spec.split(">=")[0].split("==")[0].split("~=")[0].strip()
            names.append(name)
        self.assertIn("opencv-python-headless", names)
        self.assertNotIn("opencv-python", names)
        self.assertNotIn("py-tui", names)

    def test_tp_dep_03_requirement_matches_manifest(self):
        """TP-DEP-03: dependency law states the same specs as pyproject.toml."""
        text = LAW.read_text(encoding="utf-8")
        self.assertIn("`{}`".format(CV_SPEC), text)
        self.assertIn("`{}`".format(LOG_SPEC), text)
        self.assertNotIn("py-tui", text)
        self.assertNotIn("py_tui", text)

    def test_tp_dep_04_installed_wheels_meet_floors(self):
        """TP-DEP-04: installed wheels, when present, meet the floors."""
        self._assert_floor("opencv-python-headless", (5, 0, 0, 93))
        self._assert_floor("ChronicleLogger", (1, 3, 1))

    def _assert_floor(self, dist_name, floor):
        try:
            version = metadata.version(dist_name)
        except metadata.PackageNotFoundError:
            return
        self.assertTrue(
            _at_least(version, floor),
            "{} {} is below {}".format(dist_name, version, floor),
        )


if __name__ == "__main__":
    unittest.main()
