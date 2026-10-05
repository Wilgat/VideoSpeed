**file**: docs/requirements/requirement-python-tui.md
**Status**: Active (Version 1.2.17)
**Area**: python
**Key**: `requirement-python-tui`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the picture of VideoSpeed’s text menu. The screen has two parts on one board: the menu, and a bottom input box. The first row of the menu region keeps the current path on the left and, when that row has room, a clock of the local time on the right. That clock is drawn again each second. It does not show the product name or the package version. That picture is the **default TUI style**. The session is class `Tui` in `src/VideoSpeed/tui.py`. The frame is class `MenuPainter` in `src/VideoSpeed/menu_painter.py`. Those homes are `requirement-python-oop`. `def main` stays in `src/VideoSpeed/cli.py`. Class `Cli` constructs `Tui` and passes this product’s name, version, and front board into that session. `cli.py` does not keep a second frame painter, and it does not import another menu package. `TP-OOP-03` has landed.

Which path runs stays on `requirement-python-interactive-vs-noninteractive`. This screen is the major entry when no product verb is named. `--verbose` alone on a terminal stays on that entry. A product verb opens this screen only when that mode file names it: `edit` when a target is still missing, and `list-mp4` on a terminal. `help`, `version`, `about`, and the pip lifecycle verbs stay on the terminal. The flag names also stay on `requirement-python-cli-interface`. Cut, speed, and boomerang stay on `requirement-domain-videospeed.md`. This file does not add a batch flag.

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
| The first row: Path and the folder on the left; a local clock on the right when the row has room, drawn again each second | The product name and the version on that first row. They stay on the status line. The login is not on this row |
| UTF-8 arc corners and bars, full screen width, typing on the only inner line | Frame glyphs copied into `cli.py`, and a menu pip wheel |
| The status line under the frame, and this product’s front rows (edit, language, system-log, self-management, Exit) | Putting the numbered rows inside the frame. Hello is not a front row |

| Surface | What you open | What for |
|---------|---------------|----------|
| `video-speed` on a terminal | Text screen | Menu above, input box on the bottom, status line on the last row |
| `src/VideoSpeed/cli.py` | `def main` and class `Cli` | Builds the session; does not paint the frame |
| `src/VideoSpeed/tui.py` | class `Tui` | Session loop |
| `src/VideoSpeed/menu_painter.py` | class `MenuPainter` | Frame and columns (`requirement-python-oop`). `TP-OOP-03` has landed |
| `video-speed` in a script | Error text | No screen and no wait |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Start on a terminal with no words | You see edit, language, system-log, self-management, and Exit. The bottom of the screen is one rounded box from the left edge to the right edge, then a status line. The block caret sits on the only line inside the box when that box is focused. | `video-speed` |
| Read the first row | The left side names the folder this process is in. The word before that colon is Path in English. When the row has room, the right side is a clock of the local time, hours, minutes, and seconds. It moves once a second while this board is showing. When the language is Traditional Chinese, the path word is 路徑 (`requirement-python-cli-language`). The folder and the clock are not translated. The name and the version stay on the status line under the box. | `video-speed` |
| Choose edit | The screen stays up. The menu region asks for the folder (Enter means the current directory), then the video, the cut, the percent, and boomerang. Each answer is typed in the same bottom box. Esc returns to the menu. A pause does not count as Esc. | `1` then Enter, or type `edit` |
| Choose view-log | The screen lists the log files and waits in the bottom box. It stays until you type a file number and Enter, or press Esc. A pause does not send you back to the system-log board. | `6`, then `61` |
| Start in a script | An error on stderr and a next step. The program does not draw the box and does not wait. | `video-speed` with no terminal |

## 2. Core Rules (Mandatory)

