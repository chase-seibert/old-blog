This blog is hosted on [GitHub Pages](http://pages.github.com/) using [Jekyll](http://jekyllrb.com/). If you want to fork this blog and make your own, here is how you get started.

# Clone it

First, you need to fork this repository to your own account. Github looks for a branch called `gh-pages`, so create your blog content there.

```
# fork the repository using the github UI
git clone git@github.com:username/blog.git ~/projects/blog
cd ~/projects/blog
git checkout gh-pages
```

You probably also want to remove my posts, and my git history.

```
rm -f _posts/*
rm -rf .git
git init
git checkout gh-pages
git add .
git commit -m "Initial commit"
git remote add origin git@github.com:username/blog.git
git push -u --force origin master
```

# Install Dependencies

## Linux

```
sudo apt-get install ruby1.9.1-dev python-pygments
sudo gem update --system
sudo gem install jekyll
```

## OSX

```
brew update
brew install ruby rbenv ruby-build
eval "$(rbenv init -)"  # update PATH
echo 'eval "$(rbenv init -)"' >> ~/.bash_profile  # and update PATH in future shells
rbenv install
gem install bundler
bundle install  # may need to re-open shell to get updated PATH
bundle exec jekyll serve
```

# Run it!

```bash
bundle exec jekyll serve --watch
```

You should now be able to open [http://localhost:4000/blog/index.html](http://localhost:4000/blog/index.html)

# Publish

Just create new files in _posts in the format `2013-01-01-post-title.md`. Here is a template to get you started:

```
---
layout: post
title: This is my new post
tags: python, linux
---

I [cloned this blog](https://github.com/chase-seibert/blog)
```

While you're editing, you can view your [changes live](http://localhost:4000/blog/index.html). When you're done, just push as normal.

```
git add .
git commit -m "my first blog entry"
git push origin gh-pages
```

Your blog should show up on `http://username.github.io/blog`.

* [Markdown syntax guide](http://en.wikipedia.org/wiki/Markdown#Syntax_examples)
