---
layout: post
title: Python Subprocess Asynchronous Read Stdout
tags: python subprocess threads
---

Python has a great standard library when it comes to invoking [external processes](http://docs.python.org/2/library/subprocess.html). But one weakness it does have is that it's not easy to communicate with a subprocess while it's running, i.e. streaming its stdout. If you look at the documentation for `popen`, you will repeatedly see caveats like the following from the Python docs for [Popen.communicate](http://docs.python.org/2/library/subprocess.html#subprocess.Popen.communicate):

> Interact with process: Send data to stdin. Read data from stdout and stderr, until end-of-file is reached. **Wait for process to terminate.** The optional input argument should be a string to be sent to the child process, or None, if no data should be sent to the child.

It's actually a well known problem. There is even an open enhancement proposal [PEP 3145](http://www.python.org/dev/peps/pep-3145/) to address it. But that is currently on track for Python 3.2. Python 2.x will never get that update.

Hunting around, I found a pretty decent partial solution on [Stackoverflow](http://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python), but it took me quite a bit to tweaking to get it to work in my case.

{% highlight python %}
import sys
import datetime
import fcntl
import subprocess
from threading import Thread


if __name__ == '__main__':

    mysql_process = subprocess.Popen(
        ['mysql', '--user=%s' % sys.argv[1], '--password=%s' % sys.argv[2], '--batch', '--skip-tee', '--skip-pager', '--unbuffered']
        stdin=sys.stdin,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    thread = Thread(target=log_worker, args=[mysql_process.stdout])
    thread.daemon = True
    thread.start()

    mysql_process.wait()
    thread.join(timeout=1)


def log_worker(stdout):
    ''' needs to be in a thread so we can read the stdout w/o blocking '''
    username, hostname = os.environ.get('USER'), socket.gethostname()
    log_file = '/var/log/mysql-%s.log' % username
    log = open(log_file, 'a')
    while True:
        output = non_block_read(stdout).strip()
        if output:
            ''' [Tue Oct 30 22:13:13 2012 cseibert@host1]> '''
            prompt = '[%(timestamp)s %(username)s@%(host)s]> \n' % dict(
                    timestamp=datetime.datetime.now().strftime('%a %b %d %H:%M:%S %Y'),
                    username=username,
                    host=hostname)
            print prompt + output
            log.write(prompt + output + '\n')
    log.close()


def non_block_read(output):
    ''' even in a thread, a normal read with block until the buffer is full '''
    fd = output.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    try:
        return output.read()
    except:
        return ''
{% endhighlight %}

As you can see, this code is invoking the `mysql` command-line client in batch mode. I'm piping a file into my python script, and then turning around and piping that into mysql. I start the mysql subprocess, but at the same time I'm spinning off a worker thread to read its output. Additionally, I'm re-opening stdout in non-blocking mode, so I don't have to wait for a buffer to fill up before I can read a chunk.

Then I'm reading the mysql output and writing it both to the console, and to a log file. For this application, it's critical that the mysql output be shown on the screen as it's running. What if there's an exception; the user will want to terminate before it runs any further.

Doesn't mysql provide logging by default? Yes, but only for interactive (i.e., non-batch) sessions. From the mysql command-line tool docs:

> By using the --tee option when you invoke mysql, you can log statements and their output. All the data displayed on the screen is appended into a given file. This can be very useful for debugging purposes also. mysql flushes results to the file after each statement, just before it prints its next prompt. **Tee functionality works only in interactive mode.**

One additional caveat; you need to make sure that the subprocess you are invoking is not doing its own buffering. It took me a bit to figure out that mysql does do that, which is what the `--unbuffered` flag is there to disable.
