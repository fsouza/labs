from flask import Module, render_template
from labs.models import Project

frontend = Module(__name__)

@frontend.route('/')
def index():
    return render_template('frontend/index.html')

@frontend.route('/<language_slug>/<project_slug>')
def show_project(language_slug, project_slug):
    project = Project.all().filter('slug = ', project_slug).get()
    return render_template('frontend/projects/show.html', project=project)
