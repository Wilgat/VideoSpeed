**file**: docs/requirements/requirement-python-cli-language.md
**Status**: Active (Version 1.0.1)
**Area**: python
**Key**: `requirement-python-cli-language`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the menu language for VideoSpeed. The person picks one of thirteen languages on the text menu. The choice is stored for the next run. English is the default. The front board’s row **4** opens that board. The words that follow the choice are the ones named in §2.4. Class `LanguageMenu` in `src/VideoSpeed/language_menu.py` owns the codes, the file, and those words. `Tui` writes `LanguageMenu(...)` at the site that needs it. The frame stays on `MenuPainter`. The picture of the box stays on `requirement-python-tui`. `language` is not a product verb and is not an argv token.

### 1.1 Human-facing

**In one sentence:** On the text menu, row 4 is language, and picking a language there changes the menu words for this run and for the next run.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The person at the keyboard | `video-speed`, then `4` |
| The other role | The class that stores the choice and the words | class `LanguageMenu` in `language_menu.py` |
| Not this file | The cut, the percent, the host-check page, and human help | Domain, about, and the CLI interface |

| Includes | Excludes |
|----------|----------|
| Thirteen language codes, front row **4**, and the block **40–59** | A fourteenth language, or a language row outside **40–59** |
| The file under this login’s persistence directory, and `VIDEOSPEED_LANG` at process start | The cache folder, a path under `/var`, and rewriting a bad file |
| Menu words named in §2.4 | Human help, the about host-check page, JSON, argv `version`, and encode output |

| Surface | What you open | What for |
|---------|---------------|----------|
| `video-speed` on a terminal | Text screen | Row **4** opens the language board |
| `{{HOME}}/.local/VideoSpeed/language` | One-line file | The choice for the next run |
| `src/VideoSpeed/language_menu.py` | class `LanguageMenu` | Codes, file, and the words |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Open the language board | Row **4** lists the thirteen languages. Reserved numbers are not printed. | `4` |
| Keep Traditional Chinese | The file gains one line, `zh-Hant`, and the front board comes back in that language. | `4`, then `43` |
| Leave without saving | **0** returns to the front board. The file is unchanged. | `0` |

## 2. Core Rules / Requirements (Mandatory)

Default language is English so an existing menu test keeps matching English words. The other twelve codes are the person’s choice, stored for the next run. Order on the board: English, Simplified Chinese, Traditional Chinese, then the remaining codes by native-speaker count.

### 2.1 Languages

| Code | Name on the language board | Number | Default |
|------|----------------------------|--------|---------|
| `en` | English | **41** | yes |
| `zh-Hans` | 简体中文 | **42** | no |
| `zh-Hant` | 繁體中文 | **43** | no |
| `es` | Español | **44** | no |
| `ar` | العربية | **45** | no |
| `fr` | Français | **46** | no |
| `pt` | Português | **47** | no |
| `ru` | Русский | **48** | no |
| `de` | Deutsch | **49** | no |
| `ja` | 日本語 | **50** | no |
| `ko` | 한국어 | **51** | no |
| `nl` | Nederlands | **52** | no |
| `el` | Ελληνικά | **53** | no |

**MUST** accept only these thirteen codes in this version. The language board uses only numbers **40** through **59**. That block is twenty numbers, so this menu has **not more than 20 languages**. This version assigns thirteen: **41** through **53**. **40** and **54** through **59** are reserved and are not printed. A pick of one of those reserved numbers warns and reprints this board and does not write the file. Front **5** is not a row. **MUST NOT** assign a language row outside **40–59**. **MUST NOT** assign more than twenty language rows. **MUST** treat a missing file, an empty file, or any other first line as English for this process. **MUST NOT** rewrite a file whose first line is not one of these codes. **MUST NOT** add a fourteenth code without a new revision of this file.

The short names **English**, **简体中文**, **繁體中文**, **Español**, **العربية**, **Français**, **Português**, **Русский**, **Deutsch**, **日本語**, **한국어**, **Nederlands**, and **Ελληνικά** are the same words in every language (each language’s own name).

### 2.2 Where the choice is stored

1. The leaf is `{{HOME}}/.local/VideoSpeed/language`, inside the persistence directory `CheckSystem.persistence_storage()` already names (`requirement-python-about`). **MUST NOT** put it in the cache folder. **MUST NOT** put it under `/var/video-speed`.
2. The file is one line, one of the thirteen codes, then a newline. Mode **0600**. A trailing CR is ignored. Only the first line is read.
3. `LanguageMenu` loads that line once, in its constructor, when `Tui` writes `LanguageMenu(...)`. **MUST NOT** load again in that same process: a later load would let `VIDEOSPEED_LANG` cover a pick just saved.
4. When `VIDEOSPEED_LANG` is one of those thirteen codes, that value wins over the file at process start. It does not write the file. A menu pick still writes the file and sets the code for the rest of that process.
5. `save` writes the line and sets the code only after the write succeeds. A code outside the thirteen returns failure and leaves the code unchanged. The save creates the persistence directory, mode **0700**, when that directory is missing. It does not create a cache directory. A failed write leaves the code unchanged.

