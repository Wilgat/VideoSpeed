**file**: docs/requirements/requirement-python-oop.md
**Status**: Active (Version 1.2.3)
**Area**: python
**Key**: `requirement-python-oop`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define when VideoSpeed uses a class, and name the file that holds each class. One class lives in one module. `def main` stays in `src/VideoSpeed/cli.py`. Every class in the map accepts the one status logger as an `__init__` parameter so that class can log. The line text stays on `requirement-python-cli-logging`.

The menu picture stays on `requirement-python-tui`. The about-page lines stay on `requirement-python-about`. The pyenv root and the python2, python3, and pyenv paths stay on `requirement-python-pyenv`. Encode order stays on `requirement-video-ffmpeg-pipeline`. The JSON object shape stays on `requirement-python-json-output`. This file decides the class and the file. It does not invent a second picture, a second line list, a second encode order, or a second JSON shape.

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
| One class per file; the class is the only public surface of that module | A second class in the same file, or a module-level function beside the class |
| `def main` in `src/VideoSpeed/cli.py` | Moving `main` to another module |
| Ordinary classes named in the map below | One class per function; a StateLogic rewrite |
| The one logger passed into `__init__` | A setter, a module global, or a second logger built inside the class |

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
10. `cli.py` **MUST NOT** define another class's methods. `Cli` owns `build_parser`, `_dispatch`, `_start_logger`, `_verb_help`, `_verb_page`, `_verb_about`, `_verb_hello`, `_verb_edit`, `_verb_list_mp4`, `_unknown_verb`, `stdin_is_tty`, and `stdout_is_tty`. Pip lifecycle verbs stay on `SelfManage`.  
11. `Cli` constructs the other classes and calls them. Each class receives its collaborators through its constructor. A lazy `_host()` import of `cli` is not the end state.

### 2.2a The logger arrives through `__init__`

11a. Every class in the map, and `MenuScreenError`, **MUST** accept the one ChronicleLogger as a parameter of `__init__`.  
11b. `__init__` **MUST** store that object on `self.logger`. A class that constructs another class in the map **MUST** pass that same object into that constructor.  
11c. `main` builds the logger before `Cli` (`requirement-python-cli-logging`) and **MUST** pass it into `Cli`. The parameter **MAY** default to absent so a caller that has no logger can omit it. `main` has the logger and **MUST NOT** omit it.  
11d. **MUST NOT** construct a ChronicleLogger inside a class. **MUST NOT** attach the logger through a setter or a module global after `__init__` returns.  
11e. The instantiation line, its level, and quiet stay on `requirement-python-cli-logging`. This file owns only that the logger arrives through `__init__`.

### 2.3 Text menu

12. `src/VideoSpeed/tui.py` **MUST** define class `Tui` and no other class. `Tui` owns `open_text_menu`, `menu_lines`, `self_menu_lines`, `framework_help`, `framework_hello`, `_boards`, `_edit_in_tui`, `_list_in_tui`, `_open_direct_screen`, `_visible_lines`, `_tui_read`, `_tui_notice`, `_tui_float`, `_tui_yes_no`, and `_tui_index`.  
13. Class `MenuPainter` in `src/VideoSpeed/menu_painter.py` owns `paint`, `paint_prompt`, `format_rows`, `row_parts`, `rows_for`, `screen_can_hold_box`, `_put`, `_paint_box`, `_input_field`, `_status_line`, `_result_overflow`, and `_result_room`. The frame glyphs, `MENU_ROWS`, and `SELF_ROWS` live in that module. `FRAME_TOP_LEFT` **MUST NOT** appear in `cli.py`.  
14. Class `MenuModel` in `src/VideoSpeed/menu_model.py` owns the keystroke state and `edge_keys`.  
15. Class `MenuSession` in `src/VideoSpeed/menu_session.py` owns `run` and raises `MenuScreenError`.  
16. The menu picture (rows, box, hello, about page, fail-closed small screen) stays on `requirement-python-tui`. These classes implement that picture. They do not invent a second layout.  
17. `TP-OOP-01` has landed for the session leaving `cli.py`. `cli.py` **MUST NOT** hold those session functions. `TP-OOP-03` has landed. The proof reads `MenuPainter`, `MenuModel`, and `MenuSession` in their own modules. It **MUST NOT** require `MenuSession` to live in `tui.py`.

### 2.4 Host check and about page

