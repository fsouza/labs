from flask import Module, render_template
from labs.models import Project
from labs.forms import ProjectForm

admin = Module(__name__)

@admin.route('/')
def index():
    return render_template('admin/index.html')

@admin.route('/projects')
def list_projects():
    projects = Project.all().order('name')
    return render_template('admin/projects/list.html', projects=projects)

@admin.route('/projects/new', methods=['GET'])
def new_project():
    form = ProjectForm()
    return render_template('admin/projects/new.html', form=form)

@admin.route('/projects', methods=['POST'])
def create_project():
    return 'Hello'
