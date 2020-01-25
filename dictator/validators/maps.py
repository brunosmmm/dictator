"""Map-based validators."""

from dictator.validators import Validator
from dictator.validators.base import ValidateType
import dictator.config


class SubDictValidator(Validator):
    """Automatically validate dict elements."""

    _DEFAULT_NAME = "sub_dict"

    def __init__(self, required_keys, optional_keys=None):
        """Initialize."""
        super().__init__()
        if not isinstance(required_keys, dict):
            raise TypeError("required_keys must be a dictionary")
        if optional_keys is not None and not isinstance(optional_keys, dict):
            raise TypeError("optional_keys must be a dictionary")
        self._required = required_keys
        self._optional = optional_keys

    def __call__(self, fn):
        """Decorator."""

        @ValidateType(dict)
        def _validate(_value, **kwargs):
            """Perform sub-validation."""
            return fn(
                dictator.config.validate_config(
                    _value, self._required, self._optional
                ),
                **kwargs,
            )

        return _validate