18. Every host-check function **MUST** be a method of class `CheckSystem` in `src/VideoSpeed/check_system.py`.  
19. That set is `check_system_lines`, `parse_sys_version`, `arch_label`, `libc_label`, `binary_type`, `current_user`, `shell_text`, `python_executable_name`, `command_location`, `os_text`, `inside_docker`, `cpython_soabi`, `self_location`, `under_pyenv`, `pyenv_root`, `pyenv_location`, `pyenv_version_names`, `pyenv_interpreter`, and `about_tool_location`.  
20. Class `AboutPage` in `src/VideoSpeed/about_page.py` owns `framework_about`, `about_box_lines`, `install_kind`, `install_sentence`, and `_is_source_checkout`. It **MUST** call `CheckSystem` for the check block and for `self_location`. The line text and the star box stay on `requirement-python-about`. The pyenv root and the python2, python3, and pyenv paths stay on `requirement-python-pyenv`.  
21. `TP-OOP-02` has landed. `cli.py` **MUST NOT** hold the rule 19 functions. `TP-OOP-04` has landed. The about composer is `AboutPage`. `cli.py` **MUST NOT** keep that composer.

### 2.5 The other jobs

22. Class `EditWalk` in `src/VideoSpeed/edit_walk.py` owns the shared question order: folder, file, start, end, percent, boomerang, again. The screen path and the `--json` stderr path both call it. The question text stays on `requirement-python-interactive-vs-noninteractive` and `requirement-python-json-output`.  
23. Class `Encoder` in `src/VideoSpeed/encoder.py` owns `ensure_ffmpeg`, `run_ffmpeg`, `_restore_text_screen`, `cut_clip`, `_atempo_filters`, `speed_change`, `add_boomerang`, `process_job`, `batch_session`, `build_output_name`, `valid_cut_range`, `valid_percent`, and `_length_unchanged`. Cut, speed, and boomerang order stay on `requirement-video-ffmpeg-pipeline`.  
24. Class `MediaInfo` in `src/VideoSpeed/media_info.py` owns `get_mp4_files`, `get_duration_cv2`, and `format_time`.  
25. Class `FileStage` in `src/VideoSpeed/file_stage.py` owns `staging_dir_for`, `make_temp_path`, and `promote_file`. Publish stays `shutil.move` (`requirement-python-coding-style`).  
26. Class `RunOutput` in `src/VideoSpeed/run_output.py` owns `out_info`, `out_err`, the message sink, `_call_sunk`, `_collect_lines`, and the JSON object (`_json_reset`, `_remember`, `_remember_job`, `_emit_json`). The object shape stays on `requirement-python-json-output`.  
26a. Class `SelfManage` in `src/VideoSpeed/self_management.py` owns `local_version`, `argv_for`, `run_text`, `emit`, and `_subprocess_runner`. The verb names and the pip command strings stay on `requirement-python-cli-interface`. `cli.py` **MUST NOT** build those pip argument lists.  
27. Version integers stay on `requirement-python-version` in `src/VideoSpeed/__init__.py`.  
28. `TP-OOP-04` has landed. An edit that touches one of rules 22–26 **MUST** keep that class's whole set on its class. **MUST NOT** leave the set as module-level functions in `cli.py`.

### 2.6 Implementation Notes (this project)

| Class | File | Owns |
|-------|------|------|
| `Tui` | `src/VideoSpeed/tui.py` | Text-menu session (rule 12) |
| `MenuPainter` | `src/VideoSpeed/menu_painter.py` | Frame, `MENU_ROWS`, `paint`, `format_rows` |
| `MenuModel` | `src/VideoSpeed/menu_model.py` | Keystroke state, `edge_keys` |
| `MenuSession` | `src/VideoSpeed/menu_session.py` | `run`. Raises `MenuScreenError` |
| `CheckSystem` | `src/VideoSpeed/check_system.py` | Host-check set (rule 19) |
| `AboutPage` | `src/VideoSpeed/about_page.py` | About composer. Calls `CheckSystem` |
| `EditWalk` | `src/VideoSpeed/edit_walk.py` | Folder, file, start, end, percent, boomerang, again |
| `Encoder` | `src/VideoSpeed/encoder.py` | Cut, speed, boomerang, `process_job` |
| `MediaInfo` | `src/VideoSpeed/media_info.py` | MP4 list, duration, `format_time` |
| `FileStage` | `src/VideoSpeed/file_stage.py` | Staging and `promote_file` |
| `RunOutput` | `src/VideoSpeed/run_output.py` | Info, error, and the JSON object |
| `SelfManage` | `src/VideoSpeed/self_management.py` | Local version and the pip commands for `version-check`, `self-update`, `self-install`, and `self-uninstall` |
| `Cli` | `src/VideoSpeed/cli.py` | Parser, dispatch, verbs, tty checks. `def main` stays in this file |

