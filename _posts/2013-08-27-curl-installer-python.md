---
layout: post
title: Writing a cURL to Python Install Script for a Django development environment
tags: python
---

### Paste and Pray

It's pretty common to Google a technical issue, and come up with a blog or a Stackoverflow article that promises to fix the issue by copying and pasting a simple one-liner into a terminal. At first it's just a quick `chmod`, or a simple `apt-get`. It's completely unsafe unless you know exactly what the command is doing, but it's pretty damn effective. Then you graduate to doing few lines at a time without really thinking about it too much, like a bad drug habit. Repitiion slowly convinces you that it's not insane.

In the last couple of years, I've seen a few extreme versions of this same idea, but taken to the next level. Homebrew can be installed by running `ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"`. Heroku Toolbelt for Linux is just a `wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh` away. I call these __Paste and Pray__ installers.

Sounds like fun, right? I thought so, so I came up with a version that installs a pretty vanilla Django development environment, _from scratch_. It doesn't assume anything except cURL and Python, both of which come pre-installed on OSX and Ubuntu. It does a fully automated install of Homebrew (including its dependecy XCode on OSX), as well as pip, virtualenv, your code from GitHub, Django and any other Python requirements you have. It also sets some environment variables and updates your hosts file.

Oh, did I mention that some of these steps require root access? That's right! It's more like __Super Paste and Pray__&trade;.

_Note:_ this code is not intended to be directly re-usable. Instead, I thought I would share what I learned while writing it.

### The Code

You can view the [code and documentaion](https://github.com/chase-seibert/devlocal-setup). The code itself can be run with `curl -fsS https://raw.github.com/chase-seibert/devlocal-setup/go/run.py |sudo -E python`, though it won't be useful for most people as it requires read access to a private GitHub repo. But you should be able to modify it pretty easily for any Django app.

### Sh Stuff
stdout
raw input w/ tty
sudo wrap vs. with statement
except sh.ErrorReturnCode as e:
### Sudo Madness
don't use setuid, may need to change back (Homebrew + install)
    instead, bake sudo -u
    verbose output, _out, etc
    SUDO_USER
env variables, -E, can't pass command line args like normal
### OSX Stuff
xcode direct downloads
installing a dmg via the console
xdg-open
### Python Stuff
dynamically loading stuff
    why sh - brew list -1, parse
    grep(cat)
virtualenv activate_this versus source
