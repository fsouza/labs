from flask import Module, render_template

admin = Module(__name__)

@admin.route('/')
def index():
    return render_template('admin/index.html')

import languages
import projects
