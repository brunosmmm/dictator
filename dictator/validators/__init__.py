"""Validators."""

from functools import wraps


class Validator:
    """Validator abstract class."""

    _DEFAULT_NAME = None

    @classmethod
    def get_default_name(cls):
        """Get default name."""
        if cls._DEFAULT_NAME is None:
            raise ValueError("default name unknown")

        return cls._DEFAULT_NAME

    def validate(self, _value, **kwargs):
        """Perform validation."""
        raise NotImplementedError

    def __call__(self, fn):
        """Validate as decorator."""

        @wraps(fn)
        def _validate(*args, **kwargs):
            _value = fn(*args, **kwargs)
            return self.validate(_value, **kwargs)

        return _validate
