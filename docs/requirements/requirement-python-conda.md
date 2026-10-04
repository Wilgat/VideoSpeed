**file**: docs/requirements/requirement-python-conda.md
**Status**: Active (Version 1.0.1)
**Area**: python
**Key**: `requirement-python-conda`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is how the host check decides that conda is present, and which paths the about page may print for `python2`, `python3`, and `conda`. The line labels and the rest of the page stay on `requirement-python-about`. When the check is also under pyenv, this file owns `python2` and `python3`. `pyenv location` stays on `requirement-python-pyenv`. Class `CheckSystem` in `src/VideoSpeed/check_system.py` performs the reads. The check does not install Python and does not run those programs.

### 1.1 Human-facing

**In one sentence:** On `video-speed about`, when this login has conda, the python2 and python3 lines are paths inside that conda prefix, and the conda line is `bin/conda`.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person reading the about page | `video-speed about` |
| The other role | The host check inside that page | Class `CheckSystem` fills the conda location and, when under conda, the interpreter lines |
| Not this file | The other about lines, the star box, and the pyenv launcher | `requirement-python-about` and `requirement-python-pyenv` |

| Includes | Excludes |
|----------|----------|
| Whether the check is under conda, and the conda path | A second about page, or a new host-check label |
| `python2` and `python3` inside the conda prefix when under conda | Running `python2`, `python3`, `conda`, or `pyenv` |

| Surface | What you open | What for |
|---------|---------------|----------|
| `video-speed about` | the about page | The conda line and, when under conda, the interpreter lines |
| `src/VideoSpeed/check_system.py` | class `CheckSystem` | The reads |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Open about | The page still has the same labels. When conda is present, `conda location` is `{root}/bin/conda`. It is not `{root}/condabin/conda`, even when `condabin` is earlier on `PATH`. `python2 location` and `python3 location` are inside the active prefix, or inside the base root when no prefix is active. A missing interpreter stays blank. | `video-speed about` |

## 2. Core Rules (Mandatory)

1. **One owner.** This file is the only definition of “under conda”, of `conda location`, and of `python2 location` and `python3 location` while the check is under conda. `requirement-python-about` keeps the labels, the order, and the rest of the page. `requirement-python-pyenv` keeps `pyenv location` and keeps those interpreter lines only when the check is not under conda. This file **MUST NOT** add or drop a host-check label.
2. **No spawn.** The reads **MUST NOT** spawn `python2`, `python3`, `conda`, or `pyenv`. Reading environment variables and path existence is allowed.
3. **Conda root from `CONDA_EXE`.** When `CONDA_EXE` is set and is not blank, that path is the only candidate. The parent directory of the executable **MUST** be named `bin` or `condabin`. The root is the parent of that directory. The root qualifies when `{root}/bin/conda` exists. The launcher **MAY** be a symlink. The check **MUST NOT** realpath `condabin/conda` and then treat another directory as the root. A set `CONDA_EXE` that does not qualify is not under conda. The check **MUST NOT** then read `CONDA_PREFIX` or search the login home.
4. **Conda root from `CONDA_PREFIX`.** When `CONDA_EXE` is unset or blank, and `CONDA_PREFIX` is set and is not blank, that directory is the only candidate. It qualifies when `{prefix}/bin/conda` exists. Otherwise it qualifies when the prefix is `{root}/envs/{name}`, `{name}` is one path segment other than empty, `.`, or `..`, and `{root}/bin/conda` exists. A set `CONDA_PREFIX` that does not qualify is not under conda. The check **MUST NOT** then search the login home.
5. **Conda root from the login install.** When `CONDA_EXE` and `CONDA_PREFIX` are both unset or blank, the root is the first directory in Implementation Notes that contains `bin/conda`. When none qualify, the check is not under conda.
6. **Under conda.** The check is under conda only when rules 3–5 find a root. `under_conda` **MUST** be true in that case and false otherwise. The logger read `in_conda` is `requirement-python-cli-logging`. It **MUST NOT** replace this flag, and it **MUST NOT** choose `conda location` or the interpreter lines.
7. **conda location.** When under conda, the value **MUST** be `{root}/bin/conda`. The check **MUST NOT** report `{root}/condabin/conda`, even when `condabin` appears first on `PATH`. The check **MUST NOT** use `shutil.which("conda")` for this line while under conda. When not under conda, the value **MUST** be `shutil.which("conda")`, else empty.
8. **Active prefix.** When under conda and `CONDA_PREFIX` is set, is not blank, and is either the root or `{root}/envs/{name}` with `{name}` one safe segment, that prefix is the interpreter directory. Otherwise the interpreter directory is the root.
9. **python2 and python3.** When under conda, each value **MUST** be `{prefix}/bin/python2` or `{prefix}/bin/python3` when that path exists, and **MUST** be empty otherwise. The value **MUST** be inside the conda root. The check **MUST NOT** substitute the base interpreter when the active prefix has no such file, and **MUST NOT** substitute a pyenv path or any other `PATH` hit outside the root.
10. Actor / role / subject / approver: **considered**. No dest machine. No approver. The table stays on `requirement-class-software-dev.md`.
11. Dest fence conditions: **considered — none**. Do not invent one.

### 2.1 Sample shape

`<root>` is the conda root from rules 3–5. It is not a frozen login or home path.

Active prefix `<root>/envs/demo`, with `python3` in that prefix and `python2` only in the base:

```text
    python2 location:
    python3 location: <root>/envs/demo/bin/python3
    conda location: <root>/bin/conda
```

No active prefix, with `python3` in the base:

```text
    python2 location:
    python3 location: <root>/bin/python3
    conda location: <root>/bin/conda
```

