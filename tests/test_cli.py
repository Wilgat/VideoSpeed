# TP-CLI — CLI surface (requirement-python-cli-interface)
# TP-MODE — menu walk vs one job (requirement-python-interactive-vs-noninteractive)
from __future__ import print_function, unicode_literals

import io
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
ENV = os.environ.copy()
env_pp = ENV.get("PYTHONPATH", "")
ENV["PYTHONPATH"] = str(ROOT / "src") + ((":" + env_pp) if env_pp else "")


def _run(args, stdin_devnull=True):
    kw = dict(
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=ENV,
        cwd=str(ROOT),
    )
    if stdin_devnull:
        kw["stdin"] = subprocess.DEVNULL
    return subprocess.run(
        [sys.executable, "-m", "VideoSpeed"] + args,
        **kw
    )


class TestCli(unittest.TestCase):
    def test_tp_cli_01_version_exit_0(self):
        """TP-CLI-01: python -m VideoSpeed --version exits 0, prints version."""
        import VideoSpeed

        proc = _run(["--version"])
        self.assertEqual(proc.returncode, 0, proc.stderr.decode("utf-8", "replace"))
        out = (proc.stdout + proc.stderr).decode("utf-8", "replace")
        self.assertIn(VideoSpeed.__version__, out)
        self.assertIn("VideoSpeed", out)

    def test_tp_cli_02_help_lists_usage(self):
        """TP-CLI-02: --help lists usage and batch flags."""
        proc = _run(["--help"])
        self.assertEqual(proc.returncode, 0, proc.stderr.decode("utf-8", "replace"))
        out = proc.stdout.decode("utf-8", "replace")
        self.assertIn("--file", out)
        self.assertIn("--start", out)
        self.assertIn("--end", out)
        self.assertIn("--percent", out)
        self.assertIn("--boomerang", out)
        self.assertIn("--json", out)

    def test_tp_cli_04_empty_folder_no_mp4(self):
        """TP-CLI-04: No MP4 in folder → clear message, non-success."""
        tmp = tempfile.mkdtemp(prefix="videospeed_empty_")
        try:
            proc = _run(["--folder", tmp])
            self.assertNotEqual(proc.returncode, 0)
            err = proc.stderr.decode("utf-8", "replace")
            self.assertIn("No MP4 files found", err)
        finally:
            os.rmdir(tmp)

    def test_tp_cli_06_batch_requires_file_start_end(self):
        """TP-CLI-06: --file without start/end fails closed (no hang)."""
        proc = _run(["--file", "/tmp/does-not-exist-videospeed.mp4"])
        self.assertNotEqual(proc.returncode, 0)
        err = proc.stderr.decode("utf-8", "replace")
        self.assertIn("--file", err)
        self.assertIn("--start", err)

    def test_tp_cli_06_missing_file(self):
        """TP-CLI-06: --file missing path fails closed with next-step text."""
        proc = _run([
            "--file", str(ROOT / "no-such-clip.mp4"),
            "--start", "0",
            "--end", "1",
        ])
        self.assertNotEqual(proc.returncode, 0)
        err = proc.stderr.decode("utf-8", "replace")
        self.assertIn("File not found", err)
        self.assertIn("Next:", err)

    def test_tp_mode_03_no_tty_empty_argv_fail_closed(self):
        """TP-MODE-03: empty argv with no terminal exits 1 and names a next step."""
        proc = _run([])
        self.assertEqual(proc.returncode, 1)
        err = proc.stderr.decode("utf-8", "replace")
        self.assertIn("No terminal for prompts", err)
        self.assertIn("--file", err)
        self.assertIn("--start", err)
        self.assertIn("--end", err)
        self.assertIn("Next:", err)

    def test_tp_mode_01_selector_does_not_open_menu(self):
        """TP-MODE-01: any selector stays off the menu, even when stdin is a terminal."""
        from VideoSpeed import cli

        self.assertTrue(Path(cli.__file__).resolve().is_relative_to(ROOT))
        opened = []
        saved_open = cli.open_text_menu
        saved_in = cli.stdin_is_tty
        cli.open_text_menu = lambda: opened.append("open") or None
        cli.stdin_is_tty = lambda: True
        try:
            cases = (
                ["--file", "clip.mp4"],
                ["--start", "0"],
                ["--end", "1"],
                ["--folder", "/tmp/does-not-exist-videospeed-mode"],
            )
            for argv in cases:
                err = io.StringIO()
                with redirect_stderr(err):
                    code = cli.main(argv)
                self.assertNotEqual(code, 0, argv)
                self.assertEqual(opened, [], argv)
                self.assertIn("ERROR:", err.getvalue(), argv)
        finally:
            cli.open_text_menu = saved_open
            cli.stdin_is_tty = saved_in

    def test_tp_mode_02_modifier_alone_fail_closed(self):
        """TP-MODE-02: lone --percent or --boomerang exits 1 and does not open the menu."""
        from VideoSpeed import cli

        opened = []
        saved_open = cli.open_text_menu
        saved_in = cli.stdin_is_tty
        cli.open_text_menu = lambda: opened.append("open") or None
        cli.stdin_is_tty = lambda: True
        try:
            for argv in (["--percent", "80"], ["--boomerang"]):
                err = io.StringIO()
                with redirect_stderr(err):
                    code = cli.main(argv)
                text = err.getvalue()
                self.assertEqual(code, 1, argv)
                self.assertEqual(opened, [], argv)
                self.assertIn("--file", text, argv)
                self.assertIn("--start", text, argv)
                self.assertIn("--end", text, argv)
                self.assertIn("Next:", text, argv)
        finally:
            cli.open_text_menu = saved_open
            cli.stdin_is_tty = saved_in


if __name__ == "__main__":
    unittest.main()
