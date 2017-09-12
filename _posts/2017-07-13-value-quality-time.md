---
layout: post
title: Trading off Value, Quality and Time
tags: manager newboss
---

The traditional [Iron Triangle](https://en.wikipedia.org/wiki/Project_management_triangle)
tries to explain in graphical form how software projects need to make hard
tradeoffs between scope, schedule and resources.

![img](/blog/images/ironTriangle.jpg)

This is alternatively referred to as the Time-Cost-Quality Triangle,
Triple Constraints, the Triangle of Balance, or the Iron Triangle.

# Many Triangles

There are many variants. A common variant is phrase "Fast, Cheap or Good. Pick two."

![img](/blog/images/fast-cheap-good.png)

A more nuanced version allows illustrates the nature of the tradeoffs that
you're making, an allows for a middle option where all three are in balance, but
you're not really optimizing any of them.

![img](/blog/images/Project_Management_Triangle.jpg)

Software engineers is all about managing tradeoffs. The highest level
tradeoff is during planning and prioritization in the form of trading off
value delivered, the quality level of that value and the time to deliver it.

# The Agile Triangle

>"If you're a team that practices waterfall development or new to agile development, the important thing to remember is the difference between what is fixed and what is estimated. Unlike waterfall development, agile projects have a fixed schedule and resources while the scope varies."
[https://www.atlassian.com/agile/agile-iron-triangle](https://www.atlassian.com/agile/agile-iron-triangle)

Agile methodology in particular uses fixed time periods and fixed resources. This
is typical of a start up environment, where you need to ship quickly and do not
have the resources to hire many engineers. You're also typically building an
MVP type product, trading off scope versus time. Scope can be further broken
down into feature breadth and depth, and the quality of the whole experience.

![img](/blog/images/agiletriangle.jpg)


# My Agile MVP Triangle

To simplify, my version of the Agile MVP triangle looks like this.

![img](/blog/images/Value-Quality-Time.png)

You can pick exactly one spot on this triangle for a given project. If you
choose a spot close to the value point of the triangle, you are explicitly
giving up some focus on a quality, polished experience. You're also choosing to
push out time to deliver somewhat to get more value in.

This is joking talked about as "Fast, Cheap or Good. Pick two. *No, not that one*".
Alternatively describes as "Nine women cannot make a baby in one month"
([Mythical Man Month](https://en.wikipedia.org/wiki/The_Mythical_Man-Month)),
meaning that even if you did add resources in the form of extra engineers,
you can quickly get to a point of diminishing returns where adding people
doesn't actually speed up the delivery.

What do these points mean, exactly?

## Value

This is basically scope. It could also be labeled "Features", both in terms of
breadth of different features, and the depth/scope of an individual feature. I
thought about calling this "User Value", but quality could also be considered to
deliver user value. Likewise, scope could include quality/polish work. In the
end, this isn't a perfect term, but I basically mean user value excluding
quality/polish.

## Quality

Some examples of quality are high fidelity graphic style, UX optimizations
based on feedback and performance tuning. This is often subjective, and can
take a virtually unlimited amount of time as you polish on the far end of the
diminishing returns curve. The trick is getting to 80% of max quality with 20%
of the effort.

## Time

This is simply the time to ship - to put the software in front of real users.
