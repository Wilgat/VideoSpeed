**file**: docs/requirements/requirement-python-tui.md
**Status**: Active (Version 1.1.9)
**Area**: python
**Key**: `requirement-python-tui`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the picture of VideoSpeed’s text menu. The screen has two parts on one board: the menu, and a bottom input box. That picture is the **default TUI style**. The session is class `Tui` in `src/VideoSpeed/tui.py`. The frame is class `MenuPainter` in `src/VideoSpeed/menu_painter.py`. Those homes are `requirement-python-oop`. `def main` stays in `src/VideoSpeed/cli.py`. Class `Cli` constructs `Tui` and passes this product’s name, version, and front board into that session. `cli.py` does not keep a second frame painter, and it does not import another menu package. `TP-OOP-03` has landed.

Which path runs stays on `requirement-python-interactive-vs-noninteractive`. The flag names also stay on `requirement-python-cli-interface`. Cut, speed, and boomerang stay on `requirement-domain-videospeed.md`. This file does not add a batch flag.

### 1.1 Human-facing

**In one sentence:** On a terminal, `video-speed` with no arguments shows a numbered menu and, along the bottom, a rounded box as wide as the screen, and you type on the only line inside that box.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The person at the keyboard | `video-speed` |
| The other role | The session and the painter | class `Tui` in `tui.py`; class `MenuPainter` in `menu_painter.py` |
| Not this file | The cut, the percent, and the FFmpeg steps | Domain and pipeline files |

| Includes | Excludes |
|----------|----------|
| The menu region above the box, and the rounded three-row frame | A `Choice:` line, `print` / `read`, or `input()` for that menu |
| UTF-8 arc corners and bars, full screen width, typing on the only inner line | Frame glyphs copied into `cli.py`, and a menu pip wheel |
| The status line under the frame, and this product’s front rows (edit, hello, about, Exit) | Putting the numbered rows inside the frame |

| Surface | What you open | What for |
|---------|---------------|----------|
| `video-speed` on a terminal | Text screen | Menu above, input box on the bottom, status line on the last row |
| `src/VideoSpeed/cli.py` | `def main` and class `Cli` | Builds the session; does not paint the frame |
| `src/VideoSpeed/tui.py` | class `Tui` | Session loop |
| `src/VideoSpeed/menu_painter.py` | class `MenuPainter` | Frame and columns (`requirement-python-oop`). `TP-OOP-03` has landed |
| `video-speed` in a script | Error text | No screen and no wait |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Start on a terminal with no words | You see edit, hello, about, and Exit. The bottom of the screen is one rounded box from the left edge to the right edge, then a status line. The block caret sits on the only line inside the box when that box is focused. | `video-speed` |
| Choose edit | The screen stays up. The menu region asks for the folder (Enter means the current directory), then the video, the cut, the percent, and boomerang. Each answer is typed in the same bottom box. Esc returns to the menu. | `1` then Enter, or type `edit` |
| Choose hello | The screen shows the hello message. The next key returns to the menu. | `7` then Enter, or type `hello` |
| Start in a script | An error on stderr and a next step. The program does not draw the box and does not wait. | `video-speed` with no terminal |

## 2. Core Rules (Mandatory)

1. **Package writer.** The text-menu session **MUST** be class `Tui` in `src/VideoSpeed/tui.py`. The frame **MUST** be drawn by class `MenuPainter` in `src/VideoSpeed/menu_painter.py` (`requirement-python-oop`). VideoSpeed **MUST** pass its product name, package version, and front board into that session. `cli.py` **MUST NOT** contain the frame glyphs (`FRAME_TOP_LEFT` belongs to `MenuPainter`). The product **MUST NOT** import `py_tui` and **MUST NOT** declare `py-tui`. The menu **MUST NOT** be drawn with `print` / `read` / `input()` or a `Choice:` line. After **edit** is chosen, the domain questions stay on this same screen: the question text is in the menu region, and the answer is typed in the same bottom box. Those questions **MUST NOT** close the screen or use `input()`. `TP-OOP-03` has landed.
2. **Two regions.** On the front board the writer **MUST** draw a menu region and a bottom input box on the same screen. The menu region is every row above the box. It **MUST** show the board title and the numbered rows for that board. Those rows **MUST NOT** be drawn inside the box. Each numbered row is a number, a verb, and an explain. On that board the number field is as wide as the longest number, and a shorter number is padded with spaces on the left (`11` beside ` 0` when the longest number has two digits; `232` beside `  0` when it has three). The verb field is as wide as the longest verb on that same board, and a shorter verb is padded with spaces immediately before the colon (`version:` beside `about  :`). The explain **MUST** be drawn after exactly one space. This board uses its own widths. VideoSpeed’s front board is the one in Implementation Notes: **1** edit, **7** hello, **8** about, **9** Exit. It **MUST NOT** open a self-management board.
3. **Three-row frame plus status line.** The bottom input box **MUST** be exactly three terminal rows high: a top border, one inner row, and a bottom border. The status line **MUST** be the next row, and that row **MUST** be the last row of the screen. The frame **MUST** span the full width of the screen. The left border is the first column. The right border is the last column the screen writer can place. There **MUST** be no blank column before the left border or after the right border.
4. **UTF-8 frame.** Those three rows **MUST** be drawn with these UTF-8 box-drawing characters. Each one occupies one column. ASCII `+`, `-`, and `|` **MUST NOT** stand in for them. Sharp corners `┌` `┐` `└` `┘` **MUST NOT** stand in for the arcs.