1. **Package writer.** The text-menu session **MUST** be class `Tui` in `src/VideoSpeed/tui.py`. The frame **MUST** be drawn by class `MenuPainter` in `src/VideoSpeed/menu_painter.py` (`requirement-python-oop`). VideoSpeed **MUST** pass its product name, package version, and front board into that session. `cli.py` **MUST NOT** contain the frame glyphs (`FRAME_TOP_LEFT` belongs to `MenuPainter`). The product **MUST NOT** import `py_tui` and **MUST NOT** declare `py-tui`. The menu **MUST NOT** be drawn with `print` / `read` / `input()` or a `Choice:` line. After **edit** is chosen, the domain questions stay on this same screen: the question text is in the menu region, and the answer is typed in the same bottom box. Those questions **MUST NOT** close the screen or use `input()`. `TP-OOP-03` has landed.
2. **Two regions.** On the front board the writer **MUST** draw a menu region and a bottom input box on the same screen. The menu region is every row above the box. Its first row **MUST** be the path line in rule 13. That row **MUST NOT** show the product name or the package version. The numbered rows for that board **MUST** follow the path line. Those rows **MUST NOT** be drawn inside the box. Each numbered row is a number, a verb, and an explain. On that board the number field is as wide as the longest number, and a shorter number is padded with spaces on the left (`11` beside ` 0` when the longest number has two digits; `232` beside `  0` when it has three). The verb field is as wide as the longest verb on that same board, and a shorter verb is padded with spaces immediately before the colon (`version:` beside `about  :`). Width is display columns. A character whose East Asian width is Wide or Fullwidth counts as two columns. Every other character, including Ambiguous, counts as one. Box-drawing and the block caret stay one column (rule 4). The pad and the screen column of the colon both use that width. A count of code points is not that width. A later write **MUST NOT** start on a column a wide character already occupies, including that character’s second column. A wide character that does not fit is dropped whole. The explain **MUST** be drawn after exactly one space. This board uses its own widths. VideoSpeed’s front board is the one in Implementation Notes: **1** edit, **4** language, **6** system-log, **8** self-management, **9** Exit. Front **5** is not a row. The front board **MUST NOT** list hello. Row **4** **MUST** open the language board. The codes, the file, and the words on that board stay on `requirement-python-cli-language`. Row **6** **MUST** open the system-log board. That board **MUST** list **61** view-log, **62** clear-log, **63** log-folder, and **0** Back. Row **8** **MUST** open the self-management board. That board **MUST** list **82** version, **83** about, **84** version-check, **85** self-update, **86** self-uninstall, **87** self-install, and **0** Back. `help` **MUST** stay off every numbered row. The front board **MUST NOT** list version, about, version-check, self-update, self-uninstall, self-install, view-log, clear-log, or log-folder.
3. **Three-row frame plus status line.** The bottom input box **MUST** be exactly three terminal rows high: a top border, one inner row, and a bottom border. The status line **MUST** be the next row, and that row **MUST** be the last row of the screen. The frame **MUST** span the full width of the screen. The left border is the first column. The right border is the last column the screen writer can place. There **MUST** be no blank column before the left border or after the right border.
4. **UTF-8 frame.** Those three rows **MUST** be drawn with these UTF-8 box-drawing characters. Each one occupies one column. ASCII `+`, `-`, and `|` **MUST NOT** stand in for them. Sharp corners `┌` `┐` `└` `┘` **MUST NOT** stand in for the arcs.

| Row of the box | Characters, left to right |
|----------------|---------------------------|
| Top | `╭` (U+256D), then `─` (U+2500) repeated, then `╮` (U+256E) |
| Inner | `│` (U+2502), then the input field, then `│` (U+2502) |
| Bottom | `╰` (U+2570), then `─` (U+2500) repeated, then `╯` (U+256F) |

