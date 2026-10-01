# TP-FS — filesystem / USB / promote (requirement-python-coding-style, L-XDEV-01)
from __future__ import print_function, unicode_literals

import inspect
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from VideoSpeed import cli  # noqa: E402


class TestFs(unittest.TestCase):
    def test_tp_fs_01_promote_uses_shutil_move(self):
        """TP-FS-01: promote_file uses shutil.move (source + two-dir behavior)."""
        src = inspect.getsource(cli.promote_file)
        self.assertIn("shutil.move", src)
        self.assertIn("shutil.move(str(src), str(dest))", src)

        a = Path(tempfile.mkdtemp(prefix="vs_a_"))
        b = Path(tempfile.mkdtemp(prefix="vs_b_"))
        try:
            src_file = a / "src.bin"
            dest_file = b / "dest.bin"
            src_file.write_bytes(b"videospeed-promote")
            cli.promote_file(src_file, dest_file)
            self.assertTrue(dest_file.is_file())
            self.assertEqual(dest_file.read_bytes(), b"videospeed-promote")
            self.assertFalse(src_file.exists())
        finally:
            for d in (a, b):
                for p in d.iterdir():
                    p.unlink()
                d.rmdir()

    def test_tp_fs_02_staging_dir_writable_parent(self):
        """TP-FS-02: staging_dir_for(dest) returns dest parent when writable."""
        parent = Path(tempfile.mkdtemp(prefix="vs_stage_"))
        try:
            dest = parent / "out.mp4"
            staged = cli.staging_dir_for(dest)
            self.assertEqual(Path(staged).resolve(), parent.resolve())
        finally:
            parent.rmdir()

    def test_tp_fs_04_promote_leaves_no_src_copy(self):
        """TP-FS-04: after promote, intermediate source is gone."""
        parent = Path(tempfile.mkdtemp(prefix="vs_p4_"))
        try:
            src = parent / "tmp.mp4"
            dest = parent / "final.mp4"
            src.write_bytes(b"x")
            cli.promote_file(src, dest)
            self.assertTrue(dest.is_file())
            self.assertFalse(src.exists())
        finally:
            for p in parent.iterdir():
                p.unlink()
            parent.rmdir()


if __name__ == "__main__":
    unittest.main()
