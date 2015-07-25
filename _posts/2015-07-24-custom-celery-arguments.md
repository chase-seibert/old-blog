---
layout: post
title: Customizing Celery with Task Arguments
tags: celery
---

[Celery](http://www.celeryproject.org/) is an awesome distributed asynchronous task system for Python. It's great out of the box, but a couple of times I have needed to customize it. Specifically, I want to be able to define behavior based on a new `apply_sync` arguments. Also, it would be nice to be able to pass state to the worker tasks.

First, you can subclass the main `Celery` class to define a custom `Task` class.

```python
import socket

from celery import Celery, Task
from kombu.exceptions import InconsistencyError


class MyCelery(Celery):
    """ Subclass of a Celery application class that uses a custom Task type """
    task_cls = 'myapp.mymodule:MyTask'

```

In your `Task` class, you can override `apply_async` (which is also called from `delay`), as well as `__call__`, which wraps around the actual task body.

```python


class MyTask(Task):

    abstract = True

    def apply_async(self, args=None, kwargs=None, task_id=None, producer=None,
                    link=None, link_error=None, **options):
        """ invoked either directly or via .delay() to fork a task from the main process """

        # parse any custom task options from the .delay() or .apply_async() calls
        safe = options.pop('safe', False)  # safely trap errors talking to celery broker

        options['headers'] = options.get('headers', {})
        options['headers'].update({
            'safe': safe,
        })

        try:
            return super(MyTask, self).apply_async(
                args, kwargs, task_id, producer, link, link_error, **options)
        except (InconsistencyError, socket.error) as e:
            # InconsistencyError == cannot find the celery queue
            # socket.error == cannot talk to the queue server at all
            if not safe:
                raise

    def __call__(self, *args, **kwargs):
        """ execute the task body on the remote worker """
        safe = self.get_header('safe')
        try:
            return super(NWTask, self).__call__(*args, **kwargs)
        except Exception:
            if not safe:
                raise

    def get_header(self, key, default=None):
        return (self.request.headers or {}).get(key, default)
```

In this example, I'm introducing an optional `safe` argument to `apply_async`, which traps and ignores specific exceptions trying to fork the task. It also piggy backs on the celery task headers to pass itself to the worker process, where it ignores any exception thrown by the task itself.
