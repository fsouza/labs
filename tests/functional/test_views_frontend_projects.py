import unittest
import mocker
import labs
from labs.models import ProgrammingLanguage, Project
from nose.tools import assert_true, assert_equals
from lxml import html

class TestFrontendProjects(unittest.TestCase):

    def setUp(self):
        self.mocker = mocker.Mocker()
        self.client = labs.app.test_client()

        self.language = ProgrammingLanguage(name = u'Python')
        self.language.put()

        self.project = Project(name = u'Labs', language = self.language, github_url = 'http://github.com/franciscosouza/talks')
        self.project.put()

        self.project_url = '/%s/%s' %(self.language.slug, self.project.slug)

    def test_show_a_project(self):
        "Should show a project in the URL /<language-slug>/<project-slug>"
        title = '<h2>%s</h2>' % self.project.name
        response = self.client.get(self.project_url)
        assert_true(title in response.data)

    def test_link_github(self):
        "Should link Github repository when it is present when viewing a project (/<language-slug>/<project-slug>)"
        response = self.client.get(self.project_url)
        dom = html.fromstring(response.data)
        path = '//a[@href="%s"]' % self.project.github_url
        link_list = dom.xpath(path)
        assert_equals(len(link_list), 1)

    def tearDown(self):
        self.mocker.restore()
        self.project.delete()
        self.language.delete()
