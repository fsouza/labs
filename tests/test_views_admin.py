import unittest
import mocker
import labs

class TestAdmin(unittest.TestCase):

    def setUp(self):
        self.mocker = mocker.Mocker()
        self.app = labs.app.test_client()

    def tearDown(self):
        self.mocker.restore()
