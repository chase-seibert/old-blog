This blog is hosted on [GitHub Pages](http://pages.github.com/) using [Jekyll](http://jekyllrb.com/). If you want to fork this blog and make your own, here is how you get started.

This is a two-branch system. The `master` branch is where the source code of you blog as well as the post content lives. The `gh-pages` branch is generated from the source branch and contains the actual static files for your site + posts. This is what GitHub will end up hosting for you.

# Clone it

First, you need to fork this repository to your own account. Github looks for a branch called `gh-pages`, so create your blog content there.

```
# fork the repository using the github UI
git clone git@github.com:username/blog.git ~/projects/blog
cd ~/projects/blog
```

You probably also want to remove my posts, and my git history.

```
rm -f _posts/*
rm -rf .git
git init
git add .
git commit -m "Initial commit"
git remote add origin git@github.com:username/blog.git
```

# Install Dependencies

## OSX

```
brew update
brew install ruby rbenv ruby-build
eval "$(rbenv init -)"  # update PATH
echo 'eval "$(rbenv init -)"' >> ~/.bash_profile  # and update PATH in future shells
rbenv install
gem install bundler
bundle install  # may need to re-open shell to get updated PATH
./run.sh
```

# Run it!

This command wraps `bundle exec jekyll serve --watch`, and also launches a web browser. You may need to refresh a couple of times to see the content.

```bash
./run.sh
```

You should now be able to open [http://localhost:4000/blog/index.html](http://localhost:4000/blog/index.html)

# Create a test Post and Publish

Just create new files in _posts in the format `2013-01-01-post-title.md`. Here is a template to get you started:

```
---
layout: post
title: This is my new post
tags: python linux
---

I [cloned this blog](https://github.com/chase-seibert/blog)
```

While you're editing, you can view your [changes live](http://localhost:4000/blog/index.html). When you're done, run `./publish-website.sh` to publish it.

```
git add .
git commit -m "my first blog entry"
./publish-website.sh
```

Your blog should show up on `http://username.github.io/blog`.

* [Markdown syntax guide](http://en.wikipedia.org/wiki/Markdown#Syntax_examples)


# Updating Styling

- The blog title is in `index.html`
- In `_layouts/default.html`, you can change:
    - The Facebook Opengraph meta data
    - The sidebar content w/ my name, sub-title, social media links, resume, etc
- In `_layout/post.html`, you can change:
    - Twitter handle
    - Disqus comment metadata
