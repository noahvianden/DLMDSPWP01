"""Transactional SQLite persistence using SQLAlchemy Core."""

from collections.abc import Iterable
from pathlib import Path
from typing import Self

import pandas as pd
from sqlalchemy import Column, Float, Integer, MetaData, String, Table, create_engine
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.exc import SQLAlchemyError

from .exceptions import PersistenceError
from .models import MappedPoint, SelectionResult


class DatabaseRepository:
    """Create a complete SQLite result database without half-refreshing prior output."""

    def __init__(self, database_path: Path) -> None:
        """Create a repository for one final SQLite target path.

        Parameters
        ----------
        database_path:
            Generated SQLite database path. A temporary sibling is committed and
            atomically promoted only after a successful complete run.
        """
        self.database_path = database_path

    def open_run(self) -> "DatabaseRun":
        """Open a temporary transactional database run.

        Returns
        -------
        DatabaseRun
            Context manager that writes source, selection, and mapping tables.
        """
        return DatabaseRun(self.database_path)


class DatabaseRun:
    """A staged SQLite write that replaces the prior database only on success."""

    def __init__(self, database_path: Path) -> None:
        """Initialise an unopened transactional database run."""
        self.database_path = database_path
        self.temporary_path = database_path.with_name(f".{database_path.name}.tmp")
        self.metadata = MetaData()
        self.tables = _build_tables(self.metadata)
        self._engine: Engine | None = None
        self._connection: Connection | None = None
        self._transaction = None

    def __enter__(self) -> Self:
        """Create schema tables inside a new temporary SQLite database.

        Raises
        ------
        PersistenceError
            If the output database or its schema cannot be prepared.
        """
        try:
            self.database_path.parent.mkdir(parents=True, exist_ok=True)
            if self.temporary_path.exists():
                self.temporary_path.unlink()
            self._engine = create_engine(f"sqlite:///{self.temporary_path}")
            self._connection = self._engine.connect()
            self._transaction = self._connection.begin()
            self.metadata.create_all(self._connection)
            return self
        except (OSError, SQLAlchemyError, ValueError) as error:
            self._close()
            self._discard_temporary_file()
            raise PersistenceError(
                f"Could not prepare SQLite output: {self.database_path}"
            ) from error

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> bool:
        """Commit and promote a complete run or discard a failed temporary database."""
        if exc_type is not None:
            self._rollback()
            self._close()
            self._discard_temporary_file()
            return False

        try:
            if self._transaction is not None:
                self._transaction.commit()
            self._close()
            self.temporary_path.replace(self.database_path)
        except (OSError, SQLAlchemyError) as error:
            self._rollback()
            self._close()
            self._discard_temporary_file()
            raise PersistenceError(
                f"Could not finalise SQLite output: {self.database_path}"
            ) from error
        return False

    def write_reference_tables(
        self, training_data: pd.DataFrame, ideal_functions: pd.DataFrame
    ) -> None:
        """Write the required five- and fifty-one-column source tables.

        Parameters
        ----------
        training_data:
            Validated training DataFrame.
        ideal_functions:
            Validated ideal-function DataFrame.

        Raises
        ------
        PersistenceError
            If SQLAlchemy cannot write the reference rows.
        """
        self._insert_dataframe("training_data", training_data)
        self._insert_dataframe("ideal_functions", ideal_functions)

    def write_selection_summary(self, selections: Iterable[SelectionResult]) -> None:
        """Write one reproducibility record for each training-series selection."""
        self._insert_records("selection_summary", [selection.as_record() for selection in selections])

    def write_mappings(self, mappings: Iterable[MappedPoint]) -> None:
        """Write only successful mappings to the required four-column result table."""
        self._insert_records("test_results", [mapping.as_record() for mapping in mappings])

    def _insert_dataframe(self, table_name: str, frame: pd.DataFrame) -> None:
        """Convert a DataFrame to source records and write it into one table."""
        self._insert_records(table_name, frame.to_dict(orient="records"))

    def _insert_records(self, table_name: str, records: list[dict[str, object]]) -> None:
        """Execute a checked bulk insert inside the active transaction."""
        if not records:
            return
        if self._connection is None:
            raise PersistenceError("SQLite transaction is not open.")
        try:
            self._connection.execute(self.tables[table_name].insert(), records)
        except (SQLAlchemyError, TypeError, ValueError) as error:
            raise PersistenceError(f"Could not write SQLite table: {table_name}") from error

    def _rollback(self) -> None:
        """Roll back an active transaction without replacing a prior final database."""
        if self._transaction is not None and self._transaction.is_active:
            try:
                self._transaction.rollback()
            except SQLAlchemyError:
                pass

    def _close(self) -> None:
        """Release connection and engine resources when they were allocated."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None
        if self._engine is not None:
            self._engine.dispose()
            self._engine = None

    def _discard_temporary_file(self) -> None:
        """Best-effort removal of a failed temporary SQLite file."""
        try:
            if self.temporary_path.exists():
                self.temporary_path.unlink()
        except OSError:
            pass


def _build_tables(metadata: MetaData) -> dict[str, Table]:
    """Define the required SQLite tables and one documented auxiliary table."""
    training = Table(
        "training_data",
        metadata,
        Column("x", Float, nullable=False, unique=True),
        *(Column(f"y{number}", Float, nullable=False) for number in range(1, 5)),
    )
    ideal = Table(
        "ideal_functions",
        metadata,
        Column("x", Float, nullable=False, unique=True),
        *(Column(f"y{number}", Float, nullable=False) for number in range(1, 51)),
    )
    test_results = Table(
        "test_results",
        metadata,
        Column("x", Float, nullable=False),
        Column("y", Float, nullable=False),
        Column("delta_y", Float, nullable=False),
        Column("ideal_function", Integer, nullable=False),
    )
    selection_summary = Table(
        "selection_summary",
        metadata,
        Column("training_series", String, nullable=False, unique=True),
        Column("ideal_function", Integer, nullable=False),
        Column("sse", Float, nullable=False),
        Column("max_deviation", Float, nullable=False),
        Column("threshold", Float, nullable=False),
    )
    return {
        "training_data": training,
        "ideal_functions": ideal,
        "test_results": test_results,
        "selection_summary": selection_summary,
    }
