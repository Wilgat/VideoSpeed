# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.11] - 2026-10-04

### Added
- Front menu **4** is **language**. It opens **41** English through **53** Ελληνικά, and **0** Back. The choice is one line in this login’s persistence directory and is kept for the next run. English is the default. **0** does not write. `VIDEOSPEED_LANG` wins for this process and does not write. Front **6** is **system-log**. It opens **61** view-log, **62** clear-log, **63** log-folder, and **0** Back. **view-log** lists the `.log` files and shows the chosen file. **clear-log** empties the chosen file after `Clear <name>? (y/n)` and does not delete it. **log-folder** shows the folder `logDir()` returns.
- The first menu row keeps `Path` and the current directory on the left and a local clock (`HH:MM:SS`) on the right when the row has room. The clock is drawn again each second.
- The about page, after Location, prints PID, the cache folder chain, persistence storage, and TTY / Interactive. Under conda, `python2` and `python3` stay inside that prefix, and conda location is `bin/conda`. `about --json` writes that page to the error stream. Standard output stays the JSON object.

### Removed
- The command-line verb `hello`. `video-speed hello` is an unknown verb: it exits 1, names the remaining verbs, and does not print `Hello.`. The numbered menu still has no hello row.

## [1.0.10] - 2026-10-02

### Added
- Front menu **8** is **self-management**. It opens **82** version, **83** about, **84** version-check, **85** self-update, **86** self-uninstall, **87** self-install, and **0** Back.
- Product verbs `version`, `self-install`, `version-check`, `self-update`, and `self-uninstall`. `help` and `version` are self-management verbs in the shell sense and in this Python CLI and text menu. `help` is not a numbered row.
- `version` prints the installed version and does not use the network. `version-check` runs `python -m pip index versions VideoSpeed`. `self-update` runs `python -m pip install --upgrade VideoSpeed`. `self-install` runs `python -m pip install VideoSpeed`. `self-uninstall` runs `python -m pip uninstall -y VideoSpeed` and, on the command line, requires `--force`. The text-menu row is the confirmation. These commands do not use `sudo` or `curl`.
- When this login has pyenv, the about host check prints `python2` and `python3` inside that root, and `pyenv location` is `bin/pyenv`.

## [1.0.9] - 2026-10-01

### Changed
- `main` builds one ChronicleLogger before the argument parser, in the same order as AnimeDlp: `logname`, then `logName()`, `baseDir()`, and `logDir()`.
- When `DEBUG` is already `1`, `true`, or `show`, a non-TUI, non-JSON run displays `debug mode` with the version line and `ChronicleLogger.class_version()`. `--json` and the text screen keep that mirror off the console. The daily log still records the lines.
- That same logger is passed into every class. Each object stores it and logs `instantiated` under its class name. A non-TUI, non-JSON run shows those lines. `--json` and the text screen keep them off the console. The daily log still records them.

## [1.0.8] - 2026-10-01

### Changed
- Each class lives in its own module. `def main` stays in `src/VideoSpeed/cli.py` beside class `Cli`. The console script stays `VideoSpeed.cli:main`.
- The text-menu session is class `Tui`. The frame and `MENU_ROWS` are class `MenuPainter`. Keystrokes are class `MenuModel`. The run loop is class `MenuSession`.
- The host check stays class `CheckSystem`. The about page is class `AboutPage` and calls `CheckSystem`.
- Cut, speed, and boomerang are class `Encoder`. MP4 listing and duration are class `MediaInfo`. Staging and `shutil.move` publish are class `FileStage`. User-facing lines and the JSON object are class `RunOutput`. The shared edit questions are class `EditWalk`.

## [1.0.7] - 2026-10-01

### Added
- Positional verbs `help`, `about`, `hello`, `edit`, and `list-mp4` on `video-speed` and `python -m VideoSpeed`. `help` prints the same usage as `--help`. `about` and `hello` print a page and do not ask for a folder or a file. On a terminal, `edit` asks for the folder, then the file, inside the text screen. `list-mp4` lists MP4 files and does not encode.
- An unknown positional verb exits 1 and names those five verbs. `Exit` stays a menu control. `./build.sh` tokens such as `setup` and `test` are not `video-speed` verbs.
- Menu **7 hello**: the result page shows `Hello.`.
- `requirement-python-oop` 1.0.0 names class `Tui` in `src/VideoSpeed/tui.py` and class `CheckSystem` in `src/VideoSpeed/check_system.py`. Those functions still live in `cli.py`, and the painter is still `menu.py`.

