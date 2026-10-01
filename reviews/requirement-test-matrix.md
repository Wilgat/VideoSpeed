# Requirement ↔ test matrix — VideoSpeed

**Updated:** 2026-10-02  
**Suite:** `tests/run.sh` — Core have; TP-FFMPEG skip without ffmpeg/fixture

| Requirement key | Area | TP families | Coverage notes |
|-----------------|------|-------------|----------------|
| requirement-class-software-dev | class | TP-PKG-04 · TP-STRUCT-01 | Python residual; stack honesty |
| requirement-domain-videospeed | domain | TP-DOMAIN-* · TP-FFMPEG-01..05 · TP-CLI-03 | Four pillars; workflow |
| requirement-video-ffmpeg-pipeline | video | TP-FFMPEG-* · TP-FS-* · TP-ERR-03 | Ops SSOT; **shutil.move**; temps |
| requirement-python-cli-interface | python | TP-CLI-* · TP-SELF-01 · TP-MAIN-01 | Entry, product verbs, and `main` order. `TP-CLI-07` **have**. `TP-SELF-01` **have** (pip version-check and self-update). `main` order **todo** |
| requirement-python-interactive-vs-noninteractive | python | TP-MODE-01..08 · TP-CLI-03 · TP-CLI-06 · TP-CLI-07 | Menu walk, verb prompts (folder then file), or one job. `TP-MODE-05`..`08` and `TP-CLI-07` **have**. `TP-CLI-03` **todo** |
| requirement-python-version | python | TP-VER-01..03 | Triple SSOT `1.0.7`; debug line **todo** |
| requirement-python-tui | python | TP-TUI-01..06 · TP-OOP-03 | Default TUI style. Session is class `Tui`. Frame is class `MenuPainter`. `TP-OOP-03` **have**. Menu 7 shows `Hello.`. Menu **8** opens self-management (`TP-TUI-06` **have**) |
| requirement-python-about | python | TP-ABOUT-01..10 | About page lines and the read for each line. `TP-ABOUT-09` and `TP-ABOUT-10` are the pyenv paths (`requirement-python-pyenv`) |
| requirement-python-pyenv | python | TP-ABOUT-09 · TP-ABOUT-10 | Under pyenv, python2 and python3 stay inside the root. pyenv location is `bin/pyenv`. Not under pyenv, the three lines stay on `shutil.which` |
| requirement-python-coding-style | python | TP-FS-01..02 · TP-FS-05 · TP-DOC-02 · TP-STYLE-01 · TP-PKG-01 · TP-OOP-03 · TP-OOP-04 | `shutil.move`; no import-time version `raise`. Identity locals inside `main()` (**TP-STYLE-01** todo). One class per file is **TP-OOP-03** / **TP-OOP-04** have |
| requirement-python-oop | python | TP-OOP-01 · TP-OOP-02 · TP-OOP-03 · TP-OOP-04 · TP-LOG-05 · TP-TUI-01..06 · TP-ABOUT-01..08 | One class per file. `def main` stays in `cli.py`. `SelfManage` owns the pip verbs. Each class `__init__` receives the logger (**TP-LOG-05** have). **TP-OOP-01**, **TP-OOP-02**, **TP-OOP-03**, and **TP-OOP-04** have |
| requirement-python-packaging | python | TP-PKG-* | Manifest + version dual SSOT |
| requirement-python-build-script | python | TP-BUILD-01..06 | `./build.sh` verbs. `test-install` reads the project name. Real wheel build (TP-BUILD-05) **todo** |
| requirement-python-json-output | python | TP-JSON-01..05 | `--json` one object; menu stays closed |
| requirement-python-dependency-management | python | TP-DEP-01..04 | Headless OpenCV `>=5.0.0.93`; ChronicleLogger `>=1.3.1` |
| requirement-python-cli-logging | python | TP-LOG-01..07 | ChronicleLogger in `main`, passed into every class. Each object logs `instantiated` (**TP-LOG-05**). A major file operation logs the operation and the paths (**TP-LOG-06** todo). Thread creation and thread operations log before the call that can block (**TP-LOG-07** todo; the ship unit creates no threads). A non-TUI, non-JSON run shows `debug mode` when `DEBUG` is on (**TP-LOG-03** todo) |
| requirement-python-graceful-exit | python | TP-EXIT-01 · TP-EXIT-02 | Control-C during a long child stops the group, does not publish, and exits 130. Both proofs **todo**. Not in the ship unit yet |
| requirement-python-project-structure | python | TP-STRUCT-01 | src layout; ship SSOT |
| requirement-python-error-handling | python | TP-ERR-* · TP-CLI-04..05 | Fail closed; source safe |
| requirement-runtime-prerequisites | runtime | TP-PRE-* | FFmpeg + OpenCV honesty |

**Absent by design (no TP Core):** shell online-install, `curl|sh` remote self-management, automatic channel checksum, Type 1 sudoers elevation. Python self-management is present: `TP-SELF-01` and `TP-TUI-06`. `version-check` and `self-update` call pip.
