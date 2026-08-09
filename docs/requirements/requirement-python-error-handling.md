**file**: docs/requirements/requirement-python-error-handling.md  
**Status**: Active (Version 1.0.0)  
**Area**: python  
**Key**: `requirement-python-error-handling`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define how VideoSpeed **detects, reports, and recovers from errors** during interactive sessions and FFmpeg processing without destroying the user’s source media.

---

## 2. Core Rules (Mandatory)

### 2.1 Fail-closed principles

1. **MUST NOT** silently ignore FFmpeg non-zero exits.  
2. **MUST NOT** treat invalid user input as success.  
3. **MUST** prefer clear human-readable messages over stack traces for expected user mistakes.  
4. **MUST** leave the source video intact on all failure paths.

### 2.2 Required error categories

| Category | Detection | Required action |
|----------|-----------|-----------------|
| No MP4 in folder | Discovery returns empty | Message + exit session step |
| Invalid selection index | Out of range | Fail closed; re-prompt or abort with message |
| Invalid cut range | not `0 <= start < end <= duration` | Message + re-prompt (do not encode) |
| Unreadable media / zero duration | OpenCV probe fails or duration ≤ 0 | Clear error; do not encode |
| FFmpeg missing | subprocess cannot find binary | Actionable message: install FFmpeg |
| FFmpeg failure | non-zero exit / CalledProcessError | Report failure; cleanup temps |
| Temp cleanup failure | unlink errors | Best-effort; do not mask original error |

### 2.3 Cleanup on failure

5. **MUST** attempt to remove intermediate temp files after failed or successful jobs.  
6. **MUST NOT** delete the final user output path solely because a later optional step failed, unless the partial final is known corrupt — then document and remove only that corrupt final.  
7. **MUST NOT** delete the source media as cleanup.

### 2.4 Logging

8. **SHOULD** use ChronicleLogger for durable diagnostics when configured.  
9. **MUST** still print user-visible failure reason on the console for interactive sessions.  
10. **MUST NOT** log secrets (none expected in this product).

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **FFmpeg runner** | `run_ffmpeg` uses `subprocess.run(..., check=True)` |
| **Invalid range** | re-prompt loop in `main` |
| **No MP4** | print and return |
| **Temp cleanup** | `finally` unlinks cut/speed temps |
| **ChronicleLogger** | imported; full structured error routing is **aspirational gap** — console messages remain mandatory |
| **Non-interactive** | not fully specified; prompt-only UI may hang or fail if stdin closed — future improvement |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution**: Fail closed on encode errors.  
- **Principle 11 – Temps**: Cleanup without destroying source.  
- **Principle 12 – Traceability**: User-visible failure reasons.

---

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
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| TP-ERR-01 | manual | todo | Invalid range |
| TP-ERR-02 | manual | todo | Missing ffmpeg message |
| TP-ERR-03 | manual | todo | Source intact after fail |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial error-handling law |

---

**Last Updated**: 2026-08-09  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
