.. _utils:

.. highlight:: python

Utilities
=========

Other utilities for configuration file parsing are included with dictator.

Fragment substitution
---------------------

Using the *FragmentReplace* and *AutoFragmentReplace* classes, one can replace fragments of string values with a previously parsed
key value:

::

   MY_CONFIG = {"my_key": "my_value",
                "other_key": "${my_key}_foobar"}

   MY_CONFIG_REQ = {"my_key": str,
                    "other_key": AutoFragmentReplace()}

   validate_config(MY_CONFIG, MY_CONFIG_REQ)
   # returns:
   # {"my_key": "my_value", "other_key": "my_value_foobar"}

To access keys from a parent configuration in the case where nested configurations (nested dictionaries) are present and parsed,
or access keys from the top-level of the configuration hierarchy, two different patterns can be used:

- Accessing parent key: :code:`"${..KEY_NAME}`
- Accessing top-level key: :code:`"${:KEY_NAME}"`
