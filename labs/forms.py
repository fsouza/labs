from flaskext import wtf
from flaskext.wtf import validators

class ProjectForm(wtf.Form):
    name = wtf.TextField('Name', validators=[validators.Required()])
    github_url = wtf.TextField('Github URL')
    documentation_url = wtf.TextField('Documentation URL')
