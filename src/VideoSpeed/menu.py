# =============================================================================
# Text menu screen writer for VideoSpeed.
# requirement-python-tui.md — menu region and the bottom input box.
# This module is the only painter.
# =============================================================================

from __future__ import annotations

import curses
from collections.abc import Callable

# =============================================================================
# CIAO-Lite Protection Zone
# Do NOT simplify, refactor, or remove without explicit user instruction.
# The frame glyphs are the bottom input box. requirement-python-tui.md
# =============================================================================
INPUT_MARK = "> "
INPUT_HINT = "Up/Down  •  Enter"
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
    (8, "about", "version, FFmpeg, and OpenCV", "about"),
    (9, "Exit", "leave", "exit"),
)
FRONT_ROWS = MENU_ROWS


def _edge_keys() -> tuple[int, int]:
    return (getattr(curses, "KEY_HOME", -2), getattr(curses, "KEY_END", -3))


def rows_for(layer: str) -> tuple:
    return FRONT_ROWS


def row_parts(rows: tuple) -> list[tuple[str, str, str, str]]:
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


def format_rows(rows: tuple) -> list[str]:
    """Aligned menu lines for one board. The painter and the tests share these."""
    return [
        f"{number_field}{short}{verb_pad}: {explain}"
        for number_field, short, verb_pad, explain in row_parts(rows)
    ]


class MenuScreenError(Exception):
    """The terminal cannot hold the menu and the framed input box."""


class MenuModel:
    """Keystroke state for the front board. The bottom frame is the input box.

    boards, when set, replaces the front rows for this session. Omit boards
    and the model keeps VideoSpeed's edit / about / Exit list.
    """

    def __init__(self, boards: dict | None = None) -> None:
        if boards is None:
            boards = {"front": FRONT_ROWS}
        self.boards = boards
        self.layer = "front"
        self.index = 0
        self.buffer = ""
        self.cursor = 0
        self.focus = "list"
        self.error = ""
        self.phase = "board"
        self.result_text = ""
        self.result_offset = 0

    def rows(self) -> tuple:
        found = self.boards.get(self.layer)
        if found is not None:
            return found
        return rows_for(self.layer)

    def show_result(self, text: str) -> None:
        self.result_text = text
        self.result_offset = 0
        self.phase = "result"
        self.layer = "front"
        self.index = 0
        self.buffer = ""
        self.cursor = 0
        self.focus = "list"
        self.error = ""

    def handle_key(self, key: int, screen_height: int = 24) -> str | None:
        """Return 'exit', a row kind, or None to stay."""
        if key == -1:
            if self.phase == "result":
                self._show_front()
                return None
            if self.layer != "front":
                self._show_front()
                return None
            return "exit"
        if self.phase == "result":
            lines = self.result_text.splitlines() or [""]
            if _result_overflow(screen_height, len(lines)) and key in (
                curses.KEY_UP,
                ord("k"),
            ):
                self._scroll_result(-1, screen_height)
                return None
            if _result_overflow(screen_height, len(lines)) and key in (
                curses.KEY_DOWN,
                ord("j"),
            ):
                self._scroll_result(1, screen_height)
                return None
            self._show_front()
            return None
        if key in (curses.KEY_UP, curses.KEY_DOWN) or (
            self.focus == "list" and key in (ord("k"), ord("j"))
        ):
            self._arrow(key)
            return None
        if key in (curses.KEY_LEFT, curses.KEY_RIGHT) or key in _edge_keys():
            self._slide(key)
            return None
        if key in (curses.KEY_BACKSPACE, 127, 8):
            self._backspace()
            return None
        if key in (10, 13, curses.KEY_ENTER):
            return self._commit()
        if 32 <= key < 127:
            self._insert(chr(key))
            return None
        self.error = "That choice is not on this list. Pick a listed number."
        return None

    def _show_front(self) -> None:
        self.phase = "board"
        self.layer = "front"
        self.index = 0
        self.buffer = ""
        self.cursor = 0
        self.focus = "list"
        self.error = ""
        self.result_offset = 0

    def _scroll_result(self, delta: int, screen_height: int) -> None:
        """Move the result window. Up/Down stay on the page when it overflows."""
        lines = self.result_text.splitlines() or [""]
        room = _result_room(screen_height, len(lines))
        max_offset = max(0, len(lines) - room)
        self.result_offset = min(max(0, self.result_offset + delta), max_offset)

    def _arrow(self, key: int) -> None:
        """Up/Down walks the rows, then the bottom box, then the rows again."""
        last = len(self.rows()) - 1
        down = key in (curses.KEY_DOWN, ord("j"))
        if self.focus == "input":
            self.focus = "list"
            self.index = 0 if down else last
            return
        if down:
            if self.index < last:
                self.index += 1
            else:
                self.focus = "input"
                self.cursor = len(self.buffer)
            return
        if self.index > 0:
            self.index -= 1
            return
        self.focus = "input"
        self.cursor = len(self.buffer)

    def _slide(self, key: int) -> None:
        if self.focus != "input":
            return
        home, end = _edge_keys()
        if key == curses.KEY_LEFT:
            self.cursor = max(0, self.cursor - 1)
        elif key == curses.KEY_RIGHT:
            self.cursor = min(len(self.buffer), self.cursor + 1)
        elif key == home:
            self.cursor = 0
        elif key == end:
            self.cursor = len(self.buffer)

    def _insert(self, ch: str) -> None:
        if self.focus != "input":
            self.focus = "input"
            self.cursor = len(self.buffer)
        self.cursor = min(max(self.cursor, 0), len(self.buffer))
        self.buffer = self.buffer[: self.cursor] + ch + self.buffer[self.cursor :]
        self.cursor += 1

    def _backspace(self) -> None:
        if self.focus != "input":
            self.focus = "input"
            self.cursor = len(self.buffer)
        if self.cursor <= 0 or not self.buffer:
            self.cursor = 0
            return
        self.cursor = min(self.cursor, len(self.buffer))
        self.buffer = self.buffer[: self.cursor - 1] + self.buffer[self.cursor :]
        self.cursor -= 1

    def _reject(self) -> None:
        self.error = "That choice is not on this list. Pick a listed number."
        self.focus = "input"
        self.cursor = len(self.buffer)

    def _commit(self) -> str | None:
        token = self.buffer.strip()
        self.buffer = ""
        self.cursor = 0
        if token == "":
            number, _short, _explain, kind = self.rows()[self.index]
            return self._activate(number, kind)
        if token.isdigit():
            return self._activate_number(int(token))
        for number, short, _explain, kind in self.rows():
            if token == short:
                return self._activate(number, kind)
        self._reject()
        return None

    def _activate_number(self, number: int) -> str | None:
        for row_number, _short, _explain, kind in self.rows():
            if row_number == number:
                return self._activate(number, kind)
        self._reject()
        return None

    def _activate(self, number: int, kind: str) -> str | None:
        self.error = ""
        self.focus = "list"
        self.cursor = 0
        if kind == "exit":
            return "exit"
        if kind == "back":
            self.layer = "front"
            self.index = 0
            return None
        if kind in ("version", "about"):
            return kind
        return kind


