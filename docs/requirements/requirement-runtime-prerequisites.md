**file**: docs/requirements/requirement-runtime-prerequisites.md  
**Status**: Active (Version 1.0.0)  
**Area**: runtime  
**Key**: `requirement-runtime-prerequisites`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Declare **host and Python runtime prerequisites** required to run VideoSpeed successfully. This product does **not** implement a privileged system `prerequisites` installer command; this file is the **documentation and validation SSOT** for what must already be present.

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
| `opencv-python` | pip package | duration probe | `pyproject.toml` / pip |
| `ChronicleLogger` | pip package | logging dependency (declared) | `pyproject.toml` / pip |
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
| **Declared pip deps** | `opencv-python`, `ChronicleLogger>=1.2.3` |
| **System binary** | `ffmpeg` on `PATH` |
| **Auto install command** | **none** (not implemented) |
| **Platform notes** | Linux primary; other OS OK when FFmpeg + OpenCV available |
| **Product version** | 1.0.5 |

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
| AC-2 | opencv-python listed as pip dep |
| AC-3 | No false auto root-install claim |
| AC-4 | README aligns with this table |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-python-packaging` | pip deps |
| `requirement-video-ffmpeg-pipeline` | uses FFmpeg |
| `requirement-python-error-handling` | missing tool messages |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| TP-PRE-01 | `command -v ffmpeg` | todo | Host check |
| TP-PRE-02 | import cv2 | todo | Python env |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial runtime prerequisites law |

---

**Last Updated**: 2026-08-09  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
