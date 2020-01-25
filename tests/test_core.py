"""Test dictator core."""

import pytest

from dictator.util import (
    default_validate_int,
    default_validate_str,
    default_validate_pos_int,
    default_validate_list,
    default_validate_dict,
)
from dictator.config import validate_config, ConfigurationError


def test_missing():
    """Test missing required key."""
    TEST_CONFIG = {"someKey": 1234}
    TEST_CONFIG_REQ = {"otherKey": None}

    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG, TEST_CONFIG_REQ)


def test_validate_int():
    """Test integer validation."""
    TEST_CONFIG = {"myValue": 42, "myHexValue": "0x100"}
    TEST_CONFIG_ERR = {"myValue": "str"}
    TEST_CONFIG_REQ = {
        "myValue": default_validate_int,
        "myHexValue": default_validate_int,
    }

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    # test error
    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)


def test_validate_pos_int():
    """Validate positive integers."""
    TEST_CONFIG = {"myValue": 42}
    TEST_CONFIG_ERR = {"myValue": -42}
    TEST_CONFIG_REQ = {"myValue": default_validate_pos_int}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    # test error
    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)


def test_validate_str():
    """Test integer validation."""
    TEST_CONFIG = {"myValue": "str"}
    TEST_CONFIG_ERR = {"myValue": 42}
    TEST_CONFIG_REQ = {
        "myValue": default_validate_str,
    }

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    # test error
    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)


def test_validate_list():
    """Validate a list."""
    TEST_CONFIG = {"myList": [1, 2, 3]}
    TEST_CONFIG_ERR = {"myList": "other"}
    TEST_CONFIG_REQ = {"myList": default_validate_list}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)


def test_validate_dict():
    """Validate a list."""
    TEST_CONFIG = {"myList": {0: "some"}}
    TEST_CONFIG_ERR = {"myList": "other"}
    TEST_CONFIG_REQ = {"myList": default_validate_dict}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)
