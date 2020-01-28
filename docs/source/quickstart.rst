.. _quickstart:

Dictator Quickstart
===================

Dictator validates hierarchical configuration values based on a dictionary structure.
This is very useful for usage with JSON-based configurations, for example, which map
easily to Python dictionaries using the build-in json module.


Let's begin with a handcrafted configuration. For instance, we want to validate that
a configuration contains some required keys, and enforce the data type for those keys'
values. We start with a configuration that requires the keys *answer* (integer) and
*description* (string).

Here's an example configuration:

::

   TEST_CONFIG = {"answer": 42,
                  "description": "meaning of life and universe"}

We need to tell dictator to validate that both keys exist and also validate their datatypes.
This is accomplished by writing some rules:

::

   TEST_CONFIG_REQ = {"answer": int, "description": string}

TEST_CONFIG_REQ tells the validator two main things: first, that the keys *answer* and *description* are
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
Besides python base types, callables can also be specified as key value is configuration definitions.

The library of extended default validators is composed of:

* Positive integer validator
* Percent validator
* Integer range validator
* Choice validator (choose between a list of possible choices)
* Homogeneous list validator (validates that all elements in a list are of a same type)
* Sub-configuration validators: validate child elements as first-class configurations

Default validators are dynamically generated from internal implementations and are accesible through
the dictator.validator.default.DEFAULT_VALIDATORS object.

User-defined validators
-----------------------

Since a callable can act as a validator, and will be called to validate the value passed in, a validator
can be defined in a straightforward way as a function:

::

   def validate_answer(theanswer, **kwargs):
      """Validate."""
      # do something
      if theanswer != 42:
         raise ValidationError("incorrect answer! the answer is 42!")

We come to an important characteristic of the validator system: it is actually possible to validate and
modify the value of a key, by returning something other than None. In the case above, we just move on,
keeping the value.

The mechanism for signaling an invalid value is to raise an exception, as demonstrated above.

Composite validators
--------------------

Now that we can write a simple validator, how do we go about compositing multiple validation rules
easily? The answer is in harnessing the power of Python decorators. Let's modify our configuration
a bit:

::

  TEST_CONFIG = {"answer": 42,
                 "meanings": [{"what":"life"}, {"what":"universe"}]}

How do we validate that:

1. answer is an integer
2. meanings is a list
3. meanings can contain sub-meanings "life" and "universe"

::

  from dictator.validators.base import validate_string
  from dictator.validators.lists import ValidateChoice, SubListValidator
  from dictator.errors import ValidationError


  def validate_answer(_answer, **kwargs):
      if isinstance(_answer, str) and _answer == "fortytwo":
          return 42
      if isinstance(_answer, int) and _answer == 42:
          return 42

      raise ValidationError("that is not the answer")


  @ValidateChoice("life", "universe")
  @validate_string
  def validate_meanings(meaning, **kwargs):
      """Validate possible meanings."""
      return meaning


  # our meanings are sub-configurations!
  MEANING_REQ = {"what": validate_meanings}
  TEST_CONFIG_REQ = {
      "answer": validate_answer,
      "meanings": SubListValidator(MEANING_REQ),
  }

The base validators are actually implemented in this way, and the default validator module generates
functions that are decorated by the base validators.

