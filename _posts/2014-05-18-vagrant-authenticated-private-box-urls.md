---
layout: post
title: Distributing Vagrant base boxes securely
tags: vagrant
---

[Vagrant](http://www.vagrantup.com) is typically used to provide local, uniform and *repeatable* development virtual machines. Repeatable is given little importance in the documentation, but since I've been using vagrant, I've been surprised at just how often I end up destroying and re-creating my boxes.

# Why custom base boxes

Our typical provisioning takes about 30 minutes. Half of that is downloading and installing `apt` dependencies, and half is downloading, compiling (ugh) and installing `pip` dependencies for Python. What's worse, it's not particularly robust; compiling Python libraries will fail approximately 10% of the time. Just enough to be really annoying.

Base boxes to the rescue. The included Ubuntu boxes `precise32` and `precise64` are about 300MB, and contain only the operating system and minimal other dependencies. But you can build your own base box files from a previously configured virtual machine.

# Shrinking images

Running the standard `vagrant package --output /tmp/mydev.box` command creates a base box of 2.5GB in my case. How did we go from 300MB to 2.5GB? It's actually mostly bloat. You can save quite a bit of space by running [this gist](https://gist.githubusercontent.com/adrienbrault/3775253/raw/da59136ef0414af151b917bd25a06882f0107947/purge.sh) inside your VM *before* you package it.

In my case, this trimmed it down to 800MB.

# Do you want your dev image public?

In our case, we didn't want to make this image publicly available. Although the box does not have actual code on it (it's loaded later via NFS), it *does* have development API keys/passwords. Why? A while back we removed these from the github repo and moved them into `/etc` config files. Besides, I'm not sure we want to make anything about our service config public, either.

This is a problem because Vagrant assumes your `box_url` is going to be using HTTP/HTTPS. It does support Basic Authentication, but that's hardly secure.

# What about Vagrant cloud?

Vagrant is starting a service called [Vagrant Cloud](https://vagrantcloud.com/) aimed precisely at this use case. However, it's in early beta, and doesn't support actually hosting files at this stage. You need to upload your box somewhere else and give them a URL, so you're back to square one.

# Plugins

I could not find a vagrant plugin for my use case, either. There is an interesting [vagrant-fog-box-storage](https://github.com/natlownes/vagrant-fog-box-storage) plugin that allows you to download a box image off S3. However, it doesn't work with Vagrant versions past 1.1. Plus, I'm pretty sure I don't want to include AWS access tokens in my Vagrantfile.

I'm also *very* sure I don't want to write by own plugin in ruby.

# Vagrant actually uses cURL

While searching around, I randomly ran into the vagrant [download code](https://github.com/mitchellh/vagrant/blob/master/lib/vagrant/util/downloader.rb), where I quickly realized they were using cURL to do the actual download. Great! A little known feature of cURL is that it supports many different protocols: `dict file ftp ftps gopher http https imap imaps ldap ldaps pop3 pop3s rtsp scp sftp smtp smtps telnet tftp`.

This actually turns out to be a [concious decision](https://github.com/mitchellh/vagrant/pull/1041) to support scp. All you have to do is use a scp URL like `scp://my-server:/tmp/dev.box`.

# cURL doesn't have this option by default in OSX

One big problem. Our development machines are all Apples, and the `curl` command built-in to OSX Mavericks is not compiled with the scp option. So we turn to homebrew.

{% highlight bash %}
brew install curl --with-ssh
brew link curl --force
{% endhighlight %}

**Note: This will over-ride the built-in curl, which is fairly dangerous. If the arguments don't match something another app on your system is expecting, things could very well break. [Learn more.](http://stackoverflow.com/questions/4691403/keg-only-homebrew-formulas)**

# Example vagrant file

Using a scp URL in your `Vagrantfile` is simple:

{% highlight ruby %}
# -*- mode: ruby -*-
Vagrant.configure("2") do |config|
  config.vm.hostname = "dev-vagrant"
  config.vm.box = "dev"
  config.vm.box_url = "scp://my-server:/tmp/dev.box"
end
{% endhighlight %}

# Future Work

Ideally, Vagrant itself would optionally call `scp` directly to side-step the OSX issue. It would also be ideal if they supported S3 directly, as well. In fact, just let us write our own shell command/script to download the file.
