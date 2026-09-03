"""Unit tests for exact-x threshold mapping and deterministic conflict resolution."""

import pandas as pd
import pytest

from ideal_function_assignment.exceptions import MappingError
from ideal_function_assignment.mapping import PointMapper
from ideal_function_assignment.models import SelectionResult
from ideal_function_assignment.models import TestPoint as AssignmentTestPoint


def _selection(function_number: int, threshold: float, series: str = "y1") -> SelectionResult:
    """Create a compact selection record for in-memory mapping tests."""
    return SelectionResult(series, function_number, 0.0, threshold / 2**0.5, threshold)


def test_mapper_accepts_inside_and_boundary_points_but_rejects_outside_points() -> None:
    """The mapping threshold is inclusive and no-match points are retained separately."""
    mapper = PointMapper(pd.DataFrame({"x": [0.0], "y1": [0.0]}), (_selection(1, 1.0),))
    report = mapper.map_points(
        (
            AssignmentTestPoint(0.0, 0.5, 1),
            AssignmentTestPoint(0.0, 1.0, 2),
            AssignmentTestPoint(0.0, 1.000001, 3),
        )
    )
    assert report.assigned_count == 2
    assert report.unassigned_count == 1
    assert [point.delta_y for point in report.assignments] == pytest.approx([0.5, 1.0])


def test_mapper_prefers_smallest_delta_then_smallest_function_number() -> None:
    """Multiple eligible candidates are resolved independently of selection input order."""
    ideal = pd.DataFrame({"x": [0.0], "y1": [0.0], "y2": [0.2], "y3": [0.0]})
    mapper = PointMapper(
        ideal,
        (_selection(3, 1.0, "y3"), _selection(2, 1.0, "y2"), _selection(1, 1.0, "y1")),
    )
    closer = mapper.map_points((AssignmentTestPoint(0.0, 0.15, 1),)).assignments[0]
    tie = mapper.map_points((AssignmentTestPoint(0.0, 0.1, 2),)).assignments[0]
    assert closer.ideal_function == 2
    assert tie.ideal_function == 1


def test_mapper_rejects_unknown_x_without_interpolation() -> None:
    """An unavailable supplied x value raises a mapping error rather than being approximated."""
    mapper = PointMapper(pd.DataFrame({"x": [0.0], "y1": [0.0]}), (_selection(1, 1.0),))
    with pytest.raises(MappingError, match="no exact ideal-function x value"):
        mapper.map_points((AssignmentTestPoint(0.1, 0.0, 1),))
