"""Map-based validators."""

from dictator.validators import Validator
from dictator.validators.base import ValidateType
import dictator.config
from typing import Dict, Any, Union


class SubDictValidator(Validator):
    """Automatically validate dict elements."""

    _DEFAULT_NAME = "sub_dict"

    def __init__(
        self,
        required_keys: Dict[str, Any],
        optional_keys: Union[Dict[str, Any], None] = None,
        **kwargs: Any
    ):
        """Initialize.

        Parameters
        ----------
        required_keys
            Required key mappings
        optional_keys
            Optional key mappings
        kwargs
            Any other metadata
        """
        super().__init__()
        if not isinstance(required_keys, dict):
            raise TypeError("required_keys must be a dictionary")
        if optional_keys is not None and not isinstance(optional_keys, dict):
            raise TypeError("optional_keys must be a dictionary")
        self._required = required_keys
        self._optional = optional_keys

    @ValidateType(dict)
    def validate(self, _value, **kwargs):
        """Perform sub-validation."""
        return dictator.config.validate_config(
            _value, self._required, self._optional, parent_keys=kwargs
        )
