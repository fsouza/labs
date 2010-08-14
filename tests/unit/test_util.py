#coding:utf-8
from nose.tools import assert_equals

def test_slugify_english():
    "Should slugify an english phrase"
    from labs.util import slugify
    assert_equals(slugify(u'My name is Francisco.'), u'my-name-is-francisco')

def test_slugify_portuguese():
    "Should slugify a portuguese name"
    from labs.util import slugify
    assert_equals(slugify(u'Francisco Antônio da Silva Souza.'), u'francisco-antonio-da-silva-souza')

def test_slug_generation_for_model():
    "Should generate a slug for a model"
    from labs.models import Project
    from labs.util import generate_slug_field
    assert_equals(generate_slug_field(Project, u'Undefined project'), u'undefined-project')

def test_slug_generation_for_model_repeated():
    "Should generate a slug with counter for a model when the slug already exists"
    language_name = u'Ruby'
    expected_slug = u'ruby-1'
    from labs.models import ProgrammingLanguage
    from labs.util import generate_slug_field
    language = ProgrammingLanguage(name = language_name)
    language.put()
    assert_equals(generate_slug_field(ProgrammingLanguage, language_name), expected_slug)
