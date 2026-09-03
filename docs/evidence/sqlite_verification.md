# SQLite verification

The generated SQLite database was queried after the deterministic application run.

| Table | Expected rows | SQL count | Result |
|---|---:|---:|---|
| `training_data` | 400 | 400 | match |
| `ideal_functions` | 400 | 400 | match |
| `selection_summary` | 4 | 4 | match |
| `test_results` | 34 | 34 | match |

The four `selection_summary` rows exactly match the in-memory selected functions and their unrounded SSE, maximum deviation, and threshold values.

## Sample persisted mappings

| x | y | delta_y | ideal_function |
|---:|---:|---:|---:|
| 3.4000000000 | 78.9570200000 | 0.3490200000 | y24 |
| 17.6000000000 | 57.9859200000 | 0.5416640000 | y40 |
| -0.7000000000 | -1.3512440000 | 0.6652440000 | y24 |
| -15.7000000000 | -7740.1426000000 | 0.3566000000 | y24 |
| -0.4000000000 | 106.6405100000 | 0.5984300000 | y40 |
