# Methodology and System Design

Status: Phase 4 design baseline, 3 September 2026. This document fixes the
methodological and architectural decisions that must be implemented and tested in later phases.
It does not claim that the application has already been implemented.

## 1. Scope and terminology

The application **selects** four functions from the fifty supplied ideal functions. It does not
estimate new function parameters and is not presented as training a new regression model.

- A training series is written as t_j(x_i), where j is one of y1 to y4.
- A supplied ideal function is written as f_k(x_i), where k is in 1 to 50.
- A test point is p = (x, y).
- An ideal-function number is the integer k, matching the yk column in the supplied ideal table.
- The stored delta_y value is always the non-negative absolute deviation.

The supplied archive is treated as a correct immutable input under
[DATA_CONTRACT.md](DATA_CONTRACT.md). The design therefore defines operational behaviour and
runtime error handling rather than a separate manual data-audit process.

## 2. Deterministic selection and mapping method

### 2.1 Selection of ideal functions

For each training series j and each supplied ideal function k, calculate:

~~~text
SSE(j, k) = sum from i=1 to n of (t_j(x_i) - f_k(x_i))^2
~~~

For every training series independently, select the ideal-function number with the smallest SSE.

**Tie rule:** if two or more SSE values are exactly equal in the calculation representation, choose
the smallest ideal-function number. The selected four function numbers need not be distinct,
because the assignment requires independent selection for the four training series.

For every selected pair, calculate:

~~~text
max_deviation(j) = max over i of abs(t_j(x_i) - f_k*(x_i))
threshold(j) = sqrt(2) * max_deviation(j)
~~~

SSE is retained without calculation-time rounding. Rounding is a presentation concern only.

### 2.2 Test-point mapping

For each test point p = (x, y), look up each selected f_k*(x) at the same supplied x value. No
interpolation, extrapolation, nearest-neighbour replacement, or comparison against another x is
allowed.

For every selected ideal function j, calculate:

~~~text
delta(j, p) = abs(y - f_k*(x))
~~~

A candidate is eligible when:

~~~text
delta(j, p) <= threshold(j)
~~~

Equality at the threshold is eligible.

**Multiple eligible candidates:** choose the eligible candidate with the smallest delta. If that
again ties exactly, choose the smallest ideal-function number. This makes mapping deterministic
and preserves the requirement that a test point is assigned to at most one selected function.

**No eligible candidate:** keep the point in the run summary as unassigned and increment its
counter. It is not inserted into the four-business-column test-results table, because that table
is reserved for successful mappings.

**Completeness invariant:** every input test row produces exactly one terminal runtime state:
assigned or unassigned. Therefore:

~~~text
assigned_count + unassigned_count = input_test_row_count
~~~

### 2.3 Processing order

1. Resolve the versioned archive path and extract the three CSV files to the ignored runtime data
   directory if they are not already available for the run.
2. Load training and ideal tables into pandas DataFrames.
3. Recreate the SQLite schema and persist the training and ideal tables.
4. Select the four ideal functions and persist the selection summary.
5. Read test.csv line by line; map each point immediately and batch-persist successful mappings.
6. Produce a deterministic textual run summary and Bokeh HTML output.

The line-by-line test-data step is deliberately separate from the DataFrame loaders so the
assignment requirement is directly visible in the code and tests.

## 3. Persistence design

The database is created under the configured output directory on each clean run. Schema creation,
table replacement, and the import of the two reference tables occur in a transaction. A failed
write rolls back the active transaction; no half-refreshed run is presented as successful.

| Table | Declared columns | Constraint / purpose |
|---|---|---|
| training_data | x, y1, y2, y3, y4 | x is unique; exactly the required five business columns |
| ideal_functions | x, y1 through y50 | x is unique; exactly the required 51 business columns |
| test_results | x, y, delta_y, ideal_function | exactly the four required business columns; SQLite implicit rowid preserves repeated x values |
| selection_summary | training_series, ideal_function, sse, max_deviation, threshold | auxiliary evidence table; one row per training series |

The auxiliary selection_summary table does not substitute for any required table. It makes the
selection and threshold values reproducible without re-running the whole calculation.

SQLAlchemy Core will define the schema because the required relational tables map directly to
explicit table and column definitions. SQLite's implicit rowid is intentionally used for
test_results instead of adding a visible fifth primary-key column: the assignment specifies a
four-column result table and test x values are not assumed to be unique.

## 4. Component design

~~~mermaid
flowchart TD
    A["CLI / ApplicationRunner"] --> B["AppConfig"]
    A --> C["DatasetArchive"]
    C --> D["TrainingDataLoader"]
    C --> E["IdealFunctionLoader"]
    C --> F["TestDataLoader"]
    D --> G["FunctionSelector"]
    E --> G
    D --> H["DatabaseRepository"]
    E --> H
    G --> H
    F --> I["PointMapper"]
    G --> I
    I --> H
    G --> J["BokehVisualizer"]
    I --> J
    J --> K["HTML output"]
    H --> L["SQLite output"]
~~~

