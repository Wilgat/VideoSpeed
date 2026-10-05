# Requirements index

**Product:** VideoSpeed (Python interactive CLI — cut / speed / optional boomerang for MP4)  
**Workspace state:** Specialized product law (left genesis); **software-development** class; **pip/local package** install (not shell online Type 0).  
**Updated:** 2026-10-05

| ID / key | Title | Area | Status | Path | Updated |
|----------|-------|------|--------|------|---------|
| requirement-class-software-dev | Software-development class law + residual stack (Python, setuptools) | class | Active | `requirement-class-software-dev.md` | 2026-10-02 |
| requirement-domain-videospeed | Domain surface SSOT (four pillars: workflow, features, help, about). VERSION `1.0.12` | domain | Active | `requirement-domain-videospeed.md` | 2026-10-05 |
| requirement-video-ffmpeg-pipeline | FFmpeg ops SSOT (cut → speed → optional boomerang; temps) | video | Active | `requirement-video-ffmpeg-pipeline.md` | 2026-10-01 |
| requirement-python-cli-interface | CLI entry points, product verbs (including self-management), and `main` order. Each verb's default route is the terminal unless the mode file names the screen. `--verbose` shows the console mirror except on `--json` and a text screen. Every product verb accepts `--json` | python | Active | `requirement-python-cli-interface.md` | 2026-10-05 |
| requirement-python-interactive-vs-noninteractive | Menu walk is the no-verb entry. `edit` and `list-mp4` are the named screen verbs. Other product verbs stay on the terminal. `--verbose` alone stays on the menu. There is no `--quiet` | python | Active | `requirement-python-interactive-vs-noninteractive.md` | 2026-10-05 |
| requirement-python-json-output | `--json` on every product verb quiets stdout to one object and skips the text menu. The flags `--help` and `--version` stay human | python | Active | `requirement-python-json-output.md` | 2026-10-05 |
| requirement-python-tui | Text menu: default TUI style. The screen is the no-verb entry. Top line keeps the path on the left and a local clock on the right when the row has room. Verb pad, colon column, and path row use display columns (Wide and Fullwidth are two; Ambiguous stays one). The clock is drawn again each second on the boards only. A view-log or clear-log question does not use that wait. Front **4** is language. Front **6** is system-log. Front **8** is self-management. Status-line sample is `1.0.12` | python | Active | `requirement-python-tui.md` | 2026-10-05 |
| requirement-python-cli-language | Menu language: front **4** opens thirteen codes **41**–**53**. The column pad in the samples is display columns. The choice is one line under this login’s persistence directory. `VIDEOSPEED_LANG` wins at process start and does not write. System-log is front **6** | python | Active | `requirement-python-cli-language.md` | 2026-10-04 |
| requirement-python-about | About page: identity, host check, star box, the read for each line, and the stream under `--json`. Sample version `1.0.12` | python | Active | `requirement-python-about.md` | 2026-10-05 |
| requirement-python-packaging | `pyproject.toml` / version / console script packaging. Package string `1.0.12` | python | Active | `requirement-python-packaging.md` | 2026-10-05 |
| requirement-python-build-script | Maintainer `build.sh` verbs. Tag example `v1.0.12` | python | Active | `requirement-python-build-script.md` | 2026-10-05 |
| requirement-python-version | Version SSOT: MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION. Package string `1.0.12` | python | Active | `requirement-python-version.md` | 2026-10-05 |
| requirement-python-dependency-management | Pip floors for headless OpenCV and ChronicleLogger | python | Active | `requirement-python-dependency-management.md` | 2026-10-01 |
| requirement-python-project-structure | Repository and `src/VideoSpeed` layout | python | Active | `requirement-python-project-structure.md` | 2026-10-04 |
| requirement-python-error-handling | Fail-closed errors; source-safe cleanup | python | Active | `requirement-python-error-handling.md` | 2026-10-01 |
| requirement-python-cli-logging | `def main` instantiates ChronicleLogger by writing `ChronicleLogger(...)`. The console mirror stays off unless `--verbose` is set on a run that is not `--json` and not a text screen. System status (one logger, level, component, major file operations, thread create and thread operations). The host check reads in-venv, in-pyenv, and in-conda from that logger. The log folder is `logDir()`: conda, else pyenv, else venv, else `~/.app/video-speed/log`, or `/var/video-speed/log` when root and none of those are active. The about host check is not a logger line | python | Active | `requirement-python-cli-logging.md` | 2026-10-05 |
| requirement-python-graceful-exit | Control-C asks `Exit? (y/n)` on an open text screen, logs the decision, and exits 130 on yes. A live FFmpeg child is stopped and not published first | python | Active | `requirement-python-graceful-exit.md` | 2026-10-02 |
| requirement-python-coding-style | Python style; temps; **shutil.move**; no `os.rename` or `os.replace`; no import-time static `raise`; identity, verb lists, and bounds are attributes of class `Cli`; one class per file; `ClassName(...)` at the site; a factory (a function or a method that instantiates a class) is banned; attribute access by name; no `__dict__` unless the user orders that access | python | Active | `requirement-python-coding-style.md` | 2026-10-02 |
| requirement-python-oop | One class per file; `def main` stays in `cli.py`; each class `__init__` receives the logger; class `Cli` owns its constants; the site writes `ClassName(...)`; a factory is not in the map; `SystemLog` owns the log-file list, the read, and the empty; `LanguageMenu` owns the menu language file and the words; `TP-OOP-01` through `TP-OOP-04` have landed | python | Active | `requirement-python-oop.md` | 2026-10-04 |
| requirement-runtime-prerequisites | Host FFmpeg + pip deps; no root auto-install claim. Product version `1.0.12` | runtime | Active | `requirement-runtime-prerequisites.md` | 2026-10-05 |
| requirement-python-pyenv | Under pyenv, about shows python2 and python3 inside that root, and pyenv location is bin/pyenv. `in_pyenv` does not replace that root test | python | Active | `requirement-python-pyenv.md` | 2026-10-02 |
| requirement-python-conda | Under conda, about shows python2 and python3 inside that prefix, and conda location is bin/conda. `in_conda` does not replace that root test | python | Active | `requirement-python-conda.md` | 2026-10-02 |
| requirement-python-readme | User document at root `README.md`: section order, Advantages, related projects, badges, install honesty, absolute `https` image destinations, and one paragraph plus alt per screenshot. A capture that shows a version shows the package string. The PyPI project link is the badge href in that document. Behavior stays on the peer that owns it | python | Active | `requirement-python-readme.md` | 2026-10-05 |

## Intentionally absent (by design)

| Surface | Status on VideoSpeed |
|---------|----------------------|
| Shell online install / `SCRIPT_URL` / Type O empty-argv install-ensure | **Absent** |
| Shell local `install` / `uninstall` / channel self-update Type 0 package | **Absent** (pip package). Python `version-check` and `self-update` call pip (`requirement-python-cli-interface`) |
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
