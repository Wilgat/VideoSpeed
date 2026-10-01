# VideoSpeed - Cut, speed, and boomerang MP4 clips from the CLI

![Version](https://img.shields.io/badge/Version-1.0.6-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
[![CIAO](https://img.shields.io/badge/Philosophy-CIAO%20(Caution%20%E2%80%A2%20Intentional%20%E2%80%A2%20Anti--fragile%20%E2%80%A2%20Over--engineered)-purple.svg)](https://github.com/cloudgen/ciao)
[![Stars](https://img.shields.io/github/stars/Wilgat/VideoSpeed?style=flat-square)](https://github.com/Wilgat/VideoSpeed)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square)]()
[![PyPI](https://img.shields.io/pypi/v/VideoSpeed?style=flat-square)](https://pypi.org/project/VideoSpeed/)

VideoSpeed cuts a time range from an MP4, changes that clip’s length (percent), and can append a reverse pass (boomerang). On a terminal, no arguments opens a text menu (edit, about, Exit). Choosing edit walks through the prompts. Scripts pass `--file` / `--start` / `--end`. Encoding uses **FFmpeg**; duration probing uses **OpenCV**. The menu screen uses the default text-menu style: aligned number, verb, and note, and a rounded box along the bottom.

| You | The other role | Not this |
|-----|----------------|----------|
| Editor at a terminal or a script | FFmpeg on `PATH` (does the encode) | A website, installer, or root/sudo tool |

Package version SSOT: `src/VideoSpeed/__init__.py` (`MAJOR_VERSION`, `MINOR_VERSION`, `PATCH_VERSION` → **1.0.6**). `pyproject.toml` copies that string. Console entrypoint: `video-speed`.

## Features

- Recursive **MP4** discovery under a chosen folder
- Interactive **cut** (start/end seconds) with invalid-range re-prompt
- **Length/speed** change (**20–200%**) with A/V tempo kept in sync
- Optional **boomerang** (forward then reverse)
- **USB-safe** intermediate files (staged next to the output) and final publish via `shutil.move`
- **Text menu** on a terminal (`edit`, `about`, `Exit`): columns line up, and a three-row rounded input box sits on the bottom with a status line under it
- **`--help`** / **`--version`**; no arguments in a terminal opens that menu, and **edit** starts the interactive editor
- Non-interactive job: `--file`, `--start`, `--end`, optional `--percent` / `--boomerang`. Any of `--file`, `--start`, `--end`, or `--folder` skips the menu
- Fail-closed when **FFmpeg** is missing from `PATH`, when prompts are needed without a terminal, or when `--percent` or `--boomerang` is passed without a job

## Quick Installation

### Prerequisites (system)

- **FFmpeg** on `PATH` (`ffmpeg -version`)
- A supported **Python** environment (see `requires-python` in `pyproject.toml`)

### From PyPI (registry channel)

Package name SSOT: **`VideoSpeed`** (`pyproject.toml` `[project].name`). Maintainer verbs are on `./build.sh`: `help`, `version`, `setup`, `clean`, `build`, `test`, `test-install`, `upload`, `git`, `tag`, `release` (`all` is the same chain as `release`). `test` runs `tests/run.sh`. `test-install` reads `[project].name`, removes that pip install when present, and installs this checkout. Empty `./build.sh` prints help and does not upload.

```bash
pip install VideoSpeed
```

If the index is behind a local release, install from a checkout or wheel instead (below). Live index version is shown by the PyPI badge above.

### From a git checkout (development)

```bash
git clone git@github.com:Wilgat/VideoSpeed.git
cd VideoSpeed
pip install -e .
```

This installs the console script **`video-speed`** and pulls Python deps (`opencv-python-headless>=5.0.0.93`, `ChronicleLogger>=1.3.1`).

### Local pyenv install (testing)

```sh
./setup.sh
pyenv shell 3.14
video-speed --version
```

`setup.sh` runs `pyenv shell 3.14` and installs this checkout with pip into that interpreter. Install CPython 3.14 first when it is missing (`pyenv install 3.14`). Run `./setup.sh` again after source changes. In the shell where you want the command:

```sh
pyenv shell 3.14
video-speed --help
```

The console script is installed on the pyenv 3.14 prefix. `./setup.sh` changes that interpreter only. It does not install FFmpeg and it does not use root.

### From a local wheel / sdist

```bash
# after: python -m build   (or ./build.sh build)
pip install dist/VideoSpeed-1.0.6-py3-none-any.whl
# or
pip install dist/VideoSpeed-1.0.6.tar.gz
```

### Verify

```bash
video-speed --version
# or
python -m VideoSpeed --version
```

## Usage

Text menu (no arguments, in a terminal):

```bash
video-speed
# or
python -m VideoSpeed
```

The screen shows a numbered menu and a rounded input box along the bottom, as wide as the terminal, with one line to type on and a status line under the box. **edit** continues the prompts. **about** shows the product. **Exit** leaves.

1. Folder containing MP4s (Enter = current directory)
2. Choose a video by number
3. Cut start/end seconds
4. New length percent (default 100; allowed 20–200)
5. Optional boomerang (y/n)
6. Output is written **next to the source** with a descriptive name

Non-interactive job (scripts / CI):

```bash
video-speed --file clip.mp4 --start 1 --end 5 --percent 100
video-speed --file clip.mp4 --start 1 --end 5 --percent 50 --boomerang
```

Other:

```bash
video-speed --help
video-speed --version
```

Without a terminal and without a job, the program exits with an error instead of hanging on prompts. `--percent` or `--boomerang` alone does the same and names `--file`, `--start`, and `--end`. `--folder` checks the directory. It does not pick a file.

`--json` keeps that same choice, closes the text menu, and prints one JSON object on standard output. On a terminal with no job flags, the questions are written to the error stream. Progress is not mixed into the object.

## Examples

```bash
# Install editable, then run interactive session in a folder of clips
cd /path/to/videos
video-speed

# Check identity without starting prompts
video-speed --version

# One-shot job (no prompts)
video-speed --file clip.mp4 --start 1.0 --end 5.0 --percent 100
```

Example output name shape:

```text
clip_cut1.0-5.0s_100pct.mp4
clip_cut1.0-5.0s_50pct_BOOMERANG.mp4
```

## Platform Compatibility

| Platform | Status |
|----------|--------|
| Linux | Primary (tested in development) |
| macOS / Windows | Expected to work when Python, FFmpeg, and OpenCV are available |
| Filesystems | Local disk and removable/USB volumes supported for output (temps staged beside final path) |

## Related Projects

- [VideoSpeed on GitHub](https://github.com/Wilgat/VideoSpeed)
- [VideoSpeed on PyPI](https://pypi.org/project/VideoSpeed/)

## Contributing

Fork the repository, use a checkout install (`pip install -e .` or `./setup.sh`), and open a pull request. Prefer small, tested changes. Do not strip defensive temp/publish behavior (cross-filesystem `shutil.move`) without an explicit redesign.

## License

MIT License — see [`LICENSE.md`](LICENSE.md).

## Last Update

2026-10-01 — **1.0.6**: text menu (edit, about, Exit), `--json`, job flags, and `./build.sh` maintainer verbs.
