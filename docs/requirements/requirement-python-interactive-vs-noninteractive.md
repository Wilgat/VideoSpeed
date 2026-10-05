**file**: docs/requirements/requirement-python-interactive-vs-noninteractive.md
**Status**: Active (Version 1.3.5)
**Area**: python
**Key**: `requirement-python-interactive-vs-noninteractive`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the mode contract for VideoSpeed. After `--version` has already exited, `main` chooses exactly one path: the text-menu walk, one product verb (`help`, `version`, `about`, `edit`, `list-mp4`, `self-install`, `version-check`, `self-update`, `self-uninstall`), one non-interactive job, or a fail-closed stop. The text menu is the major entry: no product verb. `--verbose` alone stays on that entry when both streams are terminals. The walk asks one field at a time on the open screen. `edit`, when a target is still missing, and `list-mp4` on a terminal, are the verbs this file names for that screen. Every other product verb stays on the terminal. A verb that still needs a target asks for the folder first, then for the specific file when that verb needs one. The job path and the non-interactive verb path never wait for a person. The verb names are `requirement-python-cli-interface` §2.3a.

Which pixels the screen uses stay on `requirement-python-tui`. What cut, percent, and boomerang mean stays on `requirement-domain-videospeed`. How `main` starts (version, logger, parser) stays on `requirement-python-cli-interface`. This file owns which path runs.

### 1.1 Human-facing

**In one sentence:** In a terminal, `video-speed` with no verb and no job flags opens the menu; `video-speed edit` asks for the folder and then the file; a script passes `edit` with `--file`, `--start`, and `--end` and the program must not wait.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person at a terminal, or a script | `video-speed` or `video-speed --file clip.mp4 --start 0 --end 5` |
| The other role | The screen painter and the encode steps | `requirement-python-tui`, `requirement-video-ffmpeg-pipeline` |
| Not this file | Frame glyphs; FFmpeg filter graphs; the version integers | Those peer files |

| Includes | Excludes |
|----------|----------|
| The choice between the menu walk, one product verb, one job, and a fail-closed stop | A second prompt style using `input()` |
| One question at a time on the open screen, folder then specific file, and a job that never reads stdin | `--quiet` as a flag. `--json` is `requirement-python-json-output` |
| Defaults for an empty answer, and a non-zero stop when a script omits `--file`, `--start`, or `--end` | Empty argv installing the program |

| Surface | What you open | What for |
|---------|---------------|----------|
| `video-speed` | console script | menu when stdin is a terminal and no job flag is set |
| `video-speed --file clip.mp4 --start 0 --end 5` | one job | cut that range at 100% length, no prompts |
| `src/VideoSpeed/cli.py` | `main` | the only mode decision |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Edit in a terminal | The menu opens. **edit** asks folder, video, start, end, percent, boomerang, then again. Each answer is one line in the bottom box. Esc returns to the menu. | `video-speed` |
| Start edit by name | The front board is skipped. On a terminal the first question is the folder, then the specific file, then the rest of the field table. | `video-speed edit` |
| List MP4 files by name | On a terminal the question is the folder, then the numbered list. There is no file pick and no encode. | `video-speed list-mp4` |
| Show about by name | The page is shown. There is no folder question and no file question. | `video-speed about` |
| Run one clip from a script | No menu and no wait. Missing file, start, or end stops with a next step. | `video-speed edit --file clip.mp4 --start 1 --end 5 --percent 100` |
| Pass only a modifier | `--percent` or `--boomerang` without a verb and without a job does not open the menu. The program stops and names the job flags. | `video-speed --percent 50` |

## 2. Core Rules (Mandatory)

