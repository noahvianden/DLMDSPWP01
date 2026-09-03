# Object-Oriented Selection and Mapping of Ideal Functions in Python: A Least-Squares and SQLite-Based Approach

> **Transfer note (not part of the submission):** This is an English manuscript draft for transfer into the existing Word template. The prose is intentionally limited to approximately 4,000 words before the reference list. With the planned three figures and three compact tables, it is designed to fit the required 12–15 pages of text in the IU template. Final pagination must be checked after the text and figures have been inserted into Word.

## 1. Introduction

Selecting a suitable function from a fixed candidate set is a deceptively constrained data-analysis problem. The task is not to invent a model or estimate a new set of parameters. Instead, it requires the systematic comparison of supplied functions against observed training series, followed by a traceable decision about which candidate best represents each series. The subsequent treatment of test points creates a second decision problem: a point must be accepted only when its deviation from a selected function satisfies a prescribed rule, while ambiguous cases must be resolved deterministically. A result is therefore credible only if mathematical selection, data handling, persistence, visualisation, and testing support the same conclusion.

Least squares provides a well-established vocabulary for comparing observed values with a model through squared deviations. In its conventional regression setting, the method estimates unknown parameters by minimising the sum of squared deviations between data and a model (National Institute of Standards and Technology [NIST] & SEMATECH, n.d., Section 4.1.4.1). The present assignment uses the criterion more narrowly: it ranks already supplied ideal functions. This distinction is important because the implementation does not fit a regression model, make forecasts, or infer population parameters. It selects the smallest error among finite, predefined alternatives.

The practical relevance of this problem lies in reproducibility. A numerical result alone does not show whether rows were aligned correctly, whether a threshold was applied consistently, or whether a repeated run would produce the same database entries. The application therefore treats deterministic computation and verifiable software behaviour as parts of the analytical result. Each stage exposes an observable outcome: validated input tables, four selected ideal functions, a persisted mapping result, a browser-based visualisation, and automated tests. The result is consequently inspectable by a reader rather than dependent on a narrative assertion that the program worked.

The research question is as follows: **How can an object-oriented Python application reproducibly select the four best-fitting ideal functions using a least-squares criterion, assign eligible test points under the prescribed deviation threshold, and persist and visualise the resulting mappings?** The aim is to answer this question through a concrete implementation using the supplied data archive. The expected outputs are a SQLite database, a stable run summary, interactive and static visual evidence, and a test suite that checks the core mathematical and technical rules.

The scope is deliberately limited. The analysis compares four training series with fifty supplied ideal functions at the supplied x values. It neither estimates new function parameters nor interpolates missing values, extrapolates beyond the available x range, or claims predictive performance outside this data set. The required \(\sqrt{2}\) factor is treated as a task-specific acceptance rule, not as a confidence interval or significance test. These boundaries prevent the language of the paper from implying more statistical evidence than the assignment produces.

The remainder of the paper first defines the functional and quality requirements and introduces the two error measures. It then explains the method, the component architecture, and the implementation decisions. The results section reports the selected functions, the mappings, and the test evidence. Finally, the discussion evaluates the strengths and limitations of the design before the conclusion answers the research question.

## 2. Requirements and Theoretical Background

### 2.1 Functional and quality requirements

The application has six functional responsibilities. First, it reads the supplied training, ideal-function, and test data without altering the source archive. Second, it selects one ideal function independently for each of the four training series. Third, it evaluates every test point at the identical supplied x value and records either an assignment or an unassigned status. Fourth, it creates the required SQLite tables. Fifth, it presents the outcome visually. Sixth, it documents a Git-based team workflow as required by the assignment.

The quality requirements are equally material to the solution. The implementation must use object-oriented design, include meaningful inheritance, provide contextual exception handling, use Pandas, SQLAlchemy, and Bokeh appropriately, and be testable. Reproducibility also requires project-relative paths, a versioned archive, declared dependencies, automated checks, and a repository from which the application can be run. These requirements are interdependent: a correct calculation that cannot be repeated or inspected does not fully answer the research question.

The supplied archive contains `train.csv`, `ideal.csv`, and `test.csv`. The training table has 400 rows with one x column and four y series; the ideal-function table has the same number of x values and fifty candidate y columns; the test table contains 100 x–y pairs. The implementation validates headers, numerical values, finite values, and duplicate x values for the two reference tables. Exact x alignment matters because an error at one x value must be compared with the ideal-function value at that same x value. In contrast, repeated x values in the test data are legitimate because distinct test observations can share one coordinate.

