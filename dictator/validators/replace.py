"""Replace string fragments with validated values."""

import re
from typing import Dict, Any
from dictator.validators import Validator
from dictator.validators.base import validate_string
from dictator.validators.dependency import KeyDependency


class FragmentReplace(Validator):
    """Replace string fragments."""

    def __init__(self, patterns: Dict[str, str], **kwargs: Dict[str, Any]):
        """Initialize.

        Arguments
        ------------
        patterns
          patterns to replace and keys to get from
        kwargs
          any other arguments
        """
        super().__init__(**kwargs)
        self._patterns = [
            (re.compile(pattern), src_key)
            for pattern, src_key in patterns.items()
        ]

    @property
    def required_keys(self):
        """Get required keys from patterns."""
        return [key for _, key in self._patterns]

    @property
    def patterns(self):
        """Get patterns."""
        return [pattern for pattern, _ in self._patterns]

    @validate_string
    def validate(self, _value, **kwargs):
        """Perform validation."""

        @KeyDependency(*self.required_keys)
        def _validate(_value, **kwargs):
            for pattern, key in self._patterns:
                return re.sub(pattern, kwargs[key], _value)

        return _validate(_value, **kwargs)


class AutoFragmentReplace(Validator):
    """Automatic fragment replacer."""

    REPLACE_PATTERN = re.compile(r"\$\{(\w+)\}")

    @validate_string
    def validate(self, _value, **kwargs):
        """Perform validation."""
        req_keys = re.findall(self.REPLACE_PATTERN, _value)

        @KeyDependency(*req_keys)
        def _validate(_value, **kwargs):
            for req_key in req_keys:
                _value = re.sub(
                    r"\$\{" + req_key + r"\}", kwargs[req_key], _value
                )
            return _value

        return _validate(_value, **kwargs)
