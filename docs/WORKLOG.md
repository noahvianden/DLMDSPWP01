# Project Worklog

| Date | Phase | Decision / evidence |
|---|---|---|
| 2026-09-01 | Phase 0 | Scope, title, research question, 15-page limit and repository-based code delivery fixed. |
| 2026-09-01 | Phase 1 | Repository cloned; baseline package, dependency specification, ignored runtime/output paths and test layout committed. |
| 2026-09-03 | Phase 1 | Fresh `.venv` created; `pip install -e '.[dev]'`, pytest (1 passed), Ruff (all checks passed) and package import (`0.1.0`) successful. A-033 completed. |
| 2026-09-03 | Phase 2 | Data contract added. The supplied archive is versioned as `data/dataset.zip`; extracted CSV files and generated artefacts remain ignored. No synthetic fixtures or separate manual dataset audit are used. |
| 2026-09-03 | Phase 3 | `docs/SOURCE_MATRIX.md` added with a verified least-squares source, a standard textbook reserve source, conditional official technical sources, APA/IU pinpoint-citation controls, and a no-secondary-citation rule. |
| 2026-09-03 | Documentation | The current, evidence-backed requirements status is versioned as `docs/07-Anforderungsliste.md`. |\n| 2026-09-03 | Phase 4 | `docs/METHODOLOGY_AND_DESIGN.md` fixes the deterministic selection/mapping rules, SQLite model, component responsibilities, inheritance, exception boundaries, visualisation, and test strategy before product code. |

## Commit rules

Commits should represent one coherent project change, use an imperative message, and be validated locally before creation. Generated data, databases, environments and caches must not be committed. The supplied `data/dataset.zip` archive is the documented exception and remains versioned unchanged.