### 2.2 Selection criterion and mapping rule

For a training series \(t_j\) and an ideal function \(f_k\), the selection score is the sum of squared errors (SSE):

\[
\operatorname{SSE}(j,k) = \sum_{i=1}^{n}\left[t_j(x_i)-f_k(x_i)\right]^2.
\]

Here, \(i\) indexes the aligned x values, \(j\) identifies one of the four training series, \(k\) identifies one of the fifty supplied ideal functions, and \(n=400\). Squaring makes positive and negative deviations contribute positively and gives larger deviations greater influence on the ranking. This use of the SSE criterion is consistent with the least-squares principle of comparing data and model through squared deviations (NIST & SEMATECH, n.d., Section 4.1.4.1). However, the result is an argmin over supplied functions, not an estimated regression equation.

The selected function for each training series is the candidate with the smallest SSE. If two candidates have exactly the same score, the smaller ideal-function number is selected. This explicit tie rule removes dependence on incidental table order. For the selected pair, the application also computes the largest absolute training deviation,

\[
d_j^{\max}=\max_i\left|t_j(x_i)-f_{k^*}(x_i)\right|,
\]

and derives the task-specific threshold \(\tau_j=\sqrt{2}\,d_j^{\max}\). Unlike SSE, which is a global ranking criterion across the 400 training observations, the threshold is used locally when evaluating an individual test point. Keeping the two measures separate avoids the erroneous assumption that a small SSE alone authorises every test-point assignment.

For a test point \(p=(x,y)\), the absolute deviation from a selected function is

\[
\delta(j,p)=\left|y-f_{k^*}(x)\right|.
\]

The point is an eligible candidate for that selected function when \(\delta(j,p)\leq\tau_j\). Equality is included. If several selected functions are eligible, the smallest \(\delta\) is chosen; an exact remaining tie is resolved by the smaller function number. If no candidate is eligible, the point is retained as unassigned. The \(\sqrt{2}\) factor is therefore a prescribed decision rule in this assignment. It is not interpreted as a statistical confidence measure, because no sampling distribution, confidence level, or inferential model is estimated.

These definitions lead directly to the methodological design. The selection stage requires exact alignment and deterministic ranking, while the mapping stage requires source-ordered point processing, an inclusive boundary comparison, and an explicit terminal state for every row.

## 3. Methodology

### 3.1 Processing sequence and input controls

The application follows a fixed sequence. It resolves the versioned archive, extracts the three CSV files to an ignored runtime location when necessary, and loads the two reference tables into Pandas DataFrames. The application validates their expected headers and rejects missing, non-numeric, non-finite, or duplicate reference values. It then recreates the SQLite database, persists the reference tables, selects the functions, calculates thresholds, evaluates the test points, stores successful mappings, writes a run summary, and produces the visual output.

The test file is handled differently from the reference tables. Its rows are yielded one at a time in source order. This design implements the assignment requirement directly and preserves a clear relationship between an input row and its terminal state. A test point with an unknown x value raises a mapping error rather than being matched to a neighbouring value. Consequently, the analysis neither silently interpolates nor turns an input inconsistency into a plausible-looking assignment.

### 3.2 Selection and mapping procedure

For each of the four training series, the selector evaluates all fifty SSE values and takes the independent minimum. It then computes the maximum absolute deviation and the derived threshold for the chosen pair. All calculations use full floating-point precision; rounding occurs only in published tables and figures. The independent selection is deliberate. The task does not require the four chosen ideal functions to be distinct, and imposing uniqueness would change the stated optimisation problem.

The mapper creates an exact-x index of the ideal-function table. For each test point, it reads the value of each selected ideal function at that x value, calculates absolute deviations, and forms the eligible-candidate set. The point is assigned only after the minimum deviation and tie-break rules have been evaluated. A successful mapping contains exactly four business values: x, y, `delta_y`, and the ideal-function number. Unassigned points remain in the run report rather than being inserted into the required result table. The completeness invariant is checked as

\[
\text{assigned count}+\text{unassigned count}=\text{input test-row count}.
\]

This invariant is important because it detects a class of silent processing errors that a table of successful mappings alone would hide.

### 3.3 Persistence, evaluation, and visualisation

