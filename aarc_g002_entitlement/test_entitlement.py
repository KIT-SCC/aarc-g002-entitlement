# pylint: disable=bad-whitespace, invalid-name, missing-docstring

import pytest

from aarc_g002_entitlement import Aarc_g002_entitlement


class TestAarc_g002_entitlement:
    def test_equality(self):
        required_group = "urn:geant:h-df.de:group:aai-admin:role = member#unity.helmholtz-data-federation.de"
        actual_group = "urn:geant:h-df.de:group:aai-admin:role = member#unity.helmholtz-data-federation.de"
        req_entitlement = Aarc_g002_entitlement(required_group)
        act_entitlement = Aarc_g002_entitlement(actual_group)
        assert act_entitlement == req_entitlement
        assert req_entitlement.is_contained_in(act_entitlement)

    def test_simple(self):
        required_group = "urn:geant:h-df.de:group:aai-admin:role=member#unity.helmholtz-data-federation.de"
        actual_group = "urn:geant:h-df.de:group:aai-admin:role=member#backupserver.used.for.developmt.de"
        req_entitlement = Aarc_g002_entitlement(required_group)
        act_entitlement = Aarc_g002_entitlement(actual_group)
        assert req_entitlement.is_contained_in(act_entitlement)

    def test_role_not_required(self):
        required_group = "urn:geant:h-df.de:group:aai-admin#unity.helmholtz-data-federation.de"
        actual_group = "urn:geant:h-df.de:group:aai-admin:role=member#backupserver.used.for.developmt.de"
        req_entitlement = Aarc_g002_entitlement(required_group)
        act_entitlement = Aarc_g002_entitlement(actual_group)
        assert req_entitlement.is_contained_in(act_entitlement)

    def test_role_required(self):
        required_group = "urn:geant:h-df.de:group:aai-admin:role=member#unity.helmholtz-data-federation.de"
        actual_group = "urn:geant:h-df.de:group:aai-admin#backupserver.used.for.developmt.de"
        req_entitlement = Aarc_g002_entitlement(required_group)
        act_entitlement = Aarc_g002_entitlement(actual_group)
        assert not req_entitlement.is_contained_in(act_entitlement)

    def test_subgroup_required(self):
        required_group = "urn:geant:h-df.de:group:aai-admin:special-admins#unity.helmholtz-data-federation.de"
        actual_group = (
            "urn:geant:h-df.de:group:aai-admin#backupserver.used.for.developmt.de"
        )
        req_entitlement = Aarc_g002_entitlement(required_group)
        act_entitlement = Aarc_g002_entitlement(actual_group)
        assert not req_entitlement.is_contained_in(act_entitlement)

    def test_user_in_subgroup(self):
        required_group = "urn:geant:h-df.de:group:aai-admin"
        actual_group = "urn:geant:h-df.de:group:aai-admin:special-admins#backupserver.used.for.developmt.de"
        req_entitlement = Aarc_g002_entitlement(required_group, strict=False)
        act_entitlement = Aarc_g002_entitlement(actual_group)
        assert req_entitlement.is_contained_in(act_entitlement)

    def test_role_required_for_supergroup(self):
        required_group = "urn:geant:h-df.de:group:aai-admin:role=admin#unity.helmholtz-data-federation.de"
        actual_group   = "urn:geant:h-df.de:group:aai-admin:special-admins:role=admin#backupserver.used.for.developmt.de"
        req_entitlement = Aarc_g002_entitlement(required_group)
        act_entitlement = Aarc_g002_entitlement(actual_group)
        assert not req_entitlement.is_contained_in(act_entitlement)

    @pytest.mark.parametrize(
        'required_group,actual_group',
        [
            ("urn:geant:h-df.de:group:aai-admin", "urn:geant:kit.edu:group:bwUniCluster"),
            ("urn:geant:h-df.de:group:myExampleColab#unity.helmholtz-data-federation.de", "urn:geant:kit.edu:group:bwUniCluster"),
            ("urn:geant:h-df.de:group:aai-admin", "urn:geant:kit.edu:group:aai-admin"),
        ]
    )
    def test_foreign_entitlement(self, required_group, actual_group):
        actual_group = "urn:geant:kit.edu:group:bwUniCluster"
        req_entitlement = Aarc_g002_entitlement(required_group, strict=False)
        act_entitlement = Aarc_g002_entitlement(actual_group, strict=False)
        assert not req_entitlement.is_contained_in(act_entitlement)

    #     #
    @pytest.mark.parametrize(
        'actual_group',
        [
            "urn:mace:dir:entitlement:common-lib-terms",
            "urn:geant:kit.edu:group:DFN-SLCS",
        ]
    )
    def test_non_aarc_entitlement(self, actual_group):
        required_group = "urn:geant:h-df.de:group:aai-admin"
        req_entitlement = Aarc_g002_entitlement(required_group, strict=False)
        act_entitlement = Aarc_g002_entitlement(actual_group, strict=False, force=False)
        assert not req_entitlement.is_contained_in(act_entitlement)

    @pytest.mark.parametrize(
        'required_group',
        [
            "urn:geant:h-df.de:group:aai-admin:role=admin",
            "urn:geant:h-df.de:group:aai-admin",
        ]
    )
    def test_failure_incomplete_but_valid_entitlement(self, required_group):
        Aarc_g002_entitlement(required_group, strict=False)

    def test_failure_incomplete_invalid_entitlement(self):
        required_group = "urn:geant:h-df.de"
        with pytest.raises(ValueError):
            Aarc_g002_entitlement(required_group)
