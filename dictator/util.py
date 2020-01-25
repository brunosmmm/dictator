"""Utilities."""

from dictator.config import validate_config, DeferValidation
from dictator.validators import Validator, ValidateType


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
        for name, dep in dependency_map.items():
            if not isinstance(name, str):
                raise TypeError("mapping key must be a string")
            if not isinstance(dep, (str, tuple, str)):
                raise TypeError("mapping value must be string, list or tuple")

            if isinstance(dep, (list, tuple)):
                for dep_name in dep:
                    if not isinstance(dep_name, str):
                        raise TypeError(
                            "in mapping value list: all values must be strings"
                        )
        self._depmap = dependency_map

    def __call__(self, fn):
        """Decorator."""

        def _validate(_value, **kwargs):
            """Perform checks."""

            missing_deps = []
            deps = self._depmap[_value]
            if isinstance(deps, str):
                deps = (deps,)
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
        for dep in dependencies:
            if not isinstance(dep, str):
                raise TypeError("dependencies must be strings")
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
