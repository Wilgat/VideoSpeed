# =============================================================================
# Text-menu frame.
# requirement-python-tui — menu region and the bottom input box.
# requirement-python-oop — class MenuPainter owns the frame and MENU_ROWS.
# =============================================================================
from __future__ import annotations

import curses
import os
import time




class MenuPainter:
    """Draws the front board and the rounded input box. One class, one module."""

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="MenuPainter")

    # =============================================================================
    # CIAO-Lite Protection Zone
    # Do NOT simplify, refactor, or remove without explicit user instruction.
    # The frame glyphs are the bottom input box. requirement-python-tui.md
    # =============================================================================
    INPUT_MARK = "> "
    INPUT_HINT = "Up/Down  •  Enter"
    # The path word is requirement-python-cli-language. This painter does not
    # detect a language. The caller sets the word. English is the default.
    PATH_LABEL_EN = "Path"
    FRAME_TOP_LEFT = "╭"
    FRAME_TOP_RIGHT = "╮"
    FRAME_BOTTOM_LEFT = "╰"
    FRAME_BOTTOM_RIGHT = "╯"
    FRAME_HORIZ = "─"
    FRAME_VERT = "│"
    CARET_BLOCK = "█"
    FRAME_ROWS = 3
    FOOTER_ROWS = 1
    CHROME_ROWS = FRAME_ROWS + FOOTER_ROWS
    MIN_MENU_ABOVE = 3
    MIN_HEIGHT = MIN_MENU_ABOVE + CHROME_ROWS
    MIN_PLACEABLE = 2 + len(" " + INPUT_MARK) + 1
    MENU_ROWS = (
        (1, "edit", "cut, speed, and optional boomerang", "edit"),
        (4, "language", "display language for this menu", "language"),
        (6, "system-log", "view, clear, and the log folder", "system-log"),
        (8, "self-management", "version, about, and pip lifecycle", "self-management"),
        (9, "Exit", "leave", "exit"),
    )
    SELF_ROWS = (
        (82, "version", "show the installed version", "version"),
        (83, "about", "version, FFmpeg, and OpenCV", "about"),
        (84, "version-check", "compare this install with pip", "version-check"),
        (85, "self-update", "upgrade this package with pip", "self-update"),
        (86, "self-uninstall", "remove this package with pip", "self-uninstall"),
        (87, "self-install", "install this package with pip", "self-install"),
        (0, "Back", "return to the main menu", "back"),
    )
    LOG_ROWS = (
        (61, "view-log", "list a log file and show it", "view-log"),
        (62, "clear-log", "empty one log file", "clear-log"),
        (63, "log-folder", "show the log folder", "log-folder"),
        (0, "Back", "return to the main menu", "back"),
    )
    LANG_ROWS = (
        (41, "English", "use English for this menu", "en"),
        (42, "简体中文", "use Simplified Chinese for this menu", "zh-Hans"),
        (43, "繁體中文", "use Traditional Chinese for this menu", "zh-Hant"),
        (44, "Español", "use Spanish for this menu", "es"),
        (45, "العربية", "use Arabic for this menu", "ar"),
        (46, "Français", "use French for this menu", "fr"),
        (47, "Português", "use Portuguese for this menu", "pt"),
        (48, "Русский", "use Russian for this menu", "ru"),
        (49, "Deutsch", "use German for this menu", "de"),
        (50, "日本語", "use Japanese for this menu", "ja"),
        (51, "한국어", "use Korean for this menu", "ko"),
        (52, "Nederlands", "use Dutch for this menu", "nl"),
        (53, "Ελληνικά", "use Greek for this menu", "el"),
        (0, "Back", "return to the main menu", "back"),
    )
    ANY_BOARD = {
        "help": "help",
        "version": "version",
        "about": "about",
        "edit": "edit",
        "list-mp4": "list-mp4",
        "self-install": "self-install",
        "version-check": "version-check",
        "self-update": "self-update",
        "self-uninstall": "self-uninstall",
        "self-management": "self-management",
        "system-log": "system-log",
        "language": "language",
        "view-log": "view-log",
        "clear-log": "clear-log",
        "log-folder": "log-folder",
    }

    def rows_for(self, layer: str) -> tuple:
        if layer == "self":
            return self.SELF_ROWS
        if layer == "log":
            return self.LOG_ROWS
        if layer == "lang":
            return self.LANG_ROWS
        return self.MENU_ROWS

    def set_path_label(self, label: str) -> None:
        """Store the path word the caller already chose. This method does not detect a language."""
        self._path_label = label

    def path_label(self) -> str:
        """The path-line word. English until the caller sets another."""
        return getattr(self, "_path_label", None) or self.PATH_LABEL_EN

    def clock_text(self) -> str:
        """Local clock HH:MM:SS. requirement-python-tui rule 13. Not translated."""
        return time.strftime("%H:%M:%S", time.localtime())

    def path_line(self, placeable: int | None = None) -> str:
        """First menu row: path on the left, local clock on the right when it fits.

        A placeable width keeps the path label and shortens the directory from the left.
        The clock is omitted when both fields do not fit. requirement-python-tui rule 13.
        The path and the clock are not translated.
        """
        prefix = self.path_label() + ": "
        current = os.path.abspath(os.getcwd())
        left = prefix + current
        right = self.clock_text()
        gap = 2
        if placeable is None:
            return left + (" " * gap) + right
        if placeable >= len(left) + gap + len(right):
            return left + (" " * (placeable - len(left) - len(right))) + right
        if placeable >= len(left):
            return left
        if placeable <= len(prefix):
            return prefix[: max(0, placeable)]
        return prefix + current[-(placeable - len(prefix)) :]

    def board_title(self, model) -> str:
        """General Purpose: The title for this layer. A result page names itself."""
        titles = getattr(model, "titles", None) or {}
        if getattr(model, "phase", "board") == "result":
            return titles.get("result", "result")
        layer = getattr(model, "layer", "front")
        if layer in titles:
            return titles[layer]
        if layer == "self":
            return "self-management"
        if layer == "log":
            return "system-log"
        if layer == "lang":
            return "language"
        return "main menu"

    def row_parts(self, rows: tuple) -> list[tuple[str, str, str, str]]:
        """One board's columns. requirement-python-tui.md

        Each row is number, verb, and explain. The number is padded on the left to
        the widest number on this board. The verb is padded with spaces immediately
        before the colon. The explain is drawn after one space.
        """
        number_width = 1
        verb_width = 0
        materialized: list[tuple[str, str, str]] = []
        for number, short, explain, _kind in rows:
            text = str(number)
            materialized.append((text, short, explain))
            if len(text) > number_width:
                number_width = len(text)
            if len(short) > verb_width:
                verb_width = len(short)
        parts: list[tuple[str, str, str, str]] = []
        for text, short, explain in materialized:
            number_field = f"{text.rjust(number_width)}. "
            verb_pad = " " * (verb_width - len(short))
            parts.append((number_field, short, verb_pad, explain))
        return parts

    def format_rows(self, rows: tuple) -> list[str]:
        """Aligned menu lines for one board. The painter and the tests share these."""
        return [
            f"{number_field}{short}{verb_pad}: {explain}"
            for number_field, short, verb_pad, explain in self.row_parts(rows)
        ]

    def _put(self, screen, y: int, x: int, text: str, attr: int = 0) -> None:
        height, width = screen.getmaxyx()
        if y < 0 or y >= height or x >= width - 1:
            return
        clipped = text[: max(0, width - x - 1)]
        if clipped:
            screen.addstr(y, x, clipped, attr)

    def _result_overflow(self, height: int, line_count: int) -> bool:
        """True when the result text needs another row past the title and the hint."""
        return line_count > max(1, height - 3)

    def _result_room(self, height: int, line_count: int) -> int:
        """Body rows under the title. One row is kept for the scroll hint when needed."""
        if self._result_overflow(height, line_count):
            return max(1, height - 4)
        return max(1, height - 3)

    def screen_can_hold_box(self, height: int, width: int) -> bool:
        """True when the path line, one menu row, the three-row frame, and the status line fit."""
        return height >= self.MIN_HEIGHT and width - 1 >= self.MIN_PLACEABLE

    def _input_field(self, model, inner: int) -> tuple[str, int | None]:
        """Cells between the side bars, and the caret index in those cells when focused."""
        prefix = " " + self.INPUT_MARK
        focused = model.focus == "input"
        cursor = min(max(model.cursor, 0), len(model.buffer))
        reserve = len(prefix) + (1 if focused else 0)
        text_room = max(0, inner - reserve)
        start = 0
        if text_room and cursor > text_room:
            start = cursor - text_room
        if text_room and start > max(0, len(model.buffer) - text_room):
            start = max(0, len(model.buffer) - text_room)
        shown = model.buffer[start : start + text_room] if text_room else ""
        rel = max(0, min(len(shown), cursor - start))
        if focused and inner >= reserve:
            body = shown[:rel] + self.CARET_BLOCK + shown[rel:]
            caret_at = len(prefix) + rel
        else:
            body = shown
            caret_at = None
        field = (prefix + body).ljust(inner)[:inner]
        if caret_at is not None and caret_at >= inner:
            caret_at = None
        return field, caret_at

    def _status_line(self, app_name: str, version: str, title: str) -> str:
        """The row under the frame: name, version, board, and the key hint."""
        return (
            f"  {app_name} {version}  {self.FRAME_VERT}  {title}  "
            f"{self.FRAME_VERT}  {self.INPUT_HINT}"
        )

    def _paint_box(self, screen, model, top: int, app_name: str, version: str, title: str) -> None:
        """Draw the rounded frame and the status line under it."""
        _height, width = screen.getmaxyx()
        placeable = width - 1
        if top < 0 or placeable < 2:
            return
        inner = placeable - 2
        field, caret_at = self._input_field(model, inner)
        side = self.FRAME_VERT
        lines = (
            self.FRAME_TOP_LEFT + (self.FRAME_HORIZ * inner) + self.FRAME_TOP_RIGHT,
            side + field + side,
            self.FRAME_BOTTOM_LEFT + (self.FRAME_HORIZ * inner) + self.FRAME_BOTTOM_RIGHT,
        )
        for offset, line in enumerate(lines):
            self._put(screen, top + offset, 0, line)
        self._put(screen, top + self.FRAME_ROWS, 0, self._status_line(app_name, version, title))
        if caret_at is None or not hasattr(screen, "move"):
            return
        try:
            screen.move(top + 1, 1 + caret_at)
        except curses.error:
            pass

    def paint(self, screen, model, app_name: str, version: str) -> None:
        """Draw one frame. This is the text-menu writer, not product logging."""
        screen.erase()
        italic = curses.A_ITALIC if hasattr(curses, "A_ITALIC") else curses.A_DIM
        title = self.board_title(model)
        if model.phase == "result":
            self._put(screen, 0, 0, app_name, curses.A_BOLD)
            cursor = len(app_name)
            self._put(screen, 0, cursor, " (")
            cursor += 2
            self._put(screen, 0, cursor, version, italic)
            cursor += len(version)
            self._put(screen, 0, cursor, f") — {title}")
        else:
            _height, width = screen.getmaxyx()
            self._put(screen, 0, 0, self.path_line(max(0, width - 1)))
        if model.phase == "result":
            lines = model.result_text.splitlines() or [""]
            height, _width = screen.getmaxyx()
            room = self._result_room(height, len(lines))
            max_offset = max(0, len(lines) - room)
            if model.result_offset > max_offset:
                model.result_offset = max_offset
            if model.result_offset < 0:
                model.result_offset = 0
            window = lines[model.result_offset : model.result_offset + room]
            y = 2
            for line in window:
                if y >= height - 1:
                    break
                self._put(screen, y, 0, line)
                y += 1
            if self._result_overflow(height, len(lines)):
                self._put(screen, height - 2, 0, "Up/Down scrolls this page.", italic)
                self._put(
                    screen, height - 1, 0,
                    "Press a key to return to the main menu.", italic,
                )
            else:
                hint_y = y + 1
                if hint_y >= height:
                    hint_y = height - 1
                self._put(screen, hint_y, 0, "Press a key to return to the main menu.", italic)
            screen.refresh()
            return
        height, _width = screen.getmaxyx()
        box_top = height - self.CHROME_ROWS
        stop = box_top
        if model.error and box_top >= 4:
            stop = box_top - 1
        y = 2
        if y < stop:
            for idx, (number_field, short, verb_pad, explain) in enumerate(
                self.row_parts(model.rows())
            ):
                if y >= stop:
                    break
                selected = idx == model.index
                if selected and model.focus == "list":
                    attr = curses.A_REVERSE
                elif selected:
                    attr = curses.A_UNDERLINE
                else:
                    attr = 0
                self._put(screen, y, 0, number_field, attr)
                verb_x = len(number_field)
                self._put(screen, y, verb_x, short, curses.A_BOLD | attr)
                colon_x = verb_x + len(short)
                self._put(screen, y, colon_x, f"{verb_pad}: ", attr)
                self._put(screen, y, colon_x + len(verb_pad) + 2, explain, italic)
                y += 1
        if model.error and box_top >= 4:
            self._put(screen, box_top - 1, 0, model.error, curses.A_BOLD)
        self._paint_box(screen, model, box_top, app_name, version, title)
        if hasattr(screen, "curs_set"):
            try:
                screen.curs_set(0)
            except curses.error:
                pass
        screen.refresh()

    def paint_prompt(
        self, screen, model, title, lines, pin_last, app_name, version, visible_lines,
    ) -> None:
        """Draw one domain question. The rounded box is the only frame."""
        screen.erase()
        italic = curses.A_ITALIC if hasattr(curses, "A_ITALIC") else curses.A_DIM
        self._put(screen, 0, 0, app_name, curses.A_BOLD)
        cursor = len(app_name)
        self._put(screen, 0, cursor, " (")
        cursor += 2
        self._put(screen, 0, cursor, version, italic)
        cursor += len(version)
        self._put(screen, 0, cursor, ") — {}".format(title))
        height, _width = screen.getmaxyx()
        box_top = height - self.CHROME_ROWS
        stop = box_top
        if model.error and box_top >= 4:
            stop = box_top - 1
        shown = visible_lines(lines, stop - 2, pin_last)
        y = 2
        for line in shown:
            if y >= stop:
                break
            self._put(screen, y, 0, line)
            y += 1
        if model.error and box_top >= 4:
            self._put(screen, box_top - 1, 0, model.error, curses.A_BOLD)
        self._paint_box(screen, model, box_top, app_name, version, title)
        if hasattr(screen, "curs_set"):
            try:
                screen.curs_set(0)
            except curses.error:
                pass
        screen.refresh()
