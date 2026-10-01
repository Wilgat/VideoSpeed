**file**: docs/requirements/requirement-video-ffmpeg-pipeline.md  
**Status**: Active (Version 1.1.1)  
**Area**: video  
**Key**: `requirement-video-ffmpeg-pipeline`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement is the **operational Single Source of Truth** for VideoSpeed media processing: segment cut, speed/length change, optional boomerang (reverse + concat), temporary file lifecycle, and FFmpeg invocation rules.

Domain feature catalog and user workflow labels live in **`requirement-domain-videospeed`**. The menu walk versus one job lives in **`requirement-python-interactive-vs-noninteractive`**. Entry stays on **`requirement-python-cli-interface`**.

### 1.1 Human-facing

**In one sentence:** This file says how a job is encoded: cut the segment, change its length, optionally reverse-and-append, write temps next to the output, never overwrite the source MP4.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person who wants a new clip | Final file appears beside the source |
| The other role | Domain / CLI | Which times and percent you asked for |
| Not this file | Help text | Domain file |

| Includes | Excludes |
|----------|----------|
| Cut → speed → optional boomerang; temps; `shutil.move` publish | Prompt wording; pip metadata |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/VideoSpeed/cli.py` | `process_job` / `cut_clip` | live encode |
| `video-speed --file clip.mp4 --start 1 --end 5` | command | one job |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Run a job | FFmpeg must not write over the original file. | `video-speed --file clip.mp4 --start 1 --end 5` |

---

## 2. Core Rules (Mandatory)

### 2.1 Pipeline order

1. **MUST** process media in this order when a full job runs: **cut → speed/length → (optional) boomerang → final path**.  
2. **MUST NOT** apply boomerang before cut/speed for a standard domain job.  
3. **MUST** write intermediate results to **temporary files**, not by overwriting the user’s source file.  
4. **MUST** place the final successful output at the path chosen by domain naming rules (same directory as source).

### 2.2 Cut (segment extract)

5. **MUST** extract the closed time window `[start, end)` or product-equivalent start/end bounds requested by the user.  
6. **MUST** reject invalid ranges where not `0 <= start < end <= duration` (duration from OpenCV probe or equivalent).  
7. **MUST** re-encode or filter so timestamps start cleanly after cut (product currently uses FFmpeg `trim` / `atrim` + `setpts` / `asetpts`).  
8. **MUST NOT** modify the original source file in place.

### 2.3 Speed / length percent

9. **MUST** accept a percent value representing **desired output length relative to the cut segment** (100 = unchanged duration intent).  
10. **MUST** reject length percent outside **20–200%** with a clear re-prompt (interactive) or error (non-interactive when added).  
11. **MUST** keep video and audio tempo in sync for the adjusted segment (product uses `setpts` + chained `atempo` filters when outside a single atempo’s 0.5–100 range).  
12. **MUST** fail closed if FFmpeg returns non-zero (see error-handling peer).

### 2.4 Boomerang

13. When enabled, **MUST** produce forward playback of the sped clip followed by reverse playback of that same clip.  
14. **MUST** reverse both video and audio for the reverse half.  
15. **MUST** concatenate forward + reverse into one MP4 at the final path.  
16. When disabled, **MUST** promote the sped intermediate to the final path without reverse half.

### 2.5 FFmpeg invocation

17. **MUST** invoke the system **`ffmpeg`** binary (PATH-resolved) via subprocess — not a reimplemented codec stack.  
18. **MUST** use non-interactive flags suitable for automation (`-y` overwrite temps, hide banner, reduced log noise preferred).  
19. **MUST NOT** shell-interpolate untrusted free-form filter strings from remote input without validation (times/percent are numeric).  
20. **MUST** treat missing `ffmpeg` as a **runtime prerequisite failure** (pointer to `requirement-runtime-prerequisites`).

### 2.6 Temporary files and cleanup

21. **MUST** create intermediate MP4 (and concat list when boomerang) via secure temp mechanisms (`tempfile` / `mkstemp` or equivalent).  
22. **MUST** prefer staging intermediate files on the **same filesystem/mount as the final output** (critical when source/output is on USB / FAT / exFAT / other removable media while system `TMPDIR` is on the root disk).  
23. **MUST** publish a completed intermediate to the final path with **`shutil.move`** (or a thin wrapper that only calls `shutil.move`). Same mount → rename; cross-device → copy then remove source (`EXDEV`-safe).  
24. **MUST NOT** use bare **`os.rename` / `os.replace` / `pathlib.Path.rename` / `pathlib.Path.replace`** alone as the sole publish path when the source may be system temp and the destination may be another mount.  
25. **MUST** attempt cleanup of intermediate temps on success and failure paths (best-effort; log if cleanup fails).  
26. **MUST NOT** leave final success dependent on deleting the user’s source.  

General file-move coding rules also live in **`requirement-python-coding-style`**; this file owns **pipeline** apply of those rules.

### 2.7 Codecs / quality (current product law)

27. **MUST** document encode defaults in Implementation Notes.  
28. Changing codec/CRF/preset **MUST** update Implementation Notes in the same change as code.  
29. **MUST NOT** claim lossless pipeline when re-encode is used.

### 2.8 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Ops module** | `src/VideoSpeed/cli.py` functions `cut_clip`, `speed_change`, `add_boomerang`, `run_ffmpeg` |
| **Cut filters** | video `trim=start:end,setpts=PTS-STARTPTS`; audio `atrim` + `asetpts` |
| **Cut encode** | libx264, preset `ultrafast`, CRF 17; audio AAC |
| **Speed math** | `speed = 100.0 / ratio_percent`; video `setpts=(1/speed)*PTS`; audio `atempo=speed` |
| **Speed encode** | libx264, preset `medium`, CRF 18; AAC 192k; `+faststart` |
| **Boomerang** | `reverse` / `areverse` then concat demuxer list of forward + reverse |
| **Duration probe** | OpenCV `VideoCapture` FPS × frame count (not FFmpeg probe) |
| **Overwrite policy** | Final path may overwrite same-named prior output (`-y` on FFmpeg stages); source file never targeted as output |
| **Temp staging** | `make_temp_path` / `staging_dir_for(final_out)` — prefer output parent (USB-safe) |
| **Final promote** | `promote_file` → **`shutil.move(src, dest)`** only |
| **Corresponding APIs (publish)** | Prefer: `shutil.move`. Avoid alone for cross-mount: `os.replace`, `os.rename`, `Path.replace`, `Path.rename`. Copy-only: `shutil.copy2` (not a move). |
| **Elevation** | None — all work as invoking user |

### 2.9 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution**: Numeric validation and non-destructive source handling.  
- **Principle 2 – Intentional**: Pipeline order and filter ownership explicit.  
- **Principle 11 – Temps**: Explicit temp lifecycle.  
- **Principle 5 – SSOT**: One ops home for encode behavior.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Fail closed on FFmpeg errors; never silent success.  
- **Intentional:** Cut → speed → boomerang order is product law.  
- **Anti-fragile:** Temp intermediates avoid partial overwrite of user media.  
- **Over-protect:** Source path is read-only input for the pipeline.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Overwrite or delete the user’s source media as the “output” path.  
2. Drop audio reverse while claiming boomerang.  
3. Remove temp cleanup without an explicit alternative safety design.  
4. Shell-out to FFmpeg with unsanitized free-form user filter graphs.  
5. Move full encode law only into domain without keeping this ops SSOT.  
6. Add root/sudo FFmpeg elevation without elev allowlist law and user order.  
7. Reintroduce bare cross-device `os.replace`/`os.rename` as the only non-boomerang publish path (must stay **`shutil.move`**).

**Violating this rule is a critical media-safety regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Pipeline order cut → speed → optional boomerang documented and implemented |
| AC-2 | Invalid time range rejected before encode |
| AC-3 | Source file not modified in place |
| AC-4 | Boomerang produces forward+reverse |
| AC-5 | Temps cleaned best-effort |
| AC-6 | FFmpeg non-zero exits fail closed |
| AC-7 | Non-boomerang job succeeds when source/output on a different mount than system TMPDIR (USB) |
| AC-8 | Non-boomerang publish uses **`shutil.move`** (not bare cross-device rename only) |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-domain-videospeed` | Domain surface |
| `requirement-python-interactive-vs-noninteractive` | Menu walk versus one job |
| `requirement-python-cli-interface` | Entry |
| `requirement-python-error-handling` | Fail messaging |
| `requirement-python-coding-style` | General file move / temp coding rules |
| `requirement-runtime-prerequisites` | `ffmpeg` present |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| TP-FFMPEG-01..05 | — | skip | Need ffmpeg + fixture MP4 |
| TP-FS-01 | `tests/test_fs.py` | have | `shutil.move` |
| TP-FS-02 | `tests/test_fs.py` | have | staging |
| TP-ERR-01 | `tests/test_errors.py` | have | Invalid range |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial FFmpeg pipeline ops law |
| 2026-08-19 | Active 1.1.0 | §1.1; FS/ERR TP have |
| 2026-10-01 | Active 1.1.1 | Walk versus job points at the mode requirement |

---

**Last Updated**: 2026-10-01  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
