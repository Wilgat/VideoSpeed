# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

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
