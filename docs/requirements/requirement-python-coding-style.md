**file**: docs/requirements/requirement-python-coding-style.md  
**Status**: Active (Version 1.4.14)  
**Area**: python  
**Key**: `requirement-python-coding-style`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define **Python coding style and defensive file I/O conventions** for VideoSpeed: how agents and maintainers write Python so path/temp/publish behavior stays multi-mount safe (including USB), without duplicating domain or FFmpeg pipeline tables.

Pipeline-specific apply of these rules is owned by **`requirement-video-ffmpeg-pipeline`**.

### 1.1 Human-facing

**In one sentence:** When VideoSpeed moves or publishes a file, including onto a USB stick or other removable disk, it uses `shutil.move` and does not call `os.rename` or `os.replace`.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Maintainer publishing a file | `FileStage.promote_file` uses `shutil.move` |
| The other role | Pipeline peer | When temps are created during encode |
| Not this file | Prompt text | CLI interface |

| Includes | Excludes |
|----------|----------|
| Same-directory staging; `shutil.move` for every move and publish; lazy OpenCV import; identity, verb lists, and bounds on class `Cli`; version equality in the suite; one class per file; `ClassName(...)` at the site that needs the object; attribute access by name | Filter graphs; argparse flags; `os.rename` / `os.replace`; import-time version `raise`; module-level assignments for identity, verb lists, and bounds; a second class in a class file; a factory (a function or a method whose job is to instantiate a class); `__dict__` unless the user orders that access for that edit |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/VideoSpeed/file_stage.py` | class `FileStage` | `promote_file` / `staging_dir_for` (`requirement-python-oop`) |
| `./tests/run.sh` | suite | TP-FS-01 / TP-FS-02 |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Save onto a USB stick | Temps sit next to the output when that folder is writable. `shutil.move` renames on the stick and copies when the stick is a different device. | Keep `FileStage.promote_file` → `shutil.move` |
| Check that the version string matches the three integers | The suite compares them. Starting the program does not raise if a maintainer left them mismatched. | `tests/test_docs.py` |
| Name the program | `APP_NAME`, the verb lists, the formatted version, and the length bounds are attributes of class `Cli`. | Read `Cli.APP_NAME` |

---

## 2. Core Rules (Mandatory)

### 2.1 General style (this product)

1. **MUST** keep the installable package under `src/VideoSpeed/` with thin module entry (`__main__` / console script → `cli.main`).  
2. **MUST** cite only live `docs/requirements/requirement-*.md` keys in product-source law comments — never templates or skills as behavioral authority.  
3. **SHOULD** use clear function **General Purpose** docstrings on public helpers.  
4. **MUST** fail closed with user-visible messages on expected errors (missing FFmpeg, invalid range, missing OpenCV).  
5. Heavy optional deps (e.g. OpenCV) **SHOULD** be imported lazily at use site when package import must succeed without them (version/help).  
6. A full StateLogic+Attr rewrite of the encoder and of `main` is **aspirational**. **MUST NOT** force that rewrite solely for style. Ordinary classes, one class per file, are ordered by `requirement-python-oop`. `def main` stays in `src/VideoSpeed/cli.py`. A procedural pile of another class's methods in `cli.py` is not an allowed end state.

### 2.2 Temporary files

7. When the final destination path is known, **MUST** prefer creating intermediate files on the **same filesystem/mount as that destination** (writable parent of the final path).  
8. **MUST NOT** assume system `TMPDIR` / `/tmp` is the same mount as user media (USB, network, secondary disks).  
9. **MUST** clean intermediate temps on success and failure paths (best-effort).

### 2.3 Moving and publishing files (sacred — removable media)

10. To **move, rename, replace, or publish** a file or a directory, product Python **MUST** use **`shutil.move`** (or a thin wrapper whose only move implementation is `shutil.move`).  
    - Same device: `shutil.move` renames.  
    - Another device, including removable media: `shutil.move` copies (default `shutil.copy2`) and then removes the source. That path is safe for `EXDEV` ("Invalid cross-device link").  
11. Product Python **MUST NOT** call **`os.rename`**, **`os.replace`**, **`pathlib.Path.rename`**, or **`pathlib.Path.replace`**. The ban covers every move and publish, including a path that looks like the same mount. Removable media (USB sticks, SD cards, external disks, exFAT, FAT32, NTFS volumes, and some FUSE or network mounts) is often a different device from the system disk and from `TMPDIR`. Those calls raise `EXDEV` and do not copy. A cleanup after that failure looks like the output vanished.  
12. **MUST NOT** reimplement a bare rename in product code. Which device a path is on is known only at runtime. `shutil.move` already renames when both paths are on the same device.  
13. **`shutil.copy2`**, **`shutil.copy`**, **`shutil.copyfile`**, and **`shutil.copytree`** copy only. If one of them is used, the code **MUST** say whether the source stays. They are not a move. A move **MUST** stay on `shutil.move`. Removing the source is allowed only after that copy has succeeded, and only when a move was the intent. Prefer `shutil.move` for that intent.  
14. A directory tree **MUST** move with **`shutil.move`**. On `EXDEV` it copies the tree and then removes the source. **MUST NOT** move a tree with `os.rename` or `os.replace`.

### 2.4 Corresponding commands / APIs (reference)

| Intent | Use | Do not call |
|--------|-----|-------------|
| Move, rename, replace, or publish a file or directory, including onto removable media | **`shutil.move(src, dst)`** | **`os.rename`**, **`os.replace`**, **`Path.rename`**, **`Path.replace`** |
| Copy and keep the source | **`shutil.copy2`** (or `shutil.copy` / `shutil.copyfile`) | Treating a copy as a move |
| Copy a directory tree and keep the source | **`shutil.copytree`** | **`os.rename`** of the tree |
| Same-device finish | Leave the rename to **`shutil.move`** | A product-level **`os.replace`** for atomicity |

### 2.4a Compile-time checks stay in the suite

15. A comparison whose both sides are fixed in source **MUST** be a suite assertion. It does not read argv, the clock, the network, or a user file. A failure means the tree was edited inconsistently.  
16. **MUST NOT** `raise` that comparison when the module is imported, and **MUST NOT** `raise` it at the start of `main()`.  
17. The version case is `_PKG_VERSION` built as `"{0}.{1}.{2}".format(MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION)` compared with `__version__`. `tests/test_docs.py` asserts they are equal. `src/VideoSpeed/cli.py` **MUST NOT** contain `raise RuntimeError("package version SSOT mismatch")`.  
18. A missing `ffmpeg`, a missing file, or a bad argument stays a runtime check.

### 2.4b Constants of class `Cli` are not module assignments

19. Product identity, the formatted package version, usage text, dates, the homepage, the download URL, the product verb lists, and numeric bounds **MUST NOT** be module-level assignments. That set is `_PKG_VERSION`, `APP_NAME`, `CONSOLE_NAME`, `PRODUCT_VERBS`, `LIFECYCLE_VERBS`, `AUTHOR_NAME`, `HOMEPAGE`, `LAST_UPDATE`, `DOWNLOAD_URL`, `BASIC_USAGE`, `RATIO_MIN`, and `RATIO_MAX`.  
20. **MUST** place each of those names on class `Cli`, or assign it inside `main()` and pass it down. This product places them on class `Cli`. An edit **MUST NOT** leave them at import, and **MUST NOT** move them back to module level.  
21. **MUST NOT** add a new module-level assignment for a value only class `Cli`, `main()`, or that call tree need. Another class keeps its own constants on that class. `MenuPainter` keeps the frame glyphs in `menu_painter.py`. The message sink is class `RunOutput`. **MUST NOT** add a module-level `_MESSAGE_SINK`.  
22. Version integers stay in `src/VideoSpeed/__init__.py` (`requirement-python-version`). Importing `MAJOR_VERSION`, `MINOR_VERSION`, and `PATCH_VERSION` into `cli.py` is that package read. Class `Cli` formats `_PKG_VERSION` from those three integers. Rules 15–18 still forbid raising the equality at import or at the start of `main()`. Rule 6 still forbids a drive-by StateLogic rewrite of helpers the edit does not touch.

### 2.4c One class per file

23. A class **MUST** live in its own module under `src/VideoSpeed/`. The file name is the class job in snake case (`MenuPainter` → `menu_painter.py`, `CheckSystem` → `check_system.py`). The class list is `requirement-python-oop`. That class's `__init__` **MUST** accept the one logger and pass it on when it constructs another class in the map. The instantiation line stays on `requirement-python-cli-logging`.  
24. That module **MUST** define one class. One exception type raised by that class **MAY** share the file.  
25. Functions that share the class's job **MUST** be methods. The module **MUST NOT** also define them at module level.  
26. `cli.py` **MUST** define class `Cli` and no other class. `def main` stays in `cli.py`. It builds the objects from `requirement-python-oop` and runs one job. `cli.py` **MUST NOT** define another class's methods. The console script stays `VideoSpeed.cli:main`.  
27. This shape is ordinary classes. A StateLogic and `Attr` rewrite is still not required. `TP-OOP-03` and `TP-OOP-04` prove this file rule. They have landed. This section does not add a new test id.

### 2.4d Construct the class at the site

28. An object **MUST** be created by writing `ClassName(...)` at the site that needs that object.  
29. **MUST NOT** write a function or a method whose job is to instantiate a class. That function or method is a factory. That includes a module function that returns `SomeClass(...)`, a method that returns `SomeClass(...)`, and `Cls.__new__(Cls)` followed by a method that builds the object. The caller writes `ClassName(...)`. The class can be created without a factory. A factory does not add a way to create the object that the call site lacks. It hides the class name behind a second home.  
30. ChronicleLogger **MUST** be created by the statement `ChronicleLogger(...)` inside `def main`. A method of class `Cli` is not that statement. `main` **MUST NOT** call `Cli.__new__` in order to build the logger. `is_quiet` on that constructor stays `requirement-python-cli-logging`.  
31. When the logger is present, that class's `__init__` **MUST** call `logger.log_message("instantiated", component="ClassName")` itself. **MUST NOT** call a module function to write that line. The wording of the line stays on `requirement-python-cli-logging`.

### 2.4e Attribute access by name

32. Product Python and the suite **MUST** read and write an attribute by its name.  
33. **MUST NOT** read or write `__dict__` on a module, a class, or an instance unless the user explicitly orders that access for that edit. Saving a `staticmethod` out of the class mapping and putting that descriptor back is that banned access.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Package** | `VideoSpeed` |
| **Primary modules** | `src/VideoSpeed/cli.py`, `__main__.py`, `__init__.py` |
| **Staging helpers** | `staging_dir_for`, `make_temp_path` |
| **Publish helper** | `FileStage.promote_file` → `shutil.move` only (`requirement-python-oop`) |
| **Ship modules** | `src/VideoSpeed/*.py` except the archive below. No `os.rename`, `os.replace`, `Path.rename`, or `Path.replace` calls |
| **Archive** | `src/VideoSpeed/cli.bootstrap-old.py` is not the ship unit. It still calls `os.replace`. Do not copy that call into ship modules |
| **Ops apply** | `requirement-video-ffmpeg-pipeline` |
| **Architecture shape today** | Ordinary classes, one class per file, ordered by `requirement-python-oop`. `def main` stays in `cli.py`. StateLogic rewrite of the encoder and of `main` is not ordered. `TP-OOP-03` and `TP-OOP-04` have landed |
| **System-status lines** | `requirement-python-cli-logging` — `def main` writes `ChronicleLogger(...)`. Pass that object into every class. Each `__init__` calls `log_message("instantiated", ...)` itself. A major file operation (write a temp, publish, discard an unfinished temp) logs the operation and the paths on that same logger. Thread creation and thread operations log on that same logger before the call that can block, and not while a work lock is held. `log_message` only. A non-TUI, non-JSON run shows `debug mode` when `isDebug()` is true. Do not add a second logger here. Do not add a factory (a function or a method whose job is to instantiate a class). Control-C is `requirement-python-graceful-exit` (ask `Exit? (y/n)` on an open text screen, log the decision, stop a live child, do not publish, exit 130 on yes) |
| **Factory** | Ship modules write `ClassName(...)` at the site. `tests/test_logging.py` `_spy_logger` still uses a function named `factory` to call `ChronicleLogger(...)`. That function is the banned shape. This version does not rewrite the spy |
| **Package version** | `requirement-python-version` |
| **Version equality** | Suite only: `tests/test_docs.py` asserts `_PKG_VERSION == __version__`. Import does not raise |
| **Identity block home** | Attributes of class `Cli` in `src/VideoSpeed/cli.py`. A local inside `main()` is the other allowed home. Module level is not |
| **Identity block** | `_PKG_VERSION`, `APP_NAME`, `CONSOLE_NAME`, `PRODUCT_VERBS`, `LIFECYCLE_VERBS`, `AUTHOR_NAME`, `HOMEPAGE`, `LAST_UPDATE`, `DOWNLOAD_URL`, `BASIC_USAGE`, `RATIO_MIN`, `RATIO_MAX`. The message sink is `RunOutput`, not a module name |
| **Attribute access** | By name on the object or the class. `__dict__` only when the user orders that access for that edit |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution**: Multi-mount path failures are loud. A source mismatch fails the suite. Import does not raise it.  
- **Principle 3 – Anti-fragile**: USB and system disk both work for publish.  
- **Principle 5 – SSOT**: One coding-style home for move, temp, and identity rules. Identity, verb lists, and bounds are attributes of class `Cli`.  
- **Principle 11 – Temps**: Explicit staging and cleanup.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, file moves and status lines stay at this login. **This requirement:** do not use admin privilege, `sudo`, or a system package manager to publish a file or to write the status log. Control-C stays `requirement-python-graceful-exit`.

---

## Sample code

`FileStage.promote_file` in `src/VideoSpeed/file_stage.py` publishes with `shutil.move`. `def main` writes `ChronicleLogger(...)` and `Cli(logger)`. It does not call `shutil.move`. The program was not changed.

```python
class FileStage:
    def promote_file(self, src, dest):
        src = Path(src)
        dest = Path(dest)
        if not src.is_file():
            raise FileNotFoundError("promote source missing: {}".format(src))
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dest))

class Cli:
    APP_NAME = "VideoSpeed"
    CONSOLE_NAME = "video-speed"

def main(argv=None, log_basedir="", log_logdir=""):
    show_mirror = Cli._show_log_mirror(argv)
    logger = ChronicleLogger(
        logname="VideoSpeed",
        basedir=log_basedir or "",
        logdir=log_logdir or "",
        is_quiet=not show_mirror,
    )
    app = Cli(logger)
    return app.run(argv, logger=logger)
```

`Cli(logger)` is the construct. A function that returns `Cli(...)` is a factory. `shutil.move` is inside `FileStage.promote_file`. Same device renames. Another device copies, then removes the source. `os.rename` and `os.replace` are not this sample.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Do not assume one filesystem.  
- **Intentional:** `shutil.move` is the only move and publish API.  
- **Anti-fragile:** Same-directory temps avoid a full-file copy. Removable media still publishes when the devices differ.  
- **Over-protect:** Ship code does not grow a same-mount exception that calls `os.rename` or `os.replace`. It also does not grow an import-time version `raise`, a module-level assignment for identity, verb lists, bounds, or a message sink, a second class in a class file, a factory (a function or method whose job is to instantiate a class), or a `__dict__` read or write the user did not order.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Call `os.rename`, `os.replace`, `Path.rename`, or `Path.replace` to move or publish a file, including when the path looks like the same disk.  
2. Stage all large intermediates only under system temp when final dest is known on another mount.  
3. Cite templates/skills as product-source behavioral authority.  
4. Force a full StateLogic rewrite of the encoder or of `main` without an explicit user order. One class per file follows `requirement-python-oop` and is not that rewrite.  
4b. Add a module-level function for a job that already has a class, or put a second class in that class's file. `cli.py` keeps class `Cli` and `def main`.  
4c. Instantiate a class from a function or a method. That function or method is a factory. The class can be created without one. The site that needs the object writes `ClassName(...)`. `def main` writes `ChronicleLogger(...)`. Each `__init__` writes its own `log_message("instantiated", ...)` call.  
5. Store secrets in style docs or code.  
6. Put the `_PKG_VERSION` versus `__version__` comparison back on the import path, or add any other source-versus-source `raise` at import or at the start of `main()`.  
7. Add a module-level assignment for `_PKG_VERSION`, `APP_NAME`, `CONSOLE_NAME`, `PRODUCT_VERBS`, `LIFECYCLE_VERBS`, `AUTHOR_NAME`, `HOMEPAGE`, `LAST_UPDATE`, `DOWNLOAD_URL`, `BASIC_USAGE`, `RATIO_MIN`, `RATIO_MAX`, `_MESSAGE_SINK`, or a new name of that kind. Place them on class `Cli`, or assign them inside `main()` and pass them down.  
8. Read or write `__dict__` on a module, a class, or an instance unless the user explicitly orders that access for that edit. Use the attribute name.

**Violating this rule is a critical regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Every file move and publish uses `shutil.move` (or a thin wrapper that only calls it) |
| AC-2 | Ship modules do not call `os.rename`, `os.replace`, `Path.rename`, or `Path.replace` |
| AC-3 | Same-FS staging preferred when dest known |
| AC-4 | Pipeline REQ remains ops SSOT for encode |
| AC-5 | Registered in index |
| AC-6 | Removable media (USB and the same class of disk) is in scope for the move rule |
| AC-7 | Version triple versus `__version__` is a suite assertion. Import does not raise it |
| AC-8 | `_PKG_VERSION`, `APP_NAME`, `CONSOLE_NAME`, `PRODUCT_VERBS`, `LIFECYCLE_VERBS`, `AUTHOR_NAME`, `HOMEPAGE`, `LAST_UPDATE`, `DOWNLOAD_URL`, `BASIC_USAGE`, `RATIO_MIN`, and `RATIO_MAX` are attributes of class `Cli` (or locals inside `main()`). They are not module-level assignments |
| AC-9 | Each class lives in its own module. `cli.py` defines class `Cli` and `def main` |
| AC-10 | No function or method exists in order to instantiate a class. `def main` contains `ChronicleLogger(...)`. Each `__init__` calls `log_message("instantiated", ...)` itself |
| AC-11 | Ship modules and the suite do not read or write `__dict__` unless the user ordered that access for that edit |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-video-ffmpeg-pipeline` | Applies move/temp rules to encode |
| `requirement-python-project-structure` | Layout |
| `requirement-python-error-handling` | Fail messaging |
| `requirement-python-cli-interface` | Entry |
| `requirement-class-software-dev` | Class residual |
| `requirement-python-oop` | Class map. One class per file. `def main` stays in `cli.py`. The logger is an `__init__` parameter |
| `requirement-python-cli-logging` | One logger. Major file operations and thread operations log here |
| `requirement-python-graceful-exit` | Control-C confirm, exit log, and the child stop |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| TP-FS-01 | `tests/test_fs.py` | have | `shutil.move` + two dirs |
| TP-FS-02 | `tests/test_fs.py` | have | staging parent |
| TP-FS-05 | `tests/test_fs.py` | have | ship modules do not call `os.rename` or `os.replace` |
| TP-DOC-02 | `tests/test_docs.py` | have | `_PKG_VERSION == __version__`; ship module does not raise that mismatch |
| TP-STYLE-01 | `tests/test_docs.py` | have | identity, verb lists, formatted version, and bounds are attributes of class `Cli`, not module assignments |
| TP-STYLE-02 | `tests/test_docs.py` | have | ship modules and the suite do not read or write `__dict__`. The archive is in that scan |
| TP-OOP-03 · TP-OOP-04 | `tests/test_tui.py` · `tests/test_cli.py` | have | One class per file. Owned by `requirement-python-oop`. `TP-OOP-04` also asserts `def main` contains `logger = ChronicleLogger(`, and that ship source has no `Cli.__new__` and no `log_instantiated`. This file does not add a style test id |
| TP-PKG-01 | `tests/test_package.py` | have | import without cv2 |
| Code review | `reviews/reports/*` | pass (2026-08-09) | later tightened by TP-FS-05 |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Coding style + shutil.move / multi-mount file I/O |
| 2026-08-19 | Active 1.1.0 | §1.1; TP-FS have |
| 2026-10-01 | Active 1.2.0 | File moves use `shutil.move`. Ship code does not call `os.rename` or `os.replace` (removable media) |
| 2026-10-01 | Active 1.3.0 | Version equality is a suite check. Identity, bounds, and the message sink belong inside `main()` |
| 2026-10-01 | Active 1.3.1 | StateLogic stays aspirational for the encoder and `main`. `Tui` and `CheckSystem` are `requirement-python-oop` |
| 2026-10-01 | Active 1.4.0 | One class per file. `def main` stays in `cli.py`. The procedural pile is not an allowed end state. `TP-OOP-03` and `TP-OOP-04` stay todo |
| 2026-10-01 | Active 1.4.1 | `TP-OOP-03` and `TP-OOP-04` have landed. Identity locals still sit at import (`TP-STYLE-01` stays todo) |
| 2026-10-01 | Active 1.4.2 | Status lines stay on ChronicleLogger. The non-TUI, non-JSON console shows `debug mode` |
| 2026-10-01 | Active 1.4.3 | Every class receives the one logger and logs `instantiated` |
| 2026-10-01 | Active 1.4.4 | Control-C is `requirement-python-graceful-exit`. Major file-operation lines stay on the one ChronicleLogger |
| 2026-10-01 | Active 1.4.5 | Thread creation and thread operations stay on `requirement-python-cli-logging`. Do not duplicate |
| 2026-10-01 | Active 1.4.6 | Each class `__init__` accepts the logger. The constructor home is `requirement-python-oop`. The instantiation line stays on `requirement-python-cli-logging` |
| 2026-10-02 | Active 1.4.7 | An object is `ClassName(...)` at the site that needs it. A function or a method does not instantiate a class. `def main` writes `ChronicleLogger(...)`. Each `__init__` writes its own instantiation line |
| 2026-10-02 | Active 1.4.8 | `TP-OOP-04` asserts that construct statement and the absence of `log_instantiated` and `Cli.__new__`. `./tests/run.sh` on this date: 86 tests, OK, skipped=1 |
| 2026-10-02 | Active 1.4.9 | Attribute access is by name. `__dict__` stays out of ship modules and the suite unless the user orders that access for that edit. `TP-STYLE-02` have. `./tests/run.sh` on this date: 87 tests, OK, skipped=1 |
| 2026-10-02 | Active 1.4.10 | Identity, the formatted version, the verb lists, and the length bounds are attributes of class `Cli`. They are not module-level assignments. `TP-STYLE-01` have. `./tests/run.sh` on this date: 88 tests, OK, skipped=1 |
| 2026-10-02 | Active 1.4.11 | A function or a method whose job is to instantiate a class is a factory. The class can be created without one. The caller writes `ClassName(...)`. No new proof id. The suite spy in `tests/test_logging.py` is still that shape |
| 2026-10-02 | Active 1.4.12 | Control-C confirm, the exit log, and the child stop stay on `requirement-python-graceful-exit`. Do not duplicate |
| 2026-10-02 | Active 1.4.13 | Sample code shows `Cli(logger)` and `shutil.move`. Identity stays on class `Cli` |
| 2026-10-05 | Active 1.4.14 | Sample code is `FileStage.promote_file` (`shutil.move` inside that method) and `def main` writing `ChronicleLogger(...)` then `Cli(logger)`. `shutil.move` is not inside `main`. The program was not changed |

---

**Last Updated**: 2026-10-05  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
