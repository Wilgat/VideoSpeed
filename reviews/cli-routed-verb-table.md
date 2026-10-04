# Commands you can type — VideoSpeed

**Product:** VideoSpeed  
**Ship unit:** `src/VideoSpeed/cli.py`  
**Dispatcher:** `_dispatch` (the `help` token returns from `main` before JSON)  
**Scan date:** 2026-10-04  
**Mode:** full (no previous table)  
**Counts:** live 9 · not-yet-wired 12 · copied 0 · re-checked 9

Inventory is the dispatcher, not the help text. Dates are the handler comment `Last updated:`. This list is not the who-is-who catalog. Who runs the program stays on `requirement-class-software-dev` (no dest machine, no approver). No separate actor file was added.

## Live

| verb | handler | privilege | last modified date | human-readable |
|------|---------|-----------|--------------------|----------------|
| help | `_verb_help` | you | 2026-10-02 | help: Print this usage. Not a numbered menu row |
| version | `_dispatch` | you | 2026-10-02 | version: Print the installed version. No pip |
| about | `_verb_about` | you | 2026-10-02 | about: Show the about page and do not ask for a folder or a file |
| edit | `_verb_edit` | you | 2026-10-02 | edit: Ask for a folder, then a file, when those are not already named |
| list-mp4 | `_verb_list_mp4` | you | 2026-10-02 | list-mp4: List MP4 files and do not encode |
| self-install | `SelfManage.emit` | you | 2026-10-02 | self-install: python -m pip install VideoSpeed |
| version-check | `SelfManage.emit` | you | 2026-10-02 | version-check: python -m pip index versions VideoSpeed |
| self-update | `SelfManage.emit` | you | 2026-10-02 | self-update: python -m pip install --upgrade VideoSpeed |
| self-uninstall | `SelfManage.emit` | you | 2026-10-02 | self-uninstall: python -m pip uninstall -y VideoSpeed. Needs --force |

## Not yet wired

These tokens are named in law and rejected by `_dispatch`. They are not live commands on `video-speed`.

| verb | handler | privilege | last modified date | human-readable | status |
|------|---------|-----------|--------------------|----------------|--------|
| Exit | — | — | — | Exit: Leave the text menu. It is not a video-speed verb | forbidden |
| exit | — | — | — | exit: Same leave control as Exit. It is not a video-speed verb | forbidden |
| setup | — | — | — | setup: Install this checkout from ./build.sh. It is not a video-speed verb | forbidden |
| clean | — | — | — | clean: Clean the checkout from ./build.sh. It is not a video-speed verb | forbidden |
| build | — | — | — | build: Build the package from ./build.sh. It is not a video-speed verb | forbidden |
| upload | — | — | — | upload: Upload from ./build.sh. It is not a video-speed verb | forbidden |
| git | — | — | — | git: Git step from ./build.sh. It is not a video-speed verb | forbidden |
| tag | — | — | — | tag: Tag from ./build.sh. It is not a video-speed verb | forbidden |
| release | — | — | — | release: Release chain from ./build.sh. It is not a video-speed verb | forbidden |
| all | — | — | — | all: Same chain as release on ./build.sh. It is not a video-speed verb | forbidden |
| test-install | — | — | — | test-install: Reinstall this checkout from ./build.sh. It is not a video-speed verb | forbidden |
| test | — | — | — | test: Run tests/run.sh from ./build.sh. It is not a video-speed verb | forbidden |

`--version` still finishes inside the parser. Empty argv is not a verb. The maintainer token `help` on `./build.sh` is a different program; the product verb `help` is live above.
