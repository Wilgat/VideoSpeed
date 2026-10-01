**file**: docs/requirements/requirement-python-interactive-vs-noninteractive.md
**Status**: Active (Version 1.1.0)
**Area**: python
**Key**: `requirement-python-interactive-vs-noninteractive`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the mode contract for VideoSpeed. After `--help` and `--version` have already exited, `main` chooses exactly one path: the text-menu walk, one non-interactive job, or a fail-closed stop. The walk asks one field at a time on the open screen. The job path never waits for a person.

Which pixels the screen uses stay on `requirement-python-tui`. What cut, percent, and boomerang mean stays on `requirement-domain-videospeed`. How `main` starts (version, logger, parser) stays on `requirement-python-cli-interface`. This file owns which path runs.

### 1.1 Human-facing

**In one sentence:** In a terminal, `video-speed` with no job flags opens the menu and edit asks one question at a time; a script passes `--file`, `--start`, and `--end` and the program must not wait.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person at a terminal, or a script | `video-speed` or `video-speed --file clip.mp4 --start 0 --end 5` |
| The other role | The screen painter and the encode steps | `requirement-python-tui`, `requirement-video-ffmpeg-pipeline` |
| Not this file | Frame glyphs; FFmpeg filter graphs; the version integers | Those peer files |

| Includes | Excludes |
|----------|----------|
| The choice between the menu walk, one job, and a fail-closed stop | A second prompt style using `input()` |
| One question at a time on the open screen, and a job that never reads stdin | `--quiet` as a flag. `--json` is `requirement-python-json-output` |
| Defaults for an empty answer, and a non-zero stop when a script omits `--file`, `--start`, or `--end` | Empty argv installing the program |

| Surface | What you open | What for |
|---------|---------------|----------|
| `video-speed` | console script | menu when stdin is a terminal and no job flag is set |
| `video-speed --file clip.mp4 --start 0 --end 5` | one job | cut that range at 100% length, no prompts |
| `src/VideoSpeed/cli.py` | `main` | the only mode decision |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Edit in a terminal | The menu opens. **edit** asks folder, video, start, end, percent, boomerang, then again. Each answer is one line in the bottom box. Esc returns to the menu. | `video-speed` |
| Run one clip from a script | No menu and no wait. Missing file, start, or end stops with a next step. | `video-speed --file clip.mp4 --start 1 --end 5 --percent 100` |
| Pass only a modifier | `--percent` or `--boomerang` without a job does not open the menu. The program stops and names the job flags. | `video-speed --percent 50` |

## 2. Core Rules (Mandatory)

1. **One decision.** After argument parsing, `main` **MUST** choose exactly one of: non-interactive job, fail closed, or interactive menu. It **MUST NOT** mix them in one run. `--help` and `--version` **MUST** finish inside the parser, before this decision, and **MUST** succeed with or without a terminal.
2. **Selectors and modifiers.** A selector is `--file`, `--start`, `--end`, or `--folder`. A modifier is `--percent` or `--boomerang`. Any selector **MUST** select the non-interactive path, even when stdin is a terminal. A modifier with no selector **MUST** fail closed. It **MUST NOT** open the menu and **MUST NOT** be ignored.
3. **No hang.** The non-interactive path and the fail-closed path **MUST NOT** read stdin, **MUST NOT** call `input()`, and **MUST NOT** open the text menu. A missing terminal on the interactive path **MUST** fail closed with a next step.
4. **Terminal measured at the decision.** `main` **MUST** treat stdin as the gate for “a person can answer.” `open_text_menu` **MUST** treat stdout as the gate for “the screen can be drawn.” Question helpers **MUST NOT** call `isatty` again. They consume the already open screen.
5. **Interactive walk.** With no selector, no lone modifier, stdin a terminal, and no `--json`, `main` **MUST** open the text menu from `requirement-python-tui`. **edit** **MUST** ask the fields in the table below, one at a time, in the same bottom box. Empty answers use the defaults. Esc **MUST** return to the front menu and **MUST NOT** encode. An invalid value **MUST** re-ask and **MUST NOT** encode. When `--json` is set, this walk **MUST NOT** open the menu. Prompts and the single object are `requirement-python-json-output`.
6. **Non-interactive job.** The job **MUST** require `--file`, `--start`, and `--end`. Omitted `--percent` **MUST** mean 100. Omitted `--boomerang` **MUST** mean no reverse pass. `--folder` **MUST** only check that the path is a directory containing at least one MP4. It **MUST NOT** pick a file and it **MUST NOT** start questions. The same range and percent checks as the walk **MUST** run before encode. Failure **MUST** be non-zero.
7. **Same domain, two exits.** “No MP4” on the walk **MUST** show the message and return to the menu. “No MP4” or a bad `--folder` on the job path **MUST** exit non-zero. A missing `ffmpeg` on the walk **MUST** show the message and return to the menu. A missing `ffmpeg` on the job path **MUST** exit non-zero.
8. **Again.** After a walk job, the again question **MUST** default to no. Yes **MUST** re-ask the cut on the same video. No **MUST** return to the menu. The job path **MUST NOT** ask again.
9. Actor / role / subject / approver: **considered**. No dest machine. No approver. The table stays on `requirement-class-software-dev.md`.
10. Dest fence conditions: **considered — none**. Do not invent one.

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

