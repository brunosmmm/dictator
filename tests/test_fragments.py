"""Test configuration fragment replacement."""

import pytest
from dictator.validators.replace import (
    FragmentReplace,
    AutoFragmentReplace,
    FragmentError,
)
from dictator.validators.lists import SubListValidator
from dictator.config import validate_config


def test_fragment_replace():
    """Test manual fragment replacement."""
    TEST_CONFIG = {
        "my_key": "my_value",
        "my_other_key": "REPLACETHIS_dontreplace",
    }
    TEST_REQ = {
        "my_key": str,
        "my_other_key": FragmentReplace({"REPLACETHIS": "my_key"}),
    }

    return validate_config(TEST_CONFIG, TEST_REQ)


def test_auto_fragment_replace():
    """Test automatic fragment replacement."""
    TEST_CONFIG = {
        "my_key": "my_value",
        "my_other_key": "${my_key}_dontreplace",
    }
    TEST_REQ = {"my_key": str, "my_other_key": AutoFragmentReplace()}

    return validate_config(TEST_CONFIG, TEST_REQ)


def test_parent_fragment_replace():
    """Test auto replacement with value from parent config."""
    TEST_CONFIG = {
        "my_key": "my_value",
        "other_keys": [{"my_other_key": "${..my_key}_blabla"}],
    }
    TEST_REQ = {
        "my_key": str,
        "other_keys": SubListValidator(
            {"my_other_key": AutoFragmentReplace()}
        ),
    }

    return validate_config(TEST_CONFIG, TEST_REQ)


def test_toplevel_fragment_replace():
    """Test auto replacement with value from toplevel config."""
    TEST_CONFIG = {
        "my_key": "my_value",
        "other_keys": [{"my_other_key": "${:my_key}_blabla"}],
    }
    TEST_REQ = {
        "my_key": str,
        "other_keys": SubListValidator(
            {"my_other_key": AutoFragmentReplace()}
        ),
    }

    return validate_config(TEST_CONFIG, TEST_REQ)


def test_fragment_replace_fail():
    """Test fragment replacement failure."""
    TEST_CONFIG = {
        "my_key": "my_value",
        "my_other_key": "${my_key2}_dontreplace",
    }
    TEST_REQ = {"my_key": str, "my_other_key": AutoFragmentReplace()}

    with pytest.raises(FragmentError):
        validate_config(TEST_CONFIG, TEST_REQ)

    return validate_config(TEST_CONFIG, TEST_REQ, my_key2="bla")


def test_fragment_key():
    """Test fragments which access keys."""
    TEST_CONFIG = {
        "my_key": {"foo": "bar"},
        "my_other_key": "${my_key::foo}_dontreplace",
    }

    TEST_CONFIG_2 = {
        "my_key": {"foo": "bar"},
        "my_other_key": "${:my_key::foo}_dontreplace",
    }
    TEST_REQ = {"my_key": dict, "my_other_key": AutoFragmentReplace()}

    validate_config(TEST_CONFIG, TEST_REQ)
    return validate_config(TEST_CONFIG_2, TEST_REQ)


if __name__ == "__main__":
    print(test_fragment_replace())
    print(test_auto_fragment_replace())
    print(test_parent_fragment_replace())
    print(test_fragment_replace_fail())
    print(test_toplevel_fragment_replace())
    print(test_fragment_key())
