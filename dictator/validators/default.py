"""Default Validators."""

from dictator.validators import Validator
from dictator.validators.base import (
    validate_integer,
    validate_string,
    validate_list,
    validate_dict,
    validate_boolean,
    validate_float,
    validate_null,
)

from dictator.validators.integer import (
    validate_percent_integer,
    validate_positive_integer,
    ValidateIntRange,
)

from dictator.validators.lists import (
    ValidateChoice,
    SubListValidator,
    HomogeneousValidator,
)
from dictator.validators.maps import SubDictValidator

from dictator.validators.dependency import (
    KeyDependency,
    KeyDependencyMap,
)

from dictator.errors import DefaultValidatorError


class _DefaultValidators:
    """Default validators."""

    VALIDATE_FUNCTIONS = (
        validate_integer,
        validate_positive_integer,
        validate_string,
        validate_list,
        validate_dict,
        validate_percent_integer,
        validate_boolean,
        validate_float,
        validate_null,
    )

    DEFAULT_NAMES = [
        "_".join(dec.__name__.split("_")[1:])
        for dec in VALIDATE_DECORATORS_NOARGS
    ]

    VALIDATE_DECORATORS_ARGS = (
        ValidateChoice,
        ValidateIntRange,
        SubListValidator,
        SubDictValidator,
        KeyDependency,
        KeyDependencyMap,
        HomogeneousValidator,
    )

    def __init__(self):
        """Initialize."""

        self._DEFAULT_VALIDATORS = {
            name: self._make_default(dec)
            for name, dec in zip(
                self.DEFAULT_NAMES, self.VALIDATE_DECORATORS_NOARGS
            )
        }

        self._DEFAULT_VALIDATOR_BUILDERS = {
            dec.get_default_name(): self._make_default_with_args(dec)
            for dec in self.VALIDATE_DECORATORS_ARGS
        }

    @staticmethod
    def _make_default(decorator):
        """Build default validator function."""

        @decorator
        def _validate_fn(_value, **kwargs):
            return _value

        # insert metadata
        _validate_fn._dictator_meta = {"decorator": True, "outer": False}

        return _validate_fn

    @staticmethod
    def _make_default_with_args(decorator):
        """Build default validator function builder."""
        if not issubclass(decorator, Validator):
            raise DefaultValidatorError("must be a subclass of Validator")

        def _outer_validate_fn(*args, **kwargs):
            @decorator(*args, **kwargs)
            def _validate_fn(_value, **_kwargs):
                return _value

            # insert metadata
            _validate_fn._dictator_meta = {"decorator": True, "outer": False}

            return _validate_fn

        # insert metadata
        _outer_validate_fn._dictator_meta = {"decorator": True, "outer": True}

        return _outer_validate_fn

    def __getattr__(self, name):
        """Get attribute."""
        if name in self._DEFAULT_VALIDATORS:
            return self._DEFAULT_VALIDATORS[name]

        if name in self._DEFAULT_VALIDATOR_BUILDERS:
            return self._DEFAULT_VALIDATOR_BUILDERS[name]

        raise AttributeError(f"default validator not available for '{name}'")


DEFAULT_VALIDATORS = _DefaultValidators()
