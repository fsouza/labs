from flaskext import wtf
from flaskext.wtf import validators

class ProjectForm(wtf.Form):
    name = wtf.TextField(u'Name', validators=[validators.Required()])
    programming_language = wtf.SelectField(u'Programming language', validators=[validators.Required()])
    github_url = wtf.TextField(u'Github URL')
    documentation_url = wtf.TextField(u'Documentation URL')

    def set_programming_languages_choices(self, languages):
        """Set the programming languages options"""
        self.programming_language.choices = [(l.slug, l.name) for l in languages]
        self.programming_language.choices.insert(0, ('', 'Select the language'))

    def set_selected_programming_language(self, language):
        """Set the selected programming language at the select box"""
        self.programming_language.data = language.slug

class LanguageForm(wtf.Form):
    name = wtf.TextField(u'Name', validators=[validators.Required()])
