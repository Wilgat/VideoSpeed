# Test plan — VideoSpeed

Maps **TP-*** coverage to automated or documented checks.  
**Suite entry:** `tests/run.sh` (`PYTHONPATH=src python3 -m unittest discover -s tests -v`)  
**Ship unit:** `src/VideoSpeed/cli.py`  
**Last update:** 2026-10-01  
**Last suite run:** 2026-10-01 (`PYENV_VERSION=3.14.7 ./tests/run.sh`: 71 ok, TP-PRE-01 skipped because ffmpeg is on PATH)

Status: **have** = automated today · **todo** = needed · **manual** = documented human procedure · **n/a** · **skip** (environment)

---

## Baseline coverage

| Area | Status | Evidence |
|------|--------|----------|
| Package import / version without OpenCV | **have** | `tests/test_package.py` |
| Pip dependency floors (OpenCV headless, ChronicleLogger) | **have** | `tests/test_dependencies.py` |
| ChronicleLogger system-status wiring | **partial** | `requirement-python-cli-logging` (`TP-LOG-01`, `TP-LOG-02`, `TP-LOG-04` have; `TP-LOG-03` todo) |
| `--version` / `--help` | **have** | `tests/test_cli.py` |
| Empty argv without TTY | **have** | `TP-MODE-03`; fail-closed; job flags named |
| Selector or lone modifier does not open the menu | **have** | `tests/test_cli.py` (`TP-MODE-01`, `TP-MODE-02`). No product verb on those rows |
| Product verbs `help`, `about`, `hello`, `edit`, `list-mp4` | **have** | `tests/test_cli.py`, `tests/test_tui.py` (`TP-CLI-07`, `TP-MODE-05`..`TP-MODE-08`) |
| Text menu frame and columns | **have** | `tests/test_tui.py` (`src/VideoSpeed/tui.py`, class `Tui`) |
| FFmpeg preflight | **have** | `tests/test_prereq.py` (missing-binary path) |
| Cut → speed (no boomerang) | **skip** | needs fixture + ffmpeg |
| Boomerang | **skip** | needs fixture + ffmpeg |
| Invalid range fail-closed | **have** | `valid_cut_range` |
| Length % outside 20–200 rejected | **have** | `valid_percent` |
| USB / cross-FS publish via `shutil.move` | **have** | `tests/test_fs.py` |
| Source file not modified | **todo** | needs encode fixture |
| Online install / Type 1 elev | **n/a** | product absent |

---

## TP rows

### TP-PKG (packaging / import)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-PKG-01 | `import VideoSpeed` without `cv2` installed; `__version__` readable | `tests/test_package.py` | packaging · coding-style · L-IMPORT-01 | **have** |
| TP-PKG-02 | `pyproject.toml` version == `__version__` | `tests/test_package.py` | packaging · requirement-python-version | **have** |
| TP-PKG-03 | Console script target `VideoSpeed.cli:main` declared | `tests/test_package.py` | packaging · CLI | **have** |
| TP-PKG-04 | `python3 -m py_compile` on package modules | `tests/test_package.py` | class / structure | **have** |

### TP-VER (version SSOT)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-VER-01 | `MAJOR_VERSION`.`MINOR_VERSION`.`PATCH_VERSION` equals `__version__` and `pyproject.toml` | `tests/test_package.py` | requirement-python-version | **have** |
| TP-VER-02 | `cli.py` does not assign `MAJOR_VERSION` or a `"1.0.6"` fallback | `tests/test_package.py` | requirement-python-version | **have** |
| TP-VER-03 | Debug line prints `v{MAJOR}.{MINOR}.{PATCH}` | — | requirement-python-version · requirement-python-cli-interface | **todo** |
| TP-MAIN-01 | `main` order: version, logger, debug, missing import, parser | — | requirement-python-cli-interface | **todo** |

### TP-DEP (pip dependency floors)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-DEP-01 | Runtime deps present; every entry has a version specifier | `tests/test_dependencies.py` | requirement-python-dependency-management | **have** |
| TP-DEP-02 | Vision wheel is `opencv-python-headless`; GUI `opencv-python` absent | `tests/test_dependencies.py` | requirement-python-dependency-management | **have** |
| TP-DEP-03 | Dependency requirement states the same specs as `pyproject.toml` | `tests/test_dependencies.py` | requirement-python-dependency-management | **have** |
| TP-DEP-04 | Installed wheels, when present, meet `>=5.0.0.93` and `>=1.3.1` | `tests/test_dependencies.py` | requirement-python-dependency-management | **have** |

