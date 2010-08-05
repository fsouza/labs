from google.appengine.ext import db

class Project(db.Model):
    name = db.StringProperty(required=True)
    slug = db.StringProperty()
    github_url = db.StringProperty()
    documentation_url = db.StringProperty()

class Page(db.Model):
    title = db.StringProperty(required=True)
    slug = db.StringProperty()
    content = db.TextProperty(required=True)
    project = db.ReferenceProperty(Project)

class Link(db.Model):
    title = db.StringProperty(required=True)
    href = db.StringProperty(required=True)
    project = db.ReferenceProperty(Project)