def _put(screen, y: int, x: int, text: str, attr: int = 0) -> None:
    height, width = screen.getmaxyx()
    if y < 0 or y >= height or x >= width - 1:
        return
    clipped = text[: max(0, width - x - 1)]
    if clipped:
        screen.addstr(y, x, clipped, attr)


def _result_overflow(height: int, line_count: int) -> bool:
    """True when the result text needs another row past the title and the hint."""
    return line_count > max(1, height - 3)


def _result_room(height: int, line_count: int) -> int:
    """Body rows under the title. One row is kept for the scroll hint when needed."""
    if _result_overflow(height, line_count):
        return max(1, height - 4)
    return max(1, height - 3)


def screen_can_hold_box(height: int, width: int) -> bool:
    """True when the title, one menu row, the three-row frame, and the status line fit."""
    return height >= MIN_HEIGHT and width - 1 >= MIN_PLACEABLE


def _input_field(model: MenuModel, inner: int) -> tuple[str, int | None]:
    """Cells between the side bars, and the caret index in those cells when focused."""
    prefix = " " + INPUT_MARK
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
        body = shown[:rel] + CARET_BLOCK + shown[rel:]
        caret_at = len(prefix) + rel
    else:
        body = shown
        caret_at = None
    field = (prefix + body).ljust(inner)[:inner]
    if caret_at is not None and caret_at >= inner:
        caret_at = None
    return field, caret_at


def _status_line(app_name: str, version: str, title: str) -> str:
    """The row under the frame: name, version, board, and the key hint."""
    return f"  {app_name} {version}  {FRAME_VERT}  {title}  {FRAME_VERT}  {INPUT_HINT}"


