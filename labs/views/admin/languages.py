from flask import render_template, flash, redirect, url_for
from labs.models import ProgrammingLanguage
from labs.forms import LanguageForm
from labs.views.admin import admin

@admin.route('/languages')
def list_languages():
    languages = ProgrammingLanguage.all().order('name')
    return render_template('admin/languages/list.html', languages=languages)

@admin.route('/languages/new')
def new_language():
    form = LanguageForm()
    return render_template('admin/languages/new.html', form=form)

@admin.route('/languages', methods=['POST'])
def create_language():
    form = LanguageForm()
    if form.validate_on_submit():
        language = ProgrammingLanguage(name = form.name.data)
        language.put()
        flash('Programming language "%s" saved on the database.' % language.name)
        return redirect(url_for('list_languages'))
    return render_template('admin/languages/new.html', form=form)

@admin.route('/languages/<slug>/edit', methods=['GET'])
def edit_language(slug):
    language = ProgrammingLanguage.all().filter('slug = ', slug).get()
    form = LanguageForm()
    form.name.data = language.name
    return render_template('admin/languages/edit.html', form=form, language=language)

@admin.route('/languages/<slug>', methods=['POST'])
def update_language(slug):
    form = LanguageForm()
    if form.validate_on_submit():
        language = ProgrammingLanguage.all().filter('slug =', slug).get()
        language.name = form.name.data
        language.put()
        flash('Programming language "%s" updated.' %language.name)
        return redirect(url_for('list_languages'))
    return render_template('admin/languages/edit.html', form=form, language=language)

@admin.route('/languages/<slug>/delete', method=['GET'])
def delete_language(slug):
    language = ProgrammingLanguage.all().filter('slug = ', slug).get()
    language.delete()
    flash('Language successful deleted.')
    return redirect(url_for('list_languages'))