### TP-LOG (ChronicleLogger system status)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-LOG-01 | One construct; read back `logName` / `baseDir` / `logDir` under a temp base | `tests/test_logging.py` | requirement-python-cli-logging | **have** |
| TP-LOG-02 | `DEBUG=1` before construct shows identity lines; unset `DEBUG` does not | `tests/test_logging.py` | requirement-python-cli-logging | **have** |
| TP-LOG-03 | `INFO` / `WARNING` / `ERROR` / `FATAL` with keyword `component` | — | requirement-python-cli-logging | **todo** |
| TP-LOG-04 | Text menu path calls `quiet(True)` before the frame | `tests/test_logging.py` | requirement-python-cli-logging | **have** |

### TP-CLI (CLI surface)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-CLI-01 | `python -m VideoSpeed --version` exits 0, prints version | `tests/test_cli.py` | CLI interface | **have** |
| TP-CLI-02 | `video-speed --help` / module `--help` lists usage | `tests/test_cli.py` | CLI interface | **have** |
| TP-CLI-03 | Empty argv starts interactive session (banner) when TTY fed | `tests/test_cli.py` | CLI · domain | **todo** |
| TP-CLI-04 | No MP4 in folder → clear message, non-success path | `tests/test_cli.py` | CLI · error-handling | **have** |
| TP-CLI-05 | Invalid video index re-prompts (not crash) | `tests/test_cli.py` | error-handling | **todo** |
| TP-CLI-06 | Batch `--file`/`--start`/`--end`; missing file / incomplete flags fail closed | `tests/test_cli.py` | CLI · domain | **have** |
| TP-CLI-07 | `help` lists `help`, `about`, `hello`, `edit`, `list-mp4`; an unknown verb exits 1 and does not open the menu | `tests/test_cli.py` | requirement-python-cli-interface · requirement-python-interactive-vs-noninteractive | **have** |

### TP-MODE (menu walk versus one job)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-MODE-01 | Any selector (`--file`, `--start`, `--end`, `--folder`) does not open the menu, even on a terminal | `tests/test_cli.py` | requirement-python-interactive-vs-noninteractive | **have** |
| TP-MODE-02 | Lone `--percent` or `--boomerang` exits 1 and does not open the menu | `tests/test_cli.py` | requirement-python-interactive-vs-noninteractive | **have** |
| TP-MODE-03 | Empty argv with no terminal exits 1 and names `--file`, `--start`, `--end` | `tests/test_cli.py` | requirement-python-interactive-vs-noninteractive | **have** |
| TP-MODE-04 | Edit asks the folder line inside the frame and does not call `input()` | `tests/test_tui.py` (`TP-TUI-04`) | requirement-python-interactive-vs-noninteractive · requirement-python-tui | **have** |
| TP-MODE-05 | `video-speed edit` on a terminal with no `--file` asks the folder line, then the video line, inside the frame, and does not call `input()` | `tests/test_tui.py` | requirement-python-interactive-vs-noninteractive | **have** |
| TP-MODE-06 | `video-speed edit` with no terminal and without `--file`, `--start`, and `--end` exits 1 and does not prompt | `tests/test_cli.py` | requirement-python-interactive-vs-noninteractive | **have** |
| TP-MODE-07 | `list-mp4` on a terminal asks for the folder when omitted, then lists, and does not encode. With no terminal it lists `--folder` or the current directory and does not prompt | `tests/test_cli.py` · `tests/test_tui.py` | requirement-python-interactive-vs-noninteractive · requirement-domain-videospeed | **have** |
| TP-MODE-08 | `about`, `help`, and `hello` do not ask for a folder or a file, with or without a terminal | `tests/test_cli.py` | requirement-python-interactive-vs-noninteractive · requirement-python-about | **have** |

