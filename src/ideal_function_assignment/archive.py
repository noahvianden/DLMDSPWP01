"""Controlled extraction of the versioned assignment dataset archive."""

from dataclasses import dataclass
from pathlib import Path
from shutil import copyfileobj
from zipfile import BadZipFile, ZipFile

from .exceptions import InputDataError


@dataclass(frozen=True)
class DatasetPaths:
    """Paths to the three runtime CSV files required by the application."""

    train: Path
    ideal: Path
    test: Path


class DatasetArchive:
    """Extract the supplied archive only when its three CSV files are unavailable."""

    expected_filenames = ("train.csv", "ideal.csv", "test.csv")

    def __init__(self, archive_path: Path, target_directory: Path) -> None:
        """Create an archive adapter.

        Parameters
        ----------
        archive_path:
            Immutable, versioned ``dataset.zip`` path.
        target_directory:
            Ignored runtime directory for the extracted CSV files.
        """
        self.archive_path = archive_path
        self.target_directory = target_directory

    def extract(self) -> DatasetPaths:
        """Return available CSV paths, extracting only the expected archive members.

        Returns
        -------
        DatasetPaths
            Paths for ``train.csv``, ``ideal.csv``, and ``test.csv``.

        Raises
        ------
        InputDataError
            If the archive is unavailable, invalid, or lacks a required CSV member.
        """
        paths = self._dataset_paths()
        if all(path.is_file() for path in (paths.train, paths.ideal, paths.test)):
            return paths

        if not self.archive_path.is_file():
            raise InputDataError(f"Dataset archive is unavailable: {self.archive_path}")

        try:
            self.target_directory.mkdir(parents=True, exist_ok=True)
            with ZipFile(self.archive_path) as archive:
                members = {
                    Path(member.filename).name: member
                    for member in archive.infolist()
                    if not member.is_dir()
                }
                missing = [name for name in self.expected_filenames if name not in members]
                if missing:
                    raise InputDataError(
                        f"Dataset archive {self.archive_path} is missing required members: "
                        f"{', '.join(missing)}"
                    )
                for filename in self.expected_filenames:
                    target = self.target_directory / filename
                    with archive.open(members[filename]) as source, target.open("wb") as destination:
                        copyfileobj(source, destination)
        except (BadZipFile, OSError) as error:
            raise InputDataError(f"Could not extract dataset archive: {self.archive_path}") from error

        return paths

    def _dataset_paths(self) -> DatasetPaths:
        """Build the conventional runtime CSV paths."""
        return DatasetPaths(
            train=self.target_directory / "train.csv",
            ideal=self.target_directory / "ideal.csv",
            test=self.target_directory / "test.csv",
        )
