**file**: docs/requirements/requirement-python-cli-interface.md  
**Status**: Active (Version 1.0.0)  
**Area**: python  
**Key**: `requirement-python-cli-interface`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define the official **command-line entry points**, **empty-argv behavior**, and **interactive session contract** for the VideoSpeed Python package.

Domain step catalog is owned by **`requirement-domain-videospeed`**. Encode ops are owned by **`requirement-video-ffmpeg-pipeline`**.

---

## 2. Core Rules (Mandatory)

### 2.1 Entry points

1. **MUST** expose a console script entry named **`video-speed`** pointing at `VideoSpeed.cli:main` (declared in packaging SSOT).  
2. **MUST** support module execution: **`python -m VideoSpeed`**.  
3. **MUST** keep `main()` as the single runtime entry for the interactive editor session (thin package surface).  
4. **MUST NOT** require root or sudo to run the CLI.

### 2.2 Empty argv / default mode (Type N)

5. **MUST** treat bare invocation (`video-speed` with no args) as **Type N**: start the **interactive domain session**, not Type O online install-ensure.  
6. **MUST NOT** default empty argv to shell channel install or self-update.  
7. Future non-interactive flags **MAY** be added only with Active updates to this file and domain peers.

### 2.3 Interactive session contract

8. **MUST** prompt for source folder (empty → current directory).  
9. **MUST** list discoverable MP4 files with 1-based indices.  
10. **MUST** exit cleanly with a clear message when no MP4 files are found.  
11. **MUST** prompt for video index, cut bounds, length percent, and boomerang choice per domain steps.  
12. **MUST** re-prompt (or loop) on invalid cut ranges rather than encoding garbage.  
13. **SHOULD** offer a “run again” loop after a successful job.  
14. **MUST** print the final output path on success.

### 2.4 Flags (current vs future)

15. **Current product law:** interactive prompts only — no required argparse surface.  
16. When flags are introduced, **MUST** document them in this file’s Implementation Notes and keep domain catalog honest.  
17. Recommended future flags (not required until implemented): `--help`, `--version`, optional non-interactive operands for folder/file/start/end/percent/boomerang.

### 2.5 Output behavior

18. **MUST** print human-readable progress for each pipeline stage.  
19. **SHOULD** route durable diagnostics through ChronicleLogger when logging is wired; **MUST** still emit user-visible errors on failure paths.  
20. **MUST NOT** mix machine-only JSON mode into normal interactive sessions unless a `--json` mode is explicitly implemented and documented.

### 2.6 Non-interactive environments

21. When stdin is not a TTY, interactive prompts **SHOULD** fail closed with a clear message **or** require non-interactive flags once those exist.  
22. Agents **MUST NOT** assume CI can drive the current prompt-only UI without a test harness that feeds stdin.

### 2.7 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Console script** | `video-speed = VideoSpeed.cli:main` |
| **Module entry** | `src/VideoSpeed/__main__.py` → `main()` |
| **CLI module** | `src/VideoSpeed/cli.py` |
| **Empty argv** | Interactive editor banner + prompts |
| **Argparse** | `--help`, `--version` only; bare invoke → interactive |
| **Quiet/JSON flags** | not implemented today |
| **Privilege** | user-level only |
| **Root launcher** | `cli-new.py` thin re-export of package `main` (checkout convenience) |
| **Bootstrap archive** | `src/VideoSpeed/cli.bootstrap-old.py` (pre-specialize body) |
| **Ship CLI SSOT** | `src/VideoSpeed/cli.py` |

### 2.8 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Entry and Type N empty-argv are explicit.  
- **Principle 16 – Interactive awareness**: Prompt UI is declared; CI limits honest.  
- **Principle 5 – SSOT**: One CLI surface for entry contract.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** No MP4 → exit; invalid range → re-prompt.  
- **Intentional:** Interactive default matches product design.  
- **Anti-fragile:** Module + console script dual entry.  
- **Over-protect:** No install-ensure on empty argv.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Change empty argv to Type O online install without explicit user order and new install requirements.  
2. Remove console script or module entry without packaging + docs update.  
3. Bypass domain/pipeline peers by reimplementing encode only in a second ad-hoc script as the “real” product.  
4. Require root to run normal editing.  
5. Leave `cli-new.py` as silent dual SSOT for entry behavior.

**Violating this rule is a critical CLI regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | `video-speed` entry declared in packaging |
| AC-2 | `python -m VideoSpeed` works |
| AC-3 | Empty argv starts interactive session |
| AC-4 | No MP4 → clear exit |
| AC-5 | Invalid cut range does not call encode |
| AC-6 | Success prints output path |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-domain-videospeed` | Domain steps |
| `requirement-video-ffmpeg-pipeline` | Encode |
| `requirement-python-packaging` | Entrypoint declaration |
| `requirement-python-error-handling` | Fail paths |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| TP-CLI-01 | manual | todo | Empty argv interactive |
| TP-CLI-02 | manual | todo | Module entry |
| TP-CLI-03 | manual | todo | No MP4 folder |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial Python CLI interface law |

---

**Last Updated**: 2026-08-09  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
