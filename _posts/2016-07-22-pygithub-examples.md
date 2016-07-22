---
layout: post
title: PyGithub Quickstart Examples
---

[PyGithub](https://github.com/PyGithub/PyGithub) is the most popular GitHub API
SDK for Python. Their [documentation](http://pygithub.readthedocs.io/en/stable/introduction.html)
is very light on examples. They [seem to think](https://github.com/PyGithub/PyGithub/issues/321)
this is fine. Prime candidate for the new
[Stack Overflow Documentation](http://stackoverflow.com/tour/documentation) site!

In the meantime, I thought I would share my example code. These took me an hour
of playing with the REPL to figure out.

## Working with Pull Requests

The main challenge here was realizing that I needed to scope everything to
my private org, not my user.

```python
git = PyGithub('GITHUB_TOKEN')
org = git.get_organization('OrgName')
repo = org.get_repo('repo-name')
pr = repo.get_pull(1)
print 'PR author: %s' % pr.user.login
comments = pr.get_issue_comments()
for comment in comments:
  print 'Comment: ', comment.created_at, comment.user.login, comment.body
pr.create_issue_comment('Comment from GITHUB_TOKEN user') # aka git.get_user()
```

## Getting the Contents of a File

From the default branch, not a particular pull request.

```python
git = PyGithub('GITHUB_TOKEN')
org = git.get_organization('OrgName')
repo = org.get_repo('repo-name')
file_contents = repo.get_file_contents('path/to/file')
```

## Listing the Members of a GitHub Team

There is no method to get a team by name, so you need to get them all and
then pick out the one you want.

```python
git = PyGithub('GITHUB_TOKEN')
org = git.get_organization('OrgName')
teams = org.get_teams()
team = [t for t in teams if t.name == 'TeamName'][0]  # assumes a match
print [m.login for m in team.get_members()]
```
