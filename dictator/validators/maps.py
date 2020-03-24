"""Map-based validators."""

from dictator.validators import Validator
from dictator.validators.base import ValidateType
import dictator.config
from typing import Dict, Any, Optional


class SubDictValidator(Validator):
    """Automatically validate dict elements."""

    _DEFAULT_NAME = "sub_dict"

    def __init__(
        self,
        required_keys: Dict[str, Any],
        optional_keys: Optional[Dict[str, Any]] = None,
        validator_options: Optional[Dict[str, bool]] = None,
        **kwargs: Any
    ):
        """Initialize.

        Parameters
        ----------
        required_keys
            Required key mappings
        optional_keys
            Optional key mappings
        validator_options
            Other options passed into main validator function
        kwargs
            Any other metadata
        """
        super().__init__()
        if not isinstance(required_keys, dict):
            raise TypeError("required_keys must be a dictionary")
        if optional_keys is not None and not isinstance(optional_keys, dict):
            raise TypeError("optional_keys must be a dictionary")
        if validator_options is not None and not isinstance(
            validator_options, dict
        ):
            raise TypeError("validator_options must be a dictionary")
        elif validator_options is None:
            self._validator_options = {}
        else:
            self._validator_options = validator_options
        self._required = required_keys
        self._optional = optional_keys

    @ValidateType(dict)
    def validate(self, _value, **kwargs):
        """Perform sub-validation."""
        return dictator.config.validate_config(
            _value,
            self._required,
            self._optional,
            parent_keys=kwargs,
            **self._validator_options
        )
