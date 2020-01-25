"""Composite integer validators."""

from dictator.validators import Validator
from dictator.validators.base import validate_integer
from dictator.errors import ValidationError


class ValidateIntRange(Validator):
    """Integer range validator."""

    _DEFAULT_NAME = "int_range"

    def __init__(self, start, end):
        """Initialize."""
        super().__init__()
        self._start = start
        self._end = end

    def __call__(self, fn):
        """Decorator."""

        @validate_integer
        def _validate(_value, **kwargs):
            """Perform validation."""
            if _value < self._start or _value > self._end:
                raise ValidationError(
                    "value out of [{}, {}] range".format(self._start, self._end)
                )
            return fn(_value, **kwargs)

        return _validate


def validate_positive_integer(fn):
    """Validate positive integer."""

    @validate_integer
    def _validate(_value, **kwargs):
        """Perform validation."""
        if _value < 0:
            raise ValidationError("value must be a positive integer")
        return fn(_value, **kwargs)

    return _validate


def validate_percent_integer(fn):
    """Validate percent value (integer)."""

    @ValidateIntRange(0, 100)
    def _validate(_value, **kwargs):
        """Perform validation."""
        return fn(_value, **kwargs)

    return _validate
