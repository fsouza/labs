from flask import redirect, request
from google.appengine.api import users
from labs import app

@app.before_request
def check_url_admin():
    if request.url.find('/admin/') > -1:
        if not users.is_current_user_admin():
            return redirect(users.create_login_url(request.url))

