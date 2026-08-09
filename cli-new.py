#!/usr/bin/env python
"""
Thin launcher for the specialized package CLI.
Bootstrap archive: src/VideoSpeed/cli.bootstrap-old.py
Ship unit / SSOT: src/VideoSpeed/cli.py
"""
from __future__ import print_function, unicode_literals

import sys
from pathlib import Path

# Prefer installed package; fall back to src/ layout for checkout runs
_ROOT = Path(__file__).resolve().parent
_SRC = _ROOT / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from VideoSpeed.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main() or 0)
