---
layout: post
title: Switching from Ubuntu Unity to LXDE
tags: linux ubuntu lxde
---

Canonical was founded with the goal of bringing polish, consistency and _usability_ to the Linux desktop. Derided unfairly by some as not contributing much technically to the open source ecosystem, Ubuntu has been undeniably popular, becoming for the last five years the closest thing we have to a de facto standard distribution. I myself switched to using Linux full time coinciding with this phenomenon, drawn by the mixture of freedom, power and flexibility. For the first time in my experience, Linux mostly "just worked".

When Unity was announced a couple of years ago, I was more than willing to give Canonical the benefit of the doubt. Being a big believer in the value of good UX in the context of my own work projects, it seemed to me that professionals could surely improve upon the existing paradigm, which was mostly an accumulation of legacy skeuomorphs left over from the initial mouse and window scheme. I had already incorporated search into my normal work flow by using "Gnome Do", so a desktop designed around search seemed like a logical step.

When the first beta came out, the reaction from geek circles was largely negative. The bulk of users were simply reluctant to embrace change. Some of the feedback was legitimate constructive criticism, though. Making a single UI usable on touch screens and desktops leaves both sub-optimal. Search results were quickly turned into obnoxious and slow pseudo-advertisements. Multi-monitor support has was knocked back five years.

But usability sessions showed that Unity was in fact easier to use for novice users. First time users were able to more quickly figure out basic tasks. Feedback from these users was largely positive. So I told myself to give it a solid six months before coming to a verdict. Inertia turned that timetable into two years, but now finally I have had enough.

Unity is just too slow. Bringing up the Unity dash has noticeable lag. Even switching between windows with ALT-TAB doesn't feel smooth. I feel like I can see the window elements being drawn. I'm sure it's something to do with my graphics card, but I don't care. The lag has persisted over five successive releases, and several totally different pieces of hardware. My guess is that it's a combination of having three monitors (and thus having many more pixels to push than your average user), refusing to use the proprietary drivers (which have their own usability issues) and my own neurosis. But it's simply bad design to require good 3D video performance for basic UI interactions on a platform that has always been synonymous with poor graphics drivers.

Windowing in LXDE on the other hand __has__ "just worked". The very first time I booted into it, it picked up my three monitors correctly, with __no__ configuration. ALT-TAB is blazing fast, if aesthetically work-a-day. "Gnome Do" is all I need to launch apps. The status bar is easily configurable and familiar.

Not everything is rosy. The `ssh-agent` integration is manual. It was a PITA to get my sound set up with a bluetooth headset. The lock screen is decidedly fugly. It seems that the power users were right, in a way. Those niceties have not made it back into the larger Linux desktop ecosystem. But at least I don't feel like I'm operating my desktop over a 200ms VNC connection anymore.

Fuck you Canonical. You showed us how awesome a smooth, integrated Linux desktop could be. Then you went ahead and messed it up. Now the power user is back to having to fiddle again just to get a good experience. At least for me, you have managed to burn the goodwill you built in those first five years. I hope this mobile play is worth it.
