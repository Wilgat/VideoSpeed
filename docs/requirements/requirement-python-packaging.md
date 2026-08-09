**file**: docs/requirements/requirement-python-packaging.md  
**Status**: Active (Version 1.0.0)  
**Area**: python  
**Key**: `requirement-python-packaging`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define packaging SSOT for the VideoSpeed Python distribution: **`pyproject.toml`**, metadata, dependencies, console entry points, and version consistency.

---

## 2. Core Rules (Mandatory)

### 2.1 Manifest SSOT

1. **`pyproject.toml` MUST** be the primary packaging manifest (PEP 517 / PEP 621).  
2. **MUST** declare: name, version, description, authors, license text, requires-python, dependencies, build-system, and console scripts.  
3. **MUST NOT** treat an ad-hoc `requirements.txt` as the primary product dependency SSOT.  
4. Legacy `setup.py` under build trees **MUST NOT** become a second source of runtime identity without deprecation plan.

### 2.2 Version SSOT

5. Package version in **`pyproject.toml`** and **`src/VideoSpeed/__init__.__version__`** **MUST** match when a release is claimed.  
6. Bumping either **MUST** update both in the same change (or automated single writer documented later).  
7. **MUST NOT** invent a third silent version constant without declaring the new SSOT.

### 2.3 Dependencies

8. **MUST** declare runtime Python dependencies required for the shipped CLI.  
9. System tools (FFmpeg) **MUST NOT** be faked as pip packages — document under runtime prerequisites.  
10. **MUST NOT** commit real secrets or private index passwords into packaging files.

### 2.4 Entry points

11. **MUST** declare console script **`video-speed`** → `VideoSpeed.cli:main`.  
12. Entry function **MUST** remain a thin launch into product logic (interactive session today).

### 2.5 Build / release helpers

13. Optional `build.sh` / CyMaster tooling **MAY** exist for maintainer packaging.  
14. **MUST** keep helper scripts consistent with `pyproject.toml` identity (project name VideoSpeed).  
15. Generated `build/` and `dist/` **MUST NOT** be treated as source SSOT.

### 2.6 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Manifest** | `pyproject.toml` |
| **Project name** | `VideoSpeed` |
| **Version** | `1.0.5` |
| **requires-python** | `>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*` (as declared — re-verify support claims before marketing) |
| **Dependencies** | `ChronicleLogger>=1.2.3`, `opencv-python` |
| **Build backend** | `setuptools.build_meta` |
| **Console script** | `video-speed = VideoSpeed.cli:main` |
| **Homepage / repo** | `https://github.com/Wilgat/VideoSpeed` |
| **Maintainer build helper** | `build.sh` |
| **CyMaster config** | `cy-master.ini` (`targetName = VideoSpeed`, `srcFolder = src`) |
| **License** | MIT (packaging claims MIT; ensure root LICENSE file present when publishing) |

### 2.7 Why This Requirement Exists (CIAO)

- **Principle 5 – SSOT**: One manifest for identity and entry.  
- **Principle 2 – Intentional**: Version dual-write is explicit.  
- **Principle 1 – Caution**: System FFmpeg not mis-declared as pip-only.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Validate version dual SSOT on release.  
- **Intentional:** PEP 621 over ad-hoc manifests.  
- **Anti-fragile:** Console script + module entry.  
- **Over-protect:** No secrets in packaging files.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Remove or rename `video-speed` entry without CLI + README update.  
2. Let `__version__` and `pyproject.toml` diverge while claiming a release.  
3. Add private credentials to `pyproject.toml`.  
4. Replace packaging SSOT with only `requirements.txt`.  
5. Change product name silently across packaging and source package directory.

**Violating this rule is a critical packaging regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | `pyproject.toml` present with name VideoSpeed |
| AC-2 | Console script `video-speed` declared |
| AC-3 | Dependencies include opencv-python |
| AC-4 | Version matches `__init__.py` when release claimed |
| AC-5 | FFmpeg documented as external, not pip-only |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-python-cli-interface` | Entry behavior |
| `requirement-python-project-structure` | Package layout |
| `requirement-runtime-prerequisites` | FFmpeg external |
| `requirement-class-software-dev` | Stack residual |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| TP-PKG-01 | `pip install -e .` smoke | todo | Entry imports |
| TP-PKG-02 | version equality check | todo | pyproject vs `__version__` |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial packaging law |

---

**Last Updated**: 2026-08-09  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
