import sys
import os

root_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(root_dir, 'lib')
sys.path.append(lib_dir)

from google.appengine.ext.webapp.util import run_wsgi_app
from labs import app

run_wsgi_app(app)
