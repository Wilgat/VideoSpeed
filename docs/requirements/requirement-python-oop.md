**file**: docs/requirements/requirement-python-oop.md
**Status**: Active (Version 1.2.16)
**Area**: python
**Key**: `requirement-python-oop`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define when VideoSpeed uses a class, and name the file that holds each class. One class lives in one module. `def main` stays in `src/VideoSpeed/cli.py`. Every class in the map accepts the one status logger as an `__init__` parameter so that class can log. The line text stays on `requirement-python-cli-logging`.

The menu picture stays on `requirement-python-tui`. The menu language stays on `requirement-python-cli-language`. The about-page lines stay on `requirement-python-about`. The pyenv root and the pyenv path stay on `requirement-python-pyenv`. The conda root, the conda path, and the python2 and python3 paths while under conda stay on `requirement-python-conda`. Encode order stays on `requirement-video-ffmpeg-pipeline`. The JSON object shape stays on `requirement-python-json-output`. This file decides the class and the file. It does not invent a second picture, a second line list, a second encode order, or a second JSON shape.

`TP-OOP-01`, `TP-OOP-02`, `TP-OOP-03`, and `TP-OOP-04` have landed. The session has left `cli.py`. The painter, the screen types, and the other jobs are the classes in the map.

### 1.1 Human-facing

**In one sentence:** Each class lives in its own file, `main` stays in `cli.py`, and each class receives the logger in `__init__`.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Maintainer adding a prompt, a host-check read, or an encode step | Put it on the class that already owns that job |
| The other role | The menu picture, the about lines, the encode order, and the JSON shape | Their own requirements |
| Not this file | A StateLogic rewrite of `main` | `requirement-python-coding-style` |

