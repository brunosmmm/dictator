"""Validate test configuration."""

import dictator.default

VERBOSITY = {"error": 3, "warning": 2, "info": 1, "debug": 0}
VERBOSITY_HEADERS = {
    "error": "ERROR",
    "warning": "WARNING",
    "info": "",
    "debug": "DEBUG",
}


class ConfigurationError(Exception):
    """Generic configuration error."""


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


def _default_logger(msg, severity, verbosity):
    """Default logger."""
    if VERBOSITY[severity] >= VERBOSITY[verbosity]:
        print(
            "{}{}".format(
                "{}{}".format(
                    VERBOSITY_HEADERS[severity],
                    ": " if VERBOSITY_HEADERS[severity] else "",
                ),
                msg,
            )
        )


def validate_config(
    config, required_keys, optional_keys=None, verbosity="error", log_fn=None
):
    """Validate configuration."""
    if not isinstance(config, dict):
        raise TypeError(
            f"configuration must be a dictionary, got: {type(config)}"
        )

    # pass validation config args down
    vargs = {"verbosity": verbosity}

    for key in required_keys:
        if key not in config:
            raise ConfigurationError(
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
            if log_fn is not None:
                _log = log_fn
            else:
                _log = _default_logger
            _log(f"unknown key: '{key}'", "warning", verbosity)
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
            if isinstance(key_loc[key], type):
                validate_fn = dictator.default.DEFAULT_VALIDATORS.get_by_type(
                    key_loc[key]
                )
            else:
                validate_fn = key_loc[key]
            try:
                new_value = validate_fn(
                    value, _validator_args=vargs, **transformed_config
                )
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
            if isinstance(key_loc[key], type):
                validate_fn = dictator.default.DEFAULT_VALIDATORS.get_by_type(
                    key_loc[key]
                )
            else:
                validate_fn = key_loc[key]
            transform = key_loc[key](
                config[key], _validator_args=vargs, **transformed_config
            )
        except DeferValidation as ex:
            # deferred validation still not done, failure
            readable_depends = ", ".join(ex.depends)
            raise ConfigurationError(
                f"unresolved dependencies found for key '{key}': '{readable_depends}'"
            )

        if transform is not None:
            transformed_config[key] = transform
        else:
            transformed_config[key] = config[key]

    return transformed_config
