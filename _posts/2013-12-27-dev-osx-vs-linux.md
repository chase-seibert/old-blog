---
layout: post
title: Development on a Mac versus Linux
tags: osx linux
---

I love the Mac computing experience. Their laptop hardware, like their phones, feel solid and elegant. OSX usability is excellent, though it is myopically geared towards the lowest common denominator of user. For most tasks, I appreciate that trade-off of affordability versus advanced power features. But not when I'm doing development. Even though I use a Mac as my home laptop, I prefer a Linux machine for work. I also keep a Windows desktop at home for gaming. To me, that's just using the right tool for the job.

# Package Management

By far my biggest complaint with OSX (and Windows) is the state of package management. Once you have experienced installing a piece of software in totally automated fashion from the command line, it's hard to go back to Googling for a binary (or worse, the source) and struggling on from there. I feel dirty, like I'm hanging out on a BBS trawling for warez. That's why almost every new language these days has package management built-in. Would you consider adopting a language without one? Then why do you put up with that for software?

Whereas on Windows there is literally nothing (that I have heard of, anyway), on a Mac at least there is the App Store, and brew. The App Store is not what I would consider a package manager for development purposes; generally you can't install stuff like MySQL, Redis, Python, etc from there. That's what Brew is for. But their "packages" consist of essentially bash scripts that go out an download a binary from the same website you would get to if you Googled it, and they have per-package code that checks for things like dependencies. Often the veil is lifted and you will be presented with a GUI installer; exactly not the point.

In my experience, brew fails to properly install something too often. Whether it's a 404 on the download, a missing dependency it did not offer to install or just plain botched logic, it's frustrating just as often as it's useful. Blind rage ensued when installing brew itself, which required me to go register for an apple.com account and download a **MASSIVE** XCode installer manually. Arg! A good effort, but about what you would expect from trying to bolt-on a package manager after the fact.

APT, on the other hand, is extremely reliable, and is much faster. It has binaries ready to go for almost every conceivable platform. It's dependency management is excellent. You can even upgrade and remove packages reliably. Imagine that!

# System Updates

Recently I upgraded a Mac from OS 1.7 to 1.8. All of a sudden my Python dependencies are broken due to some path change. XCode isn't even installed anymore. All of my project's virtualenvs needs to be re-installed from scratch.

This is one problem I have never run into on Linux. APT knows exactly what I have installed, and makes sure everything is up to date, even if you're doing a full distro upgrade. Because package management is built-in and continuously exercised on production machines, you have a much better chance of not having to manually futz with anything.

# Passive Devops Education

If your only experience with Linux starts with asking Amazon to clone an existing image, then you're missing out on a whole bunch of ancillary knowledge. Configuring X is it's own little world, complete with kernel panics and un-bootable systems. You will probably learn how to emergency boot into different run levels, and REISUB restart a seemingly dead system, both of which could come in handy if you even need to rescue a physical server. Maybe your video is skipping, so you learn all about nice levels and end up using that later on your production database. If you learn all about PPAs by tracking down a custom fork of GVIM with a transparent background, you may end up using that knowledge to easily install a commercial HBase version.

The more exposure you get to the platform, the broader your knowledge base about Linux in general. This is especially valuable if you're not really in a devops role trouble-shooting production systems every day. Sure, seemingly mundane tasks can take an unreasonable amount of time on Linux, especially for new users. But it builds character ;)

# Trade-offs

Now, you might rightly point out that you don't spend a very large percentage of your time installing packages. Nor do you update your operating system very often. You already learn a remarkable amount about Linux by simply SSHing into servers. True enough. That's why, despite my rant, I don't feel super strongly about this preference. Certainly there are times when I'm struggling to get multiple monitors working in X that I would just as soon not be wasting my time. In the end, I just like running all three of the major operating systems regularly, keeping my toe in the water for each.

Graphics display configuration is definitely not the only downside to using Linux as your desktop. Some software may not be compatible at all, such as XCode. Some, like Hipchat, have half-baked Linux versions. God help you if you try to hook up a projector to a Linux laptop, or try to get the damn thing to sleep properly. Oh, and I hope you didn't want any kind of remote desktop solution that doesn't perform like you're on a 14.4bps dial-up connection, even though Windows had that nailed back in 2000.

On the other hand, at least you have your Linux desktop merit badge. Always impresses at parties.
