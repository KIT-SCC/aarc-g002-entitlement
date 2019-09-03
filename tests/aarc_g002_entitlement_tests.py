# pylint: disable=bad-whitespace, invalid-name, missing-docstring
import unittest
from aarc_g002_entitlement.aarc_g002_entitlement import Aarc_g002_entitlement as Aarc_g002_ePE

class Aarc_g002(unittest.TestCase):
    def test_equality(self):
        required_group = 'urn:geant:h-df.de:group:aai-admin:role = member#unity.helmholtz-data-federation.de'
        actual_group   = 'urn:geant:h-df.de:group:aai-admin:role = member#unity.helmholtz-data-federation.de'
        req_ePE        = Aarc_g002_ePE(required_group)
        act_ePE        = Aarc_g002_ePE(actual_group)
        self.assertEqual(req_ePE.is_contained_in(act_ePE), True)
        self.assertEqual(act_ePE == req_ePE, True)

    def test_simple(self):
        required_group= 'urn:geant:h-df.de:group:aai-admin:role=member#unity.helmholtz-data-federation.de'
        actual_group  = 'urn:geant:h-df.de:group:aai-admin:role=member#backupserver.used.for.developmt.de'
        req_ePE        = Aarc_g002_ePE(required_group)
        act_ePE        = Aarc_g002_ePE(actual_group)
        self.assertEqual(req_ePE.is_contained_in(act_ePE), True)
        # self.assertEqual(aarc_g002_matcher.aarc_g002_matcher(required_group, actual_group), True)

    def test_role_not_required(self):
        required_group= 'urn:geant:h-df.de:group:aai-admin#unity.helmholtz-data-federation.de'
        actual_group  = 'urn:geant:h-df.de:group:aai-admin:role=member#backupserver.used.for.developmt.de'
        req_ePE        = Aarc_g002_ePE(required_group)
        act_ePE        = Aarc_g002_ePE(actual_group)
        self.assertEqual(req_ePE.is_contained_in(act_ePE), True)
        # self.assertEqual(aarc_g002_matcher.aarc_g002_matcher(required_group, actual_group), True)

    def test_role_required(self):
        required_group= 'urn:geant:h-df.de:group:aai-admin:role=member#unity.helmholtz-data-federation.de'
        actual_group  = 'urn:geant:h-df.de:group:aai-admin#backupserver.used.for.developmt.de'
        req_ePE        = Aarc_g002_ePE(required_group)
        act_ePE        = Aarc_g002_ePE(actual_group)
        self.assertEqual(req_ePE.is_contained_in(act_ePE), False)
        # self.assertEqual(aarc_g002_matcher.aarc_g002_matcher(required_group, actual_group), False)

    def test_subgroup_required(self):
        required_group= 'urn:geant:h-df.de:group:aai-admin:special-admins#unity.helmholtz-data-federation.de'
        actual_group  = 'urn:geant:h-df.de:group:aai-admin#backupserver.used.for.developmt.de'
        req_ePE        = Aarc_g002_ePE(required_group)
        act_ePE        = Aarc_g002_ePE(actual_group)
        self.assertEqual(req_ePE.is_contained_in(act_ePE), False)
        # self.assertEqual(aarc_g002_matcher.aarc_g002_matcher(required_group, actual_group), False)

    def test_user_in_subgroup(self):
        required_group= 'urn:geant:h-df.de:group:aai-admin#unity.helmholtz-data-federation.de'
        actual_group  = 'urn:geant:h-df.de:group:aai-admin:special-admins#backupserver.used.for.developmt.de'
        req_ePE        = Aarc_g002_ePE(required_group)
        act_ePE        = Aarc_g002_ePE(actual_group)
        self.assertEqual(req_ePE.is_contained_in(act_ePE), True)
        # self.assertEqual(aarc_g002_matcher.aarc_g002_matcher(required_group, actual_group), True)

    def test_role_required_for_supergroup(self):
        required_group= 'urn:geant:h-df.de:group:aai-admin:role=admin#unity.helmholtz-data-federation.de'
        actual_group  = 'urn:geant:h-df.de:group:aai-admin:special-admins:role=admin#backupserver.used.for.developmt.de'
        req_ePE        = Aarc_g002_ePE(required_group)
        act_ePE        = Aarc_g002_ePE(actual_group)
        self.assertEqual(req_ePE.is_contained_in(act_ePE), False)
        # self.assertEqual(aarc_g002_matcher.aarc_g002_matcher(required_group, actual_group), False)
    # def test_(self):
    #     required_group = ''
    #     actual_group   = ''
    #     req_ePE        = Aarc_g002_ePE(required_group)
    #     act_ePE        = Aarc_g002_ePE(actual_group)
    #     self.assertEqual(act_ePE.is_contained_in(act_ePE), True)

if __name__ == '__main__':
    unittest.main()
