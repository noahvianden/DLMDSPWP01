"""Central configuration for local data and generated outputs."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    """Filesystem locations used by an application run."""

    root: Path

    @property
    def data_dir(self) -> Path:
        """Return the directory containing locally supplied CSV files."""
        return self.root / "data"

    @property
    def output_dir(self) -> Path:
        """Return the directory for generated, ignored artefacts."""
        return self.root / "output"
