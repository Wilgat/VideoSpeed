**file**: docs/requirements/requirement-python-graceful-exit.md
**Status**: Active (Version 1.1.3)
**Area**: python
**Key**: `requirement-python-graceful-exit`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

# Requirement: python-graceful-exit

## 1. Purpose

When the operator presses Control-C, VideoSpeed asks whether to exit, records that decision on the one status logger, and leaves with status 130 only when the answer is yes or when no question can be shown. A press during an FFmpeg wait stops that child and does not publish before the question. A press while the text menu is waiting for a key does the same question and does not print a traceback. The menu row Exit stays a menu control. A real FFmpeg failure stays owned by `requirement-python-error-handling`. The logger and the component stay owned by `requirement-python-cli-logging`. The encode order and the publish call stay owned by `requirement-video-ffmpeg-pipeline`. The box pixels stay owned by `requirement-python-tui`. Which FFmpeg child is the time-consuming process, and the flashing line while the parent waits, stay owned by `requirement-python-time-consuming-process`. This file does not name a timeout. Version 1.1.0 of that file names a half-second flash and names no timeout that stops the child.

### 1.1 Human-facing

**In one sentence:** If you press Control-C, VideoSpeed asks `Exit? (y/n)` before it leaves, writes that decision into the daily status file, and a yes ends the process with status 130.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person who pressed Control-C | On the menu, `n` keeps the board. `y` leaves |
| The other role | The FFmpeg child, when one is running | It is stopped before the question. It does not keep encoding while you decide |
| Not this file | The menu row Exit, the failure sentence, and the encode recipe | Row 9 leaves without this question. A bad FFmpeg exit is `requirement-python-error-handling`. Cut, speed, and boomerang stay on `requirement-video-ffmpeg-pipeline` |

| Includes | Excludes |
|----------|----------|
| The question `Exit? (y/n)`, the exit line on the one status logger, stop-and-do-not-publish when a child is running, restore the terminal, return 130 when leaving because of Control-C | A timeout number; treating Control-C as success; treating Control-C as an FFmpeg failure; the menu row Exit; a second logger |

| Surface | What you open | What for |
|---------|---------------|----------|
| `video-speed` | console script | Press Control-C on the menu or during an encode |
| `src/VideoSpeed/menu_session.py` | key wait | The question while the text screen is open |
| `src/VideoSpeed/encoder.py` | `Encoder.run_ffmpeg` | Stop the child before the question |
| Resolved daily log | status file | The exit line after the decision |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Press Control-C on the menu | The bottom box asks `Exit? (y/n)`. Yes leaves with status 130 and no traceback. No, or Enter, stays on the same board. The daily file records which one you chose. | `video-speed` |
| Press Control-C during an encode on that screen | FFmpeg stops first. The unfinished file is not saved. Then the same question appears. No returns you to the screen. The encode does not resume. | `video-speed` |
| Press Control-C with no screen | There is no question and no hang. The process ends with status 130, and the daily file records that the question was not available. | `video-speed edit --file clip.mp4 --start 0 --end 5` |

## 2. Core Rules (Mandatory)

### 2.0 When this law applies

1. **MUST** apply when Control-C (SIGINT) arrives. That includes `KeyboardInterrupt` and a key read that returns ETX (byte 3).  
2. **MUST** ask when a text screen is already open, except during child cleanup as rule 12 states.  
3. **MUST NOT** ask when no text screen is open, when `--json` is set, or on the non-interactive job path. Those runs **MUST NOT** hang.  
4. **MUST NOT** call `isatty` inside the question. The open text screen is the gate, from `requirement-python-interactive-vs-noninteractive`.  
5. **MUST NOT** treat the text-menu Exit row as this question. That row leaves without asking and returns 0.  
6. **MUST NOT** apply the stop to a job that has already published.  
7. **MUST NOT** use this file to name a timeout. A timeout, when one exists, is named by `requirement-python-time-consuming-process`. Version 1.1.0 of that file names a half-second flash and names no timeout that stops the child. The flash interval is not this file's number.  
8. Actor / role / subject / approver: **considered**. No dest machine. No approver. The table stays on `requirement-class-software-dev`. This file does not add an actor requirement.

### 2.1 The question

