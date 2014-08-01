---
layout: post
title: Ignore pyflakes warnings with bypass_pyflakes
tags: python pyflakes
---

[Pyflakes](https://github.com/kevinw/pyflakes) is a popular linter for python, even if it [isn't being maintained](https://github.com/kevinw/pyflakes/commits/master) anymore. One [long](http://stackoverflow.com/questions/5033727/how-do-i-get-pyflakes-to-ignore-a-statement) [standing](https://github.com/kevinw/pyflakes/pull/22) request is to allow ignoring of specific warnings with comments, like many other linters allow.

For example, it's common in python config files to use `import *`. But you definitely [don't want](http://pythonconquerstheuniverse.wordpress.com/2011/03/28/why-import-star-is-a-bad-idea/) to allow that in most places.

{% highlight python %}
form settings.base import *
MY_OVERIDE = 'foobar'  # over-ride this setting from base
{% endhighlight %}

This results in the warning `settings/local.py:1: 'from settings.base import *' used; unable to detect undefined names`.

It would be nice to be able to do the following.

{% highlight python %}
form settings.base import *  # bypass_pyflakes
MY_OVERIDE = 'foobar'  # over-ride this setting from base
{% endhighlight %}

Here is a python script that monkey patches pyflakes to add this functionality.

{% highlight python %}
#!/usr/bin/env python

from pyflakes.scripts import pyflakes
from pyflakes.checker import Checker


def report_with_bypass(self, messageClass, *args, **kwargs):
    text_lineno = args[0] - 1
    with open(self.filename, 'r') as code:
        if code.readlines()[text_lineno].find('bypass_pyflakes') >= 0:
            return
    self.messages.append(messageClass(self.filename, *args, **kwargs))

# monkey patch checker to support bypass
Checker.report = report_with_bypass

pyflakes.main()
{% endhighlight %}

If you save this as `pyflakes-bypass.py`, instead of running the `pyflakes <path>` command directly, you would now run `pyflakes-bypass.py <path>`.
