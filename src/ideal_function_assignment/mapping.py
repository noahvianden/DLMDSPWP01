"""Exact-x, threshold-based mapping of test points to selected functions."""

from collections.abc import Iterable

import pandas as pd

from .exceptions import MappingError
from .models import MappedPoint, MappingReport, SelectionResult, TestPoint


class PointMapper:
    """Map each test point to at most one eligible selected ideal function."""

    def __init__(self, ideal_functions: pd.DataFrame, selections: Iterable[SelectionResult]) -> None:
        """Create a mapper using exact supplied x values.

        Parameters
        ----------
        ideal_functions:
            Full ideal-function DataFrame with an ``x`` column.
        selections:
            Four deterministic selection results with thresholds.

        Raises
        ------
        MappingError
            If ideal values cannot support exact-x lookups.
        """
        self.selections = tuple(selections)
        if not self.selections:
            raise MappingError("At least one selected ideal function is required for mapping.")
        if "x" not in ideal_functions.columns or ideal_functions["x"].duplicated().any():
            raise MappingError("Ideal functions require unique x values for exact mapping.")
        required_columns = [f"y{selection.ideal_function}" for selection in self.selections]
        missing = [column for column in required_columns if column not in ideal_functions.columns]
        if missing:
            raise MappingError(f"Selected ideal-function columns are unavailable: {', '.join(missing)}")
        try:
            self._ideal_by_x = ideal_functions.set_index("x").sort_index()
        except (KeyError, TypeError, ValueError) as error:
            raise MappingError("Ideal functions cannot be indexed by exact x values.") from error

    def map_points(self, points: Iterable[TestPoint]) -> MappingReport:
        """Evaluate each test point once and return assigned and unassigned states.

        Parameters
        ----------
        points:
            Source-ordered iterator of test points.

        Returns
        -------
        MappingReport
            Successful four-column mappings and explicitly retained non-matches.

        Raises
        ------
        MappingError
            If a test point has no identical supplied x value in the ideal data.
        """
        assignments: list[MappedPoint] = []
        unassigned: list[TestPoint] = []
        for point in points:
            if point.x not in self._ideal_by_x.index:
                raise MappingError(
                    f"Test row {point.source_row} has no exact ideal-function x value: {point.x}"
                )
            ideal_row = self._ideal_by_x.loc[point.x]
            candidates: list[tuple[float, int, str]] = []
            for selection in self.selections:
                try:
                    ideal_y = float(ideal_row[f"y{selection.ideal_function}"])
                except (KeyError, TypeError, ValueError) as error:
                    raise MappingError(
                        f"Could not read selected ideal function y{selection.ideal_function} "
                        f"at x={point.x}."
                    ) from error
                delta_y = abs(point.y - ideal_y)
                if delta_y <= selection.threshold:
                    candidates.append((delta_y, selection.ideal_function, selection.training_series))

            if not candidates:
                unassigned.append(point)
                continue

            delta_y, function_number, _ = min(candidates, key=lambda item: (item[0], item[1], item[2]))
            assignments.append(
                MappedPoint(
                    x=point.x,
                    y=point.y,
                    delta_y=delta_y,
                    ideal_function=function_number,
                )
            )
        return MappingReport(assignments=tuple(assignments), unassigned_points=tuple(unassigned))
