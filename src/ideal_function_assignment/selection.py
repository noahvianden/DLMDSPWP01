"""Deterministic least-squares selection of supplied ideal functions."""

import math

import pandas as pd

from .exceptions import FunctionSelectionError
from .models import SelectionResult


class FunctionSelector:
    """Select one lowest-SSE supplied ideal function for each training series."""

    training_columns = tuple(f"y{number}" for number in range(1, 5))
    ideal_columns = tuple(f"y{number}" for number in range(1, 51))

    def select(
        self, training_data: pd.DataFrame, ideal_functions: pd.DataFrame
    ) -> tuple[SelectionResult, ...]:
        """Calculate four deterministic selections and their mapping thresholds.

        The supplied x values are aligned by their actual keys, not by arbitrary
        input row position. Exact SSE ties select the smallest ideal-function
        number.

        Parameters
        ----------
        training_data:
            DataFrame containing ``x`` and four training columns.
        ideal_functions:
            DataFrame containing ``x`` and fifty candidate function columns.

        Returns
        -------
        tuple[SelectionResult, ...]
            One selection record for every training column in numeric order.

        Raises
        ------
        FunctionSelectionError
            If columns, x keys, or numeric selection values are unusable.
        """
        training = self._index_frame(training_data, ("x",) + self.training_columns, "training")
        ideal = self._index_frame(ideal_functions, ("x",) + self.ideal_columns, "ideal")
        if not training.index.equals(ideal.index):
            raise FunctionSelectionError(
                "Training and ideal functions do not have the same exact x values."
            )

        selections: list[SelectionResult] = []
        for training_column in self.training_columns:
            candidates: list[tuple[float, int, float]] = []
            try:
                training_values = training[training_column].astype(float)
                for function_number, ideal_column in enumerate(self.ideal_columns, start=1):
                    differences = training_values - ideal[ideal_column].astype(float)
                    sse = float((differences**2).sum())
                    max_deviation = float(differences.abs().max())
                    candidates.append((sse, function_number, max_deviation))
            except (TypeError, ValueError) as error:
                raise FunctionSelectionError(
                    f"Could not calculate SSE for training series {training_column}."
                ) from error

            sse, function_number, max_deviation = min(candidates, key=lambda item: (item[0], item[1]))
            selections.append(
                SelectionResult(
                    training_series=training_column,
                    ideal_function=function_number,
                    sse=sse,
                    max_deviation=max_deviation,
                    threshold=math.sqrt(2) * max_deviation,
                )
            )
        return tuple(selections)

    def _index_frame(
        self, frame: pd.DataFrame, expected_columns: tuple[str, ...], label: str
    ) -> pd.DataFrame:
        """Check a selection input and return it sorted and indexed by x."""
        missing = [column for column in expected_columns if column not in frame.columns]
        if missing:
            raise FunctionSelectionError(
                f"{label.capitalize()} data is missing required columns: {', '.join(missing)}"
            )
        selected = frame.loc[:, expected_columns].copy()
        if selected["x"].duplicated().any():
            raise FunctionSelectionError(f"{label.capitalize()} data contains duplicate x values.")
        try:
            return selected.set_index("x").sort_index()
        except (KeyError, TypeError, ValueError) as error:
            raise FunctionSelectionError(
                f"{label.capitalize()} data cannot be indexed by x values."
            ) from error
