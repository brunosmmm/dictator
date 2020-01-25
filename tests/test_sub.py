"""Test sub-configurations."""

import pytest
from dictator.default import DEFAULT_VALIDATORS
from dictator.config import validate_config, ConfigurationError


def test_sub_list():
    """Test sub-configuration in list."""
    TEST_CONFIG = {"myStuff": [{"value": 42}, {"value": 46}]}
    TEST_CONFIG_ERR = {"myStuff": [{"value": 42}, {"value": -50}]}
    SUB_REQ = {"value": DEFAULT_VALIDATORS.positive_integer}
    TEST_CONFIG_REQ = {"myStuff": DEFAULT_VALIDATORS.sub_list(SUB_REQ)}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)


def test_sub_dict():
    """Test sub-configuration in dict."""
    TEST_CONFIG = {"myStuff": {"value": 42}}
    TEST_CONFIG_ERR = {"myStuff": {"value": -50}}
    SUB_REQ = {"value": DEFAULT_VALIDATORS.positive_integer}
    TEST_CONFIG_REQ = {"myStuff": DEFAULT_VALIDATORS.sub_dict(SUB_REQ)}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)
