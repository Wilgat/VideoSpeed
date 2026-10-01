# TP-JSON — one JSON object on stdout (requirement-python-json-output)
from __future__ import print_function, unicode_literals

import io
import json
import os
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
ENV = os.environ.copy()
env_pp = ENV.get("PYTHONPATH", "")
ENV["PYTHONPATH"] = str(SRC) + ((":" + env_pp) if env_pp else "")


def _run(args):
    return subprocess.run(
        [sys.executable, "-m", "VideoSpeed"] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.DEVNULL,
        env=ENV,
        cwd=str(ROOT),
        check=False,
    )


def _assert_one_object(testcase, raw):
    testcase.assertTrue(raw.endswith("\n"), raw)
    doc = json.loads(raw)
    again = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    testcase.assertEqual(raw, again)
    testcase.assertEqual(
        list(doc.keys()),
        ["ok", "mode", "app", "version", "error", "next", "jobs"],
    )
    return doc


class TestJson(unittest.TestCase):
    def test_tp_json_01_modifier_alone_is_one_object(self):
        """TP-JSON-01: --json --percent does not open a menu; stdout is one object."""
        proc = _run(["--json", "--percent", "80"])
        raw = proc.stdout.decode("utf-8")
        doc = _assert_one_object(self, raw)
        self.assertEqual(proc.returncode, 1, proc.stderr.decode("utf-8", "replace"))
        self.assertFalse(doc["ok"])
        self.assertEqual(doc["mode"], "noninteractive")
        self.assertEqual(doc["jobs"], [])
        self.assertIn("--file", doc["error"])
        self.assertIn("--start", doc["next"])
        self.assertNotIn("Folder (Enter", raw)
        self.assertNotIn("Cutting", raw)

    def test_tp_json_02_incomplete_job_is_one_object(self):
        """TP-JSON-02: --json --file without a full job is one object and does not encode."""
        proc = _run(["--json", "--file", "clip.mp4"])
        raw = proc.stdout.decode("utf-8")
        doc = _assert_one_object(self, raw)
        self.assertEqual(proc.returncode, 1)
        self.assertFalse(doc["ok"])
        self.assertEqual(doc["mode"], "noninteractive")
        self.assertIn("--start", doc["error"])
        self.assertIn("--end", doc["error"])
        self.assertNotIn("Cutting", raw)

    def test_tp_json_03_no_terminal_is_one_object(self):
        """TP-JSON-03: --json with no terminal exits 1 as one object and does not wait."""
        proc = _run(["--json"])
        raw = proc.stdout.decode("utf-8")
        doc = _assert_one_object(self, raw)
        self.assertEqual(proc.returncode, 1)
        self.assertFalse(doc["ok"])
        self.assertEqual(doc["mode"], "noninteractive")
        self.assertIn("terminal", doc["error"].lower())
        self.assertNotIn("Folder (Enter", raw)

    def test_tp_json_04_tty_walk_skips_the_menu(self):
        """TP-JSON-04: a terminal plus --json asks on stderr and does not open the menu."""
        from VideoSpeed import cli

        opened = []
        saved_open = cli.open_text_menu
        saved_in = cli.stdin_is_tty
        saved_ff = cli.ensure_ffmpeg
        saved_stdin = sys.stdin
        cli.open_text_menu = lambda: opened.append("open") or None
        cli.stdin_is_tty = lambda: True
        cli.ensure_ffmpeg = lambda: True
        sys.stdin = io.StringIO("")
        out = io.StringIO()
        err = io.StringIO()
        try:
            with redirect_stdout(out), redirect_stderr(err):
                code = cli.main(["--json"])
        finally:
            cli.open_text_menu = saved_open
            cli.stdin_is_tty = saved_in
            cli.ensure_ffmpeg = saved_ff
            sys.stdin = saved_stdin
        raw = out.getvalue()
        doc = _assert_one_object(self, raw)
        self.assertEqual(code, 0, err.getvalue())
        self.assertTrue(doc["ok"])
        self.assertEqual(doc["mode"], "interactive")
        self.assertEqual(doc["jobs"], [])
        self.assertIsNone(doc["error"])
        self.assertEqual(opened, [])
        self.assertIn("Folder (Enter = current):", err.getvalue())
        self.assertNotIn("Folder (Enter", raw)

    def test_tp_json_05_version_stays_human(self):
        """TP-JSON-05: --version still prints human text and exits 0."""
        import VideoSpeed

        proc = _run(["--json", "--version"])
        text = (proc.stdout + proc.stderr).decode("utf-8", "replace")
        self.assertEqual(proc.returncode, 0, text)
        self.assertIn(VideoSpeed.__version__, text)
        self.assertNotIn('"ok"', proc.stdout.decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
