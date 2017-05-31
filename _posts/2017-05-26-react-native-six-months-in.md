---
layout: post
title: React Native Six Months In
tags:
---

NerdWallet released our first cross platform mobile app at the start of 2017,
about six months ago. We choose to use React Native, and we are still using
99% of the same code base for the iOS and Android apps. What have we learned
so far?

# Initial reasoning

We initially chose React Native because it was the only way to hit our goals. We
didn't have any native mobile engineers, and we had been asked to deliver an
iOS and Android app from scratch in just five weeks. We also happened to have
very solid React experience on the team. Additionally, the app overlapped very
nicely with some features we already had on the web, and we thought we could
get some code re-use there.

# Code Reuse Deep Dive

In our case, we started with an intuition that 50% of the mobile app codebase
could actually be NPM modules re-used from our web stack. Plus, we got the
obvious savings of 100% code re-use between the iOS and Android app code.

After 6 months, we can look at our actual code re-use to get a better sense of
where we actually ended up. Our current app has 26,000 lines of JavaScript. The
NPM modules that we include from our web app stack total 40,000 lines of
JavaScript. In practice, the maintenance of that shared code is virtually 100%
offloaded to other teams.

![react](https://docs.google.com/drawings/d/1-pqAgRwz9gh66290u3yJQ5Jfevn3hBEqzBFtORpQ9nE/pub?w=960&h=720)

Here is what it might look like if we had two separate native app code bases.

![native](https://docs.google.com/drawings/d/1QWus2w-VxQRpIbR_y51DKukeGXIgYKGObWY5eJuQ8Pk/pub?w=480&h=360)

If you think of an app codebase as 2 unit of library code and 1 unit UX code,
our app is about 1.2 units of code that we actually maintain. Writing two
native apps would be about 6 units. The most interesting learning for me was
just how much logic in an app is not related directly to the UI, as well as
how easy it is to re-purpose NPM modules targeted at web.

*Note: if you're interested in reading more about leveraging NPM modules in
React Native, see [@parshap's slides](https://t.co/tM8CSoZvlk).*

# Limitations

We have run into a number of areas where we are making compromises on the user
experience. It's not totally clear yet which of these are legitimate things that
React Native is not good at, and which are due to us as a team not having
focused on them.

## Performance

We have seen persistent issues with app performance, particularly around the
time to switch between tabs in the navigation. That issue seems to be due to a
bug in our navigation library, `react-native-router-flux`. But it's important
to call out that performance is largely dependent on getting React basics right.
Performance has been good enough that we have not dedicated time to look
into it further. In general, we still don't think there is anything that most
apps need to do for which React Native will not perform well, except maybe
custom animations.

## Animations

Basic stock animations like screen transitions are available and perform well
out of the box. For custom animations such as fading out a header as the user
scrolls down on a list view, you need to write the animation yourself. We
initially tried the naive solution where we control style properties from
JavaScript. That did not perform well. But it was relatively easy to use the
actual bridged animation primitives, at least for simple animations. We still
don't have a good sense of how difficult complex custom animations will be.

## Fonts

Initially we did not use the correct default fonts for each platform. It turned
out to be relatively simple to use either San Francisco or Roboto based on the
platform. Some font variants that are normally available are not included. This
ended up being something that probably took more time to get right than a native
app would, but if you pay attention to it the first time it should be smooth.

# Biggest risks

The largest risk with React Native is still the immaturity of the platform.
Releases come every two weeks with potentially breaking changes. But the larger
risk is more existential; even though it's still building in popularity, there
is a chance that React Native fades away in the coming years as the framework
ecosystem [continues to evolve](https://trends.google.com/trends/explore?q=react%20native,phonegap,cordova,Xamarin).

![trends](https://dl.dropboxusercontent.com/spa/sffu0th1cc1sg9q/ellfigls.png)

The second largest risk I see is a little more insidious. As we have ramped up
the team with engineers who have prior mobile experience, they have begun to
point out areas where we are not following best UX practices. Some of these are
intentional. It's very tempting once you have a cross platform app to make UX
decisions to optimize for code re-use, not the best user experience. Even more
troubling is the times when the engineers themselves don't realize that a
particular design is not following best practice UX; typically due to many of
them not having mobile experience.

# Question marks

In my mind, the biggest open question is around how these mobile native
platforms continue to evolve. Both Android and iOS have their developer
conferences this time of year. Neither are expected to announce anything ground
breaking in terms of how we build apps. This is a natural trend as the platforms
mature; there is less interesting stuff to do. This happened to the PC operating
system platforms over the last 30 years. 10 years into mobile, are we starting
to see the same? This could be the time when putting an abstraction layer on top
starts to make more sense, and actually becomes a winning strategy.