Esc at any row returns to the front menu. The process stays up until **Exit**.

### 2.2 Mode matrix (this project)

| Invocation | Path | Must not |
|------------|------|----------|
| `--help` or `--version` | Parser exits 0. Not a job and not the menu | Wait; require `cv2` |
| No selectors, no modifiers, stdin is a terminal, stdout is a terminal | Menu, then edit’s field table | `input()`; close the screen between questions |
| No selectors, no modifiers, stdin is not a terminal | Exit 1. Next step names `--file`, `--start`, `--end`, or a terminal | Open the menu; wait |
| No selectors, no modifiers, stdin is a terminal, stdout is not | Exit 1. Next step names a terminal or the job flags | Draw a partial box; wait |
| Any selector, even on a terminal | Non-interactive checks, then at most one job | Open the menu; read stdin |
| `--percent` or `--boomerang` and no selector | Exit 1. Next step names `--file`, `--start`, and `--end` | Open the menu |
| `--file` without `--start` or without `--end` | Exit 1. Name the missing flags | Encode; prompt |
| `--folder` that is not a directory, or has no MP4 | Exit 1 | Prompt for a video |
| `--folder` with MP4s but no `--file` | Exit 1. Say that `--file`, `--start`, and `--end` are still required | Pick a file for the person |
| `--file`, `--start`, `--end`, optional `--percent`, optional `--boomerang` | One job. Percent default 100. Boomerang default off | Ask again; open the menu |
| `--json` on any row above | The same path decision. The menu stays closed. Standard output is the one object in `requirement-python-json-output` | Draw the text menu; mix progress into that object |

Samples:

```text
video-speed
video-speed --file clip.mp4 --start 1 --end 5 --percent 100
video-speed --file clip.mp4 --start 0 --end 5 --boomerang
video-speed --folder ./clips
video-speed --json
video-speed --json --file clip.mp4 --start 0 --end 5
```

### 2.3 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Decision** | `src/VideoSpeed/cli.py` `main`, after `parse_args` |
| **Interactive entry** | `open_text_menu` → edit → `_edit_in_tui` |
| **Job entry** | `batch_session` |
| **Screen** | `src/VideoSpeed/menu.py` (`requirement-python-tui`) |
| **Selectors** | `--file`, `--start`, `--end`, `--folder` |
| **Modifiers** | `--percent` (default 100), `--boomerang` (default off) |
| **Percent bounds** | 20–200, same as `valid_percent` |
| **Range** | `0 <= start < end <= duration`, same as `valid_cut_range` |
| **stdin gate** | `stdin_is_tty` from `main` only |
| **stdout gate** | `stdout_is_tty` from `open_text_menu` only |
| **Quiet / JSON** | No `--quiet`. `--json` is `requirement-python-json-output`. Durable log quiet-before-menu stays on `requirement-python-cli-logging` |
| **Privilege** | normal user privilege |

