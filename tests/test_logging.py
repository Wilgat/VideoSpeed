# TP-LOG-01, TP-LOG-02, TP-LOG-04 — ChronicleLogger in main
# (requirement-python-cli-logging).
from __future__ import print_function, unicode_literals

import builtins
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


class TestLogging(unittest.TestCase):
    def _dirs(self):
        base = tempfile.mkdtemp(prefix="videospeed_log_base_")
        logd = tempfile.mkdtemp(prefix="videospeed_log_dir_")
        self.addCleanup(self._rm, base)
        self.addCleanup(self._rm, logd)
        return base, logd

    @staticmethod
    def _rm(path):
        import shutil

        shutil.rmtree(path, ignore_errors=True)

    def _push_debug(self, value):
        saved = (os.environ.get("DEBUG"), os.environ.get("debug"))

        def restore():
            self._put("DEBUG", saved[0])
            self._put("debug", saved[1])

        self.addCleanup(restore)
        if value is None:
            os.environ.pop("DEBUG", None)
            os.environ.pop("debug", None)
        else:
            os.environ["DEBUG"] = value
            os.environ.pop("debug", None)

    @staticmethod
    def _put(key, value):
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value

    def _log_text(self, logd):
        files = sorted(Path(logd).glob("video-speed-*.log"))
        self.assertTrue(files, "daily log was not created under the temp log dir")
        return "".join(path.read_text(encoding="utf-8", errors="replace") for path in files)

    def test_tp_log_01_readback_under_temp_base(self):
        """TP-LOG-01: one construct reads logName, baseDir, and logDir back."""
        from VideoSpeed import cli

        base, logd = self._dirs()
        self._push_debug(None)
        logger = cli.Cli()._start_logger(["--version"], base, logd)
        self.assertIsNotNone(logger)
        self.assertEqual(logger.logName(), "video-speed")
        self.assertEqual(str(Path(logger.baseDir())), str(Path(base)))
        self.assertEqual(str(Path(logger.logDir())), str(Path(logd)))
        with redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as caught:
                cli.main(["--version"], log_basedir=base, log_logdir=logd)
        self.assertEqual(caught.exception.code, 0)
        self.assertTrue(list(Path(logd).glob("video-speed-*.log")))

    def test_tp_log_01_missing_library_exits_before_parser(self):
        """TP-LOG-01: a missing ChronicleLogger exits 1 with the install line."""
        from VideoSpeed import cli

        real_import = builtins.__import__

        def hidden(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "ChronicleLogger":
                raise ImportError("hidden for test")
            return real_import(name, globals, locals, fromlist, level)

        builtins.__import__ = hidden
        out = io.StringIO()
        err = io.StringIO()
        try:
            with redirect_stdout(out), redirect_stderr(err):
                code = cli.main(["--help"])
        finally:
            builtins.__import__ = real_import
        self.assertEqual(code, 1)
        self.assertIn("ChronicleLogger>=1.3.1", err.getvalue())
        self.assertNotIn("usage:", out.getvalue().lower())

    def test_tp_log_02_debug_identity_is_displayed(self):
        """TP-LOG-02: DEBUG=1 displays the identity; an unset DEBUG does not."""
        from VideoSpeed import cli

        base, logd = self._dirs()
        self._push_debug("1")
        out = io.StringIO()
        with redirect_stdout(out):
            with self.assertRaises(SystemExit) as caught:
                cli.main(["--version"], log_basedir=base, log_logdir=logd)
        self.assertEqual(caught.exception.code, 0)
        text = out.getvalue()
        self.assertIn("video-speed v", text)
        self.assertIn("ChronicleLogger v", text)
        self.assertIn("Base ", text)
        logged = self._log_text(logd)
        self.assertIn("ChronicleLogger v", logged)
        self.assertIn("@main", logged)

        off_base, off_log = self._dirs()
        self._push_debug(None)
        off = io.StringIO()
        with redirect_stdout(off):
            with self.assertRaises(SystemExit):
                cli.main(["--version"], log_basedir=off_base, log_logdir=off_log)
        self.assertNotIn("ChronicleLogger v", off.getvalue())
        self.assertNotIn("ChronicleLogger v", self._log_text(off_log))

    def test_tp_log_02_json_keeps_debug_off_stdout(self):
        """TP-LOG-02: --json still stores the debug lines, and stdout stays one object."""
        from VideoSpeed import cli

        base, logd = self._dirs()
        self._push_debug("show")
        saved_tty = cli.Cli.stdin_is_tty
        cli.Cli.stdin_is_tty = lambda self: False
        out = io.StringIO()
        err = io.StringIO()
        try:
            with redirect_stdout(out), redirect_stderr(err):
                code = cli.main(
                    ["--json"], log_basedir=base, log_logdir=logd
                )
        finally:
            cli.Cli.stdin_is_tty = saved_tty
        raw = out.getvalue()
        self.assertNotIn("ChronicleLogger", raw)
        self.assertTrue(raw.strip().startswith("{"), raw)
        self.assertIn("ChronicleLogger v", self._log_text(logd))
        self.assertEqual(code, 1)

    def test_tp_log_04_menu_quiets_before_open(self):
        """TP-LOG-04: the text-menu path calls quiet(True) before the frame."""
        from VideoSpeed import cli
        from VideoSpeed.tui import Tui

        base, logd = self._dirs()
        self._push_debug(None)
        seen = {}
        saved_open = Tui.open_text_menu
        saved_tty = cli.Cli.stdin_is_tty
        saved_start = cli.Cli._start_logger

        def wrapped(self, argv, log_basedir="", log_logdir=""):
            logger = saved_start(self, argv, log_basedir, log_logdir)
            seen["logger"] = logger
            return logger

        def menu(self):
            seen["quiet"] = seen["logger"].quiet()
            return None

        cli.Cli._start_logger = wrapped
        Tui.open_text_menu = menu
        cli.Cli.stdin_is_tty = lambda self: True
        try:
            code = cli.main([], log_basedir=base, log_logdir=logd)
        finally:
            cli.Cli._start_logger = saved_start
            Tui.open_text_menu = saved_open
            cli.Cli.stdin_is_tty = saved_tty
        self.assertEqual(code, 0)
        self.assertIs(seen.get("quiet"), True)