### 2.3 Menu numbers

Front **4** opens the language board. **41** saves `en`. **42** saves `zh-Hans`. **43** saves `zh-Hant`. **44** saves `es`. **45** saves `ar`. **46** saves `fr`. **47** saves `pt`. **48** saves `ru`. **49** saves `de`. **50** saves `ja`. **51** saves `ko`. **52** saves `nl`. **53** saves `el`. Each is a valid leaf: the line above the box names the language, then the front board redisplays in that language. **0** is Back and does not write the file. An invalid choice warns and reprints this board. Numbers **40** through **59** are the only language rows (not more than 20 languages). **40** and **54** through **59** are reserved and are not printed. Front **5** is not a row.

System-log cannot stay on **4** or on **41**–**43**, because those numbers are this board. Front **6** is system-log. Its children are **61** view-log, **62** clear-log, **63** log-folder, and **0** Back. The picture of those rows stays on `requirement-python-tui`.

The bottom box inserts ASCII. These ASCII tokens open the language board from the front board: `language`, `idioma`, `langue`, `Sprache`, `sprache`, `taal`. The same rows also match these tokens when the typed buffer equals them: `語言`, `语言`, `言語`, `언어`, `لغة`, `язык`, `γλώσσα`. On the language board the ASCII tokens are `english` / `en` / `English`, `simplified-chinese` / `zh-hans` / `zh-Hans`, `traditional-chinese` / `zh-hant` / `zh-Hant`, `spanish` / `es`, `arabic` / `ar`, `french` / `fr`, `portuguese` / `pt` / `portugues`, `russian` / `ru`, `german` / `de` / `Deutsch` / `deutsch`, `japanese` / `ja`, `korean` / `ko`, `dutch` / `nl` / `Nederlands` / `nederlands`, `greek` / `el`. The endonym of each row matches as well when the buffer equals it.

`language` is not an argv verb.

Row **4** is numbered on every host, including Termux, Git Bash, and Windows cmd.

### 2.4 What follows the saved language

**MUST** follow the code on these boards: front, language, system-log, and self-management. That covers the layer title, the category shorts (`language`, `system-log`, `self-management`), the long description of those three rows, Back, Exit, the path label, and the unknown-choice line.

**MUST** keep each leaf short as the English verb in every language (`edit`, `view-log`, `clear-log`, `log-folder`, `version`, `about`, `version-check`, `self-update`, `self-uninstall`, `self-install`). A leaf explain on the self-management board and on the system-log board stays the English sentence already printed for that row. The language-board explain follows the code. English language-board explains are the lines in the sample below. The other twelve UI languages use the matching sentence stored on `LanguageMenu`.

**Stays English in this version** (this scope, not a missing sentence): human `help`, the about host-check page (`requirement-python-about`), JSON keys and JSON values, argv `version`, operational encode output, the folder path, the clock, and the result-page title `result`.

The unknown-choice line in English stays `That choice is not on this list. Pick a listed number.` The other codes use their own sentence on `LanguageMenu`. The line sits above the box. It does not exit the process.

After a successful save the line above the box is printed in the language just saved, and the front board is already in that language:

| Code | Saved |
|------|--------|
| `en` | `Menu language is English` |
| `zh-Hans` | `菜单语言是简体中文` |
| `zh-Hant` | `選單語言是繁體中文` |
| `es` | `El idioma del menú es español` |
| `ar` | `لغة القائمة هي العربية` |
| `fr` | `La langue du menu est le français` |
| `pt` | `O idioma do menu é português` |
| `ru` | `Язык меню — русский` |
| `de` | `Die Menüsprache ist Deutsch` |
| `ja` | `メニューの言語は日本語` |
| `ko` | `메뉴 언어는 한국어` |
| `nl` | `De menutaal is Nederlands` |
| `el` | `Η γλώσσα του μενού είναι ελληνικά` |

A failed write warns in the language that was current before the failed write, leaves the code unchanged, and still returns to the front board:

