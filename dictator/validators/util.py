"""Utilities."""

from typing import Callable, Union, Type, Any

from dictator.errors import ValidationError
from dictator.validators import Validator
from dictator.validators.base import DEFAULT_VALIDATOR_BY_TYPE


class InvertValidation(Validator):
    """Invert validation condition."""

    def __init__(self, condition=None):
        """Initialize."""
        if (
            condition is not None
            and not isinstance(condition, type)
            and not callable(condition)
        ):
            raise TypeError(
                "condition must either be: None, a type or a callable"
            )
        self._condition = condition

    def validate(self, _value, **kwargs):
        """Perform validation."""
        if self._condition is not None:
            try:
                _ = (
                    DEFAULT_VALIDATOR_BY_TYPE[self._condition].validate(
                        _value, **kwargs
                    )
                    if isinstance(self._condition, type)
                    else self._condition(_value, **kwargs)
                )
            except ValidationError:
                return _value

            raise ValidationError("validation passed where it shouldn't have")

    def __call__(self, fn):
        """Use as decorator."""

        def _wrapper(_value, **kwargs):
            try:
                fn(_value, **kwargs)
            except ValidationError:
                return _value

            raise ValidationError("validation passed where it shouldn't have")

        return _wrapper


# alias
invert_validation = InvertValidation()


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
        super().__init__(**kwargs)
        for condition in conditions:
            if (
                not callable(condition)
                and not isinstance(condition, type)
                and condition is not None
            ):
                raise TypeError("condition must be a callable, type or None")

            self._conditions = conditions

    def validate(self, _value, **kwargs):
        """Perform validation."""
        for condition in self._conditions:
            try:
                if isinstance(condition, type):
                    ret = DEFAULT_VALIDATOR_BY_TYPE[condition].validate(
                        _value, **kwargs
                    )
                elif isinstance(condition, Validator):
                    ret = condition.validate(_value, **kwargs)
                elif condition is None:
                    if _value is not None:
                        continue
                    ret = _value
                else:
                    ret = condition(_value, **kwargs)
                return ret
            except ValidationError:
                continue

        raise ValidationError("validate union failed for all conditions")