1. **One decision.** After argument parsing, `main` **MUST** choose exactly one of: a product verb, a non-interactive job, a fail-closed stop, or the interactive front menu. It **MUST NOT** mix them in one run. `--version` **MUST** finish inside the parser, before this decision, and **MUST** succeed with or without a terminal. The verb `help` and `--help` **MUST** print usage and exit 0, with or without a terminal, and **MUST NOT** open the menu.
2. **Selectors, modifiers, and verbs.** A selector is `--file`, `--start`, `--end`, or `--folder`. A modifier is `--percent` or `--boomerang`. A product verb is the positional token `help`, `version`, `about`, `edit`, `list-mp4`, `self-install`, `version-check`, `self-update`, or `self-uninstall`. `hello` is not a product verb. `--force` confirms `self-uninstall` only. Any selector and no product verb **MUST** select the non-interactive path, even when stdin is a terminal. That path **MUST NOT** open the front menu and **MUST NOT** ask for a file. A modifier with no selector and no product verb **MUST** fail closed. It **MUST NOT** open the menu and **MUST NOT** be ignored. A product verb is not a selector. On a terminal, the verb **MUST** ask only for the targets §2.1b still marks as missing. A complete edit job (`--file`, `--start`, and `--end`), with or without the verb `edit`, **MUST** stay on the non-interactive path even on a terminal.
3. **No hang.** The non-interactive path and the fail-closed path **MUST NOT** read stdin, **MUST NOT** call `input()`, and **MUST NOT** open the text menu. A missing terminal on the front-menu path **MUST** fail closed with a next step. `help`, `version`, `about`, `list-mp4`, `self-install`, `version-check`, `self-update`, and `self-uninstall --force` with no terminal are the verb rows in §2.1b. They run and do not wait. `edit` with no terminal is the job row or the fail-closed row. A pip child **MUST** take stdin from `DEVNULL`.
4. **Terminal measured at the decision.** `main` **MUST** treat stdin as the gate for “a person can answer.” `open_text_menu` **MUST** treat stdout as the gate for “the screen can be drawn.” Question helpers **MUST NOT** call `isatty` again. They consume the already open screen.
5. **Interactive walk.** With no product verb, no selector, no lone modifier, stdin a terminal, and no `--json`, `main` **MUST** open the text menu from `requirement-python-tui`. **edit** **MUST** ask the fields in the table below, one at a time, in the same bottom box. Empty answers use the defaults. Esc **MUST** return to the front menu and **MUST NOT** encode. An invalid value **MUST** re-ask and **MUST NOT** encode. When `--json` is set, this walk **MUST NOT** open the menu. Prompts and the single object are `requirement-python-json-output`.
6. **Non-interactive job.** The job **MUST** require `--file`, `--start`, and `--end`. The verb `edit` with those three flags is the same job. Omitted `--percent` **MUST** mean 100. Omitted `--boomerang` **MUST** mean no reverse pass. `--folder` with no product verb **MUST** only check that the path is a directory containing at least one MP4. It **MUST NOT** pick a file and it **MUST NOT** start questions. The same range and percent checks as the walk **MUST** run before encode. Failure **MUST** be non-zero.
7. **Same domain, two exits.** “No MP4” on the walk **MUST** show the message and return to the menu. “No MP4” or a bad `--folder` on the job path **MUST** exit non-zero. A missing `ffmpeg` on the walk **MUST** show the message and return to the menu. A missing `ffmpeg` on the job path **MUST** exit non-zero.
8. **Again.** After a walk job, the again question **MUST** default to no. Yes **MUST** re-ask the cut on the same video. No **MUST** return to the menu. The job path **MUST NOT** ask again.
9. Actor / role / subject / approver: **considered**. No dest machine. No approver. The table stays on `requirement-class-software-dev.md`.
10. Dest fence conditions: **considered — none**. Do not invent one.
11. **Verb targets.** §2.1b is the prompt order. The program **MUST** ask the folder before the specific file. It **MUST NOT** ask either question for `help`, `version`, `about`, `self-install`, `version-check`, `self-update`, or `self-uninstall`. It **MUST NOT** ask for a specific file for `list-mp4`. It **MUST NOT** call `input()`. On a terminal the questions use the open text screen from `requirement-python-tui`. When `--json` is set, the same order is asked on the error stream and the screen stays closed (`requirement-python-json-output`). The verb **MUST** start at that question. It **MUST NOT** require a front-board pick first. Without a terminal the verb **MUST NOT** read stdin.
12. **`list-mp4`.** On a terminal, a missing folder uses the folder prompt. Enter means the current directory. The next screen is the numbered MP4 list, then stop. Without a terminal, a missing `--folder` means the current directory, the list is printed, and the program **MUST NOT** prompt. When `--file` is present and `--folder` is absent, the folder **MUST** be the parent of that file, and the verb **MUST** still only list. No MP4 **MUST** be a non-zero exit on this path. The verb **MUST NOT** encode and **MUST NOT** pick a file for the person.
13. **`about`.** It **MUST** show its page and exit. The page is `requirement-python-about`. It **MUST NOT** ask for a folder or a file, with or without a terminal. Job selectors and modifiers on this verb **MUST** be ignored. It **MUST NOT** encode.
14. **Unknown verb.** A positional token outside `help`, `version`, `about`, `edit`, `list-mp4`, `self-install`, `version-check`, `self-update`, and `self-uninstall` **MUST** exit non-zero, **MUST** name those verbs, and **MUST NOT** open the menu or wait. `hello` is outside that list. It **MUST NOT** print `Hello.`. `./build.sh` tokens such as `setup` stay unknown here. `version` is a product verb. It is not the `./build.sh version` maintainer verb.
15. **Control-C confirm.** When the text screen is already open, Control-C asks `Exit? (y/n)` under `requirement-python-graceful-exit`. That question consumes the open screen. It **MUST NOT** call `isatty`. It is not a new mode decision and it is not row 9. `--json`, the non-interactive job, and a run with no text screen **MUST NOT** ask and **MUST NOT** hang. Those exits stay on `requirement-python-graceful-exit`.
16. **Major entry and the verb route.** The text menu is the major entry. No product verb, and `--verbose` with no product verb, **MUST** open that menu when stdin and stdout are terminals, no selector is set, no lone modifier is set, and `--json` is not set. `--json` with no product verb **MUST** stay JSON help and **MUST NOT** open the menu. A product verb **MUST** stay on the terminal unless this file names that verb for the screen. This file names `edit` when a folder or a file is still missing, and `list-mp4` on a terminal. `help`, `version`, `about`, `self-install`, `version-check`, `self-update`, and `self-uninstall` **MUST NOT** open the menu.

