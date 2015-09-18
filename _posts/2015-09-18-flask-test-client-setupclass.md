---
layout: post
title: Optimizing Flask client tests
tags: python flask
---

When writing Python integration tests, it's useful to put slow code such as database access in a 
[setUpClass](https://docs.python.org/2/library/unittest.html#setupclass-and-teardownclass) method, 
so that they are only executed once for the entire `unittest.TestCase`. Recently, when writing
integration tests for a Flask API, I wanted to make an API call once for the `TestCase`, but have
many tests that assert on various parts of the JSON response. This was a little awkward because 
the Flask [test client](http://flask.pocoo.org/docs/0.10/testing/) was only being instantiated with 
an instance of `TestCase`.

I ended up caching API responses in a global variable in my custom base `TestCase` subclass.

```python
from functools import partial
from unittest import TestCase


_cached_api_responses = {}


class MyTestCase(TestCase):

    def set_cached_json_data(self, cache_key, test_callable):
        """ We want to separate out tests for various keys in the json response 
            of an API call, but we only want to make an API once for performance
            reasons. Solution is to cache this between test calls, which is made
            more difficult due to test classes being re-instantiated between
            individual tests. Cache in a global. """
        global _cached_api_responses
        response_json = _cached_api_responses.get(cache_key)
        if not response_json:
            response = test_callable()
            response_json = response.json
            _cached_api_responses[cache_key] = response_json
        return response_json
        
        
class SpecificTestCase(MyTestCase):

    @classmethod
    def setUpClass(cls):
        # do a bunch of database record creation
        cls.db_object = ...
        
    def setUp(self):
        # cache a flask API response 
        test_callable = partial(self.get, '/my-url')
        self.response_json = self.set_cached_json_data('my-url', test_callable)
    
    def test_foo(self):
        foo = self.response_json['foo']
        self.assertEquals(len(foo), 1)
            
    def test_bar(self):
        bar = self.response_json['foo']['bar']
        self.assertEquals(len(bar), 10)
```

The use of partial is just to make it easier to pass any test client call into the caching function.

The fact that it's caching JSON and not a collection of SQLAlchemy database objects is important,
if you tried that, you would find that SQLAlchemy would throw exceptions about the objects no longer
being tied to a session in your tests. 