| Row of the box | Characters, left to right |
|----------------|---------------------------|
| Top | `╭` (U+256D), then `─` (U+2500) repeated, then `╮` (U+256E) |
| Inner | `│` (U+2502), then the input field, then `│` (U+2502) |
| Bottom | `╰` (U+2570), then `─` (U+2500) repeated, then `╯` (U+256F) |

5. **Input inside the frame.** One space, the mark `> `, the typed characters, and the caret **MUST** sit on the only inner line, strictly between the two `│` characters. The mark, the typed characters, and the caret **MUST NOT** sit on the top border, the bottom border, or a menu row. When the box is focused, the caret **MUST** be the block `█` (U+2588) at the caret index on that inner line. When the list is focused, that block **MUST NOT** be drawn. Up and Down **MUST** walk the numbered rows and the box: Down on the last row enters the box, Up on the first row enters the box, Up from the box returns to the last row, and Down from the box returns to the first row. Enter **MUST** run the typed token, or the highlighted row when the box is empty. The box **MUST NOT** be a `Choice:` line.
6. **This board’s actions.** **edit** **MUST** stay on this screen and ask the domain questions in the same bottom input box: source folder (empty means the current directory), video index, cut bounds, length percent, boomerang, and again. Esc **MUST** return to the front board. The screen **MUST NOT** close into a plain `input()` prompt for those questions. **hello** **MUST** show the result page. The page body **MUST** be the message `Hello.`. Typing `7` or `hello` **MUST** open that page. It **MUST NOT** leave the program. **about** **MUST** show the result page. The page body is `requirement-python-about` (product name, version, domain summary, host check, and install box). That page **MUST NOT** name `py-tui`. **Exit** **MUST** leave the program. An unknown token **MUST** stay on this board and show an error line in the menu region above the box. It **MUST NOT** exit the process. A positional product verb (`requirement-python-cli-interface` §2.3a) **MUST** enter that action without a front-board pick. `edit` **MUST** start at the folder question, then the specific file. `about` and `hello` **MUST** open their result pages and **MUST NOT** ask for a folder or a file. `list-mp4` **MUST** ask for the folder when it is missing, then show the numbered MP4 list on this screen, and **MUST NOT** encode and **MUST NOT** ask for a specific file. `help` **MUST NOT** draw this screen. Empty argv with no verb **MUST** still show the front board.
7. **Status line and errors.** The status line under the frame **MUST** show the product name, the version, the board title, and the key hint `Up/Down  •  Enter`, separated by `│`. It **MUST NOT** replace one of the three frame rows. An error line, when shown, **MUST** sit in the menu region above the box.
8. **Result page.** After hello or about, the result page may omit the menu rows, the box, and the status line until the next key returns to the front board.
9. **Too small or no terminal.** If stdout is not a terminal, or the screen cannot hold the title, at least one numbered menu row, the three-row box, and the status line, or cannot hold both corners plus the mark and one cell between them, the program **MUST NOT** collapse the box into one unframed row and **MUST NOT** fall back to a `Choice:` line. It **MUST** fail closed: non-zero, an operator-readable line, and a next step (`--help`, or `--file` / `--start` / `--end`).
10. **One writer.** Command text for batch jobs stays on this product’s console lines. The screen writer **MUST NOT** become a second logger for those jobs. A batch job **MUST NOT** open this screen. While **edit** is on this screen, its questions and job lines **MUST** be drawn by class `Tui` calling class `MenuPainter` (`requirement-python-oop`). They **MUST NOT** be `print` / `input()` lines that close the screen.
11. Actor / role / subject / approver: **considered**. No dest machine. No approver. The table stays on `requirement-class-software-dev.md`. This file does **not** add an actor requirement.
12. Dest fence conditions: **considered — none**. Do not invent one.

