"""Base Validators."""
"""Validators."""


class Validator:
    """Validator abstract class."""

    _DEFAULT_NAME = None

    @classmethod
    def get_default_name(cls):
        """Get default name."""
        if cls._DEFAULT_NAME is None:
            raise ValueError("default name unknown")

        return cls._DEFAULT_NAME
