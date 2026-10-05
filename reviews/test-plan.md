# Test plan — VideoSpeed

Maps **TP-*** coverage to automated or documented checks.  
**Suite entry:** `tests/run.sh` (`PYTHONPATH=src python3 -m unittest discover -s tests -v`)  
**Ship unit:** `src/VideoSpeed/cli.py`  
**Last update:** 2026-10-05  
**Last suite run:** 2026-10-05 (`./tests/run.sh`: 103 tests, OK, skipped=1 because ffmpeg is on PATH)

Status: **have** = automated today · **todo** = needed · **manual** = documented human procedure · **n/a** · **skip** (environment)

---

## Baseline coverage

| Area | Status | Evidence |
|------|--------|----------|
| Package import / version without OpenCV | **have** | `tests/test_package.py` |
| Pip dependency floors (OpenCV headless, ChronicleLogger) | **have** | `tests/test_dependencies.py` |
| ChronicleLogger system-status wiring | **partial** | `requirement-python-cli-logging` (`TP-LOG-01`, `TP-LOG-02`, `TP-LOG-04`, `TP-LOG-05`, `TP-LOG-08` have; `TP-LOG-03`, `TP-LOG-06`, `TP-LOG-07` todo) |
| Control-C confirm and child stop | **todo** | `requirement-python-graceful-exit` (`TP-EXIT-01` through `TP-EXIT-07` todo) |
| Time-consuming FFmpeg child | **have** | `requirement-python-time-consuming-process` (`TP-TIME-01` through `TP-TIME-05` have). One flashing wait line. The half-second flash does not stop the child. `./tests/run.sh` 2026-10-05: 103 tests, OK, skipped=1 |
| `--version` / `--help` | **have** | `tests/test_cli.py` |
| Empty argv without TTY | **have** | `TP-MODE-03`; fail-closed; job flags named |
| Selector or lone modifier does not open the menu | **have** | `tests/test_cli.py` (`TP-MODE-01`, `TP-MODE-02`). No product verb on those rows |
| Product verbs `help`, `version`, `about`, `edit`, `list-mp4`, `self-install`, `version-check`, `self-update`, `self-uninstall`. `hello` is an unknown verb. No verb, and `--verbose` alone, open the menu. `version`, `about`, and `help` stay on the terminal | **have** | `tests/test_cli.py`, `tests/test_tui.py` (`TP-CLI-07`, `TP-SELF-01`, `TP-TUI-06`, `TP-MODE-05`..`TP-MODE-09`) |
| Text menu frame and columns | **have** | `tests/test_tui.py` (`src/VideoSpeed/tui.py`, class `Tui`) |
| Text menu top line keeps the path on the left and a local clock on the right | **have** | `TP-TUI-07`, `TP-TUI-08`, `TP-TUI-09`, `TP-TUI-10`. Front and self-management boards paint `Path:` and the absolute working directory. The clock `HH:MM:SS` sits on the right when the row has room and is drawn again each second |
| FFmpeg preflight | **have** | `tests/test_prereq.py` (missing-binary path) |
| Cut → speed (no boomerang) | **skip** | needs fixture + ffmpeg |
| Boomerang | **skip** | needs fixture + ffmpeg |
| Invalid range fail-closed | **have** | `valid_cut_range` |
| Length % outside 20–200 rejected | **have** | `valid_percent` |
| USB / cross-FS publish via `shutil.move` | **have** | `tests/test_fs.py` |
| Source file not modified | **todo** | needs encode fixture |
| Shell online install / Type 1 elev | **n/a** | `curl\|sh` still absent |
| Python self-management (pip) | **have** | `TP-SELF-01`, `TP-TUI-06` |

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
| TP-LOG-02 | `DEBUG=1` without `--verbose` writes the identity lines and `debug mode` to the daily file and keeps them off the terminal. `DEBUG=1 --verbose` on a non-JSON, non-screen run shows them. Unset `DEBUG` does not log them. `--json` and the text screen keep that mirror off stdout even with `--verbose` | `tests/test_logging.py` | requirement-python-cli-logging | **have** |
| TP-LOG-03 | `INFO` / `WARNING` / `ERROR` / `FATAL` with keyword `component` | — | requirement-python-cli-logging | **todo** |
| TP-LOG-04 | Text menu path calls `quiet(True)` before the frame | `tests/test_logging.py` | requirement-python-cli-logging | **have** |
| TP-LOG-05 | Each constructed class stores the one logger and logs `instantiated`. Those lines appear on stdout only with `--verbose` on a non-JSON, non-screen run. `--json` keeps that line off stdout | `tests/test_logging.py` | requirement-python-cli-logging | **have** |
| TP-LOG-06 | A publish or a temp write logs the operation and the paths | — | requirement-python-cli-logging | **todo** |
| TP-LOG-07 | A thread create, start, or wait writes the action, the thread name, and the wait target before the call that can block. The log call is not made while a work lock is held | — | requirement-python-cli-logging | **todo** |
| TP-LOG-08 | `video-speed about --json` writes `ChronicleLogger(...)` inside `def main` with `is_quiet=True`. A new log folder does not print `Created directory:` on either stream. The about page on the error stream has `[CHECK SYSTEM]:` and no ChronicleLogger line. Standard output is only the JSON object | `tests/test_logging.py` | requirement-python-cli-logging · requirement-python-about | **have** |

