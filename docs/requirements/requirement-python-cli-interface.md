**file**: docs/requirements/requirement-python-cli-interface.md  
**Status**: Active (Version 1.9.8)  
**Area**: python  
**Key**: `requirement-python-cli-interface`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define the official **command-line entry points**, the **product verbs**, and the order of `main` for the VideoSpeed Python package. The verbs are `help`, `version`, `about`, `edit`, `list-mp4`, `self-install`, `version-check`, `self-update`, and `self-uninstall`. `hello` is not a product verb. `help` stays off the numbered menu. Each verb's default route is the terminal. The mode file names the screen verbs: `edit` when a target is still missing, and `list-mp4` on a terminal. `help` and `version` are self-management verbs. Which path runs after the parser — the menu walk, one verb, one job, or a fail-closed stop — is **`requirement-python-interactive-vs-noninteractive`**.

Domain step catalog is owned by **`requirement-domain-videospeed`**. Encode ops are owned by **`requirement-video-ffmpeg-pipeline`**.

### 1.1 Human-facing

**In one sentence:** This file says how you start VideoSpeed (`video-speed` or `python -m VideoSpeed`), the order inside `main`, and the product verbs. A verb stays on the terminal unless the mode file names it for the text menu.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person at a terminal or a script | `video-speed` or `video-speed --file clip.mp4 --start 0 --end 5` |
| The other role | Domain + pipeline peers | What to cut and how FFmpeg runs |
| Not this file | Filter graphs; the three version integers | Pipeline file and `requirement-python-version` |

| Includes | Excludes |
|----------|----------|
| Console script, module entry, `main` order, the flag names, the product verbs | The mode matrix (when a verb prompts); root/sudo; online install; `./build.sh` verbs |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/VideoSpeed/cli.py` | ship unit | live behavior |
| `video-speed help` | command | the same usage as `--help`, including the verb list |
| `video-speed edit` | command | the edit action, without picking it from the front board first |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Edit one clip without prompts | The program must not wait on stdin. It needs a file and a time range. The verb `edit` is optional when those flags are present. | `video-speed edit --file clip.mp4 --start 1 --end 5` |
| Run a menu action by name | The verb is the menu token. On a terminal, a verb that still needs a folder asks for the folder, then for the specific file when that verb needs one. | `video-speed edit` |
| List MP4 files | `list-mp4` lists and does not encode. | `video-speed list-mp4` |
| Walk the front board | Run with no arguments **in a terminal**. Without a terminal, and with no verb, it exits and tells you to pass flags. | `video-speed` |

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
M2. **Step 2 — logger.** **MUST** write `logger = ChronicleLogger(...)` inside `def main`, as `requirement-python-cli-logging` requires (`logname="VideoSpeed"`, then `logName()`, `baseDir()`, `logDir()`). That statement is the construct. A method is not the construct. `Cli.__new__` is not the construct. If that import fails, **MUST** print the install next step and return `1` before the parser runs.  
M3. **Step 3 — debug.** If `logger.isDebug()` is true, **MUST** log the identity line with the three integers, `ChronicleLogger.class_version()`, and a line whose message is `debug mode`, `component="main"`. Step 2 **MUST** pass `is_quiet=True` into `ChronicleLogger(...)` unless `--verbose` is set on a run that is not `--json` and will not open the text screen (`requirement-python-cli-logging`). `--json` and a text screen **MUST** stay quiet even when `--verbose` is also set. Calling `quiet(True)` only after that constructor returns does not hide a line the constructor already printed. `DEBUG` must already be set before step 2. `DEBUG` without `--verbose` writes those lines to the daily file and does not show them on the terminal. After this step, `main` **MUST** construct `Cli` with that logger. Each class stores it and logs `instantiated` (`requirement-python-cli-logging`).  
M4. **Step 4 — major import missing.** **MUST** use the AnimeDlp gate: `log_message` at `FATAL`, `component="main"`, then `return 1`. ChronicleLogger is that gate at step 2. OpenCV (`cv2`) stays lazy (`requirement-python-coding-style`). `main` **MUST** run that same FATAL gate immediately before a duration probe. The text menu stays in this package (`requirement-python-tui`). Its class home is `requirement-python-oop`. `def main` stays in `src/VideoSpeed/cli.py`. Class `Cli` in that file constructs the objects that requirement names, including class `Tui`. It is not a pip import. `--help` and `--version` **MUST** still succeed when `cv2` is absent.  
M5. **Step 5 — argument parser.** **MUST** build the `ArgumentParser` and call `parse_args` only after steps 1–3, and after the ChronicleLogger gate. Flags stay the list in §2.4. `--version` **MUST** print the package string from step 1.

### Sample code

`def main` in `src/VideoSpeed/cli.py` writes `ChronicleLogger(...)` and then `Cli(logger)`. `Cli.run` builds the parser. This sample is that function. The program was not changed.

```python
def main(argv=None, log_basedir="", log_logdir=""):
    if argv is None:
        argv = sys.argv[1:]
    argv = list(argv)
    try:
        from ChronicleLogger import ChronicleLogger
    except ImportError:
        print("ERROR: ChronicleLogger is not installed.", file=sys.stderr)
        print("   Next: pip install 'ChronicleLogger>=1.3.1'", file=sys.stderr)
        return 1

    show_mirror = Cli._show_log_mirror(argv)
    logger = ChronicleLogger(
        logname="VideoSpeed",
        basedir=log_basedir or "",
        logdir=log_logdir or "",
        is_quiet=not show_mirror,
    )
    appname = logger.logName()
    basedir = logger.baseDir()
    logger.logDir()
    if logger.isDebug():
        logger.log_message(
            "{0} v{1}.{2}.{3} ({4})".format(
                appname,
                MAJOR_VERSION,
                MINOR_VERSION,
                PATCH_VERSION,
                __file__,
            ),
            component="main",
        )
        logger.log_message(
            "Using {0}".format(ChronicleLogger.class_version()),
            component="main",
        )
        logger.log_message(
            "Base {0}".format(basedir),
            level="DEBUG",
            component="main",
        )
        logger.log_message(
            "debug mode",
            component="main",
        )
    app = Cli(logger)
    return app.run(argv, logger=logger)
