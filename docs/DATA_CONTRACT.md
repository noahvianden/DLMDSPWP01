# Data Contract

The supplied `data/dataset.zip` archive is treated as a correct, immutable input source. Its contents are not manually revalidated during project work.

## Input files

| File | Required columns | Use |
|---|---|---|
| `train.csv` | `x, y1, y2, y3, y4` | Four training series |
| `ideal.csv` | `x, y1` through `y50` | Fifty candidate ideal functions |
| `test.csv` | `x, y` | Test points to map |

## Operational rules

- The archive remains versioned as `data/dataset.zip`.
- Extracted CSV files are local runtime files and remain ignored by Git.
- The application assumes the supplied dataset is correct; no separate dataset-audit step is performed.
- Calculations and mappings use the supplied `x` values directly. No interpolation or extrapolation is introduced.
- Test-result rows require their own technical identity; `x` is not a unique result key.
- Outputs use a stable, documented order. Floating-point values are not rounded during calculation; rounding is limited to display.
- The implementation still rejects unavailable input files and propagates meaningful errors when a program run cannot proceed.
