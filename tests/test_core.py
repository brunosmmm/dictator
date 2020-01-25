"""Test dictator core."""

import pytest

from dictator.util import DEFAULT_VALIDATORS, DEFAULT_VALIDATOR_BUILDERS
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
        "myValue": DEFAULT_VALIDATORS["integer"],
        "myHexValue": DEFAULT_VALIDATORS["integer"],
    }

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    # test error
    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)


def test_validate_pos_int():
    """Validate positive integers."""
    TEST_CONFIG = {"myValue": 42}
    TEST_CONFIG_ERR = {"myValue": -42}
    TEST_CONFIG_REQ = {"myValue": DEFAULT_VALIDATORS["positive_integer"]}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    # test error
    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)


def test_validate_str():
    """Test integer validation."""
    TEST_CONFIG = {"myValue": "str"}
    TEST_CONFIG_ERR = {"myValue": 42}
    TEST_CONFIG_REQ = {
        "myValue": DEFAULT_VALIDATORS["string"],
    }

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    # test error
    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)


def test_validate_list():
    """Validate a list."""
    TEST_CONFIG = {"myList": [1, 2, 3]}
    TEST_CONFIG_ERR = {"myList": "other"}
    TEST_CONFIG_REQ = {"myList": DEFAULT_VALIDATORS["list"]}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)


def test_validate_dict():
    """Validate a list."""
    TEST_CONFIG = {"myList": {0: "some"}}
    TEST_CONFIG_ERR = {"myList": "other"}
    TEST_CONFIG_REQ = {"myList": DEFAULT_VALIDATORS["dict"]}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)


def test_validate_choice():
    """Validate a list."""
    TEST_CONFIG = {"myList": "bla"}
    TEST_CONFIG_ERR = {"myList": "other"}
    TEST_CONFIG_REQ = {
        "myList": DEFAULT_VALIDATOR_BUILDERS["choice"]("bla", "boo")
    }

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)


def test_validate_intrange():
    """Validate a list."""
    TEST_CONFIG = {"myList": 42}
    TEST_CONFIG_ERR = {"myList": 0}
    TEST_CONFIG_REQ = {
        "myList": DEFAULT_VALIDATOR_BUILDERS["int_range"](40, 46)
    }

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)


def test_validate_intpercent():
    """Validate a list."""
    TEST_CONFIG = {"myList": 42}
    TEST_CONFIG_ERR = {"myList": 200}
    TEST_CONFIG_REQ = {"myList": DEFAULT_VALIDATORS["int_percent"]}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)
