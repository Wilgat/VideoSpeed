# TP-ERR — error handling (requirement-python-error-handling, L-RANGE-01)
from __future__ import print_function, unicode_literals

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from VideoSpeed import cli  # noqa: E402


class TestErrors(unittest.TestCase):
    def test_tp_err_01_invalid_cut_range(self):
        """TP-ERR-01: invalid cut range is rejected without encode."""
        self.assertFalse(cli.valid_cut_range(5, 1, 10))
        self.assertFalse(cli.valid_cut_range(-1, 2, 10))
        self.assertFalse(cli.valid_cut_range(0, 11, 10))
        self.assertFalse(cli.valid_cut_range(0, 0, 10))
        self.assertTrue(cli.valid_cut_range(0, 5, 10))
        self.assertTrue(cli.valid_cut_range(1.0, 9.9, 10.0))

    def test_tp_err_02_percent_outside_bounds(self):
        """TP-ERR-02: length % outside 20–200 rejected."""
        self.assertFalse(cli.valid_percent(19.9))
        self.assertFalse(cli.valid_percent(200.1))
        self.assertFalse(cli.valid_percent("nope"))
        self.assertTrue(cli.valid_percent(20))
        self.assertTrue(cli.valid_percent(100))
        self.assertTrue(cli.valid_percent(200))


if __name__ == "__main__":
    unittest.main()
