import unittest
import mocker
import labs
from nose.tools import assert_true

class TestFrontend(unittest.TestCase):

    def setUp(self):
        self.mocker = mocker.Mocker()
        self.client = labs.app.test_client()

    def test_frontend_index(self):
        "Should has an index for the frontend with a welcome message"
        response = self.client.get('/')
        assert_true('<h2>Welcome to Labs</h2>' in response.data)

    def tearDown(self):
        self.mocker.restore()
