# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.4/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-12-03

### Added
- Initial public release of `video-speed`
- Full-featured logging system via `ChronicleLogger` with:
  - Daily log rotation (YYYYMMDD-based filenames)
  - Automatic archiving of logs older than 7 days (`.tar.gz`)
  - Automatic removal of logs older than 30 days
  - Smart log directory selection:
    - `/var/log/<appname>` when running as root
    - `~/.app/<appname>/log` for regular users
- `Sudoer` utility class with safe sudo detection and user warning
- Console script entrypoint: `video-speed`
  - Run `video-speed info` to display basic application info
- Comprehensive cross-Python compatibility:
  - Python 2.7 and Python 3.5–3.14 supported
  - Tested on Linux and macOS
- MIT-licensed open source project
- Complete packaging setup using `pyproject.toml` + `setuptools`
- POSIX-compliant build script (`build.sh`) with commands:
  - `setup`, `clean`, `build`, `upload`, `test`, `release`, `tag`, `git`
- Editable/development install support (`pip install -e .`)

### Security
- `Sudoer.has_sudo()` displays a clear warning before prompting for password
- No password collection or logging — designed to be audit-safe

### Documentation
- `README.md` with installation and usage instructions
- Design specification: `docs/VideoSpeed-spec.md`
- This `CHANGELOG.md`

This is the foundational release intended as a robust, production-ready logging template that can be dropped into any Python project (including Cython-based ones).