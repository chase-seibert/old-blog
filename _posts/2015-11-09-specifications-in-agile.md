---
layout: post
title: The Role of Specifications in Agile
tags: process
---

It's commonly said that everyone does Agile differently. In my experience, it's also common to do 
basically whatever you want and call it Agile. It can be useful to occasionally reset and examine 
what canonical Agile recommends. For software specifications, it's pretty simple. Do just enough, 
no more.


# Why do we need specifications at all?

> A software requirements specification (SRS) is a description of a software system to be 
developed, laying out functional and non-functional requirements, and may include a set of use 
cases that describe interactions the users will have with the software.
    - [Wikipedia](https://en.wikipedia.org/wiki/Software_requirements_specification)


Historically, specifications have been used to communicate to the customer (be it an internal or 
external customer) what will be built. Agile is built on the principle that this is actually not in
the best interest of the customer. Why? 

- Low effort specifications will have all parties making critical assumptions.
- High effort specifications take a lot of time - and will necessarily be wrong in big ways.
- Scope can and should change as we learn more about the problem.

In Agile, we build in short sprints. Documentation need only be created for the next sprint, or 
perhaps one additional sprint. This is known as 
    - ["Just in time Documentation"](http://www.agileforall.com/2009/02/new-to-agile-remember-one-thing-just-enough-just-in-time/)
    
    
# Self-directed Agile Teams

> Agile artefacts such as technical spikes and development iterations mean that high-level 
requirements can be considered sufficient at project initiation. 
    - [Ryan Hewitt](http://www.batimes.com/articles/applying-agile-principles-to-requirement-analysis.html)

For agile teams, specifications exist so that the team knows what they need to build.
Because we are committing only to one sprint at a time, we have no need to project long-term dates
that would necessitate a full specification. What documentation does the team need to get started? 
A highly detailed specification for just that first sprint.

![agile](http://www.userstories.com/system/product_image/file/980/Feedback_Flow-original.png?1392328012)

An agile team is composed of a product manager, a designer and one or more developers. This team 
must be empowered to design and implement their vision of a solution. A specification is definitely
NOT for feedback or sign-off prior to building. 
    
    
# How does the team know to build the right thing?

> Agile requirements, on the other hand, depend on a shared understanding of the customer that is 
shared between the product owner, designer, and the development team. That shared understanding and 
empathy for the target customer unlocks hidden bandwidth for product owners. They can focus on 
higher-level requirements and leave implementation details to the development team, who is fully 
equipped to do so – again, because of that shared understanding.
    - [Dan Radigan, Senior Agile Evangelist, Atlassian](https://www.atlassian.com/agile/requirements/)

User stories are the form that specifications take. Each user story is created in advance and 
placed in a backlog, but only the small set of the very next stories are flesh out in detail. Then,
the level of detail is very high. Designs are included at this stage, and so are detailed 
descriptions of fine grained behavior like validation, individual errors messages, etc.
 
Though the PM owns the user story, the team itself generates the detail through a processes called
grooming. User empathy is critical - while PM and design naturally represent the customer in the 
design process, the entire team needs to understand the customer motivation and pain points. 

In the end, the team may very well not build the right thing. This is where feedback comes in - at
the end of a sprint, once working software is produced and shown to the customer.
    
    
# When to get feedback

> Working software over comprehensive documentation
    - [The Agile Manifesto](http://agilemanifesto.org/)

In Agile, feedback is given based on working software, not specifications. The team commits to 
delivering and demoing working software every sprint. These demos are where feedback is generated. 
I've often been surprised when [customers don't really know what they want until they see it.](http://haacked.com/archive/2005/08/17/misunderstanding-agile-design.aspx/)
