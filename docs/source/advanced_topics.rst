.. _advanced_topics:

.. highlight:: python

Advanced Topics
===============

Stateful Validation
-------------------

Regular validation is stateless, that is, as key, value pairs come in, the value is validated by a
function, which might choose to keep the value untouched or modify it. However, there is no outcome, that is,
no state information is stored and/or modified.

We can perform stateful validation by declaring our own validator class based on the Validator class
as follows in this example:

::

  from dictator.config import validate_config
  from dictator.validators.lists import ValidateChoice, SubListValidator
  from dictator.validators import Validator


  class MeaningValidator(Validator):
      """Validate real meaning."""

      def __init__(self, *possible_meanings, **kwargs):
          """Initialize."""
          super().__init__()
          self._possible_meanings = possible_meanings
          self._meanings = []

      def validate(self, _value, **kwargs):
          """Perform validation."""

          @ValidateChoice(*self._possible_meanings)
          def _validate(_value, **kwargs):
              self._meanings.append(value)
              return fn(_value, **kwargs)

          return _validate(_value, **kwargs)

      @property
      def correct_meaning(self):
          """Get whether the meaning is correct."""
          if "life" in self._meanings and "universe" in self._meanings:
              return True

          return False


  stateful_meaning_validator = MeaningValidator("life", "universe")

  # our meanings are sub-configurations!
  MEANING_REQ = {"what": stateful_meaning_validator}
  TEST_CONFIG_REQ = {
      "answer": None,
      "meanings": SubListValidator(MEANING_REQ),
  }
  validate_config(TEST_CONFIG, TEST_CONFIG_REQ)
  print(stateful_meaning_validator.correct_answer)


This validator works by storing state related to the meanings that it encounters as the validation is
performed on each key,value pair. In this example, we can verify that the meaning is correct after validation
is finished. Note that in the process, it also uses the ValidateChoice validator to ensure that only the
allowed choice values are passed in.
