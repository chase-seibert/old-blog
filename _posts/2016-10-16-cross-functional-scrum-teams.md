---
layout: post
title: Cross Functional Scrum Teams
tags: scrum newboss
---

> Teams are also cross-functional; Team members must have all of the skills
necessary to create an increment of work. - [Scrum Guide](http://www.scrumguides.org/docs/scrumguide/v1/scrum-guide-us.pdf)

I've been doing scrum for maybe eight years. When that first team
enthusiastically adopted sprints, points and grooming, our stack was Java
backends and ColdFusion on the front-end, with a smattering of jQuery. Perhaps
due to chance, or perhaps because the stack was so simple, all three engineers
on the team were fully fluent with all the technologies.

In the last few years, the complexity of the front-end has grown tremendously,
and it's become common practice for engineers to specialize in front-end or
back-end. Recently, my team has also added a mobile specialty. I've largely
encouraged this specialization because that seems to be the way the industry
is going, but recently I've been rethinking it.

Instead, I'm going to try getting back to my teams being full cross-functional.
That means everyone regularly working in all parts of the stack. I'm not sure
this is better for all teams, but I think it's a good idea for a small 3-5
person product team that has to do with in many parts of the stack. Why?

# Better for Team

One tenet of scrum is group estimation and grooming. The more people that are up
to speed on the technologies and the codebase, the more likely you are to think
of all the potential gotchas related to a story. There will be fewer occasions
where a story becomes vastly more work than anticipated.

Ideally the entire team is taking ownership of ALL the stories in a sprint. I've
noticed that with specialized teams, we tend to assign a story to an individual
even before sprint planning - in some cases there is really only one person
who can do a job. If the sprint is almost done, and only a mobile story remains,
a specialized team is likely to bring in a new unrelated story to work on, rather
than swarming on the story the team actually committed to.

Additionally, cross-functional teams can also be useful for sprints where there
happens to be a lot of high priority work in one area. It allows the team to
actually deliver the most important stories, and not compromise on a mix of
importance and specialized bandwidth.

Finally, on small teams, you can remove single points of failure by being
cross-functional. On a specialized team, if your only mobile engineer goes on
vacation or quits, it's much more disruptive.

# Better for Individuals

Cross-training can be good for individual engineers, too. During an engineering
career, you will find yourself needing to pick up new languages and technologies
on a regular basis. Failure to do so can make it difficult to stay relevant (read: employed), or capitalize on job opportunities. The choice of what to specialize
in can be tricky. What if you spend a bunch of time learning Angular, but then
it's replaced by ReactJS in the zeitgeist just as you're looking for a new job?
To some extent, cross-training lets you have more irons in the fire at once. You
can place more bets in parallel.

There is also a more subtle danger to having engineers work predominantly in
one part of the stack; they may get burned out. Especially when moving from one
specialized role to another, there is a chance that the engineer will wake up
one day and feel that the move was a mistake. Even if the engineer knows at an
intellectual level their manager is more than happy to have them change
specialization again, it might be easier mentally to simply look for another job.
This could even be an unconscious process.

# Mixed Bag for the Product

It's a less obvious win at the product level. A team of specialists will
produce more raw output than cross-functional team. This is most obviously true
during the ramp-up phase when one or more engineers is learning a technology for
the first time. Even more so when multiple engineers are doing it all at once,
such as if you try to transition from specialization to cross-training. But it's
even true to some extent at steady state; keeping up with 3x as many technologies
is that much more overhead.

But it does allow you to solve a given problem at the right place in the stack.
This can result in great complexity savings, which ultimately translates into
velocity down the line. All too often, I see engineers solve a problem in a
complicated way in the wrong part of the stack, simple because that's the tool
they have for solving it. This could probably be solved somewhat by a great
tech lead who's doing super detailed grooming - but that person would themselves
need to be cross-functional.

In the end, the biggest product wins are better code reviews and thus product quality,
and better grooming/estimates.

# In Practice

In the real world, you are always going to have engineers who are better at
some parts of the stack. Those people should definitely be first in line for
code reviews and architecture design white boarding for those areas. They are
also great candidates for code pairing, especially when training up another
cross-functional engineer.

To some extent, cross-training is inevitable on small teams. With three
engineers, having fully separate back-end, front-end and mobile roles is going
to introduce a lot of schedule trashing even for simple vacations. If an engineer
leaves, you may be dead in the water for quite some time. On that level, having
at least some redundancy in a given area is a business imperative.

Some engineers are simply not going to want to do this. A common
refrain is that it's not the most efficient setup. Another reason may be that
they simply will not enjoy working in a specific part of the stack. That may be
true, or maybe they just haven't given it a try yet. For these engineers, perhaps
are more realistic goal is to have them be "T-shaped" with their skills: deep in
one area but with some baseline skill in the entire stack.
