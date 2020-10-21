"""Validators."""

from functools import wraps
from typing import Any, Union, Callable


class Validator:
    """Validator abstract class."""

    _DEFAULT_NAME: Union[None, str] = None

    def __init__(self, after_fn: bool = True, **kwargs):
        """Initialize.

        Parameters
        ----------
        after_fn
          Execute validator after decorated function
        """
        super().__init__(**kwargs)
        self._after = after_fn

    @property
    def after(self):
        """Get if executed after decorated function."""
        return self._after

    @classmethod
    def get_default_name(cls) -> str:
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

    def __call__(self, fn: Callable) -> Callable:
        """Validate as decorator."""

        @wraps(fn)
        def _validate(*args, **kwargs):
            if not self._after:
                # FIXME: getting a double self argument???
                if isinstance(args[0], Validator):
                    _value = self.validate(*args[1:], **kwargs)
                    return fn(args[0], _value, **kwargs)
                _value = self.validate(*args, **kwargs)
                return fn(_value, **kwargs)
            else:
                _value = fn(*args, **kwargs)
                return self.validate(_value, **kwargs)

        return _validate
