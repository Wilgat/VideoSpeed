**file**: docs/requirements/requirement-python-graceful-exit.md
**Status**: Active (Version 1.0.0)
**Area**: python
**Key**: `requirement-python-graceful-exit`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

# Requirement: python-graceful-exit

## 1. Purpose

When the operator presses Control-C while VideoSpeed is waiting on a long FFmpeg child, the program stops that child, does not publish the unfinished file, writes the interrupt on the one status logger, restores the text screen, and exits 130 with no traceback. A real FFmpeg failure stays owned by `requirement-python-error-handling`. The logger and the component stay owned by `requirement-python-cli-logging`. The encode order and the publish call stay owned by `requirement-video-ffmpeg-pipeline`. This file does not name a timeout.

### 1.1 Human-facing

**In one sentence:** If you press Control-C while VideoSpeed is waiting on FFmpeg, it stops that work, does not save a half-finished file, and the process ends with status 130.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person who pressed Control-C during an encode | The half-finished temp is not renamed onto your clip |
| The other role | The FFmpeg child | It is stopped with the parent. It does not keep running after you cancel |
| Not this file | The menu row Exit, the failure sentence, and the encode recipe | Exit on the text menu is a menu control. A bad FFmpeg exit is `requirement-python-error-handling`. Cut, speed, and boomerang stay on `requirement-video-ffmpeg-pipeline` |

| Includes | Excludes |
|----------|----------|
| Stop the child group, do not publish, discard the unfinished temp, log interrupted, restore the text screen, return 130 | A timeout number; treating Control-C as success; treating Control-C as an FFmpeg failure exit; the menu Exit row |

| Surface | What you open | What for |
|---------|---------------|----------|
| `video-speed` | console script | Press Control-C during a running encode |
| `src/VideoSpeed/encoder.py` | `Encoder.run_ffmpeg` | The wait this law covers |
| Resolved daily log | status file | The interrupted line after the process ends |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Cancel during the wait | The encoder child stops. Your original file stays. The unfinished temp is not presented as the result. The process status is 130, and there is no traceback. A second Control-C while cleanup runs still ends as 130. | `video-speed edit` |

## 2. Core Rules (Mandatory)

### 2.0 When this law applies

1. **MUST** apply when Control-C (SIGINT) arrives during the FFmpeg wait.  
2. **MUST NOT** apply the stop to a job that has already published.  
3. **MUST NOT** use this file to name a timeout. A timeout, when one exists, is named by the requirement that owns it.  
4. **MUST NOT** treat the text-menu Exit row as this stop. That row is a menu control.

### 2.1 Stop, do not publish, exit 130

5. The child **MUST** be started in its own session so the parent can signal the child group.  
6. The child's stdin **MUST** be discarded (`DEVNULL`). The ignore-stdin flag on the FFmpeg argument list stays owned by `requirement-video-ffmpeg-pipeline`.  
7. On SIGINT during the wait, the parent **MUST** stop the child group, **MUST NOT** call the publish function, and **MUST** discard the unfinished temp. The source file **MUST** stay intact.  
8. The interrupt **MUST** be `log_message` on the one ChronicleLogger. The component for that encode wait is `ffmpeg`, from `requirement-python-cli-logging`. The level is `WARNING`. The message **MUST** say the wait was interrupted. The call **MUST NOT** sit inside `isDebug()`. **MUST NOT** use `print`. **MUST NOT** construct a second logger.  
9. Quiet from `requirement-python-cli-logging` still applies. The text screen and `--json` **MUST NOT** mirror that line onto that console. The daily file still receives it.  
10. When a text screen is active, the parent **MUST** restore it (`curses` program mode) on the way out, including the interrupt path.  
11. The process **MUST** return 130. There **MUST** be no traceback.  
12. A second Control-C during cleanup **MUST** kill the child group and **MUST** still return 130.  
13. A top-level handler in `main` **MAY** return 130 only after the child is already stopped. It **MUST NOT** be the only handler, and it **MUST NOT** leave the child running.  
14. **MUST NOT** catch Control-C and continue as success. **MUST NOT** return 0 on this path.  
15. **MUST NOT** classify this stop as an FFmpeg non-zero exit or as `CalledProcessError`. That failure path stays `requirement-python-error-handling`.

### 2.2 What this file does not change

