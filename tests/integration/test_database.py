"""SQLite integration tests for schema, repeated x values, and atomic rollback."""

import sqlite3
from pathlib import Path

import pytest

from ideal_function_assignment.database import DatabaseRepository
from ideal_function_assignment.models import MappedPoint, SelectionResult


def _selections() -> tuple[SelectionResult, ...]:
    """Return four compact, unique summary rows for database integration tests."""
    return tuple(
        SelectionResult(f"y{number}", number, float(number), 0.5, 0.5 * 2**0.5)
        for number in range(1, 5)
    )


def _write_complete_database(
    database_path: Path,
    official_frames: object,
    mappings: tuple[MappedPoint, ...],
) -> None:
    """Write a small valid database using rows from the official reference frames."""
    repository = DatabaseRepository(database_path)
    with repository.open_run() as database_run:
        database_run.write_reference_tables(
            official_frames.training.head(2), official_frames.ideal.head(2)
        )
        database_run.write_selection_summary(_selections())
        database_run.write_mappings(mappings)


def test_database_has_required_schema_and_only_four_result_columns(
    tmp_path: Path, official_frames: object
) -> None:
    """SQLAlchemy creates the documented required and auxiliary table structure."""
    database_path = tmp_path / "assignment.sqlite"
    _write_complete_database(database_path, official_frames, ())

    with sqlite3.connect(database_path) as connection:
        tables = {
            row[0]
            for row in connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        }
        columns = list(connection.execute("PRAGMA table_info(test_results)"))
    assert tables == {"training_data", "ideal_functions", "test_results", "selection_summary"}
    assert [column[1] for column in columns] == ["x", "y", "delta_y", "ideal_function"]
    assert [column[2] for column in columns] == ["FLOAT", "FLOAT", "FLOAT", "INTEGER"]
    assert all(column[3] == 1 for column in columns)
    assert all(column[5] == 0 for column in columns)


def test_database_retains_repeated_test_x_and_non_negative_delta_y(
    tmp_path: Path, official_frames: object
) -> None:
    """Repeated result x values are stored as separate implicit-rowid records."""
    database_path = tmp_path / "assignment.sqlite"
    _write_complete_database(
        database_path,
        official_frames,
        (
            MappedPoint(1.0, 2.0, 0.25, 1),
            MappedPoint(1.0, 3.0, 0.5, 2),
        ),
    )

    with sqlite3.connect(database_path) as connection:
        rows = list(
            connection.execute(
                "SELECT x, y, delta_y, ideal_function FROM test_results ORDER BY rowid"
            )
        )
    assert rows == [(1.0, 2.0, 0.25, 1), (1.0, 3.0, 0.5, 2)]
    assert all(row[2] >= 0 for row in rows)


def test_failed_database_run_preserves_previous_complete_database(
    tmp_path: Path, official_frames: object
) -> None:
    """An exception rolls back the temporary run and leaves the prior final database intact."""
    database_path = tmp_path / "assignment.sqlite"
    _write_complete_database(
        database_path, official_frames, (MappedPoint(1.0, 2.0, 0.25, 1),)
    )
    repository = DatabaseRepository(database_path)

    with (
        pytest.raises(RuntimeError, match="forced failure"),
        repository.open_run() as database_run,
    ):
        database_run.write_reference_tables(
            official_frames.training.head(2), official_frames.ideal.head(2)
        )
        raise RuntimeError("forced failure")

    with sqlite3.connect(database_path) as connection:
        count = connection.execute("SELECT COUNT(*) FROM test_results").fetchone()[0]
    assert count == 1
    assert not (tmp_path / ".assignment.sqlite.tmp").exists()
