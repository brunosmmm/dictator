"""Utilities."""

from dictator.config import validate_config, DeferValidation
from dictator.validators import (
    Validator,
    ValidateType,
    ValidateChoice,
    ValidateIntRange,
    validate_integer,
    validate_positive_integer,
    validate_string,
    validate_list,
    validate_dict,
)

VALIDATE_DECORATORS_NOARGS = (
    validate_integer,
    validate_positive_integer,
    validate_string,
    validate_list,
    validate_dict,
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


class AutoValidateList(Validator):
    """Automatically validate list elements."""

    def __init__(self, required_keys, optional_keys=None):
        """Initialize."""
        super().__init__()
        self._required = required_keys
        self._optional = optional_keys

    def __call__(self, fn):
        """Decorator."""

        @ValidateType((tuple, list))
        def _validate(_value, **kwargs):
            """Perform sub-validation."""
            return fn(
                [
                    validate_config(entry, self._required, self._optional)
                    for entry in _value
                ],
                **kwargs,
            )

        return _validate


class AutoValidateDict(Validator):
    """Automatically validate dict elements."""

    def __init__(self, required_keys, optional_keys=None):
        """Initialize."""
        super().__init__()
        self._required = required_keys
        self._optional = optional_keys

    def __call__(self, fn):
        """Decorator."""

        @ValidateType(dict)
        def _validate(_value, **kwargs):
            """Perform sub-validation."""
            return fn(
                validate_config(_value, self._required, self._optional),
                **kwargs,
            )

        return _validate


class KeyDependencyMap(Validator):
    """Check for dependencies."""

    def __init__(self, **dependency_map):
        """Initialize."""
        super().__init__()
        self._depmap = dependency_map

    def __call__(self, fn):
        """Decorator."""

        def _validate(_value, **kwargs):
            """Perform checks."""

            missing_deps = []
            deps = self._depmap[_value]
            for dep in deps:
                if dep not in kwargs:
                    missing_deps.append(dep)

            if missing_deps:
                raise DeferValidation(*missing_deps)

            return fn(_value, **kwargs)

        return _validate


class KeyDependency(Validator):
    """Check for dependencies."""

    def __init__(self, *dependencies):
        """Initialize."""
        super().__init__()
        self._deps = dependencies

    def __call__(self, fn):
        """Decorator."""

        def _validate(_value, **kwargs):
            """Perform checks."""

            missing_deps = []
            for dep in self._deps:
                if dep not in kwargs:
                    missing_deps.append(dep)

            if missing_deps:
                raise DeferValidation(*missing_deps)

            return fn(_value, **kwargs)

        return _validate


def default_validate_int(_value, **kwargs):
    """Default integer validator."""
    return DEFAULT_VALIDATORS["integer"]


def default_validate_pos_int(_value, **kwargs):
    """Default positive integer validator."""
    return DEFAULT_VALIDATORS["positive_integer"]


def default_validate_str(_value, **kwargs):
    """Default string validator."""
    return DEFAULT_VALIDATORS["string"]


def default_validate_list(_value, **kwargs):
    """Default list validator."""
    return DEFAULT_VALIDATORS["list"]


def default_validate_dict(_value, **kwargs):
    """Default dict validator."""
    return DEFAULT_VALIDATORS["dict"]


def build_validate_choice(*choices):
    """Build a choice validator on the fly."""
    return DEFAULT_VALIDATOR_BUILDERS["choice"](*choices)


def build_validate_int_range(start, end):
    """Build integer range validator on the fly."""
    return DEFAULT_VALIDATOR_BUILDERS["int_range"](start, end)
