**file**: docs/requirements/requirement-python-cli-logging.md
**Status**: Active (Version 1.0.7)
**Area**: python
**Key**: `requirement-python-cli-logging`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

# Requirement: python-cli-logging

## 1. Purpose

VideoSpeed records **system status** through one **ChronicleLogger** instance: process start, debug identity, menu and edit steps, duration probe, encode stages, major file operations, thread creation and thread operations, and failures. The pip name and version floor live in `requirement-python-dependency-management`. User-visible failure sentences stay owned by `requirement-python-error-handling`. Stopping on Control-C stays owned by `requirement-python-graceful-exit`. The text menu stays owned by `requirement-python-tui`. This file does not name a thread-wait timeout.

### 1.1 Human-facing

**In one sentence:** When VideoSpeed runs, it writes a dated status file with ChronicleLogger, and it does not paint those lines onto the text menu.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person running `video-speed` | A failed encode is still explained on the console, and the same fact is in the log file |
| The other role | The logger library | `ChronicleLogger(logname="VideoSpeed")` resolves the folder and the line shape |
| Not this file | How the menu is drawn, and how FFmpeg cuts the file | `requirement-python-tui`, `requirement-video-ffmpeg-pipeline` |

| Includes | Excludes |
|----------|----------|
| One logger, read-back of name and folders, debug gate, `log_message` level and component, thread create and thread operations | Rewriting ChronicleLogger; a second `logging` setup; painting the menu with log lines; a thread pool |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/VideoSpeed/cli.py` | `main` | Construct the logger and pass that one instance |
| `video-speed` | console script | Writes status while it runs |
| Resolved `logDir()` | daily `.log` file | History after the process exits |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Start the program | It builds one logger named VideoSpeed, reads the resolved name and base folder back, and logs status with a component tag. | `video-speed --version` |
| Ask for the debug lines | Set `DEBUG` before the process starts. On a non-TUI, non-JSON run, `main` displays the resolved name, the version triple, `ChronicleLogger.class_version()`, and a line that says `debug mode`, before the argument parser. `--json` and the text screen keep that mirror off the console. When debug mode is off, those lines stay off. | `DEBUG=1 video-speed --version` |

## 2. Core Rules (Mandatory)

### 2.0 When this law applies

1. **MUST** send system-status history through ChronicleLogger.  
2. **MUST NOT** add `logging.basicConfig`, a second file logger, or a hand-built `~/.app/...` path for those lines.  
3. **MUST NOT** use this file as the law for editing the ChronicleLogger library itself.

### 2.1 One logger

4. **MUST** import `ChronicleLogger` from `ChronicleLogger` at the use site. Tests that freeze the clock **MUST** import `TimeProvider` from the same package. **MUST NOT** import `_Suroot`. **MUST NOT** import `FakeTimeProvider` from the package (it is not exported).  
5. **MUST** construct **one** instance per process inside `main`, with `logname` set to the product name. Helpers receive that instance. **MUST NOT** construct a second logger “for convenience.”  
6. **MUST** read back `logName()`, `baseDir()`, and `logDir()` immediately after construct, and again after any path setter. The constructor string is not the resolved name: Python mode turns CamelCase into kebab-case (`VideoSpeed` becomes `video-speed`).  
7. **MUST NOT** re-export `ChronicleLogger` from the `VideoSpeed` package.  
8. If the import fails, **MUST** fail closed on the console with a next step to install the floor named by `requirement-python-dependency-management`, and **MUST** exit non-zero. That one line cannot go through `log_message`.

### 2.2 Debug

9. **MUST** ask `logger.isDebug()` for whether debug status is on. **MUST NOT** read `DEBUG` again in product code.  
10. `isDebug()` remembers the first answer. `DEBUG` or `debug` **MUST** already be `1`, `true`, or `show` (any letter case) **before** `ChronicleLogger(...)`.  
11. The startup identity lines **MUST** run only inside `if logger.isDebug():`, and `main` **MUST** run that block before the argument parser. The block is the resolved app name, the version triple, this file’s path, `ChronicleLogger.class_version()`, the resolved base folder, and one line whose message is `debug mode`. When `isDebug()` is false, those lines **MUST NOT** be displayed.  
11a. **Console mirror.** Before that block, `main` **MUST** call `quiet(True)` when `--json` is set or when this run will open the text screen. A non-TUI run that is not `--json` **MUST** leave quiet off, so the operator sees `debug mode` on the console. `--json` and the text screen **MUST** keep that mirror off the console. The same lines still go to the daily file.

### 2.3 `log_message` level and component

12. System-status lines **MUST** call `log_message`. The component **MUST** be the keyword `component`.  
13. Allowed `component` values for this product:

| Component | Status it marks |
|-----------|-----------------|
| `main` | Process start, version, missing library, top-level failure |
| `menu` | Text menu open, choice, leave |
| `edit` | Folder, video, cut, percent, boomerang, job start and finish |
| `probe` | Duration probe |
| `ffmpeg` | Cut, speed, and boomerang stages |
| Class name | That object was constructed, and later status recorded by that object |

The class-name components are `Cli`, `RunOutput`, `FileStage`, `MediaInfo`, `Encoder`, `CheckSystem`, `AboutPage`, `EditWalk`, `Tui`, `MenuPainter`, `MenuModel`, `MenuSession`, and `MenuScreenError`.

### 2.3a Pass the logger into every class

13a. `main` **MUST** decide quiet and run the debug block before it constructs class `Cli`.  
13b. Every product class **MUST** accept that same logger as an `__init__` parameter and store it on `self.logger`. The constructor home is `requirement-python-oop`.  
13c. When the logger is present, `__init__` **MUST** call `log_message("instantiated", component="<ClassName>")`. The level is INFO. The call **MUST NOT** sit inside `if logger.isDebug():`.  
13d. A class that constructs another product class **MUST** pass that same logger.  
13e. **MUST NOT** construct a ChronicleLogger inside a class.  
13f. A caller that has no logger may omit it. `main` has the logger and **MUST** pass it.  
13g. `--json` and the text screen **MUST** already be quiet, so these lines stay off that console. The daily file still receives them. A non-TUI, non-JSON run **MUST** leave quiet off, so the operator sees each `instantiated` line.

### 2.3b Major file operations

13h. A major file operation **MUST** call `log_message` with the operation and the paths. The operations are: write a temp, publish through `FileStage.promote_file`, and discard an unfinished temp.  
13i. The `component` **MUST** come from the table in rule 13. Encode temps and publish use `ffmpeg`. The level is `INFO`. The call **MUST NOT** sit inside `if logger.isDebug():`. **MUST NOT** use `print`. **MUST NOT** construct a second logger.  
13j. Control-C stop, the exit code, and the decision not to publish are owned by `requirement-python-graceful-exit`. This file owns the logger and the `component` for those lines.  
13k. Quiet from rule 11a still applies. The daily file still receives the line.

### 2.3c Thread creation and thread operations

13l. Any thread creation and any thread operation **MUST** call `log_message` on the one ChronicleLogger. The operations are: create, start, join or other wait, lock acquire, lock release, and handing work to a pool. The line **MUST** be written **before** the call that can block or race. It names the action, the thread name, and the object it waits on when there is one.  
13m. The `component` **MUST** come from the table in rule 13: the class that performs the operation, or `main` when `main` does. Create, start, joined, acquired, and released are `INFO`. A bound that expires is `WARNING`. The call **MUST NOT** sit inside `if logger.isDebug():`. **MUST NOT** use `print`. **MUST NOT** construct a second logger, including one logger per thread.  
13n. The before-line is what keeps an endless wait visible. A join, wait, or acquire that never returns still has that line already in the daily file, with the thread name and the object it is waiting on.  
13o. `log_message` **MUST NOT** run while a work lock is held. When more than one thread can call `log_message`, one dedicated lock **MUST** wrap only that call, and that lock **MUST** be released before start, join, wait, acquire of any other lock, or any other blocking call. **MUST NOT** join a thread while holding a lock that thread must take. ChronicleLogger's file append is not a lock. A second logger is not the fix for a torn line.  
13p. This file does not name a wait timeout. When another requirement names a bound, the before-line includes it and the outcome line says `timeout` when that bound fires. An unbounded wait is still logged before it starts.  
13q. Quiet from rule 11a still applies. The daily file still receives the line. Control-C of an FFmpeg child stays `requirement-python-graceful-exit`. A thread join is not that stop.

14. Allowed `level` values: `INFO`, `DEBUG`, `WARNING`, `ERROR`, `FATAL`. The library uppercases the string. `ERROR` and `FATAL` mirror to stderr. The others mirror to stdout. Omitted `level` means `INFO`.  
15. A line with `level="DEBUG"` **MUST** sit inside `if logger.isDebug():`.  
16. **MUST NOT** put secrets into a message. This product has none. A video path is allowed.

### 2.4 Console, menu, and the file

17. `log_message` still tries to append the daily file when the folder is writable. An unwritable folder **MUST NOT** crash the process.  
18. While the text menu is on screen, **MUST** call `logger.quiet(True)` first so the console mirror does not write over the frame. The file write still happens. `requirement-python-tui` still draws the screen.  
19. A batch job that never opens the menu **MUST** leave quiet off so the operator sees the mirrored status line.  
20. A user-visible failure sentence remains owned by `requirement-python-error-handling`. The same fact **MUST** also be `log_message` at `ERROR` or `FATAL`. While quiet is on, the logger mirror is not a substitute for that console sentence.

### 2.5 Folder and line

21. **MUST** use the folders from `baseDir()` and `logDir()`. **MUST NOT** copy the library’s environment ladder into this program.  
22. The daily file basename **MUST** stay the library’s `{kebab-app}-{YYYYMMDD}.log` under `logDir()`.  
23. A file line has this shape (the library writes it; this product does not format it by hand):

```text
[{YYYY-MM-DD HH:MM:SS}] pid:{PID} [{LEVEL}] @{COMPONENT} :] {MESSAGE}
```

### 2.6 Tests

24. A test that needs a fixed day **MUST** pass `time_provider=` a subclass of `TimeProvider` defined in the test module. **MUST NOT** `from ChronicleLogger import FakeTimeProvider`.  
25. Tests **MUST** pass explicit `logdir` and `basedir` so they do not write the developer’s real app folder.

### 2.7 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| **Library** | ChronicleLogger |
| **Floor** | `ChronicleLogger>=1.3.1`, owned by `requirement-python-dependency-management` |
| **Construct site** | `main` in `src/VideoSpeed/cli.py` |
| **logname** | `VideoSpeed` |
| **Resolved name** | `video-speed` from `logName()` |
| **Call order** | Same order as the sibling product AnimeDlp: construct with `logname`, then `logName()`, then `baseDir()`, then `logDir()`, then quiet for `--json` or the text screen, then `isDebug()`, then `log_message`, including `debug mode` |
| **Quiet** | `quiet(True)` before the debug mirror when `--json` is set or the text screen will open; also before the frame. A non-TUI, non-JSON run stays audible |
| **Ship unit** | `main` constructs one ChronicleLogger, decides quiet, then builds `Cli` with that logger. Each class stores it and logs `instantiated` with `component` set to the class name. A non-TUI, non-JSON run shows those lines. Edit, probe, and ffmpeg stage lines remain `TP-LOG-03`. A temp write, a publish, and a discard of an unfinished temp are not logged yet (`TP-LOG-06`). The ship unit creates no threads and takes no log lock (`TP-LOG-07`) |
| **Debug switch** | Environment `DEBUG` only. There is no `--debug` flag |

Construct, read-back, and the debug gate:

```python
from ChronicleLogger import ChronicleLogger
from VideoSpeed import MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION

appname = "VideoSpeed"
logger = ChronicleLogger(logname=appname)
appname = logger.logName()
basedir = logger.baseDir()
logdir = logger.logDir()

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
    logger.log_message(
        "Base {0}".format(basedir),
        level="DEBUG",
        component="main",
    )
    logger.log_message(
        "debug mode",
        component="main",
    )
```

Quiet the mirror before that block when `--json` is set or the text screen will open. A non-TUI, non-JSON run does not.

`log_message` levels. `component` is always a keyword:

```python
logger.log_message(
    "menu open",
    level="INFO",
    component="menu",
)
logger.log_message(
    "percent out of range",
    level="WARNING",
    component="edit",
)
logger.log_message(
    "duration probe failed",
    level="ERROR",
    component="probe",
)
logger.log_message(
    "ffmpeg is not installed",
    level="FATAL",
    component="ffmpeg",
)
```

Before the text menu:

```python
logger.quiet(True)
```

| Sample | Value |
|--------|--------|
| **Resolved base (non-root, no conda / pyenv-virtualenv / venv)** | `~/.app/video-speed` via `baseDir()`, not a path typed in this program |
| **Log folder** | `baseDir()` + `/log` via `logDir()` |
| **Daily file** | `video-speed-20261001.log` |
| **Line** | `[2026-10-01 12:00:00] pid:12345 [INFO] @menu :] menu open` |

### 2.8 Why This Requirement Exists (CIAO)

- **Principle 5 – SSOT of output** (https://github.com/cloudgen/ciao): status history has one writer.  
- **Principle 1 – Caution** (https://github.com/cloudgen/ciao): a missing library or an unwritable log folder does not wipe the source video or smash the menu. A thread wait is logged before it blocks, and the logger is not called while a work lock is held, so the log is not the hang.  
- **Principle 2 – Intentional** (https://github.com/cloudgen/ciao): level and component are named on every status line.  
- **Principle 21 – dual policies** (https://github.com/cloudgen/ciao): the samples above are this product’s filled values.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, status files stay in the folder ChronicleLogger resolves for this login. **This requirement:** do not use admin privilege, `sudo`, or a system package manager to create the log folder or to install ChronicleLogger.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Quiet the console mirror before the text menu. Do not crash when the log folder is unwritable.  
- **Intentional:** One instance. Workflow components stay `main`, `menu`, `edit`, `probe`, and `ffmpeg`. Each class also logs under its own name. A thread line names the action, the thread name, and the wait target.  
- **Anti-fragile:** Folder choice stays inside ChronicleLogger.  
- **Over-protect:** No second logger and no package re-export of ChronicleLogger.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

1. Replace these status lines with `print` or `logging.basicConfig`.  
2. Construct more than one ChronicleLogger in a process.  
3. Skip the read-back of `logName()`, `baseDir()`, and `logDir()`.  
4. Call `isDebug()` and then expect a later `DEBUG=` change to count.  
5. Write log lines onto the text menu.  
6. Import `FakeTimeProvider` or `_Suroot`.  
7. Re-export `ChronicleLogger` from `VideoSpeed`.  
8. Hard-code `~/.app/video-speed` in product code.  
9. Treat `quiet(True)` as a JSON encoder. `--json` is `requirement-python-json-output`. While that switch is set, the console mirror **MUST** stay quiet so status lines do not join the one JSON object.  
10. Build the product objects before the logger exists, or drop the `instantiated` line, or keep a class from storing and passing that logger.  
11. Write a temp, publish, or discard an unfinished temp without a `log_message` that names the operation and the paths.  
12. Put the Control-C stop procedure in this file. That outcome is `requirement-python-graceful-exit`.  
13. Create or operate a thread (start, join, wait, lock acquire, lock release, or a pool hand-off) without a before-line on the one logger that names the action, the thread name, and the wait target.  
14. Call `log_message` while a work lock is held, hold the log lock across a join or another lock, or join a thread while holding a lock that thread must take.

**Violating this rule is a status-log and menu-integrity regression.**

## 5. Design-time verification

| TP-ID | Case | Status | Map |
|-------|------|--------|-----|
| `TP-LOG-01` | One construct; read-back `logName` / `baseDir` / `logDir` under a temp base | have | `tests/test_logging.py` |
| `TP-LOG-02` | `DEBUG=1` on a non-TUI, non-JSON run shows the identity lines and `debug mode`; unset `DEBUG` does not. `--json` and the text screen keep that mirror off stdout and still write the file | have | `tests/test_logging.py` |
| `TP-LOG-03` | `INFO`, `WARNING`, `ERROR`, `FATAL` and keyword `component` | todo | `reviews/test-plan.md` |
| `TP-LOG-04` | Text menu path calls `quiet(True)` before the frame is drawn | have | `tests/test_logging.py` |
| `TP-LOG-05` | Each constructed class stores the one logger and logs `instantiated` under its class name. `--json` keeps that mirror off stdout | have | `tests/test_logging.py` |
| `TP-LOG-06` | A publish or a temp write logs the operation and the paths on the one logger | todo | `reviews/test-plan.md` |
| `TP-LOG-07` | A thread create, start, or wait writes the action, the thread name, and the wait target on the one logger before the call that can block. The log call is not made while a work lock is held | todo | `reviews/test-plan.md` |

## 6. Related artifacts (versioned surface only)

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-python-dependency-management.md` | Pip floor `ChronicleLogger>=1.3.1` |
| `docs/requirements/requirement-python-error-handling.md` | Console failure sentence |
| `docs/requirements/requirement-python-graceful-exit.md` | Control-C stop and exit 130. This file owns the logger line only |
| `docs/requirements/requirement-python-tui.md` | Text menu; not a second logger |
| `docs/requirements/requirement-python-cli-interface.md` | Entry that must construct this logger |
| `docs/requirements/requirement-python-coding-style.md` | Points here for status lines |
| `docs/requirements/requirement-python-oop.md` | The logger is an `__init__` parameter. This file owns the instantiation line |
| `docs/requirements/requirement-class-software-dev.md` | Class residual pointer |
| `src/VideoSpeed/cli.py` | Construct site |
| `reviews/test-plan.md` | TP map |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-01 | Active 1.0.0 | System status via ChronicleLogger; AnimeDlp call order |
| 2026-10-01 | Active 1.0.1 | `--json` is not this logger; the console mirror stays quiet under that switch |
| 2026-10-01 | Active 1.0.2 | `main` displays the debug identity when debug mode is already on, and stays silent when it is off |
| 2026-10-01 | Active 1.0.3 | A non-TUI, non-JSON run shows `debug mode`. `--json` and the text screen quiet that mirror. The file still records it |
| 2026-10-01 | Active 1.0.4 | Every class receives the one logger, stores it, and logs `instantiated` |
| 2026-10-01 | Active 1.0.5 | A major file operation logs the operation and the paths. Control-C stop and exit 130 stay on `requirement-python-graceful-exit`. `TP-LOG-06` is todo |
| 2026-10-01 | Active 1.0.6 | Thread creation and thread operations log on the one ChronicleLogger before the call that can block. The log call is not made while a work lock is held. No wait timeout is named here. `TP-LOG-07` is todo. The ship unit creates no threads |
| 2026-10-01 | Active 1.0.7 | The logger arrives through `__init__`. That constructor rule's home is `requirement-python-oop`. The instantiation line stays here |

---

**Last Updated**: 2026-10-01  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
