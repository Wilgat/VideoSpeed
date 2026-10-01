# =============================================================================
# Run the text menu until Exit.
# requirement-python-oop — class MenuSession. MenuScreenError shares this file.
# =============================================================================
from __future__ import annotations

from collections.abc import Callable

from .menu_model import MenuModel
from .menu_painter import MenuPainter


class MenuScreenError(Exception):
    """The terminal cannot hold the menu and the framed input box."""


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
        self.painter = MenuPainter()
        self.model = MenuModel(boards=boards)

    def run(self, screen) -> int:
        screen.keypad(True)
        height, width = screen.getmaxyx()
        if not self.painter.screen_can_hold_box(height, width):
            raise MenuScreenError(
                "The text screen is too small for the menu and the input box."
            )
        while True:
            self.painter.paint(screen, self.model, self.app_name, self.version)
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
