"""Test sub-configurations."""

import pytest
from dictator.config import validate_config
from dictator.validators.integer import validate_positive_integer
from dictator.validators.lists import SubListValidator
from dictator.validators.maps import SubDictValidator
from dictator.errors import ConfigurationError


def test_sub_list():
    """Test sub-configuration in list."""
    TEST_CONFIG = {"myStuff": [{"value": 42}, {"value": 46}]}
    TEST_CONFIG_ERR = {"myStuff": [{"value": 42}, {"value": -50}]}
    SUB_REQ = {"value": validate_positive_integer}
    TEST_CONFIG_REQ = {"myStuff": SubListValidator(SUB_REQ)}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)


def test_sub_dict():
    """Test sub-configuration in dict."""
    TEST_CONFIG = {"myStuff": {"value": 42}}
    TEST_CONFIG_ERR = {"myStuff": {"value": -50}}
    SUB_REQ = {"value": validate_positive_integer}
    TEST_CONFIG_REQ = {"myStuff": SubDictValidator(SUB_REQ)}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)
