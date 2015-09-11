---
layout: post
title: Per-OS virtual environments in Python
tags: python
---

A common setup for web development is to have a virtual machine on your Mac running all your code. Typically this involves a shared folder containing the code, so that you can edit the file locally on your Mac, but it's also available to the guest OS to execute. At least with Vagrant and either VirutalBox or VMWare, the performance of the shared folder can quickly become a nuisance.

If you're running a long test suite, you may be sacrificing as much as 40% of the time to the virtualization in my admittedly informal testing. Also vexing is hot reloading code changes in your web app, where you suffer from lag between when a file is changed and when the event bubbles up in the guest OS. I've written about some [mitigation strategies](http://chase-seibert.github.io/blog/2014/03/09/vagrant-cachefilesd.html) before. The upshot is that you may be waiting several seconds longer than necessary before you can refresh your app the see the changes. Those seconds add up when you perform this cycle hundreds of times a day. Git hook performance can also be slower than normal.

What's preventing you from running some or all of these operations on your local Mac? Mainly that all your dependencies only exist inside the virtual machine. With Python code bases, this often translates into the fact that your virtualenv directory has architecture (Linux) specific binary packages inside it.

If you happen to use a `Makefile` to generate your virtualenv and run common commands, you can easily handle this there by creating different virtualenv directories for each environment.

```bash
VENV_DIR=venv
ifeq ($(shell uname),Darwin)
    # allows you to have two venv dirs, one for local osx development (faster)
    VENV_DIR=venv-osx
endif

test:
    @. $(VENV_DIR)/bin/activate; nosetests
```

Just remember to add the new virtualenv directories to your `.gitignore` file.
