**file**: docs/requirements/requirement-class-software-dev.md  
**Status**: Active (Version 1.0.18 – VideoSpeed software-development class law + residual stack)  
**Area**: class  
**Key**: `requirement-class-software-dev`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Declare this workspace as a **software-development** project class and hold the **residual collection** of software-engineering stack facts **not already owned** by more specific Active peer requirements: primary language, toolchain policy, package/build tooling, and runtime OS family.

This file is **class law + residual SSOT**, not a second copy of domain video features, FFmpeg pipeline ops, CLI surface, packaging tables, or error-handling tables (those stay on peer requirements).

### 1.1 Human-facing

**In one sentence:** This file says VideoSpeed is a shippable Python program (not a blank template and not a server-admin project) and records leftover stack facts that no other requirement owns.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Maintainer writing or reviewing product law | Open this file when asking “what class is this repo?” |
| The other role | Peer requirements that own cut, CLI, packaging | Domain and pipeline files, not this residual dump |
| Not this file | Encode filters, prompt text, pip metadata tables | Those live on the matching peer requirement |

| Includes | Excludes |
|----------|----------|
| Class membership; Python/CPython residual; dest approver/fences considered-none | FFmpeg filter graphs; interactive prompt copy |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/VideoSpeed/` | ship package | live behavior |
| `video-speed --help` | command | listed flags |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Confirm class | You are maintaining a Python package, not wiping to a template. Dest approval is none. | Read this file’s Implementation Notes |

---

## 2. Core Rules (Mandatory)

### 2.0 Project class membership

1. **MUST** treat this workspace as **software-development** (shippable software), not genesis-template and not server-maintenance.  
2. **MUST** use basename **`requirement-class-software-dev.md`** as the sole Active class-law file for this class.  
3. **MUST NOT** register an Active `requirement-class-server-maintenance.md` while class is software-development.  
4. **MUST** retain portable harness knowledge when present; specialized product knowledge lives in this and peer `requirement-*.md` files.  
5. **MUST** apply software-development SSOT/gate posture when claimed (identity, package ship surface, precommit when git is used — as applicable).  
6. **MUST NOT** invent hollow product docs solely to look specialized; collect real values or defer explicitly.

### 2.1 Residual collection principle (SSOT hygiene)

7. **MUST** treat this file as the **default home** for software-stack facts **not owned** by another Active requirement.  
8. **MUST NOT** duplicate full normative tables that already live in a more specific Active requirement. Prefer a **one-line pointer** to the peer requirement key.  
9. When a new specialized requirement **takes ownership** of a topic previously only listed here, **MUST** update this file in the **same change**: remove or shrink the residual entry and point to the new owner.  
10. **MUST NOT** leave contradictory stack facts across this file and peer requirements.

### 2.2 Programming language(s)

11. **MUST** declare at least one **primary programming language** for the ship unit.  
12. **SHOULD** list secondary languages only when they are real product law.  
13. **MUST** state whether the product is primarily: interpreted, compiled, polyglot, or package-multi-language.  
14. **MUST NOT** freeze a marketing product name as if it were the language name.

### 2.3 Compilers, interpreters, and toolchains

15. **MUST** declare the **target toolchain class** used to build or run the product.  
16. **MUST** state version policy as one of: unconstrained · minimum version · range · pinned.  
17. **SHOULD** record whether cross-compilation is in scope.  
18. **MUST** fail closed in CI/docs claims: do not claim “supports all interpreters” without tests or explicit unconstrained policy.

### 2.4 Project / package / build tools

19. **MUST** declare the **primary project or package tool** used for dependencies and builds.  
20. **MUST** declare how dependencies are resolved when the ecosystem supports lockfiles.  
21. **SHOULD** name the test runner and linter/formatter **classes** when they are project law.  
22. **MUST NOT** require a secret token or private registry password in this file.

### 2.5 Runtime and platform (residual)

23. **MUST** declare the intended **primary runtime/OS family** when not fully owned by another architecture requirement.  
24. **SHOULD** declare minimum CPU/arch support only when it is real product law.  
25. **MUST** separate **developer machine** toolchain requirements from **end-user runtime** requirements when they differ.

### 2.6 No-hardcode / dual policy (class file)

26. **MUST NOT** hard-code a single product/app brand, one org’s production hostname, or personal owner identity as universal core law.  
27. **MUST** put live product name, repo slug, and concrete stack choices in **Implementation Notes** after collection — complete when Status is Active.  
28. **MUST NOT** store secrets, PATs, or toy credentials in this file.

### 2.7 Implementation Notes (this project)

| Field | Value (VideoSpeed) |
|-------|---------------------|
| **Project display name** | VideoSpeed |
| **Project class** | software-development |
| **Class requirement basename** | `requirement-class-software-dev.md` |
| **Primary language(s)** | Python |
| **Language role** | primary only for runtime package under `src/VideoSpeed/` |
| **Execution model** | **interpreted** package (PyPI-style execution project); optional CyMaster/Cython tooling present for packaging experiments, not required for current CLI runtime |
| **Toolchain / interpreter** | CPython |
| **Toolchain version policy** | **range** declared in `pyproject.toml` (`requires-python`); live package claims broad support — agents **MUST** re-verify before advertising specific minor versions as tested |
| **Cross-compile in scope?** | no |
| **Primary project/package tool** | setuptools via PEP 517/621 **`pyproject.toml`** |
| **Lockfile policy** | **not used** as product law (no committed lockfile requirement) |
| **Test runner** | `tests/run.sh` (`python3 -m unittest discover`) |
| **Linter/formatter** | none as project law |
| **Primary runtime / OS family** | multi-OS where Python + FFmpeg + OpenCV bindings run (documented focus: Linux; macOS/Windows when deps exist) |
| **Architectures supported** | any arch with CPython + FFmpeg binary available |
| **Git surface** | used — remote `git@github.com:Wilgat/VideoSpeed` |
| **Ship surface** | installable Python package `VideoSpeed`; console script `video-speed`; module form `python -m VideoSpeed` |
| **Product version SSOT** | `requirement-python-version`: `MAJOR_VERSION`, `MINOR_VERSION`, `PATCH_VERSION` in `src/VideoSpeed/__init__.py`; `__version__` is built from them; `pyproject.toml` `[project].version` **MUST** stay equal |
| **Install mode** | **pip / local package** — not a shell online-install Type 0 product |
| **Type 1 elevation** | **intentionally absent** — no root/sudo product surface |
| **Author contact (non-secret)** | Wilgat Wong · `wilgat.wong@gmail.com` (also in `pyproject.toml`) |

**Residual ownership table:**

| Topic | Owner | Notes |
|-------|-------|--------|
| Project class membership | **this file** | Fixed |
| Primary language + toolchain policy | **this file** | Python / CPython |
| Package/build tool + lockfile | **this file** + `requirement-python-packaging` | packaging owns PEP 621 tables |
| Maintainer `build.sh` verbs | `requirement-python-build-script` | Do not duplicate the verb table |
| `--json` object | `requirement-python-json-output` | One object; do not duplicate the shape |
| Project layout (`src/` package) | `requirement-python-project-structure` | Do not duplicate |
| CLI entry / `main` order | `requirement-python-cli-interface` | Do not duplicate |
| Interactive walk vs one job | `requirement-python-interactive-vs-noninteractive` | Mode matrix; do not duplicate |
| Text menu look (default TUI style) | `requirement-python-tui` | Picture stays here. Session is class `Tui`. Frame is class `MenuPainter` (`requirement-python-oop`) |
| About page (identity, host check, star box) | `requirement-python-about` | Line text stays here. Host-check functions are class `CheckSystem` |
| Pyenv root and the python2, python3, and pyenv paths | `requirement-python-pyenv` | CheckSystem reads them. Labels stay on `requirement-python-about` |
| OOP grouping (one class per file) | `requirement-python-oop` | One class per file. `def main` stays in `cli.py`. Each class `__init__` receives the logger. `TP-OOP-01` through `TP-OOP-04` have landed |
| Domain surface (workflow, help framing) | `requirement-domain-videospeed` | Four pillars |
| FFmpeg cut / speed / boomerang ops | `requirement-video-ffmpeg-pipeline` | Ops SSOT |
| Error / fail-closed user messaging | `requirement-python-error-handling` | Do not duplicate |
| Python coding style / file move+temps | `requirement-python-coding-style` | `shutil.move`; no `os.rename` or `os.replace` |
| Host runtime deps (FFmpeg, OpenCV) | `requirement-runtime-prerequisites` | External tools; pip floors point at the dependency requirement |
| Pip dependency version floors | `requirement-python-dependency-management` | `opencv-python-headless` and `ChronicleLogger` strings |
| Durable system-status logs | `requirement-python-cli-logging` | One ChronicleLogger, including thread create and thread operations; do not duplicate |
| Control-C during a long child | `requirement-python-graceful-exit` | Stop the child, do not publish, exit 130. Do not duplicate |
| Product version integers | `requirement-python-version` | `MAJOR_VERSION`, `MINOR_VERSION`, `PATCH_VERSION`; do not duplicate |
| Public product reviews / TP map | `reviews/` (git-tracked) | what-to-review · test-plan · lessons · reports |
| Shell online install / Type O `curl\|sh` | **intentionally absent** | Not a shell channel product |
| Python self-management | `requirement-python-cli-interface` | `help` and `version` are in the set. `version-check` and `self-update` call pip. No `sudo`, no `curl` |
| Type 1 sudoers / root elev | **intentionally absent** | No elevation law |
| Dest actor / role / subject / approver | **this file** | **Considered — no dest approver** (see §2.8) |
| Dest fence conditions | **this file** | **Considered — no dest fence conditions** (see §2.8) |

### 2.8 Dest actor / approver / fence residuals (considered — none)

VideoSpeed is a **local Type N interactive CLI**. It has **no** dest approval machine, **no** dest inbound queue, and **no** dest Fence rows. Inventing an approver or dest fence so the class set “looks complete” is forbidden.

**Actor / role / subject / approver** (named law table; **None** is valid):

| Actor | Role | Subject | Approver |
|-------|------|---------|----------|
| Human operator | Interactive CLI user | Local MP4 files chosen in-session | **None** — no dest approval machine |

**Dest fence conditions:** **none**. There is no dest approve/reject/review inbound. Dest **MUST NOT** fence rows are not invented here.

---

## 3. Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 2 – Intentional**: Class and stack choices are explicit, not assumed from folder names.  
- **CIAO Principle 5 – SSOT**: Residual stack facts have one home until specialized requirements take ownership.  
- **CIAO Principle 1 – Caution**: Toolchain policies are declared; agents do not invent compilers or online install.  
- **CIAO Principle 21 – Dual Policies**: Portable core; filled Implementation Notes.  
- **CIAO Principle 4 (O) + Principle 20**: Protection Rule against dual stack SSOTs and wrong-class pollution.

---

## 4. Design Principles (CIAO / CIAO-Lite)

- **Caution**: Assume FFmpeg and OpenCV are missing until prerequisites are checked.  
- **Intentional**: Residual collection is deliberate — not a dump of every possible tool.  
- **Anti-fragile**: Packaging SSOT in `pyproject.toml` survives multi-env installs when versions stay consistent.  
- **Over-protect**: Protection rule prevents dual stack SSOTs and genesis/class confusion.

---

## 5. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Delete this file while the workspace remains **software-development** with other Active product requirements.  
2. Rename the specialized basename away from `requirement-class-software-dev.md` without an explicit class-model change.  
3. Hard-code secrets, personal tokens, or production host FQDNs into core rules as universal law.  
4. Duplicate full peer requirement bodies into this residual section.  
5. Leave Implementation Notes as hollow stubs when Status claims Active.  
6. Introduce Active **shell online-install** / `curl\|sh` **self-update** / shell **Type O** install-ensure law without explicit user order. Python `version-check` and `self-update` that call pip are `requirement-python-cli-interface`.  
7. Introduce Active **Type 1** sudoers / root elevation law without explicit user order and elev allowlist tables.  
8. Treat this file as server-maintenance allowlist law, or register an Active server-maintenance class file in parallel.  
9. Invent a second primary language SSOT that contradicts peer Python requirements.

**Violating any of these is considered a critical regression.**

---

## 6. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Sole Active class file is `requirement-class-software-dev.md` |
| AC-2 | Primary language declared as Python with CPython toolchain |
| AC-3 | Package tool declared as setuptools + `pyproject.toml` |
| AC-4 | Residual ownership table points to peer REQs without duplicating full tables |
| AC-5 | Online install and Type 1 elevation marked intentionally absent |
| AC-6 | Registered in `docs/requirements/index.md` with Area `class` |
| AC-7 | Dest approver and dest fence residuals are **considered — none** (no invented dest machine) |

---

## 7. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-python-packaging` | Manifest + entrypoint |
| `requirement-python-project-structure` | Layout |
| `requirement-python-cli-interface` | CLI surface |
| `requirement-python-tui` | Text menu look |
| `requirement-domain-videospeed` | Domain four pillars |
| `requirement-video-ffmpeg-pipeline` | Processing ops |
| `requirement-python-error-handling` | Errors / cleanup |
| `requirement-runtime-prerequisites` | Host tools |
| `requirement-python-cli-logging` | System-status logs |
| `requirement-python-graceful-exit` | Control-C during a long child |
| `requirement-python-version` | Version integer SSOT |
| `requirement-python-build-script` | Maintainer `./build.sh` verbs |
| `requirement-python-json-output` | `--json` object |
| `requirement-python-about` | About page body |
| `requirement-python-pyenv` | Pyenv root and the three location paths |
| `requirement-python-oop` | One class per file. `def main` stays in `cli.py` |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| n/a | — | deferred | Class residual verified by document review + packaging smoke; no dedicated suite yet |

