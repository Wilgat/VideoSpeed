**file**: docs/requirements/requirement-python-coding-style.md  
**Status**: Active (Version 1.4.1)  
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
| Same-directory staging; `shutil.move` for every move and publish; lazy OpenCV import; identity locals inside `main()`; version equality in the suite; one class per file | Filter graphs; argparse flags; `os.rename` / `os.replace`; import-time version `raise`; module globals for identity and bounds; a second class in a class file |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/VideoSpeed/file_stage.py` | class `FileStage` | `promote_file` / `staging_dir_for` (`requirement-python-oop`) |
| `./tests/run.sh` | suite | TP-FS-01 / TP-FS-02 |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Save onto a USB stick | Temps sit next to the output when that folder is writable. `shutil.move` renames on the stick and copies when the stick is a different device. | Keep `FileStage.promote_file` → `shutil.move` |
| Check that the version string matches the three integers | The suite compares them. Starting the program does not raise if a maintainer left them mismatched. | `tests/test_docs.py` |
| Name the program | `APP_NAME` and the other identity values are locals inside `main()`, passed into the menu and the about page. | Assign them in `main()` |

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

### 2.4b Module globals belong inside `main()`

19. Product identity, usage text, dates, the homepage, the download URL, numeric bounds, and the mutable message sink **MUST NOT** be module-level globals.  
20. **MUST** assign them inside `main()` and pass them into the helpers that need them.  
21. **MUST NOT** add a new module global for a value only `main()` and its call tree need.  
22. The names in Implementation Notes are that block. They still sit at import today. The next edit that touches one of them **MUST** move that name under `main()` in the same change. Rule 6 still forbids a drive-by StateLogic rewrite of helpers the edit does not touch.

### 2.4c One class per file

23. A class **MUST** live in its own module under `src/VideoSpeed/`. The file name is the class job in snake case (`MenuPainter` → `menu_painter.py`, `CheckSystem` → `check_system.py`). The class list is `requirement-python-oop`.  
24. That module **MUST** define one class. One exception type raised by that class **MAY** share the file.  
25. Functions that share the class's job **MUST** be methods. The module **MUST NOT** also define them at module level.  
26. `cli.py` **MUST** define class `Cli` and no other class. `def main` stays in `cli.py`. It builds the objects from `requirement-python-oop` and runs one job. `cli.py` **MUST NOT** define another class's methods. The console script stays `VideoSpeed.cli:main`.  
27. This shape is ordinary classes. A StateLogic and `Attr` rewrite is still not required. `TP-OOP-03` and `TP-OOP-04` prove this file rule. They have landed. This section does not add a new test id.

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
| **System-status lines** | `requirement-python-cli-logging` — do not add a second logger here |
| **Package version** | `requirement-python-version` |
| **Version equality** | Suite only: `tests/test_docs.py` asserts `_PKG_VERSION == __version__`. Import does not raise |
| **Identity block home** | Inside `main()` in `src/VideoSpeed/cli.py`. Still module-level until the next edit that touches a name |
| **Identity block** | `APP_NAME`, `CONSOLE_NAME`, `AUTHOR_NAME`, `HOMEPAGE`, `LAST_UPDATE`, `DOWNLOAD_URL`, `BASIC_USAGE`, `_MESSAGE_SINK`, `RATIO_MIN`, `RATIO_MAX` |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution**: Multi-mount path failures are loud. A source mismatch fails the suite. Import does not raise it.  
- **Principle 3 – Anti-fragile**: USB and system disk both work for publish.  
- **Principle 5 – SSOT**: One coding-style home for move, temp, and identity rules. Identity values live in `main()` and are passed down.  
- **Principle 11 – Temps**: Explicit staging and cleanup.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Do not assume one filesystem.  
- **Intentional:** `shutil.move` is the only move and publish API.  
- **Anti-fragile:** Same-directory temps avoid a full-file copy. Removable media still publishes when the devices differ.  
- **Over-protect:** Ship code does not grow a same-mount exception that calls `os.rename` or `os.replace`. It also does not grow an import-time version `raise`, a new module global for identity, bounds, or the message sink, or a second class in a class file.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Call `os.rename`, `os.replace`, `Path.rename`, or `Path.replace` to move or publish a file, including when the path looks like the same disk.  
2. Stage all large intermediates only under system temp when final dest is known on another mount.  
3. Cite templates/skills as product-source behavioral authority.  
4. Force a full StateLogic rewrite of the encoder or of `main` without an explicit user order. One class per file follows `requirement-python-oop` and is not that rewrite.  
4b. Add a module-level function for a job that already has a class, or put a second class in that class's file. `cli.py` keeps class `Cli` and `def main`.  
5. Store secrets in style docs or code.  
6. Put the `_PKG_VERSION` versus `__version__` comparison back on the import path, or add any other source-versus-source `raise` at import or at the start of `main()`.  
7. Add module globals for `APP_NAME`, `CONSOLE_NAME`, `AUTHOR_NAME`, `HOMEPAGE`, `LAST_UPDATE`, `DOWNLOAD_URL`, `BASIC_USAGE`, `_MESSAGE_SINK`, `RATIO_MIN`, `RATIO_MAX`, or a new name of that kind. Assign them inside `main()`.

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
| AC-8 | `APP_NAME`, `CONSOLE_NAME`, `AUTHOR_NAME`, `HOMEPAGE`, `LAST_UPDATE`, `DOWNLOAD_URL`, `BASIC_USAGE`, `_MESSAGE_SINK`, `RATIO_MIN`, and `RATIO_MAX` are assigned inside `main()` |
| AC-9 | Each class lives in its own module. `cli.py` defines class `Cli` and `def main` |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-video-ffmpeg-pipeline` | Applies move/temp rules to encode |
| `requirement-python-project-structure` | Layout |
| `requirement-python-error-handling` | Fail messaging |
| `requirement-python-cli-interface` | Entry |
| `requirement-class-software-dev` | Class residual |
| `requirement-python-oop` | Class map. One class per file. `def main` stays in `cli.py` |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| TP-FS-01 | `tests/test_fs.py` | have | `shutil.move` + two dirs |
| TP-FS-02 | `tests/test_fs.py` | have | staging parent |
| TP-FS-05 | `tests/test_fs.py` | have | ship modules do not call `os.rename` or `os.replace` |
| TP-DOC-02 | `tests/test_docs.py` | have | `_PKG_VERSION == __version__`; ship module does not raise that mismatch |
| TP-STYLE-01 | `tests/test_docs.py` | todo | identity block assigned inside `main()`, not at import |
| TP-OOP-03 · TP-OOP-04 | `tests/test_tui.py` · `tests/test_cli.py` | have | One class per file. Owned by `requirement-python-oop`. This file does not add a style test id |
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

---

**Last Updated**: 2026-10-01  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
