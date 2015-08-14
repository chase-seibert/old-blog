---
layout: post
title: Getting Started with Sphinx docs
tags: python
---

Everyone knows that you should write documentation for your code. Writing documentation actually is not that hard. Like any type of writing, the hardest part is beginning. So how do you begin writing documentation for your Python projects?

# Enter Sphinx

[Sphinx](http://sphinx-doc.org/) is the de-facto standard in the Python community for generating documentation for your projects. It's simple to create HTML/PDF files with code samples, tables of contents, and built in search. Many popular projects host their Sphinx docs on [readthedocs.org](https://readthedocs.org/). A couple of good examples are [celery](http://celery.readthedocs.org/en/latest/getting-started/first-steps-with-celery.html#application) and [flask](http://flask.readthedocs.org/en/latest/quickstart/).

One of the key feature of Sphinx is that it allows you to generate as much of the documentation as possible from comments in your Python code. It can also automatically pull the signatures of your modules, classes, functions and methods. Together, these features allow you to keep most of your documentation up to date automatically. Of course, you will also want to write higher level pages on specific topics, and you can easily define those in either [Markdown](http://daringfireball.net/projects/markdown/) or [reStructuredText](http://docutils.sourceforge.net/rst.html), both of which render as rich text when viewed directly in your GitHub repository.


# Quickstart

First, you need to install Sphinx. Then you run their quickstart command, which prompts you for configuration options. You're pretty safe use the defaults in most cases. **The only sphinx-quickstart options I typically customize are enabling autodoc and using "docs" as the project root.**

Here are the basic console commands. You would run these from inside your project root.

```bash
sudo pip install sphinx
sphinx-quickstart
cd docs
make html
open _build/html/index.html
```

This will be sufficient to get a basic HTML document. Typically my next steps will be to integrated with my project README, and configure autodoc to find my code.

# Update your README

I usually have my READMEs defined in Markdown, but for the purposes of Sphinx I think it's worth it to switch to reStructuredText, simply so that you can include the README as the first page of your docs. reStructuredText is pretty simple, here is a quick example of a `README.rst` to get you started.

```bash
===========================================
 IPython: Productive Interactive Computing
===========================================

Overview
========

Welcome to IPython.  Our full documentation is available on `our website
<http://ipython.org/documentation.html>`_; if you downloaded a built source
distribution the ``docs/source`` directory contains the plaintext version of
these manuals.  If you have Sphinx installed, you can build them by typing
``cd docs; make html`` for local browsing.

Instant running
===============

You can run IPython from this directory without even installing it system-wide
by typing at the terminal::

   python -m IPython
```

This example illustrates how to format titles, subtitles, links, inline code and code blocks.

# Include the README.rst in your docs

Edit your `docs/index.rst` file to include the README:

```bash
.. include:: ../README.rst
```

If that's all that's in your index file, and you run `make html` again, you should see your README contents.

# Break out into more than one file

Next, we will start breaking out our documentation into multiples files. Simply create a new reStructuredText file along side `index.rst`. You can call it anything, for example `example.rst`. You can then include this file in your index like so:

```bash
.. include:: ../README.rst

Read More
---------

.. toctree::
   :maxdepth: 2

   example
```

This tells Sphinx to render your README, followed by a subtitle of "Read More", followed by a list of other documents, one of which is your external `example.rst` file.


# Start using autodoc

In that `example.rst`, you could put the following.

```bash
Some Examples
=============

Here are some examples to get you started.

.. automodule:: src.examples
    :members:
```

This will look at your code in `src/examples.py` for classes, functions and methods. Each one will be listed in this section of the docs, along with any docstrings that where present. See the following example. All of these sections in the text are optional.

```python
def public_fn_with_sphinxy_docstring(name, state=None):
    """This function does something.

    write as much as you want here

    here is a code sample:

    >>> from example import public_fn_with_sphinxy_docstring
    >>> public_fn_with_sphinxy_docstring(
    ...     'foobar',
    ...     'pending')
    0

    :param name: The name to use.
    :type name: str.
    :param state: Current state to be in.
    :type state: bool.
    :returns:  int -- the return code.
    :raises: AttributeError, KeyError
    """
    return 0
```

# Automating Doc Generation

If you use Jenkins for your continuous integration system, you can use the [HTML Publisher Plugin](https://wiki.jenkins-ci.org/display/JENKINS/HTML+Publisher+Plugin) to automatically build the documentation every time you merge. It will also host the HTML for you, right in Jenkins.

# References

- [Sphinx Basics](https://pythonhosted.org/an_example_pypi_project/sphinx.html) - Good listing of basic reStructuredText syntax for Spinx
