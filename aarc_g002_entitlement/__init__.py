'''
Check entitlements according to the AARC G002 recommendation

https://aarc-project.eu/guidelines/aarc-g002
'''
# This code is distributed under the MIT License
# pylint
# vim: tw=100 foldmethod=indent
# pylint: disable=invalid-name, superfluous-parens, logging-too-many-args

import logging
import regex
# python2 / python3 compatible way to get access to urlencode and decode
try:
    from urllib.parse import unquote, quote_plus
except ImportError:
    from urllib import unquote, quote_plus


logger = logging.getLogger(__name__)

NAMESPACE_REGEX = (
    r'urn'
    r':(?P<nid>[^:]+)'                                 # Namespace-ID
    r':(?P<delegated_namespace>[^:]+)'                 # Delegated URN namespace
    r'(:(?P<subnamespace>[^:]+))*?'                    # Sub-namespaces
)
G002_GROUP_SUBGROUP_ROLE_REGEX = (
    r':group:'
    r'(?P<group>[^:#]+)'                               # Root group
    r'(:(?P<subgroup>[^:#]+))*?'                       # Sub-groups
    r'(:role=(?P<role>[^#]+))?'                        # Role of the user in the deepest group
)
G002_STRICT_AUTH_REGEX = (
    r'#(?P<group_authority>.+)'                        # Authoritative source of the entitlement
)
G002_LAX_AUTH_REGEX = (
    r'(#(?P<group_authority>.+))?'                     # Authoritative source of the entitlement
)

# These regexes are not compatible with stdlib 're', we need 'regex'!
# (because of repeated captures, see https://bugs.python.org/issue7132)
ENTITLEMENT_REGEX = {
    'strict': regex.compile(
        r'^'
        + NAMESPACE_REGEX
        + G002_GROUP_SUBGROUP_ROLE_REGEX
        + G002_STRICT_AUTH_REGEX
        + r'$'
    ),
    'lax': regex.compile(
        r'^'
        + NAMESPACE_REGEX
        + G002_GROUP_SUBGROUP_ROLE_REGEX
        + G002_LAX_AUTH_REGEX
        + r'$'
    ),
}


class Aarc_g002_entitlement_Error(Exception):
    """A generic error for this module"""


class Aarc_g002_entitlement_ParseError(Aarc_g002_entitlement_Error):
    """Error during parsing an entitlement"""


