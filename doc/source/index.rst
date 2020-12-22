AARC-G002 Entitlements
======================

This package provides a python Class to parse and compare entitlements according
to the AARC-G002 Recommendation https://aarc-community.org/guidelines/aarc-g002.


Example
-------

.. code-block:: python

     from aarc_g002_entitlement import Aarc_g002_entitlement

     required = Aarc_g002_entitlement(
         'urn:geant:h-df.de:group:aai-admin',
         strict=False,
     )
     actual = Aarc_g002_entitlement(
         'urn:geant:h-df.de:group:aai-admin:role=member#backupserver.used.for.developmt.de',
     )

     # is a user with actual permitted to use a resource which needs required?
     permitted = required.is_contained_in(actual) # True in this case

     # are the two entitlements the same?
     equals = required == actual # False in this case

API
---
.. automodule:: aarc_g002_entitlement
   :members:
