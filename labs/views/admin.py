from flask import Module, render_template
from labs.decorators import admin_login_required

admin = Module(__name__)

@admin.route('/')
@admin_login_required
def index():
    return render_template('admin/index.html')
