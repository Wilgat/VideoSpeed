**file**: docs/requirements/requirement-python-readme.md
**Status**: Active (Version 1.0.3)
**Area**: python
**Key**: `requirement-python-readme`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file owns the product user document at the repository root: which sections it has, which pictures it embeds, and the rule that a sentence in that document matches the requirement that owns the behavior. Project nature is a program a person builds and runs from a terminal. The menu picture stays on `requirement-python-tui`. The thirteen languages stay on `requirement-python-cli-language`. The verbs stay on `requirement-python-cli-interface`. The encode stays on `requirement-video-ffmpeg-pipeline`. The domain rows stay on `requirement-domain-videospeed`. The prerequisite table stays on `requirement-runtime-prerequisites`. The package name, the console script, and `setup.sh` stay on `requirement-python-packaging`. The version string stays on `requirement-python-version`. This file does not restate those bodies.

### 1.1 Human-facing

**In one sentence:** You open the root user document to install the program, read how the menu works, and see pictures of the language list, a short boomerang of the sample clip, self-management, and about. Project nature: a program you build and run from a terminal.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The person reading how to run the program | Open `README.md` at the checkout root |
| The other role | The requirements that own the menu, the encode, and the package | A sentence here matches those files |
| Not this file | The cut itself, the language file, and the host-check procedure | Pipeline, language, and about |

| Includes | Excludes |
|----------|----------|
| Section order, badges, install sentences, and the picture catalog | A second menu, a second verb list, or a second encode order |
| Relative links to captures of the running text menu | A generated drawing that invents row text |
| The rule that a named setup script exists, and that a wheel example uses the name the build writes | A shell online install, or root as the documented path |

| Surface | What you open | What for |
|---------|---------------|----------|
| `README.md` | Root user document | Install, usage, pictures |
| `screenshots/` | Picture folder beside that document | The links in the Screenshots section |
| `video-speed` | The program on a terminal | What those pictures show |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Read the install | The public path is pip. The document does not ask for root. | `pip install VideoSpeed` |
| Check the pictures | Row 4 is the language list. The sample clip is a boomerang from 0 to 2 seconds. About stays in English. | `video-speed`, then `4`, or edit `sample-videos/video-1.mp4` |
| Check the version line | The badge matches the package string. | `video-speed --version` |

## 2. Core Rules / Requirements (Mandatory)

The user document is how a person learns the program. It is not a second copy of product law. A claim in the document matches the requirement that owns that claim.

### 2.1 Where it lives

1. **MUST** keep the user document at the repository-root `README.md`. Product law stays under `docs/requirements/`. The layout rule that the file exists is `requirement-python-project-structure`. This file owns the sections and the pictures.
2. Pictures **MUST** live in a `screenshots/` folder at that same root. The user document **MUST** link every PNG in that folder, with a relative path. A PNG on disk and absent from `README.md` fails this file.
3. **MUST NOT** freeze a session login or a `/home/<login>/` path in this requirement or in a sentence that is law. A picture may show the directory where that capture was started. The sentence in the document names “the current directory.”

### 2.2 What the document contains

The document **MUST** keep the sections in §2.5, in that order. A new heading, a dropped heading, or a reordered heading is a revision of this file.

Each behavioral sentence **MUST** match its owner and **MUST NOT** restate that owner’s procedure:

| Claim in the document | Owner |
|-----------------------|--------|
| Cut, length percent, boomerang, output name | `requirement-domain-videospeed` and `requirement-video-ffmpeg-pipeline` |
| Menu picture, path row, clock, row numbers | `requirement-python-tui` |
| Thirteen languages and what stays English | `requirement-python-cli-language` |
| Product verbs and pip lifecycle commands | `requirement-python-cli-interface` |
| Menu walk versus one job versus fail-closed | `requirement-python-interactive-vs-noninteractive` |
| `--json` is one object and the menu stays closed | `requirement-python-json-output` |
| Package name, console script, wheel name, `setup.sh` | `requirement-python-packaging` |
| `MAJOR_VERSION` / `MINOR_VERSION` / `PATCH_VERSION` | `requirement-python-version` |
| Pip floors | `requirement-python-dependency-management` |
| `./build.sh` verbs | `requirement-python-build-script` |
| FFmpeg on `PATH`, no root auto-install | `requirement-runtime-prerequisites` |
| `shutil.move` for the published file | `requirement-python-coding-style` |
| About page, including that it stays English | `requirement-python-about` |

