**file**: docs/requirements/requirement-python-time-consuming-process.md
**Status**: Active (Version 1.1.0)
**Area**: python
**Key**: `requirement-python-time-consuming-process`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

# Requirement: python-time-consuming-process

## 1. Purpose

VideoSpeed has one time-consuming process: the FFmpeg child started by `Encoder.run_ffmpeg`. The parent waits in the foreground until that child exits. While it waits, the text screen and a plain terminal show one flashing line: a bullet, then the words `please wait for time consuming process`. The bullet alternates between ● and ○ once every half second. That half second is the flash interval. It does not stop the child. The long step is the speed encode, and it runs only when the length is not 100%. A boomerang reverse is a second long child of the same runner. Cut is the same kind of child and uses a faster preset. Cut order, filters, presets, temps, and publish stay on `requirement-video-ffmpeg-pipeline`. Control-C during the wait stays on `requirement-python-graceful-exit`. The status logger stays on `requirement-python-cli-logging`. This version names no timeout seconds that stop the child.

### 1.1 Human-facing

**In one sentence:** While FFmpeg runs, you see one flashing bullet and the words `please wait for time consuming process`, and the long wait is the speed change that runs only when you did not ask for 100% length.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person who started an edit | The menu keeps one line, `● please wait for time consuming process`, and the bullet flips to ○ and back |
| The other role | The FFmpeg child | It is the only long external process. The parent does not continue until it exits |
| Not this file | The encode recipe, the cancel question, and the dated status file | Filters and the 100% skip stay on `requirement-video-ffmpeg-pipeline`. Control-C stays on `requirement-python-graceful-exit` |

| Includes | Excludes |
|----------|----------|
| Which child is the time-consuming process; the parent waits in the foreground; the flashing wait line; the half-second flash interval | The filter graph; publish; the `Exit? (y/n)` question; a timeout that stops the child; pip install and pip upgrade; the one-second menu clock |

| Surface | What you open | What for |
|---------|---------------|----------|
| `video-speed` | console script | An edit that starts FFmpeg |
| `src/VideoSpeed/encoder.py` | `Encoder.run_ffmpeg` | The foreground wait and the flashing line |
| Text screen during an edit | one body line | `please wait for time consuming process` for the whole wait |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Ask for a length other than 100% | Cut runs first. Then the speed encode runs with the medium preset. The parent waits on that child before the file is saved. That speed encode is the long step. The bullet keeps flashing on the one wait line. | `video-speed --file clip.mp4 --start 0 --end 5 --percent 50` |
| Leave the length at 100% and leave boomerang off | The medium speed child does not start. The cut is the file that is saved. You still wait on the cut child, and that child is the faster preset. The same wait line flashes during that cut. | `video-speed --file clip.mp4 --start 0 --end 5` |
| Turn boomerang on | After the forward clip, a reverse child runs. That reverse is a second long wait on the same runner. The same wait line flashes for that child too. | `video-speed --file clip.mp4 --start 0 --end 5 --percent 50 --boomerang` |

## 2. Core Rules (Mandatory)

### 2.0 Which process

1. **MUST** treat the external `ffmpeg` child started by `Encoder.run_ffmpeg` as the time-consuming process.  
2. **MUST NOT** treat these as that process: the one-second menu clock, the OpenCV duration probe, `list-mp4`, the about page, and the pip children of class `SelfManage` (`self-install`, `version-check`, `self-update`, `self-uninstall`). Those pip children can block. They stay on `requirement-python-cli-interface`.  
3. The children of this process are the cut, the speed encode when the length is not 100%, the boomerang reverse, and the boomerang concat. Order, filters, presets, temps, `-nostdin`, and publish stay on `requirement-video-ffmpeg-pipeline`. This file names which child is the long one.  
4. The long child **MUST** be `Encoder.speed_change`. The pipeline requirement names that encode as libx264 preset `medium`. It **MUST** run only when the length is not 100%.  
5. `Encoder.add_boomerang` starts a reverse child on the same runner. That reverse is a second long child. The concat that follows is a stream copy on the same runner. It is this process, and it is not the medium re-encode.  
6. `Encoder.cut_clip` is this process. The pipeline requirement names that encode as preset `ultrafast`. It is shorter than the medium re-encode.  
7. At 100% length with boomerang off, the medium child **MUST NOT** start. The skip and the publish of the cut stay on `requirement-video-ffmpeg-pipeline`. This file does not restate the filter graph.

