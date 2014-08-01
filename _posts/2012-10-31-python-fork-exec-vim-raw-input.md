---
layout: post
title: Using $EDITOR and a less paging from Python command line apps
tags: python git
---

Python's built-in [raw_input()](http://docs.python.org/2/library/functions.html#raw_input) function is a quick and dirty way to get text input from the user in your Python command line application. But it's really only optimal for a very small input string. Also, it can't provide a default value that the user can then edit. For more substantial input, many Linux tools use your $EDITOR environment variable to launch a visual editor, potentially with default text.

Some example are [git](http://git-scm.com/) commit messages, and `crontab -e`. A typical workflow is as follows:

1. User runs a command like `git commit`.
2. Git creates a temp file with a default commit template
2. Vim, emacs or nano opens the temp file
3. User edits the text
4. User saves and quits
5. Git reads in the new contents of the temp file, and deletes it

After [some research](http://stackoverflow.com/questions/13168083/python-raw-input-replacement-that-uses-a-configurable-text-editor), I came up with the following helper to do just that in Python:

{% highlight python %}
import tempfile
import subprocess
import os

def raw_input_editor(default=None, editor=None):
    ''' like the built-in raw_input(), except that it uses a visual
    text editor for ease of editing. Unline raw_input() it can also
    take a default value. '''
    with tempfile.NamedTemporaryFile(mode='r+') as tmpfile:
        if default:
            tmpfile.write(default)
            tmpfile.flush()
        subprocess.check_call([editor or get_editor(), tmpfile.name])
        tmpfile.seek(0)
        return tmpfile.read().strip()

def get_editor():
    return (os.environ.get('VISUAL')
        or os.environ.get('EDITOR')
        or 'vi')
{% endhighlight %}

# Using less as a pager

With that turning out nicely, I decided to also try to copy git's pager. When you run a command like `git log` that can produce thousands of lines of text, it passes the content through `less`, which breaks it into scrollable pages. If you abstract your print statements into a logger or a custom function, you can easily enable/disable the pager.

{% highlight python %}
import subprocess
import sys

try:
    # args stolen fron git source, see `man less`
    pager = subprocess.Popen(['less', '-F', '-R', '-S', '-X', '-K'], stdin=subprocess.PIPE, stdout=sys.stdout)
    for num in range(1000):
        pager.write('This is output line %s\n' % num)
    pager.stdin.close()
    pager.wait()
except KeyboardInterrupt:
    # let less handle this, -K will exit cleanly
{% endhighlight %}

# Terminal Colors

Finally, adding some color to your console text is easy with the [termcolor](http://pypi.python.org/pypi/termcolor/) library.

![Color terminal text example](/blog/images/termcolor.jpeg)
