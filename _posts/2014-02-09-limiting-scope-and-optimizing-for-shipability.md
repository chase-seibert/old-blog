---
layout: post
title: Limiting Project Scope and Optimizing for Shipability
tags: process reading-list
---

>Observe that for the programmer, as for the chef, the urgency of the patron may govern the scheduled completion of the task, but it cannot govern the actual completion. An omelette, promised in two minutes, may appear to be progressing nicely. But when it has not set in two minutes, the customer has two choices--wait or eat it raw. Software customers have had the same choices. - The Mythical Man-Month

Too often software engineers find themselves 1:50 into this process thinking, "Oh god, I hope this omelet sets in the next ten seconds". You probably know this feeling. In the kitchen, it's called "being in the weeds". In a software project, it's the begrudged natural state for pretty much all project time outside the initial few week "honeymoon" phase.

This should scare the shit out of you.

Instead, I see most engineers take it in stride. Their attitude is, "This is the inevitable nature of software projects". Never mind that at any decent company, the engineers themselves came up with the schedule. They blame unrealistic requirements, never mind that they knew the requirements going into it. What they should be thinking is, "Damn, all these variables were in my control and we're still going to be late".

The variable that many engineers ignore is scope. When asked to make a 6 egg omelet that may not set in time, start thinking about how to make a one egg omelet that will definitely set quickly. That's your minimum viable breakfast, aka a *potentially shippable* omelet, and it's your golden ticket.


# Moving past breakfast

OK, the cooking analogy is breaking down. An omelet with six eggs that set at six different times is going to be totally gross. But that's not true of software. Your stake holders only care about scope (does it have mushrooms?), cost (why is this omelet $18.50?) and time (is it done yet?). Cost depends on headcount, and is usually not under your control. Scope should be something that you control, and you should seek to reduce the scope you are *committing* to as much as possible, putting most features in the "maybe" pile. Time is seen as knob to turn only in so far as you are willing to work harder, i.e. the overtime death march. But it's actually much more of a function of priorities.

Your top priority should be to get your new thing into a shippable state. As soon as possible.

Most engineers want to start with a refactoring task of unknown length, or maybe a research project with a nebulous goal. Those are fun. By doing them first, you are treating them as your top priority. While I agree that they do need to happen as part of a healthy project life cycle, they rarely need to happen first. You may be thinking of a particular project, and saying, "But those were the *necessary* pieces of the project. Nothing else would have worked without them. That was the whole point!"

But that's just it. Those items are *not* the point. The point of the entire exercise is to deliver customer value. I assure you they don't give a shit about refactoring or wiz-bang internals. What they care about is the functionality. And I bet if you put shipability first, you will see that there is likely a way to get to a shippable state with much less effort. In many cases, almost immediately.


# Born on third base

The empowering bit is that once you reach a shippable state, you're virtually assured of hitting your project timeline. In the remaining 80% of the time, go ahead and do whatever refactoring and prototyping you were planning on. Tack on every feature you have time to get to. Just keep bringing the project back to shippable at short intervals, like a week or two.
