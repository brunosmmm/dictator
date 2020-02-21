"""List-based validators."""

from typing import Any, Dict, Union, Type, Callable
from dictator.validators import Validator
from dictator.validators.base import ValidateType
from dictator.errors import ValidationError
import dictator.config

from dictator.validators.base import (
    validate_integer,
    validate_string,
    validate_list,
    validate_dict,
    validate_float,
    validate_boolean,
)


class ValidateChoice(Validator):
    """Validate choice from list."""

    _DEFAULT_NAME = "choice"

    def __init__(self, *choices: Any, **kwargs: Any):
        """Initialize.

        Parameters
        ----------
        choices
            List of choices
        kwargs
            Any other metadata
        """
        super().__init__()
        self._choices = choices

    def validate(self, _value, **kwargs):
        """Perform validation."""
        if _value not in self._choices:
            choices = ", ".join(self._choices)
            raise ValidationError(
                f"value '{_value}' is not a valid choice, choose from [{choices}]"
            )
        return _value


class SubListValidator(Validator):
    """Automatically validate list elements."""

    _DEFAULT_NAME = "sub_list"

    def __init__(
        self,
        required_keys: Dict[str, Any],
        optional_keys: Union[None, Dict[str, Any]] = None,
        **kwargs: Any,
    ):
        """Initialize.

        Parameters
        ----------
        required_keys
            Mapping of required keys and validators
        optional_keys
            Mapping of optional keys and validators
        kwargs
            Any other metadata
        """
        super().__init__()
        if not isinstance(required_keys, dict):
            raise TypeError("required_keys must be a dictionary")
        if optional_keys is not None and not isinstance(optional_keys, dict):
            raise TypeError("optional_keys must be a dictionary")
        self._required = required_keys
        self._optional = optional_keys

    @ValidateType(tuple, list)
    def validate(self, _value, **kwargs):
        """Perform sub-validation."""
        return [
            dictator.config.validate_config(
                entry, self._required, self._optional, _parent=kwargs,
            )
            for entry in _value
        ]


class HomogeneousValidator(Validator):
    """Validate that list elements are homogeneously typed."""

    _DEFAULT_NAME = "list_type"

    DEFAULT_VALIDATOR_BY_TYPE = {
        int: validate_integer,
        str: validate_string,
        list: validate_list,
        dict: validate_dict,
        bool: validate_boolean,
        float: validate_float,
    }

    def __init__(self, validator: Union[Type, Callable], **kwargs: Any):
        """Initialize.

        Parameters
        ----------
        validator
            A validator object
        kwargs
            Any other metadata
        """
        if not callable(validator) or not isinstance(validator, type):
            raise TypeError(
                "validator must either be a callable or a python type"
            )
        super().__init__()
        self._validator = validator

    @ValidateType(tuple, list)
    def validate(self, _value, **kwargs):
        validate_fn = (
            self.DEFAULT_VALIDATOR_BY_TYPE[self._validator]
            if isinstance(self._validator, type)
            else self._validator
        )
        if isinstance(validate_fn, Validator):
            validate_fn = validate_fn.validate
        modified_value = [validate_fn(item) for item in _value]
        return modified_value
