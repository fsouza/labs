from flaskext import wtf
from flaskext.wtf import validators
from labs.models import ProgrammingLanguage, Project

class ProjectForm(wtf.Form):
    name = wtf.TextField(u'Name', validators=[validators.Required()])
    programming_language = wtf.SelectField(u'Programming language', validators=[validators.Required()])
    github_url = wtf.TextField(u'Github URL')
    documentation_url = wtf.TextField(u'Documentation URL')

    def __init__(self, programming_language_choices, model_instance = None, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.model = None
        self.set_programming_languages_choices(programming_language_choices)
        if model_instance:
            self.name.data = model_instance.name
            self.programming_language.data = model_instance.language.slug
            self.github_url.data = model_instance.github_url
            self.documentation_url.data = model_instance.documentation_url
            self.model = model_instance

    def save(self):
        language = ProgrammingLanguage.all().filter('slug =', self.programming_language.data).get()
        if self.model:
            self.model.name = self.name.data
            self.model.github_url = self.github_url.data
            self.model.documentation_url = self.documentation_url.data
            self.model.language = language
        else:
            self.model = Project(
                            name = self.name.data,
                            github_url = self.github_url.data,
                            documentation_url = self.documentation_url.data,
                            language = language
                        )
        self.model.put()
        return self.model

    def set_programming_languages_choices(self, languages):
        """Set the programming languages options"""
        self.programming_language.choices = [(l.slug, l.name) for l in languages]
        self.programming_language.choices.insert(0, ('', 'Select the language'))

class LanguageForm(wtf.Form):
    name = wtf.TextField(u'Name', validators=[validators.Required()])