### 2.1 The wait

8. The parent **MUST** wait in the foreground until that child exits. The call is `subprocess.Popen`. The parent **MUST** poll with `Popen.communicate` and the flash interval below. **MUST NOT** start a thread for this wait or for the flash. The ship unit creates no threads.  
9. The flash interval **MUST** be one half second (`0.5`). `Popen.communicate` receives that interval. When `subprocess.TimeoutExpired` is raised, the parent **MUST** toggle the bullet and poll again. That exception **MUST NOT** kill the child and **MUST NOT** end the wait. This version names no timeout seconds that stop the child. `requirement-python-graceful-exit` **MUST NOT** copy a kill-timeout number from this file. `requirement-python-cli-logging` does not name one.  
10. The child's stdin **MUST** be discarded (`DEVNULL`). The child's stdout and stderr **MUST** be captured so the flashing line stays readable and so FFmpeg text stays off a `--json` object. The `-nostdin` flag stays on `requirement-video-ffmpeg-pipeline`.  
11. On an open text screen, the progress line **MUST** be three spaces, then one bullet, then one space, then the words `please wait for time consuming process`. The first bullet **MUST** be ● (U+25CF). Each flash interval the bullet **MUST** alternate with ○ (U+25CB). Both bullets are Ambiguous and count as one display column. The full command **MUST NOT** replace that line. The screen **MUST** keep a single wait line: a later wait line replaces the previous wait line, and a later step line replaces that wait line. A flash **MUST NOT** append another body line.  
12. With no text screen and without `--json`, the same line **MUST** be rewritten in place. The parent writes a carriage return and then the line. When the child exits, that line ends so the next line starts after it. The full command **MUST NOT** be that line.  
13. With `--json`, the progress line **MUST NOT** be written. The child still runs, and the parent still polls until the child exits. The one JSON object stays on `requirement-python-json-output`.  
14. After the child, a text screen **MUST** be restored by `Encoder._restore_text_screen` when a screen is active. The box pixels stay on `requirement-python-tui`.  
15. Publish stays `FileStage.promote_file`. This file does not publish and does not name a second publish call.  
16. Control-C during the wait stays on `requirement-python-graceful-exit`. This file does not ask `Exit? (y/n)` and does not return 130. If the wait is interrupted by an exception other than the flash interval expiring, the parent **MUST** stop that child and **MUST** let the exception propagate. That stop is the child stop `subprocess.run` already performed. It is not the exit question.  
17. A non-zero FFmpeg exit stays on `requirement-python-error-handling`. A kill timeout, when a later version of this file names one, is not that failure. The flash interval is not that failure.  
18. No new class owns this wait. `Encoder.run_ffmpeg` is the wait. `EditWalk.place_job_line` only chooses whether the latest line replaces the wait line. The site that needs an object still writes `ClassName(...)`. A function or a method whose job is to instantiate a class is not how this wait is built.  
19. Actor / role / subject / approver: **considered**. No dest machine. No approver. The table stays on `requirement-class-software-dev`. This file does not add an actor requirement.

