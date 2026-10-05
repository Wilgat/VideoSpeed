**file**: docs/requirements/requirement-python-build-script.md
**Status**: Active (Version 1.1.4)
**Area**: python
**Key**: `requirement-python-build-script`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the contract for the maintainer script `build.sh` at the checkout root. It names every verb the script accepts, what that verb does, and when it must stop. The product people run is still `video-speed`. This script builds, tests, and publishes the package. It does not cut video.

Manifest identity stays on `requirement-python-packaging`. The version integers stay on `requirement-python-version`. Pip floors stay on `requirement-python-dependency-management`. The suite entry stays `tests/run.sh`. `setup.sh` installs the checkout for a local trial. It is not a verb here.

### 1.1 Human-facing

**In one sentence:** A maintainer types `./build.sh` plus one verb to install build tools, replace the installed copy with this checkout, clean, build a wheel, run the suite, or publish.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Maintainer at the checkout | `./build.sh build` |
| The other role | The package manifest and the suite | `pyproject.toml`, `tests/run.sh` |
| Not this file | The `video-speed` menu and job flags | `requirement-python-cli-interface` |

| Includes | Excludes |
|----------|----------|
| The verbs on `./build.sh`, including replacing the installed copy from this checkout, and the one commit-message question | `video-speed` flags such as `--file` |
| sdist and wheel into `dist/`, then an explicit upload | Empty argv uploading or tagging |
| `test` running `tests/run.sh` | A second runner, or `setup.sh` as a verb of this script |

| Surface | What you open | What for |
|---------|---------------|----------|
| `./build.sh` | maintainer script | help when no verb is given |
| `./build.sh test` | test verb | the product suite |
| `./build.sh release` | publish chain | clean, build, upload, tag |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| See the verbs | Help lists operational verbs, then the test verb in its own heading. An unknown verb exits 1 and prints that help. | `./build.sh help` |
| Build artifacts | `build` writes an sdist and a wheel under `dist/`. It does not upload. | `./build.sh build` |
| Run the suite | `test` runs `tests/run.sh` and takes no extra arguments. | `./build.sh test` |
| Replace the installed copy | `test-install` reads the project name from the manifest, removes that pip install when it is present, then installs this checkout. | `./build.sh test-install` |
| Publish | `upload` sends `dist/*`. `tag` creates `v` plus the package version and pushes that tag. `release` and `all` do clean, then build, then upload, then tag. | `./build.sh release` |

## 2. Core Rules (Mandatory)

1. **One dispatcher.** `build.sh` **MUST** be the only maintainer verb router. The first operand **MUST** select exactly one verb. Empty argv, `help`, `-h`, and `--help` **MUST** print help and exit 0. Any other unknown token **MUST** print help and exit 1. The script **MUST NOT** treat those tokens as `video-speed` flags.
2. **Verb catalog.** The live verbs **MUST** be exactly the table below. Help **MUST** list every live verb. The test-purpose verb **MUST** appear under its own heading, apart from operational verbs. Each verb **MUST** also be named on `requirement-python-cli-interface` as a `./build.sh` verb, not as a `video-speed` flag.
3. **Version read.** The script **MUST** read `VideoSpeed.__version__` from the checkout `src` tree (`requirement-python-version`). It **MUST NOT** invent a second triple and **MUST NOT** keep going with the word `unknown`. `version`, `tag`, `release`, and `all` **MUST** exit 1 when that read fails. Help, clean, setup, build, test, test-install, upload, and git **MUST** still be reachable when the read fails, except that `release` and `all` include `tag`.
4. **Operational verbs.** `setup` **MUST** install or upgrade `build` and `twine` for the same `python3` on `PATH`, via `python3 -m pip`. It **MUST NOT** install product runtime wheels and **MUST NOT** be required before `test`. `clean` **MUST** remove generated `build/`, `dist/`, egg-info, and `__pycache__` only, and **MUST** be safe to repeat. `build` **MUST** write an sdist and a wheel into `dist/` and **MUST NOT** upload. `upload` **MUST** upload existing `dist/*` and **MUST NOT** build first. `tag` **MUST** create an annotated tag `v` plus the package version and push that tag. It **MUST NOT** move or delete an existing tag. `release` and `all` **MUST** run `clean`, then `build`, then `upload`, then `tag`, and **MUST** refuse before that chain when the version cannot be read. They **MUST NOT** run `test`.
5. **Test verb.** `test` **MUST** run `tests/run.sh` and **MUST NOT** invoke another runner. Extra arguments **MUST** exit 1 with a next step of `./build.sh test` and **MUST NOT** start the suite.
6. **Git verb.** `git` **MUST** ask for one commit message. On a terminal it **MUST** prompt `Enter commit message:`. With no terminal it **MUST** read one line from stdin and **MUST NOT** wait for a second question. An empty message **MUST** exit 1 and **MUST NOT** commit. A non-empty message **MUST** stage the checkout, commit with that message, and push the current branch. It **MUST NOT** force-push and **MUST NOT** embed a token.
7. **Checkout install verb.** `test-install` is an operational verb. It **MUST** appear with the operational verbs, not under the test-purpose heading. It **MUST** read the distribution name from `[project].name` in the checkout `pyproject.toml`. It **MUST NOT** embed that name, the import package, the console-script name, or a checkout path. When `python3 -m pip show` finds that name, it **MUST** run `python3 -m pip uninstall -y` for that name. When the name is not installed, it **MUST** continue. When that uninstall fails, it **MUST** exit 1 and **MUST NOT** install. It **MUST** then run `python3 -m pip install` of the checkout directory. Extra arguments **MUST** exit 1 and **MUST NOT** call pip. If the name cannot be read, it **MUST** exit 1 and **MUST NOT** call pip. It **MUST NOT** call `setup.sh`, select an interpreter by a fixed version, upload, tag, commit, or run the suite. The rest of this script **MUST NOT** call `setup.sh`, **MUST NOT** open the text menu, and **MUST NOT** encode video.
8. Actor / role / subject / approver: **considered**. No dest machine. No approver. The table stays on `requirement-class-software-dev.md`.
9. Dest fence conditions: **considered — none**. Do not invent one.

