# TP-FS — filesystem / USB / promote (requirement-python-coding-style, L-XDEV-01)
from __future__ import print_function, unicode_literals

import inspect
import io
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

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

    def test_tp_fs_05_ship_modules_do_not_call_os_rename_or_replace(self):
        """TP-FS-05: ship modules move with shutil; no os.rename or os.replace."""
        banned = re.compile(
            r"\b(?:os\.(?:rename|replace)|Path\.(?:rename|replace))\s*\("
        )
        offenders = []
        pkg = SRC / "VideoSpeed"
        for path in sorted(pkg.glob("*.py")):
            if path.name == "cli.bootstrap-old.py":
                continue
            for lineno, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), 1
            ):
                code = line.split("#", 1)[0]
                if banned.search(code):
                    offenders.append("{}:{}".format(path.name, lineno))
        self.assertEqual(offenders, [])

    def _job_with_fake_ffmpeg(self, percent, boomerang):
        """Run process_job. Each FFmpeg call writes its output argument."""
        folder = Path(tempfile.mkdtemp(prefix="vs_job_"))
        source = folder / "clip.mp4"
        source.write_bytes(b"source-bytes")
        calls = []

        def fake_run(cmd):
            calls.append(list(cmd))
            Path(cmd[-1]).write_bytes("pass-{}".format(len(calls)).encode("ascii"))

        try:
            with patch.object(cli, "run_ffmpeg", side_effect=fake_run):
                with redirect_stdout(io.StringIO()):
                    result = cli.process_job(source, 0.0, 1.0, percent, boomerang)
        except Exception:
            for path in folder.iterdir():
                path.unlink()
            folder.rmdir()
            raise
        return folder, source, calls, result

    def _cleanup(self, folder):
        for path in folder.iterdir():
            path.unlink()
        folder.rmdir()

    def test_percent_100_publishes_cut_without_second_encode(self):
        """100% and no boomerang renames the cut. It does not run the speed encode."""
        folder, source, calls, result = self._job_with_fake_ffmpeg(100.0, False)
        try:
            self.assertIsNotNone(result)
            self.assertEqual(result.name, "clip_cut0.0-1.0s_100pct.mp4")
            self.assertEqual(result.read_bytes(), b"pass-1")
            self.assertEqual(source.read_bytes(), b"source-bytes")
            self.assertEqual(len(calls), 1)
            self.assertIn("-nostdin", calls[0])
            joined = " ".join(str(part) for part in calls[0])
            self.assertNotIn("atempo", joined)
            self.assertNotIn("medium", joined)
            self.assertEqual(list(folder.glob("videospeed_*")), [])
        finally:
            self._cleanup(folder)

    def test_percent_50_still_runs_the_speed_encode(self):
        """A length other than 100% still runs cut, then the speed encode, then publish."""
        folder, _source, calls, result = self._job_with_fake_ffmpeg(50.0, False)
        try:
            self.assertIsNotNone(result)
            self.assertEqual(result.name, "clip_cut0.0-1.0s_50pct.mp4")
            self.assertEqual(result.read_bytes(), b"pass-2")
            self.assertEqual(len(calls), 2)
            joined = " ".join(str(part) for part in calls[1])
            self.assertIn("atempo", joined)
            self.assertIn("medium", joined)
            self.assertIn("-nostdin", calls[1])
            self.assertEqual(list(folder.glob("videospeed_*")), [])
        finally:
            self._cleanup(folder)

    def test_percent_100_with_boomerang_skips_speed_encode(self):
        """100% with boomerang still reverses the cut and does not speed-encode."""
        folder, _source, calls, result = self._job_with_fake_ffmpeg(100.0, True)
        try:
            self.assertIsNotNone(result)
            self.assertTrue(result.name.endswith("_BOOMERANG.mp4"))
            self.assertTrue(result.is_file())
            joined = " ".join(" ".join(str(part) for part in cmd) for cmd in calls)
            self.assertNotIn("atempo", joined)
            self.assertNotIn("medium", joined)
            self.assertEqual(list(folder.glob("videospeed_*")), [])
        finally:
            self._cleanup(folder)


if __name__ == "__main__":
    unittest.main()
