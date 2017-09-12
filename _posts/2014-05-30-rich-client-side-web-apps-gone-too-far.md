---
layout: post
title: Rich client side web apps gone too far!
tags: web reading-list newboss
---

## I have seen some Javascript in my time...

I've been getting paid to write web apps using Javascript for about 12 years. I
wrote a single page web based email client in 2003, years before the launch of
Gmail. I wrote a javascript instant message client for IE 5.5. I wrote a full
window manager inside the browser, complete with a dock, using IFRAMEs.

All of that stuff was extremely painful to get working back in the dark ages
before prototype and jQuery. One browser in particular absolutely sucked to write
Javascript for. Never mind debug tools, we didn't even have stack traces! About a
dozen times a day you would get an error that would just say "Object doesn't
support this property or method". That was literally it - no line number or
anything.

All this is to say that Javascript got a bad reputation. A lot of that was not
due to the language, but the platform. In recent years, the platform has gotten
a lot of love as we realized we are going to be stuck with this language. Tooling
has smoothed out remaining browser inconsistencies. But don't fool yourself; the
language still sucks.


## ... and I don't like what I see

It's just not a well designed language. Basic object comparison frequently results
in [mind-blowing violations of the principle of least astonishment](http://wtfjs.com/).
We have piled dozens of different and mutually exclusive hacks on top of the
language to support name spacing. To this day, I still stumble over the fact that
`this` will frequently not be pointing to what you think it is.

Which is why it is so unfortunate that this is the defacto language of the future.
It's the only option for cross browser client side code. Literally every other
option does not work with all browsers or is basically a language that's compiled
down to Javascript. Good luck debugging that.

To add insult to injury, web development has become more and more dominated by
rich client side work over the last 5 years. Javascript used to be a tool that
you used as sparingly as possible, sprinkling in just the barest hint of dynamic
behavior where it was absolutely necessary. Now it's common to start a new project
and assume that 50% or more of the code will be Javascript.


## At least make your fancy app act like a web page

Of course, everyone wants web apps that are responsive and interactive. For apps
like the aforementioned instant messenger and email clients, that makes total
sense. But 90% of the stuff out there does not fall under the same use case. Most
apps that are heavily Javascript based are just doing it wrong, in my opinion.
That's not how a web browser is *supposed* to work, a distinction obviously lost on
the authors of these applications when they continually break basic functionality
that we used to be able to take for granted.

I'm sure you've seen sites that refuse to record their state in the URL. Oh thanks,
I didn't want to bookmark this anyway. Too often these days I can't even tab through
form fields. If for some bat-shit crazy reason you find yourself using editable
`DIV` elements instead of actual form inputs, please at least remember to provide
the functionality we have been using since the '80s.

Then there are willful substitutions of the developer's judgement for that of the user.
I have never actually wanted a modal window to appear. Every time I see one, I just think
"well, fuck you too". Maybe you have alt-clicked on a link somewhere
only to have the link open in the current tab instead - or perhaps not open at all.
Presumably there was a good reason to re-implement the wheel by creating your own
special thing that's text you can click on, but that is not a real `A` element. NOT!

The 10th circle of hell should be for web developers who break the back button.


## How we ended up here

My pet theory is that the rise of dominance of rich client side apps is actually
mostly an accident of history. Right around 2005, with the launch of Rails and Django,
we had finally come up with ways to write server-side web apps that were not like
sticking a fork in your eye. We finally had separation of controller and view, along
with features like flash messages, session variables, and form validation, which
made it easy to implement a rich interaction with state persisted between server
side renders. On broadband, the server round-trips were so fast it felt like you
were serving up these dynamic pages from your local machine.

But at the same time, mobile was just starting to come on. All these pages we were
writing that rendered quickly on broadband absolutely sucked on mobile. No matter
how fast your server was, latency was killing you on these shit early wireless
networks. But we had a few years of AJAX under our belts, so we knew we could
deliver the illusion of responsiveness by simply not reloading the page.

I remember trying to write an app for IE7 that was 100% rendered on the client
side from a pure JSON server backend. That shit was ridiculously slow back in the
day on a broadband connected PC simply because IE7 could not render a decently
complicated HTML chunk into a previously rendered DOM without going out to lunch
for several hundred milliseconds doing god knows what - while at the same time
completely locking the UI of the browser.

But it was actually *better* on mobile. The latency was such a killer that even
though phones were even slower at rendering Ajax responses, the over-all UX felt
more responsive. So we started boldly going into the future of 100% javascript
apps.

Then a funny thing happened. Mobile users roundly rejected web apps. These days,
you are an absolute second class citizen on mobile if you don't have a native app.
Even Apple got this wrong. Their initial plan for the iPhone was to only have web
apps at the platform for third-party developers. IMO, for all our progress in
the last 5 years, wireless networks and phones are still shit, at least compared
to where we hope they will be in 10 years. Maybe then we will finally be able to
deliver write once run anywhere mobile web apps.


## Back to the future

The latest generation of developers don't even realize there is another way to
write web apps. Instead of writing just server side code, HTML and CSS, it's accepted
that we also need to write a JSON REST API, client side templates, duplicate client
side models and a whole mess of Javascript view code, hopefully on some kind of
sane framework.

I'm here to tell you that you're doing a lot more work this way. Most apps can
provide the same experience with about 5% of the client side code. Plus, you're
slowing down your development team throughput significantly. All that extra
complexity is not free. All of a sudden you have to hire people who specialize
in front-end and people who specialize in back-end. It used to be that virtually
all web devs could do both well.

The key to delivering awesome client server HTML page render apps is graceful
degradation, also called [progressive enhancement](http://en.wikipedia.org/wiki/Progressive_enhancement).
The basic idea is that your app should be fully functional even if Javascript is
disabled. This also is the thing that saves your ass when your giant blob of
minified JS is totally broken; at least the app still works.

Now if you deliver apps this way, it is absolutely critical that you serve
page renders fast. With client-side apps this is not as critical, which means
people have been getting lazy on this.

Besides development speed, you get a host of other benefits. Code is less
complicated. I have seen over and over again in my work that UI event code tends
to be the hardest to write and maintain. If it's not total spaghetti, you're doing
pretty well. Don't write that category of code if you don't have to. Your app
will be easier to debug; no more hunting down what view is calling what API to
deliver what data to your browser in a given HTML chunk. *Side note: for the love
of god put model IDs and other human-readable attributes in your client-side
generated DOM if you value your sanity*. You also reduce the compatibility
issues between browsers to relatively simple CSS differences.

Now get off my lawn!

&gt; END RANT &lt;

*Edit:* This just got posted to Hacker News. Thanks! I guess this hit a minor chord.
If you want to hear more, I'm going to do a whole episode on it on my new podcast,
the [Software Engineering Fireside Chat](http://t.co/jqnKhxF1K8). Look for it next Friday.
