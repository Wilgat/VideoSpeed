**file**: docs/requirements/requirement-python-pyenv.md
**Status**: Active (Version 1.0.0)
**Area**: python
**Key**: `requirement-python-pyenv`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is how the host check decides that pyenv is present, and which paths the about page may print for `python2`, `python3`, and `pyenv`. The line labels and the rest of the page stay on `requirement-python-about`. Class `CheckSystem` in `src/VideoSpeed/check_system.py` performs the reads. The check does not install Python and does not run those programs.

### 1.1 Human-facing

**In one sentence:** On `video-speed about`, when this login has pyenv, the python2 and python3 lines are paths inside that pyenv root, and the pyenv line is `bin/pyenv`.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person reading the about page | `video-speed about` |
| The other role | The host check inside that page | Class `CheckSystem` fills the three location lines |
| Not this file | The other about lines, the star box, and the menu | `requirement-python-about` and `requirement-python-tui` |

| Includes | Excludes |
|----------|----------|
| Whether the check is under pyenv, and the three paths | A second about page, or a new host-check label |
| Paths read from the pyenv root and its version file | Running `python2`, `python3`, `conda`, or `pyenv` |

| Surface | What you open | What for |
|---------|---------------|----------|
| `video-speed about` | the about page | The three location lines |
| `src/VideoSpeed/check_system.py` | class `CheckSystem` | The reads |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Open about | The page still has the same labels. When pyenv is present, `pyenv location` is `{root}/bin/pyenv`. It is not `{root}/libexec/pyenv`, even when `libexec` is earlier on `PATH`. `python2 location` and `python3 location` are inside that same root, or blank when that interpreter is not there. | `video-speed about` |

## 2. Core Rules (Mandatory)

1. **One owner.** The three reads in this file are the only definition of “under pyenv” and of the `python2`, `python3`, and `pyenv` location values. `requirement-python-about` keeps the labels, the order, and the rest of the page. This file **MUST NOT** add or drop a host-check label.
2. **No spawn.** The reads **MUST NOT** spawn `python2`, `python3`, `conda`, or `pyenv`. Reading environment variables, the version file, and path existence is allowed. `conda location` stays `shutil.which("conda")` on `requirement-python-about`.
3. **Pyenv root.** When `PYENV_ROOT` is set and is not blank, that directory is the only candidate. The root qualifies when `{candidate}/bin/pyenv` exists. The launcher **MAY** be a symlink. When `PYENV_ROOT` is unset or blank, the candidate is the login’s `.pyenv` directory, and it qualifies on the same test. A set `PYENV_ROOT` that does not contain `bin/pyenv` is not under pyenv. The check **MUST NOT** then search the login `.pyenv`.
4. **Under pyenv.** The check is under pyenv only when rule 3 finds a root. `under_pyenv` **MUST** be true in that case and false otherwise. The running `sys.executable` **MAY** sit outside `versions/`. That does not by itself clear the flag, and a system interpreter **MUST NOT** set the flag when no root qualifies.
5. **pyenv location.** When under pyenv, the value **MUST** be `{root}/bin/pyenv`. The check **MUST NOT** realpath that launcher into `{root}/libexec/pyenv`. The check **MUST NOT** use `shutil.which("pyenv")` for this line while under pyenv. When not under pyenv, the value **MUST** be `shutil.which("pyenv")`, else empty.
6. **Version names.** When `PYENV_VERSION` is set and is not blank, split it on `:`. Otherwise read `{root}/version` and use its lines. Skip a blank token, the token `system`, the tokens `.` and `..`, and any token that contains `/` or `\`. Keep the remaining tokens in order.
7. **python2 and python3.** When under pyenv, each value **MUST** be chosen in this order, and **MUST** be empty when none match. The value **MUST** be a path inside the root. The check **MUST NOT** substitute a `PATH` hit outside the root.
   - For each version name from rule 6, `{root}/versions/{name}/bin/python2` or `{root}/versions/{name}/bin/python3` when that path exists.
   - Otherwise `{root}/shims/python2` or `{root}/shims/python3` when that path exists.
8. **Not under pyenv.** `python2 location` and `python3 location` **MUST** stay `shutil.which("python2")` and `shutil.which("python3")`, else empty.
9. Actor / role / subject / approver: **considered**. No dest machine. No approver. The table stays on `requirement-class-software-dev.md`.
10. Dest fence conditions: **considered — none**. Do not invent one.

### 2.1 Sample shape

`<root>` is the pyenv root from rule 3. It is not a frozen login or home path.

Selected versions `3.12.11` then `2.7.18`, with both version binaries present:

```text
    python2 location: <root>/versions/2.7.18/bin/python2
    python3 location: <root>/versions/3.12.11/bin/python3
    pyenv location: <root>/bin/pyenv
```

Version file `system`, and only the shims exist:

```text
    python2 location: <root>/shims/python2
    python3 location: <root>/shims/python3
    pyenv location: <root>/bin/pyenv
