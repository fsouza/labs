import unittest
import mocker
from nose.tools import assert_equals

class TestDecorators(unittest.TestCase):

    def setUp(self):
        self.mocker = mocker.Mocker()

    def not_logged_mock(self):
        kwargs = dict()

        google_user = self.mocker.replace('google.appengine.api.users.is_current_user_admin')
        google_user()
        self.mocker.result(False)

        url_for_mock = self.mocker.replace('flask.url_for')
        url_for_mock('hello_world', _external = True, **kwargs)
        self.mocker.result('nothing')

        login_url_mock = self.mocker.replace('google.appengine.api.users.create_login_url')
        login_url_mock('nothing')
        self.mocker.result('/')

        redirect_mock = self.mocker.replace('flask.redirect')
        redirect_mock('/')
        self.mocker.result('Finish!')

        self.mocker.replay()

    def logged_mock(self):
        google_user = self.mocker.replace('google.appengine.api.users.is_current_user_admin')
        google_user()
        self.mocker.result(True)

        self.mocker.replay()

    def test_changes_function_when_there_is_no_admin_logged(self):
        "When there is no admin authenticated, the view function should be changed"
        self.not_logged_mock()

        from labs.decorators import admin_login_required
        @admin_login_required
        def hello_world():
            return 'Hello world'

        assert_equals(hello_world(), 'Finish!')

    def test_dont_changes_function_when_there_is_admin_logged(self):
        "When there is admin authenticated, the view function should not be changed"
        self.logged_mock()

        from labs.decorators import admin_login_required
        @admin_login_required
        def hello_world():
            return 'Hello world'

        assert_equals(hello_world(), 'Hello world')

    def tearDown(self):
        self.mocker.restore()
