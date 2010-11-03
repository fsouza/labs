import unittest
import mocker
import labs
from nose.tools import assert_true, assert_equals
from lxml import html
from labs.models import ProgrammingLanguage, Project

class TestAdminProjects(unittest.TestCase):

    def setUp(self):
        self.mocker = mocker.Mocker()
        self.client = labs.app.test_client()

        self.language = ProgrammingLanguage(name = u'Python')
        self.language.put()

        self.project = Project(name = u'Testing everything', github_url = u'http://github.com/franciscosouza/test', description = 'Bla bla bla', language = self.language)
        self.project.put()

    def _mock_logged_in(self, times = 1):
        logged_in = self.mocker.replace('google.appengine.api.users.is_current_user_admin')
        logged_in()
        self.mocker.result(True)
        self.mocker.count(times)
        self.mocker.replay()

    def test_list_projects(self):
        "Should list all projects in /admin/projects"
        self._mock_logged_in()
        response = self.client.get('/admin/projects')
        assert_true('Projects list' in response.data)

    def test_project_form(self):
        "Should show a form for new projects"
        self._mock_logged_in()
        response = self.client.get('/admin/projects/new')
        assert_true('<h2>New project</h2>' in response.data)

    def test_create_a_project(self):
        "Should create a project with given data by post"
        self._mock_logged_in(times = 2)
        expected_name = u'The project'
        from labs.util import slugify
        expected_slug = slugify(expected_name)
        data = {
            'name' : expected_name,
            'language' : self.language.key(),
            'description' : 'Bla bla bla'
        }
        response = self.client.post('/admin/projects', data = data, follow_redirects = True)
        from labs.models import Project
        project = Project.all().filter('slug = ', expected_slug).get()
        assert_equals(project.name, expected_name)

    def test_create_a_duplicated_name_project(self):
        "Should generate a new slug to a duplicated project"
        self._mock_logged_in(times = 4)
        expected_name = u'The project'
        from labs.util import slugify
        expected_slug = slugify(expected_name) + '-1'
        data = {
            'name' : expected_name,
            'language' : self.language.key(),
            'description' : 'Bla bla bla'
        }
        response = self.client.post('/admin/projects', data = data, follow_redirects = True)
        response = self.client.post('/admin/projects', data = data, follow_redirects = True)
        from labs.models import Project
        project = Project.all().filter('slug = ', expected_slug).get()
        assert_equals(project.name, expected_name)

    def test_validate_creating_a_project(self):
        "Should validate the new project form"
        self._mock_logged_in(times = 2)
        response = self.client.post('/admin/projects', data = {}, follow_redirects = True)
        assert_true('This field is required' in response.data)

    def test_form_edit_project(self):
        "Should show a form with the project data on /admin/projects/<slug>/edit"
        self._mock_logged_in()
        response = self.client.get('/admin/projects/%s/edit' % self.project.slug)
        dom = html.fromstring(response.data)
        name_field = dom.xpath('//input[@type="text" and @name="name"]')[0]
        github_field = dom.xpath('//input[@type="text" and @name="github_url"]')[0]
        docs_field = dom.xpath('//input[@type="text" and @name="documentation_url"]')[0]
        language_select = dom.xpath('//select[@name="language"]')[0]
        selected_language = language_select.xpath('//option[@selected="selected"]')[0]
        assert_equals(name_field.value, self.project.name)
        assert_equals(github_field.value, self.project.github_url)
        assert_equals(docs_field.value, '')
        assert_equals(selected_language.text, self.project.language.name)

    def test_update_a_project(self):
        "Should update a project with given data by post"
        self._mock_logged_in(times = 2)
        project = Project(name = u'The big project', description='Bla bla bla', language = self.language)
        project.put()
        slug = project.slug
        github_url = 'http://github.com/franciscosouza/labs'
        data = {
            'name' : project.name,
            'language' : project.language.key(),
            'description' : 'Bla bla bla',
            'github_url' : github_url
        }
        self.client.post('/admin/projects/%s' % slug, data = data, follow_redirects = True)
        project = Project.all().filter('slug =', slug).get()
        assert_equals(project.github_url, github_url)

    def test_failing_update(self):
        "Should not update if the data was not provided"
        self._mock_logged_in(times = 2)
        response = self.client.post('/admin/projects/%s' % self.project.slug, data = {}, follow_redirects = True)
        assert_true('This field is required' in response.data)

    def test_delete_a_project(self):
        "Should delete a project on URL /projects/<slug>/delete"
        self._mock_logged_in()
        from labs.models import Project
        project = Project(name = u'Ruby on Rails', description = 'Bla bla bla', language = self.language)
        project.put()
        project_slug = project.slug
        url = '/admin/projects/%s/delete' %(project_slug)
        response = self.client.get(url)
        project = Project.all().filter('slug = ', project_slug).get()
        assert_true(project is None)

    def tearDown(self):
        self.mocker.restore()
        self.language.delete()

        from labs.models import Project
        from google.appengine.ext import db
        projects = Project.all().fetch(1000)
        db.delete(projects)
