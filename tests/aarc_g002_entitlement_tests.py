# pylint: disable=bad-whitespace, invalid-name, missing-docstring
import unittest
from aarc_g002_entitlement import Aarc_g002_entitlement

class Aarc_g002(unittest.TestCase):
    def test_equality(self):
        required_group = 'urn:geant:h-df.de:group:aai-admin:role = member#unity.helmholtz-data-federation.de'
        actual_group   = 'urn:geant:h-df.de:group:aai-admin:role = member#unity.helmholtz-data-federation.de'
        req_entitlement        = Aarc_g002_entitlement(required_group)
        act_entitlement        = Aarc_g002_entitlement(actual_group)
        self.assertEqual(req_entitlement.is_contained_in(act_entitlement), True)
        self.assertEqual(act_entitlement == req_entitlement, True)

    def test_simple(self):
        required_group= 'urn:geant:h-df.de:group:aai-admin:role=member#unity.helmholtz-data-federation.de'
        actual_group  = 'urn:geant:h-df.de:group:aai-admin:role=member#backupserver.used.for.developmt.de'
        req_entitlement        = Aarc_g002_entitlement(required_group)
        act_entitlement        = Aarc_g002_entitlement(actual_group)
        self.assertEqual(req_entitlement.is_contained_in(act_entitlement), True)

    def test_role_not_required(self):
        required_group= 'urn:geant:h-df.de:group:aai-admin#unity.helmholtz-data-federation.de'
        actual_group  = 'urn:geant:h-df.de:group:aai-admin:role=member#backupserver.used.for.developmt.de'
        req_entitlement        = Aarc_g002_entitlement(required_group)
        act_entitlement        = Aarc_g002_entitlement(actual_group)
        self.assertEqual(req_entitlement.is_contained_in(act_entitlement), True)

    def test_role_required(self):
        required_group= 'urn:geant:h-df.de:group:aai-admin:role=member#unity.helmholtz-data-federation.de'
        actual_group  = 'urn:geant:h-df.de:group:aai-admin#backupserver.used.for.developmt.de'
        req_entitlement        = Aarc_g002_entitlement(required_group)
        act_entitlement        = Aarc_g002_entitlement(actual_group)
        self.assertEqual(req_entitlement.is_contained_in(act_entitlement), False)

    def test_subgroup_required(self):
        required_group= 'urn:geant:h-df.de:group:aai-admin:special-admins#unity.helmholtz-data-federation.de'
        actual_group  = 'urn:geant:h-df.de:group:aai-admin#backupserver.used.for.developmt.de'
        req_entitlement        = Aarc_g002_entitlement(required_group)
        act_entitlement        = Aarc_g002_entitlement(actual_group)
        self.assertEqual(req_entitlement.is_contained_in(act_entitlement), False)

    def test_user_in_subgroup(self):
        required_group= 'urn:geant:h-df.de:group:aai-admin'
        actual_group  = 'urn:geant:h-df.de:group:aai-admin:special-admins#backupserver.used.for.developmt.de'
        req_entitlement        = Aarc_g002_entitlement(required_group, strict=False)
        act_entitlement        = Aarc_g002_entitlement(actual_group)
        self.assertEqual(req_entitlement.is_contained_in(act_entitlement), True)

    def test_role_required_for_supergroup(self):
        required_group= 'urn:geant:h-df.de:group:aai-admin:role=admin#unity.helmholtz-data-federation.de'
        actual_group  = 'urn:geant:h-df.de:group:aai-admin:special-admins:role=admin#backupserver.used.for.developmt.de'
        req_entitlement        = Aarc_g002_entitlement(required_group)
        act_entitlement        = Aarc_g002_entitlement(actual_group)
        self.assertEqual(req_entitlement.is_contained_in(act_entitlement), False)

    def test_foreign_entitlement_1(self):
        required_group= 'urn:geant:h-df.de:group:aai-admin'
        actual_group  = 'urn:geant:kit.edu:group:bwUniCluster'
        req_entitlement        = Aarc_g002_entitlement(required_group, strict=False)
        act_entitlement        = Aarc_g002_entitlement(actual_group, strict=False)
        self.assertEqual(req_entitlement.is_contained_in(act_entitlement), False)

    def test_foreign_entitlement_2(self):
        required_group= 'urn:geant:h-df.de:group:myExampleColab#unity.helmholtz-data-federation.de'
        actual_group  = 'urn:geant:kit.edu:group:bwUniCluster'
        req_entitlement        = Aarc_g002_entitlement(required_group)
        act_entitlement        = Aarc_g002_entitlement(actual_group, strict=False)
        print ("equality in ..._2: {}".format(req_entitlement.is_contained_in(act_entitlement)))
        self.assertEqual(req_entitlement.is_contained_in(act_entitlement), False)

    def test_foreign_entitlement_1(self):
        required_group= 'urn:geant:h-df.de:group:aai-admin'
        actual_group  = 'urn:geant:kit.edu:group:aai-admin'
        req_entitlement        = Aarc_g002_entitlement(required_group, strict=False)
        act_entitlement        = Aarc_g002_entitlement(actual_group, strict=False)
        self.assertEqual(req_entitlement.is_contained_in(act_entitlement), False)

    def test_non_aarc_entitlement_1(self):
        required_group= 'urn:geant:h-df.de:group:aai-admin'
        actual_group  = 'urn:mace:dir:entitlement:common-lib-terms'
        req_entitlement        = Aarc_g002_entitlement(required_group, strict=False)
        act_entitlement        = Aarc_g002_entitlement(actual_group, strict=False)
        self.assertEqual(req_entitlement.is_contained_in(act_entitlement), False)

        # "urn:geant:kit.edu:group:DFN-SLCS",
        # "urn:geant:kit.edu:group:LSDF-DIS",
        # "urn:geant:kit.edu:group:bwGrid",
        # "urn:geant:kit.edu:group:bwLSDF-FS",
        # "urn:geant:kit.edu:group:bwUniCluster",
        # "urn:geant:kit.edu:group:bwsyncnshare",
        # "urn:geant:kit.edu:group:bwsyncnshare-idm",
        # "urn:geant:kit.edu:group:gruppenverwalter"
        #





    def test_failure_incomplete_but_valid_entitlement_1(self):
        required_group= 'urn:geant:h-df.de:group:aai-admin:role=admin'
        req_entitlement        = Aarc_g002_entitlement(required_group, strict=False)

    def test_failure_incomplete_but_valid_entitlement_2(self):
        required_group= 'urn:geant:h-df.de:group:aai-admin'
        req_entitlement        = Aarc_g002_entitlement(required_group, strict=False)

    # def test_failure_incomplete_invalid_entitlement(self):
    #     required_group= 'urn:geant:h-df.de'
    #     req_entitlement        = Aarc_g002_entitlement(required_group)

if __name__ == '__main__':
    unittest.main()
