**file**: docs/requirements/requirement-python-cli-interface.md  
**Status**: Active (Version 1.7.0)  
**Area**: python  
**Key**: `requirement-python-cli-interface`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define the official **command-line entry points** and the order of `main` for the VideoSpeed Python package. Which path runs after the parser — the menu walk, one job, or a fail-closed stop — is **`requirement-python-interactive-vs-noninteractive`**.

Domain step catalog is owned by **`requirement-domain-videospeed`**. Encode ops are owned by **`requirement-video-ffmpeg-pipeline`**.

### 1.1 Human-facing

**In one sentence:** This file says how you start VideoSpeed (`video-speed` or `python -m VideoSpeed`) and the order inside `main`; the menu walk versus one job is the mode file.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person at a terminal or a script | `video-speed` or `video-speed --file clip.mp4 --start 0 --end 5` |
| The other role | Domain + pipeline peers | What to cut and how FFmpeg runs |
| Not this file | Filter graphs; the three version integers | Pipeline file and `requirement-python-version` |

| Includes | Excludes |
|----------|----------|
| Console script, module entry, `main` order, the flag names | The mode matrix (menu walk versus one job); root/sudo; online install |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/VideoSpeed/cli.py` | ship unit | live behavior |
| `video-speed --help` | command | listed flags |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Edit one clip without prompts | The program must not wait on stdin. It needs a file and a time range. | `video-speed --file clip.mp4 --start 1 --end 5` |
| Walk through prompts | Run with no arguments **in a terminal**. Without a terminal it exits and tells you to pass flags. | `video-speed` |

---

## 2. Core Rules (Mandatory)

### 2.1 Entry points

1. **MUST** expose a console script entry named **`video-speed`** pointing at `VideoSpeed.cli:main` (declared in packaging SSOT).  
2. **MUST** support module execution: **`python -m VideoSpeed`**.  
3. **MUST** keep `main()` as the single runtime entry for the interactive editor session (thin package surface).  
4. **MUST NOT** require root or sudo to run the CLI.

### 2.1a What `main` does, in order

`main` in `src/VideoSpeed/cli.py` **MUST** perform these five steps in this order. `__main__.py` and the console script only call `main` and exit with its code. They **MUST NOT** repeat the steps. The order matches sibling product AnimeDlp’s `main`: version, logger, debug, missing libraries, then the argument parser. AnimeDlp prints `__version__` on the debug line. VideoSpeed prints the same line from `MAJOR_VERSION`, `MINOR_VERSION`, and `PATCH_VERSION` (`requirement-python-version`).

M1. **Step 1 — main’s own version.** **MUST** read `MAJOR_VERSION`, `MINOR_VERSION`, and `PATCH_VERSION` from the package. **MUST NOT** assign a second triple. The string **MUST** equal `__version__`.  
M2. **Step 2 — logger.** **MUST** construct one ChronicleLogger as `requirement-python-cli-logging` requires (`logname="VideoSpeed"`, then `logName()`, `baseDir()`, `logDir()`). If that import fails, **MUST** print the install next step and return `1` before the parser runs.  
M3. **Step 3 — debug.** If `logger.isDebug()` is true, **MUST** log the identity line with the three integers and `ChronicleLogger.class_version()`, `component="main"`. `DEBUG` must already be set before step 2.  
M4. **Step 4 — major import missing.** **MUST** use the AnimeDlp gate: `log_message` at `FATAL`, `component="main"`, then `return 1`. ChronicleLogger is that gate at step 2. OpenCV (`cv2`) stays lazy (`requirement-python-coding-style`). `main` **MUST** run that same FATAL gate immediately before a duration probe. The text menu is `VideoSpeed.menu` in this package (`requirement-python-tui`), not a pip import. `--help` and `--version` **MUST** still succeed when `cv2` is absent.  
M5. **Step 5 — argument parser.** **MUST** build the `ArgumentParser` and call `parse_args` only after steps 1–3, and after the ChronicleLogger gate. Flags stay the list in §2.4. `--version` **MUST** print the package string from step 1.

```python
from ChronicleLogger import ChronicleLogger
from VideoSpeed import MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION, __version__

