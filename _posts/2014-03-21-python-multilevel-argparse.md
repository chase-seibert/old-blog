---
layout: post
title: Multi-level argparse in Python (parsing commands like git)
tags: python
---

It's a common pattern for command line tools to have multiple subcommands that run off of a single executable. For example, `git fetch origin` and `git commit --amend` both use the same executable `/usr/bin/git` to run. Each subcommand has its own set of required and optional parameters.

This pattern is fairly easy to implement in your own Python command-line utilities using [argparse](http://docs.python.org/3.4/library/argparse.html). Here is a script that pretends to be git and provides the above two commands and arguments.

{% highlight python %}
#!/usr/bin/env python

import argparse
import sys


class FakeGit(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Pretends to be git',
            usage='''git <command> [<args>]

The most commonly used git commands are:
   commit     Record changes to the repository
   fetch      Download objects and refs from another repository
''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print 'Unrecognized command'
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def commit(self):
        parser = argparse.ArgumentParser(
            description='Record changes to the repository')
        # prefixing the argument with -- means it's optional
        parser.add_argument('--amend', action='store_true')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(sys.argv[2:])
        print 'Running git commit, amend=%s' % args.amend

    def fetch(self):
        parser = argparse.ArgumentParser(
            description='Download objects and refs from another repository')
        # NOT prefixing the argument with -- means it's not optional
        parser.add_argument('repository')
        args = parser.parse_args(sys.argv[2:])
        print 'Running git fetch, repository=%s' % args.repository


if __name__ == '__main__':
    FakeGit()
{% endhighlight %}

The argparse library gives you all kinds of great stuff. You can run `./git.py --help` and get the following:

{% highlight bash %}
usage: git <command> [<args>]

The most commonly used git commands are:
   commit     Record changes to the repository
   fetch      Download objects and refs from another repository

Pretends to be git

positional arguments:
  command     Subcommand to run

optional arguments:
  -h, --help  show this help message and exit
{% endhighlight %}

You can get help on a particular subcommand with `./git.py commit --help`.

{% highlight bash %}
usage: git.py [-h] [--amend]

Record changes to the repository

optional arguments:
  -h, --help  show this help message and exit
  --amend
{% endhighlight %}

Want bash completion on your awesome new command line utlity? Try [argcomplete](https://github.com/kislyuk/argcomplete), a drop in bash completion for Python + argparse.
