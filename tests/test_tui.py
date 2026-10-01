# TP-TUI — text menu default TUI style (requirement-python-tui)
# Writer under test: src/VideoSpeed/menu.py. cli.py does not paint the frame.
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


class TestTui(unittest.TestCase):
    def _menu(self):
        from VideoSpeed.menu import (
            MenuModel,
            MenuScreenError,
            MenuSession,
            format_rows,
            paint,
        )

        return MenuModel, MenuScreenError, MenuSession, format_rows, paint

    def test_tp_tui_01_frame(self):
        """TP-TUI-01: three-row rounded frame, full width, caret, status line."""
        MenuModel, _err, _session, _format_rows, paint = self._menu()
        from VideoSpeed import cli

        model = MenuModel(boards={"front": cli.MENU_ROWS})
        model.focus = "input"
        screen = FakeScreen([])
        paint(screen, model, cli.APP_NAME, cli._PKG_VERSION)
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
            cli.APP_NAME, cli._PKG_VERSION
        )
        self.assertIn(status, flat)
        self.assertNotIn("Choice:", flat)
        self.assertLess(flat.index("1. edit"), flat.index("╭"))

    def test_tp_tui_02_columns(self):
        """TP-TUI-02: this board's columns, and wider pads from this package's writer."""
        _model, _err, _session, format_rows, _paint = self._menu()
        from VideoSpeed import cli

        lines = cli.menu_lines()
        self.assertTrue(lines[0].startswith("VideoSpeed ("))
        self.assertIn("main menu", lines[0])
        body = format_rows(cli.MENU_ROWS)
        self.assertEqual(
            body,
            [
                "1. edit : cut, speed, and optional boomerang",
                "8. about: version, FFmpeg, and OpenCV",
                "9. Exit : leave",
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
        painter = (ROOT / "src" / "VideoSpeed" / "menu.py").read_text(encoding="utf-8")
        ship = (ROOT / "src" / "VideoSpeed" / "cli.py").read_text(encoding="utf-8")
        self.assertIn("FRAME_TOP_LEFT", painter)
        self.assertNotIn("FRAME_TOP_LEFT", ship)
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
        saved_tty = cli.stdout_is_tty
        curses.wrapper = lambda fn: fn(Tiny())
        cli.stdout_is_tty = lambda: True
        try:
            err = io.StringIO()
            with redirect_stderr(err):
                action = cli.open_text_menu()
            text = err.getvalue()
            self.assertEqual(action, "missing")
            self.assertIn("text screen", text)
            self.assertIn("Next:", text)
            self.assertIn("video-speed --help", text)
            self.assertNotIn("Choice:", text)
        finally:
            curses.wrapper = saved_wrapper
            cli.stdout_is_tty = saved_tty

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

        screen = FakeScreen(keys)
        saved_wrapper = curses.wrapper
        saved_out = cli.stdout_is_tty
        saved_in = cli.stdin_is_tty
        saved_ff = cli.ensure_ffmpeg
        saved_input = builtins.input

        def refuse_input(*_args, **_kwargs):
            raise AssertionError("input() left the text screen")

        curses.wrapper = lambda fn: fn(screen)
        cli.stdout_is_tty = lambda: True
        cli.stdin_is_tty = lambda: True
        cli.ensure_ffmpeg = lambda: True
        builtins.input = refuse_input
        out = io.StringIO()
        err = io.StringIO()
        try:
            with redirect_stdout(out), redirect_stderr(err):
                code = cli.main([])
        finally:
            curses.wrapper = saved_wrapper
            cli.stdout_is_tty = saved_out
            cli.stdin_is_tty = saved_in
            cli.ensure_ffmpeg = saved_ff
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
            cli.APP_NAME,
            cli._PKG_VERSION,
            on_version=lambda: "{} {}".format(cli.APP_NAME, cli._PKG_VERSION),
            on_about=cli.framework_about,
            boards={"front": cli.MENU_ROWS},
            on_kind=on_kind,
        )
        screen = FakeScreen([ord("1"), 10])
        code = session.run(screen)
        self.assertEqual(code, 0)
        self.assertEqual(session.leave_kind, "edit")
        drawn = "\n".join(screen.drawn)
        self.assertIn("╭", drawn)
        self.assertNotIn("Choice:", drawn)
        self.assertNotIn("self-management", drawn)

        session = MenuSession(
            cli.APP_NAME,
            cli._PKG_VERSION,
            on_version=lambda: cli._PKG_VERSION,
            on_about=cli.framework_about,
            boards={"front": cli.MENU_ROWS},
            on_kind=on_kind,
        )
        screen = FakeScreen([ord("9"), 10])
        code = session.run(screen)
        self.assertEqual(code, 0)
        self.assertIsNone(session.leave_kind)

        model = MenuModel(boards={"front": cli.MENU_ROWS})
        model.handle_key(ord("3"))
        stayed = model.handle_key(10)
        self.assertIsNone(stayed)
        self.assertTrue(model.error)
        self.assertEqual(model.layer, "front")

        model = MenuModel(boards={"front": cli.MENU_ROWS})
        model.show_result(cli.framework_about())
        screen = FakeScreen([])
        paint(screen, model, cli.APP_NAME, cli._PKG_VERSION)
        about = "\n".join(screen.drawn)
        self.assertIn("VideoSpeed", about)
        self.assertIn("Domain:", about)
        self.assertIn("[CHECK SYSTEM]:", about)
        self.assertNotIn("py-tui", about)
        self.assertNotIn("py_tui", about)
        self.assertNotIn("╭", about)
        self.assertIn("Press a key to return to the main menu.", about)

    def test_about_result_scrolls_when_the_page_is_long(self):
        """TP-ABOUT-08: a long about page scrolls; a one-line result still closes."""
        import curses

        MenuModel, _err, _session, _format_rows, paint = self._menu()
        from VideoSpeed import cli

        model = MenuModel(boards={"front": cli.MENU_ROWS})
        model.show_result("short")
        model.handle_key(curses.KEY_DOWN, 24)
        self.assertEqual(model.phase, "board")

        model.show_result(cli.framework_about())
        screen = FakeScreen([], size=(24, 80))
        paint(screen, model, cli.APP_NAME, cli._PKG_VERSION)
        first = "\n".join(screen.drawn)
        self.assertIn("Domain:", first)
        self.assertNotIn("Basic Usage:", first)
        for _ in range(16):
            model.handle_key(curses.KEY_DOWN, 24)
        screen.drawn.clear()
        paint(screen, model, cli.APP_NAME, cli._PKG_VERSION)
        scrolled = "\n".join(screen.drawn)
        self.assertIn("Basic Usage:", scrolled)
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


if __name__ == "__main__":
    unittest.main()
