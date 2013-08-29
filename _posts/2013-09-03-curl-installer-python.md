---
layout: post
title: Writing a cURL to Python Install Script for a Django development environment
tags: python
---

### Paste and Pray

It's pretty common to Google a technical issue, and come up with a blog or a Stackoverflow article that promises to fix the issue by copying and pasting a simple one-liner into a terminal. At first it's just a quick `chmod`, or a simple `apt-get`. It's completely unsafe unless you know exactly what the command is doing, but it's pretty damn effective. Then you graduate to doing few lines at a time without really thinking about it too much, like a bad drug habit. Repetition slowly convinces you that it's not insane.

In the last couple of years, I've seen a few extreme versions of this same idea, but taken to the next level. Homebrew can be installed by running `ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"`. Heroku Toolbelt for Linux is just a `wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh` away. I call these __Paste and Pray__ installers.

Sounds like fun, right? I thought so, so I came up with a version that installs a pretty vanilla Django development environment, _from scratch_. It doesn't assume anything except cURL and Python, both of which come pre-installed on OSX and Ubuntu. It does a fully automated install of Homebrew (including its dependency XCode on OSX), as well as pip, virtualenv, your code from GitHub, Django and any other Python requirements you have. It also sets some environment variables and updates your hosts file.

Oh, did I mention that some of these steps require root access? That's right! It's more like __Super Paste and Pray__&trade;.

_Note:_ this code is not intended to be directly re-usable. Instead, I thought I would share what I learned while writing it.

### The Code

You can view the [code and documentation](https://github.com/chase-seibert/paste-and-pray). The code itself can be run with `curl -fsS https://raw.github.com/chase-seibert/paste-and-pray/go/run.py |sudo -E python`. You should be able to modify it pretty easily for any Django app.

### Sh Stuff

Although I didn't want any dependencies required for the installer itself, I did want to take this chance to play around with [sh](https://github.com/amoffat/sh), a nice Python API for interfacing with the shell. Because I could not rely on pip to be installed, I just downloaded this dependency right in Python:

{% highlight python %}
urllib.urlretrieve("https://raw.github.com/amoffat/sh/master/sh.py", "sh.py")
sh = imp.load_source("sh", "sh.py")
{% endhighlight %}

Working with `sh` turned out to be a little trickier than I imagined. First off, many of my commands required root access. The easiest method was to start the script with `sudo`, and wrap any steps that did __not__ require root in a `sudo -E -u username` prefix. This is exactly what [sh.bake](http://amoffat.github.io/sh/#baking) is for.

I found it useful to redirect `_out` to `sys.stdout` for trouble-shooting purposes. Similarly, if you need to take user input, you will need to redirect stdin with something like:

{% highlight python %}
def raw_input_tty(name, prompt):
    ''' the main use case for this script has the user piping in the results from
    a curl; which over-rides stdin. But we also want to interactively prompt the user
    for some input, so dynamcially switch back to tty. '''
    sys.stdin = open('/dev/tty')
    return raw_input(prompt)
{% endhighlight %}

### Sudo Madness

Initially, I had tried calling [setuid](http://docs.python.org/2/library/os.html#os.setuid) to downgrade to a non-root user. But, I was not able to go back to root, meaning that you would need to do all the root steps in one chunk, then do all the non-root stuff. This was a show-stopper as the Homebrew install step must be run as a regular user, but subsequent `pip` and `virtualenv` tool installs required root.

Another wrinkle was getting the original username from inside sudo. This was simple, thought I did need to hunt around before I discovered that both OSX and Linux set a `SUDO_USER` environment variable for just this purpose.

### OSX Stuff

Installing Homebrew manually is straight-forward, but does require the XCode command line tools to be installed first. Normally, this is a headache as you have to create an Apple ID and hunt and peck trough their developer website for a binary installer.

It turns out there there __are__ direct download links, they just are not publicised. Here is some python code to download and install the correct version.

{% highlight python %}
def install_xcode(osx_version):
    # see: https://devimages.apple.com.edgekey.net/downloads/xcode/simulators/index-3905972D-B609-49CE-8D06-51ADC78E07BC.dvtdownloadableindex
    downloads = {
        10.7: "http://devimages.apple.com/downloads/xcode/command_line_tools_for_xcode_os_x_lion_april_2013.dmg",
        10.8: "http://devimages.apple.com/downloads/xcode/command_line_tools_for_xcode_os_x_mountain_lion_april_2013.dmg",
    }
    if osx_version not in downloads:
        raise NotImplementedError("Could not locate XCode download for OSX %s" % osx_version)
    download_file = downloads.get(osx_version)
    # save this OUTSIDE the normal tmp dir; in case we need to restart install
    dmg_file = "/tmp/xcode.dmg"
    if not os.path.exists(dmg_file):
        urllib.urlretrieve(download_file, dmg_file)
    volume_dir = "/tmp/xcode"
    if not os.path.exists(volume_dir):
        sh.hdiutil("attach", "-mountpoint", volume_dir, dmg_file)
    mpkg_file = [f for f in os.listdir(volume_dir) if f.endswith(".mpkg")][0]
    try:
        sh.installer("-pkg", os.path.join(volume_dir, mpkg_file), "-target", "/")
    except sh.ErrorReturnCode as e:
        print e.stderr
    finally:
        sh.hdiutil("detach", volume_dir)
{% endhighlight %}

As I said, the Homebrew install is easy. I did have to include a small [fixup gist](https://gist.github.com/rpavlik/768518/raw/fix_homebrew.rb) to get it to work on one of my test machines.

### Python Stuff

Working with Python made a lot of the script easier. Specifically, working with `sh` made tasks like getting the list of items currently installed by brew pretty simple:

{% highlight python %}
installed = self.sh.brew("list", "-1").split("\n")
not_installed = list(set(self.dependencies) - set(installed))
{% endhighlight %}

It also allows chaining, just like in a bash shell:

{% highlight python %}
sh.grep(sh.cat("/etc/hosts"), HOST_NAME)
{% endhighlight %}

One area that was a little tricky was activating virtualenv from inside Python. However, there is actually a [supported method](http://www.virtualenv.org/en/latest/#using-virtualenv-without-bin-python) for this.

{% highlight python %}
activate_this = '/path/to/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
{% endhighlight %}

### GitHub Stuff

For the shortest URL possible, you can set the [default branch](https://help.github.com/articles/setting-the-default-branch) in GitHub to be something short, like "go". Looking at the homebrew installer, I noticed that it's possible to leave the file name off, too. GitHub's raw file service apparently picks the first file by alphabetical order if you do this. However, I didn't want to mess with trying to get my code to show up alphabetically before `.gitignore`, so I skipped this optimization.

### Final Thoughts

Random other thoughts on writing installers:

- Create a temp directory if you need to do anything like download files.
- Make the installer idempotent; you want to be able to retry cleanly.
- Checking whether a step has already been run is a good idea.
- Don't try to hide the debug output; at least for a development audience.