### TP-EXIT (Control-C confirm and child stop)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-EXIT-01 | Control-C during the child, with no text screen, stops the group, does not publish, the log contains interrupted and `confirmed=unavailable`, the process exits 130, and there is no traceback | — | requirement-python-graceful-exit | **todo** |
| TP-EXIT-02 | A second Control-C during cleanup still exits 130, the child is gone, and the question is not shown | — | requirement-python-graceful-exit | **todo** |
| TP-EXIT-03 | Control-C on the open text menu draws `Exit? (y/n)`. `y` exits 130, the log contains `confirmed=yes` with component `menu`, and there is no traceback | — | requirement-python-graceful-exit | **todo** |
| TP-EXIT-04 | `n`, `no`, or Enter stays on the same board. The log contains `confirmed=no`. The process does not exit | — | requirement-python-graceful-exit | **todo** |
| TP-EXIT-05 | Control-C during FFmpeg while the text screen is open stops the child and does not publish, then asks. `n` returns to the screen. `y` exits 130 | — | requirement-python-graceful-exit | **todo** |
| TP-EXIT-06 | A second Control-C while the question is showing exits 130, logs `confirmed=yes`, and does not print a traceback | — | requirement-python-graceful-exit | **todo** |
| TP-EXIT-07 | `--json` and a non-interactive job do not ask and do not hang. Control-C exits 130 and logs `confirmed=unavailable` | — | requirement-python-graceful-exit | **todo** |

### TP-TIME (time-consuming FFmpeg child)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-TIME-01 | On a text screen, `Encoder.run_ffmpeg` shows `   ● please wait for time consuming process` and then the ○ line on the flash interval `0.5`. One wait line is replaced in place. `Popen` uses stdin `DEVNULL` and captured pipes. `TimeoutExpired` does not kill the child. No thread is started | `tests/test_time.py` | requirement-python-time-consuming-process | **have** |
| TP-TIME-02 | With no text screen and without `--json`, the same line is rewritten in place and both bullets appear. With `--json`, no progress line is written and the parent still polls until the child exits | `tests/test_time.py` | requirement-python-time-consuming-process | **have** |
| TP-TIME-03 | Length 100% and boomerang off does not call `speed_change`. The medium child does not start | `tests/test_time.py` | requirement-python-time-consuming-process | **have** |
| TP-TIME-04 | A length other than 100% calls `speed_change` after the cut. That command uses preset `medium`. The parent returns from that child before publish | `tests/test_time.py` | requirement-python-time-consuming-process | **have** |
| TP-TIME-05 | An exception other than the flash interval stops the child and propagates. The method does not return 130 and does not ask `Exit?` | `tests/test_time.py` | requirement-python-time-consuming-process | **have** |

