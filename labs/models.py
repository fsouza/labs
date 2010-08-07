from google.appengine.ext import db
from labs.util import slugify

class Project(db.Model):
    name = db.StringProperty(required=True)
    slug = db.StringProperty()
    github_url = db.StringProperty()
    documentation_url = db.StringProperty()

    def put(self):
        if not self.slug:
            slug = slugify(self.name)
            new_slug = slug
            counter = 1

            while Project.all().filter('slug = ', new_slug).count() > 0:
                new_slug = '%s-%d' %(slug, counter)
                counter += 1

            self.slug = new_slug

        return super(Project, self).put();

class Page(db.Model):
    title = db.StringProperty(required=True)
    slug = db.StringProperty()
    content = db.TextProperty(required=True)
    project = db.ReferenceProperty(Project)

class Link(db.Model):
    title = db.StringProperty(required=True)
    href = db.StringProperty(required=True)
    project = db.ReferenceProperty(Project)
