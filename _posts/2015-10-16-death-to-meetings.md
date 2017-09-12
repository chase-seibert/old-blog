---
layout: post
title: Death to Meetings (and other alternatives)
tags: process reading-list meetings manager newboss
---

> What percentage of your time at work do spend in meetings? If you’re a middle manager, it's likely about 35% of your time, and if you’re in upper management, it can be a whopping 50%. What's worse is how unproductive these meetings usually are. - [themuse.com](https://www.themuse.com/advice/how-much-time-do-we-spend-in-meetings-hint-its-scary)

Meetings are a fact of life in corporate America, whether you're working at a large company, or a startup. Is that 35% number correct? Seems pretty close to my personal results. I've been using [Toggl]() for a while to track time, and over the last 30 days, I have spent more like 40% of my time in meetings.

![toggl_meetings](/blog/images/toggl_meetings.png)

*The red block is meetings, green is coding, and blue is writing.*

What's worse, it's actually not that much lower for individual contributors. Do business owners really want their employees spending this much time in meetings? Is that the most productive arrangement? What's wrong with meetings, anyway?


# Bad Meetings

> Meetings are indispensable when you don't want to do anything. - [John Kenneth Galbraith](http://www.brainyquote.com/quotes/keywords/meetings.html#z5clr8zclSbxAafk.99)

Some meetings are very useful. The problem is that every meeting is very expensive. Say you get 10 people in a room for an hour. If they each make $150k/year (hey, this is the Bay Area), you just spent $750 (plus taxes and benefits). What if there are 100 such meetings a day across the company? What did you get for that money?

Have an all hands meeting for 250 people? That comes to $18,750. For that amount of money, you could book the [Indigo Girls](http://priceonomics.com/how-much-does-it-cost-to-book-your-favorite-band/) to present your powerpoint slides for you. You could give each employee a little over [2 gallons](https://www.thrillist.com/drink/nation/best-coconut-water-brand-amy-brian-coconut-juice-from-thailand-ranks-top) of coconut water. **You could hire another six engineers.**

The worst case scenario is that meetings are being called primarily for the benefit of the meeting organizer. That person obviously feels that it's a good use of time. What about everyone else? If you're not careful, you may have attendees who only need to engage for 5-10 minutes in a one hour slot, and are basically sitting idle the rest of the time.

For a software engineer, that looks a lot like synchronous blocking on I/O. You're killing throughput. Wouldn't a system of asynchronous callbacks be a lot more efficient?


# Alternative to Meetings

> If you had to identify, in one word, the reason why the human race has not achieved, and never will achieve, its full potential, that word would be 'meetings.' - [Dave Barry](http://www.brainyquote.com/quotes/keywords/meetings.html#z5clr8zclSbxAafk.99)

We have tools at our disposal to solve this problem - but we need a shift in approach.


## Slack

[Slack](https://slack.com/) is awesome. You should get it. If you're on anything else, you're missing out. How can you use it to replace some meetings? Just create a channel or private group instead of a meeting. Invite the attendees. Put the agenda in the chat. Link to some shared docs that people need to reference. Start a discussion.

One interesting thing that happens is that the conversation becomes asynchronous. It no longer strictly matters *when* people chime in. You can hold a conversation over the course of a day, or a week. This is a *big win* for everyone involved; let them participate when it makes the most sense for them.

Will people sometimes be slow to engage? Yep. That's when it's on the "meeting" organizer to ping people with an @mention. Meeting owners *need* to be driving the conversation - whether it's over Slack or in a traditional sit down.

Bonus points: your meeting is taking its own notes! Next time you have the meeting; the last meeting's notes are right there.

*PS: If you work at Slack and you're reading this - you guys should totally implement a "kill this meeting" plugin for Google calendar that deletes the meeting and sets up a temporary Slack channel with all the attendees.*

## Email

Email is another good option. Less collaborative than chat, but maybe better for longer prose. Of course, email is only slightly less maligned than meetings themselves. But hey, at least it's asynchronous.

## GoToMeeting

GoToMeeting is another good option, especially for screen sharing. Slack really needs to get on this, but for now it's probably your best option for some types of meetings.

## Recurring "Meetings"

One sticky wicket is the recurring meeting. If you have the same meeting weekly, do you still need a calendar item to remind people to join the chat, or start the email chain?

I guess you could, but that seems like the wrong tool for the job. Most recurring meetings are run by managers. Managers have a ton of things to keep track of. I guarantee they have a personal reminder system. They should use that to remind themselves to kick off the meeting on the right day.

Better yet, maybe you don't actually *need* the meeting this week. This is a subtle benefit - recurring meetings default to *not happening*, versus defaulting to happening unless someone cancels them. Inertia is a funny thing. Managers *should* be consciously thinking about whether a meeting is really required, every time.


# Good Meetings

> Meetings are at the heart of an effective organization, and each meeting is an opportunity to clarify issues, set new directions, sharpen focus, create alignment, and move objectives forward. - [Paul Axtell](http://www.amazon.com/Meetings-Matter-Strategies-Remarkable-Conversations/dp/0943097142)

Some meetings are not really meetings. One on ones are not meetings. Those should absolutely be on the calendar and happen every week.

What are some examples of good meetings?

- Demo + celebration of recently shipped projects
- Brainstorming ideas for a new product
- Strategy sessions

*Note: if you're going to have a brainstorming meeting, make sure people know how to brainstorm. Talking about potential implementation and challanges is not brainstorming.*


# Meeting Hygiene

No matter what the meeting is for, practice basic meeting hygiene.

- Have a clear meeting owner
- Have a clear agenda written down ahead of time
- Start the meeting on time
- The owner drives the discussion - stay on track
- End the meeting with a +/-/delta poll
- End the meeting on time, if not early
- Send out meeting notes via email to the whole team


# Culture

> Management's job is to convey leadership's message in a compelling and inspiring way. Not just in meetings, but also by example. - [Jeffrey Gitomer](http://www.brainyquote.com/quotes/keywords/meetings.html#z5clr8zclSbxAafk.99)

Again, most meetings are called by managers. It's up to those managers to set a culture of respect for people's time. Some parting ideas:

- Give everyone explicit permission to skip meetings at their discretion. No judgement when they do!
- Meeting notes are a great way to make sure people are not attending meetings just so they can know what's going on.
- What if a meeting owner had to put $1 in a jar every time they schedule a meeting? What if it was $1/person?
- Are you [tracking metrics](https://github.com/chase-seibert/gcal-report) on hours spent in meetings? Probably not. Why not?
