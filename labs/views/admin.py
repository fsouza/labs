from flask import Module, render_template, flash, redirect, url_for
from labs.models import Project, ProgrammingLanguage
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
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(name = form.name.data,
                          github_url = form.github_url.data,
                          documentation_url = form.documentation_url.data
                  )
        project.put()
        flash('Project saved on the database')
        return redirect(url_for('list_projects'))
    return render_template('admin/projects/new.html', form=form)

@admin.route('/languages')
def list_languages():
    languages = ProgrammingLanguage.all().order('name')
    return render_template('admin/languages/list.html', languages=languages)
