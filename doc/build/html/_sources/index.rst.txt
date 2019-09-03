AARC-G002 Entitlements
======================

Release v\ |version|.

This package provides a python Class to parse and compare entitlements according
to the AARC-G002 Recommendation https://aarc-project.eu/guidelines/aarc-g002


Example
-------

.. code-block:: console

    required_group= 'urn:geant:h-df.de:group:aai-admin#unity.helmholtz-data-federation.de'
    actual_group  = 'urn:geant:h-df.de:group:aai-admin:role=member#backupserver.used.for.developmt.de'

    required_entitlement = Aarc_g002_entitlement(required_group)
    actual_entitlement   = Aarc_g002_entitlement(actual_group)

    print('\n3: Role assigned but not required')
    print('    is_contained_in:   => {}'.format(required_entitlement.is_contained_in(actual_entitlement)))
    print('        (are equal:    => {})'.format(required_entitlement == actual_entitlement))

