---
layout: post
title: Loading classes from modules with reflection in Python (imp module)
tags: python
---

For a dynamic language, it's more difficult than it needs to be to import a module dynamically in Python. It's very easy to just `from foo import bar`, but what if you want to load a list of things and all you have is a string representation of each one, for example `foo.bar`?

One use case for this is for configuration. Django uses this pattern to initialize apps via its `INSTALLED_APPS` setting. For example, the default settings looks like this:

{% highlight python %}
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polls',
)
{% endhighlight %}

At some point, Django does the equivalent of a `from django.contrib import admin` and then starts poking around for `urls` and `models` modules. I'm guessing this is done primarily to avoid circular import issues; if Django imports your apps as normal, but your apps turn around and import Django, then you've got a problem.

I wanted to reproduce this pattern myself, and it was a little harder than I expected. Python provides an [imp](https://docs.python.org/2/library/imp.html) for just this occasion. But, from the docs:

>>> This function does not handle hierarchical module names (names containing dots). In order to find P.M, that is, submodule M of package P, use find_module() and load_module() to find and load package P, and then use find_module() with the path argument set to P.__path__. When P itself has a dotted name, apply this recipe recursively.

So, it's basically is a pain the balls to deal with. Here is a working example:

{% highlight python %}
import imp


THINGS_TO_IMPORT = (
    'utils.misc.MyClass1',   # class
    'utils.misc.foo',  # constant
    'utils.bar',  # from __init__.py
    'utils.misc',  # module
)


def import_from_dotted_path(dotted_names, path=None):
    """ import_from_dotted_path('foo.bar') -> from foo import bar; return bar """
    next_module, remaining_names = dotted_names.split('.', 1)
    fp, pathname, description = imp.find_module(next_module, path)
    module = imp.load_module(next_module, fp, pathname, description)
    if hasattr(module, remaining_names):
        return getattr(module, remaining_names)
    if '.' not in remaining_names:
        return module
    return import_from_dotted_path(remaining_names, path=module.__path__)


if __name__ == "__main__":
    for name_of_thing in THINGS_TO_IMPORT:
        thing = import_from_dotted_path(name_of_thing)
        print '%s => %r' % (name_of_thing, thing)
{% endhighlight %}

And the output as expected:

{% highlight bash %}
utils.misc.MyClass1 => <class 'misc.MyClass1'>
utils.misc.foo => {'bar': 7}
utils.bar => 'foo'
utils.misc => <module 'utils' from 'myapp/utils/__init__.pyc'>
{% endhighlight %}

Here is a directory listing of my test modules, in case this isn't clear.

{% highlight bash %}
./utils/__init__.py:

bar = 'foo'


./utils/misc.py:

class MyClass1(object):
    pass

foo = {'bar': 7}
{% endhighlight %}
