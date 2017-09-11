---
layout: post
title: Tiger Team Survival Guide - Part 1
tags: manager
---


> A tiger team is a diversified group of experts brought together for a single project, need, or event. They are usually assigned to investigate, solve, build, or recommend possible solutions to unique situations or problems. They are almost always populated with mature experts who know what's at stake, what needs to be done, and how to work well with others. Their strengths are diversity of knowledge, a single focus or purpose, cross-functional communications, decision-making sovereignty, and organizational agility. Once their venture is completed they cease to be a team and usually go back to their previous assignments.


# Scope, Time and Money

As an engineering manager, you can typically have some input on the scope, time and resources allocated to a project. This is a variation of the ["pick two problem"](https://en.wikipedia.org/wiki/Project_management_triangle#.22Pick_any_two.22). When the project scope and timeline are largely dictated by business needs for a high priority project, resourcing may be the most flexible factor.

If possible, identify a shortlist of veteran engineers with specific skill sets that can make the project successful. Talk to their managers and get buy-in. Work to alleviate any concerns the individuals may have about what you're asking from them, and whether their existing projects will fall on the floor.

Some specific resources to think about:

- Senior back-end or front-end talent
- Make sure you look at planned vacation time before asking for individuals.
- Devops
- Project management/co-ordination/communication support
- Outside experts/contractors - can you find someone who is a professional trainer in an area you need help in on short notice?
- Are you planning on making a deep technical contribution yourself, or focusing on organizing/leading?
- Make sure you have 100% alignment on the KPI for the project.

# The War Room Model

A natural instinct on a short schedule is to find a private space where the team can isolate themselves, have persistent wall space for collaborating, and cancel all other obligations within reason.

Try deputizing a specific person from workplace ops and have them handle logistics:

- Find a room big enough for the team, with room to spare. Should have ample whiteboard space and a monitor.
  - Nearby breakout spaces and or extra standing desks is ideal.
- Make sure people have badge access if needed.
- Increase lunch order size if you're moving offices.
- Plan on canceling all your own meetings except direct report 1:1s, 1:1 with your boss and critical status meetings.

Potential IT asks:

- Extra monitors, keyboards, mice and power strips in the war room.
- Any new hardware you might need (test devices).

Other stuff:

- Ask recruiting to cancel all interviews for the team
- Ask for support when engineers go to clear their calendars
- Block off everyone calendars with individual all day appointments
- Using one all day appointment that spans days or weeks is likely to be ignored by people booking conflicts

Communication tools:

- Create a Slack group
- Create an email distribution list
- Create a JIRA or Trello board
- Create a Google Docs folder
- Start compiling a list of important team links and put them on a Trello card, pinned to the Slack channel topic

# Reducing Risk

- What dependencies do you have on other teams?
  - For engineering dependencies, try to get a dedicated domain expert on the tiger team.
  - Are the APIs you need to use publicly accessible? Do they require some specific authentication, scopes or do they return results that are too highly tailored to another use case?
- Starting thinking about what you need to do for security sign off.
- Starting thinking about what you need to do for compliance sign off.
- Have design start with high level mocks - not pixel perfect. Get the flow nailed down ASAP.
- What kind of existing code will you be able to reuse?
- Does the re-use require another team to refactor something?
- What is your analytics/data integration plan?

# Sample Kick-off Day Agenda

- *start at 10am sharp*
- Intros (5 min)
- Business context and goals
- Initial mocks share out
- Need a large format print out what we can put on the wall and write on
- Define milestones
- What is everyone hoping to get out of this experience?
  - Write it down as a list on a wall
- Working agreement
  - Whitelist of outside meetings we will attend
  - Brainstorm how we can move fast - create a speed list
  - Create technical debt list
  - Create a big decision list
- Process - define how we want to work
  - Working hours
  - Daily stand up
  - Pairing
  - No code reviews?
  - Multiple merges a day
  - Daily demo
- Pair assignments and component ownership
- *lunch at 12pm*
- Code reuse strategy
- Break outs
  - Front-end architecture, how to break things into components?
  - Back-end architecture, high level system capabilities needed
- Code layout and separation of concerns
  - Write it down, eventually copy to README)
- Hacking
- Demo
- *done at 6pm*

# Make it fun

Don't make it a death march. Plan to work reasonable hours and have some fun activities mixed in.

- Booze; plan to start drinking early and often
- Video games
- Tiger team branded laptop stickers, T-shirts
- Donuts/muffins/coffee
- Massage Station
- Sonos
- Go to a related meet up as a group
- Get a photographer to document your awesomeness for posterity
- Special lunch outings (food trucks, local spots)
- Get out of the office and play basketball, or go to a movie as a team

*Stay tuned for part two...*