5. **Input inside the frame.** One space, the mark `> `, the typed characters, and the caret **MUST** sit on the only inner line, strictly between the two `│` characters. The mark, the typed characters, and the caret **MUST NOT** sit on the top border, the bottom border, or a menu row. When the box is focused, the caret **MUST** be the block `█` (U+2588) at the caret index on that inner line. When the list is focused, that block **MUST NOT** be drawn. Up and Down **MUST** walk the numbered rows and the box: Down on the last row enters the box, Up on the first row enters the box, Up from the box returns to the last row, and Down from the box returns to the first row. Enter **MUST** run the typed token, or the highlighted row when the box is empty. The box **MUST NOT** be a `Choice:` line.
6. **This board’s actions.** **edit** **MUST** stay on this screen and ask the domain questions in the same bottom input box: source folder (empty means the current directory), video index, cut bounds, length percent, boomerang, and again. Esc **MUST** return to the front board. The screen **MUST NOT** close into a plain `input()` prompt for those questions. The front board **MUST NOT** list **hello**. Typing `7` or `hello` **MUST** stay on this board and **MUST NOT** show `Hello.`. **self-management** (**8**) **MUST** open that board and **MUST NOT** leave the program. On that board, **version** (**82**) **MUST** show the installed version and **MUST NOT** call pip. **about** (**83**) **MUST** show the result page. The page body is `requirement-python-about` (product name, version, domain summary, host check, and install box). That page **MUST NOT** name `py-tui`. **version-check** (**84**) **MUST** run `python -m pip index versions VideoSpeed`. **self-update** (**85**) **MUST** run `python -m pip install --upgrade VideoSpeed`. **self-uninstall** (**86**) **MUST** run `python -m pip uninstall -y VideoSpeed`. Choosing that row is the confirmation. **self-install** (**87**) **MUST** run `python -m pip install VideoSpeed`. Those pip commands **MUST NOT** use `sudo` and **MUST NOT** use `curl`. **0** **MUST** return to the front board. **system-log** (**6**) **MUST** open that board and **MUST NOT** leave the program. **view-log** (**61**) **MUST** list the `.log` file names in the log folder and **MUST** show the chosen file on a result page. The person picks the number in the bottom box. That list **MUST** stay until the person chooses a number or presses Esc. The one-second clock wait from rule 13 **MUST NOT** close it. A pause longer than one second **MUST** keep the characters already typed. The result page **MUST** be the file name, a blank line, then the file text. An empty file **MUST** show `(empty)` in place of that text. Esc **MUST** return to the system-log board and **MUST NOT** show the file. When the folder has no `.log` file, the result page **MUST** be `No log file in <folder>.` **clear-log** (**62**) **MUST** list those same names, then ask `Clear <name>? (y/n)` in the bottom box. That list and that question **MUST** stay until the person answers or presses Esc. The one-second clock wait **MUST NOT** close them. Yes **MUST** empty that file and **MUST NOT** delete it. The result page **MUST** be `Cleared <name>.` No, Esc, or Enter **MUST** leave the file unchanged and **MUST NOT** show a result page. **log-folder** (**63**) **MUST** show `Log folder: <path>`, where `<path>` is the absolute path `logDir()` returns. When no logger is present, that page **MUST** be `No log folder.` This row **MUST NOT** type a folder ladder and **MUST NOT** create a directory. These three rows are menu actions. They are not product verbs. Typing the short name on an open screen **MUST** run that row. Before the read and before the empty, the program **MUST** call `log_message` with the operation and the path, component `menu`, level INFO. The read line **MUST** be `read log path=<path>`. The empty line **MUST** be `clear log path=<path>`. The call **MUST NOT** sit inside `isDebug()`. A chosen path **MUST** be a regular `.log` file whose parent, after resolve, is that log folder. **Exit** **MUST** leave the program. An unknown token **MUST** stay on this board and show an error line in the menu region above the box. It **MUST NOT** exit the process. A positional product verb (`requirement-python-cli-interface` §2.3a) **MUST** enter that action without a front-board pick. `edit` **MUST** start at the folder question, then the specific file. `about` **MUST** open its result page and **MUST NOT** ask for a folder or a file. `hello` is not a product verb. The command `video-speed hello` **MUST NOT** draw this screen. `version` **MUST** print the installed version and **MUST NOT** call pip. `version-check`, `self-update`, and `self-install` **MUST** run the pip command above and **MUST NOT** open this screen. `self-uninstall` on the command line **MUST** require `--force` and **MUST NOT** open this screen. `list-mp4` **MUST** ask for the folder when it is missing, then show the numbered MP4 list on this screen, and **MUST NOT** encode and **MUST NOT** ask for a specific file. The command `help` **MUST NOT** draw this screen. Typing `help` on an open screen **MUST** show a result page and **MUST NOT** add a numbered help row. Empty argv with no verb **MUST** still show the front board and **MUST NOT** run self-install or self-update.
7. **Status line and errors.** The status line under the frame **MUST** show the product name, the version, the board title, and the key hint `Up/Down  •  Enter`, separated by `│`. It **MUST NOT** replace one of the three frame rows. An error line, when shown, **MUST** sit in the menu region above the box.
8. **Result page.** After about, or after another result page, the result page may omit the menu rows, the box, and the status line until the next key returns to the front board.
9. **Too small or no terminal.** If stdout is not a terminal, or the screen cannot hold the path line from rule 13 (a path shortened to fit still counts), at least one numbered menu row, the three-row box, and the status line, or cannot hold both corners plus the mark and one cell between them, the program **MUST NOT** collapse the box into one unframed row and **MUST NOT** fall back to a `Choice:` line. It **MUST** fail closed: non-zero, an operator-readable line, and a next step (`--help`, or `--file` / `--start` / `--end`).
10. **One writer.** Command text for batch jobs stays on this product’s console lines. The screen writer **MUST NOT** become a second logger for those jobs. A batch job **MUST NOT** open this screen. While **edit** is on this screen, its questions and job lines **MUST** be drawn by class `Tui` calling class `MenuPainter` (`requirement-python-oop`). They **MUST NOT** be `print` / `input()` lines that close the screen.
11. Actor / role / subject / approver: **considered**. No dest machine. No approver. The table stays on `requirement-class-software-dev.md`. This file does **not** add an actor requirement.
12. Dest fence conditions: **considered — none**. Do not invent one.
13. **Path line.** The first row of the menu region, on the front board, on the language board, on the self-management board, and on the system-log board, **MUST** be the path line. The shape **MUST** be `<label>: <current path>`, with one space after the colon. `<current path>` **MUST** be the absolute current working directory at the moment that board is painted. The path **MUST NOT** be translated. The product name and the package version **MUST NOT** appear on this row. They stay on the status line (rule 7). The label is one translatable message. `requirement-python-cli-language` selects the language and owns the word for each code. English is `Path`. Traditional Chinese is `路徑`. This file does not detect the language, and it does not invent a second line shape. The painter stores the word the caller sets. When the path text is wider than the screen, the writer **MUST** keep the path label, the colon, and the space, and **MUST** shorten the path from the left so that field fits on one row. Fit and shorten are display columns, the same width as rule 2: Wide and Fullwidth count as two, Ambiguous counts as one, and a wide character that does not fit is dropped whole. The screen **MUST** still open.

