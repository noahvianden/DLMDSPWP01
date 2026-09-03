"""Central, project-relative configuration for an application run."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    """Filesystem locations derived from a repository root.

    Parameters
    ----------
    root:
        Repository root that contains the versioned ``data`` directory.
    """

    root: Path

    @property
    def data_dir(self) -> Path:
        """Return the directory containing the archive and runtime CSV files."""
        return self.root / "data"

    @property
    def output_dir(self) -> Path:
        """Return the directory for generated, ignored artefacts."""
        return self.root / "output"


@dataclass(frozen=True)
class AppConfig(ProjectPaths):
    """Configuration for one deterministic assignment run.

    All paths remain relative to ``root`` so the project can be cloned and run on
    another machine without changing source code.

    Parameters
    ----------
    root:
        Repository root.
    archive_filename:
        Name of the versioned source archive in ``data``.
    database_filename:
        Name of the generated SQLite database in ``output``.
    visualization_filename:
        Name of the generated Bokeh HTML file in ``output``.
    summary_filename:
        Name of the generated machine-readable run summary in ``output``.
    log_level:
        Validated minimum level for concise command-line status messages.
    """

    archive_filename: str = "dataset.zip"
    database_filename: str = "ideal_function_assignment.sqlite"
    visualization_filename: str = "ideal_function_assignment.html"
    summary_filename: str = "run_summary.json"
    log_level: str = "INFO"

    def __post_init__(self) -> None:
        """Validate portable filenames, root availability, and the log level.

        Raises
        ------
        ValueError
            If the repository root, output names, or log level are unsuitable
            for a deterministic application run.
        """
        if not self.root.is_dir():
            raise ValueError(f"Repository root is not an accessible directory: {self.root}")
        for filename in (
            self.archive_filename,
            self.database_filename,
            self.visualization_filename,
            self.summary_filename,
        ):
            if not filename or Path(filename).name != filename:
                raise ValueError(f"Configuration filename must be a simple file name: {filename!r}")
        if self.log_level not in {"DEBUG", "INFO", "WARNING", "ERROR"}:
            raise ValueError(f"Unsupported log level: {self.log_level}")

    @classmethod
    def from_root(cls, root: Path | str, log_level: str = "INFO") -> "AppConfig":
        """Create a configuration from a filesystem path.

        Parameters
        ----------
        root:
            Repository root supplied by the command-line interface.

        Returns
        -------
        AppConfig
            A configuration with an absolute, resolved repository root.
        """
        return cls(Path(root).expanduser().resolve(), log_level=log_level)

    @property
    def archive_path(self) -> Path:
        """Return the immutable supplied dataset archive path."""
        return self.data_dir / self.archive_filename

    @property
    def database_path(self) -> Path:
        """Return the SQLite target path for this run."""
        return self.output_dir / self.database_filename

    @property
    def visualization_path(self) -> Path:
        """Return the Bokeh HTML target path for this run."""
        return self.output_dir / self.visualization_filename

    @property
    def summary_path(self) -> Path:
        """Return the JSON run-summary target path for this run."""
        return self.output_dir / self.summary_filename

    def prepare_output_directory(self) -> None:
        """Create the ignored output directory when it does not yet exist.

        Raises
        ------
        OSError
            If the output directory cannot be created.
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)
