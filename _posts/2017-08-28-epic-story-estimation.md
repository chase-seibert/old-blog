---
layout: post
title: Estimating Epic Stories in Three Steps
tags: manager
---

In Agile, an Epic story is a potentially large placeholder story in the backlog.
Typically they will be broken down into manageable stories during grooming
before they are worked on. But if you need to estimate an Epic before breaking
it down, how might you do that?


# Use Story Points

In [Defense of Large Numbers](https://www.mountaingoatsoftware.com/blog/in-defense-of-large-numbers),
Mike Cohn talks about how removing the larger values from your estimation
toolkit is like deciding to strike "millions" and "billions" from our vocabulary
just because our bank balances are only in the thousands.


## #1 Show Historical Data

Pull up a list of recently completed Epics, along with their final point value.
For example, if you recently finished a "User Registration" Epic, tally up all
the points from all the stories in that Epic.

You might end up with something like this:

- Password Reset, 15 points
- User Registration, 35 points
- Admin Interface, 70 points

## #2 Discussion of Mocks

The next step is to view the mocks as a team. Yes, this means to need mocks.
Go over every screen as a team.

- Write down a high level set of features.
- Write down how many pages/screens are involved.
- Write down any complexity you see.
- Think about any dependencies you may have.

For Epic estimation, I like to cheat a little and ask the team to agree whether
this story is the same size as another Epic on the board, or whether it's
between two of the epics. That will ground planning poker.

## #3 Relative Estimation

You should be ready to play planning poker. Ask the team if they are ready to
estimate. Tell them that we are going to continue to use the Fibonacci sequence.
As a refresher, here are the larger Fibonacci numbers:

13, 21, 34, 55, 89, 144

Assign a number of fingers to each number. For example:

13 (1), 21 (2), 34 (3), 55 (4), 89 (5), 144 (6)

Now, it's time to vote. On the count of three, every one holds up a number of
fingers simultaneously. You would be surprised how often everyone in the room
holds up the same number of fingers at this point. Congratulations; you have
an Epic estimate.


# Bonus: Milestones

Remember that high level set of features you wrote down during the discussion of
the mocks? You have already done 90% of the work for milestone definition, might
as well take it over the finish line to de-risk your project. Reminder: the goal
of milestones is to deliver (usually three) potentially shippable product
increments along the way to a finished product.

Just write down labels for milestone 1, 2 and 3 on the board. Start with
the most critical features, and put them in the early milestones. You will
likely run out of room and have to bump features to later milestones. That's
fine! The goal is to keep the product potentially shippable; be ruthless in
prioritizing only features that would block a user from getting the primary
user value.


# What about T-Shirt Sizing?

On common method is to assign T-Shirt sizes to stories, such as Extra Small,
Small, Large, Extra Large, etc. This method has the benefit of being in a
non-numerical unit. It's very hard to hold a team accountable to a deadline
around an estimate of "Large".

This method also lends itself to relational estimation, versus absolute
estimation. But, you have to hold to that bar yourself. For example, you could
identify one medium sized story in the batch and randomly call it a "Medium".
Then, you can relatively estimate from there. If you do T-Shirt sizing a lot,
you should present the team with some of their previous complete stories, along
with their original T-Shirt sizes, to ground the discussion.

However, what if you also need to estimate how long the Epic might take in terms
of time? You might be tempted to equate T-Shirt sizes directly with a number of
weeks or sprints. But that's the same thing as equating story points to hours,
which is a huge no-no.
