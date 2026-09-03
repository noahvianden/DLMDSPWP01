"""Application orchestration, summary generation, and command-line entry point."""

import argparse
import json
import logging
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from .archive import DatasetArchive
from .config import AppConfig
from .database import DatabaseRepository
from .exceptions import IdealFunctionAssignmentError, PersistenceError
from .loaders import IdealFunctionLoader, TestDataLoader, TrainingDataLoader
from .mapping import PointMapper
from .models import RunSummary
from .selection import FunctionSelector
from .visualization import BokehVisualizer


@dataclass(frozen=True)
class RunArtifacts:
    """Generated artefacts and summary returned by a successful application run."""

    database_path: Path
    visualization_path: Path
    summary_path: Path
    summary: RunSummary


class ApplicationRunner:
    """Execute the documented archive-to-output workflow in one controlled order."""

    def __init__(self, config: AppConfig, logger: logging.Logger | None = None) -> None:
        """Create a runner with project-relative configuration and optional logger.

        Parameters
        ----------
        config:
            Valid application paths and output filenames.
        logger:
            Logger receiving concise status messages. The module logger is used
            when none is supplied.
        """
        self.config = config
        self.logger = logger or logging.getLogger(__name__)

    def run(self) -> RunArtifacts:
        """Generate SQLite, Bokeh HTML, and JSON summary artefacts from the archive.

        Returns
        -------
        RunArtifacts
            Paths and numerical summary of the completed deterministic run.

        Raises
        ------
        IdealFunctionAssignmentError
            If an input, selection, mapping, persistence, or visualisation step fails.
        """
        self.config.prepare_output_directory()
        self.logger.info("Resolving supplied dataset archive.")
        dataset = DatasetArchive(self.config.archive_path, self.config.data_dir).extract()

        training_data = TrainingDataLoader(dataset.train).load()
        ideal_functions = IdealFunctionLoader(dataset.ideal).load()
        self.logger.info(
            "Loaded %s training rows and %s ideal-function rows.",
            len(training_data),
            len(ideal_functions),
        )

        repository = DatabaseRepository(self.config.database_path)
        with repository.open_run() as database_run:
            database_run.write_reference_tables(training_data, ideal_functions)

            selections = FunctionSelector().select(training_data, ideal_functions)
            database_run.write_selection_summary(selections)
            self.logger.info(
                "Selected ideal functions: %s",
                ", ".join(
                    f"{selection.training_series}->y{selection.ideal_function}" for selection in selections
                ),
            )

            test_points = TestDataLoader(dataset.test).load()
            mapping_report = PointMapper(ideal_functions, selections).map_points(test_points)
            database_run.write_mappings(mapping_report.assignments)

            summary = RunSummary(
                training_row_count=len(training_data),
                ideal_row_count=len(ideal_functions),
                test_row_count=(
                    mapping_report.assigned_count + mapping_report.unassigned_count
                ),
                selections=selections,
                assigned_count=mapping_report.assigned_count,
                unassigned_count=mapping_report.unassigned_count,
            )
            if summary.assigned_count + summary.unassigned_count != summary.test_row_count:
                raise PersistenceError("Mapping completeness invariant was violated.")

        self.logger.info("Wrote SQLite database: %s", self.config.database_path)
        BokehVisualizer(self.config.visualization_path).create(
            training_data, ideal_functions, selections, mapping_report
        )
        self._write_summary(summary)
        self.logger.info(
            "Mapped %s test points; %s remain unassigned.",
            summary.assigned_count,
            summary.unassigned_count,
        )
        return RunArtifacts(
            database_path=self.config.database_path,
            visualization_path=self.config.visualization_path,
            summary_path=self.config.summary_path,
            summary=summary,
        )

    def _write_summary(self, summary: RunSummary) -> None:
        """Write a stable, atomically replaced JSON run summary.

        Raises
        ------
        PersistenceError
            If the summary file cannot be created or finalised.
        """
        temporary_path = self.config.summary_path.with_name(f".{self.config.summary_path.name}.tmp")
        try:
            temporary_path.write_text(
                json.dumps(summary.as_dict(), indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            temporary_path.replace(self.config.summary_path)
        except (OSError, TypeError, ValueError) as error:
            try:
                if temporary_path.exists():
                    temporary_path.unlink()
            except OSError:
                pass
            raise PersistenceError(
                f"Could not write run summary: {self.config.summary_path}"
            ) from error


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the CLI parser for a reproducible project-root run."""
    parser = argparse.ArgumentParser(
        description="Select ideal functions and map supplied test points deterministically."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root containing data/dataset.zip (default: current directory).",
    )
    parser.add_argument(
        "--log-level",
        choices=("DEBUG", "INFO", "WARNING", "ERROR"),
        default="INFO",
        help="Minimum console log level (default: INFO).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the application from command-line arguments and return an exit code.

    Parameters
    ----------
    argv:
        Optional argument sequence for programmatic invocation.

    Returns
    -------
    int
        Zero after successful artefact generation, otherwise one.
    """
    args = build_argument_parser().parse_args(argv)
    logger = logging.getLogger("ideal_function_assignment")
    try:
        config = AppConfig.from_root(args.root, log_level=args.log_level)
    except ValueError as error:
        logging.basicConfig(
            level=getattr(logging, args.log_level),
            format="%(levelname)s %(name)s: %(message)s",
        )
        logger.error("Invalid application configuration: %s", error)
        return 2

    logging.basicConfig(
        level=getattr(logging, config.log_level),
        format="%(levelname)s %(name)s: %(message)s",
    )
    try:
        artifacts = ApplicationRunner(config, logger).run()
    except IdealFunctionAssignmentError as error:
        logger.error("Application run failed: %s", error)
        return 1

    print(artifacts.summary.to_text())
    print(f"SQLite database: {artifacts.database_path}")
    print(f"Bokeh HTML: {artifacts.visualization_path}")
    print(f"JSON summary: {artifacts.summary_path}")
    return 0