### TP-CLI (CLI surface)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-CLI-01 | `python -m VideoSpeed --version` exits 0, prints version | `tests/test_cli.py` | CLI interface | **have** |
| TP-CLI-02 | `video-speed --help` / module `--help` lists usage | `tests/test_cli.py` | CLI interface | **have** |
| TP-CLI-03 | Empty argv starts interactive session (banner) when TTY fed | `tests/test_cli.py` | CLI · domain | **todo** |
| TP-CLI-04 | No MP4 in folder → clear message, non-success path | `tests/test_cli.py` | CLI · error-handling | **have** |
| TP-CLI-05 | Invalid video index re-prompts (not crash) | `tests/test_cli.py` | error-handling | **todo** |
| TP-CLI-06 | Batch `--file`/`--start`/`--end`; missing file / incomplete flags fail closed | `tests/test_cli.py` | CLI · domain | **have** |
| TP-CLI-07 | `help` lists the nine product verbs and the word pip, and does not list `hello`; an unknown verb, including `hello`, exits 1 and does not open the menu | `tests/test_cli.py` | requirement-python-cli-interface · requirement-python-interactive-vs-noninteractive | **have** |
| TP-SELF-01 | `version` is local. `version-check`, `self-update`, `self-install`, and `self-uninstall --force` call pip. No `sudo`. No network in the suite | `tests/test_cli.py` | requirement-python-cli-interface | **have** |

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
| TP-MODE-08 | `about` and `help` do not ask for a folder or a file, with or without a terminal | `tests/test_cli.py` | requirement-python-interactive-vs-noninteractive · requirement-python-about | **have** |
| TP-MODE-09 | Empty argv and `--verbose` alone, with both streams terminals, open the menu. `version`, `about`, and `help` do not | `tests/test_cli.py` | requirement-python-interactive-vs-noninteractive | **have** |

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
| TP-JSON-06 | Every product verb with `--json` writes one object and does not open the menu. `help --json` writes usage to stderr. Lifecycle verbs use a fake pip runner | `tests/test_json.py` | requirement-python-json-output | **have** |

### TP-TUI (text menu / default TUI style)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-TUI-01 | Three-row rounded frame, full width, block caret, status line, no `Choice:` | `tests/test_tui.py` | requirement-python-tui | **have** |
| TP-TUI-02 | This board’s number / verb / explain pads, plus two-digit and three-digit pads from `VideoSpeed.tui` | `tests/test_tui.py` | requirement-python-tui | **have** |
| TP-TUI-03 | Too-small screen fails closed; product source does not import or declare an external menu package | `tests/test_tui.py` | requirement-python-tui | **have** |
| TP-TUI-04 | edit stays and asks the folder line inside the frame; Exit leaves; unknown token stays; about result omits the frame | `tests/test_tui.py` | requirement-python-tui | **have** |
| TP-TUI-05 | The front board does not list hello, and choosing 7 stays on that board | `tests/test_tui.py` | requirement-python-tui | **have** |
| TP-TUI-06 | Row **8** opens self-management. **84** version-check runs `python -m pip index versions` with no `sudo` | `tests/test_tui.py` | requirement-python-tui | **have** |
| TP-TUI-07 | First menu row starts with `Path:` plus the absolute current working directory. Traditional Chinese label is `路徑` from the menu-language requirement. The row does not show the product name or version | `tests/test_tui.py` | requirement-python-tui | **have** |
| TP-TUI-08 | The 1.2.4 login field is withdrawn. The path line does not draw `Current:` and does not read the Current User ladder | `tests/test_tui.py` | requirement-python-tui | **have** |
| TP-TUI-09 | When the first row has room, the local clock `HH:MM:SS` ends on the last placeable column. A row that cannot hold both keeps the path and omits the clock. Result pages and edit questions keep the product title on row 0 | `tests/test_tui.py` | requirement-python-tui | **have** |
| TP-TUI-10 | While the front board is showing, one second with no key draws the clock again and does not leave. A key that arrives is still delivered. A result page does not use that wait. The session does not start a thread | `tests/test_tui.py` | requirement-python-tui | **have** |
| TP-TUI-11 | Row **6** opens system-log. **61** lists a `.log` file and shows it. **62** asks `Clear <name>? (y/n)` and empties that file. **63** shows `logDir()`. The read and the empty log `component` `menu` | `tests/test_tui.py` | requirement-python-tui | **have** |
| TP-TUI-12 | The view-log file list and the clear-log questions clear the one-second clock wait. A no-key from that wait does not return to the system-log board. The chosen file is still shown. Esc is still a real key | `tests/test_tui.py` | requirement-python-tui | **have** |
| TP-TUI-13 | Display columns. Wide and Fullwidth are two. Ambiguous stays one. The colon’s column is the display column after the short on the Simplified Chinese, Traditional Chinese, Korean, and Japanese front boards. A path label `路径`, `路徑`, or `경로` keeps the clock on the same row. A joined string is not this proof | `tests/test_tui.py` | requirement-python-tui | **have** |