### 2.1 Field table (interactive edit)

| Field | Secret | Prompt label | Empty means | On failure |
|-------|--------|--------------|-------------|------------|
| Folder | no | `Folder (Enter = current):` | current directory | Not a directory: re-ask. No MP4: show the message, then the menu |
| Video | no | `Choose video (1–N):` | no default; re-ask | Index outside 1–N: re-ask. Unreadable duration: re-ask the video |
| Start | no | `Start seconds (default 0.0):` | `0.0` | Invalid range: re-ask start for this video. Do not encode |
| End | no | `End seconds [{duration:.3f}]:` | probed duration | Same as start |
| Percent | no | `New length % [100%]:` | `100` | Outside 20–200: re-ask start for this video. Do not encode |
| Boomerang | no | `Make it go forward + backward (y/n) [n]:` | no | Anything other than y/yes/n/no: re-ask this question |
| Again | no | `Again? (y/n):` | no | Same y/n rule. Yes repeats the cut on this video |

Esc at any row returns to the front menu. The process stays up until **Exit**. Control-C asks `Exit? (y/n)` before it leaves. Declining stays. Row 9 still leaves without that question.

Direct `video-speed edit` on a terminal uses this same table. It starts at Folder when the directory is still unknown, and at Video when the directory is known and `--file` is omitted. A supplied `--file` skips Folder and Video. A supplied `--percent` or `--boomerang` pre-fills that field. It does not skip Folder or Video, and it does not cancel the verb.

