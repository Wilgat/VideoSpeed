# TP-TUI — text menu default TUI style (requirement-python-tui)
# TP-OOP-01 — class Tui owns the session and the painter (requirement-python-oop)
# Writer under test: src/VideoSpeed/tui.py. cli.py does not paint the frame.
from __future__ import print_function, unicode_literals

import builtins
import io
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def _menu_rows():
    from VideoSpeed.menu_painter import MenuPainter

    return MenuPainter.MENU_ROWS


def _about_text():
    from VideoSpeed.cli import Cli

    return Cli().about.framework_about()


class FakeScreen:
    def __init__(self, keys, size=(24, 80)):
        self.keys = list(keys)
        self.size = size
        self.drawn = []

    def getmaxyx(self):
        return self.size

    def keypad(self, _flag):
        return None

    def erase(self):
        return None

    def addstr(self, _y, _x, text, _attr=0):
        self.drawn.append(text)

    def refresh(self):
        return None

    def curs_set(self, _visibility):
        return None

    def getch(self):
        if not self.keys:
            return -1
        return self.keys.pop(0)


def _freeze_clock(case, stamp="14:05:09"):
    """Pin time.localtime so a path line can name one clock reading."""
    import time
    from unittest.mock import patch

    hour, minute, second = (int(part) for part in stamp.split(":"))
    fixed = time.struct_time((2026, 10, 2, hour, minute, second, 4, 275, 0))
    patcher = patch("time.localtime", return_value=fixed)
    patcher.start()
    case.addCleanup(patcher.stop)
    return stamp


