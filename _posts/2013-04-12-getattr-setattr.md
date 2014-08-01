---
layout: post
title: Dynamic Attributes in Python
tags: python tutorial
---

One of the strengths of a dynamic language is that it allows you to more easily work introspection and light weight meta-programming into your every day code. In Python, one of the primary ways of taking advantage of the dynamic nature of the language is through attribute access.

__Note__: this is part one in a series of posts about basic Python functionality.

In most cases, to get an attribute of an object, you just want to use `obj.field`. But if you don't know the name of the field until runtime, you can use `getattr(obj, 'field')`.

{% highlight python %}
def print_field(obj, field):
    try:
        print getattr(obj, field)
    except AttributeError:
        print 'No %s field' % field
{% endhighlight %}

This is a fairly common pattern, so you can avoid the extra try/catch and use the third `default` parameter:

{% highlight python %}
def print_field(obj, field):
    print getattr(obj, field, 'No %s field' % field)
{% endhighlight %}

Both attribute access methods are [virtually identical](http://stackoverflow.com/questions/2909423/is-it-bad-practice-to-use-pythons-getattr-extensively#answer-2909734) in terms of performance. The regular method produces slightly cleaner code, so normally you would use that. Besides, when do you __NOT__ know the names of the fields you want to access ahead of time?

If you're dealing with data, you don't always know. For example, say you're mapping URLs to view methods. If the user hits `/user/123/settings`, you could route that to a view function as follows:

{% highlight python %}
class ViewClass(object):

    def route(request):
        return getattr(self, request.url.split('/')[-1], 'not_found_404')(request)

    def settings(request):
        return HttpResponse('Here is your settings page!')

    def not_found_404(request):
        return HttpResponse('404 Page Not Found', code=404)
{% endhighlight %}

Of course, you could always do this with a pre-defined set of URLs, but the point is that you have a built-in way to avoid that code duplication. In general, this is known as keeping your code [DRY](http://en.wikipedia.org/wiki/Don't_repeat_yourself). For example, notice the duplication of tokens in code like the following:

{% highlight python %}
obj.first_name.first_child.value = 'Chase'
obj.last_name.first_child.value = 'Seibert'
obj.phone.first_child.value = '(555) 123-4567'
{% endhighlight %}

Instead, you could do something like the following:

{% highlight python %}
for (field, value) in (('first_name', 'Chase'), ('last_name', 'Seibert'), ('phone', '(555) 123-4567')):
    getattr(obj, field).first_child.value = value
{% endhighlight %}

While this is certainly more code, for a larger number of lines, there will be a code savings. It's also easy to refactor all the obj.field lines at once, if for example you need to change it to `obj.field.set(value)`.

You can also make use of dynamic attributes on the class side by over-riding `__getattr__`.

{% highlight python %}
class Counter(object):
    def __getattr__(self, name):
        ''' will only get called for undefined attributes '''
        setattr(self, name) = 0

counter = Counter()
counter.foo = counter.foo + 100
print counter.foo  # prints '100'
{% endhighlight %}

There is an alternate [magic method](http://www.rafekettler.com/magicmethods.html) called `__getattribute__` that fires even for attributes that are already declared. But be careful, it's easy to get into an infinite recursion loop here.

{% highlight python %}
class Logger(object):
    def __getattribute__(self, name):
        print 'Accessed attribute %s' % name
        return object.__getattribute__(self, name)

logger = Logger()
logger.foobar = 1  # prints 'Accessed attribute foobar'
{% endhighlight %}

This is a trivial example, better implemented with [decorators](http://wiki.python.org/moin/PythonDecorators). But that is a subject for another post!

Finally, there is a sister to `getattr` called `setattr`. As you would expect, this will set attributes by name. Here is a quick example:

{% highlight python %}
class MyModel(object):

    @classmethod
    def from_kwargs(cls, **kwargs):
        obj = cls()
        for (field, value) in kwargs.items():
            setattr(self, field, value)
        return obj

model = MyModel.from_kwargs(foo=1, bar=2)
print model.foo, model.bar  # prints '1, 2'
{% endhighlight %}
