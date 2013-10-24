---
layout: post
title: Subclassing Django's runserver causes command to be run twice
tags: django
---

This week I was creating my own version of the Django management command `runserver`. Like the built-in, I wanted to run a lightweight development only web server for my Django app. In addition, I was looking to run a syncdb, load some initial data and start up the server with that. The goal was to use an in-memory sqlite3 database, and use this command as a way to spin up an interactive test instance.

This is easily achieved by using `call_command` to call `syncdb` and `runserver` in sequence. The in-memory sqlite3 config I would leave to a Django settings file. But I noticed that `syncdb` seemed to be getting called twice, leading to double the start up time.

Rooting around in the Django bug database, I found that this was a [known issue](https://code.djangoproject.com/ticket/8085) with the default auto-reloading functionality of `runserver`. The solution turned out to be a simple as disabling that functionality by passing an option to the native `runserver` when you use `call_command`.

{% highlight python %}
import os
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.core.management.commands.runserver import BaseRunserverCommand


class Command(BaseCommand):
    ''' Runs the built-in Django runserver with initial schema and fixtures
    Note: cannot use auto-reloading because that casues resetdb to be called
    twice.
    '''

    # remove this option from the --help for this command
    option_list = (o for o in BaseRunserverCommand.option_list if o.dest != 'use_reloader')
    help = 'Starts a lightweight web server testing.'
    args = '[optional port number, or ipaddr:port] appname appname'

    def handle(self, addrport='', *args, **options):
        call_command('syncdb', *args, **options)
        # BUG: runserver gets called twice if --noreload is False
        # https://code.djangoproject.com/ticket/8085
        options['use_reloader'] = False
        call_command('runserver', addrport, *args, **options)
{% endhighlight %}
