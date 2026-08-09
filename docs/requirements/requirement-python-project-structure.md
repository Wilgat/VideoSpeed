**file**: docs/requirements/requirement-python-project-structure.md  
**Status**: Active (Version 1.0.0)  
**Area**: python  
**Key**: `requirement-python-project-structure`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define the **repository layout** and package structure for VideoSpeed as a Python package project: where source, packaging, and requirements law live.

---

## 2. Core Rules (Mandatory)

### 2.1 Source package layout

1. **MUST** keep the installable package under **`src/VideoSpeed/`**.  
2. **MUST** include `__init__.py` (version export), `__main__.py` (module entry), and `cli.py` (CLI + domain session).  
3. **MUST NOT** scatter a second installable package name that contradicts packaging SSOT without an explicit rename plan.

### 2.2 Project root layout

4. **MUST** keep `pyproject.toml` at repository root.  
5. **MUST** keep product user docs at root **`README.md`**.  
6. **MUST** keep specialized product law under **`docs/requirements/`** with `requirement-` prefix and registry `index.md`.  
7. Product design notes **MAY** live under `docs/` (e.g. design specs, changelog) without becoming requirement law unless registered.

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
| `src/VideoSpeed/__init__.py` | `__version__` |
| `src/VideoSpeed/__main__.py` | Module entry |
| `pyproject.toml` | Packaging SSOT |
| `build.sh` | Maintainer build helper |
| `cy-master`, `cy-master.ini` | CyMaster tooling |
| `docs/requirements/` | Product law |
| `docs/CHANGELOG.md` | Product changelog |
| `docs/VideoClip-spec.md` | Design notes (not substitute for requirements) |
| `cli-new.py` | Untracked/extra draft — **not** layout SSOT |
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
| `requirement-python-cli-interface` | Entry modules |
| `requirement-class-software-dev` | Class residual |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| TP-STRUCT-01 | tree review | pass (doc) | Layout matches Implementation Notes |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial project structure law |

---

**Last Updated**: 2026-08-09  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
