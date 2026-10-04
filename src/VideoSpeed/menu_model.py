# =============================================================================
# Keystroke state for the text menu.
# requirement-python-oop — class MenuModel.
# =============================================================================
from __future__ import annotations

import curses

from .menu_painter import MenuPainter



class MenuModel:
    """Keystroke state for the front board. The bottom frame is the input box.

    boards, when set, replaces the front rows for this session. Omit boards
    and the model keeps VideoSpeed's edit / language / system-log /
    self-management / Exit list, the language board under 4, the
    self-management board under 8, and the system-log board under 6.
    """

    def __init__(self, boards: dict | None = None, logger=None) -> None:
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="MenuModel")
        self.painter = MenuPainter(logger=logger)
        if boards is None:
            boards = {
                "front": MenuPainter.MENU_ROWS,
                "self": MenuPainter.SELF_ROWS,
                "log": MenuPainter.LOG_ROWS,
                "lang": MenuPainter.LANG_ROWS,
            }
        self.boards = boards
        self.titles = {}
        self.tokens = {}
        self.unknown_choice = "That choice is not on this list. Pick a listed number."
        self.layer = "front"
        self.index = 0
        self.buffer = ""
        self.cursor = 0
        self.focus = "list"
        self.error = ""
        self.phase = "board"
        self.result_text = ""
        self.result_offset = 0

    def edge_keys(self) -> tuple[int, int]:
        return (getattr(curses, "KEY_HOME", -2), getattr(curses, "KEY_END", -3))

    def rows(self) -> tuple:
        found = self.boards.get(self.layer)
        if found is not None:
            return found
        return self.painter.rows_for(self.layer)

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
            if self.painter._result_overflow(screen_height, len(lines)) and key in (
                curses.KEY_UP,
                ord("k"),
            ):
                self._scroll_result(-1, screen_height)
                return None
            if self.painter._result_overflow(screen_height, len(lines)) and key in (
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
        if key in (curses.KEY_LEFT, curses.KEY_RIGHT) or key in self.edge_keys():
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
        self.error = self.unknown_choice
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
        room = self.painter._result_room(screen_height, len(lines))
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
        home, end = self.edge_keys()
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
        self.error = self.unknown_choice
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
        hit = self.tokens.get(token)
        if hit is not None:
            kind, only_layer = hit
            if only_layer is None or only_layer == self.layer:
                return self._activate(0, kind)
        kind = MenuPainter.ANY_BOARD.get(token)
        if kind is not None:
            return self._activate(0, kind)
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
        if kind == "self-management":
            self.layer = "self"
            self.index = 0
            self.focus = "list"
            self.buffer = ""
            self.cursor = 0
            return None
        if kind == "system-log":
            self.layer = "log"
            self.index = 0
            self.focus = "list"
            self.buffer = ""
            self.cursor = 0
            return None
        if kind == "language":
            self.layer = "lang"
            self.index = 0
            self.focus = "list"
            self.buffer = ""
            self.cursor = 0
            return None
        if kind in ("version", "about"):
            return kind
        return kind