| Item | Value |
|------|--------|
| **Console script** | `video-speed = "VideoSpeed.cli:main"` |
| **Module entry** | `src/VideoSpeed/__main__.py` imports `main` from `.cli` |
| **Landed** | `TP-OOP-01` session left `cli.py`. `TP-OOP-02` host check is `CheckSystem`. `TP-OOP-03` painter and screen types left `tui.py`. `TP-OOP-04` the other jobs left `cli.py` |
| **Logger** | Every class `__init__` in the map accepts `logger` and stores it. `main` passes the one ChronicleLogger into `Cli`. Collaborators receive that same object. Already on the ship unit. The instantiation line is `requirement-python-cli-logging` (`TP-LOG-05` have) |
| **Not this split** | Menu rows, about line text, encode order, JSON object shape, version integers, the wording of the instantiation line |

### 2.7 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Each job has one class and one file. That class receives the logger in `__init__`.  
- **Principle 5 – SSOT**: `cli.py` does not keep a second copy of another class's methods. `main` has one home.  
- **Principle 1 – Caution**: The picture, the lines, the encode order, and the JSON shape stay where they already work.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, each class still receives the logger through `__init__` at this login. **This requirement:** do not use admin privilege, `sudo`, or a system package manager to construct a class or to pass the logger.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Move a whole named set together. A half-move leaves two homes.  
- **Intentional:** The map above is the class list. `main` stays in `cli.py`.  
- **Anti-fragile:** Picture, lines, encode order, and JSON shape keep their own requirements.  
- **Over-protect:** Do not flatten a class back into module functions. Do not put a second class in its file. Do not build the logger inside the class.

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
| AC-6 | `AboutPage`, `EditWalk`, `Encoder`, `MediaInfo`, `FileStage`, and `RunOutput` own their sets |
| AC-7 | `cli.py` defines class `Cli` and `def main`. The console script is `VideoSpeed.cli:main` |
| AC-8 | Menu picture, about lines, encode order, and JSON shape stay on their own requirements |
| AC-9 | Registered in the index |
| AC-10 | Every class in the map, and `MenuScreenError`, accepts the one logger in `__init__` and stores it. `main` passes it into `Cli` |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-python-tui` | Menu picture. `Tui` and `MenuPainter` implement it |
| `requirement-python-about` | About lines. `AboutPage` calls `CheckSystem` |
| `requirement-python-coding-style` | One class per file is also a style rule. StateLogic stays aspirational. `shutil.move` stays there |
| `requirement-python-project-structure` | Package directory |
| `requirement-python-cli-interface` | `main` stays in `cli.py` and builds the objects |
| `requirement-python-cli-logging` | The instantiation line. This file owns the `__init__` parameter |
| `requirement-python-interactive-vs-noninteractive` | Question order that `EditWalk` carries |
| `requirement-video-ffmpeg-pipeline` | Encode order. `Encoder` carries it |
| `requirement-python-json-output` | JSON object shape. `RunOutput` writes it |
| `requirement-python-pyenv` | Pyenv root and the three location paths. `CheckSystem` reads them |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| TP-OOP-01 | `tests/test_tui.py` | have | Session methods of `Tui` are not defined in `cli.py`. The painter split is `TP-OOP-03` |
| TP-OOP-02 | `tests/test_about.py` | have | `CheckSystem` owns the host-check set. Those functions are not defined in `cli.py` |
| TP-OOP-03 | `tests/test_tui.py` | have | `paint`, `format_rows`, and the frame glyphs are methods or constants of `MenuPainter`. `MenuModel` and `MenuSession` are their own modules. `tui.py` defines class `Tui` only |
| TP-OOP-04 | `tests/test_cli.py` | have | `cli.py` defines class `Cli` and `def main`. Encoder, file stage, media info, about page, edit walk, and run output are not module-level functions there |
| TP-LOG-05 | `tests/test_logging.py` | have | Constructors in this map accept the logger and store it. The instantiation line is owned by `requirement-python-cli-logging`. This file does not add `TP-OOP-05` |
| TP-TUI-01..06 | `tests/test_tui.py` | have | Picture stays true. Row **8** opens self-management |
| TP-ABOUT-01..08 | `tests/test_about.py` | have | Host-check lines stay true. `TP-ABOUT-08` is `tests/test_tui.py` |
| TP-ABOUT-09 · TP-ABOUT-10 | `tests/test_about.py` | have | Pyenv paths. Owned by `requirement-python-pyenv` |

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

---

**Last Updated**: 2026-10-02
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
