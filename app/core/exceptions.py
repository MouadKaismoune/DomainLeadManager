"""Application-specific exceptions."""


class ValidationError(ValueError):
    """Raised when user input violates a business rule."""


class DuplicateRecordError(ValueError):
    """Raised when an exact duplicate record already exists."""
