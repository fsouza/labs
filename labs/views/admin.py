from flask import Module, render_template
from labs.decorators import admin_login_required
from labs.models import Project
from labs.forms import ProjectForm

admin = Module(__name__)

@admin.route('/')
@admin_login_required
def index():
    return render_template('admin/index.html')

@admin.route('/projects')
@admin_login_required
def list_projects():
    projects = Project.all().order('name')
    return render_template('admin/projects/list.html', projects=projects)

@admin.route('/projects/new', methods=['GET'])
@admin_login_required
def new_project():
    form = ProjectForm()
    return render_template('admin/projects/new.html', form=form)
