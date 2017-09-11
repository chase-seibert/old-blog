---
layout: post
title: Using Points vs Hours for Estimates
tags: manager
---

One of the key innovations of Agile is that estimates should NOT be in hours,
but in points. But it doesn't just intuitively make sense. As a result, many
teams resist using points. This is one of the reasons why for teams new to
Agile, I always recommend that you try doing vanilla-by-the-book Agile first,
before you change anything. I think that if you do, the value of points will be
obvious.

If you're on a team that has always done Agile, but with hours, do you find
yourselves chronically under-estimating stories and not completing them? If so,
maybe I can convince you to give points a shot.


# Points are Relative, Hours are Absolute

One of the primary insights of Agile is that humans suck at estimating in
absolute terms, but are much better estimating in relative terms.

> Unfortunately, [reams of research](http://pm.stackexchange.com/questions/11675/is-there-any-published-research-about-story-points-vs-time-estimation) shows that humans are inherently horrible at
estimating in time. It turns out when we estimate jobs by how long they will
take us to complete we have an error rate of 400%. [Scrum, Inc](https://www.scruminc.com/points-vs-hours/)

Instead of trying to estimate how long a task with take, simply try to estimate
whether it is larger or smaller than another story. Don't think, "I should be
able to do that in three hours". Compare the story to something you have already
completed. Is it bigger than that 3 point story you did last sprint? Almost
twice as big? Would you say it's another 3, or is it more like 5 or 8?

Fundamentally, we are not estimating how long a task will take, but how large
it is relative to another task. In [terms of an analogy](https://www.mountaingoatsoftware.com/blog/the-main-benefit-of-story-points),
we want to know how long the trail is, not how long it would take you to run it.


# Points Enable Collaborative Estimates

An absolute estimate is how long it would take a particular engineer to complete
the task. If the task needs to be re-assigned to another engineer, it would need
to be re-estimated. Maybe this task involves regular expressions, or JavaScript
or schema design. The skill set between your team members is not uniform; they
will all have strengths and weaknesses.

Points are not pegged to an individual's implementation speed. Maybe we can all
agree that a story is three points, even though it would take the most senior
member on the team an hour, and other people would need five hours. That's fine!
At least we can all collaborate on a common estimate for the story. [This is
likely to make the estimates more accurate](https://www.mountaingoatsoftware.com/blog/dont-equate-story-points-to-hours);
the wisdom of the group may well identify both short-cuts and gotchas in the
details.

One particular related trap is having one person, usually the team lead, estimate
all the stories. Are you sure you are estimating how long it will take the team
to complete the story, and not how long it would take YOU? Big difference.
Besides, the team will be much more committed to estimates that they came up
with themselves.


# Points Communicate Uncertainty

In particular, Agile recommends that you stick to the Fibonacci numbers for
point estimates. Why? Because it accurately communicates the inherent
uncertainty of estimates. Estimates are wrong; everyone on the team should
internalize that. Given that they are going to be mostly wrong, we cannot also
make them very exact. Deliberating on whether a story will take 3 or 4 hours is
pointless, you are well inside the error bars. Deciding whether it's a one
point or a two point story forces you to accept an inherent margin of error.

Points may also allow for more nuance in the estimates. If forced to pick a
number of hours, there will be a tendency to be optimistic. But points should
reflect not only how large a task is, but also how much risk or uncertainty
there is. It's common to say that a story should only be 3 points of work, but
we're calling it an 8 because we're not sure about some of the details.


# Points Make the Team Accountable for Stories, not Estimates

A point is NOT equal to any number of hours - it's an average. Eventually, you
will get a sense that a point may take you anywhere from say 1 to 4 hours of
work. Note: that's just an example, points are always team specific; it's a
mistake to try to compare the velocity of one team to another using points.
But importantly, you do not expect those hours spent to converge; you will always
have a broad range of hours that a single point story took to complete.

This makes it clear to the team that they are not being held accountable for
100% or less overruns or under runs in their individual stories. If you use
hours, there is a great tendency to say "you said this would take one hour, but
it really took three". That doesn't matter! You should not even measure it.
What matters is, did you complete all of the stories in the sprint?


# References

- [Is there any published research about story points vs time estimation?](http://pm.stackexchange.com/questions/11675/is-there-any-published-research-about-story-points-vs-time-estimation)
- [Sprint Planning: Story Points Versus Hours](https://www.infoq.com/news/2009/09/story-points-versus-hours)
- [Scrum + Engineering Practices: Experiences of Three Microsoft Teams](https://collaboration.csc.ncsu.edu/laurie/Papers/ESEM11_SCRUM_Experience_CameraReady.pdf)
