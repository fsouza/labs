def setup():
    from labs import app
    app.config['TESTING'] = True
    app.config['CSRF_ENABLED'] = False
