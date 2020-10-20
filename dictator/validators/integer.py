"""Composite integer validators."""

from dictator.validators import Validator
from dictator.validators.base import ValidatorFactory, validate_integer_pre
from dictator.errors import ValidationError
from typing import Any, Union


class ValidateIntRange(Validator):
    """Integer range validator."""

    _DEFAULT_NAME = "int_range"

    def __init__(
        self, start: Union[int, None], end: Union[int, None], **kwargs: Any
    ):
        """Initialize.

        Parameters
        ----------
        start
            Start of range interval (can be None for open interval)
        end
            End of range interval (can be None for open interval)
        kwargs
            Any other metadata
        """
        super().__init__()
        self._start = start
        self._end = end

    @validate_integer_pre
    def validate(self, _value, **kwargs):
        """Perform validation."""
        if (self._start is not None and _value < self._start) or (
            self._end is not None and _value > self._end
        ):
            raise ValidationError(
                "value out of [{}, {}] range".format(self._start, self._end)
            )
        return _value


validate_positive_integer = ValidatorFactory(ValidateIntRange(0, None))
validate_percent_integer = ValidatorFactory(ValidateIntRange(0, 100))
