# TP-TIME — foreground FFmpeg wait (requirement-python-time-consuming-process)
from __future__ import print_function, unicode_literals

import io
import subprocess
import sys
import tempfile
import unicodedata
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from VideoSpeed import cli  # noqa: E402
from VideoSpeed.edit_walk import EditWalk  # noqa: E402
from VideoSpeed.encoder import Encoder  # noqa: E402
from VideoSpeed.file_stage import FileStage  # noqa: E402
from VideoSpeed.media_info import MediaInfo  # noqa: E402
from VideoSpeed.run_output import RunOutput  # noqa: E402


class _Child:
    """Stand-in for Popen. Stalls, then exits. Does not start a real process."""

    def __init__(self, stalls=0, code=0, err=b"", interrupt=False):
        self.stalls = stalls
        self.code = code
        self.err = err
        self.interrupt = interrupt
        self.timeouts = []
        self.returncode = None
        self.killed = False
        self.waited = False

    def communicate(self, timeout=None):
        self.timeouts.append(timeout)
        if self.interrupt and len(self.timeouts) == 1:
            raise KeyboardInterrupt()
        if len(self.timeouts) <= self.stalls:
            raise subprocess.TimeoutExpired(["ffmpeg"], timeout)
        self.returncode = self.code
        return b"", self.err

    def poll(self):
        return self.returncode

    def kill(self):
        self.killed = True
        self.returncode = -9

    def wait(self, timeout=None):
        self.waited = True
        return self.returncode


class _Phrase:
    WAIT_PHRASE = Encoder.WAIT_PHRASE


