---
layout: post
title: The Post/Redirect/Get (PRG) Pattern
tags: django, view, prg
---

[Mylyn](http://www.eclipse.org/mylyn/) is a "task lifecycle management framework" plugin for Eclipse. I'm not 100% sure what that means, but I know I really liked one particular feature. On teams where everything you worked on was a JIRA ticket, Mylyn let you associate source code files with a particular JIRA ticket. You would tell it that you were woring on ticket X, and it would keep track of which files you had open. If you started working on task X again at a later date, it could open all those same files again.

I've stopped using Eclipse and even JIRA since, but it seems like a workflow that's worth mapping over to my current editor and task groupings, namely vim and git branches. Vim has an excellent built-in "sessions" functionality, though the [mksession](http://vim.runpaint.org/editing/managing-sessions/) command. I wanted to be able to bind some keys to save the current session against the current git branch by name, and be able to restore a session for the current branch.

Here is a vimrc snippet that does just that.

{% highlight bash %}
{% endhighlight %}
