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
        pattern
          pattern to replace
        src_key
          source key to get value from
        kwargs
          any other arguments
        """
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
