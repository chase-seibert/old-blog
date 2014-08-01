---
layout: post
title: Why software engineers should maintain a blog
tags: reading-list career
---

I have a few pieces of standard advice that I give to anyone starting out in software engineering.
[Join a startup](http://chase-seibert.github.io/blog//2013/10/04/what-to-know-before-starting-at-a-startup.html),
[max out your 401k](http://chase-seibert.github.io/blog//2014/01/01/saving-for-retirement-as-a-software-engineer.html)
and *start a blog*. Why should you start blogging?


## Personal Branding

![calvin and hobbes](http://assets.amuniversal.com/8f870570df960131725e005056a9545d)

Early on in your career, your biggest asset is your future earning potential. *Aside: this is why you should also
consider buying disability insurance, which is super cheap*. You should be continually re-investing in yourself and
your career. Part of that is building a personal brand. When a prospective employer Googles your name, they expect
to find your LinkedIn profile and your Facebook page. If they also find a personal blog full of your writing and
your code, you just jumped ahead of 95% of applicants.

Most people on your interview loop with take the time to at least read the latest entries in your blog. They will
probably ask you questions about something you wrote about recently. *Hint: if you're actively interviewing, think
carefully about which posts you want to at the top of the list*. These are the absolute easiest interviews you will
ever have, and some of the most productive. The likely hood that you know more about the subject than the interviewer
is high.

Don't worry too much about the SEO aspect. If you produce good content and put your name in the title of all the pages,
the rest will take care of itself.


## Career Growth

When I sit down and think about what to write, I usually ask myself "What was the hardest problem I solved in the
last week"? This is a great reality check. Am I still growing and learning in my current job? If you have honestly been
putting in the effort to write, but you look back at the last three months of posts and don't see anything particularly
interesting, then you have your answer.

More and more recently, I have begun to blog about the soft side of engineering. I still write posts that explain a
particular technical issue I ran into, but I also write down my thoughts on my *philosophy* of engineering. I find these
particularly useful when growing your leadership skills. Often I will have a conversation with a new engineer, and then
reinforce my points by following up with an article I had written in the past.

You'll be doing a lot of communication during your career, both verbal and written. Honing your ability to communicate
well is going to pay dividends on whatever time you can spend on it. A surprising number of times I have found that it
also pays more direct dividends; searching for a solution and finding the answer in a blog post you had previously
written and forgotten about always makes me want to do a victory lap around the office.


## Giving Back

> Writing isn't about making money, getting famous, getting dates, getting laid, or making friends. In the end, it's
about enriching the lives of those who will read your work, and enriching your own life, as well. It's about getting
up, getting well, and getting over. Getting happy, okay? Getting happy.” ― Stephen King,
[On Writing: A Memoir of the Craft](https://www.goodreads.com/work/quotes/150292)

How many times a week do you find the perfect StackOverflow article that solves your problem and saves you hours of
banging your head against a wall? How many times do you spend hours solving a problem, but no one else ever benefits
from your solution? Help out other poor software engineers by posting your findings! The vast majority of the traffic
coming to my blog is from engineers searching for specific solutions, such as "python memory leak" or "mysql drop
column if exists".

You'll be surprised at the number of comments you will get. Most will just be a simple thank you. Yes - occasionally
someone will comment just to call you an idiot. Dealing with aggressive and confrontational people is also a
part of career growth.


## Good for your company

Personal blogging is also good for your company. Typical corporate blogs suck at conveying the personality of the actual
people on the team. Your blog can [make a bigger impact](http://www.inc.com/magazine/20100301/lets-take-this-offline.html)
just by being authentic. If you want to combine your blog, other coworker blogs and the company blog into one site and
RSS feed, you can use [Advocoders](http://advocoders.herokuapp.com/). There are many services that can then take that
RSS feed and turn it into a self-updating Facebook page or a Twitter profile.


## How to get started

> I used to tell people who asked me for advice about blogging that if they couldn't think about one interesting thing
to write about every week, they weren't trying hard enough.
[Coding Horror](http://blog.codinghorror.com/10-years-of-coding-horror/)

The hardest part is writing. The logistics of setting up blog should be easy. I would recommend looking for a platform
that supports syntax highlighting of code snippets that you include in your posts. Having an RSS feed of your posts is
critical.

Personally, I use [GitHub Pages](https://pages.github.com/) and a static site generator called
[Jekyll](http://jekyllrb.com/). The beauty of the system is that your posts are regular GitHub markdown, just like
when you're making comments on a pull request. You publish new articles with a simple `git push`. You could spend a
couple of hours crafting the HTML templates and basic Jekyll configuration yourself, or you can fork my repository:

```bash
brew install hub  # http://brew.sh/
git-hub fork git@github.com:chase-seibert/blog.git
git-hub clone blog
cd blog
git branch -D gh-pages
git checkout origin/quickstart -b gh-pages
./run.sh
```

A few minutes after you push your `gh-pages` branch to GitHub, you should be able to see your blog at
http://$username.github.io/blog.
