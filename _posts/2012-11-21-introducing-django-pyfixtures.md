---
layout: post
title: Introducing Django Pyfixtures
tags: django fixtures
---

[Django fixtures](https://docs.djangoproject.com/en/dev/howto/initial-data/) were initially touted as a great way to pre-populate your database, mainly for testing. Over time, various community leaders have suggested that fixtures are [slow](http://pyvideo.org/video/699/testing-and-django), [brittle](http://lincolnloop.com/blog/2012/may/3/fixtures-and-factories/), should be [bundled](http://nedbatchelder.com/blog/201206/tldw_speedily_practical_largescale_tests.html) instead of loaded from scratch for every unit test and should probably be replaced with class [factories](https://github.com/dnerdy/factory_boy).

If you're starting from scratch, that's great advice. But how do you get there if you already have a bunch of fixtures? Starting today, you can use [django-pyfixtures](https://github.com/chase-seibert/django-pyfixtures) to convert your json fixtures to python code.

> Using the regular Django dumpdata command, pyfixtures will generate a python file that contains all the code necessary to re-constitute that data in an empty database. You can take that code and refactor it into something you maintain going forward, or you can re-generate it from a target database when needed.

# How it works

Pyfixtures implements a new Django serializer that takes a model object stream and produces python constructors for that code. It ends up looking just as it would if you wrote the code by hand, complete with necessary imports, declaring models that other models depend on first, and using previously declared variables for foreign keys. It can also deal with circular references by letting the user decide which models to use primary keys for, instead of references.

Here is an example of what a fixture might look like.

{% highlight python %}
import datetime
import pytz
from models import Organization
from models import Group
from models import Contact


organization1 = Organization(
    id=1,
    create_date=datetime.datetime(2011, 1, 15, 44, 0, tzinfo=pytz.timezone('UTC')),
    name=u'Marvel Comics')

group1 = Group(
    id=1,
    create_date=datetime.datetime(2011, 5, 17, 1, 59, 14, tzinfo=pytz.timezone('UTC')),
    name=u'The Avengers',
    organization=organization1)

contact1 = Contact(
    id=1,
    group=group1,
    name=u'Captain America',
    organization=organization1,
    create_date=datetime.datetime(2010, 6, 17, 1, 48, 32, tzinfo=pytz.timezone('UTC')))

contact2 = Contact(
    id=2,
    group=group1,
    name=u'Iron Man',
    organization=organization1,
    create_date=datetime.datetime(2010, 6, 17, 1, 48, 32, tzinfo=pytz.timezone('UTC')))
{% endhighlight %}

# Getting Started

- `pip install django-pyfixtures`
- Edit `settings.py`

{% highlight python %}
INSTALLED_APPS = (
    ...
    'pyfixtures',
    )
...
SERIALIZATION_MODULES = {'py': 'pyfixtures.serializer'}
{% endhighlight %}

- Convert your existing fixtures to python, and test them

{% highlight bash %}
./manage.py loaddata fixtures/initial_data.json
./manage.py dumpdata --exclude contenttypes --format=py > fixtures/initial_data.py
./manage.py loaddata fixtures/initial_data.py
{% endhighlight %}
