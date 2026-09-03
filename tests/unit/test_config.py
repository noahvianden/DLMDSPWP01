"""Baseline tests for project path configuration."""

from pathlib import Path

from ideal_function_assignment.config import ProjectPaths


def test_project_paths_are_derived_from_repository_root() -> None:
    """Data and output directories remain relative to the configured root."""
    paths = ProjectPaths(Path("/project"))
    assert paths.data_dir == Path("/project/data")
    assert paths.output_dir == Path("/project/output")
