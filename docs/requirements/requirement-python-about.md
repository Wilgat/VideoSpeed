**file**: docs/requirements/requirement-python-about.md
**Status**: Active (Version 1.0.7)
**Area**: python
**Key**: `requirement-python-about`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the about page for VideoSpeed. Menu action **about** returns one text page: the product identity lines, a host check, and a star-bordered install box. This file names every line and the read that fills it.

The screen that shows the page stays on `requirement-python-tui`. The domain summary sentence stays on `requirement-domain-videospeed`. The version digits stay on `requirement-python-version`. `--version` stays a one-line human string on `requirement-python-cli-interface`. This file does not open the menu, encode a clip, or write JSON.

### 1.1 Human-facing

**In one sentence:** On the text menu, choose **about** and the page names this build, this computer, and where the program is running from.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person reading the about page | Menu row **83 about**, under **8** self-management |
| The other role | The text-menu result page | `requirement-python-tui` draws it and scrolls it |
| Not this file | Cut, speed, boomerang, and `--json` | Domain, pipeline, and JSON requirements |

| Includes | Excludes |
|----------|----------|
| Identity lines, the host-check lines, and the star box | A second about layout, a remote version lookup |
| How each value is read on this machine | Running `python2` or `python3` to ask their version |
| Install kind: global, local, or uninstalled | An install command while this product has no download URL |

| Surface | What you open | What for |
|---------|---------------|----------|
| `video-speed` | text menu on a terminal | Choose **8**, then **83**, or type `about` |
| `video-speed about` | the same page, no front-board pick | No folder prompt and no file prompt (`requirement-python-interactive-vs-noninteractive` §2.1b) |
| `src/VideoSpeed/about_page.py` | class `AboutPage` | The page text. It calls `CheckSystem` for the host check. `TP-OOP-04` has landed |
| `src/VideoSpeed/check_system.py` | class `CheckSystem` | Host-check reads. `TP-OOP-02` has landed |
| `tests/test_about.py` | suite | The lines and the reads |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Open about | The menu stays in the result page. The page starts with the product name and the domain sentence, then the host check, then the star box. Up and Down scroll when the page is longer than the screen. Any other key returns to the menu. | `video-speed`, then `8`, then `83` |
| Read the install sentence | A checkout under `src/VideoSpeed` with `pyproject.toml` above it says UNINSTALLED. A copy under your home directory says LOCAL INSTALLED. A copy under `/usr`, `/opt`, or `/bin` says GLOBAL INSTALLED. | Same page |
| Read the pyenv lines | When this login has pyenv, `python2 location` and `python3 location` are paths inside that root. `pyenv location` is `bin/pyenv`, not `libexec/pyenv`. The reads are `requirement-python-pyenv`. | `video-speed about` |

## 2. Core Rules (Mandatory)

1. **One page.** Menu action **about** and the verb `video-speed about` **MUST** show one result page whose body is this file. The verb **MUST NOT** ask for a folder or a file. The page **MUST** be three blocks in this order: identity, host check, star box. A blank line **MUST** separate the blocks. The page **MUST NOT** be `--version`, and **MUST NOT** be the JSON object.
2. **Identity block.** The first four lines **MUST** be, in order: `{APP_NAME} {version}`, `Domain: Cut → speed/length → optional boomerang for MP4`, `Runtime tools: FFmpeg (encode), OpenCV (duration probe)`, `Entry points: video-speed, python -m VideoSpeed`. `{version}` **MUST** be the package version from `requirement-python-version`. The page **MUST NOT** name `py-tui`.
3. **Host-check header.** The check **MUST** start with `{local stamp} {APP_NAME}(v{version})  [CHECK SYSTEM]:` and the next line **MUST** be two spaces then `Now checking your operation system!`. The stamp **MUST** be local time `YYYY-MM-DD HH:MM:SS.ffffff` from `datetime.datetime.now()`. There are two spaces before `[CHECK SYSTEM]:`.
4. **Host-check fields.** After the header, the page **MUST** print these labels in this order, each starting with four spaces, then the label, a colon, a space, and the value. A missing value **MUST** leave the line in place. The check **MUST NOT** spawn `python2`, `python3`, `conda`, or `pyenv`.

