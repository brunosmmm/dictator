"""Utilities."""

from dictator.validators import Validator


class DeferValidation(Exception):
    """Defer key validation."""

    def __init__(self, *depends):
        """Initialize."""
        self._depends = depends
        super().__init__("")

    @property
    def depends(self):
        """Get key dependencies."""
        return self._depends


class KeyDependencyMap(Validator):
    """Check for dependencies."""

    _DEFAULT_NAME = "dependency_map"

    def __init__(self, **dependency_map):
        """Initialize."""
        super().__init__()
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

    _DEFAULT_NAME = "dependency"

    def __init__(self, *dependencies, **kwargs):
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
