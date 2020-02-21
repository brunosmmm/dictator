"""Base validators."""

import re
from dictator.errors import ValidationError
from dictator.validators import Validator
from typing import Type, Callable, Any, Tuple, Union

HEX_REGEX = re.compile(r"^(0x)?([0-9A-Fa-f]+)$")
BIN_REGEX = re.compile(r"^(0b)?([0-1]+)$")


class ValidateType(Validator):
    """Type validator."""

    _DEFAULT_NAME = "type"

    def __init__(self, *_types: Type):
        """Initialize.

        Parameters
        ----------
        type
            The expected python type
        """
        super().__init__()
        self._types = _types

    @property
    def target_types(self) -> Tuple[Type, ...]:
        """Get target type."""
        return self._types

    def validate(self, _value, **kwargs):
        """Perform validation."""
        if not isinstance(_value, self.target_types):
            raise ValidationError(f"value has unexpected type")

        return _value


class ValidatorFactory(Validator):
    """Validator factory."""

    def __init__(self, validate_fn: Union[Callable, Validator], **kwargs):
        """Initialize.

        Parameters
        ----------
        validate_fn
            Some callable that performs actual validation
        """
        super().__init__(**kwargs)
        if not callable(validate_fn):
            raise TypeError("validate_fn must be callable")
        if isinstance(validate_fn, Validator):
            self._validatefn = validate_fn.validate
        else:
            self._validatefn = validate_fn

    def validate(self, _value, **kwargs):
        """Perform validation."""
        return self._validatefn(_value, **kwargs)


def _validate_integer(_value: Any, **kwargs: Any) -> int:
    """Validate integer value.

    Parameters
    ----------
    _value
        Some value
    kwargs
        Other metadata
    """
    if isinstance(_value, str):
        # try converting
        h = HEX_REGEX.match(_value)
        b = BIN_REGEX.match(_value)
        if h is not None:
            if h.group(1) is None and b is not None:
                # is actually binary
                return int(h.group(2), 2)
            return int(h.group(2), 16)

        raise ValidationError("cannot validate as integer")
    elif isinstance(_value, bool):
        raise ValidationError("cannot validate as integer, got boolean")
    elif isinstance(_value, int):
        return _value

    raise ValidationError("cannot validate as integer")


validate_string = ValidatorFactory(ValidateType(str))
validate_list = ValidatorFactory(ValidateType(tuple, list))
validate_dict = ValidatorFactory(ValidateType(dict))
validate_boolean = ValidatorFactory(ValidateType(bool))
validate_float = ValidatorFactory(ValidateType(float))
validate_integer = ValidatorFactory(_validate_integer)

validate_string_pre = ValidatorFactory(ValidateType(str), after_fn=False)
validate_list_pre = ValidatorFactory(ValidateType(tuple, list), after_fn=False)
validate_dict_pre = ValidatorFactory(ValidateType(dict), after_fn=False)
validate_boolean_pre = ValidatorFactory(ValidateType(bool), after_fn=False)
validate_float_pre = ValidatorFactory(ValidateType(float), after_fn=False)
validate_integer_pre = ValidatorFactory(_validate_integer, after_fn=False)


def validate_null(_value: Any, **kwargs: Any) -> None:
    """Validate null value.

    Parameters
    ---------
    _value
        Some value
    kwargs
        Other metadata
    """
    if _value is not None:
        raise ValidationError("value is not null")
    return _value


DEFAULT_VALIDATOR_BY_TYPE = {
    int: validate_integer,
    str: validate_string,
    list: validate_list,
    dict: validate_dict,
    bool: validate_boolean,
    float: validate_float,
}
