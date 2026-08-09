# VideoSpeed - Cut, speed, and boomerang MP4 clips from the CLI

![Version](https://img.shields.io/badge/Version-1.0.5-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
[![CIAO](https://img.shields.io/badge/Philosophy-CIAO%20(Caution%20%E2%80%A2%20Intentional%20%E2%80%A2%20Anti--fragile%20%E2%80%A2%20Over--engineered)-purple.svg)](https://github.com/cloudgen/ciao)
[![Stars](https://img.shields.io/github/stars/Wilgat/VideoSpeed?style=flat-square)](https://github.com/Wilgat/VideoSpeed)
[![Python](https://img.shields.io/badge/Python-2.7%2B-blue?style=flat-square)]()
[![PyPI](https://img.shields.io/pypi/v/VideoSpeed?style=flat-square)](https://pypi.org/project/VideoSpeed/)

VideoSpeed is an interactive command-line tool for short MP4 edits: pick a folder of videos, cut a time range, change length/speed (percent), and optionally append a boomerang (forward + reverse). Encoding uses **FFmpeg**; duration probing uses **OpenCV**.

Package version SSOT: `pyproject.toml` and `src/VideoSpeed/__init__.py` (**1.0.5**). Console entrypoint: `video-speed`.

## Features

- Recursive **MP4** discovery under a chosen folder
- Interactive **cut** (start/end seconds) with invalid-range re-prompt
- **Length/speed** change (**20–200%**) with A/V tempo kept in sync
- Optional **boomerang** (forward then reverse)
- **USB-safe** intermediate files (staged next to the output) and final publish via `shutil.move`
- **`--help`** / **`--version`**; bare invoke starts the interactive session (Type N)
- Fail-closed when **FFmpeg** is missing from `PATH`

## Quick Installation

### Prerequisites (system)

- **FFmpeg** on `PATH` (`ffmpeg -version`)
- A supported **Python** environment (see `requires-python` in `pyproject.toml`)

### From PyPI (registry channel)

Package name SSOT: **`VideoSpeed`** (`pyproject.toml` `[project].name`). Upload path: `build.sh` (`twine upload`).

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

This installs the console script **`video-speed`** and pulls Python deps (`opencv-python`, `ChronicleLogger`, …).

### From a local wheel / sdist

```bash
# after: python -m build   (or ./build.sh build)
pip install dist/VideoSpeed-1.0.5-py3-none-any.whl
# or
pip install dist/VideoSpeed-1.0.5.tar.gz
```

### Verify

```bash
video-speed --version
# or
python -m VideoSpeed --version
```

## Usage

Interactive editor (default):

```bash
video-speed
# or
python -m VideoSpeed
```

1. Folder containing MP4s (Enter = current directory)
2. Choose a video by number
3. Cut start/end seconds
4. New length percent (default 100; allowed 20–200)
5. Optional boomerang (y/n)
6. Output is written **next to the source** with a descriptive name

Other:

```bash
video-speed --help
video-speed --version
```

## Examples

```bash
# Install editable, then run interactive session in a folder of clips
cd /path/to/videos
video-speed

# Check identity without starting prompts
video-speed --version
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

Fork the repository, use a checkout install (`pip install -e .`), and open a pull request. Prefer small, tested changes. Do not strip defensive temp/publish behavior (cross-filesystem `shutil.move`) without an explicit redesign.

## License

MIT License — see [`LICENSE.md`](LICENSE.md).

## Last Update

2026-08-09 — README aligned with product **1.0.5**, write-readme detection-driven banners (Version / License / CIAO / Stars / Python / PyPI), and install truth (PyPI + editable + wheel).
