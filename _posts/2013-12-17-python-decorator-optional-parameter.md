---
layout: post
title: Writing a Python decorator that can be called as a function or a callable
tags: python
---

A [Python decorator](http://en.wikipedia.org/wiki/Python_syntax_and_semantics#Decorators) wraps a function with another function. Classing examples are a `@cache` decorator or a `@log` decorator, which call the wrapped function and either cache it's results or log the fact that it was called, respectively. Decorators can be implemented as functions or as classes; they just need to be callable.

Here is the basic decorator pattern. This one does nothing but prints that it was called.

{% highlight python %}
from functools import wraps


def my_decorator(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        print 'called decorator'
        return func(*args, **kwargs)
    return wrapped


@my_decorator
def function_to_wrap():
    import random
    return random.getrandbits(128)


if __name__ == "__main__":
    function_to_wrap()  # prints 'called decorator'
{% endhighlight %}

Here is an example of a `@cache` decorator implemented in this fashion (as a function). It uses Django's caching layer as the actual cache implementation.

{% highlight python %}
from functools import wraps
from django.core.cache import cache as _cache


def cache(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        cache_key = [func, args, kwargs]
        result = _cache.get(cache_key)
        if result:
            return result
        result = func(*args, **kwargs)
        _cache.set(cache_key, result)
        return result
    return wrapped


@cache
def function_to_wrap():
    import random
    return random.getrandbits(128)


if __name__ == "__main__":
    print function_to_wrap()  # prints '47141457794590517513826129394479136255'
    print function_to_wrap()  # prints '47141457794590517513826129394479136255' also (cached)
{% endhighlight %}

This uses a very simplistic cache key generation scheme. It assumes that the args and kwargs that your wrapped function will be passed are all castable to strings. Django's default [cache key generator](https://docs.djangoproject.com/en/dev/topics/cache/#cache-key-transformation) looks like:

{% highlight python %}
def make_key(key, key_prefix, version):
    return ':'.join([key_prefix, str(version), key])
{% endhighlight %}

There are also a number of caveats. For example, Django will thrown an exception if the cache key is over 250 characters. Writing your own key generation is out of the scope of this post.


You will also notice that I'm using a [functools.wraps](http://docs.python.org/2/library/functools.html#functools.wraps). This ensures that when callers introspect the `function_to_wrap` function, it shows its `__name__` attribute as `function_to_wrap` and not `cache`. This is especially useful for not mucking up your logging and performance stacktraces (for example, New Relic stats).

Here is an example of the same decorator written as a class:

{% highlight python %}
import functools
from django.core.cache import cache as _cache


class cache(object):

    def __init__(self, func):
        self.func = func
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        cache_key = [self.func, args, kwargs]
        result = _cache.get(cache_key)
        if result:
            return result
        result = self.func(*args, **kwargs)
        _cache.set(cache_key, result)
        return result


@cache
def function_to_wrap():
    import random
    return random.getrandbits(128)


if __name__ == "__main__":
    print function_to_wrap()  # prints '47141457794590517513826129394479136255'
    print function_to_wrap()  # prints '47141457794590517513826129394479136255' also (cached)
{% endhighlight %}

Both implementations have the same usage syntax. You just _decorate_ the function definition that you want to wrap with the @ syntax.

## Passing Parameters

