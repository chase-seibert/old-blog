---
layout: post
title: Hacking Django runserver to run multiple Django instances
tags: django
---

Recently at work we've been on a "servicifying" kick, meaning we're slowly converting our monolithic Django app into separate services. To start, this just means breaking up the existing runtime into pieces. Instead of one logical web process, we now have different ones for the web app, admin, login, apis, etc.

For production, this doesn't change the deployment model all that much. We just have separate servers for various roles. For development, we still want to be able to easily run all the services at once on your local machine.

Enter `runservices`, an extension of the Django `runserver` command that just launches a bunch of processes in a `screen` session (a natural choices for us, as we're already using `screen` intensively). It turns out that screen has the ability to [launch multiple windows on startup](http://superuser.com/questions/386059/how-can-i-start-multiple-screen-sessions-automatically) using a custom `.screenrc` file, passed on the command-line with `-c my.screenrc`. The format needed inside the `.screenrc` file is as follows:

{% highlight bash %}
# create two windows, called "TODO" and "coding" in vim
screen -t TODO vim TODO.txt
screen -t coding vim ~/code
{% endhighlight %}

When I first saw this, I thought we could use it to launch our various services. What I did was write a custom Django management command that dynamically writes a `.screenrc` file and executes it. You can run all the services, or specify just a few. Our services are launched by settings corresponding environment variables, which can be done on the command line itself.

{% highlight python %}
{% raw %}
import os

from django.template.base import Template
from django.template.base import Context
from django.core.management.base import BaseCommand


SERVICES = (
    # nothreading == to help with sqlite locking issues
    ('web', './manage.py runserver 0:8000 --nothreading'),
    ('admin', 'ADMIN=True ./manage.py runserver 0:8001 --nothreading'),
    ('login', 'LOGIN=True ./manage.py runserver 0:8002 --nothreading'),
    ('celery', './manage.py celery beat'),
)

ACTIVATE_REL_PATH = '../virtualenv/bin/activate'

DEFAULT_SERVICES = (
    'web',
    'admin',
)


class Command(BaseCommand):

    help = 'Runs all the services'
    args = 'appname appname'

    def handle(self, *args, **options):
        allowed_services = list(set(DEFAULT_SERVICES + args))
        services = [s for s in SERVICES if s[0] in allowed_services]
        multiplexer = ScreenMultiplexer(services)
        multiplexer.write_rc_file()
        multiplexer.run()


def render_template(source, context_dict):
    template = Template(source)
    context = Context(context_dict)
    return template.render(context)


class ScreenMultiplexer(object):

    def __init__(self, services, *args, **kwargs):
        self.services = services
        self.rc_file = '.screenrc'
        self.rc_template = '''
caption always "%{= kw}%-w%{= BW}%n %t%{-}%+w %-= Exit: C-a \ %c"
{% for name, command in services %}
screen -t {{ name }} bash -c "{{ venv }}; {{ command }}"
{% endfor %}
select 0
'''

    @property
    def venv(self):
        activate = os.path.abspath(os.path.join(os.getcwd(), ACTIVATE_REL_PATH))
        if not os.path.exists(activate):
            raise Exception("Could not locate virtualenv script %s" % activate)
        return 'source %s' % activate

    def render(self):
        return render_template(self.rc_template, {
            'venv': self.venv,
            'services': self.services,
        })

    @property
    def rc_path(self):
        return os.path.join(os.getcwd(), self.rc_file)

    def write_rc_file(self):
        with open(self.rc_path, 'w') as f:
            f.write(self.render())

    def run(self):
        os.execlp('screen', 'screen', '-c', self.rc_path)
{% endraw %}
{% endhighlight %}

The resulting `.screenrc` files ends up looking like (added comments):

{% highlight bash %}
# set a nice screen footer
caption always "%{= kw}%-w%{= BW}%n %t%{-}%+w %-= Exit: C-a \ %c"

# run web
screen -t web bash -c "source /Users/myuser/code/myproject/virtualenv/bin/activate; ./manage.py runserver 0:8000 --nothreading"

# run admin
screen -t admin bash -c "source /Users/myuser/code/myproject/virtualenv/bin/activate; ADMIN=True ./manage.py runserver 0:8000 --nothreading"

# select the first window (web) by default
select 0

{% endhighlight %}

The only tricky bit was getting `virtualenv` to activate properly inside the screen session. Because it uses the bash `source` command, I needed to have `screen` actually execute bash directly, and pass the source command.

The result is a single session of multiple windows that you can toggle through with the standard screen commans like `C-a`.

![screen django](/blog/images/screen.png)

*Note*: I'm also running into intermittent issues with `sqlite3` locking the database, due to many processes trying to access it. Running with `--nothreading` and reducing celery to one worker seems to have helped, but we may need to move to `mysql` for development.
