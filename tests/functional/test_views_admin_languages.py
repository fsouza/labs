import unittest
import mocker
import labs
from nose.tools import assert_true, assert_equals
from labs.models import ProgrammingLanguage

class TestAdminLanguages(unittest.TestCase):

    def setUp(self):
        self.mocker = mocker.Mocker()
        self.client = labs.app.test_client()
        self.language = ProgrammingLanguage(name = u'Java')
        self.language.put()

    def _mock_logged_in(self, times = 1):
        logged_in = self.mocker.replace('google.appengine.api.users.is_current_user_admin')
        logged_in()
        self.mocker.result(True)
        self.mocker.count(times)
        self.mocker.replay()

    def test_list_languages(self):
        "Should list all languages in /admin/languages"
        self._mock_logged_in()
        response = self.client.get('/admin/languages')
        assert_true('Languages list' in response.data)

    def test_show_the_languages_form(self):
        "Should show a form for language in /admin/languages/new"
        self._mock_logged_in()
        response = self.client.get('/admin/languages/new')
        assert_true('Fill the form' in response.data)

    def test_create_language_with_right_data(self):
        "Should create a language given data by post"
        from labs.util import slugify
        language_name = u'Haskell'
        language_slug = slugify(language_name)
        self._mock_logged_in(times = 2) # Two times because follow_redirects on post will be true :)
        data = { 'name' : language_name }
        response = self.client.post('/admin/languages', data = data, follow_redirects = True)
        from labs.models import ProgrammingLanguage
        language = ProgrammingLanguage.all().filter('slug =', language_slug).get()
        assert_equals(language.name, language_name)

    def test_fail_creating_language(self):
        "Should not create a language without the name"
        self._mock_logged_in(times = 2)
        response = self.client.post('/admin/languages', data = {}, follow_redirects = True)
        assert_true('This field is required' in response.data)

    def test_form_edit_language(self):
        "Should shows a form to edit the language on /admin/languages/<slug>/edit"
        self._mock_logged_in()
        response = self.client.get('/admin/languages/%s/edit' % self.language.slug)
        from lxml import html
        dom = html.fromstring(response.data)
        field = dom.xpath('//input[@type="text" and @name="name"]')[0]
        assert_equals(field.value, self.language.name)

    def test_update_language(self):
        "Should update a language with data given by post"
        self._mock_logged_in(times = 2)
        data = { 'name' : u'Javascript' }
        response = self.client.post('/admin/languages/%s' % self.language.slug, data = data, follow_redirects = True)
        language = ProgrammingLanguage.all().filter('slug =', self.language.slug).get()
        assert_equals(language.name, 'Javascript')

    def test_fail_update_language(self):
        "Should not update a language if the name is not provided"
        self._mock_logged_in(times = 2)
        response = self.client.post('/admin/languages/%s' % self.language.slug, data = {}, follow_redirects = True)
        assert_true('This field is required' in response.data)

    def test_delete_a_language(self):
        "Should delete a language on URL /admin/languages/<slug>/delete"
        self._mock_logged_in()
        language = ProgrammingLanguage(name = u'C++')
        language.put()
        slug = language.slug
        self.client.get('/admin/languages/%s/delete' % slug)
        language = ProgrammingLanguage.all().filter('slug = ', slug).get()
        assert_equals(language, None)

    def tearDown(self):
        self.mocker.restore()
        self.language.delete()
