"""End-to-end and reproducibility tests for the documented CLI workflow."""

import json
import shutil
import sqlite3
from pathlib import Path

from ideal_function_assignment.runner import main


def _prepare_clean_root(tmp_path: Path, official_archive_path: Path) -> Path:
    """Create a clean temporary project root containing only the official archive."""
    root = tmp_path / "clean_project"
    data_dir = root / "data"
    data_dir.mkdir(parents=True)
    shutil.copy2(official_archive_path, data_dir / "dataset.zip")
    return root


def _database_results(database_path: Path) -> tuple[list[tuple[object, ...]], list[tuple[object, ...]]]:
    """Read deterministic business results while excluding SQLite's implicit rowid."""
    with sqlite3.connect(database_path) as connection:
        selections = list(
            connection.execute(
                "SELECT training_series, ideal_function, sse, max_deviation, threshold "
                "FROM selection_summary ORDER BY training_series"
            )
        )
        mappings = list(
            connection.execute(
                "SELECT x, y, delta_y, ideal_function FROM test_results ORDER BY rowid"
            )
        )
    return selections, mappings


def test_cli_run_from_clean_output_creates_all_required_artefacts(
    tmp_path: Path, official_archive_path: Path, capsys: object
) -> None:
    """The documented command creates database, HTML, summary, and a successful exit code."""
    root = _prepare_clean_root(tmp_path, official_archive_path)
    assert main(["--root", str(root), "--log-level", "ERROR"]) == 0
    captured = capsys.readouterr()
    output_dir = root / "output"
    assert "Assigned test points: 34" in captured.out
    assert (output_dir / "ideal_function_assignment.sqlite").is_file()
    assert (output_dir / "ideal_function_assignment.html").is_file()
    summary = json.loads((output_dir / "run_summary.json").read_text(encoding="utf-8"))
    assert summary["assigned_count"] == 34
    assert summary["unassigned_count"] == 66


def test_two_runs_with_the_same_archive_have_identical_business_results(
    tmp_path: Path, official_archive_path: Path
) -> None:
    """Repeated clean-output runs reproduce JSON selections and SQLite business rows."""
    root = _prepare_clean_root(tmp_path, official_archive_path)
    arguments = ["--root", str(root), "--log-level", "ERROR"]
    assert main(arguments) == 0
    output_dir = root / "output"
    first_summary = (output_dir / "run_summary.json").read_text(encoding="utf-8")
    first_results = _database_results(output_dir / "ideal_function_assignment.sqlite")

    assert main(arguments) == 0
    second_summary = (output_dir / "run_summary.json").read_text(encoding="utf-8")
    second_results = _database_results(output_dir / "ideal_function_assignment.sqlite")
    assert second_summary == first_summary
    assert second_results == first_results
