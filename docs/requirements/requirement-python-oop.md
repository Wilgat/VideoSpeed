**file**: docs/requirements/requirement-python-oop.md
**Status**: Active (Version 1.0.0)
**Area**: python
**Key**: `requirement-python-oop`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define when VideoSpeed uses a class, and name the two groups that must be classes in their own files: the text menu, and the host check.

The picture of the menu stays on `requirement-python-tui`. The about-page lines stay on `requirement-python-about`. Encode order stays on `requirement-video-ffmpeg-pipeline`. This file decides the type and the file, not the screen layout and not the line text.

### 1.1 Human-facing

**In one sentence:** Related functions share one class in one file: the text menu is class `Tui` in `tui.py`, and the host check is class `CheckSystem` in `check_system.py`.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Maintainer adding a screen prompt or a host-check read | Put it on `Tui` or `CheckSystem` |
| The other role | The menu picture and the about lines | `requirement-python-tui`, `requirement-python-about` |
| Not this file | Cut, speed, and boomerang order | `requirement-video-ffmpeg-pipeline` |

| Includes | Excludes |
|----------|----------|
| Use a class when a set of functions shares one job | One class per function |
| `Tui` in `src/VideoSpeed/tui.py` | A second frame painter in `cli.py` |
| `CheckSystem` in `src/VideoSpeed/check_system.py` | A StateLogic rewrite of the encoder |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/VideoSpeed/tui.py` | class `Tui` | Menu, prompts, and the frame |
| `src/VideoSpeed/check_system.py` | class `CheckSystem` | `[CHECK SYSTEM]` reads |
| `src/VideoSpeed/cli.py` | `main` | Builds those objects and runs a job |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Add a menu prompt | It is a method on `Tui`. The frame glyphs stay in `tui.py`. | Edit `src/VideoSpeed/tui.py` |
| Add a host-check field | It is a method on `CheckSystem`. The about page calls that object for the check block. | Edit `src/VideoSpeed/check_system.py` |

---

## 2. Core Rules (Mandatory)

### 2.1 Use a class when the functions share one job

1. When a set of functions shares one job, product Python **SHOULD** make them methods of one class and put that class in its own module.  
2. **MUST NOT** make a class whose only method is a single function that nothing else in the file shares.  
3. **MUST NOT** leave a new cluster of related functions as module-level defs in `cli.py` when rule 1 applies.  
4. A full StateLogic + `Attr` rewrite of the encoder and of `main` stays aspirational (`requirement-python-coding-style`). This file does not order that rewrite. `Tui` and `CheckSystem` are ordinary classes.

### 2.2 Text menu: class `Tui`

5. Every text-menu function **MUST** be a method of class `Tui` in `src/VideoSpeed/tui.py`.  
6. That set is the session and the painter: `open_text_menu`, `menu_lines`, `_edit_in_tui`, `_visible_lines`, `_paint_prompt`, `_tui_read`, `_tui_notice`, `_tui_float`, `_tui_yes_no`, `_tui_index`, `framework_hello`, and the painter now in `src/VideoSpeed/menu.py` (`MenuSession`, `paint`, `format_rows`, and the frame glyphs). A screen-model type **MAY** stay a second class in `tui.py` when `Tui` uses it. It **MUST NOT** live in `cli.py`.  
7. `cli.py` **MUST** construct `Tui` and call it. `cli.py` **MUST NOT** define those functions and **MUST NOT** contain `FRAME_TOP_LEFT`.  
8. The menu picture (rows, box, hello, about page, fail-closed small screen) stays on `requirement-python-tui`. `Tui` implements that picture. It does not invent a second layout.  
9. Until `src/VideoSpeed/tui.py` exists, `menu.py` remains the painter and `cli.py` may still hold the session functions. The move is `TP-OOP-01`. A later edit that touches one of those functions **MUST** complete the move of that whole set in the same change.

### 2.3 Host check: class `CheckSystem`

10. Every host-check function **MUST** be a method of class `CheckSystem` in `src/VideoSpeed/check_system.py`.  
11. That set is `check_system_lines`, `parse_sys_version`, `arch_label`, `libc_label`, `binary_type`, `current_user`, `shell_text`, `python_executable_name`, `command_location`, `os_text`, `inside_docker`, `cpython_soabi`, and `self_location`.  
12. The about page **MUST** call `CheckSystem` for the `[CHECK SYSTEM]` block. The line text and the star box stay on `requirement-python-about`. `about_box_lines` and `framework_about` stay the about composer. They **MUST** call `CheckSystem` for the check block and for `self_location`.  
13. `cli.py` **MUST NOT** define the functions in rule 11 after the move.  
14. Until `src/VideoSpeed/check_system.py` exists, `cli.py` may still hold those functions. The move is `TP-OOP-02`. A later edit that touches one of them **MUST** complete the move of that whole set in the same change.

### 2.4 What stays put

15. FFmpeg cut, speed, and boomerang stay in the module `requirement-video-ffmpeg-pipeline` names. This file does not move them.  
16. `--json` assembly stays on `requirement-python-json-output`.  
17. Version integers stay on `requirement-python-version` in `src/VideoSpeed/__init__.py`.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **TUI class** | `Tui` |
| **TUI file** | `src/VideoSpeed/tui.py` |
| **Painter today** | `src/VideoSpeed/menu.py` until `TP-OOP-01` |
| **Session today** | `open_text_menu`, `_edit_in_tui`, `_tui_*`, `_paint_prompt`, `_visible_lines`, `menu_lines`, `framework_hello` in `src/VideoSpeed/cli.py` |
| **Check class** | `CheckSystem` |
| **Check file** | `src/VideoSpeed/check_system.py` |
| **Check today** | The rule 11 functions in `src/VideoSpeed/cli.py` |
| **About composer** | `framework_about`, `about_box_lines` stay the page body and call `CheckSystem` |
| **Not this split** | `cut_clip`, `speed_change`, `add_boomerang`, `process_job` |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: The menu is one type. The host check is another type.  
- **Principle 5 – SSOT**: One file owns each group, so `cli.py` does not grow a second copy.  
- **Principle 1 – Caution**: The move is two named sets. The encoder is left where it works.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Move a whole named set together. A half-move leaves two homes.  
- **Intentional:** `Tui` and `CheckSystem` are the two ordered classes.  
- **Anti-fragile:** The menu picture and the about lines keep their own requirements.  
- **Over-protect:** Do not flatten `Tui` back into module functions in `cli.py`.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Add a new text-menu function as a module-level def in `cli.py`.  
2. Add a new host-check read as a module-level def in `cli.py`.  
3. Copy `FRAME_TOP_LEFT` into `cli.py`.  
4. Split `Tui` or `CheckSystem` across two modules.  
5. Rewrite `cut_clip`, `speed_change`, or `add_boomerang` into StateLogic because this file exists.  
6. Change the about line list or the menu rows in this file.

**Violating this rule is a critical regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | A shared job is a class in its own module when that grouping is possible |
| AC-2 | Class `Tui` in `src/VideoSpeed/tui.py` owns the text-menu session and the painter |
| AC-3 | Class `CheckSystem` in `src/VideoSpeed/check_system.py` owns the host-check functions |
| AC-4 | `cli.py` calls those classes and does not keep a second copy of the sets |
| AC-5 | Menu picture and about line text stay on their own requirements |
| AC-6 | Registered in the index |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-python-tui` | Menu picture. `Tui` implements it |
| `requirement-python-about` | About lines. `CheckSystem` fills the host check |
| `requirement-python-coding-style` | StateLogic stays aspirational outside these two classes |
| `requirement-python-project-structure` | Package directory |
| `requirement-python-cli-interface` | `main` builds the objects |
| `requirement-video-ffmpeg-pipeline` | Encode stays put |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| TP-OOP-01 | `tests/test_tui.py` | todo | `Tui` in `tui.py`; session and painter not defined in `cli.py` |
| TP-OOP-02 | `tests/test_about.py` | todo | `CheckSystem` in `check_system.py`; rule 11 functions not defined in `cli.py` |
| TP-TUI-01..05 | `tests/test_tui.py` | have | Picture stays true after the move |
| TP-ABOUT-01..08 | `tests/test_about.py` | have | Host-check lines stay true after the move |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-01 | Active 1.0.0 | `Tui` and `CheckSystem`, each in its own file. Use a class when functions share one job |

---

**Last Updated**: 2026-10-01
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
