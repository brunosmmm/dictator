"""Test configuration fragment replacement."""

from dictator.validators.replace import FragmentReplace
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


if __name__ == "__main__":
    print(test_fragment_replace())
