from flaskext import wtf
from flaskext.wtf import validators

class ProjectForm(wtf.Form):
    name = wtf.TextField(u'Name', validators=[validators.Required()])
    programming_language = wtf.SelectField(u'Programming language', validators=[validators.Required()])
    github_url = wtf.TextField(u'Github URL')
    documentation_url = wtf.TextField(u'Documentation URL')

    def set_programming_languages_options(self, languages):
        """Set the programming languages options"""
        self.programming_language.options = [(l.slug, l.name) for l in languages]

class LanguageForm(wtf.Form):
    name = wtf.TextField(u'Name', validators=[validators.Required()])
