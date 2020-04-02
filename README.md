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

# Tests
Run tests for all supported python versions
```
tox
```

# Funding Notice
The AARC project has received funding from the European Union’s Horizon
2020 research and innovation programme under grant agreement No 653965 and
730941.