Picture of this board. The box in the picture is 16 columns wide so the corners stay visible. On a real screen those 16 columns become the full width, and the menu stays above the frame. The block in the picture is the focused caret:

```text
VideoSpeed (1.0.7) — main menu

1. edit : cut, speed, and optional boomerang
7. hello: show a hello message
8. about: version, FFmpeg, and OpenCV
9. Exit : leave
╭──────────────╮
│ > █          │
╰──────────────╯
  VideoSpeed 1.0.7  │  main menu  │  Up/Down  •  Enter
```

The column rule on a wider number field (same writer, not this product’s board):

```text
11. version: show the installed version
 0. about  : show the cache folders
```

### 2.1 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| **Command** | `video-speed` |
| **Open the screen** | `video-speed` or `python -m VideoSpeed` on a terminal, with no verb and no job flags |
| **Direct verb** | `edit` starts at the folder question, then the specific file. `list-mp4` asks for the folder, then lists. `about` and `hello` open their result pages. `help` does not draw this screen |
| **Session** | Class `Tui` in `src/VideoSpeed/tui.py` |
| **Painter** | Class `MenuPainter` in `src/VideoSpeed/menu_painter.py` (`paint`, `format_rows`, frame glyphs). `TP-OOP-03` has landed |
| **Caller** | Class `Cli` in `src/VideoSpeed/cli.py`. `def main` stays in that file |
| **Front rows** | **1** `edit` — cut, speed, and optional boomerang; **7** `hello` — show a hello message; **8** `about` — version, FFmpeg, and OpenCV; **9** `Exit` — leave |
| **edit** | Stays on the screen. Asks folder, video, cut, percent, boomerang, and again in the bottom box. Esc returns to the front board |
| **hello** | Result page. Body is `Hello.`. Omits the frame. The next key returns to the front board |
| **about** | Result page from `requirement-python-about`. Omits the frame. Does not name `py-tui`. Up/Down scroll when the text is longer than the screen |
| **Box height** | 3 terminal rows, then one status row |
| **Box width** | Full width the writer can place. Left border at column 0 |
| **Mark inside the frame** | one space, then `> ` |
| **Caret when the box is focused** | `█` U+2588 on the inner row |
| **Status line** | `  VideoSpeed <version>  │  main menu  │  Up/Down  •  Enter` |
| **External menu package** | Not imported and not declared |
| **Too small** | stderr names the text screen and the next step `video-speed --help` |
| **No terminal** | stderr names the missing terminal and the next step `--file`, `--start`, and `--end` |
| **Privilege** | normal user privilege |

16-column inner line, focused and empty: `│ > █          │`

