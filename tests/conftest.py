"""Shared access to the versioned official assignment archive for tests."""

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import pytest

from ideal_function_assignment.archive import DatasetArchive, DatasetPaths
from ideal_function_assignment.loaders import IdealFunctionLoader, TrainingDataLoader


@dataclass(frozen=True)
class OfficialFrames:
    """Validated reference DataFrames loaded from the supplied archive."""

    training: pd.DataFrame
    ideal: pd.DataFrame


@pytest.fixture(scope="session")
def repository_root() -> Path:
    """Return the canonical repository root without relying on the current directory."""
    return Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def official_archive_path(repository_root: Path) -> Path:
    """Return the versioned official dataset archive path."""
    return repository_root / "data" / "dataset.zip"


@pytest.fixture
def official_dataset_paths(tmp_path: Path, official_archive_path: Path) -> DatasetPaths:
    """Extract only the official archive into an isolated test-runtime directory."""
    return DatasetArchive(official_archive_path, tmp_path / "runtime_data").extract()


@pytest.fixture
def official_frames(official_dataset_paths: DatasetPaths) -> OfficialFrames:
    """Load validated official training and ideal-function reference frames."""
    return OfficialFrames(
        training=TrainingDataLoader(official_dataset_paths.train).load(),
        ideal=IdealFunctionLoader(official_dataset_paths.ideal).load(),
    )
