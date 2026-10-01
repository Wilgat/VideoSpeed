**file**: docs/requirements/requirement-domain-videospeed.md  
**Status**: Active (Version 1.1.9)  
**Area**: domain  
**Key**: `requirement-domain-videospeed`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement is the **domain surface Single Source of Truth** for VideoSpeed: which **user-facing video-editing workflow steps** exist, what **features** the product claims, and how **help / about / session messaging** must describe them.

**Operational FFmpeg processing** (cut, speed change, boomerang encode steps, temp cleanup) is **not** fully owned here — it is owned by **`requirement-video-ffmpeg-pipeline`**.  
**CLI entry** is owned by **`requirement-python-cli-interface`**. Which path runs — the menu walk, one job, or a fail-closed stop — is **`requirement-python-interactive-vs-noninteractive`**.

This file remains the sole Active **`requirement-domain-*`** (four pillars).

### 1.1 Human-facing

**In one sentence:** This file lists the editing steps VideoSpeed offers: pick an MP4, cut a time range, change length percent, optionally reverse-and-append (boomerang), write the file next to the source.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person cutting a clip | Interactive walk or `--file` job |
| The other role | Pipeline requirement | How FFmpeg actually encodes |
| Not this file | Install, packaging, root tools | Packaging / runtime files |

| Includes | Excludes |
|----------|----------|
| Workflow steps, feature names, help rows, about fields, output name pattern, batch flag names | Filter graphs; pip metadata |

| Surface | What you open | What for |
|---------|---------------|----------|
| `src/VideoSpeed/cli.py` | ship unit | live behavior |
| `video-speed --help` | command | listed verbs/flags |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Cut and speed one file | `edit` runs the four steps. `list-mp4` only lists. Flags still run one job. | `video-speed edit --file clip.mp4 --start 1 --end 5 --percent 50` |

---

## 2. Core Rules / Requirements (Mandatory)

### 2.1 Pillar A — Specialized CLI surface (workflow steps)

VideoSpeed is an **interactive domain CLI** (not a multi-verb Type 0 shell product). Domain surface **MUST** be expressed as the following ordered session steps after entry:

| Step ID | User action | Inputs | Output / effect | Ops SSOT |
|---------|-------------|--------|-----------------|----------|
| D-01 | Select source folder | path string; empty → current directory | Scan for MP4 files | CLI + domain |
| D-02 | Select video | 1-based index into listed MP4 set | Chosen `Path` to source | CLI + domain |
| D-03 | Show duration | — | Human duration from OpenCV probe | CLI + domain |
| D-04 | Cut segment | start seconds, end seconds | Bounds validated; feed pipeline | `requirement-video-ffmpeg-pipeline` |
| D-05 | Speed / length percent | percent number (default 100) | Feed pipeline | `requirement-video-ffmpeg-pipeline` |
| D-06 | Optional boomerang | y/n (default n) | Feed pipeline | `requirement-video-ffmpeg-pipeline` |
| D-07 | Write result | derived filename | Final MP4 beside source | `requirement-video-ffmpeg-pipeline` |
| D-08 | Repeat | y/n | Loop D-04… or exit | CLI |

**Routing:** Entry (`video-speed` / `python -m VideoSpeed` / `VideoSpeed.cli:main`) **MUST** reach this domain session by the mode matrix in `requirement-python-interactive-vs-noninteractive`: the text menu in `requirement-python-tui` when that matrix says the front board; the verb `edit` when that matrix says the verb; one job when that matrix says non-interactive. The steps below are what edit and the job carry out. `list-mp4` stops after D-01.

**Job flags (also named on `requirement-python-cli-interface`):** `--file`, `--folder`, `--start`, `--end`, `--percent`, `--boomerang`.

**Product verbs (also named on `requirement-python-cli-interface` §2.3a):** `help`, `about`, `hello`, `edit`, `list-mp4`. `edit` runs D-01..D-08. `list-mp4` runs D-01 and stops. It shows the MP4 list. It does not choose one file and it does not encode. On a terminal, a verb that still needs a target asks for the folder first, then for the specific file only when the verb needs one. That order is `requirement-python-interactive-vs-noninteractive` §2.1b. This list is the domain actions. It is not a Type 0 install surface.

