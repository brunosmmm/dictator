"""Validate test configuration."""

import dictator.validators.default as defaults
from dictator.errors import (
    MissingRequiredKeyError,
    MissingDependencyError,
    KeyDeclarationError,
    UnknownKeyError,
)
from dictator.validators.dependency import DeferValidation

VERBOSITY = {"error": 3, "warning": 2, "info": 1, "debug": 0}
VERBOSITY_HEADERS = {
    "error": "ERROR",
    "warning": "WARNING",
    "info": "",
    "debug": "DEBUG",
}


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


def _config_pre_checklist(fn):
    """Check configuration types."""

    def _check(config, required_keys, optional_keys=None, *args, **kwargs):
        if not isinstance(config, dict):
            raise TypeError(
                f"configuration must be a dictionary, got: {type(config)}"
            )
        if not isinstance(required_keys, dict):
            raise TypeError("required_keys must be a dictionary")

        if optional_keys is not None:
            if not isinstance(optional_keys, dict):
                raise TypeError("optional_keys must be a dictionary")

            for key in optional_keys:
                if not isinstance(key, str):
                    raise KeyDeclarationError("keys must be string values")
                if key in required_keys:
                    # warning, required AND optional
                    pass

        for key in required_keys:
            if not isinstance(key, str):
                raise KeyDeclarationError("keys must be string values")
            if key not in config:
                raise MissingRequiredKeyError(
                    f"invalid configuration, missing required key '{key}'"
                )
        return fn(config, required_keys, optional_keys, *args, **kwargs)

    return _check


@_config_pre_checklist
def validate_config(
    config,
    required_keys,
    optional_keys=None,
    verbosity="error",
    log_fn=None,
    allow_unknown=True,
):
    """Validate configuration."""
    # pass validation config args down
    vargs = {"verbosity": verbosity}

    if log_fn is not None:
        _log = log_fn
    else:
        _log = _default_logger

    transformed_config = {}
    deferred_keys = {}
    for key, value in config.items():
        if not isinstance(key, str):
            raise TypeError("keys must be string values")
        if key not in required_keys and (
            (optional_keys is not None and key not in optional_keys)
            or optional_keys is None
        ):
            # warning, unknown key
            _log(f"unknown key: '{key}'", "warning", verbosity)
            if allow_unknown is False:
                raise UnknownKeyError(f"unknown key: {key}")
            continue

        key_loc = required_keys if key in required_keys else optional_keys
        # call validate
        if key_loc[key] is None:
            # no validation
            transformed_config[key] = value
        else:
            if isinstance(key_loc[key], type):
                validate_fn = defaults.DEFAULT_VALIDATORS.get_by_type(
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
        key_loc = required_keys if key in required_keys else optional_keys
        try:
            if isinstance(key_loc[key], type):
                validate_fn = defaults.DEFAULT_VALIDATORS.get_by_type(
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
            raise MissingDependencyError(
                f"unresolved dependencies found for key '{key}':"
                f"'{readable_depends}'"
            )

        if transform is not None:
            transformed_config[key] = transform
        else:
            transformed_config[key] = config[key]

    return transformed_config
