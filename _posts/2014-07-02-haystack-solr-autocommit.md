---
layout: post
title: Enabling SOLR autocommit with a custom Haystack backend
tags: python haystack solr
---

By default [Django Haystack](http://haystacksearch.org/) makes updates to your Solr index available for
searching immediately. It does this in the simplest way possible, it commits every single update individually.
That can be quite slow. I have an index with 35 million records, and under heavy write load commits of 1,000
records can slow down and take up to 5 seconds for each chunk. In extreme cases, Solr can refuse to accept
that much write load at once, and throw an exception like the following:

{% highlight xml %}
<?xml version="1.0" encoding="UTF-8"?>
<response>
    <lst name="responseHeader">
        <int name="status">503</int>
        <int name="QTime">1492</int>
    </lst>
    <lst name="error">
        <str name="msg">Error opening new searcher. exceeded limit of maxWarmingSearchers=2, try again later.</str>
        <int name="code">503</int>
    </lst>
</response>
{% endhighlight %}

Investigating this error, I turned up a [Stackoverflow post](http://stackoverflow.com/questions/7512945/solr-error-opening-new-searcher-exceeded-limit-of-maxwarmingsearchers-2-try)
basically saying to not make so many commits. That turned up a [Haystack pull request](https://github.com/toastdriven/django-haystack/pull/624)
to make manual commits optional.

You can see the basic issue by looking at the logs that Haystack creates each time it issues a write request to the
Solr REST API:

{% highlight bash %}
Finished 'http://localhost:8080/solr/my_index/update/?commit=true' (post) with body 'u'<add>...' in 0.010 seconds.
{% endhighlight %}

As of Solr 4.0, we have much more performant options for bulk indexing. A [common setup](http://wiki.apache.org/solr/NearRealtimeSearch)
is to use `autocommit` (set by default to 15 seconds) and abstain from manually committing by passing `commit=false` on
the REST API URL. Though Haystack supports passing a commit boolean to the various back-end implementations of `update`,
`remove` and `clear`, this parameter is never explicitly set. Instead, you can [implement your own](http://www.wellfireinteractive.com/blog/custom-haystack-elasticsearch-backend/)
search back-end subclass to pass this value.


{% highlight python %}
from haystack.backends.solr_backend import SolrEngine, SolrSearchBackend


class AutoCommitSolrSearchBackend(SolrSearchBackend):

    def update(self, index, iterable, commit=False):
        super(AutoCommitSolrSearchBackend, self).update(index, iterable, commit=commit)

    def remove(self, obj_or_string, commit=False):
        super(AutoCommitSolrSearchBackend, self).remove(obj_or_string, commit=commit)

    def clear(self, models=[], commit=False):
        super(AutoCommitSolrSearchBackend, self).clear(models, commit=commit)


class AutoCommitSolrEngine(SolrEngine):
    ''' the built-in Solr engine in Haystack performs a manual commit after each update/add/remove/clear. This
    is really slow. Solr is configured by default to auto-commit changes every 15 seconds, so there is no need to
    commit manually on every update.
    '''
    backend = AutoCommitSolrSearchBackend
{% endhighlight %}

Then you can use this new `AutoCommitSolrEngine` in your `HAYSTACK_CONNECTIONS` setting.

{% highlight python %}
HAYSTACK_CONNECTIONS = {
     'default': {
         'ENGINE': 'myapp.serach.AutoCommitSolrEngine',
         'URL': 'http://localhost:8080/solr/my_index',
     }
}
{% endhighlight %}

**Note: By default, indexed items will not show up in searches right away. That's what soft-commit is for.**

> Hard commits are about durability, soft commits are about visibility. [Understanding Transaction Logs, Soft Commit and Commit in SolrCloud - Erick Erickson](http://searchhub.org/2013/08/23/understanding-transaction-logs-softcommit-and-commit-in-sorlcloud/)

To make your auto-committed items available to search in a timely fashion, you must set a `autoSoftCommit.maxTime`
in your Solr config. This is *NOT* set by default.

{% highlight xml %}
    <!-- softAutoCommit is like autoCommit except it causes a
         'soft' commit which only ensures that changes are visible
         but does not ensure that data is synced to disk.  This is
         faster and more near-realtime friendly than a hard commit.
      -->
    <autoSoftCommit>
      <maxTime>1000</maxTime>
    </autoSoftCommit>
{% endhighlight %}

Alternately, you can set `autoCommit.openSearcher` to `true`, which will cause a new searcher worker to be instantiated
every time you auto-commit. This could slow down the first searches that come in after an auto commit, however.