```

| Item | Value |
|------|--------|
| **Order today in `cli.py`** | `def main` writes `ChronicleLogger(...)` with `logname="VideoSpeed"`, `basedir`, `logdir`, and `is_quiet=not Cli._show_log_mirror(argv)`. It reads `logName()`, `baseDir()`, and `logDir()`. When `isDebug()` is true it logs the identity, `ChronicleLogger.class_version()`, the base line, and `debug mode`, `component="main"`. Then `Cli(logger)` and `return app.run(argv, logger=logger)`. `Cli.run` builds the parser. Each `__init__` writes `instantiated`. A missing ChronicleLogger returns 1 before that call. `cv2` stays a lazy FATAL at the duration probe. `TP-MAIN-01` stays **todo** for that probe gate |
| **Version binding today** | `cli.py` imports the package triple and `__version__`. It does not declare its own triple |

### 2.2 Mode (owned elsewhere)

5. **MUST** treat bare invocation as **Type N**. The menu walk, a product verb, the one job, and the fail-closed stop **MUST** follow `requirement-python-interactive-vs-noninteractive`. This file **MUST NOT** keep a second copy of that matrix.  
6. **MUST NOT** default empty argv to shell channel install, `self-install`, or `self-update`.

### 2.3 Flags

7. **MUST** implement `--help` and `--version`.  
8. **MUST** implement `--file`, `--start`, `--end`, optional `--percent`, optional `--boomerang`, `--folder`, and `--json`. When each flag selects a path is the mode requirement. What `--json` prints is `requirement-python-json-output`.  
9. Each of `--file`, `--start`, `--end`, `--percent`, `--boomerang`, `--folder` **MUST** also be named on `requirement-domain-videospeed` and on `requirement-python-interactive-vs-noninteractive`. `--json` **MUST** also be named on `requirement-python-json-output` and on `requirement-python-interactive-vs-noninteractive`.

### 2.3a Product verbs (the command line beside the menu)

The text menu is one way to start an action. The command line is the other. A **product verb** is the first positional argument. The verbs name an action a person can pick on the menu, except `help`, which stays off the numbered list. `hello` is not a product verb. Flags stay. A verb does not remove `--file`, `--start`, or `--end`.

These tokens are **not** `./build.sh` verbs. Maintainer verbs stay in §2.7.

| Verb | Same action as | Folder | Specific file |
|------|----------------|--------|---------------|
| `help` | `--help`. Usage text. The menu does not number this row. It is a self-management verb. | no | no |
| `version` | Self-management **82**. Installed version. No pip and no network. | no | no |
| `about` | Self-management **83 about**. Page body is `requirement-python-about` | no | no |
| `edit` | Menu **1 edit**. Domain steps D-01..D-08 | yes, unless `--folder` or `--file` already names the directory | yes, unless `--file` names the MP4 |
| `list-mp4` | The MP4 list edit shows after the folder question. The verb lists and stops. It does not encode | yes, unless `--folder` names the directory, or `--file` names a file whose parent is that directory | no |
| `self-install` | Self-management **87**. `python -m pip install VideoSpeed` | no | no |
| `version-check` | Self-management **84**. `python -m pip index versions VideoSpeed` | no | no |
| `self-update` | Self-management **85**. `python -m pip install --upgrade VideoSpeed` | no | no |
| `self-uninstall` | Self-management **86**. `python -m pip uninstall -y VideoSpeed`. The command line also requires `--force` | no | no |

10. **MUST** accept the positional verbs `help`, `version`, `about`, `edit`, `list-mp4`, `self-install`, `version-check`, `self-update`, and `self-uninstall` on `video-speed` and on `python -m VideoSpeed`.  
11. **MUST** make `help` and `--help` print the same usage. That usage **MUST** name each of those verbs and the job flags, and **MUST** name the pip commands for `version-check` and `self-update`.  
12. An unknown positional token **MUST** exit non-zero, **MUST** name those verbs, and **MUST NOT** open the menu and **MUST NOT** encode. `hello` is an unknown token. It **MUST NOT** print `Hello.`.  
13. **MUST NOT** delete this verb list and leave flags as the only command line. **MUST NOT** make the front board the only way to run `about`, `edit`, or `list-mp4`. **MUST NOT** add `hello` as a product verb.  
14. When a verb still needs a folder or a specific file, the order **MUST** be the folder first and the specific file second, as `requirement-python-interactive-vs-noninteractive` §2.1b. This file **MUST NOT** keep a second prompt matrix.  
15. `help`, `version`, `about`, `self-install`, `version-check`, `self-update`, and `self-uninstall` **MUST NOT** ask for a folder or a file. `version` **MUST NOT** call pip. `version-check` and `self-update` **MUST** call pip as the table says. `self-install` and `self-uninstall` **MUST** call pip as the table says. Those commands **MUST NOT** use `sudo` and **MUST NOT** use `curl`. `self-uninstall` without `--force` **MUST** exit non-zero and name `--force`. `list-mp4` **MUST NOT** ask for a specific file and **MUST NOT** encode. `Exit` stays a menu control. It is not a positional verb.  
16. Without a terminal, `help`, `version`, `about`, `list-mp4`, `self-install`, `version-check`, `self-update`, and `self-uninstall --force` **MUST** still run and **MUST NOT** wait. `edit` without a terminal **MUST** follow the one-job rule when `--file`, `--start`, and `--end` are present, and the fail-closed stop when they are not.
16a. Each product verb's default route is the terminal. This file does not put a verb on the text screen. The mode file names the exceptions: `edit` when a target is still missing, and `list-mp4` on a terminal. No product verb is the menu. `--json` with no product verb is not the menu. `--verbose` with no product verb stays on that menu when both streams are terminals.

```text
video-speed help
video-speed version
video-speed about
video-speed version-check
video-speed self-update
video-speed self-install
video-speed self-uninstall --force
video-speed edit
video-speed edit --folder ./clips
video-speed edit --file clip.mp4 --start 1 --end 5 --percent 100
video-speed list-mp4
video-speed list-mp4 --folder ./clips
```

### 2.4 Output behavior

17. **MUST** print human-readable progress for each pipeline stage.  
18. **MUST** emit user-visible errors on the console. Durable system status **MUST** follow `requirement-python-cli-logging`.  
19. **MUST** implement `--json` as `requirement-python-json-output` on every product verb, including `help`. The flags `--help` and `--version` stay human text. **MUST** implement `--verbose`. That flag shows the console mirror on a run that is not `--json` and will not open the text screen. **MUST NOT** add `--quiet`.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Console script** | `video-speed = VideoSpeed.cli:main` |
| **Module entry** | `src/VideoSpeed/__main__.py` → `main()` |
| **CLI module** | `src/VideoSpeed/cli.py` |
| **Empty argv** | Mode matrix in `requirement-python-interactive-vs-noninteractive` |
| **Argparse** | positional verb `help` \| `version` \| `about` \| `edit` \| `list-mp4` \| `self-install` \| `version-check` \| `self-update` \| `self-uninstall`; flags `--help`, `--version`, `--file`, `--folder`, `--start`, `--end`, `--percent`, `--boomerang`, `--json`, `--verbose`, `--force` |
| **Product verbs** | §2.3a. Prompt order is the mode requirement |
| **Empty argv, no TTY** | Fail closed; owned by the mode requirement |
| **JSON** | `--json` on every product verb, owned by `requirement-python-json-output`. The flags `--help` and `--version` stay human. `--verbose` shows the console mirror except on `--json` and a text screen. No `--quiet` |
| **Privilege** | user-level only |
| **Root launcher** | `cli-new.py` thin re-export of package `main` (checkout convenience) |
| **Bootstrap archive** | `src/VideoSpeed/cli.bootstrap-old.py` (pre-specialize body) |
| **Ship CLI SSOT** | `src/VideoSpeed/cli.py` |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Entry and Type N empty-argv are explicit.  
- **Principle 16 – Interactive awareness**: The mode file owns the walk, the verb, and the job.  
- **Principle 5 – SSOT**: One CLI surface for entry and for the verb names. The mode matrix has one owner.

### 2.7 Maintainer verbs (not this entry)

`./build.sh` verbs are **not** `video-speed` verbs and **not** `video-speed` flags. Behavior and samples stay on `requirement-python-build-script`. Named here so each token has a second home: `help`, `version`, `setup`, `clean`, `build`, `upload`, `git`, `tag`, `release`, `all`, `test-install`, `test`. `test` is the only test-purpose verb. `test-install` is operational: it replaces the pip install from this checkout. `all` is the same chain as `release`. The maintainer token `help` prints `./build.sh` usage. The product verb `help` prints `video-speed` usage (§2.3a).

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
8. Remove `help`, `version`, `about`, `edit`, `list-mp4`, `self-install`, `version-check`, `self-update`, or `self-uninstall`, or leave the command line as flags only. Do not add `hello` as a product verb. Do not replace the pip commands with `curl` or `sudo pip`.  
9. Treat `./build.sh` verbs as `video-speed` verbs, or treat these product verbs as maintainer verbs.

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
| AC-8 | No TTY, no verb, and no job flags → fail closed with next step |
| AC-9 | `help` and `--help` both list `help`, `version`, `about`, `edit`, `list-mp4`, `self-install`, `version-check`, `self-update`, and `self-uninstall`, and neither lists `hello` |
| AC-10 | An unknown positional verb exits non-zero, names those verbs, and does not open the menu |
| AC-11 | `about`, `version`, and `list-mp4` run without a terminal and do not wait. `hello` exits non-zero and does not wait |
| AC-12 | `version-check` and `self-update` call pip. `version` does not. `self-uninstall` without `--force` exits non-zero |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-python-interactive-vs-noninteractive` | Menu walk versus one verb versus one job versus fail closed. Folder, then file |
| `requirement-python-build-script` | `./build.sh` verbs; not this entry |
| `requirement-python-json-output` | `--json` object; not a second mode matrix |
| `requirement-python-tui` | Menu look (default TUI style) |
| `requirement-python-oop` | `def main` stays in `cli.py`. Class `Cli` builds the objects |
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
| TP-CLI-07 | `tests/test_cli.py` | have | `help` lists the product verbs; an unknown verb exits 1 and does not open the menu |
| TP-SELF-01 | `tests/test_cli.py` | have | `version` is local. `version-check` and `self-update` call pip. `self-uninstall` needs `--force` |
| TP-MODE-01..03, TP-MODE-09 | `tests/test_cli.py` | have | Mode matrix; see the mode requirement. `TP-MODE-09` is the no-verb menu and the terminal route for `version`, `about`, and `help` |
| TP-TUI-* | `tests/test_tui.py` | have | Menu look owned by `requirement-python-tui` |
| TP-MAIN-01 | — | todo | `main` order: version, logger, debug, missing lib, parser |
| TP-BUILD-01..04, TP-BUILD-06 | `tests/test_build.py` | have | `./build.sh` verbs, including `test-install`; owned by the build requirement |
| TP-JSON-01..06 | `tests/test_json.py` | have | `--json` object on every product verb; owned by the JSON requirement |

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
| 2026-10-01 | Active 1.7.1 | Text-menu class home is `requirement-python-oop`. Until `tui.py` exists, the module is `VideoSpeed.menu` |
| 2026-10-01 | Active 1.7.2 | `main` constructs ChronicleLogger and displays the debug identity before the parser |
| 2026-10-01 | Active 1.8.0 | Product verbs `help`, `about`, `hello`, `edit`, `list-mp4` returned. Prompt order stays on the mode requirement |
| 2026-10-01 | Active 1.8.1 | `main` constructs class `Tui` in `VideoSpeed.tui`. `TP-OOP-01` has landed |
| 2026-10-01 | Active 1.8.2 | `def main` stays in `cli.py`. Class `Cli` builds the objects named by `requirement-python-oop` |
| 2026-10-01 | Active 1.8.3 | Step 3 logs `debug mode`. A non-TUI, non-JSON run shows it. `--json` and the text screen quiet that mirror |
| 2026-10-01 | Active 1.8.4 | After the debug step, `Cli` is built with that logger. Each class logs `instantiated` |
| 2026-10-02 | Active 1.9.0 | Self-management verbs. `version-check` and `self-update` call pip. `help` stays unnumbered |
| 2026-10-02 | Active 1.9.1 | `hello` stays a command and is not a text-menu row |
| 2026-10-02 | Active 1.9.2 | Step 2 passes `is_quiet=True` when `--json` or the text screen is already known. `quiet(True)` after the constructor returns is not that quiet |
| 2026-10-02 | Active 1.9.3 | Step 2 is the statement `ChronicleLogger(...)` inside `def main`. A method does not instantiate the logger. `Cli.__new__` is not that step |
| 2026-10-02 | Active 1.9.4 | Sample code shows `ChronicleLogger(...)` and then `Cli(logger)` before the parser |
| 2026-10-04 | Active 1.9.5 | `hello` is not a product verb. `video-speed hello` exits non-zero and does not print `Hello.` |
| 2026-10-05 | Active 1.9.6 | `--verbose` shows the console mirror unless the run is `--json` or a text screen. There is still no `--quiet`. Every product verb, including `help`, accepts `--json`. The flags `--help` and `--version` stay human |
| 2026-10-05 | Active 1.9.7 | Each product verb's default route is the terminal. The mode file names the screen exceptions. No product verb is the menu |
| 2026-10-05 | Active 1.9.8 | Sample code is the live `def main`: `_show_log_mirror`, `ChronicleLogger(...)` with `basedir` and `logdir`, then `Cli(logger)`, then `app.run`. The parser stays in `Cli.run`. The program was not changed |

---

**Last Updated**: 2026-10-05  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