### 2.2 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 2 – Intentional** (https://github.com/cloudgen/ciao): The menu and the box are two named regions. The session is `Tui`. The frame is `MenuPainter`. A later edit cannot invent a private frame in `cli.py`.
- **CIAO Principle 16 – Interactive** (https://github.com/cloudgen/ciao): A script never draws the screen, so it cannot wait inside the box.
- **CIAO Principle 1 – Caution** (https://github.com/cloudgen/ciao): A screen too small to hold the frame fails closed instead of dropping a border.
- **CIAO Principle 5 – SSOT** (https://github.com/cloudgen/ciao): This file owns the picture. The session is class `Tui`. The painter is class `MenuPainter`. The class home is `requirement-python-oop`.
- **CIAO Principle 21 – Dual policies** (https://github.com/cloudgen/ciao): The glyph table is the claimed frame. Routing stays on the interface requirement.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** The frame is three rows plus the status line, or the screen does not open.
- **Intentional:** Typing happens on the only inner line, inside the bars, and the rows are this product’s.
- **Anti-fragile:** The right border uses the last column the writer can place, and the left border stays on column 0.
- **Over-protect (Principle 20):** Do not replace the frame with a single underlined row, and do not fork the painter into `cli.py`.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT:**

- Collapse the bottom input box to one row.
- Draw the frame with ASCII `+`, `-`, or `|`, or with sharp corners `┌` `┐` `└` `┘`.
- Put the typed text, the caret, or `> ` on a border line or on a menu row.
- Inset the box so a blank column remains on the left or the right.
- Draw the numbered menu rows inside the three-row frame.
- Draw this menu with `print` / `read` / `input()` or a `Choice:` line.
- Close the screen when **edit** is chosen and continue those questions with `input()`.
- Copy the frame glyphs into `cli.py`. `FRAME_TOP_LEFT` belongs to class `MenuPainter` in `src/VideoSpeed/menu_painter.py`.
- Declare `py-tui`, or import `py_tui`.
- Point tests at a sibling checkout for this screen.
- Open a self-management board as this product’s front board.
- Add an installer verb or an in-tool `sudo` on this screen.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, **admin privilege** and **dedicated system user privilege** stay unused. **This requirement:** drawing the menu and the input box **MUST NOT** call `sudo`, wrap `apt` / `dnf`, create a dedicated account, or recommend `sudo pip` or `sudo curl \| sh`. Git Bash and Windows cmd **MUST NOT** invoke Termux `pkg`.

## 5. Design-time verification

| ID | Suite | Status |
|----|-------|--------|
| TP-TUI-01 | `tests/test_tui.py` | have |
| TP-TUI-02 | `tests/test_tui.py` | have |
| TP-TUI-03 | `tests/test_tui.py` | have |
| TP-TUI-04 | `tests/test_tui.py` | have |
| TP-TUI-05 | `tests/test_tui.py` | have |

TP-TUI-01 asserts rules 3, 4, 5, and 7: three rows, the arc corners, full width, the mark and the block caret on the only inner line, and the status line under the frame. TP-TUI-02 asserts the number, verb, and explain columns in rule 2 for this board and for a two-digit and a three-digit number field from this package’s `format_rows`, and that `FRAME_TOP_LEFT` is absent from `cli.py`. The glyph home is class `MenuPainter`. `TP-OOP-03` has landed. The suite reads the glyph from `menu_painter.py`. TP-TUI-03 asserts rule 9 and rule 1: a screen that cannot hold the frame fails closed with a next step, and product source does not import `py_tui` or declare `py-tui`. TP-TUI-04 asserts rules 6 and 8: edit stays and asks the folder line inside the frame, Exit leaves, an unknown token stays, and the about result page omits the frame and does not name `py-tui`. TP-TUI-05 asserts rule 6 and rule 8 for **hello**: choosing **7** shows `Hello.` on the result page and that page omits the frame.

**Matrix:** `reviews/requirement-test-matrix.md`
**Map:** `reviews/test-plan.md`.

## 6. Related artifacts

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-python-interactive-vs-noninteractive.md` | Menu walk versus one job |
| `docs/requirements/requirement-python-cli-interface.md` | Entry points and flag names |
| `docs/requirements/requirement-domain-videospeed.md` | edit continues the prompt session; domain lines on about |
| `docs/requirements/requirement-python-about.md` | About page body |
| `docs/requirements/requirement-python-oop.md` | Class `Tui`, class `MenuPainter`, and their files |
| `docs/requirements/requirement-python-packaging.md` | Manifest shape |
| `docs/requirements/requirement-python-dependency-management.md` | Pip floors; no menu wheel |
| `docs/requirements/requirement-runtime-prerequisites.md` | Host tools; the screen does not add a pip package |
| `docs/requirements/requirement-class-software-dev.md` | Approver none; no dest fence |
| `src/VideoSpeed/tui.py` | Class `Tui`. Session |
| `src/VideoSpeed/menu_painter.py` | Class `MenuPainter`. Frame. `TP-OOP-03` has landed |
| `src/VideoSpeed/cli.py` | `def main` and class `Cli`. Constructs `Tui` |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-09-30 | Active 1.0.0 | Default TUI style |
| 2026-10-01 | Active 1.1.0 | Painter is `src/VideoSpeed/menu.py` |
| 2026-10-01 | Active 1.1.1 | Which path runs points at the mode requirement |
| 2026-10-01 | Active 1.1.2 | About body points at `requirement-python-about` |
| 2026-10-01 | Active 1.1.3 | Front row **7** hello shows `Hello.` |
| 2026-10-01 | Active 1.1.4 | Painter home is class `Tui` in `tui.py`. Until that file exists, `menu.py` remains the writer |
| 2026-10-01 | Active 1.1.5 | A product verb enters that action on this screen. `edit` asks folder, then the specific file. `list-mp4` lists. `help` does not draw the screen |
| 2026-10-01 | Active 1.1.6 | `TP-OOP-01` landed. The writer is class `Tui` in `tui.py` |
| 2026-10-01 | Active 1.1.7 | The session stays class `Tui`. The frame is class `MenuPainter`. Picture unchanged. `TP-OOP-03` is todo |
| 2026-10-01 | Active 1.1.8 | `TP-OOP-03` has landed. The suite reads the glyph from `MenuPainter` |
| 2026-10-01 | Active 1.1.9 | The live picture, file table, and painter row say `TP-OOP-03` has landed |

**Last Updated**: 2026-10-01
**Owner**: VideoSpeed project maintainers
**Alignment**: Registry `docs/requirements/index.md`; CIAO (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
