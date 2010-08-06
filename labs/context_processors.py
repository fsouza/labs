from google.appengine.api import users
from labs import app

@app.context_processor
def inject_logout_url():
    return { 'create_logout_url' : users.create_logout_url }