The same row **MUST** carry a clock on the right when the row has room. The clock **MUST** be the local time of this machine at the moment that row is drawn. The shape **MUST** be `HH:MM:SS`: hours, minutes, and seconds, each two digits, 24-hour, zero-padded, separated by colons. Eight characters. No date. No timezone name. No label before the clock. The clock **MUST NOT** be translated. The writer **MUST NOT** read `USER`, `USERNAME`, or `getpass` for this row, and **MUST NOT** run `id`. At least two spaces **MUST** separate the path text from the clock. When a width is known and both fields fit in that display width with those two spaces, the path field **MUST** stay at the left and the clock **MUST** end on the last column the writer can place. The gap and the fit use display columns. A wide path label that is the same display width as `Path` leaves the same gap. When both do not fit, the writer **MUST** keep the path field, including the shorten-from-the-left rule above, and **MUST NOT** draw the clock. When no width is known, the row **MUST** be the path field, then two spaces, then the clock. The product name and the package version **MUST NOT** be written as fields on this row.

While the front board, the language board, the self-management board, or the system-log board is showing, the session **MUST** wait at most one second for the next key. When that wait ends and no key arrived, the session **MUST** draw this row again with the local time at that moment and **MUST** wait again. That wait **MUST NOT** leave the program, **MUST NOT** change the highlighted row, the typed buffer, or the board, and **MUST NOT** drop a key that arrived during the wait. The session **MUST NOT** start a thread to move the clock. A screen that cannot arm this wait keeps the key read it already had. A result page, an edit question, a list-mp4 question, a notice that waits for a key, the view-log file list, the clear-log file list, and the clear confirm keep the product title on row 0. They do not draw this clock, and they do not use this one-second wait. Before each key read on those questions, the session **MUST** clear that wait. A no-key from the one-second wait **MUST NOT** be read as Esc there. The question **MUST** stay until the person answers or presses Esc. A pause longer than one second **MUST** keep the characters already typed. The clock redraw **MUST NOT** be a log line.

14. **Control-C is not row 9.** While this screen is open, Control-C is the confirm question in `requirement-python-graceful-exit`. The words are `Exit? (y/n)`. The painter draws that question on the only inner line of the bottom box. The frame stays. Row **9** Exit still leaves without that question. A clock redraw **MUST NOT** answer the question and **MUST NOT** clear it. This file does not own the yes/no decision or the exit log.

Picture of this board. The box in the picture is 16 columns wide so the corners stay visible. On a real screen those 16 columns become the full width, and the menu stays above the frame. The block in the picture is the focused caret:

```text
Path: /tmp/clips                                              14:05:09

1. edit           : cut, speed, and optional boomerang
4. language       : display language for this menu
6. system-log     : view, clear, and the log folder
8. self-management: version, about, and pip lifecycle
9. Exit           : leave
╭──────────────╮
│ > █          │
╰──────────────╯
  VideoSpeed 1.0.13  │  main menu  │  Up/Down  •  Enter
```

The same first row when the language is Traditional Chinese (`requirement-python-cli-language`):

```text
路徑: /tmp/clips                                              14:05:09
```

