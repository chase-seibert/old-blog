---
layout: post
title: Using grep from inside vim
tags: vim
---

> This is my rifle. There are many like it, but this one is mine.  - [Rifleman's Creed](http://en.wikipedia.org/wiki/Rifleman's_Creed)

There are a thousand ways to grep over files. Most developers I have observed keep a separate command line open just for searching. A few use an IDE that has file search built-in. Personally, I use a couple of vim macros.

In vim, you can execute a cross-file search with something like: `:vimgrep /dostuff()/j ../**/*.c`. I don't know about you, but the first time I saw that syntax my brain simply refused.

Instead, I have the following in my .vimrc file:

{% highlight python %}
" opens search results in a window w/ links and highlight the matches
command! -nargs=+ Grep execute 'silent grep! -I -r -n --exclude *.{json,pyc} . -e <args>' | copen | execute 'silent /<args>'
" shift-control-* Greps for the word under the cursor
:nmap <leader>g :Grep <c-r>=expand("<cword>")<cr><cr>
{% endhighlight %}

The first command is just a simple alias for the above mentioned native grep. Like all custom commands, it must start with a capital letter (to differentiate it from native commands). You simply type `:Grep foobar`, and it will search in your current directory through all file extensions (except json and pyc; you can add more to the blacklist).

It also displays the results in a nice little buffer window, which you can navigate through with normal HJKL keys, and open matches in the main editor window.

![vim Grep](/blog/images/vimgrep.png)

The second line is a key mapping that will grep for the word currently under the cursor. You can just navigate to a word and hit `Leader-g` to issue the Grep command.

