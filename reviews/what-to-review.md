# What to review — VideoSpeed

**Living checklist** (review plan). Product: **VideoSpeed** interactive MP4 cut → speed/length → optional boomerang.  
**Class:** software-development · domain SSOT present · **pip/local package** install.  
**Always load first:** `reviews/lessons.md`

**Last plan update:** 2026-08-09

---

## Pre-flight

| # | Check | Notes |
|---|--------|--------|
| P1 | Read `docs/requirements/index.md` | Class + python + domain + video + runtime |
| P2 | Confirm ship modules under `src/VideoSpeed/` | `__version__` matches `pyproject.toml` |
| P3 | Load `reviews/lessons.md` and re-check every open L-* | Mandatory |
| P4 | Compile: `python3 -m py_compile src/VideoSpeed/cli.py` | Until full suite exists |
| P5 | Confirm install mode still **pip/local** | No shell Type O / SCRIPT_URL product UX |
| P6 | Confirm Type 1 elevation still **absent** | No sudoers product surface |
| P7 | Run suite when present | `tests/run.sh` or project equivalent; record PASS/FAIL/SKIP |

---

## Product law surfaces

| Surface | Path | Review focus |
|---------|------|--------------|
| Class | `requirement-class-software-dev.md` | Python residual; no online shell package |
| Domain | `requirement-domain-videospeed.md` | Four pillars; cut/speed/boomerang catalog |
| FFmpeg pipeline | `requirement-video-ffmpeg-pipeline.md` | Order, temps, **`shutil.move`** publish, USB |
| CLI interface | `requirement-python-cli-interface.md` | Type N interactive; `--help`/`--version` |
| Coding style | `requirement-python-coding-style.md` | Temps + move APIs; no bare cross-mount rename |
| Packaging | `requirement-python-packaging.md` | pyproject, entrypoint, version dual SSOT |
| Project structure | `requirement-python-project-structure.md` | `src/` layout; cli SSOT |
| Error handling | `requirement-python-error-handling.md` | Fail closed; source safe |
| Runtime prereqs | `requirement-runtime-prerequisites.md` | FFmpeg system; OpenCV pip |

**Intentionally absent (do not “restore” without owner order):** shell online-install, self-update Type 0, Type 1 sudoers elev, channel `.sha256`.

---

## High-risk paths (ship unit)

| Path / symbol | Risk | Lesson |
|--------------|------|--------|
| `promote_file` / final publish | Bare rename across USB mounts | L-XDEV-01 |
| `staging_dir_for` / `make_temp_path` | Temps only under `/tmp` | L-XDEV-01 |
| `cut_clip` / `speed_change` / `add_boomerang` | Source overwrite; bad filters | L-SRC-01 |
| `_atempo_filters` | Extreme ratio encode fail | L-ATEMPO-01 |
| `get_duration_cv2` | Import-time OpenCV | L-IMPORT-01 |
| `ensure_ffmpeg` | Missing binary mid-job | L-FFMPEG-01 |
| Cut range validation in interactive loop | Encode after invalid range | L-RANGE-01 |
| `cli.bootstrap-old.py` / root `cli-new.py` | Dual ship SSOT | L-DUAL-01 |
| `__init__.py` | Heavy import chain | L-IMPORT-01 |

---

## Type 1 elevation — review plan gate

| Gate | Status |
|------|--------|
| Product claims Type 1 / sudoers | **No** |
| CL-SHELL-TTY-PRIVILEGE-TRAPS | **N/A** |
| Elevation TP dual rows | **n/a** |

---

## Tests surface

| Check | Path |
|-------|------|
| Suite entry | `tests/` **not present yet** — see test-plan **todo** rows |
| TP map | `reviews/test-plan.md` |
| RTM | `reviews/requirement-test-matrix.md` |

---

## Product user docs (when reviewing release readiness)

| Check | Path |
|-------|------|
| README features / install honesty | `README.md` |
| Changelog vs package version | `docs/CHANGELOG.md` vs `1.0.5` |
| Design notes not replacing REQs | `docs/VideoClip-spec.md` |

---

## Explicit non-goals for default review

- Shell `curl|sh` online install channel  
- Type 1 host package elevation  
- Full StateLogic+Attr rewrite without explicit order  
- Genesis harness tree completeness inside this product repo  

---

## Publish steps (after a review run)

1. Write `reviews/reports/YYYY-MM-DD-<scope>.md`  
2. Update `reviews/index.md`  
3. Merge new modes into `reviews/lessons.md`  
4. Update TP rows in `reviews/test-plan.md` when bugs close or new gaps found  
5. Do not leave the only copy of findings in session scratch  
