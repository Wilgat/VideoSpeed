# TP-LOG-01, TP-LOG-02, TP-LOG-04, TP-LOG-05, TP-LOG-08 — ChronicleLogger in main
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

    def _spy_logger(self):
        import ChronicleLogger as chronicle_pkg

        seen = {}
        real = chronicle_pkg.ChronicleLogger

        def factory(*args, **kwargs):
            seen["kwargs"] = dict(kwargs)
            obj = real(*args, **kwargs)
            seen["logger"] = obj
            return obj

        factory.class_version = real.class_version
        chronicle_pkg.ChronicleLogger = factory
        self.addCleanup(setattr, chronicle_pkg, "ChronicleLogger", real)
        return seen

    def _log_text(self, logd):
        files = sorted(Path(logd).glob("video-speed-*.log"))
        self.assertTrue(files, "daily log was not created under the temp log dir")
        return "".join(path.read_text(encoding="utf-8", errors="replace") for path in files)

    def test_tp_log_01_readback_under_temp_base(self):
        """TP-LOG-01: one construct reads logName, baseDir, and logDir back."""
        from VideoSpeed import cli

        base, logd = self._dirs()
        self._push_debug(None)
        seen = self._spy_logger()
        with redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as caught:
                cli.main(["--version"], log_basedir=base, log_logdir=logd)
        logger = seen["logger"]
        self.assertIsNotNone(logger)
        self.assertEqual(logger.logName(), "video-speed")
        self.assertEqual(str(Path(logger.baseDir())), str(Path(base)))
        self.assertEqual(str(Path(logger.logDir())), str(Path(logd)))
        self.assertTrue(seen["kwargs"].get("is_quiet"))
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
        """TP-LOG-02: DEBUG=1 writes the file. The terminal shows it only with --verbose."""
        from VideoSpeed import cli

        base, logd = self._dirs()
        self._push_debug("1")
        out = io.StringIO()
        with redirect_stdout(out):
            with self.assertRaises(SystemExit) as caught:
                cli.main(["--version"], log_basedir=base, log_logdir=logd)
        self.assertEqual(caught.exception.code, 0)
        text = out.getvalue()
        self.assertNotIn("video-speed v", text)
        self.assertNotIn("ChronicleLogger v", text)
        self.assertNotIn("debug mode", text)
        logged = self._log_text(logd)
        self.assertIn("ChronicleLogger v", logged)
        self.assertIn("debug mode", logged)
        self.assertIn("@main", logged)

        shown_base, shown_log = self._dirs()
        shown = io.StringIO()
        with redirect_stdout(shown):
            with self.assertRaises(SystemExit) as shown_caught:
                cli.main(
                    ["--verbose", "--version"],
                    log_basedir=shown_base,
                    log_logdir=shown_log,
                )
        self.assertEqual(shown_caught.exception.code, 0)
        shown_text = shown.getvalue()
        self.assertIn("video-speed v", shown_text)
        self.assertIn("ChronicleLogger v", shown_text)
        self.assertIn("Base ", shown_text)
        self.assertIn("debug mode", shown_text)
        shown_logged = self._log_text(shown_log)
        self.assertIn("debug mode", shown_logged)

        off_base, off_log = self._dirs()
        self._push_debug(None)
        off = io.StringIO()
        with redirect_stdout(off):
            with self.assertRaises(SystemExit):
                cli.main(
                    ["--verbose", "--version"],
                    log_basedir=off_base,
                    log_logdir=off_log,
                )
        self.assertNotIn("ChronicleLogger v", off.getvalue())
        self.assertNotIn("debug mode", off.getvalue())
        self.assertNotIn("ChronicleLogger v", self._log_text(off_log))
        self.assertNotIn("debug mode", self._log_text(off_log))

    def test_tp_log_02_json_keeps_debug_off_stdout(self):
        """TP-LOG-02: --json still stores the debug lines, and stdout stays one object."""
        from VideoSpeed import cli

        base, logd = self._dirs()
        self._push_debug("show")
        saved_tty = staticmethod(cli.Cli.stdin_is_tty)
        cli.Cli.stdin_is_tty = lambda *args: False
        out = io.StringIO()
        err = io.StringIO()
        try:
            with redirect_stdout(out), redirect_stderr(err):
                code = cli.main(
                    ["--json", "--verbose"], log_basedir=base, log_logdir=logd
                )
        finally:
            cli.Cli.stdin_is_tty = saved_tty
        raw = out.getvalue()
        self.assertNotIn("ChronicleLogger", raw)
        self.assertNotIn("debug mode", raw)
        self.assertTrue(raw.strip().startswith("{"), raw)
        logged = self._log_text(logd)
        self.assertIn("ChronicleLogger v", logged)
        self.assertIn("debug mode", logged)
        self.assertEqual(code, 1)

    def test_tp_log_04_menu_quiets_before_open(self):
        """TP-LOG-04: the text-menu path calls quiet(True) before the frame."""
        from VideoSpeed import cli
        from VideoSpeed.tui import Tui

        base, logd = self._dirs()
        self._push_debug(None)
        seen = self._spy_logger()
        saved_open = Tui.open_text_menu
        saved_tty = staticmethod(cli.Cli.stdin_is_tty)

        def menu(self):
            seen["quiet"] = seen["logger"].quiet()
            return None

        Tui.open_text_menu = menu
        cli.Cli.stdin_is_tty = lambda *args: True
        try:
            code = cli.main([], log_basedir=base, log_logdir=logd)
        finally:
            Tui.open_text_menu = saved_open
            cli.Cli.stdin_is_tty = saved_tty
        self.assertEqual(code, 0)
        self.assertIs(seen.get("quiet"), True)

    def test_tp_log_02_text_screen_keeps_debug_off_stdout(self):
        """TP-LOG-02: the text screen quiets the mirror. The file still says debug mode."""
        from VideoSpeed import cli
        from VideoSpeed.tui import Tui

        base, logd = self._dirs()
        self._push_debug("1")
        saved_open = Tui.open_text_menu
        saved_in = staticmethod(cli.Cli.stdin_is_tty)
        saved_out = staticmethod(cli.Cli.stdout_is_tty)
        Tui.open_text_menu = lambda self: None
        cli.Cli.stdin_is_tty = lambda *args: True
        cli.Cli.stdout_is_tty = lambda *args: True
        out = io.StringIO()
        try:
            with redirect_stdout(out):
                code = cli.main(
                    ["--verbose"], log_basedir=base, log_logdir=logd
                )
        finally:
            Tui.open_text_menu = saved_open
            cli.Cli.stdin_is_tty = saved_in
            cli.Cli.stdout_is_tty = saved_out
        self.assertEqual(code, 0)
        self.assertNotIn("debug mode", out.getvalue())
        self.assertIn("debug mode", self._log_text(logd))

    def test_tp_log_05_each_object_logs_instantiated(self):
        """TP-LOG-05: every constructed class stores the one logger and logs instantiated."""
        from VideoSpeed import cli
        from VideoSpeed.menu_model import MenuModel
        from VideoSpeed.menu_session import MenuScreenError, MenuSession

        base, logd = self._dirs()
        self._push_debug(None)
        out = io.StringIO()
        with redirect_stdout(out):
            with self.assertRaises(SystemExit) as caught:
                cli.main(["--version"], log_basedir=base, log_logdir=logd)
        self.assertEqual(caught.exception.code, 0)
        text = out.getvalue()
        logged = self._log_text(logd)
        for name in (
            "Cli",
            "RunOutput",
            "FileStage",
            "MediaInfo",
            "Encoder",
            "CheckSystem",
            "AboutPage",
            "EditWalk",
            "Tui",
            "MenuPainter",
            "SelfManage",
            "SystemLog",
            "LanguageMenu",
        ):
            line = "@{0} :] instantiated".format(name)
            self.assertIn(line, logged, name)
            self.assertNotIn(line, text, name)
        self.assertNotIn("debug mode", text)
        self.assertNotIn("debug mode", logged)

        verb_base, verb_log = self._dirs()
        verb_out = io.StringIO()
        with redirect_stdout(verb_out):
            with self.assertRaises(SystemExit) as verb_caught:
                cli.main(
                    ["--verbose", "--version"],
                    log_basedir=verb_base,
                    log_logdir=verb_log,
                )
        self.assertEqual(verb_caught.exception.code, 0)
        verb_text = verb_out.getvalue()
        for name in ("Cli", "Encoder", "Tui", "LanguageMenu"):
            self.assertIn("@{0} :] instantiated".format(name), verb_text)

        from ChronicleLogger import ChronicleLogger

        logger = ChronicleLogger(
            logname="VideoSpeed",
            basedir=base,
            logdir=logd,
            is_quiet=False,
        )
        app = cli.Cli(logger)
        self.assertIs(app.encoder.logger, logger)
        self.assertIs(app.tui.painter.logger, logger)
        self.assertIs(app.about.check.logger, logger)
        self.assertIs(app.edit.logger, logger)
        self.assertIs(app.media.logger, logger)
        self.assertIs(app.output.logger, logger)
        self.assertIs(app.stage.logger, logger)
        self.assertIs(app.self_manage.logger, logger)
        self.assertIs(app.tui.system_log.logger, logger)
        self.assertIs(app.tui.language.logger, logger)
        session = MenuSession(
            "VideoSpeed",
            "0",
            on_version=lambda: "0",
            on_about=lambda: "about",
            logger=logger,
        )
        self.assertIs(session.model.logger, logger)
        self.assertIs(session.model.painter.logger, logger)
        self.assertIs(MenuModel(logger=logger).logger, logger)
        self.assertIs(MenuScreenError("too small", logger=logger).logger, logger)
        logged = self._log_text(logd)
        for name in ("MenuSession", "MenuModel", "MenuScreenError"):
            self.assertIn("@{0} :] instantiated".format(name), logged)

        json_base, json_log = self._dirs()
        json_out = io.StringIO()
        with redirect_stdout(json_out):
            with self.assertRaises(SystemExit) as json_caught:
                cli.main(
                    ["--json", "--version"],
                    log_basedir=json_base,
                    log_logdir=json_log,
                )
        self.assertEqual(json_caught.exception.code, 0)
        self.assertNotIn("instantiated", json_out.getvalue())
        self.assertIn("@Cli :] instantiated", self._log_text(json_log))

    def _fresh_log(self):
        parent = tempfile.mkdtemp(prefix="videospeed_log_parent_")
        self.addCleanup(self._rm, parent)
        logd = os.path.join(parent, "fresh")
        self.assertFalse(os.path.isdir(logd))
        return parent, logd

    def test_tp_log_08_about_json_is_quiet_on_construct(self):
        """TP-LOG-08: about --json passes is_quiet before the log folder is created."""
        import json

        from VideoSpeed import cli

        base, logd = self._fresh_log()
        self._push_debug("1")
        seen = self._spy_logger()
        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(
                ["about", "--json"], log_basedir=base, log_logdir=logd
            )
        self.assertEqual(code, 0)
        self.assertIs(seen["kwargs"].get("is_quiet"), True)
        raw = out.getvalue()
        page = err.getvalue()
        self.assertNotIn("Created directory:", raw)
        self.assertNotIn("Created directory:", page)
        self.assertNotIn("debug mode", raw)
        self.assertNotIn("debug mode", page)
        self.assertNotIn("] pid:", raw)
        self.assertNotIn("] pid:", page)
        self.assertNotIn("[CHECK SYSTEM]:", raw)
        self.assertIn("[CHECK SYSTEM]:", page)
        obj = json.loads(raw)
        self.assertTrue(obj["ok"])
        self.assertEqual(obj["jobs"], [])
        logged = self._log_text(logd)
        self.assertIn("debug mode", logged)
        self.assertIn("@Cli :] instantiated", logged)

        ver_base, ver_log = self._fresh_log()
        seen.clear()
        ver_out = io.StringIO()
        with redirect_stdout(ver_out):
            with self.assertRaises(SystemExit) as caught:
                cli.main(["--version"], log_basedir=ver_base, log_logdir=ver_log)
        self.assertEqual(caught.exception.code, 0)
        self.assertTrue(seen["kwargs"].get("is_quiet"))
        self.assertNotIn("Created directory:", ver_out.getvalue())
        self.assertNotIn("debug mode", ver_out.getvalue())
        self.assertIn("debug mode", self._log_text(ver_log))

        loud_base, loud_log = self._fresh_log()
        seen.clear()
        loud_out = io.StringIO()
        with redirect_stdout(loud_out):
            with self.assertRaises(SystemExit) as loud_caught:
                cli.main(
                    ["--verbose", "--version"],
                    log_basedir=loud_base,
                    log_logdir=loud_log,
                )
        self.assertEqual(loud_caught.exception.code, 0)
        self.assertFalse(seen["kwargs"].get("is_quiet"))
        self.assertIn("Created directory:", loud_out.getvalue())
        self.assertIn("debug mode", loud_out.getvalue())