| Includes | Excludes |
|----------|----------|
| One class per file; the class is the only public surface of that module; constants that `Cli` owns live on class `Cli` | A second class in the same file, a module-level function beside the class, or a module-level assignment of `Cli`'s identity, verb lists, or bounds |
| `def main` in `src/VideoSpeed/cli.py` | Moving `main` to another module |
| Ordinary classes named in the map below | One class per function; a StateLogic rewrite |
| The one logger passed into `__init__`; `ClassName(...)` at the site that needs the object | A setter, a module global, a second logger built inside the class, or a factory |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/VideoSpeed/cli.py` | `def main` and class `Cli` | Entry. Builds the other objects and runs one job |
| `src/VideoSpeed/tui.py` | class `Tui` | Text-menu session |
| `src/VideoSpeed/check_system.py` | class `CheckSystem` | `[CHECK SYSTEM]` reads |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Add a menu prompt | It is a method on `Tui`. The frame is `MenuPainter`. | Edit the class file this requirement names |
| Add a host-check field | It is a method on `CheckSystem`. `AboutPage` calls that object. | Edit `src/VideoSpeed/check_system.py` |
| Start the program | The console script calls `VideoSpeed.cli:main`. | `video-speed` |
| Name a constant the program uses | It is an attribute of the class that owns it. `Cli` owns identity, the verb lists, and the length bounds. | `Cli.APP_NAME` |

---

## 2. Core Rules (Mandatory)

### 2.1 Use a class when the functions share one job

1. When a set of functions shares one job, product Python **MUST** make them methods of one class and put that class in its own module under `src/VideoSpeed/`.  
2. **MUST NOT** make a class whose only method is a single function that nothing else in the file shares.  
3. The class **MUST** be the only public surface of its module. A module-level `def` beside that class is a second home. **MUST NOT** add one.  
4. That module **MUST** define one class. One exception type raised by that class **MAY** share the file. `MenuScreenError` shares `menu_session.py` with `MenuSession`.  
5. The file name **MUST** be the class job in snake case (`MenuPainter` → `menu_painter.py`, `CheckSystem` → `check_system.py`).  
6. A full StateLogic + `Attr` rewrite of the encoder and of `main` stays aspirational (`requirement-python-coding-style`). This file does not order that rewrite. The classes in the map are ordinary classes.

### 2.2 Entry: `main` stays in `cli.py`

7. `src/VideoSpeed/cli.py` **MUST** define class `Cli` and **MUST NOT** define another class.  
8. `def main` **MUST** stay in `src/VideoSpeed/cli.py`. The signature stays `main(argv=None, log_basedir="", log_logdir="")`. `main` builds the objects in this file and runs one job.  
9. The console script **MUST** stay `video-speed = "VideoSpeed.cli:main"`. `src/VideoSpeed/__main__.py` **MUST** keep `from .cli import main`.  
10. `cli.py` **MUST NOT** define another class's methods. `Cli` owns `build_parser`, `_dispatch`, `_opens_text_screen`, `_verb_help`, `_verb_page`, `_verb_about`, `_verb_edit`, `_verb_list_mp4`, `_unknown_verb`, `stdin_is_tty`, and `stdout_is_tty`. `Cli` does not own `_verb_hello`. `Cli` does not own the ChronicleLogger construct. Pip lifecycle verbs stay on `SelfManage`.  
11. `Cli` constructs the other classes and calls them. Each class receives its collaborators through its constructor. A lazy `_host()` import of `cli` is not the end state.  
11f. A constant or variable that class `Cli` or `def main` owns is an attribute of class `Cli`, or a name assigned inside `main()`. It is not a module-level assignment in `cli.py`. That set is `_PKG_VERSION`, `APP_NAME`, `CONSOLE_NAME`, `PRODUCT_VERBS`, `LIFECYCLE_VERBS`, `AUTHOR_NAME`, `HOMEPAGE`, `LAST_UPDATE`, `DOWNLOAD_URL`, `BASIC_USAGE`, `RATIO_MIN`, and `RATIO_MAX`. `Cli` passes the values other classes print. Those classes do not import the names from the `cli` module.  
11g. Another class keeps its own constants. The frame glyphs, `MENU_ROWS`, and `SELF_ROWS` stay on `MenuPainter`. Version integers stay in `__init__.py` (rule 27). Importing those integers into `cli.py` is the package read that class `Cli` formats into `_PKG_VERSION`.

### 2.2a The logger arrives through `__init__`

11a. Every class in the map, and `MenuScreenError`, **MUST** accept the one ChronicleLogger as a parameter of `__init__`.  
11b. `__init__` **MUST** store that object on `self.logger`. A class that constructs another class in the map **MUST** pass that same object into that constructor.  
11c. `def main` writes `ChronicleLogger(...)` before `Cli` (`requirement-python-cli-logging`) and **MUST** pass that object into `Cli(...)`. `main` **MUST NOT** call `Cli.__new__` to build the logger. The parameter **MAY** default to absent so a caller that has no logger can omit it. `main` has the logger and **MUST NOT** omit it.  
11d. **MUST NOT** construct a ChronicleLogger inside a class or from a method. **MUST NOT** attach the logger through a setter or a module global after `__init__` returns. **MUST NOT** call a module function to write the instantiation line. `__init__` calls `log_message` itself.  
11e. The instantiation line, its level, and quiet stay on `requirement-python-cli-logging`. This file owns only that the logger arrives through `__init__`.  
11h. The site that needs an object **MUST** write `ClassName(...)`. A factory is a function or a method whose job is to instantiate a class. This map does not include a factory. The class can be created without one. The full ban stays on `requirement-python-coding-style`.  

### 2.3 Text menu

12. `src/VideoSpeed/tui.py` **MUST** define class `Tui` and no other class. `Tui` owns `open_text_menu`, `menu_lines`, `self_menu_lines`, `log_menu_lines`, `language_menu_lines`, `framework_help`, `_boards`, `_apply_language`, `_pick_language`, `_edit_in_tui`, `_list_in_tui`, `_view_log`, `_clear_log`, `_log_folder`, `_open_direct_screen`, `_visible_lines`, `_tui_read`, `_tui_notice`, `_tui_float`, `_tui_yes_no`, and `_tui_index`. `Tui` does not own `framework_hello`.  
13. Class `MenuPainter` in `src/VideoSpeed/menu_painter.py` owns `paint`, `paint_prompt`, `path_label`, `set_path_label`, `clock_text`, `path_line`, `format_rows`, `row_parts`, `rows_for`, `screen_can_hold_box`, `_put`, `_paint_box`, `_input_field`, `_status_line`, `_result_overflow`, and `_result_room`. The frame glyphs, `MENU_ROWS`, `SELF_ROWS`, `LOG_ROWS`, and `LANG_ROWS` live in that module. `FRAME_TOP_LEFT` **MUST NOT** appear in `cli.py`. `path_label`, `clock_text`, and `path_line` draw the first row of the front board, of the language board, of the self-management board, and of the system-log board. The words, the clock shape, shortening that path from the left, and when the clock is omitted stay on `requirement-python-tui` rule 13. These methods do not detect a language and do not invent a second line. `set_path_label` stores the word the caller already chose.  
14. Class `MenuModel` in `src/VideoSpeed/menu_model.py` owns the keystroke state and `edge_keys`.  
15. Class `MenuSession` in `src/VideoSpeed/menu_session.py` owns `run` and `_wait_key`, and raises `MenuScreenError`. `_wait_key` is the one-second clock wait from `requirement-python-tui` rule 13. It does not start a thread. The picture of that wait stays on that requirement.  
16. The menu picture (rows, box, about page, fail-closed small screen) stays on `requirement-python-tui`. The front board has no hello row. These classes implement that picture. They do not invent a second layout.  
17. `TP-OOP-01` has landed for the session leaving `cli.py`. `cli.py` **MUST NOT** hold those session functions. `TP-OOP-03` has landed. The proof reads `MenuPainter`, `MenuModel`, and `MenuSession` in their own modules. It **MUST NOT** require `MenuSession` to live in `tui.py`.

### 2.4 Host check and about page

18. Every host-check function **MUST** be a method of class `CheckSystem` in `src/VideoSpeed/check_system.py`.  
19. That set is `check_system_lines`, `parse_sys_version`, `arch_label`, `libc_label`, `binary_type`, `current_user`, `shell_text`, `python_executable_name`, `command_location`, `os_text`, `inside_docker`, `cpython_soabi`, `self_location`, `process_id`, `cache_folder_preferred`, `cache_folder_first_fallback`, `cache_folder_second_fallback`, `cache_folder_used`, `persistence_storage`, `tty_interactive`, `in_venv`, `in_pyenv`, `in_conda`, `under_pyenv`, `pyenv_root`, `pyenv_location`, `pyenv_version_names`, `pyenv_interpreter`, `under_conda`, `conda_root`, `conda_location`, `conda_prefix`, `conda_interpreter`, and `about_tool_location`.  
20. Class `AboutPage` in `src/VideoSpeed/about_page.py` owns `framework_about`, `about_box_lines`, `install_kind`, `install_sentence`, and `_is_source_checkout`. It **MUST** call `CheckSystem` for the check block and for `self_location`. The line text and the star box stay on `requirement-python-about`. `PID`, the cache folder chain, persistence storage, and `TTY / Interactive` stay on `requirement-python-about`. `in_venv`, `in_pyenv`, and `in_conda` stay on `requirement-python-cli-logging`. They do not choose the location lines. The pyenv root and the pyenv path stay on `requirement-python-pyenv`. The conda root, the conda path, and the python2 and python3 paths while under conda stay on `requirement-python-conda`.  
21. `TP-OOP-02` has landed. `cli.py` **MUST NOT** hold the rule 19 functions. `TP-OOP-04` has landed. The about composer is `AboutPage`. `cli.py` **MUST NOT** keep that composer.

### 2.5 The other jobs

22. Class `EditWalk` in `src/VideoSpeed/edit_walk.py` owns the shared question order: folder, file, start, end, percent, boomerang, again. The screen path and the `--json` stderr path both call it. The question text stays on `requirement-python-interactive-vs-noninteractive` and `requirement-python-json-output`.  
23. Class `Encoder` in `src/VideoSpeed/encoder.py` owns `ensure_ffmpeg`, `run_ffmpeg`, `_restore_text_screen`, `cut_clip`, `_atempo_filters`, `speed_change`, `add_boomerang`, `process_job`, `batch_session`, `build_output_name`, `valid_cut_range`, `valid_percent`, and `_length_unchanged`. Cut, speed, and boomerang order stay on `requirement-video-ffmpeg-pipeline`.  
24. Class `MediaInfo` in `src/VideoSpeed/media_info.py` owns `get_mp4_files`, `get_duration_cv2`, and `format_time`.  
25. Class `FileStage` in `src/VideoSpeed/file_stage.py` owns `staging_dir_for`, `make_temp_path`, and `promote_file`. Publish stays `shutil.move` (`requirement-python-coding-style`).  
26. Class `RunOutput` in `src/VideoSpeed/run_output.py` owns `out_info`, `out_err`, the message sink, `_call_sunk`, `_collect_lines`, and the JSON object (`_json_reset`, `_remember`, `_remember_job`, `_emit_json`). The object shape stays on `requirement-python-json-output`.  
26a. Class `SelfManage` in `src/VideoSpeed/self_management.py` owns `local_version`, `argv_for`, `run_text`, `emit`, and `_subprocess_runner`. The verb names and the pip command strings stay on `requirement-python-cli-interface`. `cli.py` **MUST NOT** build those pip argument lists.  
26b. Class `SystemLog` in `src/VideoSpeed/system_log.py` owns `log_dir`, `log_files`, `read_log`, `clear_log`, and `folder_text`. The menu rows and the result-page words stay on `requirement-python-tui`. `Tui` writes `SystemLog(...)` at the site that needs it and passes the same logger. `cli.py` **MUST NOT** list the log files, read one, or empty one.  
26c. Class `LanguageMenu` in `src/VideoSpeed/language_menu.py` owns the thirteen codes, the language file, `path`, `save`, `boards`, `titles`, `tokens`, `path_label`, `unknown_choice`, `saved_line`, `failed_line`, and `apply_to`. The menu numbers and the box stay on `requirement-python-tui`. The codes and the words that follow a language stay on `requirement-python-cli-language`. `Tui` writes `LanguageMenu(...)` at the site that needs it and passes the same logger. `apply_to` copies rows onto a session. It does not construct a class. `cli.py` **MUST NOT** read or write the language file.  
27. Version integers stay on `requirement-python-version` in `src/VideoSpeed/__init__.py`.  
28. `TP-OOP-04` has landed. An edit that touches one of rules 22–26 **MUST** keep that class's whole set on its class. **MUST NOT** leave the set as module-level functions in `cli.py`.

### 2.6 Implementation Notes (this project)

| Class | File | Owns |
|-------|------|------|
| `Tui` | `src/VideoSpeed/tui.py` | Text-menu session (rule 12) |
| `MenuPainter` | `src/VideoSpeed/menu_painter.py` | Frame, `MENU_ROWS`, `SELF_ROWS`, `LOG_ROWS`, `LANG_ROWS`, `paint`, `path_line`, `set_path_label`, `clock_text`, `format_rows` |
| `MenuModel` | `src/VideoSpeed/menu_model.py` | Keystroke state, `edge_keys` |
| `MenuSession` | `src/VideoSpeed/menu_session.py` | `run`, `_wait_key`. Raises `MenuScreenError` |
| `CheckSystem` | `src/VideoSpeed/check_system.py` | Host-check set (rule 19) |
| `AboutPage` | `src/VideoSpeed/about_page.py` | About composer. Calls `CheckSystem` |
| `EditWalk` | `src/VideoSpeed/edit_walk.py` | Folder, file, start, end, percent, boomerang, again |
| `Encoder` | `src/VideoSpeed/encoder.py` | Cut, speed, boomerang, `process_job` |
| `MediaInfo` | `src/VideoSpeed/media_info.py` | MP4 list, duration, `format_time` |
| `FileStage` | `src/VideoSpeed/file_stage.py` | Staging and `promote_file` |
| `RunOutput` | `src/VideoSpeed/run_output.py` | Info, error, and the JSON object |
| `SelfManage` | `src/VideoSpeed/self_management.py` | Local version and the pip commands for `version-check`, `self-update`, `self-install`, and `self-uninstall` |
| `SystemLog` | `src/VideoSpeed/system_log.py` | Log folder from `logDir()`, the `.log` file list, the read, and the empty (rule 26b) |
| `LanguageMenu` | `src/VideoSpeed/language_menu.py` | Thirteen codes, the language file, and the words that follow a language (rule 26c) |
| `Cli` | `src/VideoSpeed/cli.py` | Parser, dispatch, verbs, tty checks. Owns the identity constants, the verb lists, and the length bounds (rule 11f). `def main` stays in this file |

| Item | Value |
|------|--------|
| **Console script** | `video-speed = "VideoSpeed.cli:main"` |
| **Module entry** | `src/VideoSpeed/__main__.py` imports `main` from `.cli` |
| **Landed** | `TP-OOP-01` session left `cli.py`. `TP-OOP-02` host check is `CheckSystem`. `TP-OOP-03` painter and screen types left `tui.py`. `TP-OOP-04` the other jobs left `cli.py` |
| **Logger** | Every class `__init__` in the map accepts `logger` and stores it. `def main` writes `ChronicleLogger(...)` and then `Cli(logger)`. Collaborators are `OtherClass(...)` at the site that needs them. The instantiation line is written in `__init__` (`requirement-python-cli-logging`, `TP-LOG-05` have) |
| **Not this split** | Menu rows, about line text, encode order, JSON object shape, version integers, the wording of the instantiation line |

### 2.7 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Each job has one class and one file. That class receives the logger in `__init__`.  
- **Principle 5 – SSOT**: `cli.py` does not keep a second copy of another class's methods. `main` has one home.  
- **Principle 1 – Caution**: The picture, the lines, the encode order, and the JSON shape stay where they already work.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, each class still receives the logger through `__init__` at this login. **This requirement:** do not use admin privilege, `sudo`, or a system package manager to construct a class or to pass the logger.

---

## Sample code

`StateLogic` stays unordered. The site writes the class name.

```python
def main(argv=None):
    logger = ChronicleLogger(logname="VideoSpeed", is_quiet=json_or_text_screen)
    app = Cli(logger)
    return app.run(argv)