9. The question words **MUST** be `Exit? (y/n)`. While a text screen is open, class `MenuPainter` draws that line on the only inner line of the bottom box. The frame stays. `requirement-python-tui` owns the box. This file owns the words and the decision.  
10. `y` and `yes` confirm, in any letter case. `n`, `no`, Enter, and Esc decline, in any letter case. Any other answer **MUST** show the same question again and **MUST NOT** exit.  
11. A clock redraw **MUST NOT** count as an answer and **MUST NOT** clear the question.  
12. A second Control-C while the question is showing **MUST** confirm the exit. It **MUST NOT** ask again and **MUST NOT** print a traceback. A second Control-C during child cleanup **MUST NOT** show the question. It **MUST** kill the child group and **MUST** still return 130.  
13. Declining **MUST** leave the process running on the same screen. It **MUST NOT** return 0 for this press. It **MUST NOT** resume an encode that this press already stopped.

### 2.2 Stop, do not publish, exit 130

14. Before the question, or before a 130 return when no question is shown, every child this process started that is still running **MUST** be stopped. The child **MUST** be started in its own session so the parent can signal the child group. The stop **MUST NOT** signal the parent group again.  
15. The FFmpeg child's stdin **MUST** be discarded (`DEVNULL`). The ignore-stdin flag on the FFmpeg argument list stays owned by `requirement-video-ffmpeg-pipeline`.  
16. On Control-C during an FFmpeg wait, the parent **MUST** stop the child group, **MUST NOT** call the publish function, and **MUST** discard the unfinished temp. The source file **MUST** stay intact. The temp path **MUST NOT** be shown as the finished file.  
17. When a text screen is active, the parent **MUST** restore it on the way out of a confirmed exit and of an exit with no question, including `curses` program mode. Declining stays inside the screen and repaints.  
18. A confirmed exit, a second Control-C during the question, and a Control-C with no question **MUST** return 130. There **MUST** be no traceback.  
19. A top-level handler in `main` **MAY** return 130 only after every live child is already stopped and the exit line is already written. It **MUST NOT** be the only handler. It **MUST NOT** ask a second question. It **MUST NOT** leave a child running. It **MUST NOT** print a traceback.  
20. **MUST NOT** catch Control-C and continue the encode as success. **MUST NOT** return 0 on a confirmed Control-C. Declining is not that success.  
21. **MUST NOT** classify this stop as an FFmpeg non-zero exit or as `CalledProcessError`. That failure path stays `requirement-python-error-handling`. A declined confirm is not a failure sentence.

### 2.3 Exit line

22. The decision **MUST** be `log_message` on the one ChronicleLogger from `main`. **MUST NOT** use `print`. **MUST NOT** construct a second logger. The call **MUST NOT** sit inside `isDebug()`.  
23. The component comes from `requirement-python-cli-logging`. A text screen uses `menu`. No text screen uses `main`. The interrupted-wait line uses `ffmpeg` and is separate from the exit line.  
24. The exit message **MUST** be one of these, and no other wording:

| Decision | Level | Message |
|----------|-------|---------|
| Confirmed, including a second Control-C on the question | `WARNING` | `exit reason=control-c confirmed=yes code=130` |
| Declined | `INFO` | `exit reason=control-c confirmed=no` |
| No question (`--json`, no text screen, or a second Control-C during cleanup) | `WARNING` | `exit reason=control-c confirmed=unavailable code=130` |

25. When an FFmpeg child was stopped, the same logger **MUST** also record `wait interrupted` at level `WARNING` with component `ffmpeg`, before the question. That call follows the same quiet rule.  
26. Quiet from `requirement-python-cli-logging` still applies. The text screen and `--json` **MUST NOT** mirror these lines onto that console. The daily file still receives them. The question itself is the box, not a mirrored log line. `--json` stdout stays one object.

### 2.4 What this file does not change

27. A job whose length percent is 100 still publishes the cut and skips the speed encode when that child finishes. That finish path is `requirement-video-ffmpeg-pipeline`. An interrupt before publish **MUST NOT** call publish, and it **MUST NOT** remove the finished-job rule.  
28. Publish, when a finished child is published, stays `FileStage.promote_file` (`shutil.move`). This file does not replace that call.  
29. No new class owns this question. `MenuSession` asks while the screen is open. `Encoder.run_ffmpeg` stops the child. `main` is only the backstop in rule 19. The site that needs an object still writes `ClassName(...)`. A function or a method whose job is to instantiate a class is not how this question is built.

