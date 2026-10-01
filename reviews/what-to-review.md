# What to review — VideoSpeed

**Living checklist** (review plan). Product: **VideoSpeed** interactive MP4 cut → speed/length → optional boomerang.  
**Class:** software-development · domain SSOT present · **pip/local package** install.  
**Always load first:** `reviews/lessons.md`

**Last plan update:** 2026-10-01 (product verbs `help`, `about`, `hello`, `edit`, `list-mp4`)

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
| P7 | Run suite | `./tests/run.sh` — Core must PASS |

---

## Product law surfaces

| Surface | Path | Review focus |
|---------|------|--------------|
| Class | `requirement-class-software-dev.md` | Python residual; no online shell package |
| Domain | `requirement-domain-videospeed.md` | Four pillars; cut/speed/boomerang catalog |
| FFmpeg pipeline | `requirement-video-ffmpeg-pipeline.md` | Order, temps, **`shutil.move`** publish, USB |
| CLI interface | `requirement-python-cli-interface.md` | Entry points; product verbs `help`, `about`, `hello`, `edit`, `list-mp4`; `main` order; `--help`/`--version` |
| Modes | `requirement-python-interactive-vs-noninteractive.md` | Menu walk, verb prompts (folder then file), or one job. A selector with no verb must not open the menu |
| JSON output | `requirement-python-json-output.md` | `--json` is one object on stdout. No text menu. Prompts, if any, are on stderr |
| Text menu | `requirement-python-tui.md` | Default TUI style; writer is `src/VideoSpeed/menu.py` until class `Tui`; glyphs stay out of `cli.py` |
| OOP grouping | `requirement-python-oop.md` | Class `Tui` in `tui.py`; class `CheckSystem` in `check_system.py`. Session and host-check functions are still in `cli.py`. Painter is still `menu.py` |
| About page | `requirement-python-about.md` | Identity, host check, star box. Each line names its read. No curl line while the download URL is empty |
| Coding style | `requirement-python-coding-style.md` | Temps; `shutil.move` for every file move; no `os.rename` or `os.replace` (removable media) |
| Packaging | `requirement-python-packaging.md` | pyproject, entrypoint, version dual SSOT |
| Maintainer build | `requirement-python-build-script.md` | `./build.sh` verbs. `test` is `tests/run.sh`. Empty argv does not upload |
| Pip dependency floors | `requirement-python-dependency-management.md` | `opencv-python-headless>=5.0.0.93`, `ChronicleLogger>=1.3.1`; no GUI `opencv-python`; no menu wheel |
| System status log | `requirement-python-cli-logging.md` | One ChronicleLogger in `main`. Debug mode displays the version lines when `DEBUG` is `1`, `true`, or `show`. Menu path calls `quiet(True)` |
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
| `open_text_menu` / `MENU_ROWS` | Frame glyphs copied into `cli.py`, or tests aimed at a sibling menu checkout | L-TUI-01 |
| `main` mode gate | `--percent` or `--boomerang` alone, or any selector, falls through into the menu | mode requirement |
| `_dispatch` product verbs | An unknown token, `Exit`, or a `./build.sh` verb opens the menu or encodes. `edit` or `list-mp4` paints the front board before the folder question | mode requirement |
| `build.sh` dispatcher | `test` calls a second runner, empty argv uploads, or `test-install` embeds the project name | build-script requirement |
| `--json` | Menu opens, or progress shares stdout with the object | JSON requirement |

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
| Suite entry | `tests/run.sh` |
| TP map | `reviews/test-plan.md` |
| RTM | `reviews/requirement-test-matrix.md` |

---

## Product user docs (when reviewing release readiness)

| Check | Path |
|-------|------|
| README features / install honesty | `README.md` |
| Changelog vs package version | root `CHANGELOG.md` (SSOT) vs `1.0.7` |
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
