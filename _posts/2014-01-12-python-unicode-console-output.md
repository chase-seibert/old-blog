---
layout: post
title: Print to the console in Python without UnicodeEncodeErrors
tags: python
---

I can't believe I just found out about this! If you use Python with unicode data, such as Django database records, you may have seen cases where you print a value to the console, and if you hit a record with an extended (non-ascii) character, your program crashes with the following:

{% highlight bash %}
Traceback (most recent call last):
  File "foobar.py", line 792, in <module>
    print value
UnicodeEncodeError: 'ascii' codec can't encode character u'\xa0' in position 20: ordinal not in range(128)
{% endhighlight %}

This often comes up when you have a Django model instance with a user-entered field in the `__unicode__` return value. In the past, I have solved this by changing the print statement to print something that cannot be unicode, such as a database ID. Alternatively, you could do something like `value.encode('ascii', 'ignore')`. But just this week, I realized that there is a much better solution.

Your termianl can typically handle UTF8 characters just fine. The issue is actually that Python is just getting confused about what encoding the terminal accepts. However, you can [explicitly set this value](http://docs.python.org/2/using/cmdline.html#envvar-PYTHONIOENCODING).

The `PYTHONIOENCODING` environment variable controls what encoding stdout/stderr uses. If you do an `export PYTHONIOENCODING=UTF-8`, it will solve the problem. You can also prefix any given single python command-line invocation with this value, such as `PYTHONIOENCODING=UTF-8 ./manage.py runserver`.

Alternatively, you can set this value in your actual code, say in your `settings.py` file:

{% highlight python %}
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)
{% endhighlight %}
