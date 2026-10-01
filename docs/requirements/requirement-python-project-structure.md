**file**: docs/requirements/requirement-python-project-structure.md  
**Status**: Active (Version 1.1.4)  
**Area**: python  
**Key**: `requirement-python-project-structure`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define the **repository layout** and package structure for VideoSpeed as a Python package project: where source, packaging, requirements law, and tests live.

### 1.1 Human-facing

**In one sentence:** Installable code lives under `src/VideoSpeed/`; the real CLI is `cli.py`; automated checks live under `tests/`.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Maintainer adding a file | Put product code in `src/VideoSpeed/`, not a second package |
| The other role | Packaging | `pyproject.toml` at repo root |
| Not this file | How to cut video | Domain / pipeline |

| Includes | Excludes |
|----------|----------|
| `src/VideoSpeed/`, `tests/`, root product docs, `docs/requirements/` | Treating `cli.bootstrap-old.py` as ship SSOT |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/VideoSpeed/cli.py` | ship unit | live behavior |
| `tests/run.sh` | suite | Core TP cases |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Find the program | The console script runs `VideoSpeed.cli:main`. | Open `src/VideoSpeed/cli.py` |

---

## 2. Core Rules (Mandatory)

### 2.1 Source package layout

1. **MUST** keep the installable package under **`src/VideoSpeed/`**.  
2. **MUST** include `__init__.py` (version SSOT: `MAJOR_VERSION`, `MINOR_VERSION`, `PATCH_VERSION`, `__version__`), `__main__.py` (module entry), and `cli.py` (CLI + domain session). The text-menu painter today is `menu.py` (`requirement-python-tui`). `requirement-python-oop` names the later files: class `Tui` in `tui.py` and class `CheckSystem` in `check_system.py`. Those two files are required when `TP-OOP-01` and `TP-OOP-02` land. Until then this package does not have to contain them.  
3. **MUST NOT** scatter a second installable package name that contradicts packaging SSOT without an explicit rename plan.

### 2.2 Project root layout

4. **MUST** keep `pyproject.toml` at repository root.  
5. **MUST** keep product user docs at root **`README.md`**.  
6. **MUST** keep specialized product law under **`docs/requirements/`** with `requirement-` prefix and registry `index.md`.  
7. Product design notes **MAY** live under `docs/` (e.g. design specs, changelog) without becoming requirement law unless registered.  
7b. **MUST** keep executable tests under **`tests/`** (runner `tests/run.sh`) — never under `docs/`.

### 2.3 Generated / non-source

8. **MUST NOT** commit `build/` or `dist/` artifacts as product source of truth.  
9. Egg-info / `__pycache__` **MUST** remain ignore-friendly (gitignore).  
10. CyMaster binary/config at root **MAY** exist as maintainer tooling; they **MUST NOT** replace `src/VideoSpeed` as runtime package SSOT.

### 2.4 Requirements surface discipline

11. All product-law files **MUST** use basename prefix `requirement-`.  
12. **MUST** register every Active requirement in `docs/requirements/index.md`.  
13. Product source comments that cite law **MUST** cite live `requirement-*.md` keys only — never templates or skills as behavioral authority.

### 2.5 Implementation Notes (this project)

| Path | Role |
|------|------|
| `src/VideoSpeed/` | Installable package |
| `src/VideoSpeed/cli.py` | Interactive CLI + FFmpeg helpers |
| `src/VideoSpeed/menu.py` | Text-menu painter until `TP-OOP-01` (`requirement-python-tui`) |
| `src/VideoSpeed/tui.py` | Class `Tui` after `TP-OOP-01` (`requirement-python-oop`). Not in the tree yet |
| `src/VideoSpeed/check_system.py` | Class `CheckSystem` after `TP-OOP-02`. Not in the tree yet |
| `src/VideoSpeed/__init__.py` | Version SSOT (`requirement-python-version`) |
| `src/VideoSpeed/__main__.py` | Module entry |
| `pyproject.toml` | Packaging SSOT |
| `build.sh` | Maintainer verbs (`requirement-python-build-script`) |
| `setup.sh` | Local `pyenv shell 3.14` pip install for testing |
| `cy-master`, `cy-master.ini` | CyMaster tooling |
| `docs/requirements/` | Product law |
| `CHANGELOG.md` | Product changelog SSOT |
| `docs/CHANGELOG.md` | Local copy / heritage notes |
| `docs/VideoClip-spec.md` | Design notes (not substitute for requirements) |
| `tests/` | Executable suite (`run.sh`) |
| `cli-new.py` | Extra draft — **not** layout SSOT |
| `README.md` | User documentation |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Layout is explicit.  
- **Principle 5 – SSOT**: One package path, one requirements registry.  
- **Principle 17 – Storage**: Generated dirs not confused with source.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Do not invent parallel packages.  
- **Intentional:** `src/` layout for packaging.  
- **Anti-fragile:** Clear ignore of build debris.  
- **Over-protect:** Requirements registry discipline.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Move the installable package out of `src/VideoSpeed/` without packaging update.  
2. Treat `cli-new.py` as production entry without deliberate migration.  
3. Delete `docs/requirements/index.md` discipline.  
4. Commit secrets under `src/` or `docs/requirements/`.  
5. Cite templates/skills from product source as product law.

**Violating this rule is a critical structure regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Package lives under `src/VideoSpeed/` |
| AC-2 | Root `pyproject.toml` present |
| AC-3 | Requirements under `docs/requirements/` with index |
| AC-4 | Generated build/dist not source SSOT |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-python-packaging` | Manifest |
| `requirement-python-build-script` | `build.sh` verbs |
| `requirement-python-cli-interface` | Entry modules |
| `requirement-class-software-dev` | Class residual |
| `requirement-python-oop` | Later homes for `Tui` and `CheckSystem` |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| TP-STRUCT-01 | `tests/test_docs.py` | have | Ship SSOT is `cli.py` |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial project structure law |
| 2026-08-19 | Active 1.1.0 | tests/ layout; §1.1 |
| 2026-09-30 | Active 1.1.1 | `setup.sh` targets `pyenv shell 3.14` |
| 2026-10-01 | Active 1.1.2 | `menu.py` is the text-menu painter |
| 2026-10-01 | Active 1.1.3 | `build.sh` points at `requirement-python-build-script` |
| 2026-10-01 | Active 1.1.4 | `tui.py` and `check_system.py` are the OOP homes once those moves land. `menu.py` stays the painter until then |

---

**Last Updated**: 2026-10-01  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