SQLite is used as a local, inspectable persistence layer. The database contains `training_data`, `ideal_functions`, `test_results`, and the auxiliary `selection_summary` table. SQLAlchemy Core represents tables through explicit metadata, table, and column objects, which suits a schema whose required columns are known in advance (SQLAlchemy authors, n.d., “Working with Database Metadata”). The database is written first to a temporary sibling file. Only a complete transaction is promoted to the visible output file, so a failed write cannot masquerade as a complete analysis.

The evaluation strategy combines rule-level and outcome-level evidence. Unit tests verify SSE calculations, tie rules, threshold inclusion, unknown x handling, and invalid inputs. Integration tests check the SQLite schema and transaction behaviour, while end-to-end tests run the command-line workflow from a clean output location and compare two runs. The final acceptance test uses the supplied archive and independently checks the four selected functions, 34 assigned points, 66 unassigned points, and the known multiple-candidate case. pytest is used because it supports concise assertions and test organisation from small examples to functional checks (pytest-dev, n.d., “Features”); the project-specific expected values remain its own evidence rather than claims made by the framework.

The visualisation uses four comparison panels and a deviation-oriented panel. Each comparison panel contains a training series, its selected ideal function, successfully mapped test points, and visually distinct unassigned points. The deviation view places `delta_y` values against their corresponding thresholds. Bokeh is suitable for the interactive output because it creates browser-oriented visualisations (Bokeh Contributors, n.d., “Bokeh documentation”). Static SVG exports accompany the HTML output so that the same results can be inserted into the written assignment without losing vector sharpness.

The method has deliberate limits. It is valid only for the supplied functions, supplied x values, and specified threshold. The maximum-deviation threshold can be sensitive to an extreme training deviation, and it does not provide a probabilistic measure of uncertainty. These constraints are stated before the implementation and guide the later interpretation.

## 4. System Design and Architecture

Figure 1 summarises the application architecture. The central design principle is separation of responsibilities: each component owns one reason to change and exposes an explicit output to the next component.

**[Insert Figure 1 here: Processing and component architecture.]**

*Figure 1. Processing and component architecture.*  
*Source: Own representation.*

`AppConfig` resolves all project-relative paths and output targets. `DatasetArchive` locates and extracts the supplied archive. The specialised loaders then produce validated training and ideal DataFrames or a source-ordered test-point iterator. `FunctionSelector` returns four immutable selection records, while `PointMapper` returns successful mappings and retained unassigned points. `DatabaseRepository` persists the complete run transactionally, and `BokehVisualizer` creates the interactive visualisation. `ApplicationRunner` orchestrates this order and exposes the final summary through the command-line interface.

The loader hierarchy is the principal use of inheritance. `BaseCSVLoader` owns the common path and header contract. `TrainingDataLoader`, `IdealFunctionLoader`, and `TestDataLoader` share that input responsibility while implementing different schemas and output forms. The design avoids a larger artificial hierarchy: selection, mapping, persistence, and visualisation are composed by the runner because they have distinct concerns rather than a common substitutable interface. This balance makes the inheritance meaningful without allowing object orientation to obscure the data flow.

Figure 1 should be read from archive to outputs. The reference tables feed both selection and persistence; the selected functions and test iterator feed mapping; the selection and mapping results feed persistence and visualisation. The sequence prevents an output component from redefining a mathematical decision. It also makes the test boundaries clear: the selector and mapper can be tested with small in-memory data, whereas the database and command-line flow require integration-level checks.

The database schema reflects the assignment without discarding auditability. `training_data` has x and four training columns; `ideal_functions` has x and fifty ideal columns. `test_results` contains exactly x, y, `delta_y`, and `ideal_function`. It deliberately has no visible primary key because repeated test x values must be preserved; SQLite’s implicit row identifier differentiates rows internally. The auxiliary `selection_summary` table stores training-series names, selected function numbers, SSE values, maximum deviations, and thresholds. This makes the selection result independently inspectable without modifying the required four-column result table.

Exception handling is also a design boundary. File and parsing errors are translated into input-domain exceptions, selection and lookup failures into selection or mapping exceptions, and persistence failures into a persistence exception after rollback. The command-line boundary logs one contextual message and returns a non-zero status instead of exposing an uncontrolled traceback. Python explicitly supports attaching an original cause to a raised exception (Python Software Foundation, n.d., Section 7.8), which preserves diagnostic information while presenting a meaningful domain message.

Several alternatives were considered. Fully vectorised processing could calculate many deviations at once, but row-wise test mapping better expresses the assignment requirement and preserves source-row accountability. An in-memory result would be simpler, but it would not satisfy the persistence requirement or provide a durable inspection target. SQLite is selected instead of a network database because the task is local and reproducible. Finally, transactionally replacing a temporary database is preferable to overwriting the previous file because it protects the visible result from partial runs.