class Aarc_g002_entitlement:
    """
    Parse and compare EduPerson Entitlements

    Reference specification: https://aarc-project.eu/guidelines/aarc-g002

    Class instances can be tested for equality and less-than-or-equality.
    The py:meth:is_contained_in can be used to checks if a user with an entitlement `U`
    is permitted to use a resource which requires a certain entitlement `R`, like so:

        `R`.is_contained_in(`U`)

    :param str raw: The entitlement to parse. If the entitlement is '%xx' encoded it is decoded
    before parsing.

    :param strict: `False` to ignore a missing group_authority and `True` otherwise, defaults
    to `True`.
    :type strict: bool, optional

    :raises Aarc_g002_entitlement_ParseError:
        If the raw entitlement is not following the AARC-G002 recommendation
        and cannnot be parsed.

    :raises Aarc_g002_entitlement_Error:
        If the attributes extracted from the entitlement could not be assigned to this instance.

    Available attributes for AARC-G002 entitlements are listed here.
    For entitlements not following the recommendation, these are set to their default values.
    """
    # pylint: disable=too-many-instance-attributes
    #:
    namespace_id = ''
    #:
    delegated_namespace = ''
    #: List of subnamespaces. May be empty.
    subnamespaces = []
    #:
    group = ''
    #: List of subgroups. May be empty
    subgroups = []
    #: None if the entitlement has no role.
    role = None
    #: None if the entitlement has no group_authority.
    group_authority = None

    def __init__(self, raw, strict=True, **kwargs):
        """Parse a raw EduPerson entitlement string in the AARC-G002 format."""

        if "raise_error_if_unparseable" in kwargs:
            msg = "raise_error_if_unparseable is deprecated; it is now always True."
            logger.warning(msg)

        self._raw = unquote(raw)
        logger.debug('Processing entitlement: %s', self._raw)

        match = ENTITLEMENT_REGEX['strict' if strict else 'lax'].fullmatch(self._raw)
        if match is None:
            msg = 'Entitlement does not conform to AARC-G002 specification (strict=%s): %s' % (
                strict, self._raw
            )
            raise Aarc_g002_entitlement_ParseError(msg)

        capturesdict = match.capturesdict()
        logger.debug('Extracting entitlement attributes: %s', capturesdict)
        try:
            [self.namespace_id] = capturesdict.get('nid')
            [self.delegated_namespace] = capturesdict.get('delegated_namespace')
            self.subnamespaces = capturesdict.get('subnamespace')
            [self.group] = capturesdict.get('group')
            self.subgroups = capturesdict.get('subgroup')
            [self.role] = capturesdict.get('role') or [None]
            [self.group_authority] = capturesdict.get('group_authority') or [None]
        except ValueError as e:
            logger.error('On assigning the captured attributes: %s', e)
            raise Aarc_g002_entitlement_Error('Error extracting captured attributes') from e

    def __repr__(self):
        """Serialize the entitlement to the AARC-G002 format.

        This is the inverse to `__init__` and thus `ent_str == repr(Aarc_g002_entitlement(ent_str))`
        holds for any valid entitlement.
        """

        repr_str = (
            # NAMESPACE part
            'urn:{namespace_id}:{delegated_namespace}{subnamespaces}'
            # G002 part
            ':group:{group}{subgroups}{role}{group_authority}'
        ).format(
            # NAMESPACE part
            namespace_id=self.namespace_id,
            delegated_namespace=self.delegated_namespace,
            subnamespaces=''.join([':{}'.format(ns) for ns in self.subnamespaces]),
            # G002 part
            group=self.group,
            subgroups=''.join([':{}'.format(grp) for grp in self.subgroups]),
            role=':role={}'.format(self.role) if self.role else '',
            group_authority='#{}'.format(self.group_authority) if self.group_authority else '',
        )
        return repr_str

    def __str__(self):
        """Return the entitlement in human-readable string form."""

        str_str = ' '.join(
            [
                '<Aarc_g002_entitlement',
                'namespace={namespace_id}:{delegated_namespace}{subnamespaces}',
                'group={group}{subgroups}{role} auth={group_authority}>',
            ]
        ).format(
            namespace_id=self.namespace_id,
            delegated_namespace = self.delegated_namespace,
            subnamespaces = ''.join([',{}'.format(ns) for ns in self.subnamespaces]),
            group = self.group,
            subgroups = ''.join([',{}'.format(grp) for grp in self.subgroups]),
            role = 'role={}'.format(self.role) if self.role else '',
            group_authority = self.group_authority,
        )
        return str_str

    def __mstr__(self):
        """Return the nicely formatted entitlement"""
        str_str = '\n'.join(
            [
                'namespace_id:        {namespace_id}' +
                '\ndelegated_namespace: {delegated_namespace}' +
                '\nsubnamespaces:       {subnamespaces}' +
                '\ngroup:               {group}' +
                '\nsubgroups:           {subgroups}' +
                '\nrole_in_subgroup     {role}' +
                '\ngroup_authority:     {group_authority}'
            ]
            ).format(
                namespace_id = self.namespace_id,
                delegated_namespace = self.delegated_namespace,
                group = self.group,
                group_authority = self.group_authority,
                subnamespaces = ','.join(['{}'.format(ns) for ns in self.subnamespaces]),
                subgroups = ','.join(['{}'.format(grp) for grp in self.subgroups]),
                role ='{}'.format(self.role) if self.role else 'n/a'
            )
        return str_str

    def __hash__(self):
        keys = (
            self.namespace_id,
            self.delegated_namespace,
            tuple(self.subnamespaces),
            self.group,
            tuple(self.subgroups),
            self.role,
        )
        hash_id = hash(keys)
        return hash_id

    def __eq__(self, other):
        """
        Check if other object is equal.
        """

        is_equal = hash(self) == hash(other)
        return is_equal

    def __le__(self, other):
        """
        Check if self is contained in other.

        Please, use "is_contained_in", see below.
        """

        try:
            self_subgroup_for_role = self.subgroups[-1]
        except IndexError:
            self_subgroup_for_role = None

        try:
            other_subgroup_for_role = other.subgroups[-1]
        except IndexError:
            other_subgroup_for_role = None

        other_subns_len = len(other.subnamespaces)
        other_subgroups_len = len(other.subgroups)
        is_le = (
            self.namespace_id == other.namespace_id
            and self.delegated_namespace == other.delegated_namespace
            and all(
                other_subns_len > idx and subns == other.subnamespaces[idx]
                for idx, subns in enumerate(self.subnamespaces)
            )
            and self.group == other.group
            and all(
                other_subgroups_len > idx and subgroup == other.subgroups[idx]
                for idx, subgroup in enumerate(self.subgroups)
            )
            and (
                self.role == other.role
                and self_subgroup_for_role == other_subgroup_for_role
                if self.role
                else True
            )
        )

        return is_le

    def is_contained_in(self, other):
        """ Check if self is contained in other """
        return (self <= other)
