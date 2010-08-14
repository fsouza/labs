import unittest
import labs
import mocker
from nose.tools import assert_equals, assert_true

class TestHooks(unittest.TestCase):

    def setUp(self):
        self.mocker = mocker.Mocker()
        self.app = labs.app.test_client()

    def _mock_current_admin(self, expected_result):
        current_admin_mocked = self.mocker.replace('google.appengine.api.users.is_current_user_admin')
        current_admin_mocked()
        self.mocker.result(expected_result)

    def test_not_logged_redirect(self):
        "When not logged in, should be redirected"
        self._mock_current_admin(False)

        login_url_mocked = self.mocker.replace('google.appengine.api.users.create_login_url')
        login_url_mocked(mocker.ANY)
        self.mocker.result('http://www.google.com.br')

        self.mocker.replay()

        r = self.app.get('/admin/projects')
        assert_equals(r.status_code, 302)

        self.mocker.verify()

    def tearDown(self):
        self.mocker.restore()
