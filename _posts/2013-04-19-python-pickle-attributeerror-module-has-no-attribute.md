---
layout: post
title: Python pickle AttributeError 'module' object has no attribute 'foobar'
tags: python pickle
---

Ran into an interesting edge case with [pickle](http://docs.python.org/2/library/pickle.html) this week. I had a producer task that was querying objects from a database, and pickling them plus a reference to a callback function to pass to worker tasks. Everything was working fine, but I was getting sick of logging into a [Django shell](https://docs.djangoproject.com/en/dev/intro/tutorial01/#playing-with-the-api) to invoke the workers with test data. So I wrote a quick `__main__` function in my task code to do the same thing.

{% highlight python %}
import argparse
import pickle
from django.contrib.auth import user
from myproject.utils import my_task_func, worker


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Invoke the workers manually.')
    parser.add_argument('user_id', type=int, help='User ID')
    args = parser.parse_args()
    user = User.objects.get(pk=args.user_id)
    pickled_callback = pickle.dumps(my_task_func)
    pickled_cb_args = pickle.dumps([user])
    worker.delay(pickled_callback, pickled_cb_args)
{% endhighlight %}

To my surprise, this exact same code I had been typing into a shell was now throwing an exception when invoked from inside a `__main__` function.

{% highlight python %}
Traceback (most recent call last):
  ...
  File "/usr/lib/python2.4/pickle.py", line 872, in load
    dispatch[key](self)
  File "/usr/lib/python2.4/pickle.py", line 1083, in load_inst
    klass = self.find_class(module, name)
  File "/usr/lib/python2.4/pickle.py", line 1140, in find_class
    klass = getattr(mod, name)
AttributeError: 'module' object has no attribute 'my_task_func'
{% endhighlight %}

It turns out that when you pickle a function from inside a `__main__` block, the module reference that it will be pickled with is `__main__`, not the actual module namespace. This is actually a [known issue](http://bugs.python.org/issue5509). In my case, it was easy to work-around; I simply put this code into a [Django custom management command](https://docs.djangoproject.com/en/dev/howto/custom-management-commands/).

More discussion of this issue [here](http://stefaanlippens.net/pickleproblem).
