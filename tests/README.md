# Tests — VideoSpeed

Executable suite for product law. Run from repo root:

```bash
./tests/run.sh
```

or:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

| File | TP families |
|------|-------------|
| `test_package.py` | TP-PKG-01..04 |
| `test_dependencies.py` | TP-DEP-01..04 (OpenCV headless and ChronicleLogger floors) |
| `test_cli.py` | TP-CLI-01, 02, 04, 06, 07 · TP-SELF-01 · TP-MODE-01..03, 06, 07, 08 · TP-OOP-04 |
| `test_json.py` | TP-JSON-01..05 (`--json` one object; no menu) |
| `test_build.py` | TP-BUILD-01..04, TP-BUILD-06 (`./build.sh` verbs; `test-install` uses a stand-in python; no upload) |
| `test_tui.py` | TP-TUI-01..06 · TP-OOP-01 · TP-OOP-03 · TP-ABOUT-08 · TP-MODE-05 · TP-MODE-07 (direct `edit` and `list-mp4` on a fake screen) |
| `test_fs.py` | TP-FS-01, 02, 04 |
| `test_errors.py` | TP-ERR-01, 02 |
| `test_prereq.py` | TP-PRE-01, 02 |
| `test_about.py` | TP-ABOUT-01..07 · TP-ABOUT-09 · TP-ABOUT-10 · TP-OOP-02 |
| `test_docs.py` | TP-DOC-01 · TP-STRUCT-01 · TP-DOMAIN-02 |

FFmpeg encode cases (TP-FFMPEG-*) stay **skip** until `ffmpeg` is on `PATH` and a fixture MP4 is available. Interactive TTY walk (TP-CLI-03 / TP-CLI-05) stays **todo**. One class per file (`TP-OOP-03`, `TP-OOP-04`) is **have**. The text menu (`TP-TUI-*`) drives class `Tui` in `src/VideoSpeed/tui.py` with a fake screen; the frame is class `MenuPainter`. It does not need a real terminal. Last suite run: 2026-10-02, 79 tests, OK, skipped=1 (`TP-PRE-01`, ffmpeg on PATH). `TP-TUI-06` and `TP-SELF-01` are have.
