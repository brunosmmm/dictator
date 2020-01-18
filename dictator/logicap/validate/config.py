"""Validate test configuration."""


class TestConfigurationError(Exception):
    """Test configuration error."""


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


def validate_config(config, required_keys, optional_keys=None):
    """Validate configuration."""
    if not isinstance(config, dict):
        raise TypeError("configuration must be a dictionary")

    for key in required_keys:
        if key not in config:
            raise TestConfigurationError(
                f"invalid configuration, missing required key '{key}'"
            )

    transformed_config = {}
    deferred_keys = {}
    for key, value in config.items():
        if key not in required_keys and (
            (optional_keys is not None and key not in optional_keys)
            or optional_keys is None
        ):
            # warning, unknown key
            print(f"DEBUG: unknown key '{key}'")
            continue

        if key in required_keys:
            key_loc = required_keys
        elif key in optional_keys:
            key_loc = optional_keys

        # call validate
        if key_loc[key] is None:
            # no validation
            transformed_config[key] = value
        else:
            try:
                new_value = key_loc[key](value, **transformed_config)
                if new_value is None:
                    transformed_config[key] = value
                else:
                    transformed_config[key] = new_value
            except DeferValidation as defer:
                deferred_keys[key] = defer.depends

    # resolve dependencies
    for key, depends in deferred_keys.items():
        if key in required_keys:
            key_loc = required_keys
        else:
            key_loc = optional_keys
        try:
            transform = key_loc[key](config[key], **transformed_config)
        except DeferValidation as ex:
            # deferred validation still not done, failure
            readable_depends = ", ".join(ex.depends)
            raise TestConfigurationError(
                f"unresolved dependencies found for key '{key}': '{readable_depends}'"
            )

        if transform is not None:
            transformed_config[key] = transform
        else:
            transformed_config[key] = config[key]

    return transformed_config
