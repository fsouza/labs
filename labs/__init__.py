from flask import Flask
from labs.views.admin import admin

app = Flask('labs')
app.register_module(admin, url_prefix = '/admin')
