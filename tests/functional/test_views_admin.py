import unittest
import mocker
import labs

class TestAdmin(unittest.TestCase):

    def setUp(self):
        self.mocker = mocker.Mocker()
        self.client = labs.app.test_client()

    def _mock_logged_in(self, times = 1):
        logged_in = self.mocker.replace('google.appengine.api.users.is_current_user_admin')
        logged_in()
        self.mocker.result(True)
        self.mocker.count(times)
        self.mocker.replay()

    def test_home_admin(self):
        "Should render the admin home on /admin URL"
        self._mock_logged_in()
        response = self.client.get('/admin/')
        assert '<h2>Welcome</h2>' in response.data

    def tearDown(self):
        self.mocker.restore()

