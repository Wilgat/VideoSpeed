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


class TestTui(unittest.TestCase):
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
        from VideoSpeed.tui import Tui

        lines = Tui().menu_lines()
        self.assertTrue(lines[0].startswith("VideoSpeed ("))
        self.assertIn("main menu", lines[0])
        body = format_rows(_menu_rows())
        self.assertEqual(
            body,
            [
                "1. edit           : cut, speed, and optional boomerang",
                "7. hello          : show a hello message",
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
        saved_tty = cli.Cli.stdout_is_tty
        curses.wrapper = lambda fn: fn(Tiny())
        cli.Cli.stdout_is_tty = lambda self: True
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
        saved_out = cli.Cli.stdout_is_tty
        saved_in = cli.Cli.stdin_is_tty
        saved_ff = Encoder.ensure_ffmpeg
        saved_input = builtins.input

        def refuse_input(*_args, **_kwargs):
            raise AssertionError("input() left the text screen")

        curses.wrapper = lambda fn: fn(screen)
        cli.Cli.stdout_is_tty = lambda self: True
        cli.Cli.stdin_is_tty = lambda self: True
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
            cli.APP_NAME,
            cli._PKG_VERSION,
            on_version=lambda: "{} {}".format(cli.APP_NAME, cli._PKG_VERSION),
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
            cli.APP_NAME,
            cli._PKG_VERSION,
            on_version=lambda: cli._PKG_VERSION,
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
        paint(screen, model, cli.APP_NAME, cli._PKG_VERSION)
        about = "\n".join(screen.drawn)
        self.assertIn("VideoSpeed", about)
        self.assertIn("Domain:", about)
        self.assertIn("[CHECK SYSTEM]:", about)
        self.assertNotIn("py-tui", about)
        self.assertNotIn("py_tui", about)
        self.assertNotIn("╭", about)
        self.assertIn("Press a key to return to the main menu.", about)

    def test_tp_tui_05_hello_shows_the_message(self):
        """TP-TUI-05: menu 7 shows Hello. on the result page and omits the frame."""
        MenuModel, _err, _session, _format_rows, paint = self._menu()
        from VideoSpeed import cli

        from VideoSpeed.tui import Tui

        self.assertEqual(Tui().framework_hello(), "Hello.")
        code, screen, out, err = self._run_menu([ord("7"), 10])
        self.assertEqual(code, 0, err + out)
        flat = "".join(screen.drawn)
        self.assertIn("7. hello          : show a hello message", flat)
        self.assertIn("Hello.", flat)
        self.assertIn("Press a key to return to the main menu.", flat)
        self.assertNotIn("Hello.", out)
        self.assertNotIn("Choice:", flat)

        model = MenuModel(boards={"front": _menu_rows()})
        model.show_result(Tui().framework_hello())
        page = FakeScreen([])
        paint(page, model, cli.APP_NAME, cli._PKG_VERSION)
        hello = "\n".join(page.drawn)
        self.assertIn("Hello.", hello)
        self.assertNotIn("╭", hello)
        self.assertIn("Press a key to return to the main menu.", hello)

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
        saved_out = cli.Cli.stdout_is_tty
        saved_in = cli.Cli.stdin_is_tty
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
        cli.Cli.stdout_is_tty = lambda self: True
        cli.Cli.stdin_is_tty = lambda self: True
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
            "framework_hello",
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
            self.assertTrue(inspect.isfunction(Tui.__dict__[name]), name)
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
            self.assertTrue(inspect.isfunction(MenuPainter.__dict__[name]), name)
        self.assertEqual(MenuPainter.FRAME_TOP_LEFT, "╭")
        self.assertEqual(MenuPainter.MENU_ROWS[0][1], "edit")
        self.assertTrue(inspect.isfunction(MenuModel.__dict__["edge_keys"]))
        self.assertTrue(inspect.isfunction(MenuSession.__dict__["run"]))
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
        self.assertEqual(re.findall(r"^class (\w+)", tui_text, re.M), ["Tui"])
        ship = (ROOT / "src" / "VideoSpeed" / "cli.py").read_text(encoding="utf-8")
        self.assertNotIn("FRAME_TOP_LEFT", ship)
        self.assertNotIn("FRAME_TOP_LEFT", tui_text)


if __name__ == "__main__":
    unittest.main()
