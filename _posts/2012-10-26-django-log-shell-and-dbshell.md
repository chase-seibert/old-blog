
---
layout: post
title: Logging Django shell and dbshell sessions
tags: django logging
---

The Django [shell management command](https://docs.djangoproject.com/en/dev/ref/django-admin/#shell) is a supremely useful tool for developers to explore and potentially modify data in their applications, both during development and in production. For jobs where that does not perform well enough, or you need lower level access to the data, the [dbshell command](https://docs.djangoproject.com/en/dev/ref/django-admin/#dbshell) gives you even more power.

# With great power, comes great responsibility

Every developer has been in a situation where they use their supremely powerful tools to make a supremely large mistake against production data. In those cases, although it may not save you, it can be critical to have a log of what you did, exactly. If you realize your mistake while you are in front of the console, they you have all the information you need. But what if you only realize minutes, hours or days later?

Or perhaps you just need plausible deniability. In either case, it's not too hard to hookup logging to Django's shell commands. In this post, I'll show you how to enable per-user logging into separate files, with date and time stamps.

# Shell Logging with iPython

[iPython](http://ipython.org/download.html) is a great replacement for the already pretty awesome interactive interpreter built into python. You should be running it anyway, but if you're looking for another reason, it has built-in logging capability. To get Django to use iPython for its `shell` command, you just need to have iPython installed with `pip install ipython`. Django will detect and use it.

To enable logging from Django's `shell` command, put the following in you project root directory in a file called `ipython_config.py`.

{% highlight python %}
import os

# lines of code to run at IPython startup.
c = get_config()
c.InteractiveShellApp.exec_lines = [
        "%%logstart -t -o /var/log/django/shell-%s.log" % os.environ.get("USER", "none")]
{% endhighlight %}

To get `shell` to recognize your config file, you need to write your own subclass. Place this in a file under your project directory called `management/commands/shell.py`, and Django will automatically pick it up. Make sure to create `__init__.py` files in the `management` and `commands` directories.

{% highlight python %}
from django.core.management.commands.shell import Command as DjangoShellCommand
from IPython.frontend.terminal.ipapp import TerminalIPythonApp

class Command(DjangoShellCommand):

    def ipython(self):
        """ need to over-ride this to invoke the TerminalIPythonAdd, versus embed().
        The later does not take configuration options we require to enable logging.
        See: https://code.djangoproject.com/ticket/17078
        """
        app = TerminalIPythonApp.instance()
        app.initialize(argv=[])
        app.start()
{% endhighlight %}

You will also need to create the `/var/log/django` directory with write permissions.

{% highlight bash %}
mkdir /var/log/django
chown root:root /var/log/django
chmod 775 /var/log/django
{% endhighlight %}

# Database Shell Logging with MySQL

Assuming you're using MySQL as your database, you can enable logging by placing the following code in your `settings.py` file, bellow your `DATABASES` declaration.

{% highlight python %}
import os
import socket
import sys

options = DATABASES['default'].get('OPTIONS', {})
hostname = socket.gethostname()
if 'dbshell' in sys.argv and DATABASES['default'].get('ENGINE').startswith('mysql'):
    # have mysql executable log for us, using a per user config file
    mycnf = '/tmp/%s.cnf' % os.environ.get('USER')
    with open(mycnf, 'w') as file:
        contents = '''
[mysql]
prompt="[\D %(username)s@%(host)s]> "
tee=/var/log/django/dbshell-%(username)s.log
''' % dict(username=os.environ.get('USER'), host=hostname)
        file.write(contents)
    options['read_default_file'] = mycnf
DATABASES['default']['OPTIONS'] = options
{% endhighlight %}

This method also uses a logging facility built-in to an external tool, in this case the `mysql` command line interactive shell.