| Label | Read |
|-------|------|
| `Python` | `platform.python_version()`. When `sys.version` contains `[PyPy ` and `with`, append ` (` plus the text after `[` and before `with`, stripped, plus `)`. |
| `C Library` | Compiler token from `sys.version`, brackets removed. See rule 5. |
| `Operation System` | `platform.freedesktop_os_release()["PRETTY_NAME"]` when that call works and the name is non-empty. Otherwise `platform.platform()`. |
| `Architecture` | See rule 6. |
| `Current User` | Environment `USER`, else `USERNAME`, else `getpass.getuser()`. On failure, empty. |
| `Shell` | Environment `SHELL`, else empty. |
| `Python Executable` | Basename of `sys.executable`. Split on `/` or `\`. Empty when `sys.executable` is empty. |
| `python2 location` | When the check is under pyenv, the path from `requirement-python-pyenv`. Otherwise `shutil.which("python2")`, else empty. |
| `python3 location` | When the check is under pyenv, the path from `requirement-python-pyenv`. Otherwise `shutil.which("python3")`, else empty. |
| `conda location` | `shutil.which("conda")`, else empty. |
| `pyenv location` | When the check is under pyenv, `{root}/bin/pyenv` from `requirement-python-pyenv`. Otherwise `shutil.which("pyenv")`, else empty. |
| `Inside docker container` | `True` when `/.dockerenv` exists, otherwise `False`. Python’s `True` / `False` spelling. No other container probe. |
| `Cython String` | `sysconfig.get_config_var("SOABI")`, else empty. The label stays `Cython String`. |
| `Binary Type` | `{arch}-{libc}` when both are non-empty. `{arch}-` when libc is empty. Empty when arch is empty. |
| `Location` | The program path from rule 8. The same path **MUST** be the indented path inside the star box. |

5. **C Library parse.** Start from `sys.version`. If it contains a newline, keep the second line. Otherwise, if it contains `[` and `]`, keep the text between the first `[` and the first `]`. If that text is exactly `GCC`, use `[GCC]`. If it contains ` (Red Hat`, cut at that phrase and append `]`. If the probe (the extracted text when it still contains `[PyPy `, otherwise the original `sys.version`) contains `[PyPy ` and `with`, the compiler text is `[` plus the text after `with `. Strip one pair of surrounding `[` `]` before display.
6. **Architecture.** If `sys.version` contains `AMD64`, the arch is `amd64`. Else if it contains `AMD32`, the arch is `x86`. Else map `platform.machine()` ignoring case: `x86_64` and `amd64` → `amd64`; `aarch64` and `arm64` → `arm64`; `i386`, `i686`, and `x86` → `x86`. Any other machine name is kept as `platform.machine()` returned it.
7. **Libc token.** Read `platform.libc_ver()[0]`, or `unknown` when that call fails. If `sys.version` contains `AMD64` or `AMD32` and also `MSC`, the token is `msc`. If `sys.version` contains `clang` in any letter case, the token is `clang`. If the token is still empty and `SHELL` is `/bin/ash`, the token is `muslc`.
8. **Program path.** If `sys.argv[0]` is an existing file and its basename is the console script or `VideoSpeed`, use its real path. If it is an existing file in the same directory as `cli.py` and the basename is `cli.py` or `__main__.py`, use that real path. Otherwise use the real path of `cli.py`.
9. **Install kind.** Classify that real path in this order. A path under `site-packages` or `dist-packages` is packaged.
   - Not packaged, the path contains `{sep}src{sep}VideoSpeed{sep}`, and a parent within eight levels has `pyproject.toml`: **uninstalled**.
   - Under the home directory, and packaged or the basename is the console script or `VideoSpeed`: **local**.
   - Starts with `/usr/`, `/opt/`, or `/bin/`: **global**.
   - Packaged and not under the home directory: **global**.
   - Otherwise: **uninstalled**.
10. **Star box sentences.** **global** **MUST** say `You are using the GLOBAL INSTALLED version, location:`. **local** **MUST** say `You are using the LOCAL INSTALLED version, location:`. **uninstalled** **MUST** say `You are using an UNINSTALLED version, location:`.
11. **Star box lines.** Inside the border, in order: the title `{APP_NAME} ({MAJOR}.{MINOR}.{PATCH}) by {author} on {date}`; a blank line; the install sentence; four spaces and the program path; a blank line; `Basic Usage:`; four spaces and the usage line; a blank line; `Please visit our homepage: `; four spaces, a double quote, the homepage, and a double quote; then the trailing blanks from rule 12. `{MAJOR}.{MINOR}.{PATCH}` **MUST** be the version triple, not a second literal. Author, date, homepage, and usage are the constants in Implementation Notes.
12. **Border.** Take the lines of rule 11. When the download URL is empty and the homepage is non-empty, print the first twelve of those source lines (through the second blank after the homepage). When both are empty, print the first eleven. When the download URL is non-empty, the source list uses `Installation command:` and `    curl -fsSL {url} | {python basename}` in place of the extra blanks, and the print stops before the final blank. Pad every printed line on the right to the longest printed line. The top and bottom borders are that width plus four asterisks. Each body row is `* `, the padded line, ` *`. One all-space body row sits under the top border and one sits above the bottom border.
13. **No install channel on this page.** The product download URL **MUST** stay empty while no Active install requirement names a channel. The live about page **MUST NOT** contain `curl -fsSL`. The box **MAY** render that install line only when a caller passes a non-empty URL. This product’s about caller **MUST NOT** pass one.
14. **No privilege and no network.** Building the page **MUST NOT** call `sudo`, wrap `apt` or `dnf`, create an account, open a socket, or recommend `sudo pip` or `sudo curl | sh`. Git Bash and Windows cmd **MUST NOT** invoke Termux `pkg`.
15. Actor / role / subject / approver: **considered**. No dest machine. No approver. The table stays on `requirement-class-software-dev.md`.
16. Dest fence conditions: **considered — none**. Do not invent one.
17. The host-check functions named in `requirement-python-oop` **MUST** be methods of class `CheckSystem` in `src/VideoSpeed/check_system.py`. This file still owns the line text. `TP-OOP-02` has landed. Class `AboutPage` in `src/VideoSpeed/about_page.py` is the about composer. It **MUST** call `CheckSystem` for the check block and for `self_location`. `TP-OOP-04` has landed.

### 2.1 Sample shape

Values in angle brackets are the live read. They are not a frozen login or home path.

```text
VideoSpeed 1.0.7
Domain: Cut → speed/length → optional boomerang for MP4
Runtime tools: FFmpeg (encode), OpenCV (duration probe)
Entry points: video-speed, python -m VideoSpeed

2026-10-01 11:16:23.700590 VideoSpeed(v1.0.7)  [CHECK SYSTEM]:
  Now checking your operation system!
    Python: 3.12.3
    C Library: GCC 13.3.0
    Operation System: Ubuntu 24.04 LTS
    Architecture: amd64
    Current User: <login>
    Shell: /bin/bash
    Python Executable: python3
    python2 location: <python2 inside the pyenv root, or empty>
    python3 location: <python3 inside the pyenv root, or empty>
    conda location:
    pyenv location: <pyenv root>/bin/pyenv
    Inside docker container: False
    Cython String: cpython-312-x86_64-linux-gnu
    Binary Type: amd64-glibc
    Location: <program path>

*****************************************************
*                                                   *
* VideoSpeed (1.0.7) by Wilgat Wong on 2026-10-01   *
*                                                   *
* You are using an UNINSTALLED version, location:   *
*     <program path>                                *
*                                                   *
* Basic Usage:                                      *
*     video-speed --file clip.mp4 --start 0 --end 5 *
*                                                   *
* Please visit our homepage:                        *
*     "https://github.com/Wilgat/VideoSpeed"        *
*                                                   *
*                                                   *
*                                                   *
*****************************************************
```

The version string in the sample is the package version at the time of writing. A later package version **MUST** appear instead. The stamp **MUST** be the clock at the moment the page is built.

Invocation: `video-speed` on a terminal, then `8` or `about`.

### 2.2 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Page builder** | Class `AboutPage` in `src/VideoSpeed/about_page.py` (`framework_about`). `TP-OOP-04` has landed |
| **Host check** | Class `CheckSystem` in `src/VideoSpeed/check_system.py` (`requirement-python-oop`, `TP-OOP-02`) |
| **Pyenv paths** | `python2`, `python3`, and `pyenv` locations when under pyenv (`requirement-python-pyenv`) |
| **Star box** | `AboutPage.about_box_lines` calls `CheckSystem` for `self_location` and the Python executable name |
| **Menu hook** | `Tui.open_text_menu` passes `on_about` to `AboutPage.framework_about` |
| **APP_NAME** | `VideoSpeed` |
| **Console script** | `video-speed` |
| **Author** | `Wilgat Wong` (`LICENSE.md` copyright name) |
| **Homepage** | `https://github.com/Wilgat/VideoSpeed` (`pyproject.toml` Homepage) |
| **About date** | `2026-10-01` (`LAST_UPDATE`). This is the box date, not the host-check stamp |
| **Usage line** | `video-speed --file clip.mp4 --start 0 --end 5` |
| **Download URL** | empty |
| **Docker marker** | `/.dockerenv` only |
| **Privilege** | normal user privilege |

### 2.3 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 5 – SSOT** (https://github.com/cloudgen/ciao): one page owns the about lines and the reads that fill them.
- **CIAO Principle 2 – Intentional** (https://github.com/cloudgen/ciao): each label names one read. The install kind is three named sentences.
- **CIAO Principle 1 – Caution** (https://github.com/cloudgen/ciao): missing tools stay blank. The page does not run interpreters or open the network.
- **CIAO Principle 16 – Interactive** (https://github.com/cloudgen/ciao): a person opens the page from the menu. `--version` stays the short line.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, **admin privilege** and **dedicated system user privilege** stay unused. **This requirement:** building the about page **MUST NOT** call `sudo`, wrap `apt` / `dnf`, create a dedicated account, or recommend `sudo pip` or `sudo curl \| sh`. Git Bash and Windows cmd **MUST NOT** invoke Termux `pkg`. The page only reads the local interpreter, environment, and files.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** A missing `python2`, `conda`, or `pyenv` is an empty location, not an error.
- **Intentional:** Field order and the three install sentences are named.
- **Anti-fragile:** A source checkout, a home install, and a `/usr` install each get a sentence from the same path rules.
- **Over-protect (Principle 20):** Do not add a second about page, and do not print a `curl | sh` line while the download URL is empty.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT:**

- Drop a host-check label or change its order.
- Replace `shutil.which` with a subprocess that runs `python2`, `python3`, `conda`, or `pyenv`.
- Report `{root}/libexec/pyenv` as `pyenv location` when `{root}/bin/pyenv` exists. That read is `requirement-python-pyenv`.
- Probe containers by anything other than `/.dockerenv`.
- Show GLOBAL, LOCAL, or UNINSTALLED for a path the rules in this file classify differently.
- Put `curl -fsSL` on the live about page while the download URL is empty.
- Turn this page into `--version` or into the JSON object.
- Name `py-tui` on the page.
- Freeze a Unix login or a `/home/<login>/…` path into this requirement.

## 5. Design-time verification

| ID | Suite | Status |
|----|-------|--------|
| TP-ABOUT-01 | `tests/test_about.py` | have |
| TP-ABOUT-02 | `tests/test_about.py` | have |
| TP-ABOUT-03 | `tests/test_about.py` | have |
| TP-ABOUT-04 | `tests/test_about.py` | have |
| TP-ABOUT-05 | `tests/test_about.py` | have |
| TP-ABOUT-06 | `tests/test_about.py` | have |
| TP-ABOUT-07 | `tests/test_about.py` | have |
| TP-ABOUT-08 | `tests/test_tui.py` | have |
| TP-ABOUT-09 | `tests/test_about.py` | have |
| TP-ABOUT-10 | `tests/test_about.py` | have |

TP-ABOUT-01 asserts the identity line, every host-check label, the star-box title, and that the live page has no `curl -fsSL` and no `py-tui`. TP-ABOUT-02 asserts the stamp `YYYY-MM-DD HH:MM:SS.ffffff`, the `[CHECK SYSTEM]:` header, and the field order. TP-ABOUT-03 asserts the star box is one rectangle and that a global path uses the GLOBAL sentence. TP-ABOUT-04 asserts an explicit download URL renders the install line, and that the product URL stays empty. TP-ABOUT-05 asserts the GCC token, the PyPy token, the arch map, `msc`, `clang`, `muslc`, and `amd64-glibc`. TP-ABOUT-06 asserts checkout = uninstalled, a home copy = local, and `/usr` = global. TP-ABOUT-07 asserts the docker marker file and a missing `which` result. TP-ABOUT-08 asserts a long about page scrolls to `Basic Usage:` and a one-line result still closes on Down. TP-ABOUT-09 and TP-ABOUT-10 assert the pyenv paths. The pass text is `requirement-python-pyenv`.

**Matrix:** `reviews/requirement-test-matrix.md`
**Map:** `reviews/test-plan.md`.

## 6. Related artifacts

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-domain-videospeed.md` | Domain sentence on the identity block |
| `docs/requirements/requirement-python-tui.md` | Result page; scroll; no frame on about |
| `docs/requirements/requirement-python-oop.md` | Class `CheckSystem` owns the host-check reads. Class `AboutPage` owns the composer |
| `docs/requirements/requirement-python-pyenv.md` | Under pyenv, the `python2`, `python3`, and `pyenv` paths |
| `docs/requirements/requirement-python-version.md` | Version digits in the title and the stamp |
| `docs/requirements/requirement-python-cli-interface.md` | `--version` stays the short human line. The verb `about` is named there |
| `docs/requirements/requirement-class-software-dev.md` | Approver none; no dest fence |
| `src/VideoSpeed/about_page.py` | Class `AboutPage`. `framework_about`. `TP-OOP-04` has landed |
| `LICENSE.md` | Author name |
| `pyproject.toml` | Homepage URL |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-01 | Active 1.0.0 | About page: identity, host check, star box, and the read for each line |
| 2026-10-01 | Active 1.0.1 | Host-check functions belong to class `CheckSystem`. Until `check_system.py` exists, `cli.py` may hold them |
| 2026-10-01 | Active 1.0.2 | Verb `video-speed about` shows this same page and does not ask for a folder or a file |
| 2026-10-01 | Active 1.0.3 | `TP-OOP-02` landed. The about composer calls `CheckSystem` |
| 2026-10-01 | Active 1.0.4 | The composer is class `AboutPage`. Line text stays here. `TP-OOP-04` is todo |
| 2026-10-01 | Active 1.0.5 | `AboutPage` is on disk. `TP-OOP-04` has landed. Line text stays here |
| 2026-10-02 | Active 1.0.6 | `python2`, `python3`, and `pyenv` locations, when under pyenv, are `requirement-python-pyenv` |
| 2026-10-02 | Active 1.0.7 | About is row **83** under front **8** self-management. Typing `about` still opens this page |

**Last Updated**: 2026-10-02
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