### 2.1 Verb table

| Verb | Kind | What it does | Must not |
|------|------|--------------|----------|
| `help` (`-h`, `--help`, empty argv) | operational | Print the verb list. Exit 0 | Upload, tag, or commit |
| `version` | operational | Print the package version from the checkout | Print `unknown` and exit 0 |
| `setup` | operational | `python3 -m pip install --upgrade build twine` | `sudo`; product runtime wheels; OS packages |
| `clean` | operational | Delete generated build leaves | Delete `src/VideoSpeed` or `tests/` |
| `build` | operational | sdist and wheel in `dist/` | Upload |
| `upload` | operational | Upload `dist/*` | Build, tag, or run when argv was empty |
| `git` | operational | One message, then stage, commit, and push | Force-push; a second question; empty message |
| `tag` | operational | Annotated `v<version>` and push that tag | Move an existing tag; run with no version |
| `release` | operational | `clean`, `build`, `upload`, `tag` | Skip the version check; run `test` inside the chain |
| `all` | operational | Same chain as `release` | A different order |
| `test-install` | operational | Read `[project].name`. Uninstall that distribution when present. `python3 -m pip install` this checkout | A hard-coded project name; `setup.sh`; extra arguments; install after a failed uninstall |
| `test` | test-purpose | `tests/run.sh` | Extra arguments; another test runner |

### Sample code

```text
./build.sh
./build.sh help
./build.sh version
./build.sh setup
./build.sh clean
./build.sh build
./build.sh test
./build.sh test-install
./build.sh upload
./build.sh git
./build.sh tag
./build.sh release
./build.sh all
```

### 2.2 Commit message (the `git` verb)

| Field | Secret | Prompt label | Empty means | On failure |
|-------|--------|--------------|-------------|------------|
| Commit message | no | `Enter commit message:` | no default | Exit 1. Do not commit. Do not push |

### 2.3 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Script** | `build.sh` at the checkout root |
| **Dispatcher** | POSIX `case` on the first operand |
| **Version read** | `import VideoSpeed` with the checkout `src` on the module path; print `__version__` |
| **Package name** | `VideoSpeed` |
| **Build command** | `python3 -m build --sdist --wheel --outdir dist/` |
| **Upload command** | `python3 -m twine upload dist/*` |
| **Tag name** | `v` plus `__version__` (today `v1.0.13`) |
| **Suite** | `tests/run.sh` |
| **test-install** | `tomllib` reads `[project].name` from `pyproject.toml` (today `VideoSpeed`). `python3 -m pip show`, then `python3 -m pip uninstall -y` when present, then `python3 -m pip install` of the checkout directory. `read_project_name` and `do_test_install` do not embed that name |
| **Not a verb** | `setup.sh` (pyenv-selected local install). `test-install` does not call it |
| **Publish remote** | The git remote already configured in the checkout. The tag URL family is the repository named on `requirement-python-packaging` |
| **Privilege** | normal user privilege |