The spaces in those pictures stand for the gap that grows on a wider screen. The clock ends on the last column the writer can place. `14:05:09` is a sample local time, not a frozen instant. When the row cannot hold both fields, the picture of that row is the path field alone.

The column rule on a wider number field (same writer, not this product’s board):

```text
11. version: show the installed version
 0. about  : show the cache folders
```

### Sample code

`display_width` in `src/VideoSpeed/menu_painter.py` counts columns. `MenuSession._wait_key` arms the one-second clock. `Tui._tui_read` clears that wait before each question key. A no-key from the clock is not Esc. The ship unit already does this. `TP-TUI-12` has. The program was not changed.

```python
def display_width(text):
    total = 0
    for char in text:
        if unicodedata.east_asian_width(char) in ("W", "F"):
            total += 2
        else:
            total += 1
    return total

def _wait_key(self, screen):
    arm = getattr(screen, "timeout", None)
    show_clock = self.model.phase != "result"
    if arm is not None:
        if show_clock:
            arm(1000)
        else:
            arm(-1)
    key = screen.getch()
    if key == -1 and show_clock and arm is not None:
        return None
    return key

# Tui._tui_read, before each getch.
arm = getattr(screen, "timeout", None)
if arm is not None:
    arm(-1)
key = screen.getch()
if key in (-1, 27):
    return None
```

### 2.1 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| **Command** | `video-speed` |
| **Open the screen** | `video-speed` or `python -m VideoSpeed` on a terminal, with no verb and no job flags |
| **Direct verb** | `edit` starts at the folder question, then the specific file. `list-mp4` asks for the folder, then lists. `about` opens its result page. `help` does not draw this screen. `hello` is not a product verb |
| **Session** | Class `Tui` in `src/VideoSpeed/tui.py` |
| **Painter** | Class `MenuPainter` in `src/VideoSpeed/menu_painter.py` (`paint`, `format_rows`, frame glyphs). `TP-OOP-03` has landed |
| **Caller** | Class `Cli` in `src/VideoSpeed/cli.py`. `def main` stays in that file |
| **Front rows** | **1** `edit` — cut, speed, and optional boomerang; **4** `language` — display language for this menu; **6** `system-log` — view, clear, and the log folder; **8** `self-management` — version, about, and pip lifecycle; **9** `Exit` — leave. Front **5** is not a row. Hello is not a row |
| **Language rows** | **41** `English` through **53** `Ελληνικά`, and **0** `Back`. The codes, the file, and the translated words stay on `requirement-python-cli-language` |
| **System-log rows** | **61** `view-log` — list a log file and show it; **62** `clear-log` — empty one log file; **63** `log-folder` — show the log folder; **0** `Back`. These rows are not product verbs |
| **Self-management rows** | **82** `version`; **83** `about`; **84** `version-check` (pip index versions); **85** `self-update` (pip install --upgrade); **86** `self-uninstall` (pip uninstall); **87** `self-install` (pip install); **0** `Back`. `help` is typed, not numbered |
| **edit** | Stays on the screen. Asks folder, video, cut, percent, boomerang, and again in the bottom box. Esc returns to the front board |
| **about** | Row **83** on the self-management board. Result page from `requirement-python-about`. Omits the frame. Does not name `py-tui`. Up/Down scroll when the text is longer than the screen |
| **Box height** | 3 terminal rows, then one status row |
| **Box width** | Full width the writer can place. Left border at column 0 |
| **Mark inside the frame** | one space, then `> ` |
| **Caret when the box is focused** | `█` U+2588 on the inner row |
| **Top line** | Left: `Path: <absolute current working directory>`. Right, when the row has room: local time `HH:MM:SS`. Same first row on the front board, on the language board, on the self-management board, and on the system-log board. Product name and version stay on the status line |
| **Path label** | `requirement-python-cli-language` selects the word. English is `Path`. Traditional Chinese is `路徑`. The path value is not translated. This file does not detect the language |
| **Display columns** | Wide and Fullwidth count as two. Ambiguous, including box-drawing and `█`, counts as one. The verb pad, the colon column, and the path row use that width. A later write does not start inside a wide glyph. `Path` and `路徑` are both four columns |
| **Clock** | Local time, 24-hour, `HH:MM:SS`, eight characters. No label. Not translated. Sample `14:05:09` |
| **Worked top line** | `Path: /tmp/clips` then a gap, then `14:05:09` flush right. `14:05:09` is a sample local time |
| **Worked Traditional Chinese top line** | `路徑: /tmp/clips` then a gap, then `14:05:09` flush right |
| **Too narrow for the clock** | The row stays the path field. The clock is omitted. A path wider than the row is still shortened from the left |
| **Clock wait** | On the front board, the language board, the self-management board, and the system-log board, wait at most one second. No key: draw the clock again and wait again. Do not leave. Do not start a thread. Result pages, edit questions, list-mp4 questions, notices, the view-log file list, the clear-log file list, and the clear confirm do not use this wait. A no-key from the clock is not Esc on those questions |
| **Status line** | `  VideoSpeed <version>  │  main menu  │  Up/Down  •  Enter` |
| **External menu package** | Not imported and not declared |
| **Too small** | stderr names the text screen and the next step `video-speed --help` |
| **No terminal** | stderr names the missing terminal and the next step `--file`, `--start`, and `--end` |
| **Privilege** | normal user privilege |

