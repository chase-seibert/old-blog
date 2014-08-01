---
layout: post
title: Introducing Advocoders
tags: opensource blog
---

Hiring engineers is tough, especially right now with a general shortage of qualified candidates and record demand. Good companies realize they need involve their engineering team to help recruit. That could mean hosting drink ups, sending the team to conferences and old fashioned professional networking. But what about your engineering blog?

Many medium sized companies have some kind of blog for the engineering team. Larger companies often have a site run by corporate marketing disguised as a grassroots blog. Lots of companies have nothing! But I bet even those companies have engineers generating _some_ interesting content. Under their own personal [Stackoverflow](http://stackoverflow.com/) and [Github](http://github.com) accounts, they are likely generating at least a slow trickle of content. Some of them may even have their own blogs. But none of that stuff is directly tied back to the team, or aiding the recruiting effort.

That's why I'm introducing [Advocoders](http://advocoders.herokuapp.com/), a place where you can pull in the organic content your team is generating under a corporate brand. Right now it's only for Google Apps businesses, which includes most start ups.

Any engineer on your team can go sign up with their corporate Google Apps account.

![Advododers Signup 1](/blog/images/advocoders1.png)

They can fill out some basic information about themselves.

![Advododers Signup 2](/blog/images/advocoders2.png)

Then they link in their blog's RSS feed, their Stackoverflow account and their Github account.

![Advododers Signup 3](/blog/images/advocoders3.png)

They can also put in a blurb about your company.

![Advododers Signup 4](/blog/images/advocoders4.png)

Advocoders generates a combined news feed for all the engineers in the company, complete with syntax highlighting for code snippets. The engineers continue to get credit for their content, but right beside the content is a call out to contact the company for job opportunities.

![Advododers News Feed](/blog/images/advocoders.png)

Right now, it's hosted on [Heroku](https://www.heroku.com/). But it's just a Django app that you can [fork the code](https://github.com/chase-seibert/advocoders) and run yourself.