| Code | Failed write |
|------|----------------|
| `en` | `Could not save the menu language` |
| `zh-Hans` | `无法保存菜单语言` |
| `zh-Hant` | `無法儲存選單語言` |
| `es` | `No se pudo guardar el idioma del menú` |
| `ar` | `تعذر حفظ لغة القائمة` |
| `fr` | `Impossible d'enregistrer la langue du menu` |
| `pt` | `Não foi possível guardar o idioma do menu` |
| `ru` | `Не удалось сохранить язык меню` |
| `de` | `Die Menüsprache konnte nicht gespeichert werden` |
| `ja` | `メニューの言語を保存できませんでした` |
| `ko` | `메뉴 언어를 저장하지 못했습니다` |
| `nl` | `De menutaal kon niet worden opgeslagen` |
| `el` | `Δεν ήταν δυνατή η αποθήκευση της γλώσσας του μενού` |

Back and Exit:

| Code | Back | Exit |
|------|------|------|
| `en` | `Back` | `Exit` |
| `zh-Hans` | `返回` | `离开` |
| `zh-Hant` | `返回` | `離開` |
| `es` | `Atrás` | `Salir` |
| `ar` | `رجوع` | `خروج` |
| `fr` | `Retour` | `Quitter` |
| `pt` | `Voltar` | `Sair` |
| `ru` | `Назад` | `Выход` |
| `de` | `Zurück` | `Beenden` |
| `ja` | `戻る` | `終了` |
| `ko` | `뒤로` | `종료` |
| `nl` | `Terug` | `Afsluiten` |
| `el` | `Πίσω` | `Έξοδος` |

Path label (the folder and the clock stay as they are):

| Code | Label |
|------|--------|
| `en` | `Path` |
| `zh-Hans` | `路径` |
| `zh-Hant` | `路徑` |
| `es` | `Ruta` |
| `ar` | `المسار` |
| `fr` | `Chemin` |
| `pt` | `Caminho` |
| `ru` | `Путь` |
| `de` | `Pfad` |
| `ja` | `パス` |
| `ko` | `경로` |
| `nl` | `Pad` |
| `el` | `Διαδρομή` |

Before the write, when a logger is present, `save` **MUST** call `log_message` with `save language path=<path>`, component `menu`. The call **MUST NOT** sit inside `isDebug()`.

### 2.4.1 Worked samples

English front board, then the language board. Reserved **40** and **54**–**59** are not printed. The box and the status line stay on `requirement-python-tui`.

```text
1. edit           : cut, speed, and optional boomerang
4. language       : display language for this menu
6. system-log     : view, clear, and the log folder
8. self-management: version, about, and pip lifecycle
9. Exit           : leave
```

```text
41. English   : use English for this menu
42. 简体中文  : use Simplified Chinese for this menu
43. 繁體中文  : use Traditional Chinese for this menu
44. Español   : use Spanish for this menu
45. العربية   : use Arabic for this menu
46. Français  : use French for this menu
47. Português : use Portuguese for this menu
48. Русский   : use Russian for this menu
49. Deutsch   : use German for this menu
50. 日本語    : use Japanese for this menu
51. 한국어    : use Korean for this menu
52. Nederlands: use Dutch for this menu
53. Ελληνικά  : use Greek for this menu
 0. Back      : return to the main menu
```

Traditional Chinese (`zh-Hant`) front board after **43**. Leaf shorts and leaf explains stay English. The path word is `路徑`. The column pad is display columns. Wide and Fullwidth count as two. Ambiguous stays one. `系統日誌` and `自我管理` are eight columns, the same width as the longest short on this board, so they have no space before the colon. `edit`, `語言`, and `離開` are four columns and take four spaces. The screen proof is `TP-TUI-13` on `requirement-python-tui`.

```text
1. edit    : cut, speed, and optional boomerang
4. 語言    : 這個選單的顯示語言
6. 系統日誌: 檢視、清空，以及日誌資料夾
8. 自我管理: 版本、關於，以及 pip 生命週期
9. 離開    : 離開
```

11. Actor / role / subject / approver: **considered**. No dest machine. No approver. The table stays on `requirement-class-software-dev.md`. This file does **not** add an actor requirement.
12. Dest fence conditions: **considered — none**. Do not invent one.

### 2.5 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| **Class** | `LanguageMenu` in `src/VideoSpeed/language_menu.py` |
| **Construct** | `Tui` writes `LanguageMenu(...)` and passes the same logger |
| **App name** | `VideoSpeed` |
| **File** | `{{HOME}}/.local/VideoSpeed/language` |
| **Env** | `VIDEOSPEED_LANG` |
| **Front row** | **4** language. Front **5** is not a row |
| **Assigned** | **41** `en` through **53** `el` |
| **Reserved** | **40** and **54**–**59**, not printed |
| **System-log** | Front **6**, children **61** view-log, **62** clear-log, **63** log-folder |
| **Proof** | `TP-LANG-01` in `tests/test_tui.py` |

