"""Base validators."""

import re
from dictator.errors import ValidationError
from dictator.validators import Validator

HEX_REGEX = re.compile(r"^(0x)?([0-9A-Fa-f]+)$")
BIN_REGEX = re.compile(r"^(0b)?([0-1]+)$")


class ValidateType(Validator):
    """Type validator."""

    _DEFAULT_NAME = "type"

    def __init__(self, _type):
        """Initialize."""
        super().__init__()
        self._type = _type

    @property
    def target_type(self):
        """Get target type."""
        return self._type

    def validate(self, _value, **kwargs):
        """Perform validation."""
        if not isinstance(_value, self.target_type):
            if hasattr(self.target_type, "__name__"):
                type_name = self.target_type.__name__
            else:
                type_name = self.target_type
            raise ValidationError(f"value must be of type '{type_name}'")

        return _value


def validate_integer(_value, **kwargs):
    """Validate integer value."""
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


@ValidateType(str)
def validate_string(_value, **kwargs):
    """Validate string value."""
    return _value


@ValidateType((tuple, list))
def validate_list(_value, **kwargs):
    """Validate lists."""
    return _value


@ValidateType(dict)
def validate_dict(_value, **kwargs):
    """Validate dictionaries."""
    return _value


@ValidateType(bool)
def validate_boolean(_value, **kwargs):
    """Validate boolean value."""
    return _value


@ValidateType(float)
def validate_float(_value, **kwargs):
    """Validate floating point value."""
    return _value


def validate_null(_value, **kwargs):
    """Validate null value."""
    if _value is not None:
        raise ValidationError("value is not null")
    return _value