**Output switch (not a domain step):** `--json`, owned by `requirement-python-json-output`. It does not add a cut, a percent, or a boomerang.

**Non-goals as domain commands (unless a future requirement adds them):** multi-file queue, GUI, non-MP4 containers as first-class inputs, cloud upload, timeline multi-track editor, automatic color grade, root/system install ensure.

### 2.2 Pillar B — Specialized features (surface map)

| Feature area | Domain role | Full law |
|--------------|-------------|----------|
| MP4 discovery (recursive `*.mp4` / `*.MP4`) | Expose list for selection | this file + CLI |
| Duration probe | Show length before cut | OpenCV via CLI; fail closed on unreadable media |
| Segment cut | User-defined start/end | `requirement-video-ffmpeg-pipeline` |
| Playback length percent / speed | User percent (target range 20–200%) | `requirement-video-ffmpeg-pipeline` |
| Boomerang (forward + reverse concat) | Optional y/n | `requirement-video-ffmpeg-pipeline` |
| Output naming | Deterministic stem from cut + percent + optional `_BOOMERANG` | this file + ops |

Domain **MUST NOT** restate full FFmpeg filter graphs in a second competing SSOT. Pointers and feature catalog only.

### 2.3 Pillar C — Specialized project help items

Because the product is **prompt-driven**, “help” **MUST** be available as:

1. **Session banners / step labels** that name the four domain capabilities: cut, speed/length percent, optional boomerang, output path.  
2. **Product README** domain rows that match this catalog.  
3. `--help` and the verb `help` **MUST** list the same capabilities (cut, length percent, optional boomerang), the product verbs `help`, `about`, `hello`, `edit`, and `list-mp4`, and the job flags `--file`, `--start`, `--end`, `--percent`, `--boomerang`, `--folder`.

Help / README domain rows **MUST** include:

| Help row | Text intent |
|----------|-------------|
| Text menu | On a terminal, numbered rows edit / hello / about / Exit above a three-row rounded input box and a status line (`requirement-python-tui`). **7 hello** shows `Hello.` The same tokens are product verbs, plus `help` and `list-mp4` |
| Select folder | Folder containing MP4 files (default: current directory) |
| Select video | Choose from numbered list |
| Cut | Start and end time in seconds |
| Speed / length | New length as percent of cut segment (default 100%) |
| Boomerang | Optional forward+reverse effect |
| Output | Written next to source with descriptive name |

### 2.4 Pillar D — Specialized project about items

Product identity / about **MUST** be able to report these domain lines. The page that prints them, the host check, the star box, and the read for each value are `requirement-python-about`. This pillar does not restate that procedure.

| Field / line | Content |
|--------------|---------|
| Product name | VideoSpeed |
| Version | Package version SSOT (`__version__` / `pyproject.toml`) |
| Domain summary | Cut → speed/length → optional boomerang for MP4 |
| Runtime tools | FFmpeg (encode), OpenCV (duration probe) |
| Entry points | `video-speed`, `python -m VideoSpeed` |
| Text menu | Default TUI style on a terminal (`requirement-python-tui`; session class `Tui`; frame class `MenuPainter`) |