The first-row sentence in the user document **MUST** name the current directory on the left and a local clock (`HH:MM:SS`) on the right when the row has room. It **MUST NOT** name `Current`, a login, `USER`, `USERNAME`, or `getpass` as that right-hand field. The picture of the row stays on `requirement-python-tui`.

### 2.3 Pictures

1. A menu picture **MUST** be a capture of the running text menu. **MUST NOT** satisfy a menu row with a drawing that invents row text. Every PNG in `screenshots/` **MUST** be linked from the user document. A PNG that is not a menu capture **MUST** be labeled as that file and **MUST NOT** be described as a text-menu capture.
2. The Screenshots section **MUST** show the language list, then one main menu for each supported language in list order, then one worked edit, then self-management, then about, then every other PNG in `screenshots/`.
3. The worked edit **MUST** use the sample clip, the start, the end, the default length percent, and boomerang **y** named in §2.5. The saved name **MUST** sit beside the source. The domain file owns the name pattern. This file owns that one pictured job.
4. The about picture **MUST** stay in English. Leaf shorts in every menu picture **MUST** stay the English verb. That split is `requirement-python-cli-language`.
5. A live-menu capture satisfies this file when it shows the menu the program paints, including a double-width label. This file does not order a padding change.
6. The heading of each picture **MUST** be that file’s basename. The paragraph and the image alt **MUST** be the catalog cells for that file. Those words come from the basename and from what the picture shows: the words on the screen, the characters in the input box, or the scene. A language name alone, or a sentence that only says the file is a picture, fails this file. The paragraph **MUST NOT** freeze a session login or a `/home/<login>/` path. The path row is “the current directory.”

### 2.4 Install honesty

1. The public install path **MUST** be pip. **MUST NOT** document a shell online install, `sudo pip`, or `sudo curl | sh`.
2. When the document names a checkout setup script, that file **MUST** exist at the checkout root and **MUST** do what `requirement-python-packaging` says. **MUST NOT** name a script that is absent.
3. A wheel or sdist example **MUST** use the distribution file name the build writes, and the version token **MUST** match the package version.
4. The prerequisite sentences **MUST** stay aligned with `requirement-runtime-prerequisites`. This file **MUST NOT** copy that table as a second owner.
5. `./build.sh` verbs **MUST** be labeled as maintainer verbs. They are not `video-speed` verbs.

### 2.5 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| **Document** | `README.md` |
| **Pictures** | `screenshots/` |
| **Package** | `VideoSpeed` |
| **Console script** | `video-speed` |
| **Version** | `1.0.11` from `src/VideoSpeed/__init__.py` (`MAJOR_VERSION` 1, `MINOR_VERSION` 0, `PATCH_VERSION` 11). `pyproject.toml` copies that string |
| **Python** | `>=3.11` |
| **License file** | `LICENSE.md` (MIT). The file is present |
| **Homes** | `https://github.com/Wilgat/VideoSpeed` and `https://pypi.org/project/VideoSpeed/` |
| **Sample clip** | `sample-videos/video-1.mp4`, menu file **1** |
| **Pictured job** | start **0**, end **2**, length left at **100%**, boomerang **y** |
| **Pictured output** | `video-1_cut0.0-2.0s_100pct_BOOMERANG.mp4` beside the source |
| **Every PNG** | `README.md` links each PNG under `screenshots/`. `video.png` is linked and is not a menu capture |

**Title:** `VideoSpeed - Cut, speed, and boomerang MP4 clips from the CLI`.

**Badges:** a Version badge whose token is the package string; License MIT; CIAO linked to `https://github.com/cloudgen/ciao`; stars for `Wilgat/VideoSpeed`; Python 3.11+; PyPI `VideoSpeed` linked to `https://pypi.org/project/VideoSpeed/`.

