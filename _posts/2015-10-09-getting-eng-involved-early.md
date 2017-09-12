---
layout: post
title: Getting Engineering Involved Early in a Project
tags: process newboss
---

> Agile requirements are ideally visual and should be barely sufficient, i.e. the absolute
minimum required to enable development and testing to proceed with reasonable efficiency.
                    - [Agile Principle #4](http://www.allaboutagile.com/agile-principle-4-agile-requirements-are-barely-sufficient/#sthash.wIvPTKXl.dpuf)

Some engineering teams don't want to think about a feature or a product until a specification has
been written. Their ideal world would be getting handed 100 pages of specification along with high
fidelity mockups and then starting to implement. I'm not sure where this instinct comes from; it's
never been my experience of how engineering can be successful, at least in start ups.

The first thing you have to realize as an engineer is that the spec is always wrong. If you can't
write code without bugs, you can't expect a specification without bugs. In fact, because engineers
as pretty great at finding bugs, they can add a lot of value debugging specs. Just like coding,
the earlier you find the bugs, the more work you're saving yourself over time.

If you're a PM, and your engineers are saying that they don't want to be involved until specs are
written, what they *may* really be saying is that they don't want to commit to building it yet.
Make sure you're arguing about the same thing.


# My Ideal Process

For me, the ideal process is having one technical lead, one designer and one product manager sit
down over lunch before anything is set in stone. Maybe there is an email chain or a few bullets on
a powerpoint deck at this point, but certainly nothing approaching a specification that could not
also fit on a napkin.

There is a standing joke about agile teams really performing a series a medium sized waterfalls.
This is a subset that I have seen in the wild - product managers doing what is essentially a
waterfall specification and mockup exercise and only involving engineering after the fact to
estimate.

If you've spent any time in a kitchen, you may already know how critical it is to season food
*before* you cook it. Salting a piece of meat before it goes on the heat (ideally many hours before)
produces a totally different result from cooking the meat and then adding salt. This is why the
short-lived proposal on regulating just that in NYC was so laughable; it would have produced vastly
inferior products.


# How Involving Engineers Early Adds Value

Engineers are experts at complexity. They can identify complexity where no one else has, and then
quickly compartmentalize it and think about the big picture. That's essentially how they break
down problems, whether it's on code or when evaluating a spec. They are also great at finding edge
cases, i.e. holes in the spec with undefined behavior.

The goal should be to have both the design and the implementation match the user's mental model.
What does that mean? The user likely has some expectation of what's happening when they use a piece
of software. That expectation should be echoed in the design, so that their options at any given
point match their expectations. That's when software becomes easy to use. But, long term, it's also
critical that the actual implementation match the same model. Too often, a mismatch here could have
been easily avoided by getting feedback early in the process from an engineer who can already see
that there will be weird implementation implications.

Ultimately, that translates into product quality.


# Startup Culture

Most startup engineering veterans can navigate this by instinct. Early on, the company may only
*have* engineers. There is no choice; they are involved in creating specs because there is no one
else to do it. The crimes of naive engineers on innocent designs and products are the topic of
another post, but at least they are forced to be involved at the right phase - the beginning.

Engineers want to be engaged. Go light on specs, but go heavy on iteration.