```

Invocation: `video-speed about`.

### 2.2 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Reader** | Class `CheckSystem` in `src/VideoSpeed/check_system.py` |
| **Knows it is under pyenv** | `under_pyenv` |
| **Root** | `pyenv_root` |
| **Launcher path** | `pyenv_location` returns `{root}/bin/pyenv` and does not resolve the symlink into `libexec` |
| **Version names** | `pyenv_version_names` |
| **Interpreter path** | `pyenv_interpreter("python2")` and `pyenv_interpreter("python3")` |
| **Line value** | `about_tool_location` for `python2`, `python3`, and `pyenv`. `check_system_lines` calls it. `conda` stays `command_location` |
| **Labels** | Unchanged. Owned by `requirement-python-about` |
| **Page** | `video-speed about` and menu **about** print `AboutPage.framework_about`, which calls `check_system_lines` |
| **Privilege** | normal user privilege |

### 2.3 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 5 – SSOT** (https://github.com/cloudgen/ciao): one file owns the pyenv root and the three paths. The about page keeps the labels.
- **CIAO Principle 2 – Intentional** (https://github.com/cloudgen/ciao): `bin/pyenv` is the launcher. `libexec/pyenv` is not that line.
- **CIAO Principle 1 – Caution** (https://github.com/cloudgen/ciao): a missing interpreter stays blank. The check does not run pyenv.
- **CIAO Principle 3 – Anti-fragile** (https://github.com/cloudgen/ciao): a named `PYENV_ROOT` that is not a pyenv root does not fall through to another directory.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, **admin privilege** and **dedicated system user privilege** stay unused. **This requirement:** deciding the pyenv root and filling the three location lines **MUST NOT** call `sudo`, wrap `apt` or `dnf`, create a dedicated account, or recommend `sudo pip` or `sudo curl | sh`. Git Bash and Windows cmd **MUST NOT** invoke Termux `pkg`. The check only reads the environment and files under the pyenv root.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** A missing `python2`, `python3`, or `pyenv` launcher is an empty location, not an error.
- **Intentional:** Under pyenv, the pyenv line is `{root}/bin/pyenv`. The interpreter lines are inside that root.
- **Anti-fragile:** `PYENV_VERSION` and the version file select a version binary. With `system`, the shim inside the root is the path.
- **Over-protect (Principle 20):** Do not spawn pyenv to ask it where it lives, and do not print a path outside the root while under pyenv.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT:**

- Treat `{root}/libexec/pyenv` as `pyenv location` when `{root}/bin/pyenv` exists.
- Realpath `bin/pyenv` and then print the `libexec` target.
- Print `/usr/bin/python2` or `/usr/bin/python3` for those lines while the check is under pyenv.
- Fall back to the login `.pyenv` when `PYENV_ROOT` is set and does not contain `bin/pyenv`.
- Accept a version token that contains a slash, a backslash, `.`, or `..`.
- Spawn `python2`, `python3`, `conda`, or `pyenv` to fill these lines.
- Add a host-check label for this rule, or drop `python2 location`, `python3 location`, or `pyenv location`.
- Freeze a Unix login or a `/home/<login>/…` path into this requirement.

## 5. Design-time verification

| ID | Suite | Status |
|----|-------|--------|
| TP-ABOUT-09 | `tests/test_about.py` | have |
| TP-ABOUT-10 | `tests/test_about.py` | have |

TP-ABOUT-09 builds a pyenv root whose `bin/pyenv` is a symlink to `libexec/pyenv`, puts `libexec` first on `PATH`, and asserts `under_pyenv` is true. With `PYENV_VERSION` set to `3.12.11:2.7.18`, `python3 location` is `{root}/versions/3.12.11/bin/python3` and `python2 location` is `{root}/versions/2.7.18/bin/python2`. `pyenv location` is `{root}/bin/pyenv`. With the version file set to `system` and only shims present, both interpreter lines are the shims inside the root. The about page text contains those paths. The check does not spawn a process. TP-ABOUT-10 sets `PYENV_ROOT` to a directory with no `bin/pyenv` and asserts the check is not under pyenv, so the three lines stay on `shutil.which`.

**Matrix:** `reviews/requirement-test-matrix.md`
**Map:** `reviews/test-plan.md`.

## 6. Related artifacts

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-python-about.md` | Labels, order, and the rest of the about page |
| `docs/requirements/requirement-python-oop.md` | Class `CheckSystem` owns these methods |
| `docs/requirements/requirement-class-software-dev.md` | Approver none; no dest fence |
| `src/VideoSpeed/check_system.py` | The reads |
| `src/VideoSpeed/about_page.py` | Prints the host check |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-02 | Active 1.0.0 | Under pyenv, about shows python2 and python3 inside the root, and pyenv location is `bin/pyenv` |

**Last Updated**: 2026-10-02
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
