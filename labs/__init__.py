from flask import Flask
from labs.views.admin import admin
from labs.views.frontend import frontend

app = Flask('labs')
app.register_module(admin, url_prefix = '/admin')
app.register_module(frontend)
import context_processors
