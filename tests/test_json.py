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
        from VideoSpeed.tui import Tui
        saved_open = Tui.open_text_menu
        saved_in = staticmethod(cli.Cli.stdin_is_tty)
        from VideoSpeed.encoder import Encoder
        saved_ff = Encoder.ensure_ffmpeg
        saved_stdin = sys.stdin
        Tui.open_text_menu = lambda self: opened.append("open") or None
        cli.Cli.stdin_is_tty = lambda *args: True
        Encoder.ensure_ffmpeg = lambda self: True
        sys.stdin = io.StringIO("")
        out = io.StringIO()
        err = io.StringIO()
        try:
            with redirect_stdout(out), redirect_stderr(err):
                code = cli.main(["--json"])
        finally:
            Tui.open_text_menu = saved_open
            cli.Cli.stdin_is_tty = saved_in
            Encoder.ensure_ffmpeg = saved_ff
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

    def test_tp_json_06_every_verb_is_one_object(self):
        """TP-JSON-06: every product verb with --json writes one object and skips the menu."""
        from VideoSpeed import cli
        from VideoSpeed.encoder import Encoder
        from VideoSpeed.self_management import SelfManage
        from VideoSpeed.tui import Tui

        opened = []
        encoded = []
        calls = []

        def fake_runner(self, argv):
            calls.append(list(argv))
            return 0, "pip-ok", ""

        def fake_batch(self, *args):
            encoded.append(args)
            return 0

        saved_open = Tui.open_text_menu
        saved_direct = Tui._open_direct_screen
        saved_batch = Encoder.batch_session
        saved_runner = SelfManage._subprocess_runner
        Tui.open_text_menu = lambda self: opened.append("open") or None
        Tui._open_direct_screen = lambda self, *args: opened.append("direct") or 0
        Encoder.batch_session = fake_batch
        SelfManage._subprocess_runner = fake_runner
        try:
            help_out = io.StringIO()
            help_err = io.StringIO()
            with redirect_stdout(help_out), redirect_stderr(help_err):
                help_code = cli.main(["help", "--json"])
            help_raw = help_out.getvalue()
            help_doc = _assert_one_object(self, help_raw)
            self.assertEqual(help_code, 0, help_err.getvalue())
            self.assertTrue(help_doc["ok"])
            self.assertEqual(help_doc["mode"], "noninteractive")
            self.assertIn("usage:", help_err.getvalue())
            self.assertNotIn("usage:", help_raw)

            for verb in ("version", "about", "list-mp4"):
                out = io.StringIO()
                err = io.StringIO()
                with redirect_stdout(out), redirect_stderr(err):
                    code = cli.main([verb, "--json"])
                raw = out.getvalue()
                doc = _assert_one_object(self, raw)
                self.assertEqual(list(doc.keys())[0], "ok", verb)
                self.assertTrue(raw.strip().startswith("{"), verb)
                if verb == "list-mp4":
                    self.assertNotIn("1. ", raw)
                else:
                    self.assertEqual(code, 0, err.getvalue())
                    self.assertTrue(doc["ok"], verb)

            edit_out = io.StringIO()
            edit_err = io.StringIO()
            with redirect_stdout(edit_out), redirect_stderr(edit_err):
                edit_code = cli.main(["edit", "--json"])
            edit_doc = _assert_one_object(self, edit_out.getvalue())
            self.assertEqual(edit_code, 1)
            self.assertFalse(edit_doc["ok"])
            self.assertIn("--file", edit_doc["error"])
            self.assertEqual(encoded, [])

            for verb in ("self-install", "version-check", "self-update"):
                before = len(calls)
                out = io.StringIO()
                err = io.StringIO()
                with redirect_stdout(out), redirect_stderr(err):
                    code = cli.main([verb, "--json"])
                doc = _assert_one_object(self, out.getvalue())
                self.assertEqual(code, 0, err.getvalue())
                self.assertTrue(doc["ok"], verb)
                self.assertIn("pip-ok", err.getvalue())
                self.assertNotIn("pip-ok", out.getvalue())
                self.assertEqual(len(calls), before + 1, verb)

            bare_out = io.StringIO()
            before = len(calls)
            with redirect_stdout(bare_out), redirect_stderr(io.StringIO()):
                bare_code = cli.main(["self-uninstall", "--json"])
            bare_doc = _assert_one_object(self, bare_out.getvalue())
            self.assertEqual(bare_code, 1)
            self.assertFalse(bare_doc["ok"])
            self.assertEqual(len(calls), before)

            force_out = io.StringIO()
            force_err = io.StringIO()
            with redirect_stdout(force_out), redirect_stderr(force_err):
                force_code = cli.main(["self-uninstall", "--json", "--force"])
            force_doc = _assert_one_object(self, force_out.getvalue())
            self.assertEqual(force_code, 0, force_err.getvalue())
            self.assertTrue(force_doc["ok"])
            self.assertIn("uninstall", " ".join(calls[-1]))
        finally:
            Tui.open_text_menu = saved_open
            Tui._open_direct_screen = saved_direct
            Encoder.batch_session = saved_batch
            SelfManage._subprocess_runner = saved_runner
        self.assertEqual(opened, [])


if __name__ == "__main__":
    unittest.main()
