"""Test validator combinations."""

import pytest
from dictator.validators.util import ValidateUnion, InvertValidation
from dictator.errors import ValidationError
from dictator.config import validate_config
from dictator.validators.base import validate_string


def test_union():
    """Test union."""

    TEST_CONFIG_1 = {"myKey": 1}
    TEST_CONFIG_2 = {"myKey": False}
    TEST_CONFIG_REQ = {"myKey": ValidateUnion(int, bool)}

    validate_config(TEST_CONFIG_1, TEST_CONFIG_REQ)
    validate_config(TEST_CONFIG_2, TEST_CONFIG_REQ)

    with pytest.raises(ValidationError):
        validate_config({"myKey": []}, TEST_CONFIG_REQ)


def test_negate():
    """Test negation."""

    TEST_CONFIG_1 = {"myKey": False}
    TEST_CONFIG_REQ_1 = {"myKey": InvertValidation(int)}
    TEST_CONFIG_REQ_2 = {"myKey": InvertValidation(bool)}

    validate_config(TEST_CONFIG_1, TEST_CONFIG_REQ_1)

    with pytest.raises(ValidationError):
        validate_config(TEST_CONFIG_1, TEST_CONFIG_REQ_2)

    @InvertValidation()
    @validate_string
    def _validator(_value, **kwargs):
        return _value

    validate_config(TEST_CONFIG_1, {"myKey": _validator})
