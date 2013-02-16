---
layout: post
title: Why Database Integrity Matters
tags: database
---

Given the rise in popularity of [NoSQL](http://en.wikipedia.org/wiki/NoSQL) solutions, typically set apart by their explicit forfeiture of traditional [RDBMS](http://en.wikipedia.org/wiki/Relational_database_management_system) features, you might think that age old concepts like ACID transactions and foreign key constraints are simply antiquated. In the face of the new shiny hotness, why did we ever value [data integrity](ftp://public.dhe.ibm.com/software/solutions/soa/pdfs/Whydataintegritymatters-trifold.pdf) so highly, anyway?

Personally, I think it's critical to realize that NoSQL solutions were born primarily out of necessity. At some extremely high volumes of data, you simply don't have the luxury of data integrity. But that's a problem for the Facebooks and Googles of the world. The other 99% of us are flattering ourselves if we think we have the same data scaling problems. Of course, given NoSQL tools, more data will be accumulated by smaller companies, simply because it is now practical to work with.

But for traditional RDBMS systems, it's important to re-emphasize the value of data consistency. In short:

> Anything that can happen in a schema, will happen.

# Soft Deletion

Soft deleting a record refers to marking it as deleting, typically with a 0/1 value in a column like `is_deleted`. Some NoSQL solutions like HBase can do this natively, by keeping multiple versions of a data cell around. But it's actually a long-standing pattern from RDBMS. Typical reasons include enabling undo features, providing audit trails and simple fear of deleting data permanently.

Soft deletes are totally reasonable, but there are some [trade offs](http://weblogs.asp.net/fbouma/archive/2009/02/19/soft-deletes-are-bad-m-kay.aspx) to be aware of.

- Natural primary keys become more difficult. Do you allow two user records with the same username if one is deleted?
- Prevents you from using the cascading delete feature of you database, leading to orphaned records.
- Invites logically [invalid foreign key references](http://ayende.com/blog/4157/avoid-soft-deletes)- ie references from a soft-deleted record to a live record.
- Easiest to enforce through an ORM, but you won't always be accessing the data through the ORM.

Most importantly, they can slow down performance. If you have a significant amount of data, you will end up adding more indexes that you would otherwise need, simply to be sure you are always looking at non-deleted records. That will [slow down writes](http://richarddingwall.name/2009/11/20/the-trouble-with-soft-delete/) to some extent. You could regularly delete soft-deleted records, but in practice I have not seen people actually doing that regularly.

It's easy to get into a situation where you have multiple soft-deleted versions of every record. You may find that you have more deleted data than live data! One alternative to soft-deletes is to put these records into a separate archive. It could even be another RDBMS. If you really ever do need the data, it will be there. But don't be surprised if you never use it.

# Foreign Key Constraints

There seems to be a misunderstanding that "Real Internet Applications Don't Use Foreign Keys" ([source]( http://www.thisblog.runsfreesoftware.com/?q=2009/03/20/real-internet-applications-dont-use-foreign-keys)). Let me assure you, foreign key constraints are an absolutely fundamental building block of most of the web apps that you use. It's what the "relational" in RDBMS stands for!

Foreign keys are the primary method for enforcing data integrity. Without them, you are inviting [orphaned rows and giving up cascading deletes](http://stackoverflow.com/questions/83147/whats-wrong-with-foreign-keys). These are similar trade-offs to use soft deletes. In fact, soft deletes can [exacerbate the issue](http://stackoverflow.com/questions/3492485/mysql-with-soft-deletion-unique-key-and-foreign-key-constraints).

In the end, not using foreign keys is similar to not [validating your input](http://www.oreillynet.com/onlamp/blog/2006/05/misunderstanding_foreign_keys.html
). You're assuming that your infallible application layer will never insert bad data into the system. First of all, that's just wishful thinking. In practice, I have observed that if the schema allows bad data, you will eventually see that exact form of bad data in the system. Better to put as much data validation as you can right next to the data itself, where it is much harder to circumvent.

# Transactions

[ACID](http://en.wikipedia.org/wiki/ACID) compliance is a big deal. Databases competed on this playing field for decades. Yes, transactions absolutely do slow down performance. Would you rather have wrong answers quickly, or correct answers a few milliseconds later?

Yes, transactions [can throw errors](http://jasonswett.net/blog/why-you-should-use-database-transactions/
) when you are inserting data. You can't insert bad data; that's the point! When you say you want to disable transactions because "I don't ever want to loose data", I hear "I would rather have bad data in the system than no data". (Application layer isn't looking so infallible now, is it?) In general, transactions reduce the scope of data problems from "I just inserted a bunch of invalid data, let's fix the 'bugs' in the application layer to deal with it" to "one user got an error trying to insert bad data". IMHO, that's a good thing.

# JSON Data

Like all of these anti-patterns, putting JSON data into your relational database is fine in small doses. I actually think it's advisable when dealing will small bits of schema-less data. But it should be the exception, not the rule. It's all too easy to avoid the small up-front cost of parsing the data and defining a schema, only to find that you're fighting bugs in your application when you're trying to do just that on the fly per-request.

- You're relying on your application layer to validate the format; the database can't even check that it IS JSON. (Unless you use [Postgres](http://www.postgresql.org/docs/devel/static/datatype-json.html))
- You can't index inside this field.
- You are probably storing these as TEXT to account for their in determinant length; MySQL in particular can't do [standard optimizations](http://dev.mysql.com/doc/refman/5.1/en/internal-temporary-tables.html
) on tables with TEXT blobs.

Note: the later is also [not a problem](http://stackoverflow.com/questions/348416/in-postgresql-is-it-faster-to-include-text-columns-in-the-same-table-rather-th
) on Postgres.

# Conclusion

In the final analysis, poor data integrity is really all about _SPEED_. Not the speed of your application, but the speed of your engineers. Soft deletion, disabling foreign keys, eschewing transactions and not normalizing data properly all have their valid use cases. But over-used, you're slowing down every engineer that has to write new code on top of the database by inundating them with edge cases they frankly shouldn't have to worry about.

They have a reference to an active user, but the required profile record is soft-deleted. Add more code to deal with that. I tried to show the user a link from an invoice to their internal CRM with a reference_id, but that key was missing from the json column. Add more code to deal with that. Not to mention volume of bugs that can be traced back to data integrity issues.
