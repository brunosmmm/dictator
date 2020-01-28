"""Validators."""

from functools import wraps
from typing import Any, Union


class Validator:
    """Validator abstract class."""

    _DEFAULT_NAME: Union[None, str] = None

    @classmethod
    def get_default_name(cls):
        """Get default name."""
        if cls._DEFAULT_NAME is None:
            raise ValueError("default name unknown")

        return cls._DEFAULT_NAME

    def validate(self, _value: Any, **kwargs: Any) -> Any:
        """Perform validation.

        Parameters
        ----------
        _value
            The value to be validated
        kwargs
            Any other metadata for validator
        """
        raise NotImplementedError

    def __call__(self, fn):
        """Validate as decorator."""

        @wraps(fn)
        def _validate(*args, **kwargs):
            _value = fn(*args, **kwargs)
            return self.validate(_value, **kwargs)

        return _validate