### 2.2 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| **Process** | The `ffmpeg` child inside `Encoder.run_ffmpeg` in `src/VideoSpeed/encoder.py` |
| **Long step** | `Encoder.speed_change` when the length is not 100%. Pipeline preset `medium` |
| **Second long step** | Boomerang reverse inside `Encoder.add_boomerang`, only when boomerang is on |
| **Shorter step of the same process** | `Encoder.cut_clip`. Pipeline preset `ultrafast` |
| **Not started at 100% with boomerang off** | `speed_change`. The cut is published. Owned by `requirement-video-ffmpeg-pipeline` |
| **Wait** | `subprocess.Popen`, then `communicate` with the flash interval. No thread |
| **Flash interval** | `0.5` seconds. `Encoder.FLASH_SECONDS`. Not a kill timeout |
| **Wait words** | `please wait for time consuming process`. `Encoder.WAIT_PHRASE` |
| **Bullets** | ● `Encoder.WAIT_MARK_ON` (U+25CF), then ○ `Encoder.WAIT_MARK_OFF` (U+25CB) |
| **Text screen line** | `   ● please wait for time consuming process`, then the same line with ○. One body line, replaced in place by `EditWalk.place_job_line` |
| **Plain terminal line** | The same words, rewritten with a carriage return |
| **`--json`** | No progress line. Pipes captured. Parent still polls |
| **Stdin** | `subprocess.DEVNULL`. Stdout and stderr are pipes |
| **Screen restore** | `Encoder._restore_text_screen` calls `curses.reset_prog_mode` when a text screen is active |
| **Kill timeout seconds** | None in version 1.1.0 |
| **Not this process** | Menu clock, OpenCV probe, `list-mp4`, about, and the pip verbs on class `SelfManage` |
| **Proof** | `TP-TIME-01` through `TP-TIME-05` have. `./tests/run.sh` on 2026-10-05: 103 tests, OK, skipped=1 |

