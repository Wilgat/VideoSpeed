**file**: docs/requirements/requirement-runtime-prerequisites.md  
**Status**: Active (Version 1.1.7)  
**Area**: runtime  
**Key**: `requirement-runtime-prerequisites`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Declare **host and Python runtime prerequisites** required to run VideoSpeed successfully. This product does **not** implement a privileged system `prerequisites` installer command; this file is the **documentation and validation SSOT** for what must already be present.

### 1.1 Human-facing

**In one sentence:** Before VideoSpeed can encode, your computer must already have Python 3.11 or newer, the pip wheels named by `requirement-python-dependency-management` (`opencv-python-headless>=5.0.0.93`, `ChronicleLogger>=1.3.1`), and an `ffmpeg` program on `PATH`. The text menu is in this package.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Operator installing tools | `ffmpeg -version` must work |
| The other role | Packaging (pip deps) | version floors in `requirement-python-dependency-management` |
| Not this file | How to cut | Pipeline file |

| Includes | Excludes |
|----------|----------|
| CPython 3.11+, OpenCV, FFmpeg; no root installer | pip installing FFmpeg |

| Surface | What you open | What for |
|---------|---------------|----------|
| `ffmpeg` on `PATH` | system binary | encode |
| `video-speed --version` | command | package import without FFmpeg |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Check FFmpeg | The product will not install it for you. | `ffmpeg -version` |

---

## 2. Core Rules (Mandatory)

### 2.1 Scope (honest product mode)

1. **MUST** document all external tools required at runtime.  
2. **MUST NOT** claim the product auto-installs system packages via root/sudo unless a future Active elev + install requirement is added.  
3. **MUST** separate **pip-installable** Python deps from **system binaries**.

### 2.2 Required runtime components

| Component | Kind | Required for | Install surface |
|-----------|------|--------------|-----------------|
| CPython | interpreter | package import + CLI | OS / pyenv / system Python |
| `opencv-python-headless>=5.0.0.93` | pip package | duration probe | `requirement-python-dependency-management` |
| `ChronicleLogger>=1.3.1` | pip package | system-status files (`requirement-python-cli-logging`) | `requirement-python-dependency-management` |
| **FFmpeg** (`ffmpeg` on PATH) | system binary | cut / speed / boomerang | OS package manager / user install |

### 2.3 Validation expectations

4. **SHOULD** fail with an actionable message when `ffmpeg` is missing (not a cryptic stack only).  
5. **MUST** document OpenCV as required for duration probing.  
6. **MUST** document that only MP4 inputs are first-class today.

### 2.4 Privilege

7. **MUST NOT** require root to satisfy runtime prerequisites for normal use.  
8. Type 1 elevation for package install is **out of scope** for this product.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Python package install** | `pip install .` or wheel from `dist/` / PyPI when published |
| **Declared pip deps** | Owned by `requirement-python-dependency-management`: `opencv-python-headless>=5.0.0.93`, `ChronicleLogger>=1.3.1` |
| **Text menu** | In this package (`requirement-python-tui`, class `Tui` and class `MenuPainter`). Not a pip package |
| **System binary** | `ffmpeg` on `PATH` |
| **Auto install command** | **none** (not implemented) |
| **Platform notes** | Linux primary. Duration probing uses the headless OpenCV wheel, which does not need `libGL.so.1`. Other OS OK when FFmpeg + OpenCV are available |
| **Product version** | 1.0.7 |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution**: Assume FFmpeg may be missing.  
- **Principle 10 – Least privilege**: No root prerequisites command forced.  
- **Principle 2 – Intentional**: External vs pip deps separated.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Document before fail.  
- **Intentional:** No fake “one command installs OS FFmpeg” claim.  
- **Anti-fragile:** Works wherever PATH FFmpeg exists.  
- **Over-protect:** No silent elev install.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Claim FFmpeg is installed by `pip install VideoSpeed` alone.  
2. Add root package-manager elev without elev allowlist law and user order.  
3. Drop OpenCV or FFmpeg from prerequisite tables while code still depends on them.  
4. Store secrets in this file.

**Violating this rule is a critical honesty regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | FFmpeg listed as system binary |
| AC-2 | OpenCV pip dep is the headless wheel; floor is `requirement-python-dependency-management` |
| AC-3 | No false auto root-install claim |
| AC-4 | README aligns with this table |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-python-packaging` | Manifest shape |
| `requirement-python-dependency-management` | Pip names and version floors |
| `requirement-video-ffmpeg-pipeline` | uses FFmpeg |
| `requirement-python-error-handling` | missing tool messages |
| `requirement-python-tui` | Text menu painter in this package |
| `requirement-python-cli-logging` | How ChronicleLogger is used for status |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| TP-PRE-01 | `tests/test_prereq.py` | have | Missing ffmpeg message |
| TP-PRE-02 | `tests/test_prereq.py` | have | Missing OpenCV duration |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial runtime prerequisites law |
| 2026-08-19 | Active 1.1.0 | Drop ChronicleLogger; §1.1 |
| 2026-09-30 | Active 1.1.1 | `py-tui` peer is `requirement-python-tui` |
| 2026-09-30 | Active 1.1.2 | Duration dep is `opencv-python-headless` (no `libGL.so.1`) |
| 2026-09-30 | Active 1.1.3 | Pip floors owned by `requirement-python-dependency-management` |
| 2026-10-01 | Active 1.1.4 | ChronicleLogger is a pip floor again, owned by the dependency requirement |
| 2026-10-01 | Active 1.1.5 | Text menu is in this package; no menu pip row |
| 2026-10-01 | Active 1.1.6 | Text menu is class `Tui` in `src/VideoSpeed/tui.py`. Still not a pip package |
| 2026-10-01 | Active 1.1.7 | Text menu session is class `Tui`. Frame is class `MenuPainter`. Still not a pip package |

---

**Last Updated**: 2026-10-01  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
