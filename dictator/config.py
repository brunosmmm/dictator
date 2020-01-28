"""Validate test configuration."""

from dictator.validators.base import (
    validate_integer,
    validate_string,
    validate_list,
    validate_dict,
    validate_float,
    validate_boolean,
)
from dictator.errors import (
    MissingRequiredKeyError,
    MissingDependencyError,
    KeyDeclarationError,
    UnknownKeyError,
    DefaultValidatorError,
)
from dictator.validators.dependency import DeferValidation
from dictator.validators import Validator

VERBOSITY = {"error": 3, "warning": 2, "info": 1, "debug": 0}
VERBOSITY_HEADERS = {
    "error": "ERROR",
    "warning": "WARNING",
    "info": "",
    "debug": "DEBUG",
}

DEFAULT_VALIDATOR_BY_TYPE = {
    int: validate_integer,
    str: validate_string,
    list: validate_list,
    dict: validate_dict,
    bool: validate_boolean,
    float: validate_float,
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


def _get_validate_fn(entry):
    if isinstance(entry, type):
        if entry not in DEFAULT_VALIDATOR_BY_TYPE:
            raise DefaultValidatorError(
                f"no validator available for python type '{entry}'"
            )
        default_validator = DEFAULT_VALIDATOR_BY_TYPE[entry]
        if isinstance(default_validator, Validator):
            fn = default_validator.validate
        else:
            fn = default_validator
    elif isinstance(entry, Validator):
        fn = entry.validate
    else:
        fn = entry
    if hasattr(fn, "_dictator_meta") and fn._dictator_meta["outer"] is True:
        # this is a default generator that hasnt been called
        raise DefaultValidatorError(
            "default validator generator was not initialized"
        )

    return fn


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
            # try default validator
            try:
                new_value = _get_validate_fn(key_loc[key])(
                    value, _validator_args=vargs, **transformed_config
                )
                transformed_config[key] = (
                    value if new_value is None else new_value
                )
            except DeferValidation as defer:
                deferred_keys[key] = defer.depends

    # resolve dependencies
    for key, depends in deferred_keys.items():
        key_loc = required_keys if key in required_keys else optional_keys
        try:
            transform = _get_validate_fn(key_loc[key])(
                config[key], _validator_args=vargs, **transformed_config
            )
        except DeferValidation as ex:
            # deferred validation still not done, failure
            readable_depends = ", ".join(ex.depends)
            raise MissingDependencyError(
                f"unresolved dependencies found for key '{key}':"
                f"'{readable_depends}'"
            )

        transformed_config[key] = (
            transform if transform is not None else config[key]
        )

    return transformed_config
