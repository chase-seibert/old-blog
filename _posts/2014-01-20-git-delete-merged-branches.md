---
layout: post
title: Python script to delete merged git branches
tags: git python
---

One of the great things about git is how fast it is. You can create a new branch, or switch to another branch, almost as fast as you can type the command. This tends to lower the impedance of branching. As a result, many individuals and teams will naturally converge on a process where they create many, many branches.

If you're like me, you may have 30 branches at any given time. This can make viewing all the branches unwieldy. Once I week or so, I would go on a branch deletion spree by manually copying and pasting multiple branch names into a `git branch -D` statement.

The basic use case is that you want to delete any branches that are already merged into master. Here is a python script that automated just that.

{% highlight python %}
from subprocess import check_output
import sys


def get_merged_branches():
    ''' a list of merged branches, not couting the current branch or master '''
    raw_results = check_output('git branch --merged upstream/master', shell=True)
    return [b.strip() for b in raw_results.split('\n')
        if b.strip() and not b.startswith('*') and b.strip() != 'master']


def delete_branch(branch):
    return check_output('git branch -D %s' % branch, shell=True).strip()


if __name__ == '__main__':
    dry_run = '--confirm' not in sys.argv
    for branch in get_merged_branches():
        if dry_run:
            print branch
        else:
            print delete_branch(branch)
    if dry_run:
        print '*****************************************************************'
        print 'Did not actually delete anything yet, pass in --confirm to delete'
        print '*****************************************************************'
{% endhighlight %}

To print the branches that would be deleted, just execute `python delete_merged_branches.py`. To actually delete the branches, execute `python delete_merged_branches.py --confirm`.
