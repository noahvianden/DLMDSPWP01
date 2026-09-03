"""Integration test for the generated Bokeh HTML evidence output."""

from pathlib import Path

from ideal_function_assignment.loaders import TestDataLoader as AssignmentTestDataLoader
from ideal_function_assignment.mapping import PointMapper
from ideal_function_assignment.selection import FunctionSelector
from ideal_function_assignment.visualization import BokehVisualizer


def test_bokeh_html_contains_comparison_and_deviation_evidence(
    tmp_path: Path, official_dataset_paths: object, official_frames: object
) -> None:
    """The visualisation writes panels, legends, hover data, and unassigned summary text."""
    selections = FunctionSelector().select(official_frames.training, official_frames.ideal)
    report = PointMapper(official_frames.ideal, selections).map_points(
        AssignmentTestDataLoader(official_dataset_paths.test).load()
    )
    output_path = BokehVisualizer(tmp_path / "assignment.html").create(
        official_frames.training, official_frames.ideal, selections, report
    )
    html = output_path.read_text(encoding="utf-8")
    assert output_path.is_file()
    assert "Assigned test-point deviations and selection thresholds" in html
    assert "Unassigned test points:" in html
    assert "training y1" in html
    assert "ideal y13" in html
    assert "unassigned test point" in html
    assert "absolute delta_y" in html