### 2.1b Verb prompts (folder, then the specific file)

On a terminal, ask only the rows this verb still needs. One question at a time, in the bottom box. Empty folder means the current directory. Then ask the specific file only when the Need file column says yes.

| Verb | Need folder | Need file | On a terminal, when a target is missing | With no terminal |
|------|-------------|-----------|------------------------------------------|------------------|
| `help` | no | no | Usage text, exit 0. No screen | Same usage text, exit 0 |
| `version` | no | no | Installed version. No pip | Same line, exit 0 |
| `about` | no | no | About page. No folder line and no file line | Same page on the console, exit 0 |
| `self-install` | no | no | `python -m pip install VideoSpeed`. No screen | Same command, no wait |
| `version-check` | no | no | `python -m pip index versions VideoSpeed`. No screen | Same command, no wait |
| `self-update` | no | no | `python -m pip install --upgrade VideoSpeed`. No screen | Same command, no wait |
| `self-uninstall` | no | no | Needs `--force`, then `python -m pip uninstall -y VideoSpeed` | Same. Without `--force`, exit 1 |
| `edit` | yes | yes | Folder, then `Choose video (1–N):`, then §2.1 from Start | Require `--file`, `--start`, and `--end`. Missing flags exit 1. Do not prompt |
| `list-mp4` | yes | no | Folder, then the numbered MP4 list. Stop. Do not encode | List `--folder`, or the current directory when it is omitted. Do not prompt |

`edit --folder ./clips` on a terminal skips the folder line and asks for the specific file. `edit --file clip.mp4` on a terminal skips the folder line and the file line, then asks Start when `--start` or `--end` is missing. `edit --file clip.mp4 --start 1 --end 5` does not prompt, on a terminal or off it.

### 2.2 Mode matrix (this project)

| Invocation | Path | Must not |
|------------|------|----------|
| `--help`, verb `help`, or `--version` | Exit 0. Usage text, or the version line. Not a job and not the menu | Wait; require `cv2`; ask for a folder |
| Verb `about` | That page. No folder prompt and no file prompt | Encode; open the front menu first; wait for a folder |
| Verb `version` | Installed version. No pip | Open the menu; call pip |
| Verb `version-check`, `self-update`, or `self-install` | That pip command. No menu | `sudo`; `curl`; a folder prompt |
| Verb `self-uninstall` without `--force` | Exit 1. Name `--force` | Call pip; open the menu |
| Verb `self-uninstall --force` | `python -m pip uninstall -y VideoSpeed` | A folder prompt; `sudo` |
| Verb `edit` on a terminal, folder or file still missing | Edit questions in §2.1b: folder, then the specific file, then the rest of §2.1 | `input()`; start at the front board; encode before the file is chosen |
| Verb `edit` with `--file`, `--start`, and `--end` | One job. Percent default 100. Boomerang default off | Ask again; open the menu; read stdin |
| Verb `edit` with no terminal and without `--file`, `--start`, and `--end` | Exit 1. Name the missing flags | Prompt; open the menu |
| Verb `list-mp4` on a terminal, no `--folder` | Folder prompt, then the numbered list. Do not encode | Ask for a specific file; encode |
| Verb `list-mp4` with no terminal | List `--folder` or the current directory. No MP4 exits 1 | Prompt; encode; pick a file |
| Unknown positional verb | Exit 1. Name `help`, `version`, `about`, `edit`, `list-mp4`, `self-install`, `version-check`, `self-update`, `self-uninstall`. `hello` is this row | Open the menu; wait; print `Hello.` |
| No verb, no selectors, no modifiers, stdin is a terminal, stdout is a terminal | Menu, then edit’s field table | `input()`; close the screen between questions |
| No verb, `--verbose` only, stdin is a terminal, stdout is a terminal | Menu. `--verbose` is not a command token | Treat `--verbose` as a verb; skip the screen |
| No verb, no selectors, no modifiers, stdin is not a terminal | Exit 1. Next step names `--file`, `--start`, `--end`, or a terminal | Open the menu; wait |
| No verb, no selectors, no modifiers, stdin is a terminal, stdout is not | Exit 1. Next step names a terminal or the job flags | Draw a partial box; wait |
| No verb, any selector, even on a terminal | Non-interactive checks, then at most one job | Open the menu; read stdin |
| No verb, `--percent` or `--boomerang`, and no selector | Exit 1. Next step names `--file`, `--start`, and `--end` | Open the menu |
| No verb, `--file` without `--start` or without `--end` | Exit 1. Name the missing flags | Encode; prompt |
| No verb, `--folder` that is not a directory, or has no MP4 | Exit 1 | Prompt for a video |
| No verb, `--folder` with MP4s but no `--file` | Exit 1. Say that `--file`, `--start`, and `--end` are still required | Pick a file for the person |
| No verb, `--file`, `--start`, `--end`, optional `--percent`, optional `--boomerang` | One job. Percent default 100. Boomerang default off | Ask again; open the menu |
| `--json` on any row above | The same path decision. The menu stays closed. A verb that still needs a folder or a file asks on the error stream, folder then file. Standard output is the one object in `requirement-python-json-output` | Draw the text menu; mix progress into that object |