## 5. Implementation

The application targets Python 3.11–3.13 and was executed for the final analysis with Python 3.12.13 and package version 0.1.0. Dependencies are declared in `pyproject.toml`; Pandas handles tabular reference data, SQLAlchemy defines and writes the SQLite schema, and Bokeh produces the interactive HTML output. The versioned `data/dataset.zip` archive is the only source input. Generated databases, extracted CSV files, and runtime HTML output remain outside version control, while the reproducible evidence tables and SVG figures are retained under `docs/evidence`.

The import layer first validates the expected column sequence and then converts values to numeric form. Validation is intentionally performed before SSE calculations, because malformed values or duplicate reference x coordinates would make an apparently precise comparison invalid. The input layer distinguishes reference-table duplicates from repeated test x values. This distinction prevents the incorrect use of a uniqueness restriction that would discard legitimate test observations.

The persistence implementation uses explicit table declarations for the required schema. The runner opens a temporary database transaction, writes the source tables, selection summary, and successful mapping rows, and promotes the temporary file only after commit. The final database contains 400 training rows, 400 ideal-function rows, four selection-summary rows, and 34 successful mappings. The SQL verification report checks these counts and compares the persisted selection rows with the in-memory selection records.

The selection implementation aligns training and ideal functions by x key before computing each SSE. It returns an immutable record containing the training-series name, function number, unrounded SSE, maximum deviation, and threshold. This return object prevents the mapping stage from recalculating a threshold differently. The mapper subsequently processes each test row, applies the inclusive comparison, and resolves candidate conflicts using `(delta_y, ideal_function number)` as the deterministic ordering key. The database receives only the successful record, while the run summary retains both counts.

Error handling is exercised rather than merely declared. For example, a missing CSV path is translated to a contextual input error; an unknown test x value causes a mapping error; and an exception during a database run leaves the previous complete database intact. Logging reports the stage at which a failure occurred, while the command-line interface supplies an appropriate exit code. This arrangement makes expected faults understandable without conflating them with mathematical non-matches.

The visual layer uses consistent colour meanings across the panels, labelled axes, legends, and hover information for x, y, absolute deviation, selected function, and threshold. Unassigned points are shown as grey cross markers, which makes their status visible rather than reducing them to an unexplained remainder. Figure 2 presents the four training–ideal comparisons and the test-point status. Figure 3 focuses on the relationship between assigned deviations and the four thresholds.

**[Insert Figure 2 here: `docs/evidence/figures/selected_functions_and_mapping.svg`.]**

*Figure 2. Training series, selected ideal functions, and test-point status.*  
*Source: Own representation based on the provided dataset.*

**[Insert Figure 3 here: `docs/evidence/figures/assigned_deviations.svg`.]**

*Figure 3. Assigned test-point deviations and selection thresholds.*  
*Source: Own representation based on the provided dataset.*

The test suite contains 28 tests across unit, integration, and end-to-end levels. The most informative cases are not generic happy paths: they include invalid headers and values, exact threshold equality, a just-outside point, SSE ties, mapping ties, repeated result x values, rollback, deterministic repeated runs, and the official-data oracle. The suite passed with warnings promoted to errors and achieved 88% total line coverage. Coverage is treated as a diagnostic rather than a substitute for assertions; the documented functional rules have direct tests.

The repository is available at `https://github.com/noahvianden/DLMDSPWP01`. The tested implementation is recorded in commit `2102504779f95d4ca479d8ec9e1f3e942bc1aa57`; the corresponding evidence package is frozen in commit `3c561dfd929f0b771464389227969a6d229088a0`. The required team workflow can be executed without embedding credentials:

```bash
git clone --branch develop --single-branch <repository-url>
cd <repository-directory>
git switch -c feature/<feature-name>
git add <changed-files>
git commit -m "Add <feature>"
git push --set-upstream origin feature/<feature-name>
```

After pushing, a pull request from `feature/<feature-name>` to `develop` permits review. Requested corrections are committed to the same feature branch; after approval, the branch is merged into `develop`. This workflow keeps changes reviewable and separates an individual contribution from the shared integration branch.

## 6. Results and Analysis

The validated reference data contained the expected 400 training rows, 400 ideal-function rows, and 100 test rows. The training and ideal tables were aligned through their exact x values. The accepted test input retained repeated x values, which confirms why the result table cannot use x as a visible unique key. These conditions enabled a direct comparison of every training value with every candidate function at the same coordinate.

