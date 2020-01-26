"""Test malformed configurations."""

import pytest
from dictator.config import validate_config
from dictator.errors import KeyDeclarationError


def test_invalid_key():
    """Test invalid configuration key."""
    TEST_CONFIG = {0: "test"}
    TEST_REQ = {}

    with pytest.raises(TypeError):
        validate_config(TEST_CONFIG, TEST_REQ)


def test_invalid_req():
    """Test invalid key declaration."""

    TEST_CONFIG = {0: "test"}
    TEST_REQ = {0: str}
    TEST_OPT = {1: str}

    with pytest.raises(KeyDeclarationError):
        validate_config(TEST_CONFIG, TEST_REQ)

    with pytest.raises(KeyDeclarationError):
        validate_config(TEST_CONFIG, {}, TEST_OPT)


def test_invalid_config():
    """Test invalid config description."""
    TEST_CONFIG = [1, 2, 3]
    TEST_CONFIG_1 = {"some": "key"}
    TEST_REQ = {}
    TEST_REQ_1 = []
    TEST_OPT_1 = []

    with pytest.raises(TypeError):
        validate_config(TEST_CONFIG, TEST_REQ)

    with pytest.raises(TypeError):
        validate_config(TEST_CONFIG_1, TEST_REQ_1)

    with pytest.raises(TypeError):
        validate_config(TEST_CONFIG_1, TEST_REQ, TEST_OPT_1)
