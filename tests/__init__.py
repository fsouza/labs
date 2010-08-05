import sys
import os

app_path = os.path.dirname(os.path.abspath(__file__)).replace('/tests', '')
lib_path = os.path.join(app_path, 'lib')

def setup():
    sys.path.insert(0, app_path)
    sys.path.insert(0, lib_path)
    from labs import app
    app.config['TESTING'] = True

def teardown():
    sys.path.remove(app_path)
    sys.path.remove(lib_path)
