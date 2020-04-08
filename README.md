[![Documentation Status](https://readthedocs.org/projects/aarc-g002-entitlement/badge/?version=latest&token=5f5165c8ebde7726ae9df9f62331a59e7344d6e61a4bb9ea8c97cecfae25f4f3)](https://aarc-g002-entitlement.readthedocs.io/en/latest/?badge=latest)
# AARC G002 Entitlement Parser

# Introduction
This package provides a python Class to parse and compare entitlements according
to the AARC-G002 Recommendation https://aarc-project.eu/guidelines/aarc-g002.


# Example

```python
from aarc_g002_entitlement import Aarc_g002_entitlement

required = Aarc_g002_entitlement(
    'urn:geant:h-df.de:group:aai-admin',
    strict=False)
actual = Aarc_g002_entitlement(
    'urn:geant:h-df.de:group:aai-admin:role=member#backupserver.used.for.developmt.de')

# is a user with actual permitted to use a resource which needs required?
permitted = required.is_contained_in(actual) # True in this case

# are the two entitlements the same?
equals = required == actual # False in this case
```

For more examples: `./example.py`

# Installation
```
pip --user install aarc-g002-entitlement
```

# Documentation
```
tox -e docs
```
After this, the documentation should be located at `doc/build/index.html`.

Documentation is also available at [Readthedocs](https://aarc-g002-entitlement.readthedocs.io/en/latest)

# Tests
Run tests for all supported python versions
```
tox
```

# Funding Notice
The AARC project has received funding from the European Union’s Horizon
2020 research and innovation programme under grant agreement No 653965 and
730941.