### Sample code

```text
video-speed
video-speed help
video-speed about
video-speed edit
video-speed edit --folder ./clips
video-speed edit --file clip.mp4 --start 1 --end 5 --percent 100
video-speed list-mp4
video-speed list-mp4 --folder ./clips
video-speed --file clip.mp4 --start 1 --end 5 --percent 100
video-speed --file clip.mp4 --start 0 --end 5 --boomerang
video-speed --folder ./clips
video-speed --json
video-speed --json edit
video-speed --json --file clip.mp4 --start 0 --end 5
```

### 2.3 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Decision** | `def main` in `src/VideoSpeed/cli.py`, after `parse_args`. `main` stays in that file |
| **Product verbs** | `help`, `version`, `about`, `edit`, `list-mp4`, `self-install`, `version-check`, `self-update`, `self-uninstall` (`requirement-python-cli-interface` §2.3a). `hello` is not in this list |
| **Interactive entry** | No verb: `Tui.open_text_menu` → edit → `Tui._edit_in_tui`. Verb `edit` or `list-mp4` on a terminal starts at the folder question |
| **Job entry** | `Encoder.batch_session`, including `edit` with `--file`, `--start`, and `--end` (`requirement-python-oop`). `TP-OOP-04` has landed |
| **Screen** | Class `Tui` in `src/VideoSpeed/tui.py`. Frame is class `MenuPainter` (`requirement-python-tui`, `requirement-python-oop`) |
| **Selectors** | `--file`, `--start`, `--end`, `--folder` |
| **Modifiers** | `--percent` (default 100), `--boomerang` (default off) |
| **Percent bounds** | 20–200, same as `valid_percent` |
| **Range** | `0 <= start < end <= duration`, same as `valid_cut_range` |
| **stdin gate** | `Cli.stdin_is_tty` from `main` only |
| **stdout gate** | `Cli.stdout_is_tty` from `Tui.open_text_menu` only |
| **Quiet / JSON** | No `--quiet`. `--verbose` is named on `requirement-python-cli-interface` and shows status lines on a run that is not `--json` and not a text screen. `--json` is `requirement-python-json-output`. Durable log quiet-before-menu stays on `requirement-python-cli-logging` |
| **Privilege** | normal user privilege |