def main(argv=None):
    # 1. main's own version (package SSOT)
    version = "{0}.{1}.{2}".format(MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION)

    # 2. logger
    appname = "VideoSpeed"
    logger = ChronicleLogger(logname=appname)
    appname = logger.logName()
    basedir = logger.baseDir()
    logdir = logger.logDir()

    # 3. debug
    if logger.isDebug():
        logger.log_message(
            "{0} v{1}.{2}.{3} ({4})".format(
                appname, MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION, __file__
            ),
            component="main",
        )
        logger.log_message(
            "Using {0}".format(ChronicleLogger.class_version()),
            component="main",
        )

    # 4. major import missing (ChronicleLogger already gated above)
    #    cv2: same FATAL shape, at first use, not before --version

    # 5. argument parser
    parser = argparse.ArgumentParser(prog="video-speed")
    parser.add_argument("--version", action="version", version=version)
    args = parser.parse_args(argv)
```

| Item | Value |
|------|--------|
| **Order today in `cli.py`** | The parser still runs first. Steps 2–4 are not in `main` yet. `TP-MAIN-01` is **todo** |
| **Version binding today** | `cli.py` imports the package triple and `__version__`. It does not declare its own triple |

### 2.2 Mode (owned elsewhere)

5. **MUST** treat bare invocation as **Type N**. The menu walk, the one job, and the fail-closed stop **MUST** follow `requirement-python-interactive-vs-noninteractive`. This file **MUST NOT** keep a second copy of that matrix.  
6. **MUST NOT** default empty argv to shell channel install or self-update.

### 2.3 Flags

7. **MUST** implement `--help` and `--version`.  
8. **MUST** implement `--file`, `--start`, `--end`, optional `--percent`, optional `--boomerang`, `--folder`, and `--json`. When each flag selects a path is the mode requirement. What `--json` prints is `requirement-python-json-output`.  
9. Each of `--file`, `--start`, `--end`, `--percent`, `--boomerang`, `--folder` **MUST** also be named on `requirement-domain-videospeed` and on `requirement-python-interactive-vs-noninteractive`. `--json` **MUST** also be named on `requirement-python-json-output` and on `requirement-python-interactive-vs-noninteractive`.

### 2.4 Output behavior

10. **MUST** print human-readable progress for each pipeline stage.  
11. **MUST** emit user-visible errors on the console. Durable system status **MUST** follow `requirement-python-cli-logging`.  
12. **MUST** implement `--json` as `requirement-python-json-output`. **MUST NOT** add `--quiet`.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Console script** | `video-speed = VideoSpeed.cli:main` |
| **Module entry** | `src/VideoSpeed/__main__.py` → `main()` |
| **CLI module** | `src/VideoSpeed/cli.py` |
| **Empty argv** | Mode matrix in `requirement-python-interactive-vs-noninteractive` |
| **Argparse** | `--help`, `--version`, `--file`, `--folder`, `--start`, `--end`, `--percent`, `--boomerang`, `--json` |
| **Empty argv, no TTY** | Fail closed; owned by the mode requirement |
| **JSON** | `--json` owned by `requirement-python-json-output`. No `--quiet` |
| **Privilege** | user-level only |
| **Root launcher** | `cli-new.py` thin re-export of package `main` (checkout convenience) |
| **Bootstrap archive** | `src/VideoSpeed/cli.bootstrap-old.py` (pre-specialize body) |
| **Ship CLI SSOT** | `src/VideoSpeed/cli.py` |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Entry and Type N empty-argv are explicit.  
- **Principle 16 – Interactive awareness**: The mode file owns the walk versus the job.  
- **Principle 5 – SSOT**: One CLI surface for entry. The mode matrix has one owner.

### 2.7 Maintainer verbs (not this entry)

`./build.sh` verbs are **not** `video-speed` flags. Behavior and samples stay on `requirement-python-build-script`. Named here so each token has a second home: `help`, `version`, `setup`, `clean`, `build`, `upload`, `git`, `tag`, `release`, `all`, `test-install`, `test`. `test` is the only test-purpose verb. `test-install` is operational: it replaces the pip install from this checkout. `all` is the same chain as `release`.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** A bad range or a missing flag stops before encode. Walk versus job exits stay on the mode requirement.  
- **Intentional:** Interactive default matches product design.  
- **Anti-fragile:** Module + console script dual entry.  
- **Over-protect:** No install-ensure on empty argv.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Change empty argv to Type O online install without explicit user order and new install requirements.  
2. Remove console script or module entry without packaging + docs update.  
3. Bypass domain/pipeline peers by reimplementing encode only in a second ad-hoc script as the “real” product.  
4. Require root to run normal editing.  
5. Leave `cli-new.py` as silent dual SSOT for entry behavior.  
6. Copy the mode matrix back into this file. Point at `requirement-python-interactive-vs-noninteractive`.  
7. Copy `./build.sh` verb procedures into this file. Point at `requirement-python-build-script`.

**Violating this rule is a critical CLI regression.**

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, **admin privilege** and **dedicated system user privilege** stay unused. **This requirement:** starting `video-speed` **MUST NOT** call `sudo`, wrap `apt` / `dnf`, create a dedicated account, or recommend `sudo pip` or `sudo curl \| sh`. Git Bash and Windows cmd **MUST NOT** invoke Termux `pkg`.

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | `video-speed` entry declared in packaging |
| AC-2 | `python -m VideoSpeed` works |
| AC-3 | Empty argv in a terminal starts the menu walk (mode requirement) |
| AC-4 | No MP4 on the job path → clear non-zero exit |
| AC-5 | Invalid cut range does not call encode |
| AC-6 | Success prints output path |
| AC-7 | `--file` + `--start` + `--end` runs one job without prompts |
| AC-8 | No TTY and no job flags → fail closed with next step |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-python-interactive-vs-noninteractive` | Menu walk versus one job versus fail closed |
| `requirement-python-build-script` | `./build.sh` verbs; not this entry |
| `requirement-python-json-output` | `--json` object; not a second mode matrix |
| `requirement-python-tui` | Menu look (default TUI style) |
| `requirement-domain-videospeed` | Domain steps |
| `requirement-video-ffmpeg-pipeline` | Encode |
| `requirement-python-packaging` | Entrypoint declaration |
| `requirement-python-error-handling` | Fail paths |
| `requirement-python-cli-logging` | System-status logger constructed from this entry |
| `requirement-python-version` | Triple that step 1 reads |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| TP-CLI-01 | `tests/test_cli.py` | have | `--version` |
| TP-CLI-02 | `tests/test_cli.py` | have | `--help` |
| TP-CLI-03 | — | todo | Interactive TTY walk |
| TP-CLI-04 | `tests/test_cli.py` | have | Empty folder |
| TP-CLI-05 | — | todo | Invalid index re-prompt |
| TP-CLI-06 | `tests/test_cli.py` | have | Batch flags |
| TP-MODE-01..03 | `tests/test_cli.py` | have | Mode matrix; see the mode requirement |
| TP-TUI-* | `tests/test_tui.py` | have | Menu look owned by `requirement-python-tui` |
| TP-MAIN-01 | — | todo | `main` order: version, logger, debug, missing lib, parser |
| TP-BUILD-01..04, TP-BUILD-06 | `tests/test_build.py` | have | `./build.sh` verbs, including `test-install`; owned by the build requirement |
| TP-JSON-01..05 | `tests/test_json.py` | have | `--json` object; owned by the JSON requirement |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial Python CLI interface law |
| 2026-08-19 | Active 1.1.0 | Batch flags; no-TTY fail-closed; §1.1 |
| 2026-09-30 | Active 1.2.0 | Menu look points at `requirement-python-tui` |
| 2026-10-01 | Active 1.3.0 | Durable status points at `requirement-python-cli-logging` |
| 2026-10-01 | Active 1.4.0 | `main` order: version, logger, debug, missing import, parser |
| 2026-10-01 | Active 1.4.1 | Text menu is `src/VideoSpeed/menu.py`; `cv2` stays the lazy major import |
| 2026-10-01 | Active 1.5.0 | Mode matrix moved to `requirement-python-interactive-vs-noninteractive` |
| 2026-10-01 | Active 1.5.1 | `./build.sh` verbs named; procedures stay on the build requirement |
| 2026-10-01 | Active 1.6.0 | `--json` named; the object stays on `requirement-python-json-output` |
| 2026-10-01 | Active 1.7.0 | `test-install` named; the procedure stays on `requirement-python-build-script` |

---

**Last Updated**: 2026-10-01  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
