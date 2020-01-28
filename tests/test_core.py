"""Test dictator core."""

import pytest

from dictator.validators.base import validate_null
from dictator.config import validate_config
from dictator.errors import ConfigurationError, ValidationError


def test_missing():
    """Test missing required key."""
    TEST_CONFIG = {"someKey": 1234}
    TEST_CONFIG_REQ = {"otherKey": None}

    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG, TEST_CONFIG_REQ)


def test_novalidate():
    """Test no validation."""
    TEST_CONFIG = {"myValue": 42}
    TEST_CONFIG_REQ = {"myValue": None}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)


def test_validate_int():
    """Test integer validation."""
    TEST_CONFIG = {"myValue": 42, "myHexValue": "0x100", "myBinValue": "0b001"}
    TEST_CONFIG_ERR = {"myValue": 42, "myHexValue": "bla", "myBinValue": "001"}
    TEST_CONFIG_REQ = {"myValue": int, "myHexValue": int, "myBinValue": int}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    # test error
    with pytest.raises(ValidationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)


def test_validate_str():
    """Test integer validation."""
    TEST_CONFIG = {"myValue": "str"}
    TEST_CONFIG_ERR = {"myValue": 42}
    TEST_CONFIG_REQ = {"myValue": str}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    # test error
    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)


def test_validate_list():
    """Validate a list."""
    TEST_CONFIG = {"myList": [1, 2, 3]}
    TEST_CONFIG_ERR = {"myList": "other"}
    TEST_CONFIG_REQ = {"myList": list}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)


def test_validate_dict():
    """Validate a list."""
    TEST_CONFIG = {"myList": {0: "some"}}
    TEST_CONFIG_ERR = {"myList": "other"}
    TEST_CONFIG_REQ = {"myList": dict}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)


def test_validate_bool():
    """Validate a list."""
    TEST_CONFIG = {"myList": True}
    TEST_CONFIG_ERR = {"myList": "other"}
    TEST_CONFIG_REQ = {"myList": bool}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)


def test_validate_float():
    """Validate a list."""
    TEST_CONFIG = {"myList": 0.1234}
    TEST_CONFIG_ERR = {"myList": "other"}
    TEST_CONFIG_REQ = {"myList": float}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)


def test_validate_null():
    """Validate a list."""
    TEST_CONFIG = {"myList": None}
    TEST_CONFIG_ERR = {"myList": "other"}
    TEST_CONFIG_REQ = {"myList": validate_null}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)