### 2.4 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 16 – Interactive** (https://github.com/cloudgen/ciao): The menu walk, the verb prompts, and the script job are all named. A script cannot sit inside the box.
- **CIAO Principle 2 – Intentional** (https://github.com/cloudgen/ciao): One decision in `main` picks the path. Modifiers do not silently become the menu.
- **CIAO Principle 1 – Caution** (https://github.com/cloudgen/ciao): A missing flag, a bad range, or a bad percent stops before encode.
- **CIAO Principle 5 – SSOT** (https://github.com/cloudgen/ciao): This file owns the mode matrix. Peers point here.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, **admin privilege** and **dedicated system user privilege** stay unused. **This requirement:** choosing the menu or the job **MUST NOT** call `sudo`, wrap `apt` / `dnf`, create a dedicated account, or recommend `sudo pip` or `sudo curl \| sh`. Git Bash and Windows cmd **MUST NOT** invoke Termux `pkg`. A missing terminal still fails closed. It does not escalate.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** No encode until the range and the percent are valid.
- **Intentional:** The field table, the verb prompt order, and the mode matrix are the paths.
- **Anti-fragile:** Pipes and CI hit the fail-closed path, the job path, or a verb that needs no answer, and return.
- **Over-protect (Principle 20):** Do not add a second walk with `input()`, do not let a lone `--percent` open the menu, and do not delete the product verbs.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT:**

- Open the front menu when a selector is set and no product verb is asking for a missing target, or when a modifier is set with no selector and no product verb.
- Open the text menu for `help`, `version`, `about`, `self-install`, `version-check`, `self-update`, or `self-uninstall`. Those verbs stay on the terminal. The major entry is no product verb. `--verbose` alone, on a terminal, stays on that entry.
- Open the front menu for `video-speed edit` or `video-speed list-mp4` before the folder question.
- Call `input()` for folder, video, cut, percent, boomerang, or again.
- Wait on stdin when no selector and no askable verb is set and stdin is not a terminal.
- Prompt for `help`, `about`, or for a file during `list-mp4`.
- Ask for a file before the folder when both are still missing.
- Drop `help`, `about`, `edit`, or `list-mp4` and leave only the flag job. Do not add `hello` as a product verb.
- Treat empty argv as an install.
- Encode after an invalid range or an invalid percent in either path.
- Encode from `list-mp4`, `about`, or `help`.
- Make the question helpers call `isatty` as a second mode decision.
- Ask “again” on the job path.
- Turn `--folder` with no product verb into an interactive file picker.

## 5. Design-time verification

| ID | Suite | Status |
|----|-------|--------|
| TP-MODE-01 | `tests/test_cli.py` | have |
| TP-MODE-02 | `tests/test_cli.py` | have |
| TP-MODE-03 | `tests/test_cli.py` | have |
| TP-MODE-04 | `tests/test_tui.py` | have |
| TP-MODE-05 | `tests/test_tui.py` · `tests/test_cli.py` | have |
| TP-MODE-06 | `tests/test_cli.py` | have |
| TP-MODE-07 | `tests/test_cli.py` · `tests/test_tui.py` | have |
| TP-MODE-08 | `tests/test_cli.py` | have |
| TP-MODE-09 | `tests/test_cli.py` | have |
| TP-CLI-03 | — | todo |
| TP-CLI-06 | `tests/test_cli.py` | have |
| TP-CLI-07 | `tests/test_cli.py` | have |

TP-MODE-01 asserts rule 2 and rule 3 for a selector with no product verb: `--file`, `--start`, `--end`, or `--folder` does not call `open_text_menu` even when stdin is a terminal. TP-MODE-02 asserts a lone `--percent` or `--boomerang`, with no verb, exits 1, names `--file`, `--start`, and `--end`, and does not open the menu even when stdin is a terminal. TP-MODE-03 asserts empty argv with no verb and no terminal exits 1 and names a next step. TP-MODE-04 asserts edit asks the folder line inside the frame and does not call `input()` (`requirement-python-tui`, `TP-TUI-04`). TP-MODE-05 is `edit` on a terminal with no `--file`: the folder line, then the video line, inside the frame, and no `input()`. TP-MODE-06 is `edit` with no terminal and without `--file`, `--start`, and `--end`: exit 1, no prompt. TP-MODE-07 is `list-mp4`: on a terminal it asks for the folder when `--folder` is omitted, then lists, and does not encode; with no terminal it lists `--folder` or the current directory and does not prompt. TP-MODE-08 is `about` and `help`: no folder prompt and no file prompt, with or without a terminal. TP-MODE-09 asserts rule 16: empty argv and `--verbose` alone, with both streams terminals, open the menu; `version`, `about`, and `help` do not. `hello` is an unknown verb. TP-CLI-03 remains the full terminal walk. TP-CLI-06 asserts an incomplete job and a missing file fail closed. TP-CLI-07 asserts `help` lists the nine product verbs, including `version`, `self-install`, `version-check`, `self-update`, and `self-uninstall`, and does not list `hello`. An unknown verb, including `hello`, exits 1.

**Matrix:** `reviews/requirement-test-matrix.md`
**Map:** `reviews/test-plan.md`.

## 6. Related artifacts

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-python-cli-interface.md` | Entry points, product verb names, and `main` order; points here for the mode |
| `docs/requirements/requirement-python-json-output.md` | `--json`: no menu; one object on standard output |
| `docs/requirements/requirement-python-tui.md` | Screen look |
| `docs/requirements/requirement-domain-videospeed.md` | Domain steps D-01..D-08; the same flags |
| `docs/requirements/requirement-python-error-handling.md` | Console failure sentences |
| `docs/requirements/requirement-python-cli-logging.md` | Quiet before the menu |
| `docs/requirements/requirement-class-software-dev.md` | Approver none; no dest fence |
| `src/VideoSpeed/cli.py` | Decision and both paths |
| `docs/requirements/requirement-python-graceful-exit.md` | Control-C question. Not a new mode |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-01 | Active 1.0.0 | Mode matrix for the menu walk and the one-job path |
| 2026-10-01 | Active 1.1.0 | `--json` keeps this matrix and closes the menu |
| 2026-10-01 | Active 1.2.0 | Product verbs. Interactive `edit` asks folder, then the specific file. `list-mp4` asks for the folder only. `help`, `about`, and `hello` do not ask |
| 2026-10-01 | Active 1.2.1 | The text screen is class `Tui` in `src/VideoSpeed/tui.py` |
| 2026-10-01 | Active 1.2.2 | The session stays class `Tui`. The frame is class `MenuPainter`. The question order stays here. `EditWalk` carries it |
| 2026-10-01 | Active 1.2.3 | `Encoder.batch_session` is on disk. `TP-OOP-04` has landed. The question order stays here |
| 2026-10-02 | Active 1.3.0 | `version`, `self-install`, `version-check`, `self-update`, and `self-uninstall` are product verbs. Python lifecycle verbs call pip. Empty argv is not those verbs |
| 2026-10-02 | Active 1.3.1 | Control-C on an open text screen asks `Exit? (y/n)`. The question does not call `isatty`. No screen and `--json` do not ask. The decision stays on `requirement-python-graceful-exit` |
| 2026-10-02 | Active 1.3.2 | Sample code shows the menu walk and the one-job commands |
| 2026-10-04 | Active 1.3.3 | `hello` is not a product verb. That token is the unknown-verb row |
| 2026-10-05 | Active 1.3.4 | `--verbose` shows status lines except on `--json` and a text screen. There is still no `--quiet` |
| 2026-10-05 | Active 1.3.5 | The text menu is the major entry: no product verb. `--verbose` alone stays on that entry. `edit` and `list-mp4` stay the named screen verbs. Every other product verb stays on the terminal. `TP-MODE-09` has. `./tests/run.sh`: 98 tests, OK, skipped=1 |

**Last Updated**: 2026-10-05
**Owner**: VideoSpeed project maintainers
**Alignment**: Registry `docs/requirements/index.md`; CIAO (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
