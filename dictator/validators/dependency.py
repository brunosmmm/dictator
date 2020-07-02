"""Utilities."""

from dictator.validators import Validator
from typing import Tuple, Any


class DeferValidation(Exception):
    """Defer key validation."""

    def __init__(self, *depends: str):
        """Initialize.

        Parameters
        ----------
        depends
            List of key names that will be required
        """
        self._depends = depends
        super().__init__("")

    @property
    def depends(self) -> Tuple[str, ...]:
        """Get key dependencies."""
        return self._depends


class KeyDependencyMap(Validator):
    """Check for dependencies."""

    _DEFAULT_NAME = "dependency_map"

    def __init__(self, validate_after=False, **dependency_map: str):
        """Initialize.

        Parameters
        ----------
        dependency_map
            Map of dependencies according to current key value
        """
        super().__init__(after_fn=validate_after)
        for name, dep in dependency_map.items():
            if not isinstance(dep, (str, tuple, str)):
                raise TypeError("mapping value must be string, list or tuple")

            if isinstance(dep, (list, tuple)):
                for dep_name in dep:
                    if not isinstance(dep_name, str):
                        raise TypeError(
                            "in mapping value list: all values must be strings"
                        )
        self._depmap = dependency_map

    def validate(self, _value, **kwargs):
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

        return _value


class KeyDependency(Validator):
    """Check for dependencies."""

    _DEFAULT_NAME = "dependency"

    def __init__(
        self, *dependencies: str, validate_after=False, **kwargs: Any
    ):
        """Initialize.

        Parameters
        ----------
        dependencies
            Key names which are dependencies
        kwargs
            Any other metadata
        """
        super().__init__(after_fn=validate_after)
        for dep in dependencies:
            if not isinstance(dep, str):
                raise TypeError("dependencies must be strings")
        self._deps = dependencies

    def validate(self, _value, **kwargs):
        """Perform checks."""

        missing_deps = []
        for dep in self._deps:
            if dep not in kwargs:
                missing_deps.append(dep)

        if missing_deps:
            raise DeferValidation(*missing_deps)

        return _value
