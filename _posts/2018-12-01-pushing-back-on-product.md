---
layout: post
title: Pushing Back on Product
tags: manager
---

There is no shortcut for a well functioning scrum team that has built the trust
over time to be able to work at a sustainable pace. When the product owner and
the technical lead have been through war together, they can
fit almost any project into the roadmap. It generally comes down to some
combination of reducing scope and re-prioritizing. But on a new team that has
not built that trust yet, it can be a source of conflict. In that case, it's the
technical lead's job to protect the team.

You can look at this through two lenses: sprints and longer roadmaps. The same
principles and tactics apply to both.

# Basic Engineer Hygiene

You're an engineer. At the core, software engineering is all about breaking down
problems, finding creative solutions and generating the right abstractions. Pick
a work item and break it down into pieces. Can you simplify one of the pieces?
Can you postpone one of them? Can you agree to hack a solution for one piece for
the MVP and fill it in afterwards? Is one requirement accounting for a
disproportiuanate amount of the effort? Propose dropping it and see what people
say.

If you absolutely cannot reduce scope, at least plan to implement in stages. Set
milestones up front, even if it's inside a single sprint. See how quickly you
can get to a working version. Not a solution that satisfies all the criteria,
but something that solves 80%. Worst case scenario, you can have a discussion
about shipping it as-is if not everything gets done in time. But it has to be
working and shippable.

# Scrum Basics

The next bucket of tactics come directly from textbook Agile. There is a reason
these principles are so widespread; they work.

- Stack rank the work items. Focus your energy on trying to cut items that are
the lowest priority for the product owner.
- Have a stable velocity. If you're team has been running for a while, you
hopefully have predictable velocity and accurate estimates. In that case, it's
simple math as to how many stories you can do. Remember, you can
[estimate epics](http://chase-seibert.github.io/blog/2017/08/28/epic-story-estimation.html), too.
- Break stories into smaller pieces. If you can show that one piece accounts for
a lot of the work, maybe you can agree to do that work later.
- Agree to commit to less, but pull in additional stories if there is more time.
Again, textbook Agile.

For all these items, the Scrum Master is responsible for making sure the team is
living up to their own process. They should be the one to say whether the team
can commit to more work on not. This is one good reason for the Scrum Master to
NOT be one of the engineers on the team (or the product owner). There is a
perceived [conflict of interest](https://www.mountaingoatsoftware.com/blog/protecting-the-team-cuts-both-ways).

# Guerrilla Tactics:

Finally, if you have to pull out all the stops, don't be afraid to play dirty.
*Note: no actual product owners were harmed in the compilation of this list.*

## The Outside the Box

Identify something that could be significantly better about the design.
Pitch it to the product owner. Try to convince them to go back to the drawing
board.

## The Big Picture

Suggest a better long term technical solution, but one which is
otherwise not ready to proceed.

## The Deflection

Find another group that makes more sense to work on this item.

## The Disappearing Engineer

Make sure that every man-day of engineering you're assuming actually exists.
Does someone have a vacation coming up? Is there a project that you might need
to pull people off for? Are you accounting for interrupt driven work?

## The Consolidator

If you have more work items than engineers, consider having an engineer
focus on on task at a time. In many cases it would be better to go deeper on
high priority items in the backlog versus doing more discrete items. More
applicable to roadmap planning than sprint planning.

## The Missing Link

Is there a dependency which there is some uncertainty around? Consider holding
off on a work item until that dependency is actually delivered, in production
and battle tested.
