import unittest
import mocker

class TestAdmin(unittest.TestCase):

    def setUp(self):
        self.mocker = mocker.Mocker()

    def tearDown(self):
        self.mocker.restore()