class Cli:
    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="Cli")
        self.tui = Tui(logger)
```

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Move a whole named set together. A half-move leaves two homes.  
- **Intentional:** The map above is the class list. `main` stays in `cli.py`.  
- **Anti-fragile:** Picture, lines, encode order, and JSON shape keep their own requirements.  
- **Over-protect:** Do not flatten a class back into module functions. Do not put a second class in its file. Do not build the logger inside the class. Do not park `Cli`'s constants at module level. Do not add a factory. The caller writes `ClassName(...)`.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Add a module-level function for a job that already has a class.  
2. Put a second class in that class's file. `MenuScreenError` with `MenuSession` is the allowed exception.  
3. Move `def main` out of `src/VideoSpeed/cli.py`, or point the console script at another callable.  
4. Define another class's methods in `cli.py`.  
5. Copy `FRAME_TOP_LEFT` into `cli.py`.  
6. Split one class across two modules.  
7. Rewrite `cut_clip`, `speed_change`, or `add_boomerang` into StateLogic because this file exists.  
8. Change the about line list or the menu rows in this file.  
9. Mark `TP-OOP-03` or `TP-OOP-04` have before the suite asserts the new homes.  
10. Construct a class in the map without passing the logger into `__init__` when the caller has it, or attach that logger through a setter or a module global.  
11. Assign `_PKG_VERSION`, `APP_NAME`, `CONSOLE_NAME`, `PRODUCT_VERBS`, `LIFECYCLE_VERBS`, `AUTHOR_NAME`, `HOMEPAGE`, `LAST_UPDATE`, `DOWNLOAD_URL`, `BASIC_USAGE`, `RATIO_MIN`, or `RATIO_MAX` at module level in `cli.py`. Place them on class `Cli`, or assign them inside `main()`. Do not import those names from the `cli` module into another class.  
12. Add a factory. The site that needs the object writes `ClassName(...)`. A function or a method whose job is to instantiate a class is that factory. The class can be created without one. The wording of the ban stays on `requirement-python-coding-style`.

**Violating this rule is a critical regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | A shared job is one class in its own module |
| AC-2 | `tui.py` defines class `Tui` only, and that class owns the session |
| AC-3 | `MenuPainter` owns the frame glyphs, `paint`, and `format_rows` |
| AC-4 | `MenuModel` and `MenuSession` are their own modules |
| AC-5 | `CheckSystem` owns the host-check set |
| AC-6 | `AboutPage`, `EditWalk`, `Encoder`, `MediaInfo`, `FileStage`, `RunOutput`, `SelfManage`, `SystemLog`, and `LanguageMenu` own their sets |
| AC-7 | `cli.py` defines class `Cli` and `def main`. The console script is `VideoSpeed.cli:main` |
| AC-8 | Menu picture, about lines, encode order, and JSON shape stay on their own requirements |
| AC-9 | Registered in the index |
| AC-10 | Every class in the map, and `MenuScreenError`, accepts the one logger in `__init__` and stores it. `main` passes it into `Cli` |
| AC-11 | The rule 11f names are attributes of class `Cli` or locals inside `main()`. They are not module-level assignments. Other classes receive the values they print |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-python-tui` | Menu picture. `Tui` and `MenuPainter` implement it |
| `requirement-python-cli-language` | Codes, language file, and the words. `LanguageMenu` owns them. `Tui` writes `LanguageMenu(...)` |
| `requirement-python-about` | About lines. `AboutPage` calls `CheckSystem` |
| `requirement-python-coding-style` | One class per file is also a style rule. StateLogic stays aspirational. `shutil.move` stays there |
| `requirement-python-project-structure` | Package directory |
| `requirement-python-cli-interface` | `main` stays in `cli.py` and builds the objects |
| `requirement-python-cli-logging` | The instantiation line. This file owns the `__init__` parameter |
| `requirement-python-interactive-vs-noninteractive` | Question order that `EditWalk` carries |
| `requirement-video-ffmpeg-pipeline` | Encode order. `Encoder` carries it |
| `requirement-python-json-output` | JSON object shape. `RunOutput` writes it |
| `requirement-python-pyenv` | Pyenv root and the three location paths. `CheckSystem` reads them |
| `requirement-python-conda` | Conda root and the three location paths. `CheckSystem` reads them |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| TP-OOP-01 | `tests/test_tui.py` | have | Session methods of `Tui` are not defined in `cli.py`. The painter split is `TP-OOP-03` |
| TP-OOP-02 | `tests/test_about.py` | have | `CheckSystem` owns the host-check set. Those functions are not defined in `cli.py` |
| TP-OOP-03 | `tests/test_tui.py` | have | `paint`, `format_rows`, and the frame glyphs are methods or constants of `MenuPainter`. `MenuModel` and `MenuSession` are their own modules. `tui.py` defines class `Tui` only |
| TP-OOP-04 | `tests/test_cli.py` | have | `cli.py` defines class `Cli` and `def main`. Encoder, file stage, media info, about page, edit walk, and run output are not module-level functions there |
| TP-LOG-05 | `tests/test_logging.py` | have | Constructors in this map accept the logger and store it. The instantiation line is owned by `requirement-python-cli-logging`. This file does not add `TP-OOP-05` |
| TP-STYLE-01 | `tests/test_docs.py` | have | Rule 11f names live on class `Cli`. Owned by `requirement-python-coding-style`. This file does not add `TP-OOP-05` |
| TP-TUI-01..08 | `tests/test_tui.py` | have | Picture stays true. Row **8** opens self-management. The first row keeps the path on the left. The login field on the right is withdrawn |
| TP-TUI-09 · TP-TUI-10 | `tests/test_tui.py` | have | The local clock and the one-second redraw. Owned by `requirement-python-tui` |
| TP-LANG-01 | `tests/test_tui.py` | have | Front **4**, the language file, and the words. Owned by `requirement-python-cli-language`. This file names the class |
| TP-ABOUT-01..08 | `tests/test_about.py` | have | Host-check lines stay true. `TP-ABOUT-08` is `tests/test_tui.py` |
| TP-ABOUT-09 · TP-ABOUT-10 | `tests/test_about.py` | have | Pyenv paths. Owned by `requirement-python-pyenv` |
| TP-ABOUT-11 · TP-ABOUT-12 | `tests/test_about.py` | have | Conda paths. Owned by `requirement-python-conda` |
| TP-ABOUT-13 · TP-ABOUT-14 | `tests/test_about.py` | have | PID, cache chain, persistence, and TTY. Owned by `requirement-python-about` |
| TP-ABOUT-16 | `tests/test_about.py` | have | `in_venv`, `in_pyenv`, and `in_conda`. Owned by `requirement-python-cli-logging` |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-01 | Active 1.0.0 | `Tui` and `CheckSystem`, each in its own file. Use a class when functions share one job |
| 2026-10-01 | Active 1.0.1 | `TP-OOP-01` and `TP-OOP-02` landed. `cli.py` constructs the two classes and does not keep the sets |
| 2026-10-01 | Active 1.1.0 | One class per file. `def main` stays in `cli.py`. Painter, screen types, and the other jobs have their own classes. `TP-OOP-03` and `TP-OOP-04` are todo |
| 2026-10-01 | Active 1.1.1 | `TP-OOP-03` and `TP-OOP-04` have landed. The suite asserts those homes |
| 2026-10-01 | Active 1.2.0 | Every class in the map accepts the one logger in `__init__` and stores it. The instantiation line stays on `requirement-python-cli-logging`. Already on the ship unit (`TP-LOG-05` have) |
| 2026-10-02 | Active 1.2.1 | Class `SelfManage` in `self_management.py` owns the pip lifecycle verbs |
| 2026-10-02 | Active 1.2.2 | The host-check set includes the pyenv reads. The paths stay on `requirement-python-pyenv` |
| 2026-10-02 | Active 1.2.3 | `Cli` names its verb methods. Pip lifecycle verbs stay on `SelfManage`. `Tui` owns `framework_help` and the self-management board. `MenuPainter` owns `SELF_ROWS` |
| 2026-10-02 | Active 1.2.4 | The host-check set includes the conda reads. The paths stay on `requirement-python-conda` |
| 2026-10-02 | Active 1.2.5 | The host-check set includes `PID`, the cache folder chain, persistence storage, and `TTY / Interactive`. The reads stay on `requirement-python-about` |
| 2026-10-02 | Active 1.2.6 | `MenuPainter` owns `path_label` and `path_line`. The path-line picture stays on `requirement-python-tui` |
| 2026-10-02 | Active 1.2.7 | `Cli` does not own the logger construct. `def main` writes `ChronicleLogger(...)` and then `Cli(logger)`. `__init__` writes its own instantiation line |
| 2026-10-02 | Active 1.2.8 | Identity, the formatted version, the verb lists, and the length bounds are attributes of class `Cli`. Other classes receive the values they print. `TP-STYLE-01` have. `./tests/run.sh` on this date: 88 tests, OK, skipped=1 |
| 2026-10-02 | Active 1.2.9 | The site that needs an object writes `ClassName(...)`. A factory is not in the class map. The class can be created without one. The ban stays on `requirement-python-coding-style` |
| 2026-10-02 | Active 1.2.10 | The host-check set includes `in_venv`, `in_pyenv`, and `in_conda`. Those reads stay on `requirement-python-cli-logging`. They do not choose the location lines |
| 2026-10-02 | Active 1.2.11 | `MenuPainter` owns `current_label` and `_login_name`. The right-hand field on the path line stays on `requirement-python-tui` |
| 2026-10-02 | Active 1.2.12 | `MenuPainter` owns `clock_text` instead of `current_label` and `_login_name`. `MenuSession` owns `_wait_key`. The clock picture stays on `requirement-python-tui` |
| 2026-10-02 | Active 1.2.13 | Class `SystemLog` in `system_log.py` owns the log-file list, the read, and the empty. `Tui` owns the system-log screen methods. `MenuPainter` owns `LOG_ROWS`. The picture stays on `requirement-python-tui` |
| 2026-10-02 | Active 1.2.14 | Sample code shows `Cli(logger)` and `Tui(logger)`. `StateLogic` stays unordered |
| 2026-10-04 | Active 1.2.15 | Class `LanguageMenu` in `language_menu.py` owns the codes, the language file, and the words. `Tui` writes `LanguageMenu(...)`. `MenuPainter` owns `LANG_ROWS` and `set_path_label`. `Tui` owns `language_menu_lines`. The picture stays on `requirement-python-tui`. The codes stay on `requirement-python-cli-language` |
| 2026-10-04 | Active 1.2.16 | `Cli` does not own `_verb_hello`. `Tui` does not own `framework_hello` |

---

**Last Updated**: 2026-10-04
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