### 2.5 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| **Question** | `Exit? (y/n)` in the bottom box while a text screen is open |
| **Confirm** | `y` or `yes`. A second Control-C on the question is also yes |
| **Decline** | `n`, `no`, Enter, or Esc. The process stays. The encode does not resume |
| **Key wait** | `MenuSession._wait_key` in `src/VideoSpeed/menu_session.py`. Today `screen.getch()` does not catch `KeyboardInterrupt`. `curses.wrapper` then prints the traceback. This law is not in the ship unit yet |
| **FFmpeg wait** | `Encoder.run_ffmpeg` in `src/VideoSpeed/encoder.py`. Today `subprocess.Popen` and `communicate` with a half-second flash. An interrupt stops the child and propagates. No `Exit? (y/n)` handler. No `start_new_session`. No return 130 |
| **Backstop** | `main` in `src/VideoSpeed/cli.py`. Not the only handler |
| **Ignore-stdin flag** | `-nostdin` on every FFmpeg command. Owned by `requirement-video-ffmpeg-pipeline` |
| **Publish** | `FileStage.promote_file` → `shutil.move`. Not called on this interrupt |
| **Unfinished temp** | Discarded when an encode child is stopped. The source file stays |
| **Logger** | The one ChronicleLogger from `main`. Exit line component `menu` or `main`. Interrupted-wait component `ffmpeg` |
| **Screen** | The box stays up for the question. A confirmed exit restores the terminal. `_restore_text_screen` calls `curses.reset_prog_mode` when a text screen is active |
| **Exit** | 130 when leaving because of Control-C. Row 9 Exit still returns 0 and does not ask |
| **100% length** | A finished 100% job still publishes the cut and skips the speed encode. Interrupt before that publish does not publish |
| **Timeout** | This file names none. `requirement-python-time-consuming-process` 1.1.0 names a half-second flash and names no kill timeout |
| **Proof** | `TP-EXIT-01` through `TP-EXIT-07` are todo. The program was not changed for this version |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution** (https://github.com/cloudgen/ciao): a cancel must not leave a child running, present a temp as the result, or dump a traceback over the menu.  
- **Principle 2 – Intentional** (https://github.com/cloudgen/ciao): the question is one yes or no, and 130 is the named leave. An FFmpeg failure stays a different requirement.  
- **Principle 16 – Interactive** (https://github.com/cloudgen/ciao): a person at the open screen can decline. A run with no screen does not wait.  
- **Principle 11 – Temps** (https://github.com/cloudgen/ciao): the unfinished temp is discarded. The source stays.  
- **Principle 5 – SSOT of output** (https://github.com/cloudgen/ciao): the exit line and the interrupted line use the one status logger.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, Control-C is this login's own signal. **This requirement:** do not use admin privilege, `sudo`, or a system package manager to stop the child or to ask the question. Do not create a dedicated system user for the stop.

## Sample code

This is the shape the law requires. The ship unit does not contain it yet. `TP-EXIT-01` through `TP-EXIT-07` stay todo.

```python
logger.log_message("wait interrupted", level="WARNING", component="ffmpeg")
logger.log_message(
    "exit reason=control-c confirmed=yes code=130",
    level="WARNING",
    component="menu",
)
return 130
```

A declined answer uses `exit reason=control-c confirmed=no` at `INFO` and does not return 130. No text screen uses `confirmed=unavailable` and component `main`. The question words are `Exit? (y/n)`.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Stop a live child before the question. Do not publish on the way out.  
- **Intentional:** `Exit? (y/n)` is this question. 130 is the leave. Row 9 is not this question.  
- **Anti-fragile:** A second Control-C still ends at 130, with the child gone and no traceback.  
- **Over-protect:** Do not undo a finished 100% publish-the-cut path, do not invent a timeout here, and do not ask when no screen is open.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

1. Publish, or call `FileStage.promote_file`, on this Control-C path.  
2. Return 0 for a confirmed Control-C, or resume the encode after the child was stopped.  
3. Leave a traceback, or leave the child running.  
4. Treat Control-C as an FFmpeg `CalledProcessError`, as exit 1, or as a failure sentence.  
5. Name a timeout in this file.  
6. Remove the finished 100% rule that publishes the cut and skips the speed encode.  
7. Quiet the daily file for the exit line or the interrupted line. The text screen and `--json` stay unmirrored.  
8. Skip the question while a text screen is open, or ask when no text screen is open, when `--json` is set, or on the non-interactive job.  
9. Hang waiting for an answer on those no-question runs.  
10. Treat row 9 Exit, or the one-second clock wait, as this question.  
11. Add a class whose job is to ask, or a function or a method whose job is to instantiate a class for this question.  
12. Claim `TP-EXIT-01` through `TP-EXIT-07` have before the suite asserts them.  
13. Cite templates or skills as the product-source authority for this stop.

**Violating this rule is a cancel-safety regression.**

## 5. Design-time verification

| TP-ID | Case | Status | Map |
|-------|------|--------|-----|
| `TP-EXIT-01` | Control-C during the child, with no text screen, stops the group, does not publish, the log contains `interrupted` and `exit reason=control-c confirmed=unavailable code=130`, the process exits 130, and there is no traceback | todo | `reviews/test-plan.md` |
| `TP-EXIT-02` | A second Control-C during cleanup still exits 130, the child is gone, and the question is not shown | todo | `reviews/test-plan.md` |
| `TP-EXIT-03` | Control-C on the open text menu draws `Exit? (y/n)`. `y` exits 130, the log contains `exit reason=control-c confirmed=yes code=130` with component `menu`, and there is no traceback | todo | `reviews/test-plan.md` |
| `TP-EXIT-04` | `n`, `no`, or Enter stays on the same board. The log contains `exit reason=control-c confirmed=no`. The process does not exit | todo | `reviews/test-plan.md` |
| `TP-EXIT-05` | Control-C during FFmpeg while the text screen is open stops the child and does not publish, then asks. `n` returns to the screen and does not publish. `y` exits 130 | todo | `reviews/test-plan.md` |
| `TP-EXIT-06` | A second Control-C while the question is showing exits 130, logs `confirmed=yes`, and does not print a traceback | todo | `reviews/test-plan.md` |
| `TP-EXIT-07` | `--json` and a non-interactive job do not ask and do not hang. Control-C exits 130 and logs `confirmed=unavailable` | todo | `reviews/test-plan.md` |

## 6. Related artifacts (versioned surface only)

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-python-cli-logging.md` | The one logger. Components `menu`, `main`, and `ffmpeg` |
| `docs/requirements/requirement-python-error-handling.md` | FFmpeg failure sentences. Not this 130 |
| `docs/requirements/requirement-python-tui.md` | The bottom box. Row 9 is not this question |
| `docs/requirements/requirement-python-interactive-vs-noninteractive.md` | The open screen is the gate. The question does not call `isatty` |
| `docs/requirements/requirement-video-ffmpeg-pipeline.md` | Encode order, `-nostdin`, and `promote_file` on a finished job |
| `docs/requirements/requirement-python-time-consuming-process.md` | The FFmpeg child and the flashing wait line. That file names a half-second flash in 1.1.0 and names no kill timeout |
| `docs/requirements/requirement-python-coding-style.md` | Points here for Control-C |
| `docs/requirements/requirement-class-software-dev.md` | Class residual pointer |
| `src/VideoSpeed/menu_session.py` | Key wait. Law not implemented yet |
| `src/VideoSpeed/encoder.py` | FFmpeg wait. Law not implemented yet |
| `reviews/test-plan.md` | TP map |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-01 | Active 1.0.0 | Control-C during the FFmpeg wait stops the child, does not publish, and returns 130. Proofs todo. The ship unit does not catch `KeyboardInterrupt` yet. This file names no timeout |
| 2026-10-02 | Active 1.1.0 | Control-C on an open text screen asks `Exit? (y/n)` and logs the decision. Yes, or no screen, exits 130. A live child is stopped and not published before the question. `TP-EXIT-01` through `TP-EXIT-07` are todo. The program was not changed |
| 2026-10-02 | Active 1.1.1 | Sample code shows the exit line and the return 130. The program was not changed |
| 2026-10-05 | Active 1.1.2 | The blocking FFmpeg child points at `requirement-python-time-consuming-process`. This file still names no timeout. The program was not changed |
| 2026-10-05 | Active 1.1.3 | The peer wait is version 1.1.0: a half-second flash, and no kill timeout. This file still names no timeout and still does not ask `Exit?` from the ship unit. `TP-EXIT-01` through `TP-EXIT-07` stay todo |

---

**Last Updated**: 2026-10-05  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
