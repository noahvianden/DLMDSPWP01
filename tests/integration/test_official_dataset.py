"""Acceptance checks against the supplied, versioned assignment archive."""

import pytest

from ideal_function_assignment.loaders import TestDataLoader as AssignmentTestDataLoader
from ideal_function_assignment.mapping import PointMapper
from ideal_function_assignment.selection import FunctionSelector


def test_official_archive_matches_selection_and_mapping_oracles(
    official_dataset_paths: object, official_frames: object
) -> None:
    """The official dataset reproduces the precomputed selection and mapping outcomes."""
    selections = FunctionSelector().select(official_frames.training, official_frames.ideal)
    points = tuple(AssignmentTestDataLoader(official_dataset_paths.test).load())
    report = PointMapper(official_frames.ideal, selections).map_points(points)

    assert [selection.ideal_function for selection in selections] == [13, 24, 36, 40]
    assert [selection.sse for selection in selections] == pytest.approx(
        [34.0807075815, 33.4517609531, 35.5727003958, 34.9988748132], abs=1e-10
    )
    assert [selection.max_deviation for selection in selections] == pytest.approx(
        [0.499221, 0.499, 0.498943, 0.499779], abs=1e-12
    )
    assert report.assigned_count == 34
    assert report.unassigned_count == 66
    assert report.assigned_count + report.unassigned_count == len(points) == 100


def test_official_archive_has_documented_multiple_candidate_resolution(
    official_dataset_paths: object, official_frames: object
) -> None:
    """The known double candidate at zero-based source index 50 is assigned to y24."""
    selections = FunctionSelector().select(official_frames.training, official_frames.ideal)
    points = tuple(AssignmentTestDataLoader(official_dataset_paths.test).load())
    report = PointMapper(official_frames.ideal, selections).map_points(points)
    target = points[50]
    candidates = [
        selection
        for selection in selections
        if abs(
            target.y
            - float(
                official_frames.ideal.set_index("x").loc[target.x, f"y{selection.ideal_function}"]
            )
        )
        <= selection.threshold
    ]
    mapped = next(
        mapping
        for mapping in report.assignments
        if mapping.x == target.x and mapping.y == target.y
    )
    assert (target.x, target.y) == pytest.approx((-1.6, -8.079187))
    assert [selection.ideal_function for selection in candidates] == [13, 24]
    assert mapped.ideal_function == 24
    assert mapped.delta_y == pytest.approx(0.112813)


def test_official_archive_candidate_count_distribution(
    official_dataset_paths: object, official_frames: object
) -> None:
    """Exactly 33 points have one candidate and one point has two candidates."""
    selections = FunctionSelector().select(official_frames.training, official_frames.ideal)
    ideal_by_x = official_frames.ideal.set_index("x")
    candidate_counts = []
    for point in AssignmentTestDataLoader(official_dataset_paths.test).load():
        candidate_counts.append(
            sum(
                abs(point.y - float(ideal_by_x.loc[point.x, f"y{selection.ideal_function}"]))
                <= selection.threshold
                for selection in selections
            )
        )
    assert candidate_counts.count(0) == 66
    assert candidate_counts.count(1) == 33
    assert candidate_counts.count(2) == 1
