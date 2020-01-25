"""Default Validators."""

from dictator.validators import (
    ValidateChoice,
    ValidateIntRange,
    validate_integer,
    validate_positive_integer,
    validate_string,
    validate_list,
    validate_dict,
    validate_int_percent,
)

VALIDATE_DECORATORS_NOARGS = (
    validate_integer,
    validate_positive_integer,
    validate_string,
    validate_list,
    validate_dict,
    validate_int_percent,
)

VALIDATE_DECORATORS_ARGS = (ValidateChoice, ValidateIntRange)


def _make_default(decorator):
    @decorator
    def _validate_fn(_value, **kwargs):
        return _value

    return _validate_fn


def _make_default_with_args(decorator):
    def _outer_validate_fn(*args):
        @decorator(*args)
        def _validate_fn(_value, **kwargs):
            return _value

        return _validate_fn

    return _outer_validate_fn


_DEFAULT_NAMES = [
    "_".join(dec.__name__.split("_")[1:]) for dec in VALIDATE_DECORATORS_NOARGS
]

DEFAULT_VALIDATORS = {
    name: _make_default(dec)
    for name, dec in zip(_DEFAULT_NAMES, VALIDATE_DECORATORS_NOARGS)
}

DEFAULT_VALIDATOR_BUILDERS = {
    dec.get_default_name(): _make_default_with_args(dec)
    for dec in VALIDATE_DECORATORS_ARGS
}

DEFAULT_VALIDATOR_BY_TYPE = {
    int: "integer",
    str: "string",
    list: "list",
    dict: "dict",
}


def default_validate_int(_value, **kwargs):
    """Default integer validator."""
    return DEFAULT_VALIDATORS["integer"](_value, **kwargs)


def default_validate_pos_int(_value, **kwargs):
    """Default positive integer validator."""
    return DEFAULT_VALIDATORS["positive_integer"](_value, **kwargs)


def default_validate_str(_value, **kwargs):
    """Default string validator."""
    return DEFAULT_VALIDATORS["string"](_value, **kwargs)


def default_validate_list(_value, **kwargs):
    """Default list validator."""
    return DEFAULT_VALIDATORS["list"](_value, **kwargs)


def default_validate_dict(_value, **kwargs):
    """Default dict validator."""
    return DEFAULT_VALIDATORS["dict"](_value, **kwargs)


def build_validate_choice(*choices):
    """Build a choice validator on the fly."""
    return DEFAULT_VALIDATOR_BUILDERS["choice"](*choices)


def build_validate_int_range(start, end):
    """Build integer range validator on the fly."""
    return DEFAULT_VALIDATOR_BUILDERS["int_range"](start, end)