Table 1 reports the selected functions. Each training series produced a different minimum in the supplied candidate set. The SSE values are reported to ten decimal places for transparency; the application retained full calculation precision.

**Table 1. Selected ideal functions and derived thresholds**

| Training series | Selected ideal function | SSE | Maximum deviation | Threshold |
|---|---:|---:|---:|---:|
| y1 | y13 | 34.0807075815 | 0.4992210000 | 0.7060051088 |
| y2 | y24 | 33.4517609531 | 0.4990000000 | 0.7056925676 |
| y3 | y36 | 35.5727003958 | 0.4989430000 | 0.7056119575 |
| y4 | y40 | 34.9988748132 | 0.4997790000 | 0.7067942400 |

*Source: Own calculation based on the provided dataset.*

Figure 2 visually supports, but does not replace, these numerical selections. The solid dark line in each panel is the training series, while the dashed coloured line is the corresponding selected ideal function. Assigned points appear only in the panel of their selected function; unassigned points are shown as grey crosses. Thus, the figure distinguishes a close training–ideal correspondence from the separate question of whether a particular test point satisfies the threshold.

The final run assigned 34 of 100 test points and retained 66 as unassigned. Table 2 disaggregates the result. The distribution is not a measure of model prevalence or external performance; it is the outcome of the supplied test points under four specific thresholds.

**Table 2. Test-point mapping summary**

| Status | Count | Share of all test points |
|---|---:|---:|
| Assigned to y13 | 8 | 8% |
| Assigned to y24 | 9 | 9% |
| Assigned to y36 | 10 | 10% |
| Assigned to y40 | 7 | 7% |
| **Assigned total** | **34** | **34%** |
| **Unassigned** | **66** | **66%** |

*Source: Own calculation based on the provided dataset.*

The completeness invariant holds because \(34+66=100\). The SQLite verification independently confirms 34 rows in `test_results`, while the run summary records the 66 unassigned points. This agreement between source-row processing, in-memory report, database, and Table 2 is more informative than a single printed count because it rules out a lost third state.

The boundary evidence provides two useful checks. The largest successful `delta_y` is 0.665244 for source row 11 at \(x=-0.7\), assigned to y24. Its remaining margin to the y24 threshold is 0.040449, making it the closest accepted point to a threshold as well as the largest accepted deviation. The case demonstrates that the acceptance test is applied to each selected function’s own threshold rather than to a shared rounded value.

One test point had two eligible candidates. Source row 51 has \(x=-1.6\) and \(y=-8.079187\); it qualifies for y13 and y24. The mapper assigned y24 because its absolute deviation is smaller, namely 0.112813. This result is analytically important because it demonstrates the difference between detecting eligibility and deciding the final assignment. Without the minimum-deviation rule, the result could depend on function order and would no longer be reproducible.

Figure 3 shows all assigned `delta_y` values against the corresponding threshold lines. The points remain below their relevant dotted line, as required by the inclusive mapping rule. The figure should not be interpreted as an uncertainty plot. It is a diagnostic view of task-specific acceptance margins and shows why a point can be assigned to one ideal function while another point with the same x coordinate may be unassigned.

The technical evidence corroborates the numerical results. All 28 tests passed with warnings treated as errors, and the fresh-clone check installed the project, ran the tests, and executed the command-line application successfully. The final evidence manifest records the archive SHA-256 value, Python and package versions, analysis commit, timestamp, summary counts, and hashes of the exported tables and figures. These controls make the reported values traceable to a defined program and data state rather than to a manually copied result.

**Table 3. Verification summary**

| Verification level | Evidence | Result |
|---|---|---|
| Mathematical selection | Official-data acceptance test | y13, y24, y36, y40 |
| Mapping completeness | Run summary and SQLite count | 34 assigned + 66 unassigned = 100 |
| Ambiguous assignment | Source row 51 | y24 selected by smaller `delta_y` |
| Technical quality | Unit, integration, and end-to-end tests | 28 passed; warnings treated as errors |
| Reproducibility | Fresh clone and evidence manifest | Installation, CLI run, and artefact hashes verified |

*Source: Own representation based on the project verification records.*

## 7. Discussion

