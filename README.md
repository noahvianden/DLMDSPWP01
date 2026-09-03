# DLMDSPWP01 – Ideal Function Assignment

This repository contains the reproducible Python implementation and tests for the official DLMDSPWP01 written assignment.

## Status

Phase 1 establishes the project structure. The individual source dataset is not included in this repository.

## Planned layout

- `src/ideal_function_assignment/` – application package
- `tests/unit/`, `tests/integration/`, `tests/e2e/` – test suites
- `tests/fixtures/` – small synthetic test data only
- `data/` – local ignored input data
- `output/` – ignored generated results

## Development

```bash
python -m venv .venv
python -m pip install -e '.[dev]'
python -m pytest
```

The official `data/dataset.zip` archive is versioned in this repository. Extract its CSV files locally into `data/` when running the application; extracted CSV files remain ignored.
