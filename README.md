# DLMDSPWP01 – Ideal Function Assignment

This repository contains the executable, reproducible Python implementation for the official
DLMDSPWP01 written assignment. It selects four supplied ideal functions using the sum of squared
errors (SSE), maps test points using the specified `sqrt(2)` threshold rule, and produces SQLite,
Bokeh HTML, and JSON-summary artefacts.

## Prerequisites

- Python 3.11, 3.12, or 3.13
- the versioned, unchanged source archive `data/dataset.zip`

No notebook is required. The supplied archive is the only source dataset; the program extracts
its three runtime CSV files automatically and leaves them ignored by Git.

## Installation

```bash
python -m venv .venv
```

Activate the environment using the command appropriate to the operating system, then install the
application and development tools:

```bash
python -m pip install -e '.[dev]'
```

## Run the application

From the repository root, run either command:

```bash
python -m ideal_function_assignment
ideal-function-assignment
```

Use `--root` when invoking the program from another directory:

```bash
ideal-function-assignment --root /path/to/DLMDSPWP01
```

The command performs this deterministic sequence:

1. resolves and, if necessary, extracts `data/dataset.zip`;
2. loads the training and ideal data, while reading `test.csv` line by line;
3. writes the required source tables to a temporary SQLite run;
4. selects the four lowest-SSE ideal functions and maps test points at identical x values only;
5. commits the complete database, then writes the Bokeh HTML and JSON run summary.

The console output is a concise summary rather than a raw-data dump. Failures use contextual
domain exceptions and result in a non-zero exit status.

## Generated outputs

All generated artefacts are written to the ignored `output/` directory:

| File | Purpose |
|---|---|
| `ideal_function_assignment.sqlite` | SQLite database with `training_data`, `ideal_functions`, `test_results`, and `selection_summary` tables |
| `ideal_function_assignment.html` | Interactive Bokeh output: four independently scaled comparison panels, an assigned-deviation panel, hover information, and an unassigned-point count |
| `run_summary.json` | Stable machine-readable selections, SSE values, deviations, thresholds, and assignment counts |

The Bokeh HTML is the reproducible graphics source. For static figures in the written assignment,
open it in a browser at the final window size and export or print the required panel without
altering the underlying program output.

## Architecture

`ApplicationRunner` coordinates `DatasetArchive`, the three CSV loaders, `FunctionSelector`,
`PointMapper`, `DatabaseRepository`, and `BokehVisualizer`. `BaseCSVLoader` supplies the common
input contract; its training, ideal-function, and test specialisations provide a DataFrame or the
required source-ordered test-point iterator. SQLAlchemy Core creates the explicit SQLite schema;
the result table has exactly the four required business columns and uses SQLite's implicit rowid
so repeated test x values are retained.

The full methodological choices, including deterministic tie rules, are documented in
[`docs/METHODOLOGY_AND_DESIGN.md`](docs/METHODOLOGY_AND_DESIGN.md).

## Repository layout

```text
data/                         versioned dataset archive; ignored extracted CSV files
docs/                         requirements, data contract, methodology, source matrix, worklog
src/ideal_function_assignment application package and CLI
tests/                        unit, integration, and end-to-end tests
output/                       ignored generated SQLite, HTML, and JSON artefacts
```

## Quality checks

```bash
python -m pytest
ruff check .
python -m ideal_function_assignment
```

## Troubleshooting

- **`Dataset archive is unavailable`**: ensure `data/dataset.zip` is present and run from the
  repository root or pass `--root`.
- **A CSV input error**: remove only the locally extracted `data/*.csv` files and run the command
  again so they are restored from the versioned archive. Do not alter the archive.
- **Output cannot be written**: ensure the repository location is writable and that no external
  application is locking the SQLite or HTML output file.
