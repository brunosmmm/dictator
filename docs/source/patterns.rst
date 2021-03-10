.. _patterns:

.. highlight:: python

Usage Patterns
==============

Usage patterns are useful for building more complex validation structures. The first pattern emerges naturally from the
definitions of dictator validators:

::

   @validate_x
   @validate_y
   def my_validator_function(value, **kwargs):
     """Do some validation."""
     return value


By combining more than one validator used as decorators to a validation function, we create a condition akin to a logical
AND.

Validation negation
-------------------

We can negate validation logic by using the included *InvertValidation* class:

::

   # Never fails!
   @InvertValidation()
   def my_validator(value, **kwargs):
     """Always fail."""
     raise ValidationError("the entire world is wrong")

Note that if using multiple stacked validation decorators, the entire history of validation preceding the *InvertValidation* is
negated, not the most recent:

::

   # == not(validate_x && validate_y)
   @InvertValidation()
   @validate_x
   @validate_y
   def my_validator(value, **kwargs):
     """Perform validation."""
     return value

   # == validate_x && not validate_y
   @validate_x
   @InvertValidation()
   @validate_y
   def other_validator(value, **kwargs):
     """Other validation."""
     return value

Validation union
----------------

Union of two or more validators can be achieved by usage of the ValidatorUnion validator:

::

   @ValidatorUnion(validate_integer, validate_string)
   def my_validator(value, **kwargs):
     """Works with either integers or strings."""
     return value

Note that if the first validator flags the value as validated, the next validations are not executed.
