---
layout: post
title: Faster Django/sqlite runserver with /dev/shm
tags: django linux
---

When you're writing software, the feedback loop is king. Whether you're implementing new functionality, changing server configuration or writing unit tests, the speed of your feedback cycle is critical. The ideal scenario is that you make a change, and you can immediately see and effect. For web apps, this means that you should be able to save your Python/HTML/CSS/Javascript code, `ALT-TAB` to your browser, hit refresh, and see the changes. Any lag introduced in that cycle is bad; the more lag, the worse off you are.

A while back, I found out that when running Django unit tests, you can use sqlite in-memory mode to greatly speed up your test runs. Because Django unit tests create your schema from scratch and insert fixtures every time you run them, this can mean the difference between tens of seconds per change, and just one or two seconds. You can edit your `settings.py` and set the `TEST_NAME` to `None` or `:memory:` to tell sqlite to use and in-memory database.

{% highlight python %}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATABASE_DIR, 'sqlite3.db'),
        'TEST_CHARSET': 'UTF8',
        'TEST_NAME': None  # in-memory sqlite db
    }
}
{% endhighlight %}

I just recently discovered that you can also use an in-memory database for your actual `runserver` development server process. You can't just set the `NAME` to `None`; Django will not start in this mode. Presumably this is because it would not work very well in practice; every time the process started, it would create a schema-less database with no data. This is because `runserver` has no facility to run `syncdb` first. If you ran those two commands back-to-back, it would still not work because the second command-line is a separate process, where the in-memory sqlite database is again created from scratch.

The solution is to save your `sqlite3.db` file in `/dev/shm` or `/run/shm` on Linux. These are what's known as `tmpfs` file systems on Linux. They act as normal directories, except they are entirely [stored in RAM](http://www.cyberciti.biz/tips/what-is-devshm-and-its-practical-usage.html), which is [about 10,000 times faster](http://stackoverflow.com/questions/1371400/how-much-faster-is-the-memory-usually-than-the-disk) than disk for random access. One notable side-effect is that they are also completely wiped out every time you power down. For Django development, this may be OK. Depending on how good a test fixture you have, you may already be regularly blowing away and re-creating your database.

{% highlight python %}
$ mount
/dev/sda1 on / type ext4 (rw,errors=remount-ro)
...
none on /run/shm type tmpfs (rw,nosuid,nodev)
{% endhighlight %}

These directories are already world-writable. To configure Django to save its database there, you can do the following:

{% highlight python %}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/dev/shm/sqlite3.db',
        'TEST_CHARSET': 'UTF8',
        'TEST_NAME': None  # in-memory sqlite db
    }
}
{% endhighlight %}

On my system, this took a `syncdb` command from to 15 seconds (mostly creating indexes) to 3 seconds flat. The actual app also feels much faster.

For OSX, you can do the same thing, but there is no in-memory file system mounted by default. Instead, you can use the [mount-ram.sh gist](https://gist.github.com/koshigoe/822455). Simply download the gist and run `bash mount-ram.sh /tmp/shm 128` to create a 128MB RAM-backed folder.
