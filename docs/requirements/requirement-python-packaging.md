**file**: docs/requirements/requirement-python-packaging.md  
**Status**: Active (Version 1.1.10)  
**Area**: python  
**Key**: `requirement-python-packaging`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define packaging SSOT for the VideoSpeed Python distribution: **`pyproject.toml`**, metadata, dependencies, console entry points, and version consistency.

### 1.1 Human-facing

**In one sentence:** This file says how VideoSpeed is packaged: `pyproject.toml` holds the name, version, pip dependencies, and the `video-speed` command.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Maintainer cutting a release | Bump `MAJOR_VERSION`, `MINOR_VERSION`, and `PATCH_VERSION` in `__init__.py`, and keep the manifest equal |
| The other role | CLI / structure peers | How the command behaves after install |
| Not this file | FFmpeg on PATH | Runtime prerequisites |

| Includes | Excludes |
|----------|----------|
| Manifest, version dual-write, console script, pip deps | System FFmpeg; how status lines are written |

| Surface | What you open | What for |
|---------|---------------|----------|
| `pyproject.toml` | manifest | name, version, deps, entry |
| `src/VideoSpeed/__init__.py` | version SSOT | `MAJOR_VERSION`, `MINOR_VERSION`, `PATCH_VERSION`, `__version__` |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Install from checkout | Pip reads this manifest and creates `video-speed`. | `pip install -e .` |

---

## 2. Core Rules (Mandatory)

### 2.1 Manifest SSOT

1. **`pyproject.toml` MUST** be the primary packaging manifest (PEP 517 / PEP 621).  
2. **MUST** declare: name, version, description, authors, license text, requires-python, dependencies, build-system, and console scripts.  
3. **MUST NOT** treat an ad-hoc `requirements.txt` as the primary product dependency SSOT.  
4. Legacy `setup.py` under build trees **MUST NOT** become a second source of runtime identity without deprecation plan.

### 2.2 Version SSOT

5. The three integers and `__version__` are owned by `requirement-python-version`. This file does not keep a second definition.  
6. `pyproject.toml` `[project].version` **MUST** equal `__version__` when a release is claimed.  
7. Bumping the integers **MUST** update that manifest field in the same change.  
7b. **MUST NOT** put `MAJOR_VERSION`, `MINOR_VERSION`, or `PATCH_VERSION` in `cli.py`.

### 2.3 Dependencies

8. **MUST** declare runtime Python dependencies required for the shipped CLI.  
9. System tools (FFmpeg) **MUST NOT** be faked as pip packages — document under runtime prerequisites.  
10. **MUST NOT** commit real secrets or private index passwords into packaging files.

### 2.4 Entry points

11. **MUST** declare console script **`video-speed`** → `VideoSpeed.cli:main`.  
12. Entry function **MUST** remain a thin launch into product logic (interactive session today).

### 2.5 Build / release helpers

13. Maintainer verbs on `build.sh` **MUST** follow `requirement-python-build-script`. This file **MUST NOT** keep a second verb procedure. CyMaster tooling **MAY** remain beside that script.  
14. **MUST** keep helper scripts consistent with `pyproject.toml` identity (project name VideoSpeed).  
15. Generated `build/` and `dist/` **MUST NOT** be treated as source SSOT.

### 2.6 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Manifest** | `pyproject.toml` |
| **Project name** | `VideoSpeed` |
| **Version** | `1.0.11` from `MAJOR_VERSION=1`, `MINOR_VERSION=0`, `PATCH_VERSION=11` (`requirement-python-version`) |
| **requires-python** | `>=3.11` (`tomllib` in the suite; the text menu uses 3.11 typing) |
| **Dependencies** | Version floors owned by `requirement-python-dependency-management`: `opencv-python-headless>=5.0.0.93`, `ChronicleLogger>=1.3.1` |
| **Build backend** | `setuptools.build_meta` |
| **Console script** | `video-speed = VideoSpeed.cli:main` |
| **Homepage / repo** | `https://github.com/Wilgat/VideoSpeed` |
| **Maintainer build helper** | `build.sh` (`requirement-python-build-script`) |
| **Local pyenv reinstall** | `setup.sh` at the checkout root. It runs `pyenv shell 3.14` and runs pip into that interpreter. The program does not call it |
| **CyMaster config** | `cy-master.ini` (`targetName = VideoSpeed`, `srcFolder = src`) |
| **License** | MIT (packaging claims MIT; ensure root LICENSE file present when publishing) |

### 2.7 Why This Requirement Exists (CIAO)

- **Principle 5 – SSOT**: One manifest for identity and entry.  
- **Principle 2 – Intentional**: Version dual-write is explicit.  
- **Principle 1 – Caution**: System FFmpeg not mis-declared as pip-only.

---

## Sample code

```toml
[project]
name = "VideoSpeed"
version = "1.0.11"

[project.scripts]
video-speed = "VideoSpeed.cli:main"
```

The version string is the package `__version__` from `requirement-python-version`. `cli.py` does not declare a second triple.

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
| AC-3 | Dependencies match `requirement-python-dependency-management` |
| AC-4 | Version matches `__init__.py` when release claimed |
| AC-5 | FFmpeg documented as external, not pip-only |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-python-cli-interface` | Entry behavior |
| `requirement-python-project-structure` | Package layout |
| `requirement-runtime-prerequisites` | FFmpeg external |
| `requirement-python-tui` | Declared menu package draws the text screen |
| `requirement-python-dependency-management` | Pip names and version floors |
| `requirement-python-version` | Version integer SSOT |
| `requirement-python-build-script` | `./build.sh` verbs |
| `requirement-python-cli-logging` | How the ChronicleLogger floor is used |
| `requirement-class-software-dev` | Stack residual |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| TP-PKG-01 | `tests/test_package.py` | have | import without cv2 |
| TP-PKG-02 | `tests/test_package.py` | have | version equality |
| TP-PKG-03 | `tests/test_package.py` | have | console script |
| TP-PKG-04 | `tests/test_package.py` | have | py_compile |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial packaging law |
| 2026-08-19 | Active 1.1.0 | Drop ChronicleLogger; 1.0.6; §1.1 |
| 2026-09-30 | Active 1.1.1 | Menu package peer is `requirement-python-tui` |
| 2026-09-30 | Active 1.1.2 | `setup.sh` installs with `pyenv shell 3.14` |
| 2026-09-30 | Active 1.1.3 | Declared OpenCV dep is `opencv-python-headless` |
| 2026-09-30 | Active 1.1.4 | Version floors owned by `requirement-python-dependency-management` |
| 2026-10-01 | Active 1.1.5 | Manifest includes `ChronicleLogger>=1.3.1` |
| 2026-10-01 | Active 1.1.6 | Version integers owned by `requirement-python-version` |
| 2026-10-01 | Active 1.1.7 | No menu wheel; painter is `src/VideoSpeed/menu.py` |
| 2026-10-01 | Active 1.1.8 | `build.sh` verbs owned by `requirement-python-build-script` |
| 2026-10-02 | Active 1.1.9 | Sample code shows the manifest name, version `1.0.10`, and `video-speed = VideoSpeed.cli:main` |
| 2026-10-04 | Active 1.1.10 | Version row and sample are package string `1.0.11` |

---

**Last Updated**: 2026-10-04  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
