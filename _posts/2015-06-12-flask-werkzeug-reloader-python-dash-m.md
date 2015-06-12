---
layout: post
title: Flask absolute import bug in debug mode
tags: python, flask
---

Ran into a vexing issue this week. I was getting errors trying to use absolute imports in a new flask app:

```bash
Traceback (most recent call last):
  File "nw_api/example/run.py", line 5, in <module>
      from nw_api.docgen.base import DocumentationGenerator
      ImportError: No module named nw_api.docgen.base
```

I was able to use relative imports (i.e. `from docgen import base`), but that's generally considered bad practice. Plus, it was just weird. My unit tests were working with either method, which finally lead me to the offending line:

```python
flask_app.run(debug=True)
```

It turned out that setting `debug=False` fixed the problem. Of course, debug mode is really useful, so I needed to figure out exactly what was going on. That turned up this [werkzeug bug](https://github.com/mitsuhiko/werkzeug/issues/461) titled "Reloader, python -m, and sys.path".

Werkzueg, which provides a lot of Flask functionality (including the [web based debugger](http://werkzeug.pocoo.org/docs/0.10/debug/)), is doing something pretty tricky to implement hot-reloading of the source when you change a Python file. It spawns a subprocess to and loads the code again. However, it does not pass all of the arguments of the original python command line, notably missing the `-m` argument, which is how you get python to run a module versus a single file:

```bash
venv/bin/activate; (cd src && python -m nw_api.example.run)
```

That was the run line from my original Makefile. Instead, I had to go with this:

```bash
venv/bin/activate; (cd src && export PYTHONPATH=${PYTHONPATH}:nw_api && python nw_api/example/run.py)
```

Success! What's going on here is that to avoid using `-m`, you need to update your `PYTHONPATH` environment variable to include the (relative in this case) path to your module. Then you can run any single file in that module and it will pick up absolute imports for the rest.
