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
