---
layout: post
title: New Year Python Meme 2012
tags: python pythonmeme
---

View all [#2012pythonmeme](https://twitter.com/search?q=%232012pythonmeme) posts by the community.

**1. What's the coolest Python application, framework, or library you have discovered in 2012?**

Definitely [celery](https://github.com/celery/celery). It challenges you to compose your solutions into ever smaller tasks. It's sometimes frustrating as hell to debug (mostly because it's naturally UI-less). But it has been an absolutely essential piece of several large projects in the last year.

**2. What new programming technique did you learn in 2012?**

[Monkey patching](http://stackoverflow.com/questions/5626193/what-is-monkey-patching). After a couple years of using Python as if it was Java, I finally started to grok the power of a dynamic language in 2012. I then proceeded to perhaps over-use it, by [over-writing python internals](https://github.com/chase-seibert/django-nose-lint/blob/master/noselint/__init__.py), reaching into [framework internals](http://chase-seibert.github.com/blog/2012/06/05/django-nosesqlite3-too-many-sql-variables-error.html), replacing [code in memory at runtime](http://chase-seibert.github.com/blog/2012/12/21/read-only-django-shell.html) and [fabricating look-alike objects](http://chase-seibert.github.com/blog/2012/07/27/faster-django-view-unit-tests-with-mocks.html).

**3. Which open source project did you contribute to the most in 2012? What did you do?**

I had a couple of [patches](https://github.com/celery/celery/issues/447) for celery and encouraged a co-worker to [contribute back](https://code.djangoproject.com/ticket/19385) to Django. But mostly I open-sourced a couple of new things I was working on, [django-pyfixtures](https://github.com/chase-seibert/django-pyfixtures) and [django-nose-lint](https://github.com/chase-seibert/django-nose-lint).

**4. Which Python blog or website did you read the most in 2012?**

In terms of volume, it was the Reddit's [r/python](http://www.reddit.com/r/Python/). But in terms of value, it would have to be [my twitter steam](https://twitter.com/chase_seibert/following).

**5. What are the top things you want to learn in 2013?**

I need to re-engage on client side technologies, which have made tremendous progress in the last couple of years while I've been focussed on server-side stuff. I'm particularly interesting in actually using stuff like [backbone](http://backbonejs.org/), [node.js](http://nodejs.org/) and [meteorjs](http://meteor.com/) in production.

**6. What is the top software, application, or library you wish someone would write in 2013?**

An open-source replacement for [Splunk](http://www.splunk.com/). I've rarely used a product so well designed and functional. Yet I can't deal with the high cost and licensing headaches anymore.
