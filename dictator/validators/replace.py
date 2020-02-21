"""Replace string fragments with validated values."""

import re
from dictator.validators import Validator
from dictator.validators.base import validate_string
from dictator.validators.dependency import KeyDependency


class FragmentReplace(Validator):
    """Replace string fragments."""

    def __init__(self, pattern: str, src_key: str, **kwargs):
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
        self._pattern = re.compile(pattern)
        self._src = src_key

    @validate_string
    def validate(self, _value, **kwargs):
        """Perform validation."""

        @KeyDependency(self._src)
        def _validate(_value, **kwargs):
            return re.sub(self._pattern, kwargs[self._src], _value)

        return _validate(_value, **kwargs)
