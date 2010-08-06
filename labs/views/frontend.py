from flask import Module

frontend = Module(__name__)

@frontend.route('/')
def index():
    return 'Welcome to the Home'
