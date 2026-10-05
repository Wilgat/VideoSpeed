# Requirements

Authoritative specialized product law for **VideoSpeed** lives here.

**Current state (2026-10-05):** Specialized **software-development** product. Left genesis. Registry is populated (23 Active) — see `index.md`. Class residual records dest approver/fences as **considered — none**.

## Product identity (summary)

| Field | Value |
|-------|--------|
| Product / package | `VideoSpeed` |
| Version SSOT | `requirement-python-version` — `MAJOR_VERSION` 1, `MINOR_VERSION` 0, `PATCH_VERSION` 12 → `1.0.12` |
| Text menu | `requirement-python-tui` — picture; first row is Path and the current directory; session is class `Tui`; frame is class `MenuPainter`. Front row **4** is language. Front row **6** is system-log |
| User README | `requirement-python-readme` — root `README.md` sections, Advantages after Features, related projects, badges, install honesty, and the text-menu screenshots. A capture that shows a version shows the package string. The path-row sentence names the local clock |
| Menu language | `requirement-python-cli-language` — thirteen codes on row **4**; one line under this login’s persistence directory; `VIDEOSPEED_LANG` wins at process start and does not write |
| About page | `requirement-python-about` — identity, host check, star box. `about --json` writes that page to the error stream (`TP-ABOUT-15` have) |
| Pyenv paths | `requirement-python-pyenv` — under pyenv, python2 and python3 stay inside the root, and pyenv location is `bin/pyenv`. `in_pyenv` does not replace that root test |
| Conda paths | `requirement-python-conda` — under conda, python2 and python3 stay inside the prefix, and conda location is `bin/conda`. `in_conda` does not replace that root test |
| OOP grouping | `requirement-python-oop` — one class per file. `def main` stays in `cli.py` and writes `ChronicleLogger(...)`, then `Cli(logger)`. Each class `__init__` receives the logger and writes its own instantiation line. Class `Cli` owns its identity constants, verb lists, and length bounds. The site that needs an object writes `ClassName(...)`. A factory is not in the map. `TP-OOP-01` through `TP-OOP-04` have landed |
| Pip floors | `requirement-python-dependency-management` — `opencv-python-headless>=5.0.0.93`, `ChronicleLogger>=1.3.1` |
| System status log | `requirement-python-cli-logging` — `def main` instantiates ChronicleLogger by writing `ChronicleLogger(...)` in that function. The console mirror stays off unless `--verbose` is set on a run that is not `--json` and not a text screen. Each `__init__` logs `instantiated`. `CheckSystem` reads in-venv, in-pyenv, and in-conda from that logger. The log folder is the one ChronicleLogger already returns from `logDir()`: conda, else pyenv, else venv, else `~/.app/video-speed/log`, or `/var/video-speed/log` when root and none of those are active. A major file operation logs the operation and the paths. Thread creation and thread operations log before the call that can block (`TP-LOG-07` todo; the ship unit creates no threads). `DEBUG` without `--verbose` writes the daily file and does not show the terminal. `about --json` keeps the mirror off both streams, including `Created directory:`. `[CHECK SYSTEM]:` is the about page (`TP-LOG-08` have) |
| Control-C | `requirement-python-graceful-exit` — on an open text screen, ask `Exit? (y/n)` and log the decision. Yes exits 130. A live child is stopped and not published first. Not in the ship unit yet (`TP-EXIT-01` through `TP-EXIT-07` todo) |
| Modes | `requirement-python-interactive-vs-noninteractive` — the menu is the no-verb entry. `edit` and `list-mp4` are the named screen verbs. Other product verbs stay on the terminal |
| Maintainer build | `requirement-python-build-script` — `./build.sh` verbs |
| JSON output | `requirement-python-json-output` — `--json` on every product verb is one object; no text menu. The flags `--help` and `--version` stay human |
| Ship surface | Python package; console script `video-speed` |
| Install mode | **pip / local package** |
| Domain surface | `requirement-domain-videospeed` — four pillars |
| Encode ops | `requirement-video-ffmpeg-pipeline` — cut / speed / boomerang |
| Coding style | `requirement-python-coding-style` — temps; `shutil.move` for every file move; no `os.rename` or `os.replace`; one class per file; an object is `ClassName(...)` at the site; a factory (a function or a method that instantiates a class) is banned; identity, verb lists, and bounds are attributes of class `Cli`; attribute access by name; no `__dict__` unless the user orders that access |
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
