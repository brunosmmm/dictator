"""Test extended default validators."""

import pytest

from dictator.validators.integer import (
    validate_positive_integer,
    validate_percent_integer,
    ValidateIntRange,
)
from dictator.validators.lists import ValidateChoice, HomogeneousValidator
from dictator.config import validate_config
from dictator.errors import ConfigurationError


def test_validate_pos_int():
    """Validate positive integers."""
    TEST_CONFIG = {"myValue": 42}
    TEST_CONFIG_ERR = {"myValue": -42}
    TEST_CONFIG_REQ = {"myValue": validate_positive_integer}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    # test error
    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)


def test_validate_choice():
    """Validate from list of choices."""
    TEST_CONFIG = {"myList": "bla"}
    TEST_CONFIG_ERR = {"myList": "other"}
    TEST_CONFIG_REQ = {"myList": ValidateChoice("bla", "boo")}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)


def test_validate_intrange():
    """Validate integer within a range."""
    TEST_CONFIG = {"myList": 42}
    TEST_CONFIG_ERR = {"myList": 0}
    TEST_CONFIG_REQ = {"myList": ValidateIntRange(40, 46)}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)


def test_validate_intpercent():
    """Validate percent values."""
    TEST_CONFIG = {"myList": 42}
    TEST_CONFIG_ERR = {"myList": 200}
    TEST_CONFIG_REQ = {"myList": validate_percent_integer}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)


def test_validate_homogeneous():
    """Validate homogeneous list."""
    TEST_CONFIG = {"myList": [1, 2, 3, 4]}
    TEST_CONFIG_ERR = {"myList": [1, True, 2, 3]}
    TEST_CONFIG_REQ = {"myList": HomogeneousValidator(int)}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ)
