"""CSV loaders that share input handling while preserving specialised outputs."""

import csv
import math
from abc import ABC, abstractmethod
from collections.abc import Iterator, Sequence
from pathlib import Path

import numpy as np
import pandas as pd

from .exceptions import DataValidationError, InputDataError
from .models import TestPoint


class BaseCSVLoader(ABC):
    """Shared path, header, number, missing-value, and duplicate-x checks.

    Subclasses expose ``load`` with their specialised output type: complete
    DataFrames for reference data and a line-by-line iterator for test data.
    """

    expected_columns: tuple[str, ...]
    reject_duplicate_x = False

    def __init__(self, path: Path) -> None:
        """Create a loader for one extracted runtime CSV path.

        Parameters
        ----------
        path:
            CSV file to read.
        """
        self.path = path

    @abstractmethod
    def load(self) -> pd.DataFrame | Iterator[TestPoint]:
        """Load this specialised CSV representation.

        Raises
        ------
        InputDataError
            If the file cannot be read.
        DataValidationError
            If the header or numeric input contract is not met.
        """

    def _read_frame(self) -> pd.DataFrame:
        """Read and validate a full reference-data CSV frame."""
        self._require_file()
        try:
            frame = pd.read_csv(self.path)
        except (OSError, UnicodeDecodeError, pd.errors.ParserError, ValueError) as error:
            raise InputDataError(f"Could not read CSV file: {self.path}") from error

        self._validate_header(tuple(frame.columns))
        if frame.empty:
            raise DataValidationError(f"CSV file contains no data rows: {self.path}")

        converted = frame.loc[:, self.expected_columns].copy()
        try:
            for column in self.expected_columns:
                converted[column] = pd.to_numeric(converted[column], errors="raise")
        except (TypeError, ValueError) as error:
            raise DataValidationError(f"CSV contains non-numeric values: {self.path}") from error

        if converted.isna().any().any():
            raise DataValidationError(f"CSV contains missing values: {self.path}")

        try:
            values = converted.to_numpy(dtype=float)
        except (TypeError, ValueError) as error:
            raise DataValidationError(f"CSV cannot be converted to finite numbers: {self.path}") from error
        if not np.isfinite(values).all():
            raise DataValidationError(f"CSV contains non-finite values: {self.path}")

        if self.reject_duplicate_x and converted["x"].duplicated().any():
            raise DataValidationError(f"CSV contains duplicate x values: {self.path}")
        return converted

    def _require_file(self) -> None:
        """Ensure that the configured CSV path is an accessible file."""
        if not self.path.is_file():
            raise InputDataError(f"CSV input file is unavailable: {self.path}")

    def _validate_header(self, actual_columns: Sequence[str] | None) -> None:
        """Require the exact documented header and column order.

        Parameters
        ----------
        actual_columns:
            Header names received from pandas or ``csv.DictReader``.

        Raises
        ------
        DataValidationError
            If the header differs from the documented input contract.
        """
        if tuple(actual_columns or ()) != self.expected_columns:
            expected = ", ".join(self.expected_columns)
            actual = ", ".join(actual_columns or ())
            raise DataValidationError(
                f"Unexpected CSV header in {self.path}; expected [{expected}], received [{actual}]"
            )


class TrainingDataLoader(BaseCSVLoader):
    """Load the four complete training series into a validated DataFrame."""

    expected_columns = ("x", "y1", "y2", "y3", "y4")
    reject_duplicate_x = True

    def load(self) -> pd.DataFrame:
        """Return a finite, duplicate-free training DataFrame.

        Raises
        ------
        InputDataError
            If ``train.csv`` cannot be opened.
        DataValidationError
            If its documented data contract is violated.
        """
        return self._read_frame()


class IdealFunctionLoader(BaseCSVLoader):
    """Load the fifty complete candidate ideal functions into a DataFrame."""

    expected_columns = ("x",) + tuple(f"y{number}" for number in range(1, 51))
    reject_duplicate_x = True

    def load(self) -> pd.DataFrame:
        """Return a finite, duplicate-free ideal-function DataFrame.

        Raises
        ------
        InputDataError
            If ``ideal.csv`` cannot be opened.
        DataValidationError
            If its documented data contract is violated.
        """
        return self._read_frame()


class TestDataLoader(BaseCSVLoader):
    """Expose supplied test points as a source-ordered, line-by-line iterator."""

    expected_columns = ("x", "y")

    def load(self) -> Iterator[TestPoint]:
        """Return a test-point iterator after checking file and header availability.

        Returns
        -------
        Iterator[TestPoint]
            Points produced one CSV row at a time in source order.

        Raises
        ------
        InputDataError
            If ``test.csv`` cannot be opened.
        DataValidationError
            If its header differs from the documented input contract.
        """
        self._require_file()
        try:
            with self.path.open("r", encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                self._validate_header(reader.fieldnames)
        except (OSError, UnicodeDecodeError) as error:
            raise InputDataError(f"Could not read CSV file: {self.path}") from error
        return self._iter_points()

    def _iter_points(self) -> Iterator[TestPoint]:
        """Yield validated points without constructing a test-data DataFrame."""
        try:
            with self.path.open("r", encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                self._validate_header(reader.fieldnames)
                for source_row, row in enumerate(reader, start=1):
                    yield self._parse_point(row, source_row)
        except (OSError, UnicodeDecodeError) as error:
            raise InputDataError(f"Could not read CSV file: {self.path}") from error

    def _parse_point(self, row: dict[str, str | None], source_row: int) -> TestPoint:
        """Convert one source row to finite numeric coordinates.

        Raises
        ------
        DataValidationError
            If the row has missing, non-numeric, or non-finite coordinates.
        """
        try:
            x = float(row["x"])
            y = float(row["y"])
        except (KeyError, TypeError, ValueError) as error:
            raise DataValidationError(
                f"Test CSV row {source_row} contains missing or non-numeric values: {self.path}"
            ) from error
        if not math.isfinite(x) or not math.isfinite(y):
            raise DataValidationError(
                f"Test CSV row {source_row} contains non-finite values: {self.path}"
            )
        return TestPoint(x=x, y=y, source_row=source_row)
