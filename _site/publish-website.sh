#!/bin/bash
jekyll build
git branch -D gh-pages
git checkout -b gh-pages
git filter-branch --subdirectory-filter _site/ -f
cp -R _site/* .
git add .
git commit -m "new site"
git checkout master
git push --all origin --force
