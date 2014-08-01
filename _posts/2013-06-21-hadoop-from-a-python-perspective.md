---
layout: post
title: Hadoop from a Python Perspective
tags: python hbase hadoop
---

I'm just coming off a project where we decided to use Hadoop for the first time. We're a Python shop developing an analytics feature. We have about 150m records we need to analyze daily, or approx 20GB of data. Even in our initial discussions, we knew that we could do this with our existing stack of Python and MySQL. But we wanted to "get our feet wet" with Hadoop, and gain some experience with it to see if we could make use of it more broadly.

> Big data is like teenage sex: everyone talks about it, nobody really knows how to do it, everyone thinks everyone else is doing it, so everyone claims they are doing it... - [Dan Ariely](https://www.facebook.com/dan.ariely/posts/904383595868?imm_mid=0a9701&cmp=em-strata-newsletters-strata-olc-20130529-elist)

We actually did get everything working with a stack of HBase/Sqoop/Hive. But we were so unhappy with a number of aspects of the solution that we're currently going back and re-implementing in Python/MySQL. So what did we learn?

## Hadoop/HBase are not general purpose

As should be obvious from even a cursory reading of the documentation, Hadoop HDFS itself is not a general purpose random access system. That's was HBase is for. But even then, you're gaining scalability of bulk writes and reads, but losing flexibility in the form of fast deletes and updates, as well as real-time sorting. You also end up having to denormalize your data once for every read pattern you will have. Having worked for so long with relational databases, you tend to take for granted all of the flexibility they give you to change your requirements on the fly. SQL is down-right magical for data sets up to a fairly large size like 1TB.

Don't give up one of the most valuable tools in your toolbox until you absolutely have to. I would go as far as to say if you have a big data problem, you'll know it because it's crushing your servers and you have already spent months optimizing. Until then, avoid Hadoop.

> It's likely that you simply have "large data," which practically every company has. Large data - and even most big data right now - can be analyzed and visualized in real time using BI software like arcplan without the need to invest in in-memory appliances like SAP HANA, massive data warehouses like Teradata, NoSQL databases like Cassandra, and distributed processing like Hadoop. - [Tiemo Winterkamp](http://biblog.arcplan.com/2012/12/why-im-not-impressed-with-your-big-data/)

## You can't avoid Java

I've worked with Java a lot in the past, and I made an explicit decision to re-orient my career more towards Python. I could list a dozen reasons why, but it all boils down to this: I personally find working with Python to be a joy, while working with Java always felt like work. With that in mind, you shouldn't delude yourself into thinking that you can treat Hadoop like a black box.

In theory you can just talk to HBase and kick off Hive jobs via their respective thrift clients. In practice, you end up having to deploy the services themselves, which is fairly complicated even with good distributions like Cloudera. You will also end up tuning JVM parameters and hunting through I-shit-you-not hundred line `CLASSPATH` declarations. You will end up Googling for that one JAR that you just can't seem to find, and then decompressing it to make sure it really is the exact version you need.

You will watch everything crash and burn because of a .01 version discrepancy between two dependencies you're only notionally aware of. And you will find yourself staring at a 1,000 line stacktrace that tells you absolutely nothing about what the actual problem is. Don't say I didn't warn you.

## You can't avoid MapReduce, either

Don't think you can get away with exclusively using Hive or Pig for your map reduce jobs. Firstly, even if you could, the best case scenario is that you end up with either pig of hql scripts. Those are fairly ugly looking pieces of code, especially the pig scripts. They provide a decent abstraction layer, but not enough that you could put an actual Python abstraction layer on top of them without losing all their functionality. They are also not testable outside a JVM, so be prepared to implement a new stack of continuous integrations tests.

Pig does have some Python interoperability. You can write custom UDFs in Python, and they will run via Jython in your map reduce jobs. But that only gives you very basic extensions. There are whole classes of UDFs that can only be written in Java.

Hive, while pretty cool, is also missing a lot of basic operations. For example, there is currently no way to compute a running total without [a custom UDF](https://issues.apache.org/jira/browse/HIVE-2361). Implementing one is non-trivial; we're talking thousands of lines of Java code, during which you have to fully comprehend the way map reduce works. Suddenly your map reduce abstraction isn't so abstract.

## Hadoop is still maturing

Hadoop itself is fairly tricky to deploy. It's also still a work in progress. Even minor version changes can still break things in spectacular fashion. Definitely use Cloudera, but don't expect a turn-key deployment. You should expect to invest in at least a dozen physical machines or VMs to get started. In fact, if you're not willing to eventually run tens or hundreds of machines in a cluster, you probably don't really need Hadoop.

Be prepared to spend at least some time on reliability issues. Like anything, new infrastructure can be flaky and will go down regularly until you work out all the kinks. For that reason, I would not recommend having anything user facing directly hitting HBase.

## Trust your gut

> You don't have a Big Data problem. - [Brent Ozar](http://www.brentozar.com/archive/2013/03/you-dont-have-a-big-data-problem/)

Double and triple check that you really need a big data solution. Until then, you're  better off with a traditional stack. If you think you can deliver a solution using Python + MySQL, do that. Leverage the "magic" of a relational database. Don't under-value the loss of data integrity, flexibility, tooling, testability and maintainability of your existing stack.

If you do end up with a big data infrastructure project, at least take a look at some of the newer Python native solutions. Also, think about doing a pure research/prototyping spike before you try to deliver a new feature AND a new infrastructure together.

> A recent Microsoft research investigation facetiously titled 'No one ever got fired for using Hadoop on a cluster' found misguided Hadoop installations both at their company and at Yahoo!,  processing less than 14G of data.  The paper concludes by advising analysts to not go through the Hadoop hoops until your data size passes standard hard drive limits (currently around 1 Terabyte) or at least reasonable memory limits (512 GB). - [Dave Fowler](http://www.wired.com/insights/2012/11/lets-talk-your-data-not-big-data/)