**Opening:** cut a time range, change length as a percent, optional boomerang, menu rows edit / language / system-log / self-management / Exit, FFmpeg encodes, OpenCV probes duration. The role table is the editor, FFmpeg on `PATH`, and not a website, installer, or root tool. The version sentence names `src/VideoSpeed/__init__.py`, the copy in `pyproject.toml`, and the console entrypoint `video-speed`.

**Sections, in order:**

| Heading | What this document must keep | Owner of the behavior |
|---------|------------------------------|------------------------|
| Features | Recursive MP4 discovery. Cut with re-prompt. Length 20–200% with picture and sound kept together. Optional boomerang. Temps beside the output and publish by `shutil.move`. Text menu on the verbs above, with the path and a local clock. Product verbs `help`, `version`, `about`, `hello`, `edit`, `list-mp4`, `self-install`, `version-check`, `self-update`, `self-uninstall` (`self-uninstall` needs `--force`). `Exit` is menu-only. `./build.sh` verbs are not `video-speed` verbs. `--help` / `--version`. No arguments on a terminal opens the menu. A job is `--file` / `--start` / `--end` with optional `--percent` / `--boomerang`. Fail closed when FFmpeg is missing, when prompts need a terminal and there is none, or when percent or boomerang arrives without a job | Peers in §2.2. The path-row sentence is the clock rule in §2.2 |
| Quick Installation | The five subsections below | This table |
| Prerequisites (system) | FFmpeg on `PATH`. Python matches `requires-python` | `requirement-runtime-prerequisites` |
| From PyPI (registry channel) | Package name `VideoSpeed`. Maintainer verbs on `./build.sh`: `help`, `version`, `setup`, `clean`, `build`, `test`, `test-install`, `upload`, `git`, `tag`, `release` (`all` is that same chain). Empty `./build.sh` prints help and does not upload. `pip install VideoSpeed`. The PyPI badge is the live index | `requirement-python-packaging`, `requirement-python-build-script` |
| From a git checkout (development) | `git clone git@github.com:Wilgat/VideoSpeed.git`, then `pip install -e .`. Floors `opencv-python-headless>=5.0.0.93` and `ChronicleLogger>=1.3.1` | `requirement-python-packaging`, `requirement-python-dependency-management` |
| Local pyenv install (testing) | Only while `./setup.sh` exists at the checkout root and runs `pyenv shell 3.14` plus pip into that interpreter, without installing FFmpeg and without root | `requirement-python-packaging` |
| From a local wheel / sdist | After `python -m build` or `./build.sh build`, the example names are the files the build writes for this version | `requirement-python-packaging` |
| Verify | `video-speed --version` and `python -m VideoSpeed --version` | `requirement-python-version` |
| Usage | Path on the left, local clock `HH:MM:SS` on the right. **language** is **4**. **system-log** is **6**, with **61** view-log, **62** clear-log, **63** log-folder. **self-management** is **8**. The verb samples in the document. Edit steps: folder, number, cut, percent default 100 allowed 20–200, boomerang y/n, output next to the source. Non-interactive examples. `--help` / `--version`. Fail closed without a terminal. `--json` is one object and the menu stays closed | `requirement-python-tui`, `requirement-python-cli-language`, `requirement-python-cli-interface`, `requirement-python-interactive-vs-noninteractive`, `requirement-python-json-output` |
| Screenshots | Lead: each heading is the file name, and the paragraph is what that picture shows (the words on the screen, the characters in the input box, or the scene). Package **1.0.11**. The paragraph and the image alt are the catalog below | This file |
| Examples | `cd /path/to/videos`, then `video-speed`, then `--version`, then one shot `--file clip.mp4 --start 1.0 --end 5.0 --percent 100`. Shapes `clip_cut1.0-5.0s_100pct.mp4` and `clip_cut1.0-5.0s_50pct_BOOMERANG.mp4` illustrate the domain pattern. They are not the pictured job | `requirement-domain-videospeed` |
| Platform Compatibility | Linux primary. macOS and Windows when Python, FFmpeg, and OpenCV are present. Local disk and USB. Temps sit beside the final path | `requirement-video-ffmpeg-pipeline`, `requirement-python-coding-style` |
| Related Projects | The GitHub and PyPI links above | This file |
| Contributing | Fork, `pip install -e .` or `./setup.sh` when that file exists, a pull request, and do not strip `shutil.move` | `requirement-python-coding-style` |
| License | MIT, link `LICENSE.md`, and that file exists | `requirement-python-packaging` |
| Last Update | Names the package version. The current line may also name front **4**, front **6**, the path and the clock, and the about fields PID, cache chain, persistence, and TTY. A screenshot sentence is not required | This file for the line. `requirement-python-version` for the string |