16-column inner line, focused and empty: `│ > █          │`

### 2.2 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 2 – Intentional** (https://github.com/cloudgen/ciao): The menu and the box are two named regions. The session is `Tui`. The frame is `MenuPainter`. A later edit cannot invent a private frame in `cli.py`. The first row keeps the folder on the left and the local clock on the right, and that clock moves once a second, so the operator sees the time before choosing a row.
- **CIAO Principle 16 – Interactive** (https://github.com/cloudgen/ciao): A script never draws the screen, so it cannot wait inside the box.
- **CIAO Principle 1 – Caution** (https://github.com/cloudgen/ciao): A screen too small to hold the frame fails closed instead of dropping a border.
- **CIAO Principle 5 – SSOT** (https://github.com/cloudgen/ciao): This file owns the picture. The session is class `Tui`. The painter is class `MenuPainter`. The class home is `requirement-python-oop`.
- **CIAO Principle 21 – Dual policies** (https://github.com/cloudgen/ciao): The glyph table is the claimed frame. Routing stays on the interface requirement.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** The frame is three rows plus the status line, or the screen does not open.
- **Intentional:** Typing happens on the only inner line, inside the bars, and the rows are this product’s. The first row keeps the path on the left and the local clock on the right when the row has room, and the clock is drawn again each second.
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
- Put **about** on the front board as row **8**. Row **8** is **self-management**.
- Put **view-log**, **clear-log**, or **log-folder** on the front board. Row **4** is **language**. Row **6** is **system-log**. Those three rows stay on the system-log board.
- Make front **5** a row, or put a language code on the front board. The thirteen language rows stay under **4**.
- Delete a log file from **clear-log**. That row empties the chosen file.
- Type a log-folder ladder into the program. **log-folder** shows the path `logDir()` returns.
- Put **hello** on the front board. `hello` is not a product verb and does not draw this screen.
- Call `sudo`, `sudo pip`, or `curl` from a self-management row. version-check and self-update use pip without sudo.
- Put the product name or the package version on the first row of the menu region. That row is the path on the left and the local clock on the right when the row has room. The status line keeps the name and the version.
- Translate the folder path or the clock. The word `Path` is the message. Traditional Chinese for that word is `路徑`.
- Drop the path field to make room for the clock. A row that cannot hold both keeps the path and omits the clock.
- Put `Current`, a login, `USER`, `USERNAME`, or `getpass` on this row. Do not run `id` to fill it.
- Start a thread to move the clock. The session waits at most one second for a key, then draws the row again.
- Treat that one-second wait as Exit. No key redraws the clock and stays on the board.
- Treat that one-second wait as Esc on a bottom-box question. view-log, clear-log, edit, list-mp4, and a notice stay until the person answers or presses Esc. A pause keeps the characters already typed.
- Draw the clock on a result page or on an edit question. Those pages keep the product title on row 0.
- Write a log line for each clock redraw.
- Treat Control-C as row **9**, or let it print a traceback. The question and the exit log are `requirement-python-graceful-exit`. The painter only draws `Exit? (y/n)` in the bottom box.
- Size the verb pad, the colon’s screen column, or the path row with a code-point count when the board can contain a wide character. Wide and Fullwidth are two display columns. Ambiguous stays one.
- Start a later write inside a wide glyph, or split a wide character that does not fit.
- Mark `TP-TUI-13` have from a joined menu string alone. The suite records each screen write and its column.
- Shorten a stored short to the glyph that survives an overlap. The words stay on `requirement-python-cli-language`.
- Send `help`, `version`, `about`, or a pip lifecycle verb onto this screen because a text menu exists. Those verbs stay on the terminal. The major entry is no product verb.

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
| TP-TUI-06 | `tests/test_tui.py` | have |
| TP-TUI-07 | `tests/test_tui.py` | have |
| TP-TUI-08 | `tests/test_tui.py` | have |
| TP-TUI-09 | `tests/test_tui.py` | have |
| TP-TUI-10 | `tests/test_tui.py` | have |
| TP-TUI-11 | `tests/test_tui.py` | have |
| TP-TUI-12 | `tests/test_tui.py` | have |
| TP-TUI-13 | `tests/test_tui.py` | have |

TP-TUI-01 asserts rules 3, 4, 5, and 7: three rows, the arc corners, full width, the mark and the block caret on the only inner line, and the status line under the frame. TP-TUI-02 asserts the number, verb, and explain columns in rule 2 for this board and for a two-digit and a three-digit number field from this package’s `format_rows`, and that `FRAME_TOP_LEFT` is absent from `cli.py`. The glyph home is class `MenuPainter`. `TP-OOP-03` has landed. The suite reads the glyph from `menu_painter.py`. TP-TUI-03 asserts rule 9 and rule 1: a screen that cannot hold the frame fails closed with a next step, and product source does not import `py_tui` or declare `py-tui`. TP-TUI-04 asserts rules 6 and 8: edit stays and asks the folder line inside the frame, Exit leaves, an unknown token stays, and the about result page omits the frame and does not name `py-tui`. TP-TUI-05 asserts rule 6: the front board does not list hello, and choosing **7** stays on that board. TP-TUI-06 asserts rule 2 and rule 6: row **8** opens the self-management board, and **84** version-check runs `python -m pip index versions VideoSpeed` with no `sudo`. TP-TUI-07 asserts rule 13: the first row of the front board and of the self-management board starts with `Path: ` plus the absolute current working directory, and that row does not contain the product name or the package version as fields. A path wider than the screen is shortened from the left. The label, the colon, and the space stay. The label is `Path` in English. Traditional Chinese is `路徑` from `requirement-python-cli-language`. The painter stores the word the caller sets and does not detect a language. The status line keeps the product name and the version. TP-TUI-08 asserts that the withdrawn login field stays off this row: the path line does not draw `Current:` and does not read the Current User ladder. The 1.2.4 pass criteria that put the login on the right are withdrawn. TP-TUI-09 asserts the clock that replaced that field: when the row has room, it ends with the local time `HH:MM:SS`, flush with the last column the writer can place, and at least two spaces sit between the path and that clock. A row that cannot hold both keeps the path and omits the clock. The clock has no label and is not translated. A result page and an edit question keep the product title on row 0 and do not draw the clock. TP-TUI-10 asserts the one-second wait: while the front board, the language board, the self-management board, or the system-log board is showing, a wait of one second with no key draws the clock again and does not leave. A key that arrives is still delivered. The session does not start a thread. A result page does not use that wait, so a no-key read there still returns to the board. TP-TUI-11 asserts rule 2 and rule 6: row **6** opens the system-log board, **61** lists `.log` names and shows the chosen file, **62** asks `Clear <name>? (y/n)` and empties that file without deleting it, and **63** shows the path from `logDir()`. The read and the empty each write one `log_message` with component `menu`. TP-TUI-12 asserts rule 6 and rule 13: the view-log file list and the clear-log questions clear the one-second wait before each key read. A no-key from that wait does not return to the system-log board, and the chosen file is still shown. Esc is still a real key. A notice that waits for a key clears that same wait. TP-TUI-13 asserts rule 2 and rule 13 on the screen, not on the joined string: Wide and Fullwidth count as two columns, Ambiguous (including `╭─╮` and `█`) counts as one, the colon’s column is the display column after the short for `语言`, `系統日誌`, `시스템-로그`, and `終了`, and a path label `路径`, `路徑`, or `경로` keeps the clock on the same row when the row has room. A joined `format_rows` line is not that proof.

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
| `docs/requirements/requirement-python-cli-language.md` | Row **4** language. Codes, file, and the words that follow a language |
| `src/VideoSpeed/language_menu.py` | Class `LanguageMenu`. The painter does not detect a language |
| `docs/requirements/requirement-python-packaging.md` | Manifest shape |
| `docs/requirements/requirement-python-dependency-management.md` | Pip floors; no menu wheel |
| `docs/requirements/requirement-runtime-prerequisites.md` | Host tools; the screen does not add a pip package |
| `docs/requirements/requirement-class-software-dev.md` | Approver none; no dest fence |
| `src/VideoSpeed/tui.py` | Class `Tui`. Session |
| `src/VideoSpeed/menu_painter.py` | Class `MenuPainter`. Frame. `TP-OOP-03` has landed |
| `src/VideoSpeed/system_log.py` | Class `SystemLog`. Log file list, read, and empty. The menu picture stays in this file |
| `src/VideoSpeed/cli.py` | `def main` and class `Cli`. Constructs `Tui` |
| `docs/requirements/requirement-python-graceful-exit.md` | Control-C question and exit log. Not row **9** |

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
| 2026-10-02 | Active 1.2.0 | Front row **8** is self-management. About moves to **83**. version-check and self-update call pip |
| 2026-10-02 | Active 1.2.1 | The front board does not list hello. `video-speed hello` does not draw this screen |
| 2026-10-02 | Active 1.2.2 | The first menu row is `Path: <current path>`. The word Path translates when a multi-language environment requirement is Active. Traditional Chinese is `路徑`. Name and version stay on the status line. `TP-TUI-07` is todo |
| 2026-10-02 | Active 1.2.3 | `TP-TUI-07` has landed. The front board and the self-management board paint the path line |
| 2026-10-02 | Active 1.2.4 | The same row keeps that path on the left and, when the row has room, `Current: <login>` on the right. `TP-TUI-08` has landed |
| 2026-10-02 | Active 1.2.5 | That right-hand field is a local clock `HH:MM:SS`, drawn again each second. The login reading is withdrawn. `TP-TUI-09` and `TP-TUI-10` have landed |
| 2026-10-02 | Active 1.2.6 | Control-C while this screen is open draws `Exit? (y/n)` in the bottom box. The decision and the exit log stay on `requirement-python-graceful-exit`. Row **9** is unchanged. No new TUI proof |
| 2026-10-02 | Active 1.2.7 | Front row **4** is system-log. That board lists **41** view-log, **42** clear-log, **43** log-folder, and **0** Back. **41** lists `.log` names and shows the chosen file. **42** empties the chosen file after `Clear <name>? (y/n)`. **43** shows `logDir()`. `TP-TUI-11` has landed. `./tests/run.sh`: 93 tests, OK, skipped=1 |
| 2026-10-02 | Active 1.2.8 | The view-log file list, the clear-log questions, edit questions, list-mp4 questions, and a notice clear the one-second clock wait. A no-key from that wait is not Esc. `TP-TUI-12` has landed. `./tests/run.sh`: 94 tests, OK, skipped=1 |
| 2026-10-02 | Active 1.2.9 | Sample code shows `timeout(-1)` before a question key. The one-second wait stays on the three boards. The program was not changed |
| 2026-10-04 | Active 1.2.10 | Status-line sample is package string `1.0.11` |
| 2026-10-04 | Active 1.2.11 | Front row **4** is language. Front **5** is not a row. System-log moves to **6**, with **61** view-log, **62** clear-log, **63** log-folder, and **0** Back. The language board uses the same path line and the same one-second clock. The path word stays on `requirement-python-cli-language`. `TP-TUI-11` still has |
| 2026-10-04 | Active 1.2.12 | `hello` is not a product verb. The front board still does not list it. Typing `7` or `hello` stays on that board |
| 2026-10-04 | Active 1.2.13 | Rule 2 and rule 13 measure the verb pad, the colon column, and the path row in display columns. Wide and Fullwidth count as two. Ambiguous stays one. A later write does not start inside a wide glyph. `TP-TUI-13` has. `./tests/run.sh`: 96 tests, OK, skipped=1 |
| 2026-10-05 | Active 1.2.14 | Status-line sample is package string `1.0.12` |
| 2026-10-05 | Active 1.2.15 | This screen is the major entry when no product verb is named. `edit` and `list-mp4` stay the named screen verbs. Other product verbs stay on the terminal. No new picture |
| 2026-10-05 | Active 1.2.16 | Sample code is `display_width`, `MenuSession._wait_key`, and the `timeout(-1)` lines in `Tui._tui_read`. The program was not changed |
| 2026-10-05 | Active 1.2.17 | Status-line sample is package string `1.0.13`. During an edit job, one body line is the flashing wait from `requirement-python-time-consuming-process`. The clock on the boards is unchanged |

**Last Updated**: 2026-10-05
**Owner**: VideoSpeed project maintainers
**Alignment**: Registry `docs/requirements/index.md`; CIAO (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
