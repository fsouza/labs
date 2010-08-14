import unittest
import mocker
import labs
from nose.tools import assert_true, assert_equals

class TestAdminProjects(unittest.TestCase):

    def setUp(self):
        self.mocker = mocker.Mocker()
        self.app = labs.app.test_client()

        from labs.models import ProgrammingLanguage
        self.language = ProgrammingLanguage(name = u'Python')
        self.language.put()

    def _mock_logged_in(self, times = 1):
        logged_in = self.mocker.replace('google.appengine.api.users.is_current_user_admin')
        logged_in()
        self.mocker.result(True)
        self.mocker.count(times)
        self.mocker.replay()

    def test_list_projects(self):
        "Should list all projects in /admin/projects"
        self._mock_logged_in()
        response = self.app.get('/admin/projects')
        assert_true('Projects list' in response.data)

    def test_project_form(self):
        "Should show a form for new projects"
        self._mock_logged_in()
        response = self.app.get('/admin/projects/new')
        assert_true('<h2>New project</h2>' in response.data)

    def test_create_a_project(self):
        "Should create a project with given data by post"
        self._mock_logged_in(times = 2)
        expected_name = u'The project'
        from labs.util import slugify
        expected_slug = slugify(expected_name)
        data = {
            'name' : expected_name,
            'programming_language' : self.language.slug,
        }
        response = self.app.post('/admin/projects', data = data, follow_redirects = True)
        from labs.models import Project
        project = Project.all().filter('slug = ', expected_slug).get()
        assert_equals(project.name, expected_name)

    def test_validate_creating_a_project(self):
        "Should validate the new project form"
        self._mock_logged_in(times = 2)
        response = self.app.post('/admin/projects', data = {}, follow_redirects = True)
        assert_true('This field is required' in response.data)

    def test_delete_a_project(self):
        "Should delete a project on URL /projects/<slug>/delete"
        self._mock_logged_in()
        from labs.models import Project
        project = Project(name = u'Ruby on Rails', language = self.language)
        project.put()
        project_slug = project.slug
        url = '/admin/projects/%s/delete' %(project_slug)
        response = self.app.get(url)
        project = Project.all().filter('slug = ', project_slug).get()
        assert_true(project is None)

    def tearDown(self):
        self.mocker.restore()
        self.language.delete()

        from labs.models import Project
        from google.appengine.ext import db
        projects = Project.all().fetch(1000)
        db.delete(projects)
