---
layout: post
title: Long Term Software Estimates
tags: manager newboss
---

> False scheduling to match a patron's desired date is more common in our discipline than elsewhere in engineering because it is VERY DIFFICULT to make a vigorous, plausible, job-risking defense of an estimate that is derived by no quantitative method, supported by little data, and brought about by the hunches of developers.
- Mythical Man Month

Estimating a timeline for a project that will take many months and dozens of
engineers to complete has a very high failure rate - defined as the rate of
projects that take longer than the estimate to complete.

# The Myth of Software Project Planning

The biggest myth of software engineering is that we can estimate with any
accuracy. Junior engineers often learn this the hard way; coming up with estimates
that are best case scenarios, and working extra hours when the inevitable complications
arise. Seasoned engineers learn to pad their estimates (by a lot) to account
for the risk of going over. They learn that estimates are not reliable.

So why do we keep relying on estimates that the estimators themselves know are
unreliable? Because there is a legitimate business need to know. But we should
not confuse the need for certainty with the ability to be certain.

# Estimates Change as Scope Changes

![Dilbert](https://s-media-cache-ak0.pinimg.com/736x/7f/cc/b0/7fccb03a99c29ca90290709cf08afc7c.jpg)

There is often a great amount of accepted uncertainly around what will be built.
A successful business realizes that they need to keep requirements loosely defined
so that they can respond to new data as it comes up. Of course, if the scope
of a project is not high confidence, the estimate cannot be high confidence, either.

# Agile - Enter the Ordered Backlog

> No battle plan survives contact with the enemy.
- [Helmuth von Moltke](http://www.lexician.com/lexblog/2010/11/no-battle-plan-survives-contact-with-the-enemy/)

There are two main problems that need to be solved with making project estimates:

1. Humans are really bad at estimating.
2. We know that the scope of the project will change.

I'm not someone who believes that process can solve everything, but
[Agile](http://chase-seibert.github.io/blog/2013/07/19/agile-motivations-and-objections.html)
 does address these problems pretty well. The practice of using [relative pointing](http://chase-seibert.github.io/blog/2016/05/13/agile-points-vs-hours.html)
for estimates helps greatly with accounting for uncertainty and human error. Using
an ordered backlog chops uncertainty into bite sized chunks and using a well
established velocity keeps the error bars on longer term estimates manageable.

The most important thing is to ship it early and iterate.
