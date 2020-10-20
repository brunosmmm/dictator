"""Replace string fragments with validated values."""

import re
from typing import Dict, Any
from dictator.validators import Validator
from dictator.validators.base import validate_string
from dictator.validators.dependency import KeyDependency
from dictator.errors import ValidationError


class FragmentError(ValidationError):
    """Fragment replacement error."""


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

    REPLACE_PATTERN = re.compile(r"\$\{((?:\.\.)|:)?([\w:]+)\}")
    KEY_REF_TYPES = ("parent", "top", "normal")

    @staticmethod
    def get_key_type(leading_str):
        """Get key type."""
        if leading_str == ":":
            return "top"
        if leading_str == "..":
            return "parent"
        if leading_str == "":
            return "normal"

        raise ValueError("invalid leading characters")

    def validate(self, _value, **kwargs):
        """Perform validation."""
        if not isinstance(_value, str):
            # ignore if not string
            return _value
        req_keys = re.findall(self.REPLACE_PATTERN, _value)
        req_keys = [(key, self.get_key_type(rel)) for rel, key in req_keys]

        true_depends = []
        soft_depends = {}
        for req_key, ktype in req_keys:
            key_accessor = req_key.split("::")
            if ktype == "parent":
                if "_parent" not in kwargs or kwargs["_parent"] is None:
                    raise ValidationError(
                        "key requires a parent configuration which is not available"
                    )
                key_src = kwargs["_parent"]
            elif ktype == "normal":
                true_depends.append(key_accessor[0])
                continue
            else:
                # top-level
                parent = kwargs["_parent"]
                if parent is None:
                    # already at top-level
                    key_src = kwargs
                else:
                    key_src = None
                    while parent is not None:
                        key_src = parent
                        parent = parent["_parent"]

            if key_accessor[0] not in key_src:
                raise ValidationError(
                    f"couldn't find key {req_key} in referred configuration level"
                )
            if len(key_accessor) > 1:
                for accessor in key_accessor:
                    if not isinstance(key_src, dict):
                        raise ValidationError(
                            "key is not dictionary, cannot access member"
                        )
                    if accessor not in key_src:
                        raise FragmentError(f"member {accessor} not found")
                    key_src = key_src[accessor]

                soft_depends[req_key] = key_src
            else:
                soft_depends[req_key] = key_src[req_key]

        @KeyDependency(*true_depends, validate_after=True)
        def _validate(_value, **kwargs):
            for req_key, ktype in req_keys:
                value_src = soft_depends if ktype != "normal" else kwargs
                key_accessor = req_key.split("::")
                if len(key_accessor) > 1 and ktype == "normal":
                    if key_accessor[0] not in value_src:
                        raise FragmentError(
                            f"key {key_accessor[0]} is not available"
                        )
                    if not isinstance(value_src[key_accessor[0]], dict):
                        raise FragmentError(
                            "sub-key requested from key which is not dictionary"
                        )
                    for accessor in key_accessor:
                        value_src = value_src[accessor]
                elif req_key not in value_src:
                    raise FragmentError(f"key {req_key} is not available")
                else:
                    value_src = value_src[req_key]
                _value = re.sub(
                    r"\$\{((?:\.\.)|:)?" + req_key + r"\}", value_src, _value
                )
            return _value

        return _validate(_value, **kwargs)
