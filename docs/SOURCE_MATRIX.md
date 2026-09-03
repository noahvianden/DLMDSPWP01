# Phase 3 Source Matrix

Status: controlled citation register, created 3 September 2026.

## Purpose and use rule

This register controls the sources that may be used in the written assignment. It is not itself
the final reference list. A source enters the final reference list only if it is actually cited in
the paper.

- Every factual or theoretical statement in the paper needs a source card marked **Ready** and
  the listed exact page, page range, or named web section.
- The IU citation rules require a pinpoint reference for paraphrases as well as quotations. For
  web documentation without stable page numbers, cite the named section.
- Course book, lectures, webinars, the assignment PDF, and the project assessment guidance are
  governing project materials. They are not used as academic literature in the paper.
- The task-specific selection and mapping rules, including the prescribed \(\sqrt{2}\) threshold,
  are explained as the project's own methodology. They must not be attributed to an external
  source.
- Official documentation is used only to support a concrete product capability. Routine
  implementation steps, such as reading a CSV into a DataFrame, do not need a decorative
  citation.
- Secondary citations are not permitted unless the original source cannot be obtained. In that
  exceptional case, use the IU “as cited in” form and list only the accessible secondary source.

## Search record

| Area | Search terms recorded | Resulting source decision |
|---|---|---|
| Least squares / SSE | `least squares`, `sum of squared deviations`, `residual sum of squares`, `ideal-function selection` | Use the NIST/SEMATECH handbook for the definition and Hastie et al. as standard statistical background. |
| Residuals and deviation measures | `residual`, `absolute deviation`, `maximum deviation` | Explain the project's maximum-deviation and threshold rules as task-specific methodology; avoid claiming a general statistical estimator where none is implemented. |
| Object-oriented design | `object-oriented responsibilities`, `inheritance design`, `separation of concerns` | Treat component boundaries and justified inheritance as own design decisions; no general OOP claim is planned. |
| Data persistence | `SQLAlchemy metadata`, `SQLAlchemy transactions`, `SQLite schema` | Cite official SQLAlchemy documentation only if the paper makes a claim about its metadata or transaction facilities. |
| Software tests | `pytest assertions`, `unit testing Python`, `integration testing Python` | Cite pytest documentation only if a framework capability is discussed; the project's test cases are own evidence. |
| Visualisation | `Bokeh interactive visualizations`, `Bokeh browser output` | Cite Bokeh documentation only if the paper makes a technical claim about the interactive output. |

## Source hierarchy

1. **Scientific standard literature and primary/authoritative methods sources** support mathematics,
   statistical terminology, and general methodological claims.
2. **Official technical documentation** supports only concrete, version-sensitive capabilities of
   Python libraries and the language.
3. Search snippets, blogs, course materials, code examples, and secondary quotations are not
   evidence sources for the written assignment.

## Claim matrix

| ID | Planned claim (paraphrase, not quotation) | Source / exact location | Quality and intended paper section | Status |
|---|---|---|---|---|
| MATH-01 | Least squares obtains parameter estimates by minimising the sum of squared deviations between data and model. The paper uses this only to motivate comparing pre-defined functions by SSE; it does **not** claim to fit a new regression model. | NIST/SEMATECH, Section 4.1.4.1, “Why ‘Least Squares’?” | Authoritative government statistical handbook; **Methodology** | **Ready** |
| MATH-02 | A standard account of linear methods for regression and least squares is available for contextual background. Use only if a broad background sentence is necessary. | Hastie et al. (2009), Chapter 3, “Linear Methods for Regression,” pp. 43–99. | Scholarly standard textbook; **Introduction / Methodology** | **Ready, sparing use** |
| TECH-01 | SQLAlchemy represents database metadata through `MetaData`, `Table`, and `Column` objects. | SQLAlchemy documentation, “Working with Database Metadata,” especially “Setting up MetaData with Table objects” and “Components of `Table`.” | Official product documentation; **Implementation**, only if this capability is discussed | **Ready, conditional** |
| TECH-02 | Bokeh creates interactive visualisations for modern web browsers. | Bokeh documentation, “Bokeh documentation” overview. | Official product documentation; **Implementation / Visualisation**, only if this capability is discussed | **Ready, conditional** |
| TECH-03 | pytest supports small readable tests and can scale to functional testing. | pytest documentation, “pytest: helps you write better programs” and “Features.” | Official product documentation; **Testing**, only if the framework capability is discussed | **Ready, conditional** |
| TECH-04 | Python supports explicit exception chaining using the `raise ... from ...` form. | Python language reference, “7.8. The `raise` statement.” | Official language documentation; **Implementation**, only if exception chaining is discussed | **Ready, conditional** |

## Verified reference records

### MATH-01

National Institute of Standards and Technology, & SEMATECH. (n.d.). *4.1.4.1. Linear
least squares regression*. In *NIST/SEMATECH e-Handbook of Statistical Methods*.
https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd141.htm

- Verification: organisation, title, section number, URL, and content match checked.
- In-text form: `(National Institute of Standards and Technology [NIST] & SEMATECH, n.d.,
  Section 4.1.4.1)`.
- Do not use the handbook to claim that this project estimates new model parameters; the
  assignment selects among functions that are already supplied.

### MATH-02

Hastie, T., Tibshirani, R., & Friedman, J. (2009). Linear methods for regression. In
*The elements of statistical learning: Data mining, inference, and prediction* (2nd ed.,
pp. 43–99). Springer. https://doi.org/10.1007/978-0-387-84858-7_3

- Verification: authors, publication year, edition, page range, publisher, and chapter DOI match
  the publisher record.
- In-text form for a chapter-level paraphrase: `(Hastie et al., 2009, pp. 43–99)`.
- Before a narrower claim is written, replace the broad chapter range with the precise relevant
  page(s) from the cited edition.

### TECH-01

SQLAlchemy authors. (n.d.). *Working with database metadata*. *SQLAlchemy 2.0
Documentation*. https://docs.sqlalchemy.org/en/20/tutorial/metadata.html

- In-text form: `(SQLAlchemy authors, n.d., “Working with Database Metadata”)`.
- Use only for a factual statement about SQLAlchemy; the chosen database schema remains the
  project's own design.

### TECH-02

Bokeh Contributors. (n.d.). *Bokeh documentation*. https://docs.bokeh.org/en/latest/

- In-text form: `(Bokeh Contributors, n.d., “Bokeh documentation”)`.
- Use only for the product capability, not as authority for visual interpretation.

### TECH-03

pytest-dev. (n.d.). *pytest documentation*. https://docs.pytest.org/en/stable/

- In-text form: `(pytest-dev, n.d., “Features”)`.
- Test results, expected values, and coverage belong to the project's own evidence and are not
  attributed to pytest.

### TECH-04

Python Software Foundation. (n.d.). *7. Simple statements: The `raise` statement*.
*Python documentation*. https://docs.python.org/3/reference/simple_stmts.html

- In-text form: `(Python Software Foundation, n.d., Section 7.8)`.
- Use only when the paper explains exception chaining as a language feature.

## Final citation controls

Before drafting a paragraph:

1. Record the planned claim in this matrix.
2. Confirm that the source supports precisely that claim and that the exact location is present.
3. Paraphrase in the writer's own words; do not copy source language.
4. Add the matching APA 7 / IU in-text citation and, only then, the reference-list entry.
5. Check that every reference-list entry has an in-text citation and vice versa.

This initial source package is sufficient for the mathematical basis and the currently planned,
strictly limited technical claims. New theory claims require a new verified source card before they
enter the manuscript.
