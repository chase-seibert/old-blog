---
layout: post
title: Writing a Python decorator that can be called as a function or a callable
tags: python
---

A [Python decorator](http://en.wikipedia.org/wiki/Python_syntax_and_semantics#Decorators) wraps a function with another function. Classing examples are a `@cache` decorator or a `@log` decorator, which call the wrapped function and either cache its results or log the fact that it was called, respectively. Decorators can be implemented as functions or as classes; they just need to be callable.

Here is the basic decorator pattern. This one does nothing but prints that it was called.

{% highlight python %}
from functools import wraps
import random


def my_decorator(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        print 'called decorator'
        return func(*args, **kwargs)
    return wrapped


@my_decorator
def function_to_wrap(bits=128):
    return random.getrandbits(bits)


if __name__ == "__main__":
    function_to_wrap()  # prints 'called decorator'
{% endhighlight %}

Here is an example of a `@cache` decorator implemented in this fashion (as a function). It uses Django's caching layer as the actual cache implementation.

{% highlight python %}
from functools import wraps
import random
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
def function_to_wrap(bits=128):
    return random.getrandbits(bits)


if __name__ == "__main__":
    print function_to_wrap()  # prints '47141457794590517513826129394479136255'
    print function_to_wrap()  # prints '47141457794590517513826129394479136255' also (cached)
{% endhighlight %}

This uses a very simplistic cache key generation scheme. It assumes that the args and kwargs that your wrapped function will be passed are all castable to strings. Django's default [cache key generator](https://docs.djangoproject.com/en/dev/topics/cache/#cache-key-transformation) looks like:

{% highlight python %}
def make_key(key, key_prefix, version):
    return ':'.join([key_prefix, str(version), key])
{% endhighlight %}

There are also a number of caveats. For example, Django will throw an exception if the cache key is over 250 characters. Writing your own key generation is out of the scope of this post.


You will also notice that I'm using a [functools.wraps](http://docs.python.org/2/library/functools.html#functools.wraps). This ensures that when callers introspect the `function_to_wrap` function, it shows its `__name__` attribute as `function_to_wrap` and not `cache`. This is especially useful for not mucking up your logging and performance stacktraces (for example, New Relic stats).

Here is an example of the same decorator written as a class:

{% highlight python %}
import functools
import random
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
def function_to_wrap(bits=128):
    return random.getrandbits(bits)


if __name__ == "__main__":
    print function_to_wrap()  # prints '47141457794590517513826129394479136255'
    print function_to_wrap()  # prints '47141457794590517513826129394479136255' also (cached)
{% endhighlight %}

Both implementations have the same usage syntax. You just _decorate_ the function definition that you want to wrap with the @ syntax.

## Passing Parameters

Sometimes you want to pass parameters to your decorators. The trick here is to add another layer of indirection and create a function that takes parameters and returns your original decorator. As you can see, the naming also gets a little mind-bending here; as we struggle to propery name what should really be anonymous functions for the callable we're returning, and the function that defines the logic of our decorator.

{% highlight python %}
from functools import wraps
import random
from django.core.cache import cache as _cache


def cache(seconds=None):

    def callable(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            cache_key = [func, args, kwargs]
            result = _cache.get(cache_key)
            if result:
                return result
            result = func(*args, **kwargs)
            _cache.set(cache_key, result, timeout=seconds)
            return result
        return wrapped

    return callable


@cache(seconds=60)
def function_to_wrap(bits=128):
    return random.getrandbits(bits)


if __name__ == "__main__":
    print function_to_wrap()  # prints '47141457794590517513826129394479136255'
    print function_to_wrap()
{% endhighlight %}

Of course, you can also do the same thing in the class style. Again, the trick is that a decorator can be a callable, _or return a callable_.

{% highlight python %}
from functools import wraps
import random
from django.core.cache import cache as _cache


class cache(object):

    def __init__(self, seconds=None):
        self.seconds = seconds

    def __call__(self, func):

        @wraps(func)
        def callable(*args, **kwargs):
            cache_key = [func, args, kwargs]
            result = _cache.get(cache_key)
            if result:
                return result
            result = func(*args, **kwargs)
            _cache.set(cache_key, result, timeout=self.seconds)
            return result

        return callable


@cache(seconds=60)
def function_to_wrap(bits=128):
    return random.getrandbits(bits)


if __name__ == "__main__":
    print function_to_wrap()  # prints '47141457794590517513826129394479136255'
    print function_to_wrap()  # prints '47141457794590517513826129394479136255' also (cached)
{% endhighlight %}

## Optional Parameters

Now, a whole in the design of decorators, in my opinion, is that while you're deciding to make your decorator a callable or return a callable, you may also be struggling with how to make it do both at once.

What if I don't want the `seconds` argument to be mandatory? With either the functional or class based implementations, you will end up using your decorator like so:

{% highlight python %}
@cache()
def function_to_wrap(bits=128):
    return random.getrandbits(bits)
{% endhighlight %}

This is just ugly. It introduces a source of errors (leaving off the `()` will throw a somewhat mysterious exception:

{% highlight python %}
TypeError: __call__() takes exactly 2 arguments (1 given)
{% endhighlight %}

With a little ingenuity, you can have your callable and return it, too. Here is a functional decorator that can be used as `@cache(seconds=60)`, or just `@cache`.

{% highlight python %}
from functools import wraps
import random
from django.core.cache import cache as _cache


def cache(*args, **kwargs):

    func = None
    if len(args) == 1 and __builtins__.callable(args[0]):
        func = args[0]

    if func:
        seconds = 60  # default values

    if not func:
        seconds = kwargs.get('seconds')

    def callable(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            cache_key = [func, args, kwargs]
            result = _cache.get(cache_key)
            if result:
                return result
            result = func(*args, **kwargs)
            _cache.set(cache_key, result, timeout=seconds)
            return result
        return wrapped

    return callable(func) if func else callable


@cache(seconds=60)
def function_to_wrap(bits=128):
    return random.getrandbits(bits)

@cache
def function_to_wrap2(bits=128):
    return random.getrandbits(bits)


if __name__ == "__main__":
    print function_to_wrap()  # prints '47141457794590517513826129394479136255'
    print function_to_wrap()  # prints '47141457794590517513826129394479136255' also (cached)
    print function_to_wrap2(32)  # prints '2202905596'
    print function_to_wrap2(32)  # prints '2202905596' also (cached)
{% endhighlight %}

First, you decide whether your decorator has been called as a callable or not. If not, you pull out your optional parameters (and default them if needed). Then you dynamically return either your decorator or a callable. Admittedly this is pretty ugly, but the resulting API is nice and clear. I've also failed repeatedly to produce a class based version of this. Submissions welcome!

