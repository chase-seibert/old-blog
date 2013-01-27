---
layout: post
title: Mocking HTTP calls in Python tests
tags: python
---

There are at least a few decent libraries out there for mocking out HTTP calls in Python unit tests. The best solution looks like [HTTPretty](https://github.com/gabrielfalcao/HTTPretty). One feature that it does not have, however, is the ability to [specify url parameters](https://github.com/gabrielfalcao/HTTPretty/issues/25). For many applications, such as testing OAuth flows, a lot of the behavior you are trying to validate involves parameters being passed. At the same time, you don't want to be forced to specify _all_ the parameters. For example, the `oauth_timestamp` changes for every REST call; it's dynamic based on the system clock.

Here is a quick class that can mock `urllib2` requests, and lets you specify some parameters that you want to validate are being passed. Any parametes that you don't specify are allowed.

{% highlight python %}
import urllib2
from StringIO import StringIO
import json
import httplib
import urlparse
import urllib


class MockHTTPHandler(urllib2.HTTPSHandler):

    def __init__(self):
        self.requests = {}
        self.responses = {}
        self.calls_made = []

    @staticmethod
    def hash_args(args):
        ''' takes an args dict and makes a hashable key, normalizing order '''
        return urllib.urlencode(args)

    def mock(self, url, validate_args={}, status_code=200, *args, **kwargs):
        data = kwargs.get('data')
        if data is None:
            fixture = kwargs.get('fixture')
            if fixture:
                data = open(fixture).read()
        if data is None:
            json_data = kwargs.get('json_data')
            if json_data is not None:
                data = json.dumps(json_data)
        if data is None:
            raise ValueError('must pass either data or fixture argument')
        if url not in self.responses:
            self.responses[url] = {}
        self.responses[url][MockHTTPHandler.hash_args(validate_args)] = (status_code, data)

    def https_open(self, req):
        return self.http_open(req)

    def http_open(self, req):
        url_with_args = req.get_full_url()
        parsed = urlparse.urlparse(url_with_args)
        url = url_with_args.replace('?' + parsed.query, '')
        actual_args = urlparse.parse_qs(parsed.query)
        if url in self.responses:
            for args_qs, (status_code, data) in self.responses.get(url).items():
                # check if this request matches all the args in a registered call
                expected_args = urlparse.parse_qs(args_qs)
                if not all(item in actual_args.items() for item in expected_args.items()):
                    continue
                resp = urllib2.addinfourl(StringIO(data), {}, req.get_full_url())
                resp.code = status_code
                resp.msg = httplib.responses.get(status_code, 'OK')
                self.calls_made.append(url + '?' + args_qs)
                return resp
        raise NotImplementedError('need to mock url %s' % req.get_full_url())

    def assert_all_called(self, test):
        calls_expected = []
        for url in self.responses:
            for args_qs in self.responses.get(url):
                calls_expected.append(url + '?' + args_qs)
        test.assertEquals(set(calls_expected), set(self.calls_made))


    @staticmethod
    def patch():
        opener = urllib2.build_opener(MockHTTPHandler)
        urllib2.install_opener(opener)
        return [h for h in opener.handlers if isinstance(h, MockHTTPHandler)][0]

    @staticmethod
    def unpatch():
        urllib2._opener = None

{% endhighlight %}

You can enable this mock in your unit tests as follows. Note the call to `unpatch()` to remove the mock. Without this, other tests in your test suite may fail if they try to make a HTTP call.

{% highlight python %}
import unittest


class TwitterOAuthCallsTest(unittest.TestCase):
    def setUp(self):
        self.requests = MockHTTPHandler.patch()

    def tearDown(self):
        MockHTTPHandler.unpatch()

    def test_http_request(self):

        # you can specify json results directly
        self.requests.mock('https://api.twitter.com/1/friends/ids.json', {
            'screen_name': 'foobar',
            'oauth_token': 'BAR',
            'oauth_consumer_key': 'dsafsdfdsfsdf'},
            json_data={
                "ids": [
                    38596298,
                    30516966,
                    14399709,
                ],
                "next_cursor": 0,
                "next_cursor_str": "0",
                "previous_cursor": 0,
                "previous_cursor_str": "0"
            })

        # you can also specify json via an external file
        self.requests.mock('https://api.twitter.com/1/users/lookup.json', {
            'user_id': '38596298,30516966,14399709'},
            fixture='twitter/fixtures/lookup.json')

        # INVOKE THE TWITTER CODE HERE

        # test that all the urls you registered were called
        self.requests.assert_all_called(self)
{% endhighlight %}
