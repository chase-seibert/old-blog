---
layout: post
title: Per-request Query Caching in Django
tags: python cache
---

The Django ORM is a wonderful thing. It makes it so easy to access the database, that sometimes you forget that it's even happening. That is, until you open [django-debug-toolbar](https://github.com/django-debug-toolbar/django-debug-toolbar) and see that you're suddenly running hundreds of queries! Not only that, but looking at the actual queries, many of them are duplicates! You think "Where did all these queries come from? Stupid coworkers, not writing efficient code!" Then you inevitably realize that half of the extra queries were ones you wrote yourself. How does this happen?

It's all too easy. Maybe you have a `User` object with a helper method on it that performs a join to get their recent activity. You're passing `user` instances around in many of your method calls. So as not to assume a wider contract than necessary with the caller, utility methods all over the place are calling this helper method. Your code is nice and tight; you're not repeating yourself anywhere, but some page requests are calling this function from various places in the stack half a dozen times!

Why is this a big deal? After the first query, the database will probably have a nice warm version in its cache. What you will likely see in the debug toolbar is that many of your duplicate queries will return in less than 2 milliseconds. However, any latency to the database server [can still kill you](http://chase-seibert.github.com/blog/2011/10/07/django-performance-latency-kills.html). Plus, even tiny queries are still causing some contention and load on the database.

There are [various](http://packages.python.org/johnny-cache/) [existing](https://github.com/dziegler/django-cachebot) [solutions](http://pypi.python.org/pypi/django-cache-machine) for query caching in Django. In general, they all require that you expire cache results manually if you have edge cases like writing data to your database. In other words, they are likely to introduce bugs.

What I have come up with is a monkey-patch for some Django internals to cache the results of individual SQL statements, but only inside the life cycle of a single request. This will take zero load off of your database if you have perfect code. For mere mortals, it could likely reduce your database calls significantly.

You start by adding a piece of middlware:

{% highlight python %}
from myapp.utils import query_cache


class QueryCacheMiddleware:
    def process_request(self, request):
        query_cache.patch()
{% endhighlight %}

Then, you have to enable that middleware in `settings.py`:

{% highlight python %}
 MIDDLEWARE_CLASSES = (
    ...
    'myapp.middleware.QueryCacheMiddleware',
{% endhighlight %}

Finally, here is the `query_cache` patch itself.

{% highlight python %}
'''
Hack to cache SELECT statements inside a single Django request. The patch() method replaces
the Django internal execute_sql method with a stand-in called execute_sql_cache. That method
looks at the sql to be run, and if it's a select statement, it checks a thread-local cache first.
Only if it's not found in the cache does it proceed to execute the SQL. On any other type of
sql statement, it blows away the cache. There is some logic to not cache large result sets,
meaning anything over 100 records. This is to preserve Django's lazy query set evaluation.
'''
from threading import local
import itertools
from django.db.models.sql.constants import MULTI
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.datastructures import EmptyResultSet
from django.db.models.sql.constants import GET_ITERATOR_CHUNK_SIZE


_thread_locals = local()


def get_sql(compiler):
    ''' get a tuple of the SQL query and the arguments '''
    try:
        return compiler.as_sql()
    except EmptyResultSet:
        pass
    return ('', [])


def execute_sql_cache(self, result_type=MULTI):

    if hasattr(_thread_locals, 'query_cache'):

        sql = get_sql(self)  # ('SELECT * FROM ...', (50)) <= sql string, args tuple
        if sql[0][:6].upper() == 'SELECT':

            # uses the tuple of sql + args as the cache key
            if sql in _thread_locals.query_cache:
                return _thread_locals.query_cache[sql]

            result = self._execute_sql(result_type)
            if hasattr(result, 'next'):

                # only cache if this is not a full first page of a chunked set
                peek = result.next()
                result = list(itertools.chain([peek], result))

                if len(peek) == GET_ITERATOR_CHUNK_SIZE:
                    return result

            _thread_locals.query_cache[sql] = result

            return result

        else:
            # the database has been updated; throw away the cache
            _thread_locals.query_cache = {}

    return self._execute_sql(result_type)


def patch():
    ''' patch the django query runner to use our own method to execute sql '''
    _thread_locals.query_cache = {}
    if not hasattr(SQLCompiler, '_execute_sql'):
        SQLCompiler._execute_sql = SQLCompiler.execute_sql
        SQLCompiler.execute_sql = execute_sql_cache
{% endhighlight %}

What's going on here is that I'm replacing the Django internal `execute_sql` method with a wrapper that caches results in a thread local dictionary. It only caches small result sets. For any result more that 100 rows, Django will fire up a database cursor and a generator. Caching those without eagerly querying for the entire dataset would be [quite tricky](http://jeffelmore.org/2010/09/25/smarter-caching-of-django-querysets/), so I bail in that case. I have noticed that in my codebase, the majority of repeated calls are for a single record, or a small set of records.

So as not to have to deal with any tricky invalidation cases, I simply delete the cache if any UPDATE, INSERT or DELETE statement is run.

Of course, this will not work if you have long running page requests that purposely make the same request over and over, waiting for a particular result.
