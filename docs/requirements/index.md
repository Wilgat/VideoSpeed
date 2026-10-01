# Requirements index

**Product:** VideoSpeed (Python interactive CLI — cut / speed / optional boomerang for MP4)  
**Workspace state:** Specialized product law (left genesis); **software-development** class; **pip/local package** install (not shell online Type 0).  
**Updated:** 2026-10-01

| ID / key | Title | Area | Status | Path | Updated |
|----------|-------|------|--------|------|---------|
| requirement-class-software-dev | Software-development class law + residual stack (Python, setuptools) | class | Active | `requirement-class-software-dev.md` | 2026-10-01 |
| requirement-domain-videospeed | Domain surface SSOT (four pillars: workflow, features, help, about) | domain | Active | `requirement-domain-videospeed.md` | 2026-10-01 |
| requirement-video-ffmpeg-pipeline | FFmpeg ops SSOT (cut → speed → optional boomerang; temps) | video | Active | `requirement-video-ffmpeg-pipeline.md` | 2026-10-01 |
| requirement-python-cli-interface | CLI entry points, product verbs (`help`, `about`, `hello`, `edit`, `list-mp4`), and `main` order | python | Active | `requirement-python-cli-interface.md` | 2026-10-01 |
| requirement-python-interactive-vs-noninteractive | Menu walk, product verb (folder then file), or one non-interactive job | python | Active | `requirement-python-interactive-vs-noninteractive.md` | 2026-10-01 |
| requirement-python-json-output | `--json` quiets stdout to one object and skips the text menu | python | Active | `requirement-python-json-output.md` | 2026-10-01 |
| requirement-python-tui | Text menu: default TUI style. A product verb enters that action without a front-board pick | python | Active | `requirement-python-tui.md` | 2026-10-01 |
| requirement-python-about | About page: identity, host check, star box, and how each line is read | python | Active | `requirement-python-about.md` | 2026-10-01 |
| requirement-python-packaging | `pyproject.toml` / version / console script packaging | python | Active | `requirement-python-packaging.md` | 2026-10-01 |
| requirement-python-build-script | Maintainer `build.sh` verbs | python | Active | `requirement-python-build-script.md` | 2026-10-01 |
| requirement-python-version | Version SSOT: MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION | python | Active | `requirement-python-version.md` | 2026-10-01 |
| requirement-python-dependency-management | Pip floors for headless OpenCV and ChronicleLogger | python | Active | `requirement-python-dependency-management.md` | 2026-10-01 |
| requirement-python-project-structure | Repository and `src/VideoSpeed` layout | python | Active | `requirement-python-project-structure.md` | 2026-10-01 |
| requirement-python-error-handling | Fail-closed errors; source-safe cleanup | python | Active | `requirement-python-error-handling.md` | 2026-10-01 |
| requirement-python-cli-logging | System status via ChronicleLogger (one logger, level, component, major file operations, thread create and thread operations) | python | Active | `requirement-python-cli-logging.md` | 2026-10-01 |
| requirement-python-graceful-exit | Control-C during a long FFmpeg child: stop, do not publish, exit 130 | python | Active | `requirement-python-graceful-exit.md` | 2026-10-01 |
| requirement-python-coding-style | Python style; temps; **shutil.move**; no `os.rename` or `os.replace`; no import-time static `raise`; identity locals belong in `main()`; one class per file | python | Active | `requirement-python-coding-style.md` | 2026-10-01 |
| requirement-python-oop | One class per file; `def main` stays in `cli.py`; each class `__init__` receives the logger; `TP-OOP-01` through `TP-OOP-04` have landed | python | Active | `requirement-python-oop.md` | 2026-10-01 |
| requirement-runtime-prerequisites | Host FFmpeg + pip deps; no root auto-install claim | runtime | Active | `requirement-runtime-prerequisites.md` | 2026-10-01 |

## Intentionally absent (by design)

| Surface | Status on VideoSpeed |
|---------|----------------------|
| Shell online install / `SCRIPT_URL` / Type O empty-argv install-ensure | **Absent** |
| Shell local `install` / `uninstall` / self-update Type 0 package | **Absent** (pip package product) |
| Type 1 sudoers / root elevation allowlist | **Absent** |
| Automatic companion `.sha256` channel integrity law | **Absent** |
| Second Active `requirement-domain-*` | **Forbidden** while domain-videospeed is Active |

**Install mode:** **pip / local package** (`video-speed` console script). Not dual-mode shell+pip install-ensure.

**Rules for agents:**

1. Treat rows above as the **live product-law inventory** for VideoSpeed.  
2. **Do not invent** additional `requirement-*.md` paths — verify on disk and add a registry row in the same change when creating one.  
3. Product source comments cite **only** these live requirement files — never templates/skills as behavioral authority.  
4. This versioned surface lists **requirement rows only** — do not dump templates / skills / terminologies / incidents path inventories here.  
5. Keep Status and Path in sync with each file’s header when status changes.  
6. **Class gate:** software-development requires exactly one Active `requirement-class-software-dev.md` (this registry includes it).  
7. **Domain SSOT:** exactly one Active domain file (`requirement-domain-videospeed`).  
8. **Do not introduce** online shell install or Type 1 elevation without explicit user order and registry update.

When adding a requirement: append a row, create the file under `docs/requirements/`, keep Status in sync with the file header.