### 2.4 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 16 – Interactive** (https://github.com/cloudgen/ciao): The menu walk and the script job are both named. A script cannot sit inside the box.
- **CIAO Principle 2 – Intentional** (https://github.com/cloudgen/ciao): One decision in `main` picks the path. Modifiers do not silently become the menu.
- **CIAO Principle 1 – Caution** (https://github.com/cloudgen/ciao): A missing flag, a bad range, or a bad percent stops before encode.
- **CIAO Principle 5 – SSOT** (https://github.com/cloudgen/ciao): This file owns the mode matrix. Peers point here.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, **admin privilege** and **dedicated system user privilege** stay unused. **This requirement:** choosing the menu or the job **MUST NOT** call `sudo`, wrap `apt` / `dnf`, create a dedicated account, or recommend `sudo pip` or `sudo curl \| sh`. Git Bash and Windows cmd **MUST NOT** invoke Termux `pkg`. A missing terminal still fails closed. It does not escalate.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** No encode until the range and the percent are valid.
- **Intentional:** The field table and the mode matrix are the two paths.
- **Anti-fragile:** Pipes and CI hit the fail-closed or job path and return.
- **Over-protect (Principle 20):** Do not add a second walk with `input()`, and do not let a lone `--percent` open the menu.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT:**

- Open the text menu when any selector is set, or when a modifier is set without a selector.
- Call `input()` for folder, video, cut, percent, boomerang, or again.
- Wait on stdin when no selector is set and stdin is not a terminal.
- Treat empty argv as an install.
- Encode after an invalid range or an invalid percent in either path.
- Make the question helpers call `isatty` as a second mode decision.
- Ask “again” on the job path.
- Turn `--folder` into an interactive file picker.

## 5. Design-time verification

| ID | Suite | Status |
|----|-------|--------|
| TP-MODE-01 | `tests/test_cli.py` | have |
| TP-MODE-02 | `tests/test_cli.py` | have |
| TP-MODE-03 | `tests/test_cli.py` | have |
| TP-MODE-04 | `tests/test_tui.py` | have |
| TP-CLI-03 | — | todo |
| TP-CLI-06 | `tests/test_cli.py` | have |

TP-MODE-01 asserts rule 2 and rule 3: `--file`, `--start`, `--end`, or `--folder` does not call `open_text_menu` even when stdin is a terminal. TP-MODE-02 asserts a lone `--percent` or `--boomerang` exits 1, names `--file`, `--start`, and `--end`, and does not open the menu even when stdin is a terminal. TP-MODE-03 asserts empty argv with no terminal exits 1 and names a next step. TP-MODE-04 asserts edit asks the folder line inside the frame and does not call `input()` (`requirement-python-tui`, `TP-TUI-04`). TP-CLI-03 remains the full terminal walk. TP-CLI-06 asserts an incomplete job and a missing file fail closed.

**Matrix:** `reviews/requirement-test-matrix.md`
**Map:** `reviews/test-plan.md`.

## 6. Related artifacts

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-python-cli-interface.md` | Entry points and `main` order; points here for the mode |
| `docs/requirements/requirement-python-json-output.md` | `--json`: no menu; one object on standard output |
| `docs/requirements/requirement-python-tui.md` | Screen look |
| `docs/requirements/requirement-domain-videospeed.md` | Domain steps D-01..D-08; the same flags |
| `docs/requirements/requirement-python-error-handling.md` | Console failure sentences |
| `docs/requirements/requirement-python-cli-logging.md` | Quiet before the menu |
| `docs/requirements/requirement-class-software-dev.md` | Approver none; no dest fence |
| `src/VideoSpeed/cli.py` | Decision and both paths |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-01 | Active 1.0.0 | Mode matrix for the menu walk and the one-job path |
| 2026-10-01 | Active 1.1.0 | `--json` keeps this matrix and closes the menu |

**Last Updated**: 2026-10-01
**Owner**: VideoSpeed project maintainers
**Alignment**: Registry `docs/requirements/index.md`; CIAO (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
