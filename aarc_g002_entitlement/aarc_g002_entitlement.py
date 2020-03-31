'''Check entitlements according to the AARC G002 recommendation
   https://aarc-project.eu/guidelines/aarc-g002'''
# This code is distributed under the MIT License
# pylint
# vim: tw=100 foldmethod=indent
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace

import logging
import regex
# python2 / python3 compatible way to get access to urlencode and decode
try:
    from urllib.parse import unquote, quote_plus
except ImportError:
    from urllib import unquote, quote_plus

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
        r'(:role=(?P<role>[^#]+))?' +                         # Role of the user in the deepest group
        r'(#(?P<group_authority>.+))?'                            # Authoritative source of the entitlement (URN)
    )
}

class Aarc_g002_entitlement :
    """EduPerson Entitlement attribute (de-)serialisation.

    As specified in: https://aarc-project.eu/guidelines/aarc-g002/
    """

    def __init__(self, raw, strict=True):
        """Parse a raw EduPerson entitlement string in the AARC-G002 format."""

        raw_dec = unquote(raw)
        match = ENTITLEMENT_REGEX['strict' if strict else 'lax'].fullmatch(raw_dec)

        if match is None:
            logger.info('Input did not match (strict=%s): %s', strict, raw_dec)

            msg = 'Input does not seem to be an AARC-G002 Entitlement'

            if strict:
                raise ValueError(msg)
            raise ValueError(msg + ' (Omitting the group authority was permitted)')


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
            logger.error('On assigning the captured attributes: %s', e)
            raise Exception('Error extracting captured attributes: %s', e)

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

    def __le__(self, other):
        """ Check if self is contained in other.
        Please use "is_contained_in", see below"""
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
            if self.role != other.role:
                return False

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

        return True

    def is_contained_in(self, other):
        """ Check if self is contained in other """
        return (self <= other)

# TODO: Add more Weird combinations of these with roles
