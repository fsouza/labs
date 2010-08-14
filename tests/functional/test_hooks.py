import unittest
import labs
import mocker
from nose.tools import assert_equals

class TestHooks(unittest.TestCase):

    def setUp(self):
        self.mocker = mocker.Mocker()
        self.app = labs.app.test_client()

    def test_not_logged_redirect(self):
        "When not logged in, should be redirected"
        r = self.app.get('/admin/projects')
        assert_equals(r.status_code, 302)

    def tearDown(self):
        self.mocker.restore()
