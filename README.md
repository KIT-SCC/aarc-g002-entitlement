# AARC G002 Entitlement Parser

# Introduction
This package provides a python Class to parse and compare entitlements according
to the AARC-G002 Recommendation https://aarc-project.eu/guidelines/aarc-g002.


## Example

```python
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
```

For more examples:
```shell
./example.py
```

## Installation
```shell
pip install --user aarc-g002-entitlement
```

## Documentation
The documentation is available at [readthedocs](https://aarc-g002-entitlement.readthedocs.io/en/latest/).


# Tests
Run tests for the supported python versions:
```shell
pip install tox
tox
```

# Funding Notice
The AARC project has received funding from the European Union’s Horizon
2020 research and innovation programme under grant agreement No 653965 and
730941.

