from nose.tools import assert_equals

def test_inject_logout_url():
    "Should inject the logout URL"
    from labs.context_processors import inject_logout_url
    from google.appengine.api.users import create_logout_url

    assert_equals(inject_logout_url(), { 'create_logout_url' : create_logout_url })
