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

# These regexes are not compatible with stdlib 're', we need 'regex'!
# (because of repeated captures, see https://bugs.python.org/issue7132)
ENTITLEMENT_REGEX = {
    'strict': regex.compile(
        # NAMESPACE REGEX
        r'urn:'
        r'(?P<nid>[^:]+)'                                  # Namespace-ID
        r':(?P<delegated_namespace>[^:]+)'                 # Delegated URN namespace
        r'(:(?P<subnamespace>[^:]+))*?'                    # Sub-namespaces
        # G002 REGEX
        r':group:'
        r'(?P<group>[^:]+)'                                # Root group
        r'(:(?P<subgroup>[^:]+))*?'                        # Sub-groups
        r'(:role=(?P<role>.+))?'                           # Role of the user in the deepest group
        r'#(?P<group_authority>.+)'                        # Authoritative source of the entitlement
    ),
    'lax': regex.compile(
        # NAMESPACE REGEX
        r'urn:'
        r'(?P<nid>[^:]+)'                                  # Namespace-ID
        r':(?P<delegated_namespace>[^:]+)'                 # Delegated URN namespace
        r'(:(?P<subnamespace>[^:]+))*?'                    # Sub-namespaces
        # G002 REGEX
        r':group:'
        r'(?P<group>[^:#]+)'                               # Root group
        r'(:(?P<subgroup>[^:#]+))*?'                       # Sub-groups
        r'(:role=(?P<role>[^#]+))?'                        # Role of the user in the deepest group
        r'(#(?P<group_authority>.+))?'                     # Authoritative source of the entitlement
    ),
}

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

    :param raise_error_if_unparseable: `True` to raise a ValueError, if the entitlements does
    not follow the AARC-G002 recommendation and `False` to create the (largely empty) entitlement
    object, defaults to `False`.
    :type raise_error_if_unparseable: bool, optional

    :raises ValueError:
        If raw does not contain a group_authority and strict is `True`,
        or if the raw entitlement is not following the AARC-G002 recommendation at all and
        `raise_error_if_unparseable is `True`.

    :raises Exception: If the attributes extracted from the entitlement could not be assigned
    to this instance.

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

    def __init__(self, raw, strict=True, raise_error_if_unparseable=False):
        """Parse a raw EduPerson entitlement string in the AARC-G002 format."""

        self._raw = unquote(raw)
        logger.debug('Processing entitlement: %s', self._raw)

        match = ENTITLEMENT_REGEX['strict' if strict else 'lax'].fullmatch(self._raw)
        if match is None:
            msg = 'Entitlement does not conform to AARC-G002 specification (strict=%s): %s' % (
                strict, self._raw
            )
            logger.info(msg)

            if raise_error_if_unparseable:
                logger.error(msg)
                raise ValueError(msg)

            return

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
            raise Exception('Error extracting captured attributes') from e

    def __repr__(self):
        """Serialize the entitlement to the AARC-G002 format.

        This is the inverse to `__init__` and thus `ent_str == repr(Aarc_g002_entitlement(ent_str))`
        holds for any valid entitlement.
        """

        # handle non-g002
        if not self.is_aarc_g002:
            return self._raw

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

        # handle non-g002
        if not self.is_aarc_g002:
            return self._raw

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

    def __eq__(self, other):
        """ Check if other object is equal """

        # handle non-g002
        if not self.is_aarc_g002:
            if not other.is_aarc_g002:
                return self._raw == other._raw
            return False

        is_equal = (
            self.namespace_id == other.namespace_id
            and self.delegated_namespace == other.delegated_namespace
            and all(
                subnamespace in other.subnamespaces
                for subnamespace in self.subnamespaces
            )
            and self.group == other.group
            and self.subgroups == other.subgroups
            and self.role == other.role
        )

        return is_equal

    def __le__(self, other):
        # pylint: disable=too-many-return-statements, too-many-branches
        """ Check if self is contained in other.
        Please use "is_contained_in", see below"""

        # handle non-g002
        if not self.is_aarc_g002:
            if not other.is_aarc_g002:
                return self._raw == other._raw
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

        if other.subgroups:
            logger.debug("Checking subgroups")

            for subgroup in self.subgroups:
                logger.debug(F"is {other.subgroups} in {subgroup}  ??")
                if subgroup not in other.subgroups:
                    logger.debug("    => No")
                    return False
                logger.debug("    => Yes")

        if self.role is not None:
            logger.debug ("Checking role")
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

    @property
    def is_aarc_g002(self):
        """ Check if this entitlements follows the AARC-G002 recommendation
        Note this only works with raise_error_if_unparseable=False

        :return: True if the recommendation is followed
        :rtype: bool
        """
        return self.group != ''

# TODO: Add more Weird combinations of these with roles