### TP-BUILD (maintainer `build.sh` verbs)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-BUILD-01 | Help and empty argv list every verb and separate `test` | `tests/test_build.py` | requirement-python-build-script | **have** |
| TP-BUILD-02 | Unknown verb exits 1 | `tests/test_build.py` | requirement-python-build-script | **have** |
| TP-BUILD-03 | `version` prints the checkout package version | `tests/test_build.py` | requirement-python-build-script · requirement-python-version | **have** |
| TP-BUILD-04 | Extra `test` arguments exit 1 and do not start the suite | `tests/test_build.py` | requirement-python-build-script | **have** |
| TP-BUILD-05 | `build` writes an sdist and a wheel | — | requirement-python-build-script | **todo** |
| TP-BUILD-06 | `test-install` reads the project name, uninstalls that pip install when present, then installs this checkout | `tests/test_build.py` | requirement-python-build-script | **have** |

### TP-JSON (`--json` one object)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-JSON-01 | `--json --percent` exits 1 as one object and does not open the menu | `tests/test_json.py` | requirement-python-json-output | **have** |
| TP-JSON-02 | `--json --file` without start and end is one object and does not encode | `tests/test_json.py` | requirement-python-json-output | **have** |
| TP-JSON-03 | `--json` with no terminal is one object and does not wait | `tests/test_json.py` | requirement-python-json-output | **have** |
| TP-JSON-04 | Terminal plus `--json` asks on stderr and does not open the menu | `tests/test_json.py` | requirement-python-json-output · requirement-python-interactive-vs-noninteractive | **have** |
| TP-JSON-05 | `--json --version` stays human text and exits 0 | `tests/test_json.py` | requirement-python-json-output | **have** |

### TP-TUI (text menu / default TUI style)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-TUI-01 | Three-row rounded frame, full width, block caret, status line, no `Choice:` | `tests/test_tui.py` | requirement-python-tui | **have** |
| TP-TUI-02 | This board’s number / verb / explain pads, plus two-digit and three-digit pads from `VideoSpeed.tui` | `tests/test_tui.py` | requirement-python-tui | **have** |
| TP-TUI-03 | Too-small screen fails closed; product source does not import or declare an external menu package | `tests/test_tui.py` | requirement-python-tui | **have** |
| TP-TUI-04 | edit stays and asks the folder line inside the frame; Exit leaves; unknown token stays; about result omits the frame | `tests/test_tui.py` | requirement-python-tui | **have** |
| TP-TUI-05 | Menu 7 shows `Hello.` on the result page and that page omits the frame | `tests/test_tui.py` | requirement-python-tui | **have** |

### TP-ABOUT (about page)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-ABOUT-01 | Identity line, every host-check label, star-box title; live page has no curl line and no `py-tui` | `tests/test_about.py` | requirement-python-about | **have** |
| TP-ABOUT-02 | Stamp, `[CHECK SYSTEM]:` header, and field order | `tests/test_about.py` | requirement-python-about | **have** |
| TP-ABOUT-03 | Star box is one rectangle; global path uses the GLOBAL sentence | `tests/test_about.py` | requirement-python-about | **have** |
| TP-ABOUT-04 | A passed download URL renders the install line; the product URL stays empty | `tests/test_about.py` | requirement-python-about | **have** |
| TP-ABOUT-05 | GCC and PyPy tokens, arch map, libc tokens, `amd64-glibc` | `tests/test_about.py` | requirement-python-about | **have** |
| TP-ABOUT-06 | Checkout is uninstalled; a home copy is local; `/usr` is global | `tests/test_about.py` | requirement-python-about | **have** |
| TP-ABOUT-07 | Docker follows the marker file; a missing tool location stays blank | `tests/test_about.py` | requirement-python-about | **have** |
| TP-ABOUT-08 | A long about page scrolls to Basic Usage; a one-line result still closes on Down | `tests/test_tui.py` | requirement-python-about · requirement-python-tui | **have** |

### TP-PRE (runtime prerequisites)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-PRE-01 | Missing `ffmpeg` → preflight error, no encode | `tests/test_prereq.py` | runtime-prerequisites · L-FFMPEG-01 | **have** |
| TP-PRE-02 | Missing OpenCV → clear error on duration probe | `tests/test_prereq.py` | runtime-prerequisites · L-IMPORT-01 | **have** |

### TP-ERR (error handling)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-ERR-01 | Invalid cut range does not call encode | `tests/test_errors.py` | error-handling · L-RANGE-01 | **have** |
| TP-ERR-02 | Length % outside 20–200 rejected | `tests/test_errors.py` | domain · pipeline | **have** |
| TP-ERR-03 | FFmpeg non-zero → job failed message; source intact | `tests/test_errors.py` | error-handling · pipeline | **todo** |

