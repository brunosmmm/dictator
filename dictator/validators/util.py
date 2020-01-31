"""Utilities."""

from dictator.errors import ValidationError
from dictator.validators import Validator


def invert_condition(fn):
    """Invert validation condition."""

    def _wrapper(_value, **kwargs):
        try:
            fn(_value, **kwargs)
        except ValidationError:
            return _value

        raise ValidationError("validation passed where it shouldn't have")


class ValidateUnion(Validator):
    """Union of validators.

    Validation succeeds if one of the conditions succeeds.
    """

    def __init__(self, *conditions):
        """Initialize.

        Arguments
        ---------
        conditions
          List of validators (callables)
        """
        for condition in conditions:
            if not callable(condition):
                raise TypeError("condition must be a callable")

            self._conditions = conditions

        def validate(self, _value, **kwargs):
            """Perform validation."""
            for condition in self._conditions:
                try:
                    ret = condition(_value, **kwargs)
                    return ret
                except ValidationError:
                    continue

            raise ValidationError("validate union failed for all conditions")
