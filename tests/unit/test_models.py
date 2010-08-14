import unittest
import mocker
from labs.models import Project, ProgrammingLanguage
from nose.tools import assert_equals

class TestModels(unittest.TestCase):

    def setUp(self):
        self.mocker = mocker.Mocker()
        self.language = ProgrammingLanguage(name = u'Python')
        self.language.put()

    def test_save_project_with_slug(self):
        "Before put a project, should generate a slug"
        project = Project(name = u'My Project', language = self.language)
        project.put()
        assert_equals(project.slug, u'my-project')

    def test_save_language_with_slug(self):
        "Before put a language, should generate a slug"
        assert_equals(self.language.slug, u'python')

    def tearDown(self):
        self.mocker.restore()
