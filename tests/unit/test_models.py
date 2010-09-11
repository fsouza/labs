#coding: utf-8
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
        project = Project(name = u'My Project', language = self.language, description='Bla bla bla')
        project.put()
        assert_equals(project.slug, u'my-project')

    def test_get_project_url(self):
        "The project should contain a URL in the format: /<language-slug>/<project-slug> using url_for for building"
        project = Project(name = u'Comunicação avançada', language = self.language, description='Bla bla bla')
        project.put()
        url = '/%s/%s' %(project.language.slug, project.slug)

        url_for_mocked = self.mocker.replace('flask.url_for')
        url_for_mocked(mocker.ANY, language_slug = self.language.slug, project_slug = project.slug)
        self.mocker.result(url)
        self.mocker.replay()

        assert_equals(project.get_url(), url)

    def test_save_language_with_slug(self):
        "Before put a language, should generate a slug"
        assert_equals(self.language.slug, u'python')

    def tearDown(self):
        self.language.delete()
        self.mocker.restore()
