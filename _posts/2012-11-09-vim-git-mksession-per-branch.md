---
layout: post
title: Keep Track of Vim Tabs Per Git Branch
tags: django view prg
---

[Mylyn](http://www.eclipse.org/mylyn/) is a "task lifecycle management framework" plugin for Eclipse. I'm not 100% sure what that means, but I know I really liked one particular feature. On teams where everything you worked on was a JIRA ticket, Mylyn let you associate source code files with a particular JIRA ticket. You would tell it that you were woring on ticket X, and it would keep track of which files you had open. If you started working on task X again at a later date, it could open all those same files again.

I've stopped using Eclipse and even JIRA since, but it seems like a workflow that's worth mapping over to my current editor and task groupings, namely vim and git branches. Vim has an excellent built-in "sessions" functionality, through the [mksession](http://vim.runpaint.org/editing/managing-sessions/) command. I wanted to be able to bind some keys to save the current session against the current git branch by name, and be able to restore a session for the current branch.

Here is a vimrc snippet that does just that.

{% highlight bash %}
let s:sessions_dir = "~/.vim/sessions/"

function! GetCurrentGitBranch()
    return system("git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* //'")
endfunction

function! GetWorkingDirectory()
    redir => current_dir
    silent pwd
    redir END
    return current_dir
endfunction

function! GetSessionFile()
    let branch = GetCurrentGitBranch()
    if branch == ""
        echo "No git repository at " . GetWorkingDirectory()
    else
        return s:sessions_dir . GetCurrentGitBranch()
    endif
    return ""
endfunction

function! GitSessionSave()
    let session_file = GetSessionFile()
    if session_file != ""
        execute "mksession! " . session_file
        echo "Saved session to " . session_file
    endif
endfunction

function! GitSessionRestore()
    let session_file = GetSessionFile()
    if session_file != ""
        execute "tabo"
        execute "source " . session_file
        echo "Restored session " . session_file
    endif
endfunction

command! Gss call GitSessionSave()
command! Gsr call GitSessionRestore()
{% endhighlight %}
