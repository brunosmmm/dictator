"""Composite integer validators."""

from dictator.validators import Validator
from dictator.validators.base import validate_integer
from dictator.errors import ValidationError


class ValidateIntRange(Validator):
    """Integer range validator."""

    _DEFAULT_NAME = "int_range"

    def __init__(self, start, end, **kwargs):
        """Initialize."""
        super().__init__()
        self._start = start
        self._end = end

    def validate(self, _value, **kwargs):
        """Perform validation."""
        _value = validate_integer(_value, **kwargs)
        if (self._start is not None and _value < self._start) or (
            self._end is not None and _value > self._end
        ):
            raise ValidationError(
                "value out of [{}, {}] range".format(self._start, self._end)
            )
        return _value


@ValidateIntRange(0, None)
def validate_positive_integer(_value, **kwargs):
    return _value


@ValidateIntRange(0, 100)
def validate_percent_integer(_value, **kwargs):
    """Validate percent value (integer)."""
    return _value
