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
from dictator.util import (
    KeyDependency,
    KeyDependencyMap,
    AutoValidateDict,
    AutoValidateList,
)


class _DefaultValidators:
    """Default validators."""

    VALIDATE_DECORATORS_NOARGS = (
        validate_integer,
        validate_positive_integer,
        validate_string,
        validate_list,
        validate_dict,
        validate_int_percent,
    )

    DEFAULT_NAMES = [
        "_".join(dec.__name__.split("_")[1:])
        for dec in VALIDATE_DECORATORS_NOARGS
    ]

    VALIDATE_DECORATORS_ARGS = (
        ValidateChoice,
        ValidateIntRange,
        AutoValidateList,
        AutoValidateDict,
        KeyDependency,
        KeyDependencyMap,
    )

    DEFAULT_VALIDATOR_BY_TYPE = {
        int: "integer",
        str: "string",
        list: "list",
        dict: "dict",
    }

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

        return _validate_fn

    @staticmethod
    def _make_default_with_args(decorator):
        """Build default validator function builder."""

        def _outer_validate_fn(*args, **kwargs):
            @decorator(*args, **kwargs)
            def _validate_fn(_value, **_kwargs):
                return _value

            return _validate_fn

        return _outer_validate_fn

    def get_by_type(self, _type):
        """Get default validator by type."""
        if _type in self.DEFAULT_VALIDATOR_BY_TYPE:
            return getattr(self, self.DEFAULT_VALIDATOR_BY_TYPE[_type])

        raise TypeError("default validator not available for type f'{_type}'")

    def __getattr__(self, name):
        """Get attribute."""
        if name in self._DEFAULT_VALIDATORS:
            return self._DEFAULT_VALIDATORS[name]

        if name in self._DEFAULT_VALIDATOR_BUILDERS:
            return self._DEFAULT_VALIDATOR_BUILDERS[name]

        raise AttributeError(f"default validator not available for '{name}'")


DEFAULT_VALIDATORS = _DefaultValidators()
