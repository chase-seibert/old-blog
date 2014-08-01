---
layout: post
title: Celery fail silently context manager
tags: python celery
---

[Celery](http://www.celeryproject.org/) ships with an configuration option called [CELERY_ALWAYS_EAGER](http://celery.readthedocs.org/en/latest/configuration.html#celery-always-eager) which causes all tasks to be executed immediately instead of being asynchronously executed on workers. This can be very useful for unit tests. Instead of running a real message queue and separate worker processes, your unit tests can execute all in one process and still run the necessary tasks.

But in many cases, those tasks are not necessary for the unit tests to succeed. Say you have a task that fires when you create a user that sends a welcome email. You don't want the caller to wait while a worker composes a MIME message and contacts the SMTP server; that could take a little time. It's more of a fire and forget model. Actually, this is ALWAYS the case if you don't use the celery results backend; your callers have no way of receiving a result from the task, so it can't depend on it in a strict sense, unless it's doing some kind of database polling and waiting.

If this matches your usage pattern for celery, it may make you wish that you have a setting called CELERY_ALWAYS_FAIL_SILENTLY, instead. To save time on your unit tests, you could tell celery to simply discard any calls to `.delay()` or `.apply_async()`. It would be just as if celery had accepted the task, but it hadn't got around to running just yet. Except that it would never run.

It turns out that you can implement this yourself by monkeypatching celery. Here is a context manager that does just that:

{% highlight python %}
from contextlib import contextmanager
from celery import Celery

app = Celery('tasks', broker='amqp://guest:guest@localhost:5672//')

@app.task
def mytask():
    print 'Inside mytask'

@contextmanager
def celery_fail_silenty(*args):
    ''' short-circuit all tasks unless we are in eager mode '''

    from celery.app import current_app
    app = current_app()

    def send_task(self, *args, **kwargs):
        if app.conf.CELERY_ALWAYS_EAGER:
            return original_send_task(*args, **kwargs)

    original_send_task = app.send_task
    app.send_task = send_task
    try:
        yield 1
    finally:
        app.send_task = original_send_task


if __name__ == '__main__':
    #app.conf.update(CELERY_ALWAYS_EAGER=True)
    with celery_fail_silenty():
        mytask.delay()
{% endhighlight %}

As an added feature, it will execute the task in process if CELERY_ALWAYS_ENABLED is set. That way, you can use something like Django's [override settings](https://docs.djangoproject.com/en/1.4/topics/testing/#overriding-settings) if you want just a small subset of your unit tests to actually execute their tasks.

I originally tried to mock `apply_async` directly, but that is a bound method per-task, and they are bound on import, so you can't easily change them all at runtime.
