# pylint: disable=invalid-name, missing-docstring, no-self-use

import pytest

from aarc_g002_entitlement import Aarc_g002_entitlement
from aarc_g002_entitlement import Aarc_g002_entitlement_Error
from aarc_g002_entitlement import Aarc_g002_entitlement_ParseError


class TestAarc_g002_entitlement:
    def test_equality(self):
        required_group = "urn:geant:h-df.de:group:aai-admin:role=member#unity.helmholtz-data-federation.de"
        actual_group   = "urn:geant:h-df.de:group:aai-admin:role=member#unity.helmholtz-data-federation.de"
        req_entitlement = Aarc_g002_entitlement(required_group)
        act_entitlement = Aarc_g002_entitlement(actual_group)
        assert act_entitlement == req_entitlement
        assert req_entitlement.is_contained_in(act_entitlement)

    def test_order_of_subnamespaces_equality(self):
        required_group = "urn:geant:h-df.de:subns1:subns2:group:aai-admin:role=member#unity.helmholtz-data-federation.de"
        actual_group   = "urn:geant:h-df.de:subns2:subns1:group:aai-admin:role=member#unity.helmholtz-data-federation.de"
        req_entitlement = Aarc_g002_entitlement(required_group)
        act_entitlement = Aarc_g002_entitlement(actual_group)
        assert act_entitlement != req_entitlement
        assert not req_entitlement.is_contained_in(act_entitlement)

    def test_order_of_subgroups_equality(self):
        required_group = "urn:geant:h-df.de:group:aai-admin:subgroup1:subgroup2:subgroup3:role=member#unity.helmholtz-data-federation.de"
        actual_group   = "urn:geant:h-df.de:group:aai-admin:subgroup2:subgroup1:subgroup3:role=member#unity.helmholtz-data-federation.de"
        req_entitlement = Aarc_g002_entitlement(required_group)
        act_entitlement = Aarc_g002_entitlement(actual_group)
        assert act_entitlement != req_entitlement
        assert not req_entitlement.is_contained_in(act_entitlement)

    def test_order_of_subnamespaces_out_of_bounds_equality(self):
        required_group = "urn:geant:h-df.de:subns1:subns2:subns0:group:aai-admin:role=member#unity.helmholtz-data-federation.de"
        actual_group   = "urn:geant:h-df.de:subns1:subns2:group:aai-admin:role=member#unity.helmholtz-data-federation.de"
        req_entitlement = Aarc_g002_entitlement(required_group)
        act_entitlement = Aarc_g002_entitlement(actual_group)
        assert act_entitlement != req_entitlement
        assert not req_entitlement.is_contained_in(act_entitlement)

    def test_order_of_subgroups_out_of_bounds_equality(self):
        required_group = "urn:geant:h-df.de:group:aai-admin:subgroup1:subgroup2:subgroup3:role=member#unity.helmholtz-data-federation.de"
        actual_group   = "urn:geant:h-df.de:group:aai-admin:subgroup1:subgroup2:role=member#unity.helmholtz-data-federation.de"
        req_entitlement = Aarc_g002_entitlement(required_group)
        act_entitlement = Aarc_g002_entitlement(actual_group)
        assert act_entitlement != req_entitlement
        assert not req_entitlement.is_contained_in(act_entitlement)

    def test_simple(self):
        required_group = "urn:geant:h-df.de:group:aai-admin:role=member#unity.helmholtz-data-federation.de"
        actual_group   = "urn:geant:h-df.de:group:aai-admin:role=member#backupserver.used.for.developmt.de"
        req_entitlement = Aarc_g002_entitlement(required_group)
        act_entitlement = Aarc_g002_entitlement(actual_group)
        assert req_entitlement.is_contained_in(act_entitlement)

    def test_group(self):
        required_group = "urn:geant:h-df.de:group:aai-admin"
        actual_group   = "urn:geant:h-df.de:group:aai-admin#backupserver.used.for.developmt.de"
        req_entitlement = Aarc_g002_entitlement(required_group, strict=False)
        act_entitlement = Aarc_g002_entitlement(actual_group, strict=False)
        assert req_entitlement.is_contained_in(act_entitlement)

    def test_intentional_authority_mismatch(self):
        required_group = "urn:geant:h-df.de:group:aai-admin#authority_a"
        actual_group   = "urn:geant:h-df.de:group:aai-admin#totally_different_authority"
        req_entitlement = Aarc_g002_entitlement(required_group, strict=False)
        act_entitlement = Aarc_g002_entitlement(actual_group, strict=False)
        assert req_entitlement.is_contained_in(act_entitlement)

    def test_intentional_authority_mismatch_2(self):
        required_group = "urn:geant:h-df.de:group:aai-admin"
        actual_group   = "urn:geant:h-df.de:group:aai-admin#totally_different_authority"
        req_entitlement = Aarc_g002_entitlement(required_group, strict=False)
        act_entitlement = Aarc_g002_entitlement(actual_group, strict=False)
        assert req_entitlement.is_contained_in(act_entitlement)

    def test_role_not_required(self):
        required_group = "urn:geant:h-df.de:group:aai-admin#unity.helmholtz-data-federation.de"
        actual_group   = "urn:geant:h-df.de:group:aai-admin:role=member#backupserver.used.for.developmt.de"
        req_entitlement = Aarc_g002_entitlement(required_group)
        act_entitlement = Aarc_g002_entitlement(actual_group)
        assert req_entitlement.is_contained_in(act_entitlement)

    def test_role_required(self):
        required_group = "urn:geant:h-df.de:group:aai-admin:role=member#unity.helmholtz-data-federation.de"
        actual_group   = "urn:geant:h-df.de:group:aai-admin#backupserver.used.for.developmt.de"
        req_entitlement = Aarc_g002_entitlement(required_group)
        act_entitlement = Aarc_g002_entitlement(actual_group)
        assert not req_entitlement.is_contained_in(act_entitlement)

    def test_subgroup_required(self):
        required_group = "urn:geant:h-df.de:group:aai-admin:special-admins#unity.helmholtz-data-federation.de"
        actual_group   = ("urn:geant:h-df.de:group:aai-admin#backupserver.used.for.developmt.de")
        req_entitlement = Aarc_g002_entitlement(required_group)
        act_entitlement = Aarc_g002_entitlement(actual_group)
        assert not req_entitlement.is_contained_in(act_entitlement)

    def test_subgroup_required_and_available(self):
        required_group = "urn:geant:h-df.de:group:m-team:feudal-developers"
        actual_group   = "urn:geant:h-df.de:group:m-team:feudal-developers#login.helmholtz.de"
        req_entitlement = Aarc_g002_entitlement(required_group, strict=False)
        act_entitlement = Aarc_g002_entitlement(actual_group, strict=False)
        assert req_entitlement.is_contained_in(act_entitlement)

    def test_user_in_subgroup(self):
        required_group = "urn:geant:h-df.de:group:aai-admin"
        actual_group   = "urn:geant:h-df.de:group:aai-admin:special-admins#backupserver.used.for.developmt.de"
        req_entitlement = Aarc_g002_entitlement(required_group, strict=False)
        act_entitlement = Aarc_g002_entitlement(actual_group, strict=False)
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
            "urn:mace:egi.eu:aai.egi.eu:vm_operator@eosc-synergy.eu",
            "urn:mace:egi.eu:aai.egi.eu:admins:member@covid19.eosc-synergy.eu",
        ]
    )
    def test_non_aarc_entitlement(self, actual_group):
        with pytest.raises(Aarc_g002_entitlement_ParseError):
            Aarc_g002_entitlement(actual_group, strict=False, raise_error_if_unparseable=False)

    @pytest.mark.parametrize(
        'required_group',
        [
            "urn:geant:h-df.de:group:aai-admin:role=admin",
            "urn:geant:h-df.de:group:aai-admin",
            "urn:geant:kit.edu:group:DFN-SLCS",
        ]
    )
    def test_failure_incomplete_but_valid_entitlement(self, required_group):
        Aarc_g002_entitlement(required_group, strict=False)

    def test_failure_incomplete_invalid_entitlement(self):
        required_group = "urn:geant:h-df.de"
        with pytest.raises(Aarc_g002_entitlement_ParseError):
            Aarc_g002_entitlement(required_group, raise_error_if_unparseable=True)
