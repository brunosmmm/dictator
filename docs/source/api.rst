.. _api:

API reference
=============


Validators
----------

.. automodule:: dictator.validators
.. autoclass:: Validator
               :members: __init__, validate


.. automodule:: dictator.validators.base
.. autoclass:: ValidatorFactory
               :members: __init__


Type-based validators
---------------------

.. autoclass:: ValidateType
               :members: __init__

Integer-based validators
^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: dictator.validators.integer
.. autoclass:: ValidateIntRange
               :members: __init__

List-based validators
---------------------

.. automodule:: dictator.validators.lists
.. autoclass:: ValidateChoice
               :members: __init__
.. autoclass:: SubListValidator
               :members: __init__
.. autoclass:: HomogeneousValidator
               :members: __init__

Mapping-based validators
------------------------

.. automodule:: dictator.validators.maps
.. autoclass:: SubDictValidator
               :members: __init__

Validator composition
---------------------

.. automodule:: dictator.validators.util
.. autoclass:: InvertValidation
               :members: __init__
.. autoclass:: ValidateUnion
               :members: __init__
