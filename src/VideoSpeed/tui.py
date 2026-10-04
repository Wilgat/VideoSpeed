# =============================================================================
# Text menu session for VideoSpeed.
# requirement-python-tui — menu region and the bottom input box.
# requirement-python-oop — this module defines class Tui only.
# The frame is class MenuPainter. cli.py constructs Tui and calls it.
# =============================================================================
from __future__ import annotations

import curses

from .language_menu import LanguageMenu
from .menu_painter import MenuPainter
from .menu_session import MenuScreenError, MenuSession
from .system_log import SystemLog



class Tui:
    """Text menu session. Prompts and the front board.

    MenuModel, MenuSession, and MenuPainter live in their own modules.
    The menu rows stay the front board from requirement-python-tui.
    """

    def __init__(self, app=None, app_name="VideoSpeed", version=None, logger=None, home=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="Tui")
        self.app = app
        self.app_name = app_name
        if version is None:
            from . import __version__
            version = __version__
        self.version = version
        self.painter = MenuPainter(logger=logger)
        self.system_log = SystemLog(logger=logger)
        name = app_name
        if app is not None and getattr(app, "app_name", None):
            name = app.app_name
        self.language = LanguageMenu(logger=logger, app_name=name, home=home)
        self.painter.set_path_label(self.language.path_label())

    def _name(self):
        if self.app is not None:
            return self.app.app_name
        return self.app_name

    def _ver(self):
        if self.app is not None:
            return self.app.version
        return self.version

    def menu_lines(self):
        """
        General Purpose: Path line and aligned menu rows for the text screen.
        The first row is the current directory. The column widths come from
        MenuPainter, so a shorter verb is padded before the colon.
        """
        return [self.painter.path_line()] + self.painter.format_rows(self.language.boards()["front"])

    def self_menu_lines(self):
        """General Purpose: Path line and rows for the self-management board under 8."""
        return [self.painter.path_line()] + self.painter.format_rows(self.language.boards()["self"])

    def log_menu_lines(self):
        """General Purpose: Path line and rows for the system-log board under 6."""
        return [self.painter.path_line()] + self.painter.format_rows(self.language.boards()["log"])

    def language_menu_lines(self):
        """General Purpose: Path line and rows for the language board under 4."""
        return [self.painter.path_line()] + self.painter.format_rows(self.language.boards()["lang"])

    def framework_help(self):
        """
        General Purpose: Help text for the typed help verb on the text screen.
        requirement-python-tui: help is a self-management verb and is not a numbered row.
        """
        return (
            "help: usage for VideoSpeed.\n"
            "Verbs: help, version, about, edit, list-mp4, "
            "self-install, version-check, self-update, self-uninstall.\n"
            "version shows the installed version.\n"
            "version-check runs: python -m pip index versions VideoSpeed\n"
            "self-update runs: python -m pip install --upgrade VideoSpeed\n"
            "self-install runs: python -m pip install VideoSpeed\n"
            "self-uninstall runs: python -m pip uninstall -y VideoSpeed\n"
            "On the command line, self-uninstall also needs --force.\n"
            "edit asks for a folder, then a file. list-mp4 lists and does not encode."
        )

    def _boards(self):
        return self.language.boards()

    def _apply_language(self, session):
        """Copy the current language onto the session. Does not construct a class."""
        self.language.apply_to(session.model, session.painter)
        self.painter.set_path_label(self.language.path_label())

    def _pick_language(self, session, code):
        """Save one code, then return to the front board in that language."""
        saved = self.language.save(code)
        self._apply_language(session)
        if saved:
            session.model.error = self.language.saved_line()
        else:
            session.model.error = self.language.failed_line()
        session.model.layer = "front"
        session.model.index = 0
        session.model.buffer = ""
        session.model.cursor = 0
        session.model.focus = "list"
        return None

    def _visible_lines(self, lines, room, pin_last):
        """General Purpose: Lines that fit above the input box.

        A question pins its last line so the prompt stays on screen. A job log
        keeps the newest lines.
        """
        if room < 1:
            return []
        if len(lines) <= room:
            return list(lines)
        if not pin_last:
            return list(lines[-room:])
        if room == 1:
            return [lines[-1]]
        return list(lines[: room - 2]) + ["…", lines[-1]]

    def _paint_lines(self, screen, model, title, lines, pin_last):
        """Hand one question to MenuPainter. The session does not draw a second frame."""
        self.painter.paint_prompt(
            screen,
            model,
            title,
            lines,
            pin_last,
            self._name(),
            self._ver(),
            self._visible_lines,
        )

    def _tui_read(self, screen, model, lines, title="edit"):
        """
        General Purpose: Read one line from the bottom input box.

        Returns the text, or None when the person presses Esc. The board's
        one-second clock wait is cleared before each key, so that wait is
        not Esc. requirement-python-tui rule 13.
        """
        model.buffer = ""
        model.cursor = 0
        model.focus = "input"
        while True:
            self._paint_lines(screen, model, title, lines, pin_last=True)
            # Rule 13: a no-key from the board clock must not close this question.
            arm = getattr(screen, "timeout", None)
            if arm is not None:
                arm(-1)
            key = screen.getch()
            if key in (-1, 27):
                model.error = ""
                model.buffer = ""
                model.cursor = 0
                model.focus = "list"
                return None
            if key in (10, 13, curses.KEY_ENTER):
                text = model.buffer
                model.buffer = ""
                model.cursor = 0
                model.error = ""
                return text
            if key in (curses.KEY_BACKSPACE, 127, 8):
                model._backspace()
                model.error = ""
                continue
            if key in (curses.KEY_LEFT, curses.KEY_RIGHT) or key in model.edge_keys():
                model._slide(key)
                continue
            if key in (curses.KEY_UP, curses.KEY_DOWN):
                continue
            if 32 <= key < 127:
                model._insert(chr(key))
                model.error = ""
                continue

    def _tui_notice(self, screen, model, lines):
        """General Purpose: Show lines on the edit screen until the next key."""
        model.buffer = ""
        model.cursor = 0
        model.focus = "list"
        model.error = ""
        body = list(lines) + ["", "Press a key to return to the main menu."]
        self._paint_lines(screen, model, "edit", body, pin_last=True)
        # Rule 13: the board clock's one-second wait is not this notice.
        arm = getattr(screen, "timeout", None)
        if arm is not None:
            arm(-1)
        try:
            screen.getch()
        except Exception:
            return

    def _tui_float(self, screen, model, lines, default=None):
        """General Purpose: Read a float from the box; empty uses default."""
        while True:
            raw = self._tui_read(screen, model, lines)
            if raw is None:
                return None
            raw = raw.strip()
            if raw == "" and default is not None:
                return float(default)
            try:
                return float(raw.replace("%", ""))
            except ValueError:
                model.error = "Please enter a number"

    def _tui_yes_no(self, screen, model, lines, default_no=True, title="edit"):
        """General Purpose: y/n from the box; empty uses the default."""
        while True:
            raw = self._tui_read(screen, model, lines, title=title)
            if raw is None:
                return None
            raw = raw.strip().lower()
            if raw == "":
                return not default_no
            if raw in ("y", "yes"):
                return True
            if raw in ("n", "no"):
                return False
            model.error = "Please enter y or n"

    def _tui_index(self, screen, model, lines, count, title="edit"):
        """General Purpose: Read a 1-based index from the box; re-ask on error."""
        while True:
            raw = self._tui_read(screen, model, lines, title=title)
            if raw is None:
                return None
            raw = raw.strip()
            try:
                idx = int(raw)
            except ValueError:
                model.error = "Please type a number"
                continue
            if 1 <= idx <= count:
                return idx - 1
            model.error = "Enter 1–{}".format(count)

    def open_text_menu(self):
        """
        General Purpose: Draw the text menu and keep edit's questions on it.

        The session is MenuSession with this product's name, package version,
        and MENU_ROWS. edit asks for the folder and the later steps in the
        same bottom box. Returns "missing" when the screen cannot open, and
        None when the person leaves.
        """
        app = self.app
        if not app.stdout_is_tty():
            app.output.out_err(
                "ERROR: No terminal for the text menu. "
                "Next: pass --file, --start, and --end, or run in a terminal."
            )
            return "missing"
        try:
            import curses
        except ImportError:
            app.output.out_err("ERROR: The text menu could not be loaded.")
            app.output.out_err("   Next: video-speed --help")
            return "missing"

        screen_box = {}

        def on_kind(kind):
            if kind == "help":
                return self.framework_help()
            if kind in ("version-check", "self-update", "self-install", "self-uninstall"):
                _code, text = app.self_manage.run_text(kind)
                return text
            if kind == "list-mp4":
                screen = screen_box.get("screen")
                if screen is not None:
                    self._list_in_tui(screen, session.model)
                return None
            if kind == "view-log":
                screen = screen_box.get("screen")
                if screen is None:
                    return None
                return self._view_log(screen, session.model)
            if kind == "clear-log":
                screen = screen_box.get("screen")
                if screen is None:
                    return None
                return self._clear_log(screen, session.model)
            if kind == "log-folder":
                return self._log_folder()
            if kind in self.language.CODES:
                return self._pick_language(session, kind)
            if kind != "edit":
                return None
            screen = screen_box.get("screen")
            if screen is None:
                return None
            try:
                self._edit_in_tui(screen, session.model)
            except Exception as exc:
                self._tui_notice(screen, session.model, ["ERROR: {}".format(exc)])
            finally:
                session.model._show_front()
            return None

        session = MenuSession(
            app.app_name,
            app.version,
            on_version=lambda: "{} {}".format(app.app_name, app.version),
            on_about=app.about.framework_about,
            boards=self._boards(),
            on_kind=on_kind,
            logger=self.logger,
        )
        self._apply_language(session)

        def _wrapped(screen):
            screen_box["screen"] = screen
            session.run(screen)

        try:
            curses.wrapper(_wrapped)
        except MenuScreenError:
            app.output.out_err(
                "ERROR: The text screen is too small for the menu and the input box."
            )
            app.output.out_err("   Next: video-speed --help")
            return "missing"
        except Exception:
            app.output.out_err("ERROR: The text menu could not open on this terminal.")
            app.output.out_err("   Next: video-speed --help")
            return "missing"
        return None

    def _view_log(self, screen, model):
        """General Purpose: List log files and return the chosen file for the result page."""
        folder = self.system_log.log_dir()
        if not folder:
            return "No log folder."
        files = self.system_log.log_files()
        if not files:
            return "No log file in {0}.".format(folder)
        lines = ["Log files:"]
        for index, path in enumerate(files, start=1):
            lines.append("{0}. {1}".format(index, path.name))
        lines.append("")
        lines.append("Choose a log file:")
        picked = self._tui_index(screen, model, lines, len(files), title="system-log")
        if picked is None:
            return None
        path = files[picked]
        body = self.system_log.read_log(path)
        if body is None:
            return "ERROR: {0} is not a log file in the log folder.".format(path.name)
        if body == "":
            body = "(empty)"
        return "{0}\n\n{1}".format(path.name, body)

    def _clear_log(self, screen, model):
        """General Purpose: List log files, confirm, and empty the chosen file."""
        folder = self.system_log.log_dir()
        if not folder:
            return "No log folder."
        files = self.system_log.log_files()
        if not files:
            return "No log file in {0}.".format(folder)
        lines = ["Log files:"]
        for index, path in enumerate(files, start=1):
            lines.append("{0}. {1}".format(index, path.name))
        lines.append("")
        lines.append("Choose a log file to clear:")
        picked = self._tui_index(screen, model, lines, len(files), title="system-log")
        if picked is None:
            return None
        path = files[picked]
        answer = self._tui_yes_no(
            screen,
            model,
            ["Clear {0}? (y/n)".format(path.name)],
            title="system-log",
        )
        if answer is not True:
            return None
        if not self.system_log.clear_log(path):
            return "ERROR: {0} is not a log file in the log folder.".format(path.name)
        return "Cleared {0}.".format(path.name)

    def _log_folder(self):
        """General Purpose: The log-folder result page. The path is logDir()."""
        return self.system_log.folder_text()

    def _edit_in_tui(
        self,
        screen,
        model,
        folder=None,
        video=None,
        start_preset=None,
        end_preset=None,
        percent_preset=None,
        boomerang_preset=None,
    ):
        """Screen path of the edit questions. The order lives on EditWalk."""
        return self.app.edit.run_screen(
            self,
            screen,
            model,
            folder=folder,
            video=video,
            start_preset=start_preset,
            end_preset=end_preset,
            percent_preset=percent_preset,
            boomerang_preset=boomerang_preset,
        )

    def _list_in_tui(self, screen, model, folder=None):
        """
        General Purpose: Folder question, then the numbered MP4 list. No encode.
        Last updated: 2026-10-01
        Esc during the folder question returns 0. No MP4 returns 1.
        """
        from pathlib import Path

        folder_path = Path(folder) if folder else None
        while True:
            if folder_path is None:
                raw = self._tui_read(
                    screen,
                    model,
                    [
                        "List MP4 files",
                        "Esc returns to the menu.",
                        "",
                        "Folder (Enter = current):",
                    ],
                )
                if raw is None:
                    return 0
                folder = raw.strip() or "."
                folder_path = Path(folder)
            if not folder_path.is_dir():
                model.error = "ERROR: Not a directory: {}".format(folder_path)
                folder_path = None
                continue
            files = self.app.media.get_mp4_files(folder_path)
            if not files:
                self._tui_notice(screen, model, ["No MP4 files found!"])
                return 1
            listing = ["{:2d}. {}".format(i, item.name) for i, item in enumerate(files, 1)]
            self._tui_notice(screen, model, listing)
            return 0

    def _open_direct_screen(self, kind, args):
        """
        General Purpose: Open the text screen on one verb, not on the front board.
        Last updated: 2026-10-01
        A test driver exposes keys. A finished script must not spin on an empty
        key list. A real screen has no keys attribute, so the front board waits.
        """
        app = self.app
        if not app.stdout_is_tty():
            app.output.out_err(
                "ERROR: No terminal for the text menu. "
                "Next: pass --file, --start, and --end, or run in a terminal."
            )
            return 1
        try:
            import curses
        except ImportError:
            app.output.out_err("ERROR: The text menu could not be loaded.")
            app.output.out_err("   Next: video-speed --help")
            return 1

        code_box = {"code": 0}
        session = MenuSession(
            app.app_name,
            app.version,
            on_version=lambda: "{} {}".format(app.app_name, app.version),
            on_about=app.about.framework_about,
            boards=self._boards(),
            on_kind=lambda _kind: None,
            logger=self.logger,
        )
        self._apply_language(session)

        def _wrapped(screen):
            try:
                if kind == "edit":
                    self._edit_in_tui(
                        screen,
                        session.model,
                        folder=args.folder,
                        video=args.file,
                        start_preset=args.start,
                        end_preset=args.end,
                        percent_preset=args.percent,
                        boomerang_preset=True if args.boomerang else None,
                    )
                else:
                    code_box["code"] = self._list_in_tui(
                        screen, session.model, args.folder
                    )
            except Exception as exc:
                self._tui_notice(screen, session.model, ["ERROR: {}".format(exc)])
                code_box["code"] = 1
            finally:
                session.model._show_front()
            if getattr(screen, "keys", None) == []:
                self.painter.paint(screen, session.model, app.app_name, app.version)
                return
            session.run(screen)

        try:
            curses.wrapper(_wrapped)
        except MenuScreenError:
            app.output.out_err(
                "ERROR: The text screen is too small for the menu and the input box."
            )
            app.output.out_err("   Next: video-speed --help")
            return 1
        except Exception:
            app.output.out_err("ERROR: The text menu could not open on this terminal.")
            app.output.out_err("   Next: video-speed --help")
            return 1
        return code_box["code"]
