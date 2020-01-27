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

    def __call__(self, fn):
        """Decorator."""

        def _validate(_value, **kwargs):
            """Perform validation."""
            if not isinstance(_value, self.target_type):
                if hasattr(self.target_type, "__name__"):
                    type_name = self.target_type.__name__
                else:
                    type_name = self.target_type
                raise ValidationError(f"value must be of type '{type_name}'")

            return fn(_value, **kwargs)

        return _validate


def validate_integer(fn):
    """Validate integer."""

    def _validate(_value, **kwargs):
        """Perform validation."""
        if isinstance(_value, str):
            # try converting
            h = HEX_REGEX.match(_value)
            b = BIN_REGEX.match(_value)
            if h is not None:
                if h.group(1) is None and b is not None:
                    # is actually binary
                    return fn(int(h.group(2), 2), **kwargs)
                return fn(int(h.group(2), 16), **kwargs)

            raise ValidationError("cannot validate as integer")
        elif isinstance(_value, bool):
            raise ValidationError("cannot validate as integer, got boolean")
        elif isinstance(_value, int):
            return fn(_value, **kwargs)

        raise ValidationError("cannot validate as integer")

    return _validate


def validate_string(fn):
    """Validate string value."""

    @ValidateType(str)
    def _validate(_value, **kwargs):
        """Perform validation."""
        return fn(_value, **kwargs)

    return _validate


def validate_list(fn):
    """Validate lists."""

    @ValidateType((tuple, list))
    def _validate(_value, **kwargs):
        """Perform validation"""
        return fn(_value, **kwargs)

    return _validate


def validate_dict(fn):
    """Validate dictionaries."""

    @ValidateType(dict)
    def _validate(_value, **kwargs):
        """Perform validation."""
        return fn(_value, **kwargs)

    return _validate


def validate_boolean(fn):
    """Validate boolean value."""

    @ValidateType(bool)
    def _validate(_value, **kwargs):
        return fn(_value, **kwargs)

    return _validate


def validate_float(fn):
    """Validate floating point value."""

    @ValidateType(float)
    def _validate(_value, **kwargs):
        return fn(_value, **kwargs)

    return _validate


def validate_null(fn):
    """Validate null value."""

    def _validate(_value, **kwargs):
        if _value is not None:
            raise ValidationError("value is not null")
        return fn(_value, **kwargs)

    return _validate
