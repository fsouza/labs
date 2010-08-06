from flask import Flask
from labs.views.admin import admin
from labs.views.frontend import frontend

import settings

app = Flask('labs')
app.config.from_object('labs.settings')
app.register_module(admin, url_prefix = '/admin')
app.register_module(frontend)
import context_processors