### 2.4 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 2 – Intentional** (https://github.com/cloudgen/ciao): Every maintainer verb is named. `all` is the same chain as `release`.
- **CIAO Principle 1 – Caution** (https://github.com/cloudgen/ciao): Empty argv does not upload. A missing version does not tag. `test` does not accept a foreign runner. `test-install` does not guess a project name.
- **CIAO Principle 5 – SSOT** (https://github.com/cloudgen/ciao): This file owns the verb table. Packaging and the product CLI point here.
- **CIAO Principle 16 – Interactive** (https://github.com/cloudgen/ciao): `git` asks one question on a terminal and reads one line when stdin is not a terminal.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, **admin privilege** and **dedicated system user privilege** stay unused. **This requirement:** `./build.sh` **MUST NOT** call `sudo`, wrap `apt` / `dnf`, create a dedicated account, or recommend `sudo pip` or `sudo curl \| sh`. Git Bash and Windows cmd **MUST NOT** invoke Termux `pkg`. Publish verbs still need the operator’s existing credentials. They do not escalate.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Upload, tag, and push run only when that verb was typed.
- **Intentional:** The verb table is the whole router.
- **Anti-fragile:** Help and an unknown token return without publishing.
- **Over-protect (Principle 20):** Do not add a second test runner, do not let `test` arguments fall through into another tool, and do not install when the project name cannot be read.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT:**

- Add a verb that help does not list, or leave a live verb off help.
- Point `test` at a runner other than `tests/run.sh`.
- Upload, tag, or push from empty argv.
- Force-move a git tag or force-push from this script.
- Print `unknown` as a successful version.
- Treat `./build.sh` verbs as `video-speed` flags, or copy their procedures into `requirement-python-cli-interface`.
- Call `sudo` from this script.
- Delete the package tree or the suite during `clean`.
- Hard-code the distribution name, import package, or console-script name inside `test-install`.
- Let the suite run `test-install` against the live interpreter.

## 5. Design-time verification

| ID | Suite | Status |
|----|-------|--------|
| TP-BUILD-01 | `tests/test_build.py` | have |
| TP-BUILD-02 | `tests/test_build.py` | have |
| TP-BUILD-03 | `tests/test_build.py` | have |
| TP-BUILD-04 | `tests/test_build.py` | have |
| TP-BUILD-05 | — | todo |
| TP-BUILD-06 | `tests/test_build.py` | have |

TP-BUILD-01 asserts help (and empty argv) exits 0, lists every verb, and puts `test` under a separate heading. `test-install` stays with the operational verbs. TP-BUILD-02 asserts an unknown verb exits 1 and names the error. TP-BUILD-03 asserts `version` prints the checkout `__version__`. TP-BUILD-04 asserts extra `test` arguments exit 1 without running the suite, and the script calls `tests/run.sh`. TP-BUILD-05 remains a real sdist/wheel build. TP-BUILD-06 asserts `test-install` reads `[project].name`, uninstalls that distribution when present, then pip-installs the checkout, and that the verb text does not embed the name. The suite supplies a stand-in `python3` and does not change the live install.

**Matrix:** `reviews/requirement-test-matrix.md`
**Map:** `reviews/test-plan.md`.

## 6. Related artifacts

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-python-cli-interface.md` | Names these verbs again; they are not `video-speed` flags |
| `docs/requirements/requirement-python-packaging.md` | Manifest the build consumes |
| `docs/requirements/requirement-python-version.md` | Version integers the script reads |
| `docs/requirements/requirement-python-project-structure.md` | Where `build.sh` sits |
| `docs/requirements/requirement-class-software-dev.md` | Approver none; no dest fence |
| `build.sh` | Dispatcher |
| `tests/run.sh` | Suite the `test` verb runs |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-01 | Active 1.0.0 | Maintainer verbs for `build.sh` |
| 2026-10-01 | Active 1.1.0 | `test-install` reads the project name, uninstalls that pip install, then installs this checkout |
| 2026-10-02 | Active 1.1.1 | Sample code shows the `./build.sh` verbs |
| 2026-10-04 | Active 1.1.2 | Tag example is `v` plus package string `1.0.11` |
| 2026-10-05 | Active 1.1.3 | Tag example is `v` plus package string `1.0.12`. This release was not tagged |
| 2026-10-05 | Active 1.1.4 | Tag example is `v` plus package string `1.0.13`. This release was not tagged |

**Last Updated**: 2026-10-05
**Owner**: VideoSpeed project maintainers
**Alignment**: Registry `docs/requirements/index.md`; CIAO (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