### TP-FS (filesystem / USB / promote)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-FS-01 | `promote_file` uses `shutil.move` (source code or behavior across two dirs) | `tests/test_fs.py` | coding-style · pipeline · L-XDEV-01 | **have** |
| TP-FS-02 | `staging_dir_for(dest)` returns dest parent when writable | `tests/test_fs.py` | coding-style · pipeline | **have** |
| TP-FS-03 | Non-boomerang job: final appears on “other mount” simulation (two temp roots) | `tests/test_fs.py` | pipeline AC-7 | **todo** |
| TP-FS-04 | After promote, intermediate source gone or not left as sole copy | `tests/test_fs.py` | pipeline | **have** |
| TP-FS-05 | Ship modules do not call `os.rename` or `os.replace` (archive excluded) | `tests/test_fs.py` | coding-style · pipeline · L-XDEV-01 | **have** |
| TP-STYLE-01 | Identity block (`APP_NAME`, `CONSOLE_NAME`, `AUTHOR_NAME`, `HOMEPAGE`, `LAST_UPDATE`, `DOWNLOAD_URL`, `BASIC_USAGE`, `_MESSAGE_SINK`, `RATIO_MIN`, `RATIO_MAX`) is assigned inside `main()` | `tests/test_docs.py` | coding-style | **todo** |
| TP-OOP-01 | Class `Tui` lives in `src/VideoSpeed/tui.py` and owns the text-menu session. Those functions are not defined in `cli.py`. The painter split is TP-OOP-03 | `tests/test_tui.py` | requirement-python-oop | **have** |
| TP-OOP-02 | Class `CheckSystem` lives in `src/VideoSpeed/check_system.py` and owns the host-check functions. Those functions are not defined in `cli.py` | `tests/test_about.py` | requirement-python-oop | **have** |
| TP-OOP-03 | `paint`, `format_rows`, and the frame glyphs are methods or constants of `MenuPainter`. `MenuModel` and `MenuSession` are their own modules. `tui.py` defines class `Tui` only | `tests/test_tui.py` | requirement-python-oop | **have** |
| TP-OOP-04 | `cli.py` defines class `Cli` and `def main`. Encoder, file stage, media info, about page, edit walk, and run output are not module-level functions there | `tests/test_cli.py` | requirement-python-oop | **have** |

### TP-FFMPEG (encode pipeline)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-FFMPEG-01 | Cut only (100% speed, no boom) produces output MP4 | `tests/test_pipeline.py` | pipeline · domain | **skip** (no ffmpeg/fixture) |
| TP-FFMPEG-02 | Speed 50% and 200% within bounds | `tests/test_pipeline.py` | pipeline · L-ATEMPO-01 | **skip** |
| TP-FFMPEG-03 | Boomerang produces longer/forward+reverse media | `tests/test_pipeline.py` | pipeline · domain | **skip** |
| TP-FFMPEG-04 | Source file byte-identical after job | `tests/test_pipeline.py` | pipeline · L-SRC-01 | **skip** |
| TP-FFMPEG-05 | Output naming pattern matches domain | `tests/test_pipeline.py` | domain | **skip** |

### TP-DOMAIN (domain surface)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-DOMAIN-01 | Workflow steps cut→speed→optional boom still wired | encode suite | domain | **todo** (needs ffmpeg) |
| TP-DOMAIN-02 | About/version identity fields honest | `tests/test_docs.py` | domain pillar D | **have** |

### TP-STRUCT / TP-DOC

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-STRUCT-01 | Ship SSOT is `src/VideoSpeed/cli.py` not bootstrap-old alone | `tests/test_docs.py` | structure · L-DUAL-01 | **have** |
| TP-DOC-01 | README version/install claims vs pyproject | `tests/test_docs.py` | packaging · L-DOCS-01 | **have** |

### Intentionally n/a

| TP family | Reason |
|-----------|--------|
| TP-ONLINE / TP-CURL | No online install product mode |
| TP-ELEV / TTY privilege traps | No Type 1 elevation claimed |

---

## Rules

1. Closing a **bug** finding updates the matching TP toward **have** (and preferably adds an assertion).  
2. Do not mark TP **have** without a suite assertion (or honest skip/n/a with environment reason).  
3. Do not reintroduce online/elev TP as Core without product-mode change.  
4. Prefer implementing high-risk **TP-FS-*** and **TP-PKG-01** first (no media fixture required for pure unit cases).  
