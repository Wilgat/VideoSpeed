**file**: docs/requirements/requirement-domain-videospeed.md  
**Status**: Active (Version 1.0.0)  
**Area**: domain  
**Key**: `requirement-domain-videospeed`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement is the **domain surface Single Source of Truth** for VideoSpeed: which **user-facing video-editing workflow steps** exist, what **features** the product claims, and how **help / about / session messaging** must describe them.

**Operational FFmpeg processing** (cut, speed change, boomerang encode steps, temp cleanup) is **not** fully owned here — it is owned by **`requirement-video-ffmpeg-pipeline`**.  
**CLI entry and interactive session contract** are owned by **`requirement-python-cli-interface`**.

This file remains the sole Active **`requirement-domain-*`** (four pillars).

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

**Routing:** Entry (`video-speed` / `python -m VideoSpeed` / `VideoSpeed.cli:main`) **MUST** reach this interactive domain session unless a future Active requirement adds non-interactive flags.

**Non-goals as domain commands (unless a future requirement adds them):** multi-file batch queue, GUI, non-MP4 containers as first-class inputs, cloud upload, timeline multi-track editor, automatic color grade, root/system install ensure.

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
3. When a future `--help` flag is implemented (CLI peer), it **MUST** list the same capabilities and non-goals.

Help / README domain rows **MUST** include:

| Help row | Text intent |
|----------|-------------|
| Select folder | Folder containing MP4 files (default: current directory) |
| Select video | Choose from numbered list |
| Cut | Start and end time in seconds |
| Speed / length | New length as percent of cut segment (default 100%) |
| Boomerang | Optional forward+reverse effect |
| Output | Written next to source with descriptive name |

### 2.4 Pillar D — Specialized project about items

Product identity / about **MUST** be able to report (via package metadata and/or future `about`/`--version` surface):

| Field / line | Content |
|--------------|---------|
| Product name | VideoSpeed |
| Version | Package version SSOT (`__version__` / `pyproject.toml`) |
| Domain summary | Cut → speed/length → optional boomerang for MP4 |
| Runtime tools | FFmpeg (encode), OpenCV (duration probe) |
| Entry points | `video-speed`, `python -m VideoSpeed` |

**About is not** a remote version-check and **must not** advertise a shell `curl|sh` install channel unless a future install requirement is Active.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Product / package name** | `VideoSpeed` |
| **Console script** | `video-speed` |
| **Domain implementation module** | `src/VideoSpeed/cli.py` |
| **VERSION** | `1.0.5` (align `__init__.py` and `pyproject.toml`) |
| **Input formats (current)** | MP4 only (`*.mp4`, `*.MP4`), recursive under selected folder |
| **Output location** | Same directory as source video |
| **Output name pattern** | `{stem}_cut{start:.1f}-{end:.1f}s_{int(ratio)}pct[_BOOMERANG].mp4` |
| **Ops SSOT** | `requirement-video-ffmpeg-pipeline` |
| **CLI SSOT** | `requirement-python-cli-interface` |
| **Current interaction model** | Interactive prompts by default; `--help` / `--version` supported; length percent hard-bounded 20–200% |

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
5. Claim batch or non-MP4 first-class support without updating this file and peers.

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
| `requirement-python-cli-interface` | Entry + interactive session |
| `requirement-runtime-prerequisites` | FFmpeg / OpenCV presence |
| `requirement-python-error-handling` | Invalid range / missing files |
| `requirement-class-software-dev` | Class residual |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| TP-DOMAIN-01 | manual / future automated | todo | Interactive cut→speed path |
| TP-DOMAIN-02 | manual / future automated | todo | Boomerang output naming |
| TP-DOMAIN-03 | manual / future automated | todo | No MP4 → clear exit |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Domain SSOT for VideoSpeed interactive video editing |

---

**Last Updated**: 2026-08-09  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