**Screenshot catalog, in this order.** Each row is a relative link `screenshots/<file>`. The paragraph and the alt are the words `README.md` prints for that file.

| Order | File | Paragraph | Alt |
|------:|------|-----------|-----|
| 1 | `language-menu.png` | Row **4** has opened the language list. **41 English** is highlighted, with the note “use English for this menu.” The other rows are **42 简体中文**, **43 繁體中文**, **44 Español**, **45 العربية**, **46 Français**, **47 Português**, **48 Русский**, **49 Deutsch**, **50 日本語**, **51 한국어**, **52 Nederlands**, and **53 Ελληνικά**. Each note says to use that language for this menu. **0 Back** says “return to the main menu.” The path label is `Path`, the clock is on the right, and the status line says `language`. VideoSpeed 1.0.11. | Language list, 41 English highlighted |
| 2 | `main-menu-en.png` | English main menu. There is no saved-language line above the box. The path label is `Path`. The rows are **1 edit** “cut, speed, and optional boomerang”, **4 language** “display language for this menu”, **6 system-log** “view, clear, and the log folder”, **8 self-management** “version, about, and pip lifecycle”, and **9 Exit** “leave.” The status line says `main menu`. | English main menu |
| 3 | `main-menu-zh-hans.png` | Simplified Chinese main menu. The line above the box says `菜单语言是简体中文`. The path label is `路径`. The clock’s last digit wraps onto the next line. Row **1** stays `edit`. Row **4** is `语言`, row **6** is `系统日志`, row **8** is `自我管理`, and row **9** is `离开`. The status line says `主菜单`. | Simplified Chinese main menu |
| 4 | `main-menu-zh-hant.png` | Traditional Chinese main menu. The line above the box says `選單語言是繁體中文`. The path label is `路徑`. The clock’s last digit wraps onto the next line. Row **1** stays `edit`. Row **4** is `語言`, row **6** is `系統日誌`, row **8** is `自我管理`, and row **9** is `離開`. The status line says `主選單`. | Traditional Chinese main menu |
| 5 | `main-menu-es.png` | Spanish main menu. The line above the box says `El idioma del menú es español`. The path label is `Ruta`. Row **1** stays `edit`. Row **4** is `idioma`, row **6** is `registro`, row **8** is `autogestión`, and row **9** is `Salir`. The status line says `menú principal`. | Spanish main menu |
| 6 | `main-menu-ar.png` | Arabic main menu. The line above the box says `لغة القائمة هي العربية`. The path label is `المسار`. The row text runs right to left, so the columns do not sit like the English board. Row **1** stays `edit`. The status line says `القائمة الرئيسية`. | Arabic main menu |
| 7 | `main-menu-fr.png` | French main menu. The line above the box says `La langue du menu est le français`. The path label is `Chemin`. Row **1** stays `edit`. Row **4** is `langue`, row **6** is `journal`, row **8** is `autogestion`, and row **9** is `Quitter`. The status line says `menu principal`. | French main menu |
| 8 | `main-menu-pt.png` | Portuguese main menu. The line above the box says `O idioma do menu é português`. The path label is `Caminho`. Row **1** stays `edit`. Row **4** is `idioma`, row **6** is `registo`, row **8** is `autogestão`, and row **9** is `Sair`. The status line says `menu principal`. | Portuguese main menu |
| 9 | `main-menu-ru.png` | Russian main menu. The line above the box says `Язык меню — русский`. The path label is `Путь`. Row **1** stays `edit`. Row **4** is `язык`, row **6** is `журнал`, row **8** is `самоуправление`, and row **9** is `Выход`. The status line says `главное меню`. | Russian main menu |
| 10 | `main-menu-de.png` | German main menu. The line above the box says `Die Menüsprache ist Deutsch`. The path label is `Pfad`. Row **1** stays `edit`. Row **4** is `Sprache`, row **6** is `Systemprotokoll`, row **8** is `Selbstverwaltung`, and row **9** is `Beenden`. The status line says `Hauptmenü`. | German main menu |
| 11 | `main-menu-ja.png` | Japanese main menu. The line above the box says `メニューの言語は日本語`. The path label is `パス`. The clock’s last digit wraps onto the next line. Row **1** stays `edit`. Row **4** is `言語`, row **6** is `システムログ`, row **8** is `自己管理`, and row **9** is `終了`. The status line says `メインメニュー`. | Japanese main menu |
| 12 | `main-menu-ko.png` | Korean main menu. The line above the box says `메뉴 언어는 한국어`. The path label is `경로`. The clock’s last digit wraps onto the next line. Row **1** stays `edit`. Row **4** is `언어`, row **6** is `시스템-로그`, row **8** is `자기관리`, and row **9** is `종료`. The status line says `주 메뉴`. | Korean main menu |
| 13 | `main-menu-nl.png` | Dutch main menu. The line above the box says `De menutaal is Nederlands`. The path label is `Pad`. Row **1** stays `edit`. Row **4** is `taal`, row **6** is `systeemlog`, row **8** is `zelfbeheer`, and row **9** is `Afsluiten`. The status line says `hoofdmenu`. | Dutch main menu |
| 14 | `main-menu-el.png` | Greek main menu. The line above the box says `Η γλώσσα του μενού είναι ελληνικά`. The path label is `Διαδρομή`. Row **1** stays `edit`. Row **4** is `γλώσσα`, row **6** is `αρχείο-καταγραφής`, row **8** is `αυτοδιαχείριση`, and row **9** is `Έξοδος`. The status line says `κύριο μενού`. | Greek main menu |
| 15 | `folder-menu.png` | Edit, first question. The title is `VideoSpeed (1.0.11) – edit`. The page says `Cut → Speed → Optional Boomerang` and `Esc returns to the menu.` The prompt is `Folder (Enter = current):`. The input box contains `sample-videos`. The status line says `edit`. | Folder prompt with sample-videos typed |
| 16 | `file-menu.png` | The folder listing inside edit. The page lists `1. video-1.mp4` and `2. video-2.mp4`, then `Choose video (1–2):`. The input box contains `1`. | Choose video, 1 typed for video-1.mp4 |
| 17 | `tui-input-star.png` | The file name is the start question (`star` for start). The page says `Selected: video-1.mp4` and `Duration: 00:18.042 (18.042s)`, then `Step 1/4 – Cut segment` and `Start seconds (default 0.0):`. The input box contains `0`. | Start seconds, 0 typed |
| 18 | `tui-input-end.png` | End of the cut. The page still shows `Selected: video-1.mp4` and `Duration: 00:18.042 (18.042s)`, then `Start: 0.000s` and `End seconds [18.042]:`. The input box contains `2`. | End seconds, 2 typed |
| 19 | `tui-length.png` | Length question. The page says `Step 2/4 – Resize length (20–200%)` and `New length % [100%]:`. The input box is empty, so the bracketed default **100%** stands. The status line says `edit`. | Length prompt, default 100 percent, box empty |
| 20 | `tui-boomerang-choice.png` | Boomerang question. The page says `Step 3/4 – Add boomerang effect?` and `Make it go forward + backward (y/n) [n]:`. The input box contains `y`. | Boomerang question, y typed |
| 21 | `tui-video-done.png` | The encode has finished. The page says `Saved video-1_cut0.0-2.0s_100pct_BOOMERANG.mp4 – Again? (y/n):`. The input box is empty. | Saved the 0-to-2 boomerang clip |
| 22 | `self-management.png` | Row **8** has opened self-management. **82 version** is highlighted: “show the installed version.” Then **83 about** “version, FFmpeg, and OpenCV”, **84 version-check** “compare this install with pip”, **85 self-update** “upgrade this package with pip”, **86 self-uninstall** “remove this package with pip”, **87 self-install** “install this package with pip”, and **0 Back** “return to the main menu.” The path label is `Path`, and the status line says `self-management`. | Self-management, 82 version highlighted |
| 23 | `tui-about.png` | **about** (83) on the result page. The title is `VideoSpeed (1.0.11) – result`. The page prints `VideoSpeed 1.0.11`, `Domain: Cut → speed/length → optional boomerang for MP4`, `Runtime tools: FFmpeg (encode), OpenCV (duration probe)`, and `Entry points: video-speed, python -m VideoSpeed`. The host check is stamped `2026-10-04 15:05:39.108458` and headed `[CHECK SYSTEM]:`. Visible lines include Python 3.12.11, C Library GCC 13.3.0, Ubuntu 24.04.5 LTS, amd64, the current user, the shell, the Python executable, python2 location, python3 location, conda location, pyenv location, and `Inside docker container: False`. The footer says `Up/Down scrolls this page.` and `Press a key to return to the main menu.` The page stays in English. | About host check, English |
| 24 | `video.png` | A still picture. A woman with long brown hair, in a grey shirt with a small blue mark, sits at a round wooden table and holds a white cup. An open book with a worn cover and a metal clasp lies on the table. Behind her are a beige sofa, a wide window onto trees, a potted plant, and a wooden floor in daylight. | Woman at a table with an open book and a cup |

