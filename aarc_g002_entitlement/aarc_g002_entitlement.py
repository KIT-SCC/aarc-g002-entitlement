'''Check entitlements according to the AARC G002 recommendation
   https://aarc-project.eu/guidelines/aarc-g002'''
# This code is distributed under the MIT License
# pylint
# vim: tw=100 foldmethod=indent
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace

import logging
import regex

logger = logging.getLogger(__name__)

# These regexes are not compatible with stdlib 're', we need 'regex'!
# (because of repeated captures, see https://bugs.python.org/issue7132)
ENTITLEMENT_REGEX = {
    'strict':  regex.compile(
        r'urn:' +
        r'(?P<nid>[^:]+):(?P<delegated_namespace>[^:]+)' +     # Namespace-ID and delegated URN namespace
        r'(:(?P<subnamespace>[^:]+))*?' +                      # Sub-namespaces
        r':group:' +
        r'(?P<group>[^:]+)' +                                  # Root group
        r'(:(?P<subgroup>[^:]+))*?' +                          # Sub-groups
        r'(:role=(?P<role>.+))?' +                             # Role of the user in the deepest group
        r'#(?P<group_authority>.+)'                               # Authoritative soruce of the entitlement (URN)
    ),
    'lax': regex.compile(
        r'urn:' +
        r'(?P<nid>[^:]+):(?P<delegated_namespace>[^:]+)' +     # Namespace-ID and delegated URN namespace
        r'(:(?P<subnamespace>[^:]+))*?' +                      # Sub-namespaces
        r':group:' +
        r'(?P<group>[^:#]+)' +                                 # Root group
        r'(:(?P<subgroup>[^:#]+))*?' +                         # Sub-groups
        r'(:role=(?P<role>[^#]+))*?' +                         # Role of the user in the deepest group
        r'(#(?P<group_authority>.+))?'                            # Authoritative soruce of the entitlement (URN)
    )
}

class Failure(ValueError):
    """Indicates a failure to parse an Aarc_g002_entitlement
    """
    def __init__(self, message, **kwargs):
        # logging here logs in the calling scope of Aarc_g002_entitlement
        # Aarc_g002_entitlement should log before raising an exception
        logging.error(message)
        super().__init__(message, **kwargs)

