"""Test validator combinations."""

import pytest
from dictator.validators.util import ValidateUnion
from dictator.errors import ValidationError
from dictator.config import validate_config


def test_union():
    """Test union."""

    TEST_CONFIG_1 = {"myKey": 1}
    TEST_CONFIG_2 = {"myKey": False}
    TEST_CONFIG_REQ = {"myKey": ValidateUnion(int, bool)}

    validate_config(TEST_CONFIG_1, TEST_CONFIG_REQ)
    validate_config(TEST_CONFIG_2, TEST_CONFIG_REQ)

    with pytest.raises(ValidationError):
        validate_config({"myKey": []}, TEST_CONFIG_REQ)