**About is not** a remote version-check and **must not** advertise a shell `curl|sh` install channel. `version-check` and `self-update` are the pip verbs on `requirement-python-cli-interface`.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Product / package name** | `VideoSpeed` |
| **Console script** | `video-speed` |
| **Domain implementation module** | `src/VideoSpeed/cli.py` |
| **VERSION** | `1.0.7` (`requirement-python-version`: `MAJOR_VERSION` 1, `MINOR_VERSION` 0, `PATCH_VERSION` 7) |
| **Input formats (current)** | MP4 only (`*.mp4`, `*.MP4`), recursive under selected folder |
| **Output location** | Same directory as source video |
| **Output name pattern** | `{stem}_cut{start:.1f}-{end:.1f}s_{int(ratio)}pct[_BOOMERANG].mp4` |
| **Ops SSOT** | `requirement-video-ffmpeg-pipeline` |
| **CLI SSOT** | `requirement-python-cli-interface` (entry); `requirement-python-interactive-vs-noninteractive` (which path runs) |
| **Current interaction model** | Mode matrix in `requirement-python-interactive-vs-noninteractive`. Screen look in `requirement-python-tui`. Length percent 20–200% |
| **Batch sample** | `video-speed --file clip.mp4 --start 1 --end 5 --percent 100` |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Domain surface is explicit (four pillars) and not mixed with full encode law.  
- **Principle 5 – SSOT**: One Active domain file for feature catalog.  
- **Principle 1 – Caution**: Non-goals listed so agents do not invent cloud/GUI scope.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Do not invent a second FFmpeg ops SSOT in domain.  
- **Intentional:** Pillars A–D only; encode details in pipeline requirement.  
- **Anti-fragile:** Clear ownership boundaries reduce drift between README and CLI.  
- **Over-protect:** Keep sole Active domain file; supersede before replace.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Duplicate full FFmpeg filter/command law here once `requirement-video-ffmpeg-pipeline` is Active.  
2. Add online install, cloud upload, or root elevation as silent domain behavior without new requirements.  
3. Create a second Active `requirement-domain-*` without superseding this one.  
4. Drop cut / speed / boomerang from the claimed domain catalog while README still advertises them.  
5. Claim non-MP4 first-class support without updating this file and peers. Drop `--file`/`--start`/`--end` without updating this file and the CLI peer.

**Violating this rule is a critical domain regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Four pillars present (workflow steps, feature map, help framing, about fields) |
| AC-2 | Cut, speed/length percent, and boomerang listed with pipeline peer pointer |
| AC-3 | Output naming pattern documented |
| AC-4 | Non-goals include cloud/GUI/Type 0 shell install unless later law says otherwise |
| AC-5 | Registered as sole Active domain SSOT |
| AC-6 | No competing full FFmpeg ops body (defers to video-ffmpeg-pipeline) |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-video-ffmpeg-pipeline` | **Operational encode SSOT** |
| `requirement-python-cli-interface` | Entry, `main` order, and product verb names |
| `requirement-python-interactive-vs-noninteractive` | Menu walk versus one verb versus one job. Folder, then file |
| `requirement-python-tui` | Menu look; edit / hello / about / Exit |
| `requirement-python-about` | About page body and how each line is read |
| `requirement-runtime-prerequisites` | FFmpeg / OpenCV presence |
| `requirement-python-error-handling` | Invalid range / missing files |
| `requirement-class-software-dev` | Class residual |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| TP-DOMAIN-01 | — | todo | Full encode path needs ffmpeg + fixture |
| TP-DOMAIN-02 | `tests/test_docs.py` | have | About/version identity |
| TP-DOMAIN-03 | `tests/test_cli.py` | have | No MP4 → clear exit (via TP-CLI-04) |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Domain SSOT for VideoSpeed interactive video editing |
| 2026-08-19 | Active 1.1.0 | Batch flags dual-mention; §1.1 |
| 2026-09-30 | Active 1.1.1 | Menu look points at `requirement-python-tui` |
| 2026-10-01 | Active 1.1.2 | Painter is `src/VideoSpeed/menu.py` |
| 2026-10-01 | Active 1.1.3 | Routing points at the mode matrix |
| 2026-10-01 | Active 1.1.4 | `--json` is an output switch, not a domain step |
| 2026-10-01 | Active 1.1.5 | About page body points at `requirement-python-about` |
| 2026-10-01 | Active 1.1.6 | Menu row **7 hello** shows `Hello.` |
| 2026-10-01 | Active 1.1.7 | Product verbs `help`, `about`, `hello`, `edit`, `list-mp4`. `list-mp4` is D-01 only |
| 2026-10-01 | Active 1.1.8 | Text-menu painter is class `Tui` in `src/VideoSpeed/tui.py` |
| 2026-10-01 | Active 1.1.9 | Text-menu session is class `Tui`. Frame is class `MenuPainter`. Domain steps unchanged |

---

**Last Updated**: 2026-10-01  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
