import pytest

from src.classes.Registry import Registry


@pytest.fixture(params=[
    lambda: Registry()], ids=['registry'])
def registry(request):
    register = request.param()

    register.add_role('user')
    register.add_role('active_user', parents=['user'])
    register.add_role('editor', parents=['writer', 'manager'])
    register.add_role('super')

    # add resources
    register.add_resource('comment')
    register.add_resource('post')
    register.add_resource('news', parents=['post'])

    # set super permission
    register.allow('super', None, None)

    return register


def test_allow(register):
    # add allowed rules
    register.allow('active_user', 'view', 'news')

    # test 'view' operation
    roles = ['active_user']

    for role in roles:
        for resource in ['news']:
            assert register.is_allowed(role, 'view', resource)
        for resource in ['post']:
            assert not register.is_allowed(role, 'view', resource)

    for resource in ['news']:
        assert register.is_any_allowed(roles, 'view', resource)
    for resource in ['post']:
        assert not register.is_any_allowed(roles, 'view', resource)

    for resource in ['post', 'news']:
        assert not register.is_allowed('user', 'view', resource)
        assert register.is_allowed('super', 'view', resource)
        assert register.is_allowed('super', 'new', resource)
        assert register.is_any_allowed(['user', 'super'], 'view', resource)


def test_deny(register):
    # add allowed rule and denied rule
    register.allow('active_user', 'new', 'comment')
    register.deny('manager', 'new', 'comment')

    # test allowed rules
    roles = ['active_user']

    for role in roles:
        assert register.is_allowed(role, 'new', 'comment')

    assert register.is_any_allowed(roles, 'new', 'comment')

    # test denied rules
    roles = ['manager']

    for role in roles:
        assert not register.is_allowed(role, 'new', 'comment')

    assert not register.is_any_allowed(roles, 'new', 'comment')


def test_undefined(register):
    # test denied undefined rule
    roles = ['user', 'active_user', 'manager']

    for resource in ['comment', 'post', 'news']:
        for role in roles:
            assert not register.is_allowed(role, 'x', resource)
            assert not register.is_allowed(role, '', resource)
            assert not register.is_allowed(role, None, resource)
        assert not register.is_any_allowed(roles, 'x', resource)
        assert not register.is_any_allowed(roles, '', resource)
        assert not register.is_any_allowed(roles, None, resource)

    # test `None` defined rule
    for resource in ['comment', 'post', 'news', 'event', None]:
        for op in ['undefined', 'x', '', None]:
            assert register.is_allowed('super', op, resource)