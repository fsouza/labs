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
    form = ProjectForm(languages)
    return render_template('admin/projects/new.html', form=form)

@admin.route('/projects', methods=['POST'])
def create_project():
    languages = ProgrammingLanguage.all()
    form = ProjectForm(languages)
    if form.validate_on_submit():
        form.save()
        flash('Project saved on the database')
        return redirect(url_for('list_projects'))
    return render_template('admin/projects/new.html', form=form)

@admin.route('/projects/<slug>/edit')
def edit_project(slug):
    project = Project.all().filter('slug =', slug).get()
    languages = ProgrammingLanguage.all()
    form = ProjectForm(languages, project)
    return render_template('admin/projects/edit.html', form=form, project=project)

@admin.route('/projects/<slug>', methods=['POST'])
def update_project(slug):
    project = Project.all().filter('slug =', slug).get()
    languages = ProgrammingLanguage.all()
    form = ProjectForm(languages)
    if form.validate_on_submit():
        form.model = project
        form.save()
        flash('Project updated')
        return redirect(url_for('list_projects'))
    return render_template('admin/projects/edit.html', form=form, project=project)

@admin.route('/projects/<slug>/delete')
def delete_project(slug):
    project = Project.all().filter('slug =', slug).get()
    project.delete()
    flash('Project successful deleted')
    return redirect(url_for('list_projects'))