class Aarc_g002_entitlement :
    """EduPerson Entitlement attribute (de-)serialisation.

    As specified in: https://aarc-project.eu/guidelines/aarc-g002/
    """

    def __init__(self, raw, strict=True):
        """Parse a raw EduPerson entitlement string in the AARC-G002 format."""

        match = ENTITLEMENT_REGEX['strict' if strict else 'lax'].fullmatch(raw)

        if match is None:
            logger.warning("Input did not match (strict=%s): %s", strict, raw)

            if strict:
                raise Failure("Input did not match the strict entitlement regex")
            raise Failure("Input did not match the entitlement regex")


        capturesdict = match.capturesdict()
        logger.debug("Extracting entitlement attributes: %s", capturesdict)
        try:
            [self.namespace_id] = capturesdict.get('nid')
            [self.delegated_namespace] = capturesdict.get('delegated_namespace')
            self.subnamespaces = capturesdict.get('subnamespace')

            [self.group] = capturesdict.get('group')
            self.subgroups = capturesdict.get('subgroup')
            [self.role] = capturesdict.get('role') or [None]

            [self.group_authority] = match.captures('group_authority') or [None]
        except ValueError as e:
            raise Failure("Failed to parse entitlements attribute [2/2]") from e

    def __repr__(self):
        """Serialize the entitlement to the AARC-G002 format.

        This is the inverse to `__init__` and thus `ent_str == repr(Aarc_g002_entitlement(ent_str))`
        holds for any valid entitlement.
        """
        return ((
            'urn:{namespace_id}:{delegated_namespace}{subnamespaces}' +
            ':group:{group}{subgroups}{role}' +
            '#{group_authority}'
        ).format(**{
                'namespace_id': self.namespace_id,
                'delegated_namespace': self.delegated_namespace,
                'group': self.group,
                'group_authority': self.group_authority,
                'subnamespaces': ''.join([':{}'.format(ns) for ns in self.subnamespaces]),
                'subgroups': ''.join([':{}'.format(grp) for grp in self.subgroups]),
                'role': ':role={}'.format(self.role) if self.role else ''
        }))

    def __str__(self):
        """Return the entitlement in human-readable string form."""
        return ((
            '<Aarc_g002_entitlement' +
            ' namespace={namespace_id}:{delegated_namespace}{subnamespaces}' +
            ' group={group}{subgroups}' +
            '{role}' +
            ' auth={group_authority}>'
        ).format(**{
                'namespace_id': self.namespace_id,
                'delegated_namespace': self.delegated_namespace,
                'group': self.group,
                'group_authority': self.group_authority,
                'subnamespaces': ''.join([',{}'.format(ns) for ns in self.subnamespaces]),
                'subgroups': ''.join([',{}'.format(grp) for grp in self.subgroups]),
                'role': ' role={}'.format(self.role) if self.role else ''
        }))
    def __mstr__(self):
        return ((
            'namespace_id:        {namespace_id}' +
            '\ndelegated_namespace: {delegated_namespace}' +
            '\nsubnamespaces:       {subnamespaces}' +
            '\ngroup:               {group}' +
            '\nsubgroups:           {subgroups}' +
            '\nrole_in_subgroup     {role}' +
            '\ngroup_authority:     {group_authority}'
        ).format(**{
                'namespace_id': self.namespace_id,
                'delegated_namespace': self.delegated_namespace,
                'group': self.group,
                'group_authority': self.group_authority,
                'subnamespaces': ','.join(['{}'.format(ns) for ns in self.subnamespaces]),
                'subgroups': ','.join(['{}'.format(grp) for grp in self.subgroups]),
                'role':'{}'.format(self.role) if self.role else 'n/a'
        }))

    def __eq__(self, other):
        """ Check if other object is equal """
        if self.namespace_id != other.namespace_id:
            return False

        if self.delegated_namespace != other.delegated_namespace:
            return False

        for subnamespace in self.subnamespaces:
            if subnamespace not in other.subnamespaces:
                return False

        if self.group != other.group:
            return False

        if self.subgroups != other.subgroups:
            return False

        if self.role != other.role:
            return False

        return True

    def __le__(self,other):
        """ Check if self is contained in other.
        Please use "is_contained_in", see below"""
        if not hasattr(self, 'namespace_id'):
            return False
        if not hasattr(other, 'namespace_id'):
            return False

        if self.namespace_id != other.namespace_id:
            return False

        if self.delegated_namespace != other.delegated_namespace:
            return False

        for subnamespace in self.subnamespaces:
            if subnamespace not in other.subnamespaces:
                return False

        if self.group != other.group:
            return False

        for subgroup in self.subgroups:
            if subgroup not in other.subgroups:
                return False

        if self.role is not None:
            try:
                myown_subgroup_for_role = self.subgroups[-1]
            except IndexError:
                myown_subgroup_for_role = None
            try:
                other_subgroup_for_role = other.subgroups[-1]
            except IndexError:
                other_subgroup_for_role = None

            if myown_subgroup_for_role != other_subgroup_for_role:
                return False
            if self.role != other.role:
                return False

        return True

    def is_contained_in(self, other):
        """ Check if self is contained in other """
        return (self <= other)