### 2.3 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution** (https://github.com/cloudgen/ciao): the operator can see that a long child is still running, and a cancel stays a different requirement.  
- **Principle 2 – Intentional** (https://github.com/cloudgen/ciao): one process is named. The medium speed encode is the long step. The flash interval is named. A second-count that stops the child is not invented here.  
- **Principle 5 – SSOT** (https://github.com/cloudgen/ciao): encode order stays on the pipeline requirement. This file owns the wait and the flashing line.  
- **Principle 16 – Interactive** (https://github.com/cloudgen/ciao): the text screen keeps one short line for the whole wait. `--json` does not print that line and does not hang for a question.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, this child still runs as this login. **This requirement:** do not use admin privilege, `sudo`, or a system package manager to start FFmpeg or to wait for it. Do not create a dedicated system user for the encode.

## Sample code

This is the live wait. The flash interval is not a `timeout` that stops the child. `EditWalk.place_job_line` replaces the one wait line on the text screen.

```python
mark = self.WAIT_MARK_ON
self._show_wait(mark)
proc = subprocess.Popen(
    cmd,
    stdin=subprocess.DEVNULL,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
while True:
    try:
        _stdout, stderr = proc.communicate(timeout=self.FLASH_SECONDS)
        break
    except subprocess.TimeoutExpired:
        mark = self.WAIT_MARK_OFF if mark == self.WAIT_MARK_ON else self.WAIT_MARK_ON
        self._show_wait(mark)
```

`_show_wait` writes nothing when `--json` is set. On a text screen it passes `   ● please wait for time consuming process` (and then the ○ line) to the message sink. On a plain terminal it writes a carriage return and that same line. An exception other than `TimeoutExpired` stops the child and propagates. The speed encode is still the long child, and it still runs only when the length is not 100%.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Name the child the operator is stuck on. Show one flashing line. Do not treat a clock tick or a pip verb as that child.  
- **Intentional:** The medium speed encode is the long step. 100% length does not start it. The flash interval is half a second.  
- **Anti-fragile:** The parent waits in the foreground. A later kill-timeout has one home. A flash does not stack lines.  
- **Over-protect:** Do not invent a timeout that stops the child. Do not move the encode recipe or the Control-C question into this file. Do not start a thread to flip the bullet.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

1. Move cut order, filters, presets, temps, `-nostdin`, or publish into this file.  
2. Name a timeout that stops the child in this version, or put that number on `requirement-python-graceful-exit` or `requirement-python-cli-logging`.  
3. Treat the half-second flash interval as that timeout, or kill the child because `TimeoutExpired` fired.  
4. Start a thread for this wait or for the flash.  
5. Treat the menu clock, the OpenCV probe, `list-mp4`, the about page, or a pip lifecycle verb as this process.  
6. Publish from this file, or replace `FileStage.promote_file`.  
7. Treat Control-C as a finished graceful exit, ask `Exit? (y/n)` from this file, or return 130 from this file.  
8. Replace the wait phrase on the text screen with the full command, or append a new body line for each flash.  
9. Print the progress line on `--json` stdout.  
10. Claim `TP-TIME-01` through `TP-TIME-05` have before the suite asserts them.  
11. Add a class whose job is this wait, or a function or a method whose job is to instantiate a class for this wait.  
12. Use admin privilege or `sudo` to start or wait on the child.  
13. Cite templates or skills as the product-source authority for this wait.

**Violating this rule is a wait-identity regression.**

## 5. Design-time verification

| TP-ID | Case | Status | Map |
|-------|------|--------|-----|
| `TP-TIME-01` | On a text screen, `Encoder.run_ffmpeg` shows `   ● please wait for time consuming process` and then the ○ line on the flash interval `0.5`. One wait line is replaced in place. `Popen` uses stdin `DEVNULL` and captured pipes. `TimeoutExpired` does not kill the child. No thread is started | have | `tests/test_time.py` · `reviews/test-plan.md` |
| `TP-TIME-02` | With no text screen and without `--json`, the same line is rewritten in place and both bullets appear. With `--json`, no progress line is written and the parent still polls until the child exits | have | `tests/test_time.py` · `reviews/test-plan.md` |
| `TP-TIME-03` | Length 100% and boomerang off does not call `speed_change`. The medium child does not start | have | `tests/test_time.py` · `reviews/test-plan.md` |
| `TP-TIME-04` | A length other than 100% calls `speed_change` after the cut. That command uses preset `medium`. The parent returns from that child before publish | have | `tests/test_time.py` · `reviews/test-plan.md` |
| `TP-TIME-05` | An exception other than the flash interval stops the child and propagates. The method does not return 130 and does not ask `Exit?` | have | `tests/test_time.py` · `reviews/test-plan.md` |

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`

## 6. Related artifacts (versioned surface only)

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-video-ffmpeg-pipeline.md` | Encode order, presets, `-nostdin`, and publish |
| `docs/requirements/requirement-python-graceful-exit.md` | Control-C during this wait. This file names no kill timeout |
| `docs/requirements/requirement-python-cli-logging.md` | The one status logger. This file does not add a logger line |
| `docs/requirements/requirement-python-error-handling.md` | A non-zero FFmpeg exit |
| `docs/requirements/requirement-python-json-output.md` | The one JSON object. No progress line on that stream |
| `docs/requirements/requirement-python-tui.md` | The text screen. The one-second clock is not this process |
| `docs/requirements/requirement-python-cli-interface.md` | Pip lifecycle children. Not this process |
| `docs/requirements/requirement-python-oop.md` | Class `Encoder`. No new class for this wait |
| `docs/requirements/requirement-class-software-dev.md` | Class residual pointer |
| `src/VideoSpeed/encoder.py` | `Encoder.run_ffmpeg` |
| `src/VideoSpeed/edit_walk.py` | `EditWalk.place_job_line` |
| `tests/test_time.py` | `TP-TIME-01` through `TP-TIME-05` |
| `reviews/test-plan.md` | TP map |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-05 | Active 1.0.0 | The time-consuming process is the FFmpeg child in `Encoder.run_ffmpeg`. The long step is `speed_change` when the length is not 100%. No timeout seconds. `TP-TIME-01` through `TP-TIME-04` are todo. The wait already blocked. This version adds the law and a citation |
| 2026-10-05 | Active 1.1.0 | The text screen and a plain terminal show one flashing line: a bullet and `please wait for time consuming process`. The bullet alternates ● and ○ every half second. That interval does not stop the child. The parent polls with `Popen.communicate`. `--json` stays silent. `TP-TIME-01` through `TP-TIME-05` have. `./tests/run.sh`: 103 tests, OK, skipped=1 |

---

**Last Updated**: 2026-10-05  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
