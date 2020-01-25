"""List-based validators."""

from dictator.validators import Validator
from dictator.validators.base import ValidateType
from dictator.errors import ValidationError
import dictator.config


class ValidateChoice(Validator):
    """Validate choice from list."""

    _DEFAULT_NAME = "choice"

    def __init__(self, *choices):
        """Initialize."""
        super().__init__()
        self._choices = choices

    def __call__(self, fn):
        """Decorator."""

        def _validate(_value, **kwargs):
            """Perform validation."""
            if _value not in self._choices:
                choices = ", ".join(self._choices)
                raise ValidationError(
                    f"value '{_value}' is not a valid choice, choose from [{choices}]"
                )
            return fn(_value, **kwargs)

        return _validate


class SubListValidator(Validator):
    """Automatically validate list elements."""

    _DEFAULT_NAME = "sub_list"

    def __init__(self, required_keys, optional_keys=None):
        """Initialize."""
        super().__init__()
        if not isinstance(required_keys, dict):
            raise TypeError("required_keys must be a dictionary")
        if optional_keys is not None and not isinstance(optional_keys, dict):
            raise TypeError("optional_keys must be a dictionary")
        self._required = required_keys
        self._optional = optional_keys

    def __call__(self, fn):
        """Decorator."""

        @ValidateType((tuple, list))
        def _validate(_value, **kwargs):
            """Perform sub-validation."""
            return fn(
                [
                    dictator.config.validate_config(
                        entry, self._required, self._optional
                    )
                    for entry in _value
                ],
                **kwargs,
            )

        return _validate