16. A job whose length percent is 100 still publishes the cut and skips the speed encode when that child finishes. That finish path is `requirement-video-ffmpeg-pipeline`. An interrupt before publish **MUST NOT** call publish, and it **MUST NOT** remove the finished-job rule.  
17. Publish, when a finished child is published, stays `FileStage.promote_file` (`shutil.move`). This file does not replace that call.

### 2.3 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| **Wait** | `Encoder.run_ffmpeg` in `src/VideoSpeed/encoder.py` |
| **Ship unit today** | `subprocess.run` with stdin `DEVNULL`. No `KeyboardInterrupt` handler. No `start_new_session`. This law is not in the ship unit yet |
| **Ignore-stdin flag** | `-nostdin` on every FFmpeg command. Owned by `requirement-video-ffmpeg-pipeline` |
| **Publish** | `FileStage.promote_file` → `shutil.move`. Not called on this interrupt |
| **Unfinished temp** | Discarded on this interrupt. The source file stays |
| **Logger** | The one ChronicleLogger from `main`. Component `ffmpeg`. Message records that the wait was interrupted |
| **Screen** | `_restore_text_screen` calls `curses.reset_prog_mode` when a text screen is active |
| **Exit** | 130. A second Control-C during cleanup still 130 |
| **100% length** | A finished 100% job still publishes the cut and skips the speed encode. Interrupt before that publish does not publish |
| **Timeout** | This file names none |
| **Proof** | `TP-EXIT-01` and `TP-EXIT-02` are todo |

### 2.4 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution** (https://github.com/cloudgen/ciao): a cancel must not leave a child running or present a temp as the result.  
- **Principle 2 – Intentional** (https://github.com/cloudgen/ciao): exit 130 is the named interrupt outcome, separate from an FFmpeg failure.  
- **Principle 11 – Temps** (https://github.com/cloudgen/ciao): the unfinished temp is discarded. The source stays.  
- **Principle 5 – SSOT of output** (https://github.com/cloudgen/ciao): the interrupted line uses the one status logger.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, Control-C is this login's own signal. **This requirement:** do not use admin privilege, `sudo`, or a system package manager to stop the child. Do not create a dedicated system user for the stop.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Stop the child group before returning. Do not publish on the way out.  
- **Intentional:** 130 is this outcome. An FFmpeg failure stays a different requirement.  
- **Anti-fragile:** A second Control-C during cleanup still ends at 130, with the child gone.  
- **Over-protect:** Do not undo a finished 100% publish-the-cut path, and do not invent a timeout here.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

1. Publish, or call `FileStage.promote_file`, on this Control-C path.  
2. Return 0, or continue the job, after Control-C.  
3. Leave a traceback, or leave the child running.  
4. Treat Control-C as an FFmpeg `CalledProcessError` or as exit 1.  
5. Name a timeout in this file.  
6. Remove the finished 100% rule that publishes the cut and skips the speed encode.  
7. Quiet the daily file for the interrupted line. The text screen and `--json` stay unmirrored.  
8. Claim `TP-EXIT-01` or `TP-EXIT-02` have before the suite asserts them.  
9. Cite templates or skills as the product-source authority for this stop.

**Violating this rule is a cancel-safety regression.**

## 5. Design-time verification

| TP-ID | Case | Status | Map |
|-------|------|--------|-----|
| `TP-EXIT-01` | Control-C during the child stops the group, does not publish, the log contains interrupted, the process exits 130, and there is no traceback | todo | `reviews/test-plan.md` |
| `TP-EXIT-02` | A second Control-C during cleanup still exits 130 and the child is gone | todo | `reviews/test-plan.md` |

## 6. Related artifacts (versioned surface only)

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-python-cli-logging.md` | The one logger and component `ffmpeg` |
| `docs/requirements/requirement-python-error-handling.md` | FFmpeg failure sentences. Not this 130 |
| `docs/requirements/requirement-video-ffmpeg-pipeline.md` | Encode order, `-nostdin`, and `promote_file` on a finished job |
| `docs/requirements/requirement-python-coding-style.md` | Points here for Control-C |
| `docs/requirements/requirement-class-software-dev.md` | Class residual pointer |
| `src/VideoSpeed/encoder.py` | Wait site. Law not implemented yet |
| `reviews/test-plan.md` | TP map |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-01 | Active 1.0.0 | Control-C during the FFmpeg wait stops the child, does not publish, and returns 130. Proofs todo. The ship unit does not catch `KeyboardInterrupt` yet. This file names no timeout |

---

**Last Updated**: 2026-10-01  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
