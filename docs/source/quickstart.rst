
Dictator Quickstart
===================

Dictator validates hierarchical configuration values based on a dictionary structure.
This is very useful for usage with JSON-based configurations, for example, which map
easily to Python dictionaries using the build-in json module.


Let's begin with a handcrafted configuration. For instance, we want to validate that
a configuration contains some required keys, and enforce the data type for those keys'
values. We start with a configuration that requires the keys *reason* (integer) and
*description* (string).

Here's an example configuration:

::
   TEST_CONFIG = {"reason": 42, "description": "meaning of life and universe"}

We need to tell dictator to validate that both keys exist and also validate their datatypes.
This is accomplished by writing some rules:

::
   TEST_CONFIG_REQ = {"reason": int, "description": string}

TEST_CONFIG_REQ tells the validator two main things: first, that the keys *reason* and *description* are
required keys, second, that the data types must be integer and string respectively.

Now, we validate the configuration by calling the validate_config function:

::
   validate_config(TEST_CONFIG, TEST_CONFIG_REQ)

That's it for basic configurations which require only key existence and data type validation. Note that
this type of validation using a mapping directly to the native Python type only works for the following
basic Python types:

* int
* str
* list (validated by type only, no other item validation)
* dict (validated by type only, NOT as sub-configuration)
* bool
* float

So you'll quickly notice that for a slightly more complex problem, such as validating for positive integers
only, or validating for a list of homogeneously typed elements or validating a sub-configuration, we need
some other mechanism.

Extended default validators
---------------------------

For validation of slightly more complex and common patterns, dictator provides the default validator module.

User-defined validators
-----------------------