**Distribution names the build writes for 1.0.11:** `dist/videospeed-1.0.11-py3-none-any.whl` and `dist/videospeed-1.0.11.tar.gz`. The document’s wheel and sdist lines **MUST** use those basenames.

**Open gaps (the document is not corrected in the revision that added this file):**

| Gap | Law | Live `README.md` |
|-----|-----|------------------|
| Path row | The Features sentence names the local clock | The Features bullet still says `Current` plus this login. Usage and Last Update already name the clock |
| Setup script | A named `./setup.sh` exists at the checkout root | Local pyenv install and Contributing name `./setup.sh`. The file is absent. Packaging still describes what it would do |
| Wheel names | Examples use `videospeed-1.0.11-py3-none-any.whl` and `videospeed-1.0.11.tar.gz` | The document prints `VideoSpeed-1.0.11-py3-none-any.whl` and `VideoSpeed-1.0.11.tar.gz` |

`TP-DOC-01` in `tests/test_docs.py` asserts the Version badge token and the string `video-speed --file`. It does not assert headings, picture links, the clock sentence, the setup script, or the wheel basename. `TP-DOC-03` is that remaining check. It stays **todo**. Map: `reviews/test-plan.md`.

### 2.6 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 2 – Intentional** (https://github.com/cloudgen/ciao): The sections and every PNG in `screenshots/` are a named catalog. A later edit cannot drop the language list, leave a PNG unlinked, or swap in a drawing for a menu row.
- **CIAO Principle 5 – SSOT** (https://github.com/cloudgen/ciao): This file owns the document. Behavior stays on the peer that already owns it.
- **CIAO Principle 16 – Interactive** (https://github.com/cloudgen/ciao): The pictures show the text menu a person actually drives, including row **4**, the 0-to-2 boomerang, self-management, and about.
- **CIAO Principle 21 – Dual policies** (https://github.com/cloudgen/ciao): The portable rule is “the document matches its owner.” The VideoSpeed headings and file names live in §2.5.
- **CIAO Principle 4 – Over-protect** (https://github.com/cloudgen/ciao): Do not publish a setup script that is not on disk, or a wheel name the build does not write.

## Under command line for normal user only

The documented install is for this login. **This requirement:** the user document **MUST NOT** tell the reader to use `sudo`, `sudo pip`, `sudo curl | sh`, or a dedicated system account. Git Bash and Windows cmd **MUST NOT** be told to invoke Termux `pkg`. The public install path is pip. A picture does not change who may run a verb.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** An install sentence that names a missing script is a defect, even when an older note described that script.
- **Intentional:** Twenty-four pictures, one pictured job, one section order. Each paragraph is the catalog cell for that file.
- **Anti-fragile:** A new PNG in `screenshots/` becomes a required link in the same change. A non-menu file stays labeled as itself.
- **Over-protect (Principle 20):** Do not let the user document become a second menu, a second verb list, or a second encode procedure.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

- Restate encode order, verb lists, menu numbers, language codes, about fields, JSON shape, or the prerequisite table in this file as a second procedure.
- Replace a capture with a generated image.
- Leave any PNG in `screenshots/` out of `README.md`.
- Describe `screenshots/video.png` as a text-menu capture.
- Caption a picture with only a language name, or with a sentence that does not say what the picture shows.
- Describe the path row’s right side as `Current` or a login.
- Print a wheel or sdist name the build does not write.
- Name `./setup.sh` while that file is absent.
- Add a shell online install, `sudo pip`, or `sudo curl | sh` to the user document.
- Freeze a session login or a `/home/<login>/` path in this file.
- Mark `TP-DOC-03` have before the suite asserts the headings, the picture links, the clock sentence, the setup script, and the wheel basename.
- Treat `./build.sh` verbs as `video-speed` verbs.

## 5. Definition of done

1. `README.md` has the sections in §2.5, in that order.
2. The Version badge token matches the package string.
3. The Screenshots section links every PNG in `screenshots/`, in catalog order, including `video.png`. Each heading is the basename. Each paragraph and each image alt are the catalog cells for that file.
4. The path-row sentence names the local clock.
5. A named `./setup.sh` exists at the checkout root and matches `requirement-python-packaging`.
6. The wheel and sdist examples use `videospeed-1.0.11-py3-none-any.whl` and `videospeed-1.0.11.tar.gz` for this version.
7. `TP-DOC-01` has for the badge and `video-speed --file`. `TP-DOC-03` stays **todo** until the suite asserts the headings, the links, and the three honesty checks.

The Screenshots paragraphs and alts are the live `README.md`. Items 4, 5, and 6 stay open in the gap table. This revision does not change those three sentences.

### Design-time verification

| TP family / ID | Suite | Status |
|----------------|-------|--------|
| **TP-DOC-01** Version badge matches the package string, and `video-speed --file` is in the user document | `tests/test_docs.py` | have |
| **TP-DOC-03** Section headings, the screenshot links, each catalog paragraph and alt, the clock sentence, a named setup script exists, and the wheel example matches the built distribution name | `tests/test_docs.py` | todo |

## 6. Related artifacts

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry SSOT |
| `docs/requirements/requirement-python-project-structure.md` | Root `README.md` exists. Sections and pictures are this file |
| `docs/requirements/requirement-domain-videospeed.md` | Domain rows inside the user document |
| `docs/requirements/requirement-runtime-prerequisites.md` | Prerequisite sentences. That file’s AC-4 |
| `docs/requirements/requirement-python-packaging.md` | Package name, console script, wheel name, `setup.sh` |
| `docs/requirements/requirement-python-version.md` | Package string on the badge and Last Update |
| `docs/requirements/requirement-python-tui.md` | Menu picture and the clock |
| `docs/requirements/requirement-python-cli-language.md` | Row **4** and the thirteen codes. About stays English |
| `docs/requirements/requirement-python-about.md` | About page the picture shows |
| `docs/requirements/requirement-python-cli-interface.md` | Product verbs the document lists |
| `docs/requirements/requirement-class-software-dev.md` | Dest approver considered — none |
| `README.md` | The user document |
| `screenshots/` | The captures |
| `reviews/test-plan.md` | `TP-DOC-01` have. `TP-DOC-03` todo |

**Last Updated**: 2026-10-04
**Owner**: VideoSpeed project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-04 | Active 1.0.0 | User document sections and the twenty-three text-menu pictures. Three live gaps recorded (clock sentence, absent `setup.sh`, capital-V wheel names). `TP-DOC-03` todo. `README.md` not edited |
| 2026-10-04 | Active 1.0.1 | Every PNG in `screenshots/` is a required link. `video.png` is linked and is not a menu capture |
| 2026-10-04 | Active 1.0.2 | Each picture’s heading is its basename. The paragraph is taken from the filename and from what the picture shows |
| 2026-10-04 | Active 1.0.3 | The catalog paragraph and alt for each PNG are the words in the live Screenshots section |
