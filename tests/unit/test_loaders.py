"""Unit tests for loader error translation without stored synthetic CSV fixtures."""

import io
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from ideal_function_assignment.exceptions import DataValidationError, InputDataError
from ideal_function_assignment.loaders import (
    IdealFunctionLoader,
    TrainingDataLoader,
)
from ideal_function_assignment.loaders import (
    TestDataLoader as AssignmentTestDataLoader,
)


def test_reference_loaders_accept_the_official_archive(official_dataset_paths: object) -> None:
    """Official reference CSV files load into their documented shapes."""
    training_path = official_dataset_paths.train
    ideal_path = official_dataset_paths.ideal
    assert TrainingDataLoader(training_path).load().shape == (400, 5)
    assert IdealFunctionLoader(ideal_path).load().shape == (400, 51)


@pytest.mark.parametrize(
    ("frame", "message"),
    [
        (pd.DataFrame({"x": [0.0], "y1": [1.0]}), "Unexpected CSV header"),
        (
            pd.DataFrame(
                {"x": [0.0], "y1": ["not-a-number"], "y2": [0.0], "y3": [0.0], "y4": [0.0]}
            ),
            "non-numeric",
        ),
        (
            pd.DataFrame({"x": [0.0], "y1": [np.nan], "y2": [0.0], "y3": [0.0], "y4": [0.0]}),
            "missing values",
        ),
        (
            pd.DataFrame({"x": [0.0], "y1": [np.inf], "y2": [0.0], "y3": [0.0], "y4": [0.0]}),
            "non-finite",
        ),
        (
            pd.DataFrame({"x": [0.0, 0.0], "y1": [0.0, 1.0], "y2": [0.0, 1.0], "y3": [0.0, 1.0], "y4": [0.0, 1.0]}),
            "duplicate x",
        ),
        (pd.DataFrame(columns=["x", "y1", "y2", "y3", "y4"]), "no data rows"),
    ],
)
def test_training_loader_rejects_invalid_reference_frames(
    monkeypatch: pytest.MonkeyPatch,
    official_dataset_paths: object,
    frame: pd.DataFrame,
    message: str,
) -> None:
    """Header, numeric, missing-value, finite-value, and duplicate-x rules are enforced."""
    monkeypatch.setattr("ideal_function_assignment.loaders.pd.read_csv", lambda _: frame)
    with pytest.raises(DataValidationError, match=message):
        TrainingDataLoader(official_dataset_paths.train).load()


def test_loader_reports_missing_reference_file(tmp_path: Path) -> None:
    """A non-existent reference CSV is translated to an input-domain error."""
    with pytest.raises(InputDataError, match="unavailable"):
        TrainingDataLoader(tmp_path / "missing.csv").load()


def test_test_loader_is_source_ordered_and_permits_repeated_x(
    official_dataset_paths: object,
) -> None:
    """The official test data remains an iterator and may repeat x values."""
    points = list(AssignmentTestDataLoader(official_dataset_paths.test).load())
    assert len(points) == 100
    assert points[0].source_row == 1
    assert len({point.x for point in points}) < len(points)


@pytest.mark.parametrize(
    ("csv_text", "error_match"),
    [
        ("x,wrong\n0,1\n", "Unexpected CSV header"),
        ("x,y\nnot-a-number,1\n", "non-numeric"),
        ("x,y\n0,nan\n", "non-finite"),
    ],
)
def test_test_loader_translates_virtual_invalid_rows_without_csv_fixtures(
    monkeypatch: pytest.MonkeyPatch, csv_text: str, error_match: str
) -> None:
    """Virtual file handles exercise test-row validation without writing fixture files."""
    loader = AssignmentTestDataLoader(Path("/virtual/test.csv"))
    monkeypatch.setattr(loader, "_require_file", lambda: None)
    monkeypatch.setattr(Path, "open", lambda *_args, **_kwargs: io.StringIO(csv_text))
    with pytest.raises(DataValidationError, match=error_match):
        list(loader.load())
