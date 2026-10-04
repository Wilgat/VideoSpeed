**file**: docs/requirements/requirement-python-error-handling.md  
**Status**: Active (Version 1.2.5)  
**Area**: python  
**Key**: `requirement-python-error-handling`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define how VideoSpeed **detects, reports, and recovers from errors** during interactive sessions, non-interactive jobs, and FFmpeg processing without destroying the user’s source media.

### 1.1 Human-facing

**In one sentence:** When something is wrong (no file, bad time range, missing FFmpeg), VideoSpeed must say so on the console and leave your original MP4 untouched.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person whose clip must not be deleted | Invalid `--start`/`--end` prints an error and does not encode |
| The other role | CLI + pipeline | Who prompts vs who runs FFmpeg |
| Not this file | Feature catalog | Domain file |

| Includes | Excludes |
|----------|----------|
| Fail-closed categories; source-safe cleanup; console errors | Silent `pass`; deleting the source |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/VideoSpeed/cli.py` | ship unit | live messages |
| `video-speed --file missing.mp4 --start 0 --end 1` | command | “File not found” + Next |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Give a bad range | The program must not start FFmpeg. | `video-speed --file clip.mp4 --start 9 --end 1` |

---

## 2. Core Rules (Mandatory)

### 2.1 Fail-closed principles

1. **MUST NOT** silently ignore FFmpeg non-zero exits.  
2. **MUST NOT** treat invalid user input as success.  
3. **MUST** prefer clear human-readable messages over stack traces for expected user mistakes.  
4. **MUST** leave the source video intact on all failure paths.  
4a. **MUST NOT** classify Control-C / SIGINT as an FFmpeg non-zero exit or as `CalledProcessError`. Exit 130, the confirm question, stopping the child, and not publishing belong to `requirement-python-graceful-exit`. A declined confirm is not a failure sentence in this file. A real FFmpeg failure stays here.

### 2.2 Required error categories

| Category | Detection | Required action |
|----------|-----------|-----------------|
| No MP4 in folder | Discovery returns empty | Message + exit session step |
| Invalid selection index | Out of range | Fail closed; re-prompt or abort with message |
| Invalid cut range | not `0 <= start < end <= duration` | Message + re-prompt (do not encode) |
| Unreadable media / zero duration | OpenCV probe fails or duration ≤ 0 | Clear error; do not encode |
| FFmpeg missing | subprocess cannot find binary | Actionable message: install FFmpeg |
| FFmpeg failure | non-zero exit / CalledProcessError | Report failure; cleanup temps. Exit 130 is not this row |
| Control-C | SIGINT, including on the text screen | Not this table. The question and exit 130 are `requirement-python-graceful-exit` |
| Temp cleanup failure | unlink errors | Best-effort; do not mask original error |

### 2.3 Cleanup on failure

5. **MUST** attempt to remove intermediate temp files after failed or successful jobs.  
6. **MUST NOT** delete the final user output path solely because a later optional step failed, unless the partial final is known corrupt — then document and remove only that corrupt final.  
7. **MUST NOT** delete the source media as cleanup.

### 2.4 Logging

8. **MUST** print a user-visible failure reason on the console (interactive and batch).  
9. Durable system-status copies of those facts **MUST** follow `requirement-python-cli-logging` (`log_message` at `ERROR` or `FATAL`). This file still owns the console sentence.  
10. **MUST NOT** log secrets (none expected in this product).

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **FFmpeg runner** | `run_ffmpeg` uses `subprocess.run(..., check=True)` |
| **Invalid range** | Re-ask on the walk; non-zero on the job. Mode file owns which |
| **No MP4** | Menu return on the walk; non-zero on `--folder` |
| **Temp cleanup** | `finally` unlinks cut/speed temps |
| **Logging** | Console sentence stays here. Durable status file is `requirement-python-cli-logging` |
| **Control-C** | Not an FFmpeg failure. The question and exit 130 are `requirement-python-graceful-exit` |
| **Non-interactive** | `requirement-python-interactive-vs-noninteractive` |
| **JSON** | The same failure sentence is `error` in `requirement-python-json-output`. It is not a second stdout line |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution**: Fail closed on encode errors.  
- **Principle 11 – Temps**: Cleanup without destroying source.  
- **Principle 12 – Traceability**: User-visible failure reasons.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, a failure is still reported at this login and the source file stays. **This requirement:** do not use admin privilege, `sudo`, or a system package manager to clean up a failed encode or to stop a child. Control-C stays `requirement-python-graceful-exit`.

---

## Sample code

`StateLogic` is not this file. The console sentence is.

```python
def fail(sentence, next_step=None):
    print(sentence, file=sys.stderr)
    if next_step:
        print(next_step, file=sys.stderr)
    return 1
```

```text
ERROR: ffmpeg is not on PATH.
Next: install FFmpeg.
```

Control-C is not this function. Exit 130 stays on `requirement-python-graceful-exit`.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Invalid range never reaches FFmpeg.  
- **Intentional:** Category table is product law.  
- **Anti-fragile:** Cleanup best-effort.  
- **Over-protect:** Source media is sacred.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Swallow FFmpeg errors without user-visible failure.  
2. Delete source media on error.  
3. Encode after invalid range validation failure.  
4. Replace clear messages with silent `pass`.  
5. Log credentials or API tokens (none should exist).  
6. Treat Control-C as an FFmpeg failure exit. That stop is `requirement-python-graceful-exit`.

**Violating this rule is a critical safety regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Invalid range does not encode |
| AC-2 | FFmpeg failure surfaces error |
| AC-3 | Source file remains after failure |
| AC-4 | Temps cleaned best-effort |
| AC-5 | Empty MP4 list exits with message |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-video-ffmpeg-pipeline` | Encode failures |
| `requirement-python-cli-interface` | Prompt re-entry |
| `requirement-runtime-prerequisites` | Missing FFmpeg |
| `requirement-python-cli-logging` | Durable status copy of a failure |
| `requirement-python-graceful-exit` | Control-C confirm and exit 130. Not an FFmpeg failure |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| TP-ERR-01 | `tests/test_errors.py` | have | Invalid range helper |
| TP-ERR-02 | `tests/test_errors.py` | have | Percent bounds |
| TP-ERR-03 | — | todo | Source intact after ffmpeg fail (needs encode fixture) |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial error-handling law |
| 2026-08-19 | Active 1.1.0 | Console-only errors; drop ChronicleLogger; §1.1 |
| 2026-10-01 | Active 1.2.0 | Console sentence stays; durable copy points at `requirement-python-cli-logging` |
| 2026-10-01 | Active 1.2.1 | Walk versus job exits point at the mode requirement |
| 2026-10-01 | Active 1.2.2 | `--json` repeats the failure sentence inside the one object |
| 2026-10-01 | Active 1.2.3 | Control-C during a long child is not an FFmpeg failure. Exit 130 is `requirement-python-graceful-exit` |
| 2026-10-02 | Active 1.2.4 | A Control-C confirm, including a declined answer, is not a failure sentence. The question stays on `requirement-python-graceful-exit` |
| 2026-10-02 | Active 1.2.5 | Sample code is the operator sentence. `StateLogic` stays off this file |

---

**Last Updated**: 2026-10-02  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