| Component | Responsibility | Key output |
|---|---|---|
| AppConfig | Resolve project-relative paths, output locations, and run options without user-specific hard-coded paths. | Immutable configuration object |
| DatasetArchive | Locate the versioned archive and extract its three files to the ignored runtime location. | CSV paths |
| BaseCSVLoader | Shared path and header handling for CSV specialisations. This is the meaningful inheritance base. | Common loading contract |
| TrainingDataLoader | Load the four training series into a DataFrame. | Training DataFrame |
| IdealFunctionLoader | Load the fifty ideal functions into a DataFrame. | Ideal DataFrame |
| TestDataLoader | Yield test points one row at a time in source order. | Iterator of test points |
| FunctionSelector | Calculate SSE, max deviation, thresholds, and deterministic selections. | Four selection records |
| PointMapper | Apply the test-point eligibility and tie rules. | Assigned mappings and unassigned count |
| DatabaseRepository | Recreate schema, write source tables, selection summary, and successful results transactionally. | SQLite database |
| BokehVisualizer | Create HTML visualisation from selected functions, mappings, and run summary. | HTML file |
| ApplicationRunner | Enforce the documented end-to-end order and publish the run summary. | Exit status and artefact paths |

### 4.1 Inheritance

BaseCSVLoader is an abstract base class for the three specialised loaders. It owns the common
input-path and header contract; TrainingDataLoader and IdealFunctionLoader return whole
DataFrames, while TestDataLoader exposes the required row iterator. The specialisations retain
the same public loading contract but have distinct, relevant output behaviour. This is
inheritance for shared input responsibility, not an artificial requirement-only hierarchy.

### 4.2 Error model

~~~text
IdealFunctionAssignmentError
|- InputDataError
|- FunctionSelectionError
|- MappingError
|- PersistenceError
+- VisualizationError
~~~

Expected underlying exceptions are handled at component boundaries:

| Boundary | Standard exception | Project response |
|---|---|---|
| archive and CSV paths | FileNotFoundError, OSError, UnicodeDecodeError | raise InputDataError with path and cause |
| parsing or shape conversion | ValueError, TypeError, pandas parser errors | raise InputDataError with contextual message |
| selection or missing exact x lookup | KeyError, ValueError | raise FunctionSelectionError or MappingError |
| SQLite and SQLAlchemy writes | SQLAlchemyError, OSError | rollback and raise PersistenceError |
| visualisation output | ValueError, OSError | raise VisualizationError |

Wrapped exceptions use explicit Python exception chaining. The runner logs one useful failure
message and returns a non-zero exit status; it must not swallow broad exceptions.

## 5. Visualisation design

The HTML output contains:

1. Four comparable panels, each showing one training series, its selected ideal function, and the
   successfully mapped test points.
2. Per-panel y-axis ranges rather than one global scale, so a high-magnitude function cannot hide
   smaller series.
3. Consistent colour and marker meanings across all panels, a legend, labelled axes, and hover
   data containing x, y, delta_y, selected function number, and threshold.
4. A separate deviation-oriented panel or summary view showing assigned deviations relative to
   their threshold and the number of unassigned points.

Unassigned test points remain visible in an aggregated overview or summary, but are visually
distinct from successful mappings. Every graphic later used in the written assignment is derived
from the final program output and labelled as an own representation based on the supplied data.

## 6. Test strategy before implementation

No synthetic CSV fixture files are used. Small unit tests create in-memory DataFrames and
test-point objects; temporary SQLite databases are used for persistence tests. The supplied
archive is reserved for integration and end-to-end acceptance tests.

| Level | Scope | Core cases |
|---|---|---|
| Unit | Selector and mapper rules | hand-calculated SSE; exact SSE tie; max absolute deviation; inside, boundary, outside threshold; multiple candidates; no candidate; same-x lookup |
| Unit | Exception translation | unavailable paths, invalid runtime conversion, chained domain errors |
| Integration | SQLAlchemy / SQLite | required tables and columns; transaction rollback; repeated x result rows; non-negative delta_y |
| Integration | Official archive | loading, four selections, summary invariants, output schema |
| End-to-end | CLI run from clean output directory | database, HTML, summary, and successful exit status |
| Reproducibility | two clean runs from identical input | identical selections, mappings, and summary values |

## 7. Design decisions and consequences

| Decision | Alternative rejected | Reason and consequence |
|---|---|---|
| Compare only at equal supplied x | positional comparison or interpolation | respects the task's supplied pair structure and avoids unsupported assumptions |
| Use SSE rather than MSE for selection | MSE | both rank equal-length series identically, but SSE is the stated task criterion |
| Smallest function number breaks exact ties | first encountered candidate | deterministic behaviour independent of iteration order |
| Smallest eligible delta breaks mapping conflicts | allow duplicate mappings | one test point receives one clear, explainable assignment |
| Store absolute delta_y | signed residual only | the task asks for deviation; non-negative values simplify database and plot interpretation |
| Preserve only successful mappings in test_results | store synthetic status rows for non-matches | maintains the stipulated four-business-column table while reporting non-matches separately |
| SQLAlchemy Core and SQLite rowid | ORM plus visible fifth primary key | direct schema representation and preservation of the required four visible result columns |
| Loader inheritance | unrelated classes only | satisfies a real shared responsibility without coupling selection, persistence, and visualisation |
| In-memory unit data, no CSV fixtures | synthetic CSV files | meets the explicit project decision while retaining small deterministic rule tests |

## 8. Implementation acceptance checklist

Phase 5 implementation may begin only by preserving these decisions. A future change to a rule
requires a documented reason, matching test update, source-matrix review where a theoretical
claim changes, and a change-log entry.

| Requirements covered | Evidence in this document |
|---|---|
| A-059 to A-070 | Sections 1 and 2 |
| A-071 to A-073 | Section 3 |
| A-074 to A-078 | Section 4 |
| A-079 | Section 5 |
| A-080 | Section 6 |
| A-081 and A-082 | Sections 4 and 7 |
