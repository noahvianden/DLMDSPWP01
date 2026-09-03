"""Domain exceptions with contextual, chained failure reporting."""


class IdealFunctionAssignmentError(Exception):
    """Base class for expected application-domain failures."""


class InputDataError(IdealFunctionAssignmentError):
    """Raised when an archive or supplied CSV input cannot be used."""


class DataValidationError(InputDataError):
    """Raised when a supplied CSV violates the loader input contract."""


class FunctionSelectionError(IdealFunctionAssignmentError):
    """Raised when ideal functions cannot be selected deterministically."""


class MappingError(IdealFunctionAssignmentError):
    """Raised when a test point cannot be mapped at its exact supplied x value."""


class PersistenceError(IdealFunctionAssignmentError):
    """Raised when a SQLite artefact cannot be written transactionally."""


class VisualizationError(IdealFunctionAssignmentError):
    """Raised when the Bokeh HTML artefact cannot be generated."""
