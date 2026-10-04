# Reviews — VideoSpeed

Public product review surface (peer of `tests/` when present).

| File | Role |
|------|------|
| `what-to-review.md` | Living review plan / checklist |
| `test-plan.md` | TP-* status map |
| `requirement-test-matrix.md` | Requirement → TP families |
| `lessons.md` | Durable failure modes to re-check |
| `index.md` | Report index |
| `cli-routed-verb-table.md` | Live `video-speed` verbs from the dispatcher |
| `reports/` | Dated review run reports |

**Product:** VideoSpeed (Python interactive CLI)  
**Package / version SSOT:** `1.0.11` (`pyproject.toml` + `src/VideoSpeed/__init__.py`)  
**Ship surface:** `src/VideoSpeed/` (one class per module; `def main` in `cli.py`) · console script `video-speed` · `python -m VideoSpeed`  
**Install mode:** pip / local package (not shell Type 0 online install)  
**Type 1 elevation:** intentionally absent  

**Always load first:** `reviews/lessons.md`  
**Last plan update:** 2026-09-30
