#!/usr/bin/env python
from aarc_g002_entitlement import Aarc_g002_entitlement

if __name__ == "__main__":
    required_group = "urn:geant:h-df.de:group:aai-admin:role=member#unity.helmholtz-data-federation.de"
    actual_group = "urn:geant:h-df.de:group:aai-admin:role=member#unity.helmholtz-data-federation.de"
    required_entitlement = Aarc_g002_entitlement(required_group)
    actual_entitlement = Aarc_g002_entitlement(actual_group)
    print("\n1: Simple case: Different authorities, everything else same")
    print("    Required group: " + required_group)
    print("    Actual   group: " + actual_group)
    print(
        "    is_contained_in:   => {}".format(
            required_entitlement.is_contained_in(actual_entitlement)
        )
    )
    print(
        "        (are equal:    => {})".format(
            required_entitlement == actual_entitlement
        )
    )

    required_group = "urn:geant:h-df.de:group:aai-admin:role=member#unity.helmholtz-data-federation.de"
    actual_group = "urn:geant:h-df.de:group:aai-admin:role=member#backupserver.used.for.developmt.de"
    required_entitlement = Aarc_g002_entitlement(required_group)
    actual_entitlement = Aarc_g002_entitlement(actual_group)

    print("\n2: Simple case: Different authorities, everything else same")
    print("    Required group: " + required_group)
    print("    Actual   group: " + actual_group)
    print(
        "    is_contained_in:   => {}".format(
            required_entitlement.is_contained_in(actual_entitlement)
        )
    )
    print(
        "        (are equal:    => {})".format(
            required_entitlement == actual_entitlement
        )
    )

    required_group = (
        "urn:geant:h-df.de:group:aai-admin#unity.helmholtz-data-federation.de"
    )
    actual_group = "urn:geant:h-df.de:group:aai-admin:role=member#backupserver.used.for.developmt.de"
    required_entitlement = Aarc_g002_entitlement(required_group)
    actual_entitlement = Aarc_g002_entitlement(actual_group)

    print("\n3: Role assigned but not required")
    print("    Required group: " + required_group)
    print("    Actual   group: " + actual_group)
    print(
        "    is_contained_in:   => {}".format(
            required_entitlement.is_contained_in(actual_entitlement)
        )
    )
    print(
        "        (are equal:    => {})".format(
            required_entitlement == actual_entitlement
        )
    )

    required_group = "urn:geant:h-df.de:group:aai-admin:role=member#unity.helmholtz-data-federation.de"
    actual_group = (
        "urn:geant:h-df.de:group:aai-admin#backupserver.used.for.developmt.de"
    )
    required_entitlement = Aarc_g002_entitlement(required_group)
    actual_entitlement = Aarc_g002_entitlement(actual_group)

    print("\n4: Role required but not assigned")
    print("    Required group: " + required_group)
    print("    Actual   group: " + actual_group)
    print(
        "    is_contained_in:   => {}".format(
            required_entitlement.is_contained_in(actual_entitlement)
        )
    )
    print(
        "        (are equal:    => {})".format(
            required_entitlement == actual_entitlement
        )
    )

    required_group = "urn:geant:h-df.de:group:aai-admin:special-admins#unity.helmholtz-data-federation.de"
    actual_group = (
        "urn:geant:h-df.de:group:aai-admin#backupserver.used.for.developmt.de"
    )
    required_entitlement = Aarc_g002_entitlement(required_group)
    actual_entitlement = Aarc_g002_entitlement(actual_group)

    print("\n5: Subgroup required, but not available")
    print("    Required group: " + required_group)
    print("    Actual   group: " + actual_group)
    print(
        "    is_contained_in:   => {}".format(
            required_entitlement.is_contained_in(actual_entitlement)
        )
    )
    print(
        "        (are equal:    => {})".format(
            required_entitlement == actual_entitlement
        )
    )

    required_group = (
        "urn:geant:h-df.de:group:aai-admin#unity.helmholtz-data-federation.de"
    )
    actual_group = "urn:geant:h-df.de:group:aai-admin:testgroup:special-admins#backupserver.used.for.developmt.de"
    required_entitlement = Aarc_g002_entitlement(required_group)
    actual_entitlement = Aarc_g002_entitlement(actual_group)

    print("\n6: Edge case: User in subgroup, but only supergroup required")
    print("    Required group: " + required_group)
    print("    Actual   group: " + actual_group)
    print(
        "    is_contained_in:   => {}".format(
            required_entitlement.is_contained_in(actual_entitlement)
        )
    )
    print(
        "        (are equal:    => {})".format(
            required_entitlement == actual_entitlement
        )
    )

    required_group = "urn:geant:h-df.de:group:aai-admin:role=admin#unity.helmholtz-data-federation.de"
    actual_group = "urn:geant:h-df.de:group:aai-admin:special-admins:role=admin#backupserver.used.for.developmt.de"
    required_entitlement = Aarc_g002_entitlement(required_group)
    actual_entitlement = Aarc_g002_entitlement(actual_group)

    print("\n7: role required for supergroup but only assigned for subgroup")
    print("    Required group: " + required_group)
    print("    Actual   group: " + actual_group)
    print(
        "    is_contained_in:   => {}".format(
            required_entitlement.is_contained_in(actual_entitlement)
        )
    )
    print(
        "        (are equal:    => {})".format(
            required_entitlement == actual_entitlement
        )
    )
