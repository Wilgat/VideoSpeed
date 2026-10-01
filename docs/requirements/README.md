# Requirements

Authoritative specialized product law for **VideoSpeed** lives here.

**Current state (2026-10-02):** Specialized **software-development** product. Left genesis. Registry is populated (20 Active) — see `index.md`. Class residual records dest approver/fences as **considered — none**.

## Product identity (summary)

| Field | Value |
|-------|--------|
| Product / package | `VideoSpeed` |
| Version SSOT | `requirement-python-version` — `MAJOR_VERSION` 1, `MINOR_VERSION` 0, `PATCH_VERSION` 10 → `1.0.10` |
| Text menu | `requirement-python-tui` — picture; session is class `Tui`; frame is class `MenuPainter` |
| About page | `requirement-python-about` — identity, host check, star box |
| Pyenv paths | `requirement-python-pyenv` — under pyenv, python2 and python3 stay inside the root, and pyenv location is `bin/pyenv` |
| OOP grouping | `requirement-python-oop` — one class per file. `def main` stays in `cli.py`. Each class `__init__` receives the logger. `TP-OOP-01` through `TP-OOP-04` have landed |
| Pip floors | `requirement-python-dependency-management` — `opencv-python-headless>=5.0.0.93`, `ChronicleLogger>=1.3.1` |
| System status log | `requirement-python-cli-logging` — one ChronicleLogger, passed into every class. Each object logs `instantiated`. A major file operation logs the operation and the paths. Thread creation and thread operations log before the call that can block (`TP-LOG-07` todo; the ship unit creates no threads). A non-TUI, non-JSON run shows `debug mode` |
| Control-C during a long child | `requirement-python-graceful-exit` — stop the child, do not publish, exit 130. Not in the ship unit yet (`TP-EXIT-01`, `TP-EXIT-02` todo) |
| Modes | `requirement-python-interactive-vs-noninteractive` — menu walk, product verb (folder then file), or one job |
| Maintainer build | `requirement-python-build-script` — `./build.sh` verbs |
| JSON output | `requirement-python-json-output` — `--json` is one object; no text menu |
| Ship surface | Python package; console script `video-speed` |
| Install mode | **pip / local package** |
| Domain surface | `requirement-domain-videospeed` — four pillars |
| Encode ops | `requirement-video-ffmpeg-pipeline` — cut / speed / boomerang |
| Coding style | `requirement-python-coding-style` — temps; `shutil.move` for every file move; no `os.rename` or `os.replace`; one class per file |
| Runtime tools | FFmpeg (system) + OpenCV (pip) |
| Public reviews | `reviews/` — what-to-review, test-plan, lessons, reports |

## Class requirement gate

| Class | Required class file |
|-------|---------------------|
| software-development | `requirement-class-software-dev.md` (**Active**) |
| genesis-template | N/A — this workspace is no longer genesis for product law |

## Purpose

- **Plan** designs work by reading and updating these docs.  
- **Implement** delivers code that **traces** to these requirements.  
- **Review** verifies delivery against requirements and CIAO checklists.

## Layout

| Path | Role |
|------|------|
| `docs/requirements/index.md` | Registry of all requirements — keep in sync |
| `docs/requirements/requirement-*.md` | CIAO-style project requirements |

## Status values

Typical: `draft` · `Active` · `approved` · `in-progress` · `done` · `deprecated` · `superseded`

## Rules

1. Never invent paths — verify on disk.  
2. Class files only via class process; non-class via create-specific process.  
3. Never dump harness inventories into this versioned surface.  
4. Online shell install and Type 1 elevation stay **absent** unless product mode is explicitly changed.  
5. Sole domain SSOT: `requirement-domain-videospeed.md`.
