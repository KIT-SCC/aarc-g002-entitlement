# AARC G002 Entitlement Parser

# Introduction
As part of the AARC Project several recommendations were made. G002
https://aarc-project.eu/guidelines/aarc-g002 describes encoding group
membersip in entitlements.

This package provides a python Class to parse and compare such entitlements.

# Example

```
    required_group= 'urn:geant:h-df.de:group:aai-admin#unity.helmholtz-data-federation.de'
    actual_group  = 'urn:geant:h-df.de:group:aai-admin:role=member#backupserver.used.for.developmt.de'

    required_entitlement = Aarc_g002_entitlement(required_group)
    actual_entitlement   = Aarc_g002_entitlement(actual_group)

    print('\n3: Role assigned but not required')
    print('    is_contained_in:   => {}'.format(required_entitlement.is_contained_in(actual_entitlement)))
    print('        (are equal:    => {})'.format(required_entitlement == actual_entitlement))
```

# Funding Notice 
The AARC project has received funding from the European Union’s Horizon
2020 research and innovation programme under grant agreement No 653965 and
730941.
