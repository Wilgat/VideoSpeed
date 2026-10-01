**file**: docs/requirements/requirement-python-version.md
**Status**: Active (Version 1.0.3)
**Area**: python
**Key**: `requirement-python-version`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

# Requirement: python-version

## 1. Purpose

This file is the **version SSOT** for VideoSpeed. The product version is three integers, `MAJOR_VERSION`, `MINOR_VERSION`, and `PATCH_VERSION`, written once. The release string is built from those integers. Packaging copies that string into the manifest. `main` reads the integers. It does not keep a second triple.

### 1.1 Human-facing

**In one sentence:** VideoSpeed’s version is the three numbers in `src/VideoSpeed/__init__.py`, and every other place prints the string those numbers make.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person checking which build is installed | `video-speed --version` |
| The other role | The manifest that pip reads | `pyproject.toml` `[project].version` |
| Not this file | How the text menu is drawn | `requirement-python-tui` |

| Includes | Excludes |
|----------|----------|
| The three integers, the joined string, and which file wins | A second `MAJOR_VERSION` inside `cli.py` |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/VideoSpeed/__init__.py` | version SSOT | The three integers and `__version__` |
| `pyproject.toml` | manifest copy | Must equal `__version__` |
| `video-speed --version` | command | Prints the same string |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Ask the program its version | It prints the string built from `MAJOR_VERSION`, `MINOR_VERSION`, and `PATCH_VERSION`. | `video-speed --version` |
| Cut a release | Change the three integers, and the string and the manifest move with them in the same change. | Edit `src/VideoSpeed/__init__.py` and `pyproject.toml` together |

## 2. Core Rules (Mandatory)

1. **MUST** store the product version as three integers named `MAJOR_VERSION`, `MINOR_VERSION`, and `PATCH_VERSION`.  
2. **MUST** keep those three names in `src/VideoSpeed/__init__.py` only. That module is the version SSOT.  
3. **MUST** set `__version__` in that same module to `"{0}.{1}.{2}".format(MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION)`.  
4. Each integer **MUST** be a non-negative whole number. The string **MUST** be three numeric fields and two dots, with no extra suffix.  
5. `pyproject.toml` `[project].version` **MUST** equal `__version__`. Packaging owns the manifest shape and **points here** for the digits.  
6. `main` **MUST** read these three integers from the package. **MUST NOT** declare another `MAJOR_VERSION`, `MINOR_VERSION`, or `PATCH_VERSION` in `cli.py` or in `main`.  
7. A debug status line **MUST** show the three integers as `v{MAJOR}.{MINOR}.{PATCH}` (the same shape the sibling product AnimeDlp uses for that line).  
8. Bumping any integer **MUST** update `__version__` and `pyproject.toml` `[project].version` in the same change.  
9. **MUST NOT** keep a fallback literal such as `"1.0.6"` in `cli.py` for when the package import fails.  
10. **MUST NOT** import `cli` from `__init__.py`. Reading the version must not load the editor.

### 2.1 Implementation Notes (this project)

Sibling product **AnimeDlp** names the same three fields, `MAJOR_VERSION`, `MINOR_VERSION`, and `PATCH_VERSION`. Its packaging rule says a copy of that triple inside `cli.py` must match the package version, and the package (`__version__` and `pyproject.toml`) is authoritative when the two differ. Its suite then forbids a second triple on the CLI module. VideoSpeed follows that lesson: the three integers live once, on the package, and `main` reads them.

| Field | Value |
|-------|--------|
| **SSOT file** | `src/VideoSpeed/__init__.py` |
| **MAJOR_VERSION** | `1` |
| **MINOR_VERSION** | `0` |
| **PATCH_VERSION** | `10` |
| **`__version__`** | `1.0.10` |
| **Manifest copy** | `pyproject.toml` `[project].version` = `1.0.10` |
| **Who reads it** | `main` in `src/VideoSpeed/cli.py` (`requirement-python-cli-interface`) |
| **Debug line shape** | `{appname} v1.0.10 ({file})` from the three integers |

```python
MAJOR_VERSION = 1
MINOR_VERSION = 0
PATCH_VERSION = 10
__version__ = "{0}.{1}.{2}".format(MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION)
```

### 2.2 Why This Requirement Exists (CIAO)

- **Principle 5 – SSOT** (https://github.com/cloudgen/ciao): one triple, one string.  
- **Principle 2 – Intentional** (https://github.com/cloudgen/ciao): major, minor, and patch are named.  
- **Principle 1 – Caution** (https://github.com/cloudgen/ciao): a hardcoded fallback in `cli.py` cannot drift away from the package.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, the version is still the three integers in the package. **This requirement:** do not use admin privilege to read or print the version.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** No second triple and no fallback literal.  
- **Intentional:** Three named integers, then the string.  
- **Anti-fragile:** Manifest and `--version` both follow the package.  
- **Over-protect:** `__init__.py` does not import the CLI.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

1. Put `MAJOR_VERSION`, `MINOR_VERSION`, or `PATCH_VERSION` in `cli.py`.  
2. Let `__version__` differ from the three integers.  
3. Let `pyproject.toml` `[project].version` differ from `__version__` while claiming a release.  
4. Restore a string literal fallback in `cli.py`.  
5. Import `cli` from `__init__.py` so that reading the version loads the editor.

**Violating this rule is a version-SSOT regression.**

## 5. Design-time verification

| TP-ID | Case | Status | Map |
|-------|------|--------|-----|
| `TP-VER-01` | Triple joins to `__version__` and that string is in `pyproject.toml` | have | `tests/test_package.py` · `reviews/test-plan.md` |
| `TP-VER-02` | `cli.py` does not assign `MAJOR_VERSION` | have | `tests/test_package.py` |
| `TP-VER-03` | Debug line prints `v{MAJOR}.{MINOR}.{PATCH}` | todo | `reviews/test-plan.md` |

## 6. Related artifacts (versioned surface only)

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-python-packaging.md` | Manifest copy of `__version__` |
| `docs/requirements/requirement-python-cli-interface.md` | `main` reads the triple first |
| `docs/requirements/requirement-python-cli-logging.md` | Debug line that prints the triple |
| `docs/requirements/requirement-class-software-dev.md` | Residual points here |
| `src/VideoSpeed/__init__.py` | Version SSOT |
| `pyproject.toml` | Manifest copy |
| `reviews/test-plan.md` | TP map |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-01 | Active 1.0.0 | Triple SSOT; AnimeDlp names; package wins |
| 2026-10-01 | Active 1.0.1 | Patch 8. Package string `1.0.8` |
| 2026-10-01 | Active 1.0.2 | Patch 9. Package string `1.0.9`. The non-TUI debug line still uses this triple |
| 2026-10-02 | Active 1.0.3 | Patch 10. Package string `1.0.10` |

---

**Last Updated**: 2026-10-01  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
