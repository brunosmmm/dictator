"""Standard validators."""

import re
import dictator.config

HEX_REGEX = re.compile(r"^(0x)?([0-9A-Fa-f]+)$")
BIN_REGEX = re.compile(r"^(0b)?([0-1]+)$")


class Validator:
    """Validator abstract class."""

    _DEFAULT_NAME = None

    @classmethod
    def get_default_name(cls):
        """Get default name."""
        if cls._DEFAULT_NAME is None:
            raise ValueError("default name unknown")

        return cls._DEFAULT_NAME


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
                raise dictator.config.ValidationError(
                    f"value must be of type '{type_name}'"
                )

            return fn(_value, **kwargs)

        return _validate


class ValidateIntRange(Validator):
    """Integer range validator."""

    _DEFAULT_NAME = "int_range"

    def __init__(self, start, end):
        """Initialize."""
        super().__init__()
        self._start = start
        self._end = end

    def __call__(self, fn):
        """Decorator."""

        @validate_integer
        def _validate(_value, **kwargs):
            """Perform validation."""
            if _value < self._start or _value > self._end:
                raise dictator.config.ValidationError(
                    "value out of [{}, {}] range".format(self._start, self._end)
                )
            return fn(_value, **kwargs)

        return _validate


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
                raise dictator.config.ValidationError(
                    f"value '{_value}' is not a valid choice, choose from [{choices}]"
                )
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
                    print(f"binary: {_value}")
                    return fn(int(h.group(2), 2), **kwargs)
                print(f"hex: {_value}")
                return fn(int(h.group(2), 16), **kwargs)

            raise dictator.config.ValidationError("cannot validate as integer")
        elif isinstance(_value, int):
            return fn(_value, **kwargs)

        raise dictator.config.ValidationError("cannot validate as integer")

    return _validate


def validate_positive_integer(fn):
    """Validate positive integer."""

    @validate_integer
    def _validate(_value, **kwargs):
        """Perform validation."""
        if _value < 0:
            raise dictator.config.ValidationError(
                "value must be a positive integer"
            )
        return fn(_value, **kwargs)

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


def validate_int_percent(fn):
    """Validate percent value (integer)."""

    @ValidateIntRange(0, 100)
    def _validate(_value, **kwargs):
        """Perform validation."""
        return fn(_value, **kwargs)

    return _validate