## 8. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial software-dev class law for VideoSpeed |
| 2026-09-30 | Active 1.0.2 | Text menu look owned by `requirement-python-tui` |
| 2026-09-30 | Active 1.0.3 | Pip version floors owned by `requirement-python-dependency-management` |
| 2026-10-01 | Active 1.0.4 | Status logs owned by `requirement-python-cli-logging` |
| 2026-10-01 | Active 1.0.5 | Version integers owned by `requirement-python-version` |
| 2026-10-01 | Active 1.0.6 | Text menu painter is `src/VideoSpeed/menu.py` |
| 2026-10-01 | Active 1.0.7 | Mode matrix owned by `requirement-python-interactive-vs-noninteractive` |
| 2026-10-01 | Active 1.0.8 | `build.sh` verbs owned by `requirement-python-build-script` |
| 2026-10-01 | Active 1.0.9 | `--json` object owned by `requirement-python-json-output` |
| 2026-10-01 | Active 1.0.10 | About page owned by `requirement-python-about` |
| 2026-10-01 | Active 1.0.11 | OOP grouping owned by `requirement-python-oop` (`Tui`, `CheckSystem`) |
| 2026-10-01 | Active 1.0.12 | Painter home is class `Tui` in `tui.py`. Host check is class `CheckSystem` |
| 2026-10-01 | Active 1.0.13 | OOP map is one class per file. `def main` stays in `cli.py`. `TP-OOP-03` and `TP-OOP-04` are todo |
| 2026-10-01 | Active 1.0.14 | `TP-OOP-03` and `TP-OOP-04` have landed. `def main` stays in `cli.py` |
| 2026-10-01 | Active 1.0.15 | Control-C during a long child points at `requirement-python-graceful-exit`. Do not duplicate |
| 2026-10-01 | Active 1.0.16 | Thread create and thread operations stay on `requirement-python-cli-logging`. Do not duplicate |
| 2026-10-01 | Active 1.0.17 | The logger is an `__init__` parameter on `requirement-python-oop`. Do not duplicate |
| 2026-10-02 | Active 1.0.18 | Pyenv root and the python2, python3, and pyenv paths point at `requirement-python-pyenv`. Do not duplicate |

---

**Last Updated**: 2026-10-02  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