Invocation: `video-speed about`.

### 2.2 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Reader** | Class `CheckSystem` in `src/VideoSpeed/check_system.py` |
| **Knows it is under conda** | `under_conda` |
| **Root** | `conda_root` |
| **Launcher path** | `conda_location` returns `{root}/bin/conda` and does not report `condabin/conda` |
| **Interpreter directory** | `conda_prefix` |
| **Interpreter path** | `conda_interpreter("python2")` and `conda_interpreter("python3")` |
| **Line value** | `about_tool_location` for `python2`, `python3`, and `conda`. `check_system_lines` calls it. When under conda, `python2` and `python3` use this file even if `under_pyenv` is also true |
| **Login install names** | In order, under the login home: `miniconda3`, `anaconda3`, `miniforge3`, `mambaforge`. Used only when `CONDA_EXE` and `CONDA_PREFIX` are both unset or blank |
| **Labels** | Unchanged. Owned by `requirement-python-about` |
| **Page** | `video-speed about` and menu **about** print `AboutPage.framework_about`, which calls `check_system_lines` |
| **Privilege** | normal user privilege |

### 2.3 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 5 – SSOT** (https://github.com/cloudgen/ciao): one file owns the conda root, the conda launcher, and the interpreter lines while under conda.
- **CIAO Principle 2 – Intentional** (https://github.com/cloudgen/ciao): `bin/conda` is the launcher. `condabin/conda` is not that line.
- **CIAO Principle 1 – Caution** (https://github.com/cloudgen/ciao): a missing interpreter stays blank. The check does not run conda.
- **CIAO Principle 3 – Anti-fragile** (https://github.com/cloudgen/ciao): a named `CONDA_EXE` or `CONDA_PREFIX` that is not a conda root does not fall through to another directory.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, **admin privilege** and **dedicated system user privilege** stay unused. **This requirement:** deciding the conda root and filling the conda and interpreter lines **MUST NOT** call `sudo`, wrap `apt` or `dnf`, create a dedicated account, or recommend `sudo pip` or `sudo curl | sh`. Git Bash and Windows cmd **MUST NOT** invoke Termux `pkg`. The check only reads the environment and files under the conda root.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** A missing `python2`, `python3`, or `conda` launcher is an empty location, not an error.
- **Intentional:** Under conda, the conda line is `{root}/bin/conda`. The interpreter lines are inside the active prefix.
- **Anti-fragile:** An active environment without `python2` leaves that line blank. It does not borrow the base interpreter.
- **Over-protect (Principle 20):** Do not spawn conda to ask it where it lives, and do not print a path outside the root while under conda.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT:**

- Treat `{root}/condabin/conda` as `conda location` when `{root}/bin/conda` exists.
- Realpath `condabin/conda` and then print a different launcher path.
- Print a pyenv shim, or `/usr/bin/python2` or `/usr/bin/python3`, for those lines while the check is under conda.
- Fall back to the login home install when `CONDA_EXE` or `CONDA_PREFIX` is set and does not qualify.
- Fall back from an active prefix to the base interpreter when the prefix has no `python2` or `python3`.
- Accept an environment name that contains a slash, a backslash, `.`, or `..`.
- Spawn `python2`, `python3`, `conda`, or `pyenv` to fill these lines.
- Replace `under_conda` with the logger read `inConda`. That read is `in_conda` on `requirement-python-cli-logging`. The location lines stay on this file’s root test.
- Add a host-check label for this rule, or drop `python2 location`, `python3 location`, or `conda location`.
- Freeze a Unix login or a `/home/<login>/…` path into this requirement.

## 5. Design-time verification

| ID | Suite | Status |
|----|-------|--------|
| TP-ABOUT-11 | `tests/test_about.py` | have |
| TP-ABOUT-12 | `tests/test_about.py` | have |

TP-ABOUT-11 builds a conda root whose `condabin/conda` sits ahead of `bin/conda` on `PATH`, sets `CONDA_EXE` to that `condabin` file, and sets `CONDA_PREFIX` to `{root}/envs/demo`. It asserts `under_conda` is true, `conda location` is `{root}/bin/conda`, `python3 location` is `{root}/envs/demo/bin/python3`, and `python2 location` is empty even though the base has `python2`. A pyenv root in the same environment does not replace those interpreter lines, and `pyenv location` stays `{pyenv}/bin/pyenv`. With both conda variables unset, a login install named `miniconda3` supplies the root and the base `python3`. The about page text contains those paths. The check does not spawn a process. TP-ABOUT-12 sets `CONDA_EXE` to a path that is not `bin/conda` or `condabin/conda`, with a `miniconda3` tree available on the login search, and asserts the check is not under conda, so the three lines stay on `shutil.which`.

**Matrix:** `reviews/requirement-test-matrix.md`
**Map:** `reviews/test-plan.md`.

## 6. Related artifacts

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-python-about.md` | Labels, order, and the rest of the about page |
| `docs/requirements/requirement-python-pyenv.md` | Pyenv launcher, and interpreter lines when not under conda |
| `docs/requirements/requirement-python-oop.md` | Class `CheckSystem` owns these methods |
| `docs/requirements/requirement-class-software-dev.md` | Approver none; no dest fence |
| `src/VideoSpeed/check_system.py` | The reads |
| `src/VideoSpeed/about_page.py` | Prints the host check |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-02 | Active 1.0.0 | Under conda, about shows python2 and python3 inside the prefix, and conda location is `bin/conda` |
| 2026-10-02 | Active 1.0.1 | `in_conda` stays on `requirement-python-cli-logging`. It does not replace `under_conda` and does not choose these location lines |

**Last Updated**: 2026-10-02
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
