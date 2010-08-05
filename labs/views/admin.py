from flask import Module
from labs.decorators import admin_login_required

admin = Module(__name__)

@admin.route('/')
@admin_login_required
def index():
    pass