class TestTui(unittest.TestCase):
    def setUp(self):
        """Point HOME at a temp directory so a menu pick cannot touch this login's language file."""
        import os
        import tempfile

        self._saved_home = os.environ.get("HOME")
        self._saved_lang = os.environ.get("VIDEOSPEED_LANG")
        self._home = tempfile.mkdtemp(prefix="videospeed_menu_home_")
        os.environ["HOME"] = self._home
        os.environ.pop("VIDEOSPEED_LANG", None)

    def tearDown(self):
        import os
        import shutil

        if self._saved_home is None:
            os.environ.pop("HOME", None)
        else:
            os.environ["HOME"] = self._saved_home
        if self._saved_lang is None:
            os.environ.pop("VIDEOSPEED_LANG", None)
        else:
            os.environ["VIDEOSPEED_LANG"] = self._saved_lang
        shutil.rmtree(self._home, ignore_errors=True)

    def _menu(self):
        from VideoSpeed.menu_model import MenuModel
        from VideoSpeed.menu_painter import MenuPainter
        from VideoSpeed.menu_session import MenuScreenError, MenuSession

        painter = MenuPainter()
        return MenuModel, MenuScreenError, MenuSession, painter.format_rows, painter.paint

    def test_tp_tui_01_frame(self):
        """TP-TUI-01: three-row rounded frame, full width, caret, status line."""
        MenuModel, _err, _session, _format_rows, paint = self._menu()
        from VideoSpeed import cli

        model = MenuModel(boards={"front": _menu_rows()})
        model.focus = "input"
        screen = FakeScreen([])
        paint(screen, model, cli.Cli.APP_NAME, cli.Cli._PKG_VERSION)
        _height, width = screen.getmaxyx()
        placeable = width - 1
        inner = placeable - 2
        framed = [line for line in screen.drawn if line[:1] in "╭╰│"]
        self.assertEqual(len(framed), 3, screen.drawn)
        top, field, bottom = framed
        self.assertEqual(top, "╭" + ("─" * inner) + "╮")
        self.assertEqual(len(top), placeable)
        self.assertTrue(field.startswith("│ > █"), field)
        self.assertTrue(field.endswith("│"), field)
        self.assertEqual(len(field), placeable)
        self.assertNotIn("█", field[field.index("█") + 1 :])
        self.assertEqual(bottom, "╰" + ("─" * inner) + "╯")
        self.assertEqual(len(bottom), placeable)
        self.assertNotIn("┌", top)
        self.assertNotIn("+", top)
        flat = "".join(screen.drawn)
        status = "  {} {}  │  main menu  │  Up/Down  •  Enter".format(
            cli.Cli.APP_NAME, cli.Cli._PKG_VERSION
        )
        self.assertIn(status, flat)
        self.assertNotIn("Choice:", flat)
        self.assertLess(flat.index("1. edit"), flat.index("╭"))

    def test_tp_tui_02_columns(self):
        """TP-TUI-02: this board's columns, and wider pads from this package's writer."""
        _model, _err, _session, format_rows, _paint = self._menu()
        from VideoSpeed import cli
        from VideoSpeed.tui import Tui

        lines = Tui().menu_lines()
        self.assertTrue(lines[0].startswith("Path: "))
        self.assertNotIn("main menu", lines[0])
        body = format_rows(_menu_rows())
        self.assertEqual(
            body,
            [
                "1. edit           : cut, speed, and optional boomerang",
                "4. language       : display language for this menu",
                "6. system-log     : view, clear, and the log folder",
                "8. self-management: version, about, and pip lifecycle",
                "9. Exit           : leave",
            ],
        )
        self_body = format_rows(Tui().painter.SELF_ROWS)
        self.assertEqual(
            self_body,
            [
                "82. version       : show the installed version",
                "83. about         : version, FFmpeg, and OpenCV",
                "84. version-check : compare this install with pip",
                "85. self-update   : upgrade this package with pip",
                "86. self-uninstall: remove this package with pip",
                "87. self-install  : install this package with pip",
                " 0. Back          : return to the main menu",
            ],
        )
        self.assertEqual(lines[1:], body)
        width_two = format_rows(
            (
                (11, "version", "show the installed version", "x"),
                (0, "about", "show the cache folders", "x"),
            )
        )
        self.assertEqual(
            width_two,
            [
                "11. version: show the installed version",
                " 0. about  : show the cache folders",
            ],
        )
        width_three = format_rows(
            (
                (232, "version", "show the installed version", "x"),
                (0, "about", "show the cache folders", "x"),
            )
        )
        self.assertEqual(
            width_three,
            [
                "232. version: show the installed version",
                "  0. about  : show the cache folders",
            ],
        )
        painter = (ROOT / "src" / "VideoSpeed" / "menu_painter.py").read_text(encoding="utf-8")
        ship = (ROOT / "src" / "VideoSpeed" / "cli.py").read_text(encoding="utf-8")
        session = (ROOT / "src" / "VideoSpeed" / "tui.py").read_text(encoding="utf-8")
        self.assertIn("FRAME_TOP_LEFT", painter)
        self.assertNotIn("FRAME_TOP_LEFT", ship)
        self.assertNotIn("FRAME_TOP_LEFT", session)
        self.assertNotIn("Choice:", ship)

    def test_tp_tui_03_fail_closed(self):
        """TP-TUI-03: a screen that cannot hold the frame fails closed."""
        import curses

        from VideoSpeed import cli

        class Tiny:
            def getmaxyx(self):
                return (4, 40)

            def keypad(self, _flag):
                return None

            def getch(self):
                return -1

        saved_wrapper = curses.wrapper
        saved_tty = staticmethod(cli.Cli.stdout_is_tty)
        curses.wrapper = lambda fn: fn(Tiny())
        cli.Cli.stdout_is_tty = lambda *args: True
        try:
            err = io.StringIO()
            with redirect_stderr(err):
                action = cli.Cli().tui.open_text_menu()
            text = err.getvalue()
            self.assertEqual(action, "missing")
            self.assertIn("text screen", text)
            self.assertIn("Next:", text)
            self.assertIn("video-speed --help", text)
            self.assertNotIn("Choice:", text)
        finally:
            curses.wrapper = saved_wrapper
            cli.Cli.stdout_is_tty = saved_tty

    def test_tp_tui_03_package_has_no_external_menu(self):
        """TP-TUI-03: product source does not import or declare an external menu package."""
        for path in (SRC / "VideoSpeed").rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("py_tui", text, str(path))
            self.assertNotIn("py-tui", text, str(path))
        manifest = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertNotIn("py-tui", manifest)
        self.assertNotIn("py_tui", manifest)

    def _run_menu(self, keys):
        """Drive the real menu on a fake screen. input() means the TUI was left."""
        import curses

        from VideoSpeed import cli
        from VideoSpeed.encoder import Encoder

        screen = FakeScreen(keys)
        saved_wrapper = curses.wrapper
        saved_out = staticmethod(cli.Cli.stdout_is_tty)
        saved_in = staticmethod(cli.Cli.stdin_is_tty)
        saved_ff = Encoder.ensure_ffmpeg
        saved_input = builtins.input

        def refuse_input(*_args, **_kwargs):
            raise AssertionError("input() left the text screen")

        curses.wrapper = lambda fn: fn(screen)
        cli.Cli.stdout_is_tty = lambda *args: True
        cli.Cli.stdin_is_tty = lambda *args: True
        Encoder.ensure_ffmpeg = lambda self: True
        builtins.input = refuse_input
        out = io.StringIO()
        err = io.StringIO()
        try:
            with redirect_stdout(out), redirect_stderr(err):
                code = cli.main([])
        finally:
            curses.wrapper = saved_wrapper
            cli.Cli.stdout_is_tty = saved_out
            cli.Cli.stdin_is_tty = saved_in
            Encoder.ensure_ffmpeg = saved_ff
            builtins.input = saved_input
        return code, screen, out.getvalue(), err.getvalue()

    def test_tp_tui_04_board_actions(self):
        """TP-TUI-04: Exit leaves, unknown stays, about omits the frame."""
        MenuModel, _err, MenuSession, _format_rows, paint = self._menu()
        from VideoSpeed import cli

        def on_kind(kind):
            if kind == "edit":
                return "leave"
            return None

        session = MenuSession(
            cli.Cli.APP_NAME,
            cli.Cli._PKG_VERSION,
            on_version=lambda: "{} {}".format(cli.Cli.APP_NAME, cli.Cli._PKG_VERSION),
            on_about=_about_text,
            boards={"front": _menu_rows()},
            on_kind=on_kind,
        )
        screen = FakeScreen([ord("1"), 10])
        code = session.run(screen)
        self.assertEqual(code, 0)
        self.assertEqual(session.leave_kind, "edit")
        drawn = "\n".join(screen.drawn)
        flat = "".join(screen.drawn)
        self.assertIn("╭", drawn)
        self.assertNotIn("Choice:", drawn)
        self.assertIn("self-management", flat)
        self.assertNotIn("version-check", flat)

        session = MenuSession(
            cli.Cli.APP_NAME,
            cli.Cli._PKG_VERSION,
            on_version=lambda: cli.Cli._PKG_VERSION,
            on_about=_about_text,
            boards={"front": _menu_rows()},
            on_kind=on_kind,
        )
        screen = FakeScreen([ord("9"), 10])
        code = session.run(screen)
        self.assertEqual(code, 0)
        self.assertIsNone(session.leave_kind)

        model = MenuModel(boards={"front": _menu_rows()})
        model.handle_key(ord("3"))
        stayed = model.handle_key(10)
        self.assertIsNone(stayed)
        self.assertTrue(model.error)
        self.assertEqual(model.layer, "front")

        model = MenuModel(boards={"front": _menu_rows()})
        model.show_result(_about_text())
        screen = FakeScreen([])
        paint(screen, model, cli.Cli.APP_NAME, cli.Cli._PKG_VERSION)
        about = "\n".join(screen.drawn)
        self.assertIn("VideoSpeed", about)
        self.assertIn("Domain:", about)
        self.assertIn("[CHECK SYSTEM]:", about)
        self.assertNotIn("py-tui", about)
        self.assertNotIn("py_tui", about)
        self.assertNotIn("╭", about)
        self.assertIn("Press a key to return to the main menu.", about)

    def test_tp_tui_05_front_board_has_no_hello(self):
        """TP-TUI-05: the front board does not list hello, and 7 stays on that board."""
        MenuModel, _err, _session, _format_rows, _paint = self._menu()

        code, screen, out, err = self._run_menu([ord("7"), 10, -1])
        self.assertEqual(code, 0, err + out)
        flat = "".join(screen.drawn)
        self.assertNotIn("hello", flat)
        self.assertNotIn("Hello.", flat)
        self.assertIn("self-management", flat)
        self.assertNotIn("Choice:", flat)
        model = MenuModel(boards={"front": _menu_rows()})
        model.handle_key(ord("7"))
        stayed = model.handle_key(10)
        self.assertIsNone(stayed)
        self.assertTrue(model.error)
        self.assertEqual(model.layer, "front")

    def test_tp_tui_06_self_management_board(self):
        """TP-TUI-06: row 8 opens self-management; version-check runs pip."""
        from VideoSpeed.self_management import SelfManage

        calls = []

        def fake(self, argv):
            calls.append(list(argv))
            return 0, "pip-ok", ""

        saved = SelfManage._subprocess_runner
        SelfManage._subprocess_runner = fake
        try:
            code, screen, out, err = self._run_menu(
                [ord("8"), 10, ord("8"), ord("4"), 10, -1]
            )
        finally:
            SelfManage._subprocess_runner = saved
        self.assertEqual(code, 0, err + out)
        flat = "".join(screen.drawn)
        self.assertIn("self-management", flat)
        self.assertIn("version-check", flat)
        self.assertIn("self-update", flat)
        self.assertIn("self-uninstall", flat)
        self.assertIn("self-install", flat)
        self.assertIn("pip-ok", flat)
        self.assertNotIn("curl", flat)
        self.assertEqual(calls[0][1:], ["-m", "pip", "index", "versions", "VideoSpeed"])
        self.assertNotIn("sudo", calls[0])

    def test_tp_tui_11_system_log_board(self):
        """TP-TUI-11: row 6 opens system-log; 61 shows a file; 62 empties one; 63 shows logDir()."""
        import os
        import tempfile

        from VideoSpeed.menu_model import MenuModel
        from VideoSpeed.menu_painter import MenuPainter
        from VideoSpeed.system_log import SystemLog
        from VideoSpeed.tui import Tui

        log_body = MenuPainter().format_rows(MenuPainter.LOG_ROWS)
        self.assertEqual(
            log_body,
            [
                "61. view-log  : list a log file and show it",
                "62. clear-log : empty one log file",
                "63. log-folder: show the log folder",
                " 0. Back      : return to the main menu",
            ],
        )
        self.assertTrue(Tui().log_menu_lines()[0].startswith("Path: "))
        front = "\n".join(Tui().menu_lines())
        self.assertIn("4. language", front)
        self.assertIn("6. system-log", front)
        self.assertNotIn("view-log", front)

        model = MenuModel()
        model.handle_key(ord("6"))
        self.assertIsNone(model.handle_key(10))
        self.assertEqual(model.layer, "log")
        self.assertEqual(model.rows()[0][1], "view-log")
        model.handle_key(ord("0"))
        self.assertIsNone(model.handle_key(10))
        self.assertEqual(model.layer, "front")

        blocked = MenuModel()
        blocked.handle_key(ord("4"))
        blocked.handle_key(ord("1"))
        self.assertIsNone(blocked.handle_key(10))
        self.assertTrue(blocked.error)
        self.assertEqual(blocked.layer, "front")

        code, screen, out, err = self._run_menu(
            [ord("6"), 10, ord("6"), ord("3"), 10, -1, -1]
        )
        flat = "".join(screen.drawn)
        self.assertEqual(code, 0, err + out)
        self.assertIn("system-log", flat)
        self.assertIn("view-log", flat)
        self.assertIn("Log folder:", flat)

        class FolderLogger:
            def __init__(self, folder):
                self.folder = folder
                self.messages = []

            def logDir(self):
                return self.folder

            def log_message(self, message, level="INFO", component=""):
                self.messages.append((message, component))

        with tempfile.TemporaryDirectory() as folder:
            kept = os.path.join(folder, "kept.log")
            shown = os.path.join(folder, "shown.log")
            with open(kept, "w", encoding="utf-8") as handle:
                handle.write("keep-me\n")
            with open(shown, "w", encoding="utf-8") as handle:
                handle.write("show-me\n")
            outside = os.path.join(folder, "notes.txt")
            with open(outside, "w", encoding="utf-8") as handle:
                handle.write("not-a-log\n")
            logger = FolderLogger(folder)
            logs = SystemLog(logger=logger)
            names = [path.name for path in logs.log_files()]
            self.assertEqual(names, ["kept.log", "shown.log"])
            tui = Tui(logger=logger)
            page = tui._view_log(FakeScreen([ord("2"), 10]), MenuModel())
            self.assertEqual(page, "shown.log\n\nshow-me\n")
            shown_path = str(Path(shown).resolve())
            kept_path = str(Path(kept).resolve())
            self.assertIn(("read log path={0}".format(shown_path), "menu"), logger.messages)
            declined = tui._clear_log(FakeScreen([ord("1"), 10, ord("n"), 10]), MenuModel())
            self.assertIsNone(declined)
            with open(kept, encoding="utf-8") as handle:
                self.assertEqual(handle.read(), "keep-me\n")
            self.assertFalse(any(message.startswith("clear log ") for message, _component in logger.messages))
            cleared = tui._clear_log(FakeScreen([ord("1"), 10, ord("y"), 10]), MenuModel())
            self.assertEqual(cleared, "Cleared kept.log.")
            with open(kept, encoding="utf-8") as handle:
                self.assertEqual(handle.read(), "")
            self.assertTrue(os.path.isfile(kept))
            self.assertIn(("clear log path={0}".format(kept_path), "menu"), logger.messages)
            self.assertIsNone(tui._clear_log(FakeScreen([ord("2"), 10, 10]), MenuModel()))
            self.assertEqual(tui._log_folder(), "Log folder: {0}".format(folder))
            self.assertIsNone(logs.read_log(outside))
            self.assertFalse(logs.clear_log(outside))
            empty = os.path.join(folder, "blank.log")
            with open(empty, "w", encoding="utf-8"):
                pass
            blank = tui._view_log(FakeScreen([ord("1"), 10]), MenuModel())
            self.assertEqual(blank, "blank.log\n\n(empty)")

    def test_tp_lang_01_language_menu(self):
        """TP-LANG-01: front 4 is language; the file is 0600; reserved numbers and a bad line do not write."""
        import os
        import stat

        from VideoSpeed.language_menu import LanguageMenu
        from VideoSpeed.menu_model import MenuModel
        from VideoSpeed.menu_painter import MenuPainter
        from VideoSpeed.tui import Tui

        self.assertEqual([row[0] for row in MenuPainter.MENU_ROWS], [1, 4, 6, 8, 9])
        self.assertNotIn(5, [row[0] for row in MenuPainter.MENU_ROWS])
        self.assertEqual(
            [row[0] for row in MenuPainter.LANG_ROWS if row[0]],
            list(range(41, 54)),
        )
        self.assertEqual(LanguageMenu.RESERVED, (40, 54, 55, 56, 57, 58, 59))
        self.assertEqual(len(LanguageMenu.CODES), 13)
        self.assertEqual(len(LanguageMenu.LANG_LONG), 12)
        for code, pack in LanguageMenu.LANG_LONG.items():
            self.assertEqual(len(pack), 13, code)

        side = os.path.join(self._home, "side")
        english = LanguageMenu(home=side)
        self.assertEqual(english.code, "en")
        self.assertEqual(english.boards()["front"], MenuPainter.MENU_ROWS)
        self.assertEqual(english.boards()["self"], MenuPainter.SELF_ROWS)
        self.assertEqual(english.boards()["log"], MenuPainter.LOG_ROWS)
        self.assertEqual(english.boards()["lang"], MenuPainter.LANG_ROWS)
        self.assertFalse(os.path.exists(english.path()))
        painter = MenuPainter()
        self.assertEqual(
            painter.format_rows(MenuPainter.LANG_ROWS),
            [
                "41. English   : use English for this menu",
                "42. 简体中文      : use Simplified Chinese for this menu",
                "43. 繁體中文      : use Traditional Chinese for this menu",
                "44. Español   : use Spanish for this menu",
                "45. العربية   : use Arabic for this menu",
                "46. Français  : use French for this menu",
                "47. Português : use Portuguese for this menu",
                "48. Русский   : use Russian for this menu",
                "49. Deutsch   : use German for this menu",
                "50. 日本語       : use Japanese for this menu",
                "51. 한국어       : use Korean for this menu",
                "52. Nederlands: use Dutch for this menu",
                "53. Ελληνικά  : use Greek for this menu",
                " 0. Back      : return to the main menu",
            ],
        )

        os.makedirs(english.directory, mode=0o700)
        with open(english.path(), "w", encoding="utf-8") as handle:
            handle.write("nope\n")
        with open(english.path(), encoding="utf-8") as handle:
            bad_bytes = handle.read()
        loaded = LanguageMenu(home=side)
        self.assertEqual(loaded.code, "en")
        with open(english.path(), encoding="utf-8") as handle:
            self.assertEqual(handle.read(), bad_bytes)

        with open(english.path(), "w", encoding="utf-8", newline="") as handle:
            handle.write("de\r\nfr\n")
        cr = LanguageMenu(home=side)
        self.assertEqual(cr.code, "de")
        with open(english.path(), "rb") as handle:
            stored = handle.read()
        self.assertEqual(stored, b"de\r\nfr\n")

        os.environ["VIDEOSPEED_LANG"] = "es"
        try:
            forced = LanguageMenu(home=side)
            self.assertEqual(forced.code, "es")
            with open(english.path(), "rb") as handle:
                self.assertEqual(handle.read(), stored)
        finally:
            os.environ.pop("VIDEOSPEED_LANG", None)
        os.environ["VIDEOSPEED_LANG"] = "nope"
        try:
            ignored = LanguageMenu(home=side)
            self.assertEqual(ignored.code, "de")
        finally:
            os.environ.pop("VIDEOSPEED_LANG", None)

        menu_file = os.path.join(self._home, ".local", "VideoSpeed", "language")
        code, screen, out, err = self._run_menu([ord("4"), 10, ord("0"), 10, -1])
        self.assertEqual(code, 0, err + out)
        self.assertFalse(os.path.exists(menu_file))
        self.assertIn("English", "".join(screen.drawn))

        code, screen, out, err = self._run_menu(
            [ord(ch) for ch in "en"] + [10, -1]
        )
        self.assertEqual(code, 0, err + out)
        self.assertFalse(os.path.exists(menu_file))
        self.assertIn("That choice is not on this list", "".join(screen.drawn))

        code, screen, out, err = self._run_menu(
            [ord(ch) for ch in "language"] + [10, -1, -1]
        )
        self.assertEqual(code, 0, err + out)
        self.assertFalse(os.path.exists(menu_file))
        self.assertIn("use English for this menu", "".join(screen.drawn))

        for keys in (
            [ord("4"), 10, ord("4"), ord("0"), 10, -1, -1],
            [ord("4"), 10, ord("5"), ord("9"), 10, -1, -1],
        ):
            code, screen, out, err = self._run_menu(keys)
            self.assertEqual(code, 0, err + out)
            self.assertFalse(os.path.exists(menu_file))
            self.assertIn("That choice is not on this list", "".join(screen.drawn))

        code, screen, out, err = self._run_menu(
            [ord("4"), 10, ord("4"), ord("3"), 10, -1]
        )
        self.assertEqual(code, 0, err + out)
        with open(menu_file, encoding="utf-8") as handle:
            self.assertEqual(handle.read(), "zh-Hant\n")
        self.assertEqual(stat.S_IMODE(os.stat(menu_file).st_mode), 0o600)
        flat = "".join(screen.drawn)
        self.assertIn("選單語言是繁體中文", flat)
        self.assertIn("路徑:", flat)

        fresh = os.path.join(self._home, "fresh")
        made = LanguageMenu(home=fresh)
        self.assertTrue(made.save("en"))
        self.assertEqual(stat.S_IMODE(os.stat(made.directory).st_mode), 0o700)
        self.assertEqual(stat.S_IMODE(os.stat(made.path()).st_mode), 0o600)

        class Note:
            def __init__(self):
                self.messages = []

            def log_message(self, message, level="INFO", component=""):
                self.messages.append((message, component))

        note = Note()
        logged = LanguageMenu(logger=note, home=fresh)
        self.assertTrue(logged.save("ja"))
        self.assertIn(("instantiated", "LanguageMenu"), note.messages)
        self.assertIn(
            ("save language path={0}".format(logged.path()), "menu"),
            note.messages,
        )

        keep = os.path.join(self._home, "keep")
        kept = LanguageMenu(home=keep)
        os.makedirs(kept.directory, mode=0o755)
        os.chmod(kept.directory, 0o755)
        self.assertTrue(kept.save("de"))
        self.assertEqual(stat.S_IMODE(os.stat(kept.directory).st_mode), 0o755)
        self.assertEqual(kept.code, "de")
        self.assertFalse(kept.save("nope"))
        self.assertEqual(kept.code, "de")
        with open(kept.path(), encoding="utf-8") as handle:
            self.assertEqual(handle.read(), "de\n")

        fail_home = os.path.join(self._home, "fail")
        os.makedirs(fail_home)
        with open(os.path.join(fail_home, ".local"), "w", encoding="utf-8") as handle:
            handle.write("not-a-directory\n")
        failed = LanguageMenu(home=fail_home)
        self.assertFalse(failed.save("fr"))
        self.assertEqual(failed.code, "en")
        self.assertEqual(failed.failed_line(), "Could not save the menu language")

        class Bag:
            def __init__(self):
                self.model = MenuModel()
                self.painter = MenuPainter()

        bag = Bag()
        tui = Tui(home=fail_home)
        self.assertIsNone(tui._pick_language(bag, "fr"))
        self.assertEqual(tui.language.code, "en")
        self.assertEqual(bag.model.layer, "front")
        self.assertEqual(bag.model.error, "Could not save the menu language")
        zh = LanguageMenu(home=side)
        zh.save("zh-Hant")
        self.assertEqual(
            painter.format_rows(zh.boards()["front"]),
            [
                "1. edit: cut, speed, and optional boomerang",
                "4. 語言  : 這個選單的顯示語言",
                "6. 系統日誌: 檢視、清空，以及日誌資料夾",
                "8. 自我管理: 版本、關於，以及 pip 生命週期",
                "9. 離開  : 離開",
            ],
        )

    def test_tp_tui_12_view_log_stays_through_the_clock_wait(self):
        """TP-TUI-12: the one-second clock wait does not close the log-file question."""
        import os
        import tempfile

        from VideoSpeed.menu_model import MenuModel
        from VideoSpeed.system_log import SystemLog
        from VideoSpeed.tui import Tui

        class ClockQuestionScreen(FakeScreen):
            """The board left timeout(1000) armed. A positive wait returns -1 and keeps the key."""

            def __init__(self, keys):
                super().__init__(keys)
                self.delay = 1000
                self.timeouts = [1000]

            def timeout(self, ms):
                self.delay = ms
                self.timeouts.append(ms)

            def getch(self):
                if self.delay is not None and self.delay >= 0:
                    return -1
                key = super().getch()
                self.delay = 1000
                return key

        class FolderLogger:
            def __init__(self, folder):
                self.folder = folder

            def logDir(self):
                return self.folder

            def log_message(self, message, level="INFO", component=""):
                return None

        with tempfile.TemporaryDirectory() as folder:
            kept = os.path.join(folder, "kept.log")
            shown = os.path.join(folder, "shown.log")
            with open(kept, "w", encoding="utf-8") as handle:
                handle.write("keep-me\n")
            with open(shown, "w", encoding="utf-8") as handle:
                handle.write("show-me\n")
            logger = FolderLogger(folder)
            tui = Tui(logger=logger)
            self.assertEqual(
                [path.name for path in SystemLog(logger=logger).log_files()],
                ["kept.log", "shown.log"],
            )

            listed = ClockQuestionScreen([ord("2"), 10])
            page = tui._view_log(listed, MenuModel())
            self.assertEqual(page, "shown.log\n\nshow-me\n")
            self.assertEqual(listed.keys, [])
            self.assertEqual(listed.timeouts[0], 1000)
            self.assertIn(-1, listed.timeouts)
            self.assertLess(listed.timeouts.index(1000), listed.timeouts.index(-1))

            escaped = ClockQuestionScreen([27])
            self.assertIsNone(tui._view_log(escaped, MenuModel()))
            self.assertEqual(escaped.keys, [])
            self.assertIn(-1, escaped.timeouts)

            cleared = ClockQuestionScreen([ord("1"), 10, ord("y"), 10])
            self.assertEqual(
                tui._clear_log(cleared, MenuModel()),
                "Cleared kept.log.",
            )
            self.assertEqual(cleared.keys, [])
            with open(kept, encoding="utf-8") as handle:
                self.assertEqual(handle.read(), "")

            notice = ClockQuestionScreen([10])
            tui._tui_notice(notice, MenuModel(), ["still here"])
            self.assertEqual(notice.keys, [])
            self.assertIn(-1, notice.timeouts)

    def test_tp_tui_07_path_line(self):
        """TP-TUI-07: the first menu row is Path and the absolute working directory."""
        import os
        import tempfile

        from VideoSpeed import cli
        from VideoSpeed.menu_model import MenuModel
        from VideoSpeed.menu_painter import MenuPainter
        from VideoSpeed.tui import Tui

        from VideoSpeed.language_menu import LanguageMenu

        right = _freeze_clock(self)
        self.assertFalse(hasattr(MenuPainter, "PATH_LABEL_ZH_HANT"))
        self.assertEqual(MenuPainter.PATH_LABEL_EN, "Path")
        painter = MenuPainter()
        self.assertEqual(painter.path_label(), "Path")
        label = LanguageMenu(home=os.path.join(self._home, "label"))
        self.assertEqual(label.path_label(), "Path")
        self.assertTrue(label.save("zh-Hant"))
        self.assertEqual(label.path_label(), "路徑")
        painter.set_path_label(label.path_label())
        self.assertEqual(painter.path_label(), "路徑")
        painter.set_path_label("Path")
        folder = tempfile.mkdtemp(prefix="clips_", dir="/tmp")
        nested = tempfile.mkdtemp(prefix="later_", dir="/tmp")
        previous = os.getcwd()
        saved_user = os.environ.get("USER")
        saved_username = os.environ.get("USERNAME")
        os.environ["USER"] = "clipuser"
        os.environ.pop("USERNAME", None)
        os.chdir(folder)
        try:
            current = os.path.abspath(folder)
            left = "Path: " + current
            self.assertNotIn("clipuser", left)
            logical = left + "  " + right
            self.assertNotIn(cli.Cli.APP_NAME, left)
            self.assertNotIn(cli.Cli._PKG_VERSION, left)
            self.assertEqual(Tui().menu_lines()[0], logical)
            self.assertEqual(Tui().self_menu_lines()[0], logical)
            self.assertEqual(Tui().log_menu_lines()[0], logical)
            self.assertEqual(Tui().language_menu_lines()[0], logical)
            self.assertNotIn("Current:", logical)
            self.assertNotIn("clipuser", logical)
            self.assertFalse(logical.startswith("路徑"))

            model = MenuModel()
            screen = FakeScreen([])
            _height, width = screen.getmaxyx()
            placeable = width - 1
            painted = left + (" " * (placeable - len(left) - len(right))) + right
            painter.paint(screen, model, cli.Cli.APP_NAME, cli.Cli._PKG_VERSION)
            self.assertEqual(screen.drawn[0], painted)
            self.assertTrue(screen.drawn[0].startswith(left))
            flat = "".join(screen.drawn)
            self.assertIn(
                "  {} {}  │  main menu  │  Up/Down  •  Enter".format(
                    cli.Cli.APP_NAME, cli.Cli._PKG_VERSION
                ),
                flat,
            )
            self.assertIn("1. edit", flat)
            self.assertLess(flat.index(left), flat.index("1. edit"))

            model.layer = "self"
            screen.drawn.clear()
            painter.paint(screen, model, cli.Cli.APP_NAME, cli.Cli._PKG_VERSION)
            self.assertEqual(screen.drawn[0], painted)
            flat = "".join(screen.drawn)
            self.assertIn(
                "  {} {}  │  self-management  │  Up/Down  •  Enter".format(
                    cli.Cli.APP_NAME, cli.Cli._PKG_VERSION
                ),
                flat,
            )
            self.assertIn("82. version", flat)
            self.assertNotIn(cli.Cli.APP_NAME, screen.drawn[0])
            self.assertNotIn(cli.Cli._PKG_VERSION, screen.drawn[0])

            tail = 4
            narrow_width = len("Path: ") + tail
            self.assertEqual(painter.path_line(narrow_width), "Path: " + current[-tail:])
            self.assertNotIn(right, painter.path_line(narrow_width))
            narrow = FakeScreen([], size=(24, narrow_width + 1))
            model.layer = "front"
            painter.paint(narrow, model, cli.Cli.APP_NAME, cli.Cli._PKG_VERSION)
            self.assertEqual(narrow.drawn[0], "Path: " + current[-tail:])
            self.assertNotEqual(narrow.drawn[0], painted)
            self.assertTrue(current.endswith(narrow.drawn[0][len("Path: ") :]))

            os.chdir(nested)
            screen.drawn.clear()
            painter.paint(screen, model, cli.Cli.APP_NAME, cli.Cli._PKG_VERSION)
            moved_left = "Path: " + os.path.abspath(nested)
            moved_paint = moved_left + (" " * (placeable - len(moved_left) - len(right))) + right
            self.assertEqual(screen.drawn[0], moved_paint)
            self.assertEqual(Tui().menu_lines()[0], moved_left + "  " + right)
            self.assertNotEqual(moved_left, left)
        finally:
            os.chdir(previous)
            if saved_user is None:
                os.environ.pop("USER", None)
            else:
                os.environ["USER"] = saved_user
            if saved_username is None:
                os.environ.pop("USERNAME", None)
            else:
                os.environ["USERNAME"] = saved_username
            os.rmdir(folder)
            os.rmdir(nested)

    def test_tp_tui_08_login_field_stays_off_the_path_line(self):
        """TP-TUI-08: the withdrawn login field is not drawn on the path line."""
        import inspect

        from VideoSpeed.menu_painter import MenuPainter

        _freeze_clock(self, "08:09:10")
        painter = MenuPainter()
        self.assertFalse(hasattr(painter, "current_label"))
        self.assertFalse(hasattr(painter, "_login_name"))
        self.assertFalse(hasattr(MenuPainter, "CURRENT_LABEL_EN"))
        self.assertFalse(hasattr(MenuPainter, "CURRENT_LABEL_ZH_HANT"))
        line = painter.path_line()
        self.assertNotIn("Current:", line)
        self.assertNotIn("當前", line)
        source = (ROOT / "src" / "VideoSpeed" / "menu_painter.py").read_text(encoding="utf-8")
        self.assertNotIn("getpass", source)
        self.assertNotIn("subprocess", source)
        self.assertNotIn('"id"', source)
        self.assertNotIn("current_label", source)
        self.assertNotIn("_login_name", source)
        self.assertIsNone(inspect.getattr_static(MenuPainter, "current_label", None))
        self.assertIsNone(inspect.getattr_static(MenuPainter, "_login_name", None))

    def test_tp_tui_09_clock_on_the_right(self):
        """TP-TUI-09: the local clock sits on the right when the path row has room."""
        import os

        from VideoSpeed import cli
        from VideoSpeed.menu_model import MenuModel
        from VideoSpeed.menu_painter import MenuPainter
        from VideoSpeed.tui import Tui

        right = _freeze_clock(self, "14:05:09")
        painter = MenuPainter()
        self.assertEqual(painter.clock_text(), right)
        self.assertRegex(right, r"^\d{2}:\d{2}:\d{2}$")
        self.assertEqual(len(right), 8)
        source = (ROOT / "src" / "VideoSpeed" / "menu_painter.py").read_text(encoding="utf-8")
        self.assertIn("localtime", source)
        self.assertNotIn("gmtime", source)
        left = "Path: " + os.path.abspath(os.getcwd())
        logical = painter.path_line()
        self.assertEqual(logical, left + "  " + right)
        self.assertGreaterEqual(logical.find(right) - len(left), 2)
        wide = len(left) + 2 + len(right)
        self.assertEqual(painter.path_line(wide), left + "  " + right)
        self.assertEqual(len(painter.path_line(wide + 5)), wide + 5)
        self.assertTrue(painter.path_line(wide + 5).endswith(right))
        self.assertEqual(painter.path_line(wide - 1), left)
        self.assertNotIn(right, painter.path_line(wide - 1))
        self.assertEqual(Tui().menu_lines()[0], logical)
        self.assertEqual(Tui().self_menu_lines()[0], logical)

        model = MenuModel()
        screen = FakeScreen([])
        _height, width = screen.getmaxyx()
        placeable = width - 1
        painted = left + (" " * (placeable - len(left) - len(right))) + right
        painter.paint(screen, model, cli.Cli.APP_NAME, cli.Cli._PKG_VERSION)
        self.assertEqual(screen.drawn[0], painted)
        model.layer = "self"
        screen.drawn.clear()
        painter.paint(screen, model, cli.Cli.APP_NAME, cli.Cli._PKG_VERSION)
        self.assertEqual(screen.drawn[0], painted)

        model.show_result("page")
        screen.drawn.clear()
        painter.paint(screen, model, cli.Cli.APP_NAME, cli.Cli._PKG_VERSION)
        self.assertEqual(screen.drawn[0], cli.Cli.APP_NAME)
        self.assertFalse(screen.drawn[0].startswith("Path:"))

        model.phase = "board"
        screen.drawn.clear()
        painter.paint_prompt(
            screen,
            model,
            "edit",
            ["Folder?"],
            True,
            cli.Cli.APP_NAME,
            cli.Cli._PKG_VERSION,
            lambda lines, _room, _pin: lines,
        )
        self.assertEqual(screen.drawn[0], cli.Cli.APP_NAME)
        self.assertNotIn(right, screen.drawn[0])

    def test_tp_tui_10_clock_updates_each_second(self):
        """TP-TUI-10: one second with no key redraws the clock and stays on the board."""
        import inspect
        import time
        from unittest.mock import patch

        from VideoSpeed import cli
        from VideoSpeed.menu_session import MenuSession

        counter = {"n": 0}

        def localtime():
            second = counter["n"]
            counter["n"] += 1
            return time.struct_time((2026, 10, 2, 12, 0, second, 4, 275, 0))

        class ClockScreen(FakeScreen):
            def __init__(self, keys):
                super().__init__(keys)
                self.timeouts = []
                self.calls = 0

            def timeout(self, ms):
                self.timeouts.append(ms)

            def getch(self):
                self.calls += 1
                if self.calls > 40:
                    raise AssertionError("the clock wait did not stop")
                return super().getch()

        with patch("time.localtime", side_effect=localtime):
            screen = ClockScreen([-1, ord("9"), 10])
            code = MenuSession(
                cli.Cli.APP_NAME,
                cli.Cli._PKG_VERSION,
                on_version=lambda: cli.Cli._PKG_VERSION,
                on_about=lambda: "about page",
                boards={"front": _menu_rows()},
                on_kind=lambda _kind: None,
            ).run(screen)
        self.assertEqual(code, 0)
        self.assertEqual(screen.keys, [])
        self.assertEqual(screen.timeouts[0], 1000)
        self.assertIn(1000, screen.timeouts)
        path_rows = [line for line in screen.drawn if line.startswith("Path: ")]
        self.assertGreaterEqual(len(path_rows), 2)
        self.assertTrue(path_rows[0].endswith("12:00:00"))
        self.assertTrue(path_rows[1].endswith("12:00:01"))
        self.assertGreaterEqual(path_rows[0].find("12:00:00") - len("Path: "), 2)

        counter["n"] = 0
        with patch("time.localtime", side_effect=localtime):
            screen = ClockScreen(
                [ord("a"), ord("b"), ord("o"), ord("u"), ord("t"), 10, -1, ord("9"), 10]
            )
            code = MenuSession(
                cli.Cli.APP_NAME,
                cli.Cli._PKG_VERSION,
                on_version=lambda: cli.Cli._PKG_VERSION,
                on_about=lambda: "about page",
                boards={"front": _menu_rows()},
                on_kind=lambda _kind: None,
            ).run(screen)
        self.assertEqual(code, 0, screen.timeouts)
        self.assertEqual(screen.keys, [])
        self.assertIn(-1, screen.timeouts)
        self.assertLess(screen.timeouts.index(1000), screen.timeouts.index(-1))

        session_source = (ROOT / "src" / "VideoSpeed" / "menu_session.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("threading", session_source)
        self.assertNotIn("Thread(", session_source)
        wait_source = inspect.getsource(MenuSession._wait_key)
        self.assertNotIn("log_message", wait_source)

    def test_about_result_scrolls_when_the_page_is_long(self):
        """TP-ABOUT-08: a long about page scrolls; a one-line result still closes."""
        import curses

        MenuModel, _err, _session, _format_rows, paint = self._menu()
        from VideoSpeed import cli

        model = MenuModel(boards={"front": _menu_rows()})
        model.show_result("short")
        model.handle_key(curses.KEY_DOWN, 24)
        self.assertEqual(model.phase, "board")

        model.show_result(_about_text())
        screen = FakeScreen([], size=(24, 80))
        paint(screen, model, cli.Cli.APP_NAME, cli.Cli._PKG_VERSION)
        first = "\n".join(screen.drawn)
        self.assertIn("Domain:", first)
        self.assertNotIn("Basic Usage:", first)
        scrolled = first
        found = False
        for _ in range(40):
            model.handle_key(curses.KEY_DOWN, 24)
            screen.drawn.clear()
            paint(screen, model, cli.Cli.APP_NAME, cli.Cli._PKG_VERSION)
            scrolled = "\n".join(screen.drawn)
            if "Basic Usage:" in scrolled:
                found = True
                break
        self.assertTrue(found, scrolled)
        self.assertIn("Up/Down scrolls this page.", scrolled)
        model.handle_key(10, 24)
        self.assertEqual(model.phase, "board")

    def test_tp_tui_04_edit_asks_inside_the_screen(self):
        """TP-TUI-04: edit asks for the folder in the same frame, not via input()."""
        import os
        import tempfile

        code, screen, out, err = self._run_menu([ord("1"), 10])
        self.assertEqual(code, 0, err + out)
        flat = "".join(screen.drawn)
        self.assertIn("Folder (Enter = current):", flat)
        self.assertLess(
            flat.index("Folder (Enter = current):"),
            flat.rfind("╭"),
        )
        self.assertNotIn("====", out)
        self.assertNotIn("Folder (Enter = current):", out)
        self.assertNotIn("Choice:", flat)

        code, screen, out, err = self._run_menu(
            [ord("1"), 10] + [ord(c) for c in "no-such-videospeed-folder"] + [10, 27]
        )
        self.assertEqual(code, 0, err + out)
        flat = "".join(screen.drawn)
        self.assertIn("ERROR: Not a directory: no-such-videospeed-folder", flat)
        self.assertNotIn("Not a directory", err)

        folder = tempfile.mkdtemp(prefix="videospeed_tui_")
        try:
            code, screen, out, err = self._run_menu(
                [ord("1"), 10] + [ord(c) for c in folder] + [10]
            )
            flat = "".join(screen.drawn)
            self.assertIn("No MP4 files found!", flat)
            self.assertNotIn("No MP4 files found!", out)
            self.assertNotIn("No MP4 files found!", err)
            self.assertEqual(code, 0, err + out)
        finally:
            os.rmdir(folder)

    def test_edit_shows_saved_name_after_full_length(self):
        """Full length, 100%, no boomerang: the screen shows the saved name."""
        import tempfile

        from VideoSpeed import cli
        from VideoSpeed.encoder import Encoder
        from VideoSpeed.media_info import MediaInfo
        from VideoSpeed.menu_model import MenuModel

        folder = Path(tempfile.mkdtemp(prefix="vs_edit_"))
        (folder / "clip.mp4").write_bytes(b"")
        saved = {}

        def fake_duration(_path):
            return 1.0

        def fake_job(video_path, start, end, ratio, boomerang):
            saved["args"] = (start, end, ratio, boomerang)
            out = video_path.parent / "clip_cut0.0-1.0s_100pct.mp4"
            out.write_bytes(b"ok")
            return out

        keys = [ord(c) for c in str(folder)] + [10]
        keys += [ord("1"), 10, 10, 10, 10, 10]
        screen = FakeScreen(keys)
        model = MenuModel(boards={"front": _menu_rows()})
        original = (Encoder.ensure_ffmpeg, MediaInfo.get_duration_cv2, Encoder.process_job)
        Encoder.ensure_ffmpeg = lambda self: True
        MediaInfo.get_duration_cv2 = lambda self, path: fake_duration(path)
        Encoder.process_job = lambda self, video_path, start, end, ratio, boomerang: fake_job(
            video_path, start, end, ratio, boomerang
        )
        try:
            cli.Cli().tui._edit_in_tui(screen, model)
        finally:
            Encoder.ensure_ffmpeg, MediaInfo.get_duration_cv2, Encoder.process_job = original
            for path in folder.iterdir():
                path.unlink()
            folder.rmdir()
        flat = "\n".join(screen.drawn)
        self.assertEqual(saved["args"], (0.0, 1.0, 100.0, False))
        self.assertIn(
            "Saved clip_cut0.0-1.0s_100pct.mp4 — Again? (y/n):",
            flat,
        )

    def _run_verb(self, argv, keys, cwd=None):
        """Drive one product verb on a fake screen. input() means the TUI was left."""
        import curses
        import os

        from VideoSpeed import cli
        from VideoSpeed.encoder import Encoder

        screen = FakeScreen(keys)
        saved_wrapper = curses.wrapper
        saved_out = staticmethod(cli.Cli.stdout_is_tty)
        saved_in = staticmethod(cli.Cli.stdin_is_tty)
        saved_ff = Encoder.ensure_ffmpeg
        saved_job = Encoder.process_job
        saved_input = builtins.input
        jobs = []
        ffmpeg_calls = []

        def refuse_input(*_args, **_kwargs):
            raise AssertionError("input() left the text screen")

        def count_ffmpeg(self):
            ffmpeg_calls.append(1)
            return True

        curses.wrapper = lambda fn: fn(screen)
        cli.Cli.stdout_is_tty = lambda *args: True
        cli.Cli.stdin_is_tty = lambda *args: True
        Encoder.ensure_ffmpeg = count_ffmpeg
        Encoder.process_job = lambda self, *args, **_kwargs: jobs.append(args) or None
        builtins.input = refuse_input
        previous = os.getcwd()
        if cwd is not None:
            os.chdir(cwd)
        out = io.StringIO()
        err = io.StringIO()
        try:
            with redirect_stdout(out), redirect_stderr(err):
                code = cli.main(list(argv))
        finally:
            curses.wrapper = saved_wrapper
            cli.Cli.stdout_is_tty = saved_out
            cli.Cli.stdin_is_tty = saved_in
            Encoder.ensure_ffmpeg = saved_ff
            Encoder.process_job = saved_job
            builtins.input = saved_input
            os.chdir(previous)
        return code, screen, out.getvalue(), err.getvalue(), jobs, ffmpeg_calls

    def test_tp_mode_05_edit_starts_inside_the_frame(self):
        """TP-MODE-05: edit on a terminal asks folder, then the video, inside the frame."""
        import os
        import tempfile

        folder = tempfile.mkdtemp(prefix="videospeed_edit_")
        clip = Path(folder) / "clip.mp4"
        clip.write_bytes(b"")
        try:
            code, screen, out, err, jobs, _ff = self._run_verb(
                ["edit"], [10], cwd=folder
            )
            flat = "".join(screen.drawn)
            self.assertEqual(code, 0, err + out)
            self.assertIn("Folder (Enter = current):", flat)
            self.assertIn("Choose video (1–1):", flat)
            self.assertLess(
                flat.index("Folder (Enter = current):"),
                flat.index("Choose video (1–1):"),
            )
            self.assertLess(
                flat.index("Folder (Enter = current):"),
                flat.index("1. edit"),
            )
            self.assertLess(
                flat.index("Folder (Enter = current):"),
                flat.rfind("╭"),
            )
            self.assertNotIn("Folder (Enter = current):", out)
            self.assertNotIn("Choice:", flat)
            self.assertEqual(jobs, [])

            code, screen, out, err, jobs, _ff = self._run_verb(
                ["edit", "--folder", folder], []
            )
            flat = "".join(screen.drawn)
            self.assertEqual(code, 0, err + out)
            self.assertNotIn("Folder (Enter = current):", flat)
            self.assertIn("Choose video (1–1):", flat)
            self.assertEqual(jobs, [])

            code, screen, out, err, jobs, _ff = self._run_verb(
                ["edit", "--percent", "50"], [10], cwd=folder
            )
            flat = "".join(screen.drawn)
            self.assertEqual(code, 0, err + out)
            self.assertIn("Folder (Enter = current):", flat)
            self.assertNotIn("need --file", err)
            self.assertEqual(jobs, [])
        finally:
            clip.unlink()
            os.rmdir(folder)

    def test_tp_mode_07_list_mp4_on_a_terminal(self):
        """TP-MODE-07: list-mp4 on a terminal asks for the folder, lists, and does not encode."""
        import os
        import tempfile

        folder = tempfile.mkdtemp(prefix="videospeed_list_")
        clip = Path(folder) / "clip.mp4"
        clip.write_bytes(b"")
        empty = tempfile.mkdtemp(prefix="videospeed_list_")
        try:
            code, screen, out, err, jobs, ffmpeg_calls = self._run_verb(
                ["list-mp4"], [10], cwd=folder
            )
            flat = "".join(screen.drawn)
            self.assertEqual(code, 0, err + out)
            self.assertIn("Folder (Enter = current):", flat)
            self.assertIn("1. clip.mp4", flat)
            self.assertNotIn("Choose video", flat)
            self.assertLess(
                flat.index("Folder (Enter = current):"),
                flat.index("1. clip.mp4"),
            )
            self.assertNotIn("Processing", out + err)
            self.assertEqual(jobs, [])
            self.assertEqual(ffmpeg_calls, [])

            code, screen, out, err, jobs, ffmpeg_calls = self._run_verb(
                ["list-mp4", "--folder", folder], []
            )
            flat = "".join(screen.drawn)
            self.assertEqual(code, 0, err + out)
            self.assertNotIn("Folder (Enter = current):", flat)
            self.assertIn("1. clip.mp4", flat)
            self.assertEqual(jobs, [])
            self.assertEqual(ffmpeg_calls, [])

            code, screen, out, err, jobs, _ff = self._run_verb(
                ["list-mp4"], [27], cwd=empty
            )
            self.assertEqual(code, 0, err + out)
            self.assertEqual(jobs, [])

            code, screen, out, err, jobs, _ff = self._run_verb(
                ["list-mp4", "--folder", empty], []
            )
            flat = "".join(screen.drawn)
            self.assertEqual(code, 1, err + out)
            self.assertIn("No MP4 files found!", flat)
            self.assertNotIn("Choose video", flat)
            self.assertEqual(jobs, [])
        finally:
            clip.unlink()
            os.rmdir(folder)
            os.rmdir(empty)

    def test_tp_oop_01_tui_owns_the_menu(self):
        """TP-OOP-01: class Tui in tui.py owns the session. Those functions are not in cli.py."""
        import inspect

        from VideoSpeed import cli
        from VideoSpeed.tui import Tui

        self.assertTrue(inspect.isclass(Tui))
        self.assertEqual(
            Path(inspect.getfile(Tui)).resolve(),
            (ROOT / "src" / "VideoSpeed" / "tui.py").resolve(),
        )
        names = (
            "open_text_menu",
            "menu_lines",
            "log_menu_lines",
            "language_menu_lines",
            "framework_hello",
            "_view_log",
            "_clear_log",
            "_log_folder",
            "_edit_in_tui",
            "_list_in_tui",
            "_open_direct_screen",
            "_visible_lines",
            "_tui_read",
            "_tui_notice",
            "_tui_float",
            "_tui_yes_no",
            "_tui_index",
        )
        ship = (ROOT / "src" / "VideoSpeed" / "cli.py").read_text(encoding="utf-8")
        session = (ROOT / "src" / "VideoSpeed" / "tui.py").read_text(encoding="utf-8")
        for name in names:
            self.assertTrue(inspect.isfunction(inspect.getattr_static(Tui, name)), name)
            self.assertFalse(inspect.isfunction(getattr(cli, name, None)), name)
            self.assertNotIn("\ndef {}(".format(name), "\n" + ship)
        self.assertIn("class Tui", session)
        self.assertNotIn("class MenuSession", session)
        self.assertNotIn("class MenuModel", session)
        self.assertIn("Tui(", ship)
        self.assertFalse((ROOT / "src" / "VideoSpeed" / "menu.py").exists())

    def test_tp_oop_03_one_class_per_menu_file(self):
        """TP-OOP-03: painter, model, and session each have their own module."""
        import inspect
        import re

        from VideoSpeed.menu_model import MenuModel
        from VideoSpeed.menu_painter import MenuPainter
        from VideoSpeed.menu_session import MenuScreenError, MenuSession

        painter_names = (
            "paint",
            "paint_prompt",
            "format_rows",
            "path_label",
            "set_path_label",
            "clock_text",
            "path_line",
            "row_parts",
            "rows_for",
            "screen_can_hold_box",
            "_put",
            "_paint_box",
            "_input_field",
            "_status_line",
            "_result_overflow",
            "_result_room",
        )
        for name in painter_names:
            self.assertTrue(inspect.isfunction(inspect.getattr_static(MenuPainter, name)), name)
        self.assertEqual(MenuPainter.FRAME_TOP_LEFT, "╭")
        self.assertEqual(MenuPainter.MENU_ROWS[0][1], "edit")
        self.assertTrue(inspect.isfunction(inspect.getattr_static(MenuModel, "edge_keys")))
        self.assertTrue(inspect.isfunction(inspect.getattr_static(MenuSession, "run")))
        self.assertTrue(inspect.isfunction(inspect.getattr_static(MenuSession, "_wait_key")))
        self.assertTrue(issubclass(MenuScreenError, Exception))
        homes = {
            MenuPainter: "menu_painter.py",
            MenuModel: "menu_model.py",
            MenuSession: "menu_session.py",
        }
        for cls, filename in homes.items():
            self.assertEqual(Path(inspect.getfile(cls)).name, filename)
        session_file = (ROOT / "src" / "VideoSpeed" / "menu_session.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("class MenuScreenError", session_file)
        tui_text = (ROOT / "src" / "VideoSpeed" / "tui.py").read_text(encoding="utf-8")
        ship = (ROOT / "src" / "VideoSpeed" / "cli.py").read_text(encoding="utf-8")
        self.assertEqual(re.findall(r"^class (\w+)", tui_text, re.M), ["Tui"])
        lang_text = (ROOT / "src" / "VideoSpeed" / "language_menu.py").read_text(
            encoding="utf-8"
        )
        self.assertEqual(re.findall(r"^class (\w+)", lang_text, re.M), ["LanguageMenu"])
        self.assertIn("LanguageMenu(", tui_text)
        self.assertNotIn("LanguageMenu(", ship)
        self.assertNotIn("FRAME_TOP_LEFT", ship)
        self.assertNotIn("FRAME_TOP_LEFT", tui_text)


if __name__ == "__main__":
    unittest.main()
