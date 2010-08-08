import re
from unicodedata import normalize

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))

def generate_slug_field(model, field, slug_field_name = 'slug'):
    slug = slugify(field)
    new_slug = slug
    counter = 1
    query = '%s =' % slug_field_name

    while model.all().filter(query, new_slug).count() > 0:
        new_slug = '%s-%d' %(slug, counter)
        counter += 1

    return new_slug