def _paint_box(screen, model: MenuModel, top: int, app_name: str, version: str, title: str) -> None:
    """Draw the rounded frame and the status line under it."""
    _height, width = screen.getmaxyx()
    placeable = width - 1
    if top < 0 or placeable < 2:
        return
    inner = placeable - 2
    field, caret_at = _input_field(model, inner)
    side = FRAME_VERT
    lines = (
        FRAME_TOP_LEFT + (FRAME_HORIZ * inner) + FRAME_TOP_RIGHT,
        side + field + side,
        FRAME_BOTTOM_LEFT + (FRAME_HORIZ * inner) + FRAME_BOTTOM_RIGHT,
    )
    for offset, line in enumerate(lines):
        _put(screen, top + offset, 0, line)
    _put(screen, top + FRAME_ROWS, 0, _status_line(app_name, version, title))
    if caret_at is None or not hasattr(screen, "move"):
        return
    try:
        screen.move(top + 1, 1 + caret_at)
    except curses.error:
        pass


def paint(screen, model: MenuModel, app_name: str, version: str) -> None:
    """Draw one frame. This is the text-menu writer, not product logging."""
    screen.erase()
    italic = curses.A_ITALIC if hasattr(curses, "A_ITALIC") else curses.A_DIM
    title = "result" if model.phase == "result" else "main menu"
    _put(screen, 0, 0, app_name, curses.A_BOLD)
    cursor = len(app_name)
    _put(screen, 0, cursor, " (")
    cursor += 2
    _put(screen, 0, cursor, version, italic)
    cursor += len(version)
    _put(screen, 0, cursor, f") — {title}")
    if model.phase == "result":
        lines = model.result_text.splitlines() or [""]
        height, _width = screen.getmaxyx()
        room = _result_room(height, len(lines))
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
            _put(screen, y, 0, line)
            y += 1
        if _result_overflow(height, len(lines)):
            _put(screen, height - 2, 0, "Up/Down scrolls this page.", italic)
            _put(screen, height - 1, 0, "Press a key to return to the main menu.", italic)
        else:
            hint_y = y + 1
            if hint_y >= height:
                hint_y = height - 1
            _put(screen, hint_y, 0, "Press a key to return to the main menu.", italic)
        screen.refresh()
        return
    height, _width = screen.getmaxyx()
    box_top = height - CHROME_ROWS
    stop = box_top
    if model.error and box_top >= 4:
        stop = box_top - 1
    y = 2
    if y < stop:
        for idx, (number_field, short, verb_pad, explain) in enumerate(row_parts(model.rows())):
            if y >= stop:
                break
            selected = idx == model.index
            if selected and model.focus == "list":
                attr = curses.A_REVERSE
            elif selected:
                attr = curses.A_UNDERLINE
            else:
                attr = 0
            _put(screen, y, 0, number_field, attr)
            verb_x = len(number_field)
            _put(screen, y, verb_x, short, curses.A_BOLD | attr)
            colon_x = verb_x + len(short)
            _put(screen, y, colon_x, f"{verb_pad}: ", attr)
            _put(screen, y, colon_x + len(verb_pad) + 2, explain, italic)
            y += 1
    if model.error and box_top >= 4:
        _put(screen, box_top - 1, 0, model.error, curses.A_BOLD)
    _paint_box(screen, model, box_top, app_name, version, title)
    if hasattr(screen, "curs_set"):
        try:
            screen.curs_set(0)
        except curses.error:
            pass
    screen.refresh()


class MenuSession:
    """Run the text menu until Exit. Leaf commands return to the front board.

    on_kind returns "leave" to close the screen, a string to show a result page,
    or None to stay.
    """

    def __init__(
        self,
        app_name: str,
        version: str,
        on_version: Callable[[], str],
        on_about: Callable[[], str],
        boards: dict | None = None,
        on_kind: Callable[[str], str | None] | None = None,
    ) -> None:
        self.app_name = app_name
        self.version = version
        self.on_version = on_version
        self.on_about = on_about
        self.on_kind = on_kind
        self.leave_kind = None
        self.model = MenuModel(boards=boards)

    def run(self, screen) -> int:
        screen.keypad(True)
        height, width = screen.getmaxyx()
        if not screen_can_hold_box(height, width):
            raise MenuScreenError(
                "The text screen is too small for the menu and the input box."
            )
        while True:
            paint(screen, self.model, self.app_name, self.version)
            _height, _width = screen.getmaxyx()
            action = self.model.handle_key(screen.getch(), _height)
            if action == "exit":
                return 0
            if action == "version":
                self.model.show_result(self.on_version())
            elif action == "about":
                self.model.show_result(self.on_about())
            elif action:
                outcome = self.on_kind(action) if self.on_kind is not None else None
                if outcome == "leave":
                    self.leave_kind = action
                    return 0
                if isinstance(outcome, str) and outcome:
                    self.model.show_result(outcome)