### 2.6 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 2 – Intentional** (https://github.com/cloudgen/ciao): The language is a named row, a named file, and a closed list of codes. A later edit cannot invent a fourteenth code or a second file.
- **CIAO Principle 5 – SSOT** (https://github.com/cloudgen/ciao): One class owns the codes and the words. The painter does not detect a language.
- **CIAO Principle 16 – Interactive** (https://github.com/cloudgen/ciao): The choice is a menu row. It is not an argv verb, so a script does not hang waiting for it.
- **CIAO Principle 21 – Dual policies** (https://github.com/cloudgen/ciao): The number block is the claimed menu. The picture of the box stays on `requirement-python-tui`.
- **CIAO Principle 22 – File modes** (https://github.com/cloudgen/ciao): The language file is mode **0600**. The persistence directory created for that file is mode **0700**.

## Under command line for normal user only

The language file lives under this login’s home. **This requirement:** saving a language **MUST NOT** call `sudo`, wrap `apt` / `dnf`, create a dedicated account, or recommend `sudo`. Git Bash and Windows cmd **MUST NOT** invoke Termux `pkg`. Row **4** stays numbered on that class. Changing language does not change who may run a verb.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** A missing, empty, or unrecognized file is English for this process and is not rewritten.
- **Intentional:** Thirteen codes, twenty numbers, front row **4**.
- **Anti-fragile:** `VIDEOSPEED_LANG` can force a language for one process without deleting the file.
- **Over-protect (Principle 20):** Do not add a fourteenth code, do not store the file in the cache folder, and do not let the painter pick a language by itself.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

- Add a fourteenth language code without a new revision of this file.
- Assign a language row outside **40–59**, or assign more than twenty language rows.
- Print reserved **40** or **54**–**59**, or make front **5** a row.
- Put system-log back on **4** or on **41**–**43**. Those numbers are the language board. System-log stays on **6** / **61**–**63**.
- Store the language file in the cache folder or under `/var/video-speed`.
- Rewrite an unrecognized language file on load.
- Load again after a menu pick in the same process.
- Set the code when the write failed.
- Make `language` an argv verb.
- Translate leaf shorts, human help, the about host-check page, JSON, argv `version`, encode output, the folder path, or the clock.
- Detect the language inside `MenuPainter`. The caller passes the path word.
- Construct `LanguageMenu` from a factory. `Tui` writes `LanguageMenu(...)`.
- Treat a code-point count as the screen column of a wide short. The pad in the samples below is display columns. Wide and Fullwidth count as two. Ambiguous stays one. The screen proof is `TP-TUI-13` on `requirement-python-tui`.

## 5. Definition of done

1. Front **4** opens the language board. **41**–**53** are the thirteen codes in the order above. **40** and **54**–**59** are not printed.
2. A pick writes `{{HOME}}/.local/VideoSpeed/language` mode **0600** and the front board uses that language.
3. **0** does not write. A reserved number warns and does not write.
4. A missing, empty, or unrecognized file is English and is not rewritten.
5. `VIDEOSPEED_LANG` set to one of the thirteen codes shows that language even when the file says `en`, and does not write the file.
6. A failed write keeps the previous language and shows that language’s failed-write sentence.
7. `TP-LANG-01` asserts the joined lines in this file. `TP-TUI-13` on `requirement-python-tui` asserts the screen columns. `TP-TUI-11` asserts system-log on **6** / **61**–**63**.

### Design-time verification

| TP family / ID | Suite | Status |
|----------------|-------|--------|
| **TP-LANG-01** front **4**, block **40–59** (assigned **41–53**), file, unrecognized line, `VIDEOSPEED_LANG`, saved line | `tests/test_tui.py` | have |
| **TP-TUI-11** system-log on **6**, children **61**–**63** | `tests/test_tui.py` | have |

## 6. Related artifacts

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry SSOT |
| `docs/requirements/requirement-python-tui.md` | Menu picture. Row **4** is language. Row **6** is system-log |
| `docs/requirements/requirement-python-oop.md` | `LanguageMenu` is one class in its own module. `Tui` writes `LanguageMenu(...)` |
| `docs/requirements/requirement-python-about.md` | Persistence directory. The about page stays English |
| `docs/requirements/requirement-class-software-dev.md` | Dest approver considered — none |
| `src/VideoSpeed/language_menu.py` | The class |
| `src/VideoSpeed/tui.py` | Constructs `LanguageMenu` and opens row **4** |

**Last Updated**: 2026-10-04
**Owner**: VideoSpeed project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-04 | Active 1.0.0 | Front **4** is language. Block **40–59**, assigned **41–53**. System-log moves to **6** / **61**–**63**. `TP-LANG-01` has |
| 2026-10-04 | Active 1.0.1 | The column pad in the samples is display columns. Wide and Fullwidth count as two. Ambiguous stays one. The screen proof stays `TP-TUI-13` |
