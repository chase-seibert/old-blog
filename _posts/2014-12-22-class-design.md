---
layout: post
title: Thoughts on Object Oriented Class Design
tags: computer-science object-oriented
---

> The problem with object-oriented languages is they've got all this implicit environment that they carry around with them. You wanted a banana but what you got was a gorilla holding the banana and the entire jungle. - Joe Armstrong

In my experience, class design is an area where software engineers are prone to over-estimate their own abilities. This also happens with SQL and regular expressions. The concepts seem simple enough that it's easy to fool yourself into thinking that knowing the basics is equivalent to being an expert. The reality is that most people could use a refresher on what makes a good object oriented abstraction.


## Encapsulation - Hiding Implementation Details

> [Encapsulation is] the process of compartmentalizing the elements of an abstraction that constitute its structure and behavior; encapsulation serves to separate the contractual interface of an abstraction and its implementation. - Gary Brooch


At the core, class design is about encapsulation. You want to make it easier to think about your problem space by limiting what you need to keep in your brain at any given time. You want classes that hide unnecessary implementation details from the outside world, are well tested, and are easy to use. That allows you to think about your problem space as the interaction of instance of these objects, versus the low level detail.

For example, say you have a class that represents a zipped file. Internally, it uses a regular file descriptor to access the base file. That's not something you want to expose to callers; it's an implementation detail. Maybe you decide later that you want to be able to have the base file be an S3 URL. If you expose the internal file descriptor in the initial implementation, that may end up limiting your options down the road.

In some languages like Python, it's not possible to hide implementation details by marking methods and members as private. Even there, it's well worth using standard conventions for communicating to other developers what should and should not be accessed.


## Cohesion - Consistency of Abstraction

> Cohesion refers to the degree to which the elements of a module belong together. Thus, it is a measure of how strongly related each piece of functionality expressed by the source code of a software module is.

I think of cohesion as the level of consistency in the abstraction. If you have a class that represent a web request, you could conceivably try to handle HTTP methods, URL parameters, headers in one large class with a hundred methods on it. But you're probably better off breaking that down into separate more focussed classes. That way your URL parameters class has just a few methods on it, and they are all related to a small problem space.

One tool I find helpful for writing cohesive classes is to start by thinking about the class API first. What are you going to call the class? What are the methods you are going to provide? By thinking first about how you would ideally like to use this hypothetical class, you can focus on making the API cohesive before getting bogged down in implementation details. Once you have started implementation, it's very tempting to allow the scope of the class to grow.

Good naming is one of the hardest parts of writing any code. It's especially important for writing cohesive classes; if your class methods are becoming too awkward, it may be because your class is doing to much.


## Loose Coupling - Swappable Components

![loose coupling](http://i.stack.imgur.com/OJFhI.jpg)

If your components are encapsulated and cohesive, it should be easy to compose them together. It should also be easy to swap out a particular component for another version that implements the same interface. The degree to which this is easy determines whether your system is loosely coupled.

You can typically make components less coupled by reducing the number of things needed to construct them. Similarly, you can have your methods take standard primitives and collections versus custom objects.


## Common Pitfalls

> The phrase "object-oriented" means a lot of things. Half are obvious, and the other half are mistakes. - Paul Graham

Here are some common mistakes in class design.

- Large interfaces. Even small changes in the API may require many updates.
- Subclass methods that are empty/pass. This may be a sign that the abstraction needs to be refactored.
- Multiple inheritance. Often hard to reason about. Limit yourself to simple mixins if you must do it.
- Tying the interface to the implementation. Example: persistent object that exposes underlying database functions directly.
- Invalid method sequences. If you can't call `process` until you call `open`, then `process` should do that for you.