class TestTime(unittest.TestCase):
    def _encoder(self):
        output = RunOutput(cli.Cli.APP_NAME, cli.Cli._PKG_VERSION)
        encoder = Encoder(
            output, None, FileStage(), cli.Cli.RATIO_MIN, cli.Cli.RATIO_MAX
        )
        return output, encoder

    def _run(self, encoder, child, cmd=None):
        seen = {}

        def fake_popen(argv, **kwargs):
            seen["argv"] = argv
            seen["kwargs"] = kwargs
            return child

        def refuse_run(*_args, **_kwargs):
            raise AssertionError("subprocess.run")

        with patch("subprocess.Popen", fake_popen), patch("subprocess.run", refuse_run):
            encoder.run_ffmpeg(cmd or ["ffmpeg", "-nostdin", "clip.mp4"])
        return seen

    def test_tp_time_01_screen_flashes_one_line(self):
        """TP-TIME-01: the text screen replaces one wait line. The flash does not kill."""
        output, encoder = self._encoder()
        lines = []

        def sink(msg, _is_err):
            lines.append(msg)

        output.message_sink = sink
        child = _Child(stalls=2)
        seen = self._run(encoder, child)
        on = encoder._wait_line(Encoder.WAIT_MARK_ON)
        off = encoder._wait_line(Encoder.WAIT_MARK_OFF)
        self.assertEqual(lines, [on, off, on])
        self.assertEqual(child.timeouts, [Encoder.FLASH_SECONDS] * 3)
        self.assertEqual(Encoder.FLASH_SECONDS, 0.5)
        self.assertFalse(child.killed)
        self.assertIs(seen["kwargs"]["stdin"], subprocess.DEVNULL)
        self.assertIs(seen["kwargs"]["stdout"], subprocess.PIPE)
        self.assertIs(seen["kwargs"]["stderr"], subprocess.PIPE)
        self.assertNotIn("timeout", seen["kwargs"])
        self.assertNotIn(" ".join(seen["argv"]), "\n".join(lines))
        self.assertEqual(unicodedata.east_asian_width(Encoder.WAIT_MARK_ON), "A")
        self.assertEqual(unicodedata.east_asian_width(Encoder.WAIT_MARK_OFF), "A")
        source = (SRC / "VideoSpeed" / "encoder.py").read_text(encoding="utf-8")
        self.assertNotIn("threading", source)
        self.assertNotIn("Thread(", source)

        walk = EditWalk(output, _Phrase(), None, cli.Cli.RATIO_MIN, cli.Cli.RATIO_MAX)
        body = ["Working…", "1. Cutting segment..."]
        walk.place_job_line(body, on)
        walk.place_job_line(body, off)
        self.assertEqual(body[-1], off)
        self.assertEqual(
            sum(1 for line in body if Encoder.WAIT_PHRASE in line),
            1,
        )
        walk.place_job_line(body, "2. Length stays 100%...")
        self.assertEqual(body[-1], "2. Length stays 100%...")
        self.assertFalse(any(Encoder.WAIT_PHRASE in line for line in body))

    def test_tp_time_02_plain_line_and_json_silence(self):
        """TP-TIME-02: a plain terminal rewrites one line. --json writes no progress."""
        output, encoder = self._encoder()
        child = _Child(stalls=1)
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            self._run(encoder, child)
        text = buf.getvalue()
        self.assertIn("\r" + encoder._wait_line(Encoder.WAIT_MARK_ON), text)
        self.assertIn("\r" + encoder._wait_line(Encoder.WAIT_MARK_OFF), text)
        self.assertTrue(text.endswith("\n"))
        self.assertNotIn("ffmpeg -nostdin", text)
        self.assertFalse(child.killed)

        output.json_mode = True
        quiet = _Child(stalls=1)
        out_buf = io.StringIO()
        err_buf = io.StringIO()
        with patch("sys.stdout", out_buf), patch("sys.stderr", err_buf):
            self._run(encoder, quiet)
        self.assertNotIn(Encoder.WAIT_PHRASE, out_buf.getvalue())
        self.assertNotIn(Encoder.WAIT_PHRASE, err_buf.getvalue())
        self.assertEqual(quiet.timeouts, [Encoder.FLASH_SECONDS, Encoder.FLASH_SECONDS])
        self.assertFalse(quiet.killed)

    def _job(self, percent, boomerang):
        folder = Path(tempfile.mkdtemp(prefix="vs_time_"))
        source = folder / "clip.mp4"
        source.write_bytes(b"source-bytes")
        calls = []

        def fake_run(cmd):
            calls.append(list(cmd))
            Path(cmd[-1]).write_bytes("pass-{}".format(len(calls)).encode("ascii"))

        output = RunOutput(cli.Cli.APP_NAME, cli.Cli._PKG_VERSION)
        encoder = Encoder(
            output,
            MediaInfo(output),
            FileStage(),
            cli.Cli.RATIO_MIN,
            cli.Cli.RATIO_MAX,
        )
        try:
            with patch.object(encoder, "run_ffmpeg", side_effect=fake_run):
                with redirect_stdout(io.StringIO()):
                    result = encoder.process_job(source, 0.0, 1.0, percent, boomerang)
        except Exception:
            for path in folder.iterdir():
                path.unlink()
            folder.rmdir()
            raise
        return folder, calls, result

    def _cleanup(self, folder):
        for path in list(folder.iterdir()):
            path.unlink()
        folder.rmdir()

    def test_tp_time_03_percent_100_skips_speed(self):
        """TP-TIME-03: 100% and boomerang off does not start the medium child."""
        folder, calls, result = self._job(100.0, False)
        try:
            self.assertIsNotNone(result)
            self.assertEqual(len(calls), 1)
            joined = " ".join(str(part) for part in calls[0])
            self.assertNotIn("atempo", joined)
            self.assertNotIn("medium", joined)
            self.assertIn("-nostdin", calls[0])
        finally:
            self._cleanup(folder)

    def test_tp_time_04_other_percent_waits_on_speed(self):
        """TP-TIME-04: a length other than 100% runs medium after the cut, then publishes."""
        folder, calls, result = self._job(50.0, False)
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

    def test_tp_time_05_interrupt_stops_the_child(self):
        """TP-TIME-05: KeyboardInterrupt stops the child and propagates. No Exit?."""
        output, encoder = self._encoder()
        lines = []
        output.message_sink = lambda msg, _is_err: lines.append(msg)
        child = _Child(interrupt=True)
        with self.assertRaises(KeyboardInterrupt):
            self._run(encoder, child)
        self.assertTrue(child.killed)
        self.assertTrue(child.waited)
        blob = "\n".join(lines)
        self.assertNotIn("Exit?", blob)
        self.assertNotIn("130", blob)
        method = (SRC / "VideoSpeed" / "encoder.py").read_text(encoding="utf-8")
        start = method.index("    def run_ffmpeg")
        end = method.index("    def cut_clip")
        body = method[start:end]
        self.assertNotIn("Exit?", body)
        self.assertNotIn("130", body)


if __name__ == "__main__":
    unittest.main()
