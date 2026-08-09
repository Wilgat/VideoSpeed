# Test plan — VideoSpeed

Maps **TP-*** coverage to automated or documented checks.  
**Suite entry:** *not present* — target `tests/run.sh` or `pytest` when implemented.  
**Ship unit:** `src/VideoSpeed/cli.py`  
**Last update:** 2026-08-09  
**Last suite run:** none (no suite on disk)

Status: **have** = automated today · **todo** = needed · **manual** = documented human procedure · **n/a** · **skip** (environment)

---

## Baseline coverage

| Area | Status | Evidence |
|------|--------|----------|
| Package import / version without OpenCV | **manual** / compile | `__init__.py` version-only; TP-PKG-01 todo automated |
| `--version` / `--help` | **manual** | argparse path; TP-CLI-02/03 |
| Type N empty argv → interactive | **manual** | requires TTY + media |
| FFmpeg preflight | **manual** | `ensure_ffmpeg` |
| Cut → speed (no boomerang) | **todo** | needs fixture + ffmpeg |
| Boomerang | **todo** | needs fixture + ffmpeg |
| Invalid range fail-closed | **todo** | stdin scripted |
| Length % outside 20–200 rejected | **todo** | |
| USB / cross-FS publish via `shutil.move` | **todo** | TP-FS-*; two temp dirs unit possible without ffmpeg |
| Source file not modified | **todo** | |
| Online install / Type 1 elev | **n/a** | product absent |

---

## TP rows

### TP-PKG (packaging / import)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-PKG-01 | `import VideoSpeed` without `cv2` installed; `__version__` readable | `tests/test_package.py` | packaging · coding-style · L-IMPORT-01 | **todo** |
| TP-PKG-02 | `pyproject.toml` version == `__version__` | `tests/test_package.py` | packaging | **todo** |
| TP-PKG-03 | Console script target `VideoSpeed.cli:main` declared | `tests/test_package.py` | packaging · CLI | **todo** |
| TP-PKG-04 | `python3 -m py_compile` on package modules | `tests/test_package.py` or CI | class / structure | **manual** (pass 2026-08-09 on agent host) |

### TP-CLI (CLI surface)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-CLI-01 | `python -m VideoSpeed --version` exits 0, prints version | `tests/test_cli.py` | CLI interface | **todo** |
| TP-CLI-02 | `video-speed --help` / module `--help` lists usage | `tests/test_cli.py` | CLI interface | **todo** |
| TP-CLI-03 | Empty argv starts interactive session (banner) when TTY fed | `tests/test_cli.py` | CLI · domain | **todo** |
| TP-CLI-04 | No MP4 in folder → clear message, non-success path | `tests/test_cli.py` | CLI · error-handling | **todo** |
| TP-CLI-05 | Invalid video index re-prompts (not crash) | `tests/test_cli.py` | error-handling | **todo** |

### TP-PRE (runtime prerequisites)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-PRE-01 | Missing `ffmpeg` → preflight error, no encode | `tests/test_prereq.py` | runtime-prerequisites · L-FFMPEG-01 | **todo** |
| TP-PRE-02 | Missing OpenCV → clear error on duration probe | `tests/test_prereq.py` | runtime-prerequisites · L-IMPORT-01 | **todo** |

### TP-ERR (error handling)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-ERR-01 | Invalid cut range does not call encode | `tests/test_errors.py` | error-handling · L-RANGE-01 | **todo** |
| TP-ERR-02 | Length % outside 20–200 rejected | `tests/test_errors.py` | domain · pipeline | **todo** |
| TP-ERR-03 | FFmpeg non-zero → job failed message; source intact | `tests/test_errors.py` | error-handling · pipeline | **todo** |

### TP-FS (filesystem / USB / promote)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-FS-01 | `promote_file` uses `shutil.move` (source code or behavior across two dirs) | `tests/test_fs.py` | coding-style · pipeline · L-XDEV-01 | **todo** |
| TP-FS-02 | `staging_dir_for(dest)` returns dest parent when writable | `tests/test_fs.py` | coding-style · pipeline | **todo** |
| TP-FS-03 | Non-boomerang job: final appears on “other mount” simulation (two temp roots) | `tests/test_fs.py` | pipeline AC-7 | **todo** |
| TP-FS-04 | After promote, intermediate source gone or not left as sole copy | `tests/test_fs.py` | pipeline | **todo** |

### TP-FFMPEG (encode pipeline)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-FFMPEG-01 | Cut only (100% speed, no boom) produces output MP4 | `tests/test_pipeline.py` | pipeline · domain | **todo** |
| TP-FFMPEG-02 | Speed 50% and 200% within bounds | `tests/test_pipeline.py` | pipeline · L-ATEMPO-01 | **todo** |
| TP-FFMPEG-03 | Boomerang produces longer/forward+reverse media | `tests/test_pipeline.py` | pipeline · domain | **todo** |
| TP-FFMPEG-04 | Source file byte-identical after job | `tests/test_pipeline.py` | pipeline · L-SRC-01 | **todo** |
| TP-FFMPEG-05 | Output naming pattern matches domain | `tests/test_pipeline.py` | domain | **todo** |

### TP-DOMAIN (domain surface)

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-DOMAIN-01 | Workflow steps cut→speed→optional boom still wired | `tests/test_domain.py` or pipeline | domain | **todo** |
| TP-DOMAIN-02 | About/version identity fields honest | `tests/test_cli.py` | domain pillar D | **todo** |

### TP-STRUCT / TP-DOC

| TP-ID | Intent | Suite (planned) | Primary requirement(s) | Status |
|-------|--------|-----------------|------------------------|--------|
| TP-STRUCT-01 | Ship SSOT is `src/VideoSpeed/cli.py` not bootstrap-old alone | review / path check | structure · L-DUAL-01 | **manual** |
| TP-DOC-01 | README version/install claims vs pyproject | review | packaging · L-DOCS-01 | **todo** (docs drift known) |

### Intentionally n/a

| TP family | Reason |
|-----------|--------|
| TP-ONLINE / TP-CURL | No online install product mode |
| TP-ELEV / TTY privilege traps | No Type 1 elevation claimed |

---

## Rules

1. Closing a **bug** finding updates the matching TP toward **have** (and preferably adds an assertion).  
2. Do not mark TP **have** without a suite assertion (or honest skip/n/a with environment reason).  
3. Do not reintroduce online/elev TP as Core without product-mode change.  
4. Prefer implementing high-risk **TP-FS-*** and **TP-PKG-01** first (no media fixture required for pure unit cases).  
