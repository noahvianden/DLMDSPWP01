"""Immutable value objects exchanged between application components."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TestPoint:
    """One test-data row read directly from ``test.csv``.

    Parameters
    ----------
    x:
        Supplied x coordinate.
    y:
        Supplied y coordinate.
    source_row:
        One-based CSV data-row number, excluding the header.
    """

    x: float
    y: float
    source_row: int


@dataclass(frozen=True)
class SelectionResult:
    """Deterministic best ideal-function choice for one training series.

    Parameters
    ----------
    training_series:
        Training column name, for example ``y1``.
    ideal_function:
        Numeric suffix of the selected ideal-function column.
    sse:
        Sum of squared errors without calculation-time rounding.
    max_deviation:
        Greatest absolute training-to-ideal deviation.
    threshold:
        Mapping threshold, ``sqrt(2) * max_deviation``.
    """

    training_series: str
    ideal_function: int
    sse: float
    max_deviation: float
    threshold: float

    def as_record(self) -> dict[str, float | int | str]:
        """Return a SQLite-ready selection-summary record."""
        return {
            "training_series": self.training_series,
            "ideal_function": self.ideal_function,
            "sse": self.sse,
            "max_deviation": self.max_deviation,
            "threshold": self.threshold,
        }


@dataclass(frozen=True)
class MappedPoint:
    """A successful mapping of a test point to one ideal function.

    Parameters
    ----------
    x, y:
        Original test-point coordinates.
    delta_y:
        Non-negative absolute y deviation to the assigned function.
    ideal_function:
        Numeric suffix of the assigned ideal-function column.
    """

    x: float
    y: float
    delta_y: float
    ideal_function: int

    def as_record(self) -> dict[str, float | int]:
        """Return a SQLite-ready four-business-column result record."""
        return {
            "x": self.x,
            "y": self.y,
            "delta_y": self.delta_y,
            "ideal_function": self.ideal_function,
        }


@dataclass(frozen=True)
class MappingReport:
    """Successful and unsuccessful terminal mapping states for one run."""

    assignments: tuple[MappedPoint, ...]
    unassigned_points: tuple[TestPoint, ...]

    @property
    def assigned_count(self) -> int:
        """Return the number of successfully mapped test points."""
        return len(self.assignments)

    @property
    def unassigned_count(self) -> int:
        """Return the number of test points with no eligible function."""
        return len(self.unassigned_points)


@dataclass(frozen=True)
class RunSummary:
    """Reproducible numerical summary of an application run."""

    training_row_count: int
    ideal_row_count: int
    test_row_count: int
    selections: tuple[SelectionResult, ...]
    assigned_count: int
    unassigned_count: int

    def as_dict(self) -> dict[str, Any]:
        """Return a deterministic JSON-serialisable representation."""
        return {
            "assigned_count": self.assigned_count,
            "ideal_row_count": self.ideal_row_count,
            "selections": [selection.as_record() for selection in self.selections],
            "test_row_count": self.test_row_count,
            "training_row_count": self.training_row_count,
            "unassigned_count": self.unassigned_count,
        }

    def to_text(self) -> str:
        """Return a concise human-readable run summary without raw-data output."""
        lines = [
            "Ideal Function Assignment run summary",
            f"Training rows: {self.training_row_count}",
            f"Ideal-function rows: {self.ideal_row_count}",
            f"Test rows: {self.test_row_count}",
            f"Assigned test points: {self.assigned_count}",
            f"Unassigned test points: {self.unassigned_count}",
            "Selected ideal functions:",
        ]
        lines.extend(
            (
                f"  {selection.training_series} -> y{selection.ideal_function} "
                f"(SSE={selection.sse:.12g}, max deviation={selection.max_deviation:.12g}, "
                f"threshold={selection.threshold:.12g})"
            )
            for selection in self.selections
        )
        return "\n".join(lines)
