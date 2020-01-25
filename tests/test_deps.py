"""Test dependencies."""

import pytest
from dictator.config import validate_config, ConfigurationError
from dictator.util import KeyDependency, KeyDependencyMap


@KeyDependency("myDependency")
def _validate_my_key(_value, **kwargs):
    """Validate myKey."""
    return _value


@KeyDependencyMap(someValue="someKey", otherValue="otherKey")
def _validate_my_key_mapped(_value, **kwargs):
    """Validate myKey depending on value."""
    return _value


def test_dependency():
    """Test key dependency."""
    TEST_CONFIG = {"myKey": "someValue", "myDependency": 42}
    TEST_CONFIG_ERR = {"myKey": "someValue"}  # missing dependency
    TEST_CONFIG_REQ = {"myKey": _validate_my_key}
    TEST_CONFIG_OPT = {"myDependency": int}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ, TEST_CONFIG_OPT)

    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ, TEST_CONFIG_OPT)


def test_dependency_map():
    """Test key dependency."""
    TEST_CONFIG = {"myKey": "someValue", "someKey": 42, "otherKey": "bla"}
    TEST_CONFIG_ERR = {"myKey": "someValue"}  # missing dependency
    TEST_CONFIG_REQ = {"myKey": _validate_my_key_mapped}
    TEST_CONFIG_OPT = {"someKey": int, "otherKey": str}

    validate_config(TEST_CONFIG, TEST_CONFIG_REQ, TEST_CONFIG_OPT)

    with pytest.raises(ConfigurationError):
        validate_config(TEST_CONFIG_ERR, TEST_CONFIG_REQ, TEST_CONFIG_OPT)
