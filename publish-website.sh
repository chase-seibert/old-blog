#!/bin/bash
git branch -D gh-pages
git checkout -b gh-pages
git filter-branch --subdirectory-filter _site/ -f
git checkout master
git push --all origin --force