### Changed
- File moves use `shutil.move` (`requirement-python-coding-style` 1.2.0). Ship code does not call `os.rename` or `os.replace`, including when the output is on removable media.
- The version-string match is a test (`requirement-python-coding-style` 1.3.0). Importing the CLI does not raise if the formatted triple and `__version__` differ.
- `main` constructs ChronicleLogger before the argument parser (`requirement-python-cli-logging` 1.0.2). When `DEBUG` is `1`, `true`, or `show`, it displays the version and the ChronicleLogger version. When debug mode is off, those lines stay off.

### Fixed
- Interactive edit at full length, 100%, and no boomerang no longer sits on a second encode. The cut is published under the final name, and the text screen shows `Saved <filename> — Again? (y/n):`.

## [1.0.6] - 2026-10-01

### Added
- Menu **8 about** (`requirement-python-about`): identity lines, the host check, and the star box.
- `--json` (`requirement-python-json-output`): one JSON object on standard output. Questions, when the walk runs, go to the error stream. `--help` and `--version` stay human text.
- `./build.sh` verbs (`requirement-python-build-script`): `help`, `version`, `setup`, `clean`, `build`, `upload`, `git`, `tag`, `release`, `all`, `test-install`, and `test`. `test` runs `tests/run.sh`. `release` and `all` are clean, then build, then upload, then tag.
- Mode matrix (`requirement-python-interactive-vs-noninteractive`). After `--help` and `--version`, `main` chooses the text-menu walk, one job (`--file`, `--start`, `--end`), or a fail-closed stop. A lone `--percent` or `--boomerang` exits 1.
- Version SSOT (`requirement-python-version`): `MAJOR_VERSION`, `MINOR_VERSION`, and `PATCH_VERSION` in `src/VideoSpeed/__init__.py` (`1.0.6`).
- `main` order (`requirement-python-cli-interface`): version, ChronicleLogger, debug, missing major imports, then the argument parser.
- System-status logs (`requirement-python-cli-logging`). One ChronicleLogger (`logname="VideoSpeed"`). Pip floor `ChronicleLogger>=1.3.1`.
- Text menu (`requirement-python-tui`) painted by `src/VideoSpeed/menu.py`. No arguments in a terminal opens **edit**, **about**, and **Exit**.
- Non-interactive job flags: `--file`, `--start`, `--end`, optional `--percent` / `--boomerang`, and `--folder`.
- Automated suite under `tests/` (`./tests/run.sh`).
- Product-root `SECURITY.md` and product-root `CHANGELOG.md`.
- `requires-python` is `>=3.11`.

### Changed
- Runtime pip floors are `opencv-python-headless>=5.0.0.93` and `ChronicleLogger>=1.3.1`. The GUI wheel `opencv-python` is not a dependency. `py-tui` is not a dependency.
- Main-menu **edit** stays inside the text screen. Esc returns to the menu.
- `setup.sh` installs this checkout with pip into the interpreter selected by `pyenv shell 3.14`.
- `.gitignore` tracks `docs/requirements/**` and ignores harness trees.
- No arguments without a terminal fail closed.

## [1.0.5] - 2026-08-09

### Fixed
- Cross-filesystem / USB publish: stage temps next to the output path and publish with `shutil.move` (no bare `os.replace` from system temp onto removable media).
- Package import no longer requires OpenCV at import time (`__init__.py` version-only).
- FFmpeg missing on PATH fails closed before encode; invalid cut range and length % outside 20–200% re-prompt without encoding.
- Boomerang intermediate cleanup on failure paths; chained `atempo` for extreme rates.

### Added
- CLI `--help` and `--version` (bare invoke remains interactive Type N session).
- Product requirements under `docs/requirements/` and public `reviews/` test plan / lessons surface.

### Changed
- Specialized interactive CLI from bootstrap archive (`cli.bootstrap-old.py`); ship SSOT remains `src/VideoSpeed/cli.py`.

## [0.1.0] - 2025-12-03

Historical bootstrap / packaging template release (logging-template heritage). Current ship unit is the 1.0.x interactive cut/speed/boomerang CLI.

### Added
- Initial public release of `video-speed`
- Console script entrypoint and `pyproject.toml` packaging
- MIT license
