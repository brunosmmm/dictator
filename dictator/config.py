"""Validate test configuration."""

from typing import Type, Union, Callable, Dict, List, Tuple, Optional, Any

from dictator.errors import (
    MissingRequiredKeyError,
    MissingDependencyError,
    KeyDeclarationError,
    UnknownKeyError,
    DefaultValidatorError,
    ValidationError,
)
from dictator.validators.dependency import DeferValidation
from dictator.validators.util import ValidateUnion
from dictator.validators import Validator
from dictator.validators.base import DEFAULT_VALIDATOR_BY_TYPE

VERBOSITY = {"error": 3, "warning": 2, "info": 1, "debug": 0}
VERBOSITY_HEADERS = {
    "error": "ERROR",
    "warning": "WARNING",
    "info": "",
    "debug": "DEBUG",
}


def _default_logger(msg: str, severity: str, verbosity: str):
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


def _config_pre_checklist(fn: Callable) -> Callable:
    """Check configuration types."""

    def _check(config, required_keys, optional_keys=None, *args, **kwargs):
        if not isinstance(config, dict):
            raise TypeError(
                f"configuration must be a dictionary, got: {type(config)}"
            )

        if required_keys is not None:
            if not isinstance(required_keys, dict):
                raise TypeError("required_keys must be a dictionary")

            for key in required_keys:
                if not isinstance(key, str):
                    raise KeyDeclarationError("keys must be string values")
                if key not in config:
                    raise MissingRequiredKeyError(
                        f"invalid configuration, missing required key '{key}'"
                    )

        if optional_keys is not None:
            if not isinstance(optional_keys, dict):
                raise TypeError("optional_keys must be a dictionary")

            for key in optional_keys:
                if not isinstance(key, str):
                    raise KeyDeclarationError("keys must be string values")
                if required_keys is not None and key in required_keys:
                    # warning, required AND optional
                    pass

        return fn(config, required_keys, optional_keys, *args, **kwargs)

    return _check


def _get_validate_fn(entry: Union[Type, Validator, Callable]) -> Callable:
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
    elif isinstance(entry, (list, tuple)):
        fn = ValidateUnion(*entry).validate
    else:
        fn = entry

    return fn


ValidatorConfiguration = Union[Dict[str, Union[Callable, type, None]]]
JSONBaseTypes = Union[str, int, bool, float, None]
ConfigurationType = Dict[str, Union[Dict, List, Tuple, JSONBaseTypes]]


@_config_pre_checklist
def validate_config(
    config: ConfigurationType,
    required_keys: Optional[ValidatorConfiguration] = None,
    optional_keys: Optional[ValidatorConfiguration] = None,
    verbosity: str = "error",
    log_fn: Optional[Callable] = None,
    allow_unknown: bool = True,
    gobble_unknown: bool = True,
    inherit_options: bool = False,
    pop_extra_kwargs: bool = False,
    parent_keys: Optional[Dict[str, Any]] = None,
    **extra_kwargs: Dict[str, Any],
):
    """Validate configuration."""

    _log = log_fn if log_fn is not None else _default_logger

    allow_unknown = (
        parent_keys.get("allow_unknown", allow_unknown)
        if inherit_options
        else allow_unknown
    )
    gobble_unknown = (
        parent_keys.get("gobble_unknown", gobble_unknown)
        if inherit_options
        else gobble_unknown
    )

    required_keys = {} if required_keys is None else required_keys

    # pass validation config args down
    vargs = {
        "verbosity": verbosity,
        "allow_unknown": allow_unknown,
        "gobble_unknown": gobble_unknown,
    }

    transformed_config = extra_kwargs.copy()
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
            if not gobble_unknown:
                # passes through without validation
                transformed_config[key] = value
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
                    value,
                    _validator_args=vargs,
                    _parent=parent_keys,
                    **transformed_config,
                )
                transformed_config[key] = (
                    value if new_value is None else new_value
                )
            except DeferValidation as defer:
                deferred_keys[key] = defer.depends
            except ValidationError as err:
                _err = str(err)
                raise ValidationError(
                    f"while validating key {key}: " + _err
                ) from err

    # resolve dependencies
    for key, depends in deferred_keys.items():
        # FIXME: mypy complains
        key_loc = required_keys if key in required_keys else optional_keys
        try:
            transform = _get_validate_fn(key_loc[key])(
                config[key],
                _validator_args=vargs,
                _parent=parent_keys,
                **transformed_config,
            )
        except DeferValidation as ex:
            # deferred validation still not done, failure
            readable_depends = ", ".join(ex.depends)
            raise MissingDependencyError(
                f"unresolved dependencies found for key '{key}':"
                f"'{readable_depends}'"
            )
        except ValidationError as err:
            _err = str(err)
            raise ValidationError(
                f"while validating key {key}: " + _err
            ) from err

        transformed_config[key] = (
            transform if transform is not None else config[key]
        )

    # pop extra kwargs
    if pop_extra_kwargs:
        for kwarg in extra_kwargs:
            if kwarg in transformed_config:
                transformed_config.pop(kwarg)

    return transformed_config
