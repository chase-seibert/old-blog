---
layout: post
title: Reload Python inside uWSGI as fast as humanely possible
tags: python uwsgi
---

The Django development web server you get when you execute `./manage.py runserver` optimizes for one thing; fast hot reloading when you change your Python code. It does almost nothing else well, by design.

>DO NOT USE THIS SERVER IN A PRODUCTION SETTING. It has not gone through security audits or performance tests. (And that’s how it’s gonna stay. We’re in the business of making Web frameworks, not Web servers, so improving this server to be able to handle a production environment is outside the scope of Django.)...
>The development server automatically reloads Python code for each request, as needed. You don’t need to restart the server for code changes to take effect. -  [The Django Docs](https://docs.djangoproject.com/en/dev/ref/django-admin/#runserver-port-or-address-port)

If you're running [uWSGI](http://projects.unbit.it/uwsgi/) in production, you may decide that you want to run it in development, as well. But you'll quickly notice that by default, code is not hot-reloaded in uWSGI. You can enable that with the [py-autoreload setting](http://uwsgi-docs.readthedocs.org/en/latest/Options.html#py-auto-reload-py-autoreload-python-auto-reload-python-autoreload). It works by polling the code every X seconds.

Polling is already not ideal, but the story gets even worse if your code is on a remote file system, like an NFS share. This is a common setup if your development environment is running in a VM, like [Vagrant](http://www.vagrantup.com/). The problem is that polling is relatively slow over NFS. It can take 10 seconds on a medium sized code base to pick up changes. This is a bummer if you're coming from a virtually instantaneous runserver reload.

Recent versions of uwsgi also support [inotify](https://github.com/unbit/uwsgi-docs/blob/master/Changelog-1.9.14.rst#filesystem-monitoring-interface-fsmon) to pick up changes more quickly. But that also doesn't work over NFS.

The good news is that uWSGI also supports touch reloading. Basically you set a `touch-reload` file in your config, and if you do a `touch thatfile`, your Python code gets reloaded immediately. This works well over NFS because uWSGI polls that file much more quickly.

So how can we get an OSX host machine to update the touch file in the guest Linux host every time your code changes? Basically, you can use an inotify replacement for OSX called [fswatch](https://github.com/alandipert/fswatch). In this case, we're going to have it run a command to open a socket to the guest VM, and tell a custom daemon to touch the reload file.

First, you need to install fswatch locally.

{% highlight bash %}
brew install fswatch
{% endhighlight%}

Then, fork off a process watching your code directory, and pinging the remote daemon. I'm assuming that your VM has an entry in your hosts file called `vagrant-vm`. You can also use a static IP. The daemon will be listening on port 9001. *Note: fswatch does not currently take an extension filter, so this will restart uWSGI on ANY file change.*

{% highlight bash %}
fswatch ~/mycode "echo '.' |nc vagrant-vm 9001" &
{% endhighlight%}

Then, on the Linux VM guest, you fork off the daemon listener.

{% highlight bash %}
nc -l 9001 -k > ~/mycode/.reload
{% endhighlight%}

This is assuming you have the uWSGI `touch-reload` file set to `~/mycode/.reload`. That's it! When you update a file in `~/mycode` locally, you should see the following immediately in the uWSGI logs:

{% highlight bash %}
...gracefully killing workers...
Gracefully killing worker 1 (pid: 25505)...
worker 1 buried after 1 seconds
binary reloading uWSGI...
...
WSGI app 0 (mountpoint='') ready in 0 seconds on interpreter 0x239b270 pid: 18792 (default app)
gracefully (RE)spawned uWSGI master process (pid: 18792)
spawned uWSGI worker 1 (pid: 25512, cores: 1)
Sun Mar 30 18:01:26 2014 - [emperor] vassal is ready to accept requests
Python auto-reloader enabled
{% endhighlight %}
