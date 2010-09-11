from flaskext import wtf
from labs.models import ProgrammingLanguage, Project
from wtforms.ext.appengine.db import model_form

BaseProjectForm = model_form(Project, base_class = wtf.Form, exclude = ['slug'])

class ProjectForm(BaseProjectForm):
    def __init__(self, model_instance = None, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.model = None
        self.language.label_attr = 'name'
        self.language.query.order('name')
        if model_instance:
            self.name.data = model_instance.name
            self.language.data = str(model_instance.language.key())
            self.github_url.data = model_instance.github_url
            self.documentation_url.data = model_instance.documentation_url
            self.model = model_instance

    def save(self):
        language = ProgrammingLanguage.get(self.language.data)
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

LanguageForm = model_form(ProgrammingLanguage, base_class = wtf.Form, exclude = ['slug'])
