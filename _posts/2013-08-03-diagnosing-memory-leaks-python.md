---
layout: post
title: Diagnosing Memory "Leaks" in Python
tags: python
---

## The Problem

We wrote some new code in the form of [celery](https://github.com/celery/celery) tasks that we expected to run for up to five minutes, and use a few hundred megabytes of memory. Rinse and repeat for a thousand different data sets. We ran through a few data sets successfully, but once we started running though ALL of them, we noticed that the memory of the celery process was continuing to grow.

In celery, each task runs in one of a fixed number of processes that persist between tasks. We assumed we had a memory leak on our hands; somehow we were leaving references around to our data structures that were remaining in memory and not being garbage collected between tasks. But how do you go about investigating exactly what is happening?

**Note:** Stop everything, and make sure that you're not in `DEBUG` mode, assuming you're using Django. In that mode, every database query you make will be stored in memory, which [looks a lot like a memory leak](https://docs.djangoproject.com/en/dev/faq/models/#why-is-django-leaking-memory).

## Linux Utilities

The command line utilities [top](http://linux.about.com/od/commands/l/blcmdl1_top.htm) or the more pleasing [htop](http://htop.sourceforge.net/) should be your first stop for any CPU or memory load investigation. In our case, we had observed that the machine would run out of memory and start paging while running our tasks. So we kicked them off again, and watched the processes in htop. Indeed, the processes grew from their initial size of 100MB, slowly, all the way up to 1GB before we killed them. We could see from the logs that any individual tasks were being completed successfully along the way.

We were able to reproduce the behavior in our development environment, though we only had enough data for the process to balloon to a few hundred megabytes. Once we had the behavior reproducible in a script that could be run on it's own outside of celery (using `CELERY_ALWAYS_EAGER`), we could using the GNU `time` command to track peak memory usage, ie `/usr/bin/time -v myscript.py`.

**Note:** we're specifying the full path to time so that we get the GNU time command, and not the one built into bash.

**Note:** there is a bug in some versions of the utility that [mis-reports memory usage](https://bugzilla.redhat.com/show_bug.cgi?id=702826) by multiplying it by a factor of four. Double-check using top.

## Resource Module

You can actually get the amount of memory your process is using from inside your Python process, using the resource module.

{% highlight python %}
import resource
print 'Memory usage: %s (kb)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
{% endhighlight %}

This can be useful for adding logging statements to your code to measure memory usage over time, or at critical junctures of a long-running process. This can help you isolate the critical section of your code that's causing the memory issue.

## Objgraph

Once you have identified a spot in your code just after the memory issue has occurred, you can query for the objects currently in memory right from Python, as well. You will probably need to do a `pip install objgraph` first.

{% highlight python %}
import gc
gc.collect()  # don't care about stuff that would be garbage collected properly
import objgraph
objgraph.show_most_common_types()
tuple                      5224
function                   1329
wrapper_descriptor         967
dict                       790
builtin_function_or_method 658
method_descriptor          340
weakref                    322
list                       168
member_descriptor          167
type                       163
{% endhighlight %}

## Heapy

Maybe you'll get lucky and see a custom class that you've defined at the top of the list. But if not, what exactly is in those generic type buckets? Enter [guppy](http://guppy-pe.sourceforge.net/), which is like `show_most_common_types` on steroids. Again, you will likely need to install this via `pip install guppy`. The great thing about guppy/heapy is that you can take a snapshot of the heap before your critical section and after, and diff them, just getting the objects that were added to the heap in between.

{% highlight python %}
from guppy import hpy
hp = hpy()
before = hp.heap()

# critical section here

after = hp.heap()
leftover = after - before
import pdb; pdb.set_trace()
{% endhighlight %}

You probably want a [pdb](http://docs.python.org/2/library/pdb.html) session here, so you can interactively investigate the heap diff. The best heapy tutorial I have found is [How to use guppy/heapy for tracking down memory usage](http://www.smira.ru/wp-content/uploads/2011/08/heapy.html).

{% highlight python %}
>leftover
Partition of a set of 134243 objects. Total size = 65671752 bytes.
 Index  Count   %     Size   % Cumulative  % Kind (class / dict of class)
     0  16081  12 45332744  69  45332744  69 unicode
     1  18714  14  5493360   8  50826104  77 dict (no owner)
     2  47441  35  3925672   6  54751776  83 str
     3  21300  16  1786080   3  56537856  86 tuple
     4    344   0   820544   1  57358400  87 dict of module
     5    654   0   685392   1  58043792  88 dict of django.db.models.related.RelatedObject
     6   5543   4   665160   1  58708952  89 function
     7    708   1   640992   1  59349944  90 type
     8   4946   4   633088   1  59983032  91 types.CodeType
     9    705   1   442776   1  60425808  92 dict of type

>leftover.byrcs[0].byid
Set of 16081 <unicode> objects. Total size = 45332744 bytes.
 Index     Size   %   Cumulative  %   Representation (limited)
     0       80   0.0        80   0.0 'media-plugin...re20051219-r1'
     1       76   0.0       156   0.0 'app-emulatio...4.20041102-r1'
     2       76   0.0       232   0.0 'dev-php5/ezc...hemaTiein-1.0'
     3       76   0.0       308   0.0 'games-misc/f...wski-20030120'
     4       76   0.0       384   0.0 'mail-client/...pt-viewer-0.8'
     5       76   0.0       460   0.0 'media-fonts/...-100dpi-1.0.0'
     6       76   0.0       536   0.0 'media-plugin...gdemux-0.10.4'
     7       76   0.0       612   0.0 'media-plugin...3_pre20051219'
     8       76   0.0       688   0.0 'media-plugin...3_pre20051219'
     9       76   0.0       764   0.0 'media-plugin...3_pre20060502
{% endhighlight %}

**Note:** memory dumps have been fabricated to protect the innocent.

## GDB

An interesting thing happened when we were using heapy. We noticed that heapy was only reporting 128MB of objects in memory, where as the resource module and top agreed that there was almost 1GB being used.

To get an idea of what was comprising the remaining 800+ MBs, we turned to gdb, specifically to a python helper called [gdb-heap](https://github.com/rogerhu/gdb-heap).

{% highlight python %}
sudo apt-get install libc6-dev
sudo apt-get install libc6-dbg
sudo apt-get install python-gi
sudo apt-get install libglib2.0-dev
sudo apt-get install python-ply

# assuming 7458 is the PID of your memory hogging python process
sudo gdb -p 7458
>generate-core-file

# this will save a .core file, which you can then examine in gdb
sudo gdb python myfile.core -x ~/gdb-heap-commands
{% endhighlight %}

In our case, what we saw was mostly indecipherable. But there seemed to be a ton of tiny little objects around, like integers.

## Explanation

Long running Python jobs that consume a lot of memory while running may not return that memory to the operating system until the process actually terminates, even if everything is garbage collected properly. That was news to me, but it's true. What this means is that processes that do need to use a lot of memory will exhibit a "high water" behavior, where they remain forever at the level of memory usage that they required at their peak.

**Note:** this behavior may be Linux specific; there are anecdotal reports that Python on Windows does not have this problem.

This problem arises from the fact that the Python VM does its own internal memory management. It's commonly know as [memory fragmentation](http://revista.python.org.ar/2/en/html/memory-fragmentation.html). Unfortunately, there doesn't seem to be any fool-proof method of avoiding it.

Celery tends to bring out this behavior for a lot of users.

> AFAIK this is just how Python works. I would guess that the operating system will reuse the memory anyway, since it can just swap it out if it's not used.  If you have allocated a chunk of memory, there's a big chance that you will need it again, and it's better to delegate memory management to the operating system.
> ... There is no solution - that I know of - to make Python release the memory ... [Ask Solem, author of celery](https://groups.google.com/forum/#!topic/celery-users/jVc3I3kPtlw)


## Workarounds

For celery in particular, you can roll the celery worker processes regularly. This is exactly what the `CELERYD_MAX_TASKS_PER_CHILD` setting does. However, you may end up having to roll the workers so often that you incur an undesirable performance overhead.

For non-celery systems, you can use the `multiprocessing` module to run any function in a separate process. There is a simple looking gist called [processify](https://gist.github.com/schlamar/2311116) that does just that.

**Note:** This may have the undesirable effect of using more shared resources, like database connections.

You could also run your Python jobs using Jython, which uses the Java JVM and does not exhibit this behavior. Likewise, you could [upgrade to Python 3.3](http://bugs.python.org/issue11849),

Ultimately, the best solution is to simply use less memory. In our case, we ended up breaking the work into smaller chunks (individual days). For some tasks, this may not be possible, or may require complicated task coordination.
