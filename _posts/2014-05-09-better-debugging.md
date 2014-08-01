---
layout: post
title: Better debugging through healthy living
tags: process debugging reading-list
---

Debugging code is more of an art than a science. It's an art form that you will have plenty of time to practice as a software engineer.

> Reworking defects in requirements, design, and code consumes 40-50% of the total cost of software development. - [Improving Software Productivity](http://programmers.stackexchange.com/questions/91758/debugging-facts-and-statistics)


## Fallacies about bugs

Bugs are failures. Failures to predict a scenario, or failures in assuming that this case would never happen. The first step is admitting that you have a problem. Related cognitive dissonance:

1. "It's not my fault." False. 99% of the time, it is your fault.
2. "It worked yesterday, and nothing changed." Yes, something changed. You just don't know what. It could be a change in data or a change in a dependency, but something changed.
3. "It must be the tools/frameworks/universe out to get me." See #1. Don't attribute to malice what can be explained by your own stupidity.
4. "It's a bug, but it's not MY fault". Famous last words.

## Debugging Mindset

Don't go into a debugging session looking to assign blame to someone else (see #4). Most bugs are caused by assumptions, your first task is to consciously question the assumptions are you making as you read the code. Don't assume a variable has the value you think it does. Don't assume the database returned the data you're expecting. Verify. Contrary thinking is useful here.

This includes being skeptical of the assumptions made in the original bug report. Whether it's from a customer or a QA person or another developer, follow the creed "trust, but verify".

## Before you start

In fact, before you even begin looking at code, make sure you can reproduce the issue. 98% of the time, a bug should have a repo case. Every issue can be reproduced, it's just a matter of isolating the variables. That said, in the 2% case where coming up with a repo case is too difficult, it's reasonable to start debugging without one. But you should expend a serious amount of effort yourself trying to reproduce it before you give up on a repo case. After all, if you have no repo case, how are you going to know if you fixed it?

Once you have a repo case, trim it down to the bare essentials. Try reproducing the issue without some of the initial steps, and see if it still happens. If so, omit those steps. For more specific particulars of the repo case, make sure that it does not also happen in the general case; those too are erroneous details that can cloud your thinking.

## Techniques

The basic debugging stages, in order, are:

1. Reproduce. Don't skip this step. Trust but verify.
2. Gathering info (stack traces, logs, screen shots, IDs, accounts, etc.)
3. Isolating the code causing the problem. It was OK up until a particular line of code.
4. Fix it. Usually this is easy after you know what the problem is.

Stack traces are you best friend here. In many cases, they are all you need to isolate the issue to a single line of code. At worst, you've isolated the issue to something that calls this code. But if you don't have a stack trace, what do you do?

Step through the code. This is boring, but extremely time efficient. It's the fastest way to validate your assumptions. You can speed things up significantly with some intelligent guessing about your initial breakpoint. This is where your intuition comes in.

Sometimes you can't step through the code. Maybe you're in an older web browser that doesn't support breakpoints. Maybe you're trapped in 1999 debugging PHP 3. Whatever. You can simulate stepping through the code with logging, print statements, alert() calls, etc.

A couple of other techniques that sometimes come in handy:

- Binary search/bisect. If you've isolated it down to a piece of offending code that's fairly long, you can try deleting half of the code and see if the problem still happens. If it does, you know the problem was with the other half. Repeat. Of course, this is only applicable in the cases where deleting a large chunk leaves you with a viable running program.
- Rubber duck debugging. This is a good one. If you're ever really stuck, trying explaining the problem to someone else. If no one is around, try explaining it to an inanimate object. You might be surprised how often this leads you to a solution.

##  Debugging Tools

What tools should you use when debugging? Anything you can get your hands on. Graphical IDEs with debuggers are great, but not necessary. Their primary utility is that they let you "explore" the variables in scope, and evaluate expressions. You can get the same thing out of a good interactive interpreter.

No matter which tools you use, you want to get your "debug cycle" as fast as possible. This is the time it takes between you changing the code and running through the entire repo case to see if it's still happening. Again, the ultimate short debug cycle is being able to repo the issue with a single statement in an interactive interpreter.

If you have used a language with an interactive shell such as python, node, etc, you will miss them when you're using a language that doesn't have them such as Java, C#, etc.

## Skills

Personally, I feel that generalists are better at debugging. The more pieces of the software stack you understand, the quicker you will be able to isolate where the issue is occurring. General experience in a particular code base or stack will similarly speed your debugging. Unfortunately, both of those skills simply take time to develop.

## Prevention

Because debugging does take a significant amount of time, anything you can do to reduce it will pay off. Writing good unit tests are huge here. They will help you think about the assumptions you are making when you're writing the code, as well as force you to explicitly deal with invalid assumptions.
