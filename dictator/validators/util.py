"""Utilities."""

from typing import Callable, Union, Type, Any

from dictator.errors import ValidationError
from dictator.validators import Validator
from dictator.validators.base import DEFAULT_VALIDATOR_BY_TYPE


def invert_condition(fn: Callable) -> Callable:
    """Invert validation condition."""

    def _wrapper(_value, **kwargs):
        try:
            fn(_value, **kwargs)
        except ValidationError:
            return _value

        raise ValidationError("validation passed where it shouldn't have")

    return _wrapper


class ValidateUnion(Validator):
    """Union of validators.

    Validation succeeds if one of the conditions succeeds.
    """

    def __init__(self, *conditions: Union[Callable, Type], **kwargs: Any):
        """Initialize.

        Arguments
        ---------
        conditions
          List of validators (callables)
        kwargs
          Any other metadata
        """
        for condition in conditions:
            if not callable(condition) and not isinstance(condition, type):
                raise TypeError("condition must be a callable or a type")

            self._conditions = conditions

    def validate(self, _value, **kwargs):
        """Perform validation."""
        for condition in self._conditions:
            try:
                ret = (
                    DEFAULT_VALIDATOR_BY_TYPE[condition].validate(
                        _value, **kwargs
                    )
                    if isinstance(condition, type)
                    else condition(_value, **kwargs)
                )
                return ret
            except ValidationError:
                continue

        raise ValidationError("validate union failed for all conditions")
