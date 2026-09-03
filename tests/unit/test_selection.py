"""Unit tests for deterministic, x-aligned SSE selection."""

import math

import pandas as pd
import pytest

from ideal_function_assignment.exceptions import FunctionSelectionError
from ideal_function_assignment.selection import FunctionSelector


def _ideal_frame(x_values: list[float], overrides: dict[int, list[float]]) -> pd.DataFrame:
    """Build a minimal in-memory full ideal-function table for rule tests."""
    data: dict[str, list[float]] = {"x": x_values}
    for number in range(1, 51):
        data[f"y{number}"] = overrides.get(number, [100.0] * len(x_values))
    return pd.DataFrame(data)


def _training_frame(x_values: list[float], y1: list[float]) -> pd.DataFrame:
    """Build four in-memory training series while varying only y1 as needed."""
    return pd.DataFrame(
        {
            "x": x_values,
            "y1": y1,
            "y2": [2.0] * len(x_values),
            "y3": [3.0] * len(x_values),
            "y4": [4.0] * len(x_values),
        }
    )


def test_selector_calculates_hand_checked_sse_and_maximum_deviation() -> None:
    """SSE uses squared values while the threshold uses the absolute maximum difference."""
    training = _training_frame([0.0, 1.0], [1.0, 3.0])
    ideal = _ideal_frame(
        [1.0, 0.0],
        {
            1: [0.0, 0.0],
            2: [2.0, 0.0],
            3: [9.0, 9.0],
            4: [10.0, 10.0],
        },
    )
    selection = FunctionSelector().select(training, ideal)[0]
    assert selection.ideal_function == 2
    assert selection.sse == pytest.approx(2.0)
    assert selection.max_deviation == pytest.approx(1.0)
    assert selection.threshold == pytest.approx(math.sqrt(2))


def test_selector_breaks_exact_sse_ties_by_smallest_function_number() -> None:
    """Equal candidate SSE values select the lower ideal-function suffix deterministically."""
    training = _training_frame([0.0, 1.0], [0.0, 0.0])
    ideal = _ideal_frame(
        [0.0, 1.0],
        {
            1: [0.0, 0.0],
            2: [0.0, 0.0],
            3: [3.0, 3.0],
            4: [4.0, 4.0],
        },
    )
    assert FunctionSelector().select(training, ideal)[0].ideal_function == 1


def test_selector_rejects_unaligned_x_sets() -> None:
    """Reference rows are aligned by exact x keys rather than incidental positions."""
    training = _training_frame([0.0, 1.0], [0.0, 1.0])
    ideal = _ideal_frame([0.0, 2.0], {})
    with pytest.raises(FunctionSelectionError, match="same exact x values"):
        FunctionSelector().select(training, ideal)