The results answer the research question at the level of the supplied task. A reproducible selection-and-mapping application is achieved by combining a fixed error criterion with explicit software rules around it. The numerical core alone identifies y13, y24, y36, and y40. The surrounding architecture ensures that these selections are derived from aligned data, propagated unchanged to mapping, stored with their context, and independently checked. Reproducibility therefore emerges from the interaction of method and implementation rather than from the SSE calculation in isolation.

Several design choices strengthen this result. The deterministic tie rules prevent incidental candidate order from changing an output. Exact-x lookup prevents a visually plausible but undocumented approximation. Separation of loaders, selector, mapper, database repository, visualiser, and runner localises responsibilities and supports small tests. Transactional database replacement protects the visible output from incomplete runs. Finally, the combination of an interactive HTML visualisation, static SVGs, and a hash-recorded evidence package provides readers with more than one way to inspect the result.

The same choices introduce costs. The object-oriented structure creates more components than a short script would require, and the fixed CSV contract is intentionally less flexible than a general data-ingestion framework. SQLite is appropriate for a local reproducible assignment but not a multi-user production service. Static figures require a separate export step even though the Bokeh HTML is interactive. These costs are acceptable in this context because each component maps to a stated requirement or a testable responsibility, but they should not be represented as universally optimal engineering choices.

The methodological limitations are more fundamental. The candidate functions and the \(\sqrt{2}\) threshold are specified externally. A different candidate set could produce different selected functions, while a different threshold rule could change the 34/66 split. Because the threshold depends on the maximum training deviation, an extreme training discrepancy can affect the admissible range. The method also deliberately refuses interpolation, so it cannot assign a test point whose x value is absent from the ideal-function table. These are design boundaries, not implementation defects.

Accordingly, the results do not establish predictive accuracy, statistical significance, or general superiority of any ideal function. They show only that the supplied data, candidate functions, and prescribed rule yield a deterministic, internally consistent outcome. Alternative distance measures, normalised errors, or parameter-estimation approaches could be considered in a different study, but they would answer a different question and should not be retrofitted into this assignment.

Practical reproducibility is nevertheless a substantive result. The versioned archive, declared dependencies, repository commits, test suite, SQLite verification, and evidence manifest allow a reviewer to rerun and inspect the workflow. This does not eliminate the need for a final submission tag and Word/PDF checks, but it provides a transparent base for those final controls.

## 8. Conclusion

The research question can be answered affirmatively for the supplied task. An object-oriented Python application can reproducibly select and map ideal functions when the calculation, data contract, persistence, visualisation, and tests are designed as one controlled workflow. The implementation selected y13 for y1, y24 for y2, y36 for y3, and y40 for y4 by minimum SSE. It then assigned 34 of 100 test points and retained 66 as unassigned under the prescribed threshold rule.

The central contribution is not a claim of general predictive modelling. It is the traceable implementation of a fixed selection and mapping procedure. Exact-x alignment, deterministic tie handling, transactional SQLite persistence, and rule-focused tests make the output inspectable and repeatable. The known double-candidate case further demonstrates that reproducibility depends on an explicit mapping decision, not merely on finding candidates.

The interpretation remains bounded by the supplied archive, candidate set, and threshold. In particular, the \(\sqrt{2}\) factor is a task rule rather than a statistical confidence statement. Within these boundaries, the repository, evidence package, and final Word/PDF quality checks provide an appropriate basis for submitting a concise and reproducible written assignment.

The next submission controls should preserve this traceability rather than expand the analytical claim. The Word version should retain the stated figure and table sources, use the final repository tag or commit once it has been created, and keep the reference list synchronised with the in-text citations. A page-by-page PDF review is still necessary because pagination, figure scaling, and reference formatting depend on the final template. These editorial steps do not change the substantive conclusion; they ensure that the documented implementation, evidence, and submitted document remain the same auditable work.

## References

Bokeh Contributors. (n.d.). *Bokeh documentation*. https://docs.bokeh.org/en/latest/

National Institute of Standards and Technology, & SEMATECH. (n.d.). *4.1.4.1. Linear least squares regression*. In *NIST/SEMATECH e-Handbook of Statistical Methods*. https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd141.htm

pytest-dev. (n.d.). *pytest documentation*. https://docs.pytest.org/en/stable/

Python Software Foundation. (n.d.). *7. Simple statements: The raise statement*. *Python documentation*. https://docs.python.org/3/reference/simple_stmts.html

SQLAlchemy authors. (n.d.). *Working with database metadata*. *SQLAlchemy 2.0 Documentation*. https://docs.sqlalchemy.org/en/20/tutorial/metadata.html
