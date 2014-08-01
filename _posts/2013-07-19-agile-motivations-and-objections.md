---
layout: post
title: Agile Motivations and Objections
tags: agile scrum
---

Often when I first start talking to someone new about Agile and/or Scrum, they have questions and occasionally objections. More often they just don't understand the motivation for trying a new development process. It's rare that these biases against Scrum persist, which is probably a testament to how common-sense it all is.

Still, in these situations I find it personally useful to have my thoughts collected and written down somewhere. So here is a quick run-down of common motivations and objections for Scrum.

## Motivation - For Engineers

TL;DR - Scrum is purpose built to make developer's lives easier.

### Fewer interruptions

In many development environments, it's common to be constantly or at least persistently distracted from your primary work by secondary requests coming in from outside the development team. Maybe it's a bug fix for a customer, or a site outage. Maybe it's an important feature to close a sale.

Most of the time, those tasks make sense and need to happen. Sometimes they really do need to happen **right now**. But too often, they are mis-prioritized and improperly allocated to a particular person instead of to the whole team. Scrum at least makes the product owner aware that these are coming in and reducing team velocity. In the best case, a good Scrum Master will deflect or service the majority of these themselves.

### Sustainable pace, aka the anti-crunch

No one likes crunch time. Many organizations institutionalize their lack of planning, and impose it as a recurring crisis on the engineering team. It doesn't have to be that way. Scrum empowers developers to own their commitments, but makes sure those estimates are solely reality driven. No PM can sign you up for an unrealistic deadline. If your estimates are off, they can only effect your life for on average half the sprint duration (usually one week).

### No requirements changes during the sprint

Tired of doing some work, showing it to a PM and having them say "actually, I meant THIS". Tough, that will always be the case! But at least with Scrum you can have a structured discussion about whether this scope change is large enough to constitute a new story for **next** sprint. If it's small, you can always just do it.

### Have a say in what gets built

Good teams always do this. With Scrum, it's a formally acknowledged part of the process. Engineers have an explicit venue (the grooming session) to talk about the technical details and design trade-offs of an upcoming story **before** it gets committed to.

### Someone to support YOU for a change

Sometimes engineers feel like everyone in the company has license to wander up and ask them to do some very important totally random task. Sweet, you must be super indispensable. With Scrum, now you have a lackey to hand these tasks off too; someone **you** can ask to "just take care of something". Meet your friendly neighborhood Scrum Master. They are like a task rabbit that can code.

## Motivation - For Product Managers

Product peeps have a (another) trade-off to make. With Scrum, you are giving up the illusion that you can predict what exact features can be delivered 6 or 12 months from now. But, your team will maximize customer value and deliver what they say they will deliver on time, consistently.

### Predictability

Maybe you don't know where you will end up in 6 months, but you will always be making progress on the next most valuable feature. Bonus: you will have a high degree of confidence that the current work will be done in two weeks or less. Plus, now that really means "Done-Done", i.e. no stuff that's 90% done for weeks on end.

### Definition of done

Speaking of which, you get to formally define a definition of what it means for a story to be "Done-Done". If you want that to include manually checking 16 different language packs, you can do that (if you can get the team to agree to it).

### Fast feedback

Every two weeks, you can also show the new hotness to actual users. Done means deployable, which means it's all integrated and ready to show to a customer. You can get real feedback on a real, working version of the feature in as little as two weeks.

### Bounds planning errors to two weeks

What happens if you royally, totally mess up scoping/grooming/executing an entire sprints worth of work? You lose exactly two weeks. That's it.

### Can change mind between sprints

True, you cannot change your mind about what you want to build during a sprint. But between sprints you can make any super radical pivot you want. It's less than two weeks away!

## Common Objections

### More meetings

Yeah, you may spend up to 10% of your time on stand-ups, grooming meetings, planning meetings, demos and retrospectives. You might be talking about one day of collaborating for a two week sprint. You will quickly get better at it, and get it down to maybe four hours.

In my experience, you are probably currently wasting way more time than that by not always working on the right thing. If you re-allocate the hours from that once a quarter, three day "oh my god we're so behind, what do we do?" Uber-meeting, it's a wash.

### But we **NEED** a 6 month plan

Just make one up at random. It's probably as accurate as the one you thought you had with a Waterfall design process.

### Can't change priorities

What are you talking about? You're now in **sole** control of the priority list. True, you need to wait until the end of the sprint, which is at most two weeks away.

### Story Points don't mean anything

By design, story points do not equate to hours. That's fine; they are only used for comparing stories _relative_ to each other.

## Pitfalls

### Velocity is not an employee evaluation metric

If you tie compensation to velocity, I assure you that you will get exactly what you asked for. Your velocity will quickly approach infinity. You can breathlessly tweet that your mobile team just completed 8 billion story points in two weeks. It will also cease to have any correlation to actual work getting done.

### Velocity should not be ever-increasing

See above. You can expect velocity to start out rocky with a new Scrum team. Things should stabilize in a just a few sprints, as people get the hang of it. After that, you can expect it to plateau, except for unrelated efficiency gains in automation/tooling/etc. Adding people to the team will temporarily drop velocity, but it should plateau again at a higher level (at least up to 7 or 9 total members).

### Scrum masters should not manage team members

This one is tricky for smaller organizations. Ideally, a Scrum team should be self-organizing. It can be difficult for all team members to feel fully self-directed and free to speak their mind if the person who gives them their performance review is also on the team. Scrum Master is especially at risk as they are explicitly not supposed to tell team members what to do, or how to do it.

### Retrospectives are forever

The process is malleable. But don't stop holding a retrospective regularly. Don't even cancel just one, not even once. As soon as you stop your commitment to self-improvement, you begin a slow atrophy to dysfunction. Morale is unsurprisingly correlated to how empowered team members feel.

## Trade-offs

Everything is a trade-off. Scrum is no different.

### No gold plating time

Quality should be built in. Refactoring is a daily routine that falls under the same bucket as writing new code in your estimates. The other 80% of "polishing" time is probably not adding as much value as the engineers think it is. YAGNI. If it is really valuable, you should be able to sell it to the product owner as worthwhile.

### Pure refactoring negotiable

Everyone has larger pieces of pure technical debt that need to be addressed. The barrier to entry for actually getting time allocated to those **is** higher with Scrum, which is exclusively focused on delivering user facing value. As an engineer, you need to learn to articulate those projects in terms of value. Also, try to tie them to related feature work.

### Forces grooming up front

Some seasoned teams can execute on features with little or no planning effectively. Even if you're in that camp, you will benefit from talking through the work in a low level of detail before you begin coding. Your design will improve, if nothing else. For most teams, it's simply critical to the cause of getting it right the first time.
