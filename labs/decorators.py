from google.appengine.api import users
from flask import redirect, url_for

class admin_login_required(object):

    def __init__(self, function):
        self._function = function
        self.__name__ = function.__name__

    def __call__(self, *args, **kwargs):
        if users.is_current_user_admin():
            return self._function(*args, **kwargs)
        else:
            self._url = url_for(self.__name__, _external = True, **kwargs)
            return redirect(users.create_login_url(self._url))
