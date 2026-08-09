# Requirements

Authoritative specialized product law for **VideoSpeed** lives here.

**Current state (2026-08-09):** Specialized **software-development** product. Left genesis. Registry is populated — see `index.md`.

## Product identity (summary)

| Field | Value |
|-------|--------|
| Product / package | `VideoSpeed` |
| Version SSOT | `1.0.5` (`pyproject.toml` + `src/VideoSpeed/__init__.py`) |
| Ship surface | Python package; console script `video-speed` |
| Install mode | **pip / local package** |
| Domain surface | `requirement-domain-videospeed` — four pillars |
| Encode ops | `requirement-video-ffmpeg-pipeline` — cut / speed / boomerang |
| Coding style | `requirement-python-coding-style` — temps + `shutil.move` publish |
| Runtime tools | FFmpeg (system) + OpenCV (pip) |
| Public reviews | `reviews/` — what-to-review, test-plan, lessons, reports |

## Class requirement gate

| Class | Required class file |
|-------|---------------------|
| software-development | `requirement-class-software-dev.md` (**Active**) |
| genesis-template | N/A — this workspace is no longer genesis for product law |

## Purpose

- **Plan** designs work by reading and updating these docs.  
- **Implement** delivers code that **traces** to these requirements.  
- **Review** verifies delivery against requirements and CIAO checklists.

## Layout

| Path | Role |
|------|------|
| `docs/requirements/index.md` | Registry of all requirements — keep in sync |
| `docs/requirements/requirement-*.md` | CIAO-style project requirements |

## Status values

Typical: `draft` · `Active` · `approved` · `in-progress` · `done` · `deprecated` · `superseded`

## Rules

1. Never invent paths — verify on disk.  
2. Class files only via class process; non-class via create-specific process.  
3. Never dump harness inventories into this versioned surface.  
4. Online shell install and Type 1 elevation stay **absent** unless product mode is explicitly changed.  
5. Sole domain SSOT: `requirement-domain-videospeed.md`.
