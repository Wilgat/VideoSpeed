**file**: docs/requirements/requirement-python-dependency-management.md  
**Status**: Active (Version 1.2.2)  
**Area**: python  
**Key**: `requirement-python-dependency-management`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file owns the **pip requirement strings** VideoSpeed declares. The machine copy is `pyproject.toml` `[project].dependencies`. Two libraries have floors: the headless OpenCV wheel used to read clip length, and ChronicleLogger for system-status files. The text menu is drawn by this package (`requirement-python-tui`), so it is not a pip wheel. Packaging law owns the manifest shape. Runtime-prerequisite law owns the system `ffmpeg` program. How status lines are written is `requirement-python-cli-logging`. This file owns the names and version floors.

### 1.1 Human-facing

**In one sentence:** Before a duration probe or a status log can run, the interpreter must have OpenCV headless at least 5.0.0.93 and ChronicleLogger at least 1.3.1, as written in `pyproject.toml`. The text menu does not add a pip wheel.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Install the declared wheels with pip | `pip install 'opencv-python-headless>=5.0.0.93'` |
| The other role | The manifest that lists those strings | `pyproject.toml` |
| Not this file | The system encode program | `ffmpeg` on `PATH` |

| Includes | Excludes |
|----------|----------|
| Version floors for the vision wheel and ChronicleLogger | Installing operating-system packages, and a pip wheel for the text menu |
| One list shared by the manifest and this file | A second `requirements.txt` authority |

| Surface | What you open | What for |
|---------|---------------|----------|
| `pyproject.toml` | `[project].dependencies` | The live strings |
| `video-speed` | console script | Uses those libraries after install |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Install the vision wheel | Duration probing imports `cv2` from the headless build, which does not need `libGL.so.1`. | `pip install 'opencv-python-headless>=5.0.0.93'` |
| Install the status logger | System-status files use ChronicleLogger 1.3.1 or newer. | `pip install 'ChronicleLogger>=1.3.1'` |

## 2. Core Rules (Mandatory)

1. **MUST** declare runtime pip libraries only in `pyproject.toml` `[project].dependencies`.  
2. **MUST** attach a PEP 440 version specifier to every entry. A bare name is not a declaration.  
3. **MUST** keep the strings in Implementation Notes identical to that list.  
4. **MUST** use the headless OpenCV wheel for the duration probe. **MUST NOT** declare the GUI wheel `opencv-python`.  
5. **MUST NOT** declare a menu distribution. The text menu is painted by this package (`requirement-python-tui`, class `MenuPainter`; session is class `Tui`; `requirement-python-oop`).  
6. **MUST** keep the status-log floor at ChronicleLogger 1.3.1, the release `requirement-python-cli-logging` consumes.  
7. **MUST NOT** install operating-system packages, and **MUST NOT** use admin privilege, to satisfy these strings.  
8. **MUST NOT** add `requirements.txt` as a second authority.

### 2.1 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| **Vision spec** | `opencv-python-headless>=5.0.0.93` |
| **Status-log spec** | `ChronicleLogger>=1.3.1` |
| **Menu distribution** | Not declared. Painter is class `MenuPainter`. Session is class `Tui` (`requirement-python-oop`) |
| **GUI build forbidden** | `opencv-python` is not declared |
| **Manifest** | `pyproject.toml` `[project].dependencies` |
| **Why this OpenCV floor** | 5.0.0.93 is the headless wheel verified to import `cv2` and expose `VideoCapture` without `libGL.so.1` |
| **Why this logger floor** | 1.3.1 is the ChronicleLogger release whose `logname`, `logName`, `baseDir`, `isDebug`, and `log_message` match `requirement-python-cli-logging` |
| **Install helper** | `setup.sh` installs `opencv-python-headless>=5.0.0.93` and `ChronicleLogger>=1.3.1` into the pyenv 3.14 interpreter and removes `opencv-python` when that GUI wheel is present. It does not install OS packages |

### 2.2 Why This Requirement Exists (CIAO)

- **Principle 5 – SSOT**: One manifest and one law file for the pip strings.  
- **Principle 2 – Intentional**: The vision floor is chosen, and the text menu is not a pip wheel.  
- **Principle 1 – Caution**: An unpinned OpenCV wheel is how a GUI build that needs `libGL.so.1` gets installed.  
- **Principle 10 – Least privilege**: pip as this login; no root package install.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, these wheels stay a normal-user pip install. **This requirement:** do not satisfy `opencv-python-headless>=5.0.0.93` or `ChronicleLogger>=1.3.1` with admin privilege, a system package manager, or `sudo pip`.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Pin the vision wheel that imports on a machine without GL.  
- **Intentional:** The text menu stays in this package.  
- **Anti-fragile:** Headless OpenCV does not depend on `libGL.so.1`.  
- **Over-protect:** Tests read the manifest and the strings in this file.

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Drop the version specifier from either dependency.  
2. Replace `opencv-python-headless` with `opencv-python` while the program only uses `VideoCapture`.  
3. Add a menu distribution while the painter is class `MenuPainter` in this package.  
4. Lower the ChronicleLogger floor below 1.3.1 while status lines use `log_message`.  
5. Add a root installer for these libraries.  
6. Leave this file’s strings different from `pyproject.toml`.

**Violating this rule is a dependency-honesty regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | `opencv-python-headless>=5.0.0.93` is a dependency |
| AC-2 | No menu distribution is declared |
| AC-3 | `ChronicleLogger>=1.3.1` is a dependency |
| AC-4 | No dependency entry lacks a version specifier |
| AC-5 | `opencv-python` is not a dependency |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `docs/requirements/index.md` | Registry |
| `requirement-python-packaging` | Manifest shape; points here for floors |
| `requirement-runtime-prerequisites` | System `ffmpeg`; pip strings point here |
| `requirement-python-tui` | Menu writer in this package; no menu wheel here |
| `requirement-python-cli-logging` | Status logger that needs the ChronicleLogger floor |
| `requirement-class-software-dev` | Residual points here |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| TP-DEP-01 | `tests/test_dependencies.py` | have | Vision and logger specs; every entry versioned |
| TP-DEP-02 | `tests/test_dependencies.py` | have | Headless wheel; GUI wheel absent |
| TP-DEP-03 | `tests/test_dependencies.py` | have | This file matches the manifest |
| TP-DEP-04 | `tests/test_dependencies.py` | have | Installed wheels meet the floors when present |

**Matrix:** `reviews/requirement-test-matrix.md`  
**Map:** `reviews/test-plan.md`

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-09-30 | Active 1.0.0 | Vision and menu pip floors |
| 2026-10-01 | Active 1.1.0 | Add `ChronicleLogger>=1.3.1` |
| 2026-10-01 | Active 1.2.0 | Menu wheel removed; painter is `src/VideoSpeed/menu.py` |
| 2026-10-01 | Active 1.2.1 | Painter is class `Tui` in `src/VideoSpeed/tui.py`. Still no menu wheel |
| 2026-10-01 | Active 1.2.2 | Painter is class `MenuPainter`. Still no menu wheel. `TP-OOP-03` is todo |

---

**Last Updated**: 2026-10-01  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
