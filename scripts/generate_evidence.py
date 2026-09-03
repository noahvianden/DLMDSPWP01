"""Create the versioned Phase-7 evidence package from the supplied archive.

The generated CSV, Markdown, JSON, and SVG files are intended for the written
assignment.  Calculations remain in the application modules; this script only
records their outputs and renders presentation-ready, dependency-free SVGs.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import sqlite3
import subprocess
from collections import Counter
from collections.abc import Iterable, Sequence
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path
from xml.sax.saxutils import escape

import pandas as pd

from ideal_function_assignment.archive import DatasetArchive
from ideal_function_assignment.config import AppConfig
from ideal_function_assignment.loaders import (
    IdealFunctionLoader,
    TestDataLoader,
    TrainingDataLoader,
)
from ideal_function_assignment.mapping import PointMapper
from ideal_function_assignment.models import MappedPoint, SelectionResult, TestPoint
from ideal_function_assignment.runner import ApplicationRunner
from ideal_function_assignment.selection import FunctionSelector

PALETTE = ("#0072B2", "#D55E00", "#009E73", "#CC79A7")
SVG_WIDTH = 1260
SVG_HEIGHT = 880


def _parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Return command-line settings for one explicit evidence-generation run."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Evidence destination (default: <root>/docs/evidence).",
    )
    parser.add_argument(
        "--commit",
        default=None,
        help="Commit identifier to record; defaults to git HEAD when available.",
    )
    return parser.parse_args(argv)


def _git_commit(root: Path) -> str:
    """Return the checked-out commit without failing when Git is unavailable."""
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def _sha256(path: Path) -> str:
    """Return the SHA-256 digest of a file without loading it all at once."""
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _write_csv(path: Path, rows: Iterable[dict[str, object]], fieldnames: Sequence[str]) -> None:
    """Write a deterministic UTF-8 CSV with a documented field order."""
    with path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _float(value: float) -> str:
    """Format numeric evidence with enough precision for reported results."""
    return f"{value:.10f}"


def _mapping_decisions(
    points: Sequence[TestPoint], ideal_functions: pd.DataFrame, selections: Sequence[SelectionResult]
) -> list[dict[str, object]]:
    """Evaluate every source row once to make assignment status auditable."""
    ideal_by_x = ideal_functions.set_index("x")
    decisions: list[dict[str, object]] = []
    for point in points:
        ideal_row = ideal_by_x.loc[point.x]
        candidates = [
            (
                abs(point.y - float(ideal_row[f"y{selection.ideal_function}"])),
                selection,
            )
            for selection in selections
            if abs(point.y - float(ideal_row[f"y{selection.ideal_function}"])) <= selection.threshold
        ]
        if not candidates:
            decisions.append(
                {
                    "source_row": point.source_row,
                    "x": _float(point.x),
                    "y": _float(point.y),
                    "status": "unassigned",
                    "candidate_count": 0,
                    "ideal_function": "",
                    "delta_y": "",
                    "threshold": "",
                    "margin_to_threshold": "",
                }
            )
            continue
        delta_y, selection = min(
            candidates, key=lambda candidate: (candidate[0], candidate[1].ideal_function)
        )
        decisions.append(
            {
                "source_row": point.source_row,
                "x": _float(point.x),
                "y": _float(point.y),
                "status": "assigned",
                "candidate_count": len(candidates),
                "ideal_function": selection.ideal_function,
                "delta_y": _float(delta_y),
                "threshold": _float(selection.threshold),
                "margin_to_threshold": _float(selection.threshold - delta_y),
            }
        )
    return decisions


def _svg_document(body: str, title: str, description: str) -> str:
    """Wrap SVG drawing content with an accessible title and fixed presentation style."""
    return "\n".join(
        (
            '<?xml version="1.0" encoding="UTF-8"?>',
            (
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" '
                f'height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" role="img">'
            ),
            f"<title>{escape(title)}</title>",
            f"<desc>{escape(description)}</desc>",
            '<rect width="100%" height="100%" fill="white"/>',
            '<style>text{font-family:Arial,sans-serif;fill:#1f2937}.axis{stroke:#374151;stroke-width:1}.grid{stroke:#d1d5db;stroke-width:1}.training{stroke:#111827;stroke-width:1.6;fill:none}.ideal{fill:none;stroke-width:1.6;stroke-dasharray:6 4}.threshold{fill:none;stroke-width:1.3;stroke-dasharray:3 3}.mapped{stroke:white;stroke-width:.5}.unassigned{stroke:#6b7280;stroke-width:1.2}</style>',
            body,
            "</svg>",
        )
    )


def _line_path(points: Iterable[tuple[float, float]]) -> str:
    """Return an SVG path from already scaled x/y coordinates."""
    return " ".join(
        f"{'M' if index == 0 else 'L'} {x:.2f} {y:.2f}" for index, (x, y) in enumerate(points)
    )


def _scaler(values: Sequence[float], start: float, length: float, reverse: bool = False):
    """Return a stable linear scaler with a small guard margin."""
    low, high = min(values), max(values)
    pad = (high - low) * 0.06 or 1.0
    low -= pad
    high += pad

    def scale(value: float) -> float:
        fraction = (value - low) / (high - low)
        return start + (1 - fraction if reverse else fraction) * length

    return scale, low, high


def _panel_svg(
    left: float,
    top: float,
    width: float,
    height: float,
    training: pd.DataFrame,
    ideal_functions: pd.DataFrame,
    selection: SelectionResult,
    assignments: Sequence[MappedPoint],
    unassigned: Sequence[TestPoint],
    colour: str,
) -> str:
    """Render one comparison panel with training, candidate, and point statuses."""
    ideal_column = f"y{selection.ideal_function}"
    panel_assignments = [point for point in assignments if point.ideal_function == selection.ideal_function]
    x_scale, x_low, x_high = _scaler(training["x"].tolist(), left + 48, width - 60)
    y_values = (
        training[selection.training_series].tolist()
        + ideal_functions[ideal_column].tolist()
        + [point.y for point in panel_assignments]
        + [point.y for point in unassigned]
    )
    y_scale, y_low, y_high = _scaler(y_values, top + height - 38, height - 68, reverse=True)
    items = [
        f'<text x="{left + 8:.1f}" y="{top + 18:.1f}" font-size="13" font-weight="bold">{escape(selection.training_series)} vs y{selection.ideal_function}</text>',
        f'<text x="{left + 8:.1f}" y="{top + 34:.1f}" font-size="10">threshold = {selection.threshold:.6f}</text>',
        f'<line class="axis" x1="{left + 48:.1f}" y1="{top + height - 38:.1f}" x2="{left + width - 12:.1f}" y2="{top + height - 38:.1f}"/>',
        f'<line class="axis" x1="{left + 48:.1f}" y1="{top + 30:.1f}" x2="{left + 48:.1f}" y2="{top + height - 38:.1f}"/>',
    ]
    for fraction in (0.25, 0.5, 0.75):
        y = top + 30 + (height - 68) * fraction
        items.append(f'<line class="grid" x1="{left + 48:.1f}" y1="{y:.1f}" x2="{left + width - 12:.1f}" y2="{y:.1f}"/>')
    items.extend(
        (
            f'<path class="training" d="{_line_path(zip(training["x"].map(x_scale), training[selection.training_series].map(y_scale), strict=True))}"/>',
            f'<path class="ideal" stroke="{colour}" d="{_line_path(zip(ideal_functions["x"].map(x_scale), ideal_functions[ideal_column].map(y_scale), strict=True))}"/>',
        )
    )
    items.extend(
        f'<circle class="mapped" cx="{x_scale(point.x):.2f}" cy="{y_scale(point.y):.2f}" r="2.7" fill="{colour}"/>'
        for point in panel_assignments
    )
    items.extend(
        f'<path class="unassigned" d="M {x_scale(point.x)-2.7:.2f} {y_scale(point.y)-2.7:.2f} L {x_scale(point.x)+2.7:.2f} {y_scale(point.y)+2.7:.2f} M {x_scale(point.x)-2.7:.2f} {y_scale(point.y)+2.7:.2f} L {x_scale(point.x)+2.7:.2f} {y_scale(point.y)-2.7:.2f}"/>'
        for point in unassigned
    )
    items.extend(
        (
            f'<text x="{left + 48:.1f}" y="{top + height - 20:.1f}" font-size="9">x: {x_low:.1f} to {x_high:.1f}</text>',
            f'<text x="{left + width - 82:.1f}" y="{top + height - 20:.1f}" font-size="9">y: {y_low:.1f} to {y_high:.1f}</text>',
        )
    )
    return "\n".join(items)


def _comparison_svg(
    path: Path,
    training: pd.DataFrame,
    ideal_functions: pd.DataFrame,
    selections: Sequence[SelectionResult],
    assignments: Sequence[MappedPoint],
    unassigned: Sequence[TestPoint],
) -> None:
    """Write a four-panel SVG showing all point statuses across selections."""
    panels = []
    for index, (selection, colour) in enumerate(zip(selections, PALETTE, strict=True)):
        panels.append(
            _panel_svg(
                34 + (index % 2) * 610,
                54 + (index // 2) * 366,
                576,
                326,
                training,
                ideal_functions,
                selection,
                assignments,
                unassigned,
                colour,
            )
        )
    legend = (
        '<text x="34" y="28" font-size="18" font-weight="bold">Training series, selected ideal functions, and test-point status</text>'
        '<line class="training" x1="850" y1="22" x2="875" y2="22"/><text x="880" y="26" font-size="10">training</text>'
        '<line class="ideal" stroke="#0072B2" x1="950" y1="22" x2="975" y2="22"/><text x="980" y="26" font-size="10">selected ideal</text>'
        '<circle class="mapped" cx="1080" cy="22" r="3" fill="#0072B2"/><text x="1087" y="26" font-size="10">assigned</text>'
        '<path class="unassigned" d="M 1170 19 L 1176 25 M 1170 25 L 1176 19"/><text x="1180" y="26" font-size="10">unassigned</text>'
        '<text x="34" y="846" font-size="10">Source: Own representation based on the provided dataset. Unassigned points are shown in each panel to make their status explicit; assigned points appear only with their selected function.</text>'
    )
    path.write_text(
        _svg_document(
            legend + "\n" + "\n".join(panels),
            "Training, selected ideal functions, and test-point status",
            "Four comparison panels with training lines, selected ideal-function lines, assigned test points, and unassigned test points.",
        ),
        encoding="utf-8",
    )


def _deviation_svg(path: Path, selections: Sequence[SelectionResult], assignments: Sequence[MappedPoint]) -> None:
    """Write an SVG of mapped deviations with each applicable threshold."""
    x_scale, x_low, x_high = _scaler([point.x for point in assignments], 78, 1120)
    upper = max(max(point.delta_y for point in assignments), max(item.threshold for item in selections))
    y_scale, _, y_high = _scaler([0.0, upper], 790, 680, reverse=True)
    items = [
        '<text x="34" y="30" font-size="18" font-weight="bold">Assigned test-point deviations and selection thresholds</text>',
        '<line class="axis" x1="78" y1="790" x2="1198" y2="790"/>',
        '<line class="axis" x1="78" y1="110" x2="78" y2="790"/>',
    ]
    for fraction in (0.25, 0.5, 0.75):
        y = 110 + 680 * fraction
        items.append(f'<line class="grid" x1="78" y1="{y:.1f}" x2="1198" y2="{y:.1f}"/>')
    for selection, colour in zip(selections, PALETTE, strict=True):
        items.append(
            f'<line class="threshold" stroke="{colour}" x1="78" y1="{y_scale(selection.threshold):.2f}" x2="1198" y2="{y_scale(selection.threshold):.2f}"/>'
        )
        items.extend(
            f'<circle class="mapped" cx="{x_scale(point.x):.2f}" cy="{y_scale(point.delta_y):.2f}" r="4" fill="{colour}"/>'
            for point in assignments
            if point.ideal_function == selection.ideal_function
        )
    legend = "".join(
        f'<circle class="mapped" cx="{155 + index * 180}" cy="68" r="4" fill="{colour}"/><text x="{164 + index * 180}" y="72" font-size="11">y{selection.ideal_function}: points / threshold</text>'
        for index, (selection, colour) in enumerate(zip(selections, PALETTE, strict=True))
    )
    items.extend(
        (
            legend,
            f'<text x="78" y="814" font-size="10">x: {x_low:.1f} to {x_high:.1f}</text>',
            f'<text x="1080" y="814" font-size="10">maximum scale: {y_high:.3f}</text>',
            '<text x="34" y="850" font-size="10">Source: Own representation based on the provided dataset. Solid circles are assigned test points; dotted lines are the corresponding prescribed sqrt(2) thresholds.</text>',
        )
    )
    path.write_text(
        _svg_document(
            "\n".join(items),
            "Assigned deviations and thresholds",
            "Mapped test-point deviations plotted against their selected ideal-function thresholds.",
        ),
        encoding="utf-8",
    )


def _database_report(database_path: Path, selections: Sequence[SelectionResult], assignments: Sequence[MappedPoint]) -> str:
    """Return SQL-backed evidence that persisted results agree with memory results."""
    expected_rows = {
        "training_data": 400,
        "ideal_functions": 400,
        "selection_summary": len(selections),
        "test_results": len(assignments),
    }
    with sqlite3.connect(database_path) as connection:
        counts = {
            table: connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            for table in expected_rows
        }
        persisted = list(
            connection.execute(
                "SELECT training_series, ideal_function, sse, max_deviation, threshold "
                "FROM selection_summary ORDER BY training_series"
            )
        )
        sample = list(
            connection.execute(
                "SELECT x, y, delta_y, ideal_function FROM test_results ORDER BY rowid LIMIT 5"
            )
        )
    expected = [
        (
            selection.training_series,
            selection.ideal_function,
            selection.sse,
            selection.max_deviation,
            selection.threshold,
        )
        for selection in selections
    ]
    if counts != expected_rows or persisted != expected:
        raise RuntimeError("SQLite evidence does not match the in-memory analysis results.")
    lines = [
        "# SQLite verification",
        "",
        "The generated SQLite database was queried after the deterministic application run.",
        "",
        "| Table | Expected rows | SQL count | Result |",
        "|---|---:|---:|---|",
    ]
    lines.extend(
        f"| `{table}` | {expected_rows[table]} | {counts[table]} | match |" for table in expected_rows
    )
    lines.extend(
        (
            "",
            "The four `selection_summary` rows exactly match the in-memory selected functions and their unrounded SSE, maximum deviation, and threshold values.",
            "",
            "## Sample persisted mappings",
            "",
            "| x | y | delta_y | ideal_function |",
            "|---:|---:|---:|---:|",
        )
    )
    lines.extend(f"| {_float(x)} | {_float(y)} | {_float(delta)} | y{function} |" for x, y, delta, function in sample)
    return "\n".join(lines) + "\n"


def generate(root: Path, evidence_dir: Path, commit: str) -> dict[str, Path]:
    """Run the application and create its immutable Phase-7 presentation evidence."""
    root = root.resolve()
    evidence_dir = evidence_dir.resolve()
    figures_dir = evidence_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    config = AppConfig.from_root(root, log_level="ERROR")
    artifacts = ApplicationRunner(config).run()
    paths = DatasetArchive(config.archive_path, config.data_dir).extract()
    training = TrainingDataLoader(paths.train).load()
    ideal_functions = IdealFunctionLoader(paths.ideal).load()
    selections = FunctionSelector().select(training, ideal_functions)
    points = tuple(TestDataLoader(paths.test).load())
    report = PointMapper(ideal_functions, selections).map_points(points)
    decisions = _mapping_decisions(points, ideal_functions, selections)

    selected_path = evidence_dir / "selected_functions.csv"
    _write_csv(
        selected_path,
        [
            {
                "training_series": selection.training_series,
                "ideal_function": f"y{selection.ideal_function}",
                "sse": _float(selection.sse),
                "max_deviation": _float(selection.max_deviation),
                "threshold": _float(selection.threshold),
            }
            for selection in selections
        ],
        ("training_series", "ideal_function", "sse", "max_deviation", "threshold"),
    )

    counts = Counter(point.ideal_function for point in report.assignments)
    mapping_path = evidence_dir / "mapping_summary.csv"
    _write_csv(
        mapping_path,
        [
            {
                "status": f"assigned_to_y{selection.ideal_function}",
                "count": counts[selection.ideal_function],
                "share_of_all_test_points": _float(counts[selection.ideal_function] / len(points)),
            }
            for selection in selections
        ]
        + [
            {"status": "assigned_total", "count": report.assigned_count, "share_of_all_test_points": _float(report.assigned_count / len(points))},
            {"status": "unassigned", "count": report.unassigned_count, "share_of_all_test_points": _float(report.unassigned_count / len(points))},
        ],
        ("status", "count", "share_of_all_test_points"),
    )

    decisions_path = evidence_dir / "mapping_decisions.csv"
    _write_csv(
        decisions_path,
        decisions,
        (
            "source_row",
            "x",
            "y",
            "status",
            "candidate_count",
            "ideal_function",
            "delta_y",
            "threshold",
            "margin_to_threshold",
        ),
    )
    assigned_decisions = [row for row in decisions if row["status"] == "assigned"]
    boundary_path = evidence_dir / "boundary_cases.csv"
    _write_csv(
        boundary_path,
        sorted(assigned_decisions, key=lambda row: float(str(row["margin_to_threshold"])))[:5]
        + [row for row in assigned_decisions if row["candidate_count"] == 2],
        (
            "source_row",
            "x",
            "y",
            "status",
            "candidate_count",
            "ideal_function",
            "delta_y",
            "threshold",
            "margin_to_threshold",
        ),
    )

    database_path = evidence_dir / "sqlite_verification.md"
    database_path.write_text(_database_report(artifacts.database_path, selections, report.assignments), encoding="utf-8")
    comparison_path = figures_dir / "selected_functions_and_mapping.svg"
    _comparison_svg(comparison_path, training, ideal_functions, selections, report.assignments, report.unassigned_points)
    deviation_path = figures_dir / "assigned_deviations.svg"
    _deviation_svg(deviation_path, selections, report.assignments)

    artifacts_to_hash = {
        "selected_functions.csv": selected_path,
        "mapping_summary.csv": mapping_path,
        "mapping_decisions.csv": decisions_path,
        "boundary_cases.csv": boundary_path,
        "sqlite_verification.md": database_path,
        "figures/selected_functions_and_mapping.svg": comparison_path,
        "figures/assigned_deviations.svg": deviation_path,
    }
    manifest_path = evidence_dir / "analysis_manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "analysis_commit": commit,
                "analysis_timestamp_utc": datetime.now(UTC).isoformat(),
                "dataset_archive": "data/dataset.zip",
                "dataset_sha256": _sha256(config.archive_path),
                "python_version": platform.python_version(),
                "package_version": version("dlmdspwp01"),
                "result_summary": {
                    "assigned_count": report.assigned_count,
                    "unassigned_count": report.unassigned_count,
                    "test_row_count": len(points),
                    "selected_ideal_functions": [selection.ideal_function for selection in selections],
                },
                "artefact_sha256": {name: _sha256(path) for name, path in artifacts_to_hash.items()},
                "interpretation_guardrail": "The prescribed sqrt(2) factor is a mapping rule, not a statistical confidence measure.",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return {**artifacts_to_hash, "analysis_manifest.json": manifest_path}


def main(argv: Sequence[str] | None = None) -> int:
    """Execute evidence generation and print the stable list of created files."""
    args = _parse_arguments(argv)
    root = args.root.resolve()
    evidence_dir = (args.output_dir or root / "docs" / "evidence").resolve()
    created = generate(root, evidence_dir, args.commit or _git_commit(root))
    print("Generated Phase-7 evidence:")
    for name, path in created.items():
        print(f"  {name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
