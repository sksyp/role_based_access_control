import itertools


class Registry(object):
    """The registry of access control list."""

    def __init__(self):
        self._roles = {}
        self._resources = {}
        self._allowed = {}
        self._denied = {}

    def add_role(self, role, parents=None):
        """Add a role or append parents roles to a special role.
        """
        if parents is None:
            parents = []
        self._roles.setdefault(role, set())
        self._roles[role].update(parents)

    def add_resource(self, resource, parents=None):
        """Add a resource or append parents resources to a special resource.
        """
        if parents is None:
            parents = []
        self._resources.setdefault(resource, set())
        self._resources[resource].update(parents)

    def allow(self, role, operation, resource, assertion=None):
        assert not role or role in self._roles
        assert not resource or resource in self._resources
        self._allowed[role, operation, resource] = assertion

    def deny(self, role, operation, resource, assertion=None):
        assert not role or role in self._roles
        assert not resource or resource in self._resources
        self._denied[role, operation, resource] = assertion

    def is_allowed(self, role, operation, resource):
        """Check the permission.
        """
        assert not role or role in self._roles
        assert not resource or resource in self._resources

        roles = set(get_family(self._roles, role))
        operations = {None, operation}
        resources = set(get_family(self._resources, resource))

        is_allowed = None
        default_assertion = lambda *args: True

        for permission in itertools.product(roles, operations, resources):
            if permission in self._denied:
                assertion = self._denied[permission] or default_assertion
                if assertion(self, role, operation, resource):
                    return False  # denied by rule immediately

            if permission in self._allowed:
                assertion = self._allowed[permission] or default_assertion
                if assertion(self, role, operation, resource):
                    is_allowed = True  # allowed by rule

        return is_allowed

    def is_any_allowed(self, roles, operation, resource):
        """Check the permission with many roles."""
        is_allowed = None  # there is no matching rules
        for role in roles:
            is_current_allowed = self.is_allowed(role, operation, resource)
            if is_current_allowed is False:
                return False  # denied by rule
            elif is_current_allowed is True:
                is_allowed = True
        return is_allowed

    def get_resources(self):
        return self._resources


def get_family(all_parents, current):
    """Iterate current object and its all parents recursively."""
    yield current
    for parent in get_parents(all_parents, current):
        yield parent
    yield None


def get_parents(all_parents, current):
    """Iterate current object's all parents."""
    for parent in all_parents.get(current, []):
        yield parent
        for grandparent in get_parents(all_parents, parent):
            yield grandparent
