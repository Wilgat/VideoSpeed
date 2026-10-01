# Review reports index — VideoSpeed

| Date | Report | Scope | Verdict | Suite |
|------|--------|-------|---------|-------|
| 2026-08-09 | `reports/2026-08-09-product-review-initial.md` | Full product (law + ship unit + reviews bootstrap) | **Revise** (historical) | no suite then |
| 2026-08-19 | this index residual | Close open suggestions from 2026-08-09 | **Pass** Core | `tests/run.sh` green |

## Open summary (living)

| Severity | Count (open) | Themes |
|----------|-------------:|--------|
| bug | 0 | — |
| suggestion | 0 | — |
| nit | 0 | — |

Encode-path TPs remain **skip** until ffmpeg + fixture (not a product-review open issue).

**Living plans:** `what-to-review.md` · `test-plan.md` · `lessons.md` · `requirement-test-matrix.md`

## Residual (2026-08-19)

| Item | State |
|------|--------|
| Issue 1 — no `tests/` | **closed** — `tests/run.sh` Core green |
| Issue 2 — README/CHANGELOG version honesty | **closed** |
| Issue 3 — unused ChronicleLogger | **closed** — dropped from `pyproject.toml`; console-only errors |
| Issue 4 — interactive-only CLI | **closed** — `--file`/`--start`/`--end`/`--percent`/`--boomerang` |
| Issue 5 — bootstrap archive | **closed** (TP-STRUCT-01 have) |
| L-DOCS-01 / L-TEST-01 / L-IMPORT-01 / L-FFMPEG-01 / L-RANGE-01 / L-XDEV-01 / L-DUAL-01 | **closed** (have) |
| REQ §1.1 Human-facing | **closed** — all 9 REQs |
| Pip floors (OpenCV headless, ChronicleLogger) | **closed** — `requirement-python-dependency-management`; TP-DEP-01..04 |
| TP-FFMPEG-* / L-SRC-01 / L-ATEMPO-01 | **skip / watch** — need ffmpeg + fixture, not an open suggestion |
| Host SSH identity for push | **blocked** (environment; default face DENIED; no matching vault) |
