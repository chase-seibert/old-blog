git branch -D gh-pages
git checkout origin/quickstart -b gh-pages
brew update
brew install ruby rbenv ruby-build
eval "$(rbenv init -)"  # update PATH
echo 'eval "$(rbenv init -)"' >> ~/.bash_profile  # and update PATH in future shells
rbenv install
gem install bundler
bundle install
echo "If you have any problems, you may need to close/open a new terminal to update PATH"