### TP-LANG (menu language)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-LANG-01 | Front **4** opens the language board (**41**–**53**). Reserved **40** and **54**–**59** do not write. The file is mode **0600**. A bad line stays English and is not rewritten. `VIDEOSPEED_LANG` overrides without writing. **0** Back does not write. A failed write leaves the previous language | `tests/test_tui.py` | requirement-python-cli-language | **have** |

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
| TP-ABOUT-09 | Under pyenv, `pyenv location` is `{root}/bin/pyenv`, and python2 and python3 are inside that root. The about page shows those paths. The check does not spawn | `tests/test_about.py` | requirement-python-pyenv · requirement-python-about | **have** |
| TP-ABOUT-10 | A `PYENV_ROOT` with no `bin/pyenv` is not under pyenv. The three lines stay on `shutil.which` | `tests/test_about.py` | requirement-python-pyenv · requirement-python-about | **have** |
| TP-ABOUT-11 | Under conda, `conda location` is `{root}/bin/conda`, and python2 and python3 are inside the active prefix. Conda wins those two lines over pyenv. The about page shows those paths. The check does not spawn | `tests/test_about.py` | requirement-python-conda · requirement-python-about | **have** |
| TP-ABOUT-12 | A `CONDA_EXE` that is not `bin/conda` or `condabin/conda` is not under conda, even when a login install exists. The lines stay on `shutil.which` | `tests/test_about.py` | requirement-python-conda · requirement-python-about | **have** |
| TP-ABOUT-13 | `PID`, the four cache lines, persistence, and `TTY / Interactive` appear after `Location`. Building the check does not create those directories | `tests/test_about.py` | requirement-python-about | **have** |
| TP-ABOUT-14 | Cache folder used follows `/dev/shm`, then `/tmp`, then the 2nd fallback. The 2nd leaf has no username | `tests/test_about.py` | requirement-python-about | **have** |
| TP-ABOUT-15 | `video-speed about --json` writes the three blocks to the error stream only. Standard output is one JSON object, `jobs` empty, `mode` `noninteractive`, with no `[CHECK SYSTEM]:`. On a terminal stdout, `TTY / Interactive` is `yes` | `tests/test_about.py` | requirement-python-about · requirement-python-json-output | **have** |
| TP-ABOUT-16 | `CheckSystem.in_venv`, `in_pyenv`, and `in_conda` return the stored logger’s `inVenv()`, `inPyenv()`, and `inConda()`. An absent logger is false. Those booleans do not replace `under_pyenv` or `under_conda` | `tests/test_about.py` | requirement-python-cli-logging · requirement-python-oop | **have** |

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
| TP-STYLE-01 | Identity, formatted version, verb lists, and bounds (`_PKG_VERSION`, `APP_NAME`, `CONSOLE_NAME`, `PRODUCT_VERBS`, `LIFECYCLE_VERBS`, `AUTHOR_NAME`, `HOMEPAGE`, `LAST_UPDATE`, `DOWNLOAD_URL`, `BASIC_USAGE`, `RATIO_MIN`, `RATIO_MAX`) are attributes of class `Cli`, not module assignments. The message sink is `RunOutput` | `tests/test_docs.py` | coding-style · requirement-python-oop | **have** |
| TP-STYLE-02 | Ship modules and the suite read and write attributes by name. They do not use `__dict__` unless the user ordered that access for that edit | `tests/test_docs.py` | coding-style | **have** |
| TP-OOP-01 | Class `Tui` lives in `src/VideoSpeed/tui.py` and owns the text-menu session. Those functions are not defined in `cli.py`. The painter split is TP-OOP-03 | `tests/test_tui.py` | requirement-python-oop | **have** |
| TP-OOP-02 | Class `CheckSystem` lives in `src/VideoSpeed/check_system.py` and owns the host-check functions. Those functions are not defined in `cli.py` | `tests/test_about.py` | requirement-python-oop | **have** |
| TP-OOP-03 | `paint`, `format_rows`, and the frame glyphs are methods or constants of `MenuPainter`. `MenuModel` and `MenuSession` are their own modules. `tui.py` defines class `Tui` only | `tests/test_tui.py` | requirement-python-oop | **have** |
| TP-OOP-04 | `cli.py` defines class `Cli` and `def main`. Encoder, file stage, media info, about page, edit walk, and run output are not module-level functions there | `tests/test_cli.py` | requirement-python-oop | **have** |

The logger parameter on each class `__init__` is `TP-LOG-05` (**have**). `requirement-python-oop` does not add `TP-OOP-05`.

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
| TP-DOC-03 | README section headings including Advantages, the comparison table, screenshot links, each catalog paragraph and alt, path-row clock sentence, named setup script exists, wheel example matches the built distribution name | `tests/test_docs.py` | requirement-python-readme | **todo** |

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
