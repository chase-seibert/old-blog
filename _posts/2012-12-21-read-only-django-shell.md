---
layout: post
title: Read only Django shell
tags: django shell
---

Say you have a bunch of developers that occasionally need Django shell access to production, but you want this to be an exceptional event. Here is a drop-in replacement for `./manage.py shell` that defaults to read-only mode, but lets the developer switch to writable mode on the fly, while notifying the team.

{% highlight python %}
import sys
import os
from optparse import make_option
from django.core.management.commands.shell import Command as DjangoShellCommand
from django.db import router
from django.core.management.base import NoArgsCommand
from myapp.utils import hipchat


_original_db_for_write = None


def confirm_writable(self, *args, **kwargs):
    ''' user can over-ride the shell to be writable at any time, but it sends a message '''

    # for migrations, you might be in a non-interactive shell
    # so don't prompt, but still send out the notification
    if sys.stdin.isatty():
        cont = raw_input('Are you sure you want to connect to the production database in writable mode? [y/N] ')
        if not cont.lower().startswith('y'):
            raise IOError('Database in read-only mode.')

    router.db_for_write = _original_db_for_write
    send_alert()


def send_alert():
    hipchat.send_message("I'm opening up a writable prod shell!",
        from_name=os.environ.get('USER'),
        color='red')


class Command(DjangoShellCommand):

    option_list = DjangoShellCommand.option_list + (
        make_option('--write', action='store_true', dest='writable',
            help='Connect to the database in writable mode.'),
    )

    def handle_noargs(self, **options):

        # only allow read-only shells in prod by default
        if options.get('writable'):
            send_alert()
        else:
            global _original_db_for_write
            _original_db_for_write = router.db_for_write
            router.db_for_write = confirm_writable

        return super(Command, self).handle_noargs(**options)
{% endhighlight %}

The strategy here is to use Django's [database router](https://docs.djangoproject.com/en/dev/topics/db/multi-db/#using-routers) mechanism to throw an exception when trying to write to the database.

# Install

Drop this into your project as `myapp/management/commands/shell.py` and it will over-ride the default shell command.

# Hipchat

In my case, I'm notifying the team via [Hipchat](https://www.hipchat.com/). Of course, you can replace this function with a version that sends out an email, etc. If you're curious, here is the hipchat code:

{% highlight python %}
import json
import urllib
import urllib2


def _make_hipchat_request(url, auth_token=None):
    if not auth_token:
        from django.conf import settings
        auth_token = settings.HIPCHAT_TOKEN
    HIPCHAT_BASE_URL = "https://api.hipchat.com/v1"
    final_url = "%s%s%sauth_token=%s" % (
        HIPCHAT_BASE_URL,
        url,
        '&' if '?' in url else '?',
        auth_token)
    return urllib2.urlopen(final_url).read()


def send_message(message, room_id='Engineering', from_name='Django', auth_token=None, color='yellow'):
    url = '/rooms/message?message=%s&room_id=%s&from=%s&message_format=text&color=%s' % (
        urllib.quote(message),
        urllib.quote(room_id),
        urllib.quote(from_name),
        urllib.quote(color))
    _make_hipchat_request(url, auth_token)
{% endhighlight %}
