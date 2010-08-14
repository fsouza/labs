from flask import render_template, flash, redirect, url_for
from labs.models import Project, ProgrammingLanguage
from labs.forms import ProjectForm
from labs.views.admin import admin

@admin.route('/projects')
def list_projects():
    projects = Project.all().order('name')
    return render_template('admin/projects/list.html', projects=projects)

@admin.route('/projects/new')
def new_project():
    languages = ProgrammingLanguage.all()
    form = ProjectForm()
    form.set_programming_languages_choices(languages)
    return render_template('admin/projects/new.html', form=form)

@admin.route('/projects', methods=['POST'])
def create_project():
    form = ProjectForm()
    languages = ProgrammingLanguage.all()
    form.set_programming_languages_choices(languages)
    if form.validate_on_submit():
        language = ProgrammingLanguage.all().filter('slug =', form.programming_language.data).get()
        project = Project(name = form.name.data,
                          github_url = form.github_url.data,
                          documentation_url = form.documentation_url.data,
                          language = language
                  )
        project.put()
        flash('Project saved on the database')
        return redirect(url_for('list_projects'))
    return render_template('admin/projects/new.html', form=form)

@admin.route('/projects/<slug>/delete')
def delete_project(slug):
    project = Project.all().filter('slug =', slug).get()
    project.delete()
    flash('Project successful deleted')
    return redirect(url_for('list_projects'))