if __name__ == '__main__':
    required_group= 'urn:geant:h-df.de:group:aai-admin:role=member#unity.helmholtz-data-federation.de'
    actual_group  = 'urn:geant:h-df.de:group:aai-admin:role=member#unity.helmholtz-data-federation.de'
    required_entitlement = Aarc_g002_entitlement(required_group)
    actual_entitlement   = Aarc_g002_entitlement(actual_group)
    print('\n1: Simple case: Different authorities, everything else same')
    print('    Required group: ' + required_group)
    print('    Actual   group: ' + actual_group)
    print('    is_contained_in:   => {}'.format(required_entitlement.is_contained_in(actual_entitlement)))
    print('        (are equal:    => {})'.format(required_entitlement == actual_entitlement))


    required_group= 'urn:geant:h-df.de:group:aai-admin:role=member#unity.helmholtz-data-federation.de'
    actual_group  = 'urn:geant:h-df.de:group:aai-admin:role=member#backupserver.used.for.developmt.de'
    required_entitlement = Aarc_g002_entitlement(required_group)
    actual_entitlement   = Aarc_g002_entitlement(actual_group)

    print('\n2: Simple case: Different authorities, everything else same')
    print('    Required group: ' + required_group)
    print('    Actual   group: ' + actual_group)
    print('    is_contained_in:   => {}'.format(required_entitlement.is_contained_in(actual_entitlement)))
    print('        (are equal:    => {})'.format(required_entitlement == actual_entitlement))


    required_group= 'urn:geant:h-df.de:group:aai-admin#unity.helmholtz-data-federation.de'
    actual_group  = 'urn:geant:h-df.de:group:aai-admin:role=member#backupserver.used.for.developmt.de'
    required_entitlement = Aarc_g002_entitlement(required_group)
    actual_entitlement   = Aarc_g002_entitlement(actual_group)

    print('\n3: Role assigned but not required')
    print('    Required group: ' + required_group)
    print('    Actual   group: ' + actual_group)
    print('    is_contained_in:   => {}'.format(required_entitlement.is_contained_in(actual_entitlement)))
    print('        (are equal:    => {})'.format(required_entitlement == actual_entitlement))


    required_group= 'urn:geant:h-df.de:group:aai-admin:role=member#unity.helmholtz-data-federation.de'
    actual_group  = 'urn:geant:h-df.de:group:aai-admin#backupserver.used.for.developmt.de'
    required_entitlement = Aarc_g002_entitlement(required_group)
    actual_entitlement   = Aarc_g002_entitlement(actual_group)

    print('\n4: Role required but not assigned')
    print('    Required group: ' + required_group)
    print('    Actual   group: ' + actual_group)
    print('    is_contained_in:   => {}'.format(required_entitlement.is_contained_in(actual_entitlement)))
    print('        (are equal:    => {})'.format(required_entitlement == actual_entitlement))


    required_group= 'urn:geant:h-df.de:group:aai-admin:special-admins#unity.helmholtz-data-federation.de'
    actual_group  = 'urn:geant:h-df.de:group:aai-admin#backupserver.used.for.developmt.de'
    required_entitlement = Aarc_g002_entitlement(required_group)
    actual_entitlement   = Aarc_g002_entitlement(actual_group)

    print('\n5: Subgroup required, but not available')
    print('    Required group: ' + required_group)
    print('    Actual   group: ' + actual_group)
    print('    is_contained_in:   => {}'.format(required_entitlement.is_contained_in(actual_entitlement)))
    print('        (are equal:    => {})'.format(required_entitlement == actual_entitlement))

    required_group= 'urn:geant:h-df.de:group:aai-admin#unity.helmholtz-data-federation.de'
    actual_group  = 'urn:geant:h-df.de:group:aai-admin:testgroup:special-admins#backupserver.used.for.developmt.de'
    required_entitlement = Aarc_g002_entitlement(required_group)
    actual_entitlement   = Aarc_g002_entitlement(actual_group)

    print('\n6: Edge case: User in subgroup, but only supergroup required')
    print('    Required group: ' + required_group)
    print('    Actual   group: ' + actual_group)
    print('    is_contained_in:   => {}'.format(required_entitlement.is_contained_in(actual_entitlement)))
    print('        (are equal:    => {})'.format(required_entitlement == actual_entitlement))


    required_group= 'urn:geant:h-df.de:group:aai-admin:role=admin#unity.helmholtz-data-federation.de'
    actual_group  = 'urn:geant:h-df.de:group:aai-admin:special-admins:role=admin#backupserver.used.for.developmt.de'
    required_entitlement = Aarc_g002_entitlement(required_group)
    actual_entitlement   = Aarc_g002_entitlement(actual_group)

    print('\n7: role required for supergroup but only assigned for subgroup')
    print('    Required group: ' + required_group)
    print('    Actual   group: ' + actual_group)
    print('    is_contained_in:   => {}'.format(required_entitlement.is_contained_in(actual_entitlement)))
    print('        (are equal:    => {})'.format(required_entitlement == actual_entitlement))



# TODO: Add more Weird combinations of these with roles
