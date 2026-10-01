# Lessons — VideoSpeed

Durable failure modes. **Always re-check on product review.**

| ID | Mode | Prevention | Status |
|----|------|------------|--------|
| L-XDEV-01 | Bare `os.replace` / `os.rename` from system temp → USB/other mount fails (`EXDEV`) or looks like “file not found” after cleanup | Stage temps near final output; publish with **`shutil.move`** only (`promote_file`); `requirement-python-coding-style` · `requirement-video-ffmpeg-pipeline`; **TP-FS-01**, **TP-FS-02** | closed (have) |
| L-SRC-01 | Pipeline overwrites or deletes user source media | Source is read-only input; temps + final beside source; never final path = source; **TP-FFMPEG-04** | open watch (encode skip) |
| L-ATEMPO-01 | Single `atempo` outside 0.5–100 breaks extreme length % | Chained `_atempo_filters`; ratio hard-bound 20–200%; **TP-FFMPEG-02** | open watch (encode skip) |
| L-IMPORT-01 | Package import pulls heavy deps (`cv2`) so `--version` / import fails without OpenCV | Lazy OpenCV import; `__init__.py` version-only; **TP-PKG-01**, **TP-CLI-02** | closed (have) |
| L-FFMPEG-01 | Missing `ffmpeg` on PATH → mid-job cryptic failure | `ensure_ffmpeg` preflight; `requirement-runtime-prerequisites`; **TP-PRE-01** | closed (have) |
| L-RANGE-01 | Invalid cut range still reaches encode | Re-prompt / fail closed before `cut_clip`; **TP-ERR-01** | closed (have) |
| L-DUAL-01 | Root `cli-new.py` or bootstrap archive treated as ship SSOT | Ship SSOT = `src/VideoSpeed/cli.py`; launcher thin re-export only; **TP-STRUCT-01** | closed (have) |
| L-DOCS-01 | README/CHANGELOG claim drift (version, layout, template heritage) | Align user docs with REQs before release claims; **TP-DOC-01** | closed (have) |
| L-TEST-01 | No automated suite → regressions (USB, range, entry) silent | Implement `tests/` against `reviews/test-plan.md`; close TP **todo** → **have** | closed (have) |
| L-TUI-01 | Menu tests import a sibling painter, or `cli.py` draws its own frame glyphs | Draw with `src/VideoSpeed/menu.py`; keep `FRAME_TOP_LEFT` out of `cli.py`; do not declare a menu wheel; `requirement-python-tui`; **TP-TUI-01** … **TP-TUI-04** | closed (have) |

**Intentionally out of scope for default lessons:** shell online install Type O, Type 1 sudoers elevation (product has neither).
