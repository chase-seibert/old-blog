---
layout: post
title: Django Nose Lint Quickstart - Enforce fast unit tests
tags: django testing
---

In the battle for blazing fast unit tests, you need all the tools you can get at your disposal. Enter [django-nose-lint](https://github.com/chase-seibert/django-nose-lint), a new [Nose](https://nose.readthedocs.org/en/latest/) plugin that lets you enforce certain runtime constraints on your test suite. You can just flat out fail tests that take over a configurable amount of time. You can also get more granular and fail tests that try to do certain slow stuff. For example, using the [Django test client](https://docs.djangoproject.com/en/dev/topics/testing/#module-django.test.client).

Here are the things it can currently check for:

- ESOK = Used a TCP socket
- ECLI = Used the Django Test Client
- ETEM = Tried to render a Django template
- ESLO = Test took over 1 second (takes --maxms argument)
- EALL = All of the above

## Quickstart for exsting Django projects already using django-nose

If you're already running `django-nose` on your Django app, all you need to do is install `django-nose-lint`, and run your tests with the `--lint` flag.

{% highlight bash %}
pip install django-nose-lint
./manage.py test --lint=EALL
{% endhighlight %}

## Starting from scratch on a new Django project

This is mostly an re-hash of the [django-nose setup docs](https://github.com/jbalogh/django-nose#readme). I assume you have [virtualenv](http://pypi.python.org/pypi/virtualenv) installed, and want to use it to isolate this skunkworks from your existing python stuff.

First, setup a new Django project inside `virtualenv`.

{% highlight bash %}
mkdir django-nose-lint-test
cd django-nose-lint-test/
virtualenv --no-site-packages --distribute virtualenv
source virtualenv/bin/activate
pip install django nose django-nose django-nose-lint
django-admin.py startproject mysite
cd mysite/
{% endhighlight %}

Then, edit your Django `settings.py` file to do basic setup, and attach `django-nose`.

{% highlight python %}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '',
    }
}

INSTALLED_APPS = (
    ...
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
{% endhighlight %}

Create a basic test that we want to fail. Create this as `mysite/tests.py`. It should be along-side `urls.py` in the directory structure.

{% highlight python %}
import unittest
import time


class MyTest(unittest.TestCase):

    def test_one(self):
        time.sleep(1.1)
        self.assertTrue(True)
{% endhighlight %}

Run your test suite.

{% highlight bash %}
>python manage.py test --lint=EALL
Creating test database for alias 'default'...
.E
======================================================================
ERROR: test_one (tests.MyTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/cseibert/projects/django-nose-lint-test/virtualenv/lib/python2.7/site-packages/nose/case.py", line 133, in run
    self.runTest(result)
  File "/Users/cseibert/projects/django-nose-lint-test/virtualenv/lib/python2.7/site-packages/nose/case.py", line 151, in runTest
    test(result)
  File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/unittest/case.py", line 376, in __call__
    return self.run(*args, **kwds)
  File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/unittest/case.py", line 355, in run
    result.stopTest(self)
  File "/Users/cseibert/projects/django-nose-lint-test/virtualenv/lib/python2.7/site-packages/nose/proxy.py", line 180, in stopTest
    self.plugins.stopTest(self.test)
  File "/Users/cseibert/projects/django-nose-lint-test/virtualenv/lib/python2.7/site-packages/nose/plugins/manager.py", line 99, in __call__
    return self.call(*arg, **kw)
  File "/Users/cseibert/projects/django-nose-lint-test/virtualenv/lib/python2.7/site-packages/nose/plugins/manager.py", line 167, in simple
    result = meth(*arg, **kw)
  File "/Users/cseibert/projects/django-nose-lint-test/virtualenv/lib/python2.7/site-packages/noselint/__init__.py", line 76, in stopTest
    raise DeprecationWarning('DjangoNoseLint Error: ESLO - test took %s ms' % delta_ms)
DeprecationWarning: DjangoNoseLint Error: ESLO - test took 1101 ms

----------------------------------------------------------------------
Ran 1 test in 1.104s

FAILED (errors=1)
{% endhighlight %}

If you run without the `--lint` flag, the same test should pass.

## Call for ideas

I'm looking for some more ideas of things to fail in unit tests. Please [submit a bug](https://github.com/chase-seibert/django-nose-lint/issues) to the tracker if you have any ideas.


