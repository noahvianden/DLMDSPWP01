# DLMDSPWP01 – Ideal Function Assignment

This repository contains the reproducible Python implementation and tests for the official DLMDSPWP01 written assignment.

## Status

Phase 1 establishes the project structure. The official source archive is versioned as `data/dataset.zip`.

## Planned layout

- `src/ideal_function_assignment/` – application package
- `tests/unit/`, `tests/integration/`, `tests/e2e/` – test suites
- `data/` – versioned source archive; extracted CSV files are ignored
- `output/` – ignored generated results

## Development

```bash
python -m venv .venv
python -m pip install -e '.[dev]'
python -m pytest
```

Extract `data/dataset.zip` locally into `data/` when running the application. The extracted CSV files remain ignored by Git.
