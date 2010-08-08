from google.appengine.ext import db
from labs.util import generate_slug_field

class ProgrammingLanguage(db.Model):
    name = db.StringProperty(required=True)
    slug = db.StringProperty()

    def put(self):
        if not self.slug:
            self.slug = generate_slug_field(ProgrammingLanguage, self.name)

        return super(ProgrammingLanguage, self).put()

class Project(db.Model):
    name = db.StringProperty(required=True)
    slug = db.StringProperty()
    github_url = db.StringProperty()
    documentation_url = db.StringProperty()
    language = db.ReferenceProperty(ProgrammingLanguage, required=True)

    def put(self):
        if not self.slug:
            self.slug = generate_slug_field(Project, self.name)

        return super(Project, self).put()

class Page(db.Model):
    title = db.StringProperty(required=True)
    slug = db.StringProperty()
    content = db.TextProperty(required=True)
    project = db.ReferenceProperty(Project)

class Link(db.Model):
    title = db.StringProperty(required=True)
    href = db.StringProperty(required=True)
    project = db.ReferenceProperty(Project)
