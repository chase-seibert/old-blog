---
layout: post
title: Write CSV data into Hive and Python
tags: python hive
---

[Apache Hive](http://hive.apache.org/) is a high level SQL-like interface to Hadoop. It lets you execute mostly unadulterated SQL, like this:

{% highlight sql %}
CREATE TABLE test_table(key string, stats map<string, int>);
{% endhighlight %}

The `map` column type is the only thing that doesn't look like vanilla SQL here. Hive can actually use different backends for a given table. Map is used to interface with column oriented backends like HBase. Essentially, because we won't know ahead of time all the column names that could be in the HBase table, Hive will just return them all as a key/value dictionary. There are then helpers to access individual columns by key, or even pivot the map into one key per logical row.

As part of the Hadoop family, Hive is focused on bulk loading and processing. So it's not a surprise that Hive does not support inserting raw values like the following SQL:

{% highlight sql %}
INSERT INTO suppliers (supplier_id, supplier_name) VALUES (24553, 'IBM');
{% endhighlight %}

However, for unit testing Hive scripts, it would be nice to be able to insert a few records manually. Then you could run your map reduce HQL, and validate the output. Luckily, Hive can load CSV files, so it's relatively easy to insert a handful or records that way.

{% highlight sql %}
CREATE TABLE foobar(key string, stats map<string, bigint>)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
COLLECTION ITEMS TERMINATED BY '|'
MAP KEYS TERMINATED BY ':' ;

LOAD DATA LOCAL INPATH '/tmp/foobar.csv' INTO TABLE foobar;
{% endhighlight %}

This will load a CSV file with the following data, where `c4ca4-0000001-79879483-000000000124` is the key, and `comments` and `likes` are columns in a map.

{% highlight text %}
c4ca4-0000001-79879483-000000000124,comments:0|likes:0
c4ca4-0000001-79879483-000000000124,comments:0|likes:0
{% endhighlight %}

Because I've been doing this quite a bit in my unit tests, I wrote a quick Python helper to dump a list of key/map tuples to a temporary CSV file, and then load it into Hive. This uses [hiver](https://github.com/tebeka/hiver) to talk to Hive over thrift.

{% highlight python %}
import hiver
from django.core.files.temp import NamedTemporaryFile


def _hql(self, hql):
    client = hiver.connect(settings.HIVE_HOST, settings.HIVE_PORT)
    try:
        client.execute(hql)
    finally:
        client.shutdown()


def insert(self, table_name, rows):
    ''' cannot insert single rows via hive, need to save to a temp file and bulk load that '''
    csv_file = NamedTemporaryFile(delete=True)
    for row in rows:
        map_repr = '|'.join('%s:%s' % (key, value) for key, value in row[1].items())
        csv_file.write(row[0] + "," + map_repr + "\n")
    csv_file.flush()
    try:
        _hql('DROP TABLE IF EXISTS %s' % table_name)
        _hql("""
            CREATE TABLE
                %s (
                    key string,
                    map<string, int>
                )
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            COLLECTION ITEMS TERMINATED BY '|'
            MAP KEYS TERMINATED BY ':'
        """ % (table_name))
        _hql("""
            LOAD DATA LOCAL INPATH '%s' INTO TABLE %s
        """ % (csv_file.name, table_name)
    finally:
        csv_file.close()
{% endhighlight %}

You can call it like this:

{% highlight python %}
    insert('test_table', [
        ('c4ca4-0000001-79879483-000000000124', {'comments': 1, 'likes': 2}),
        ('c4ca4-0000001-79879483-000000000124', {'comments': 1, 'likes': 2}),
        ('c4ca4-0000001-79879496-000000000124', {'comments': 1, 'likes': 2}),
        ('b4aed-0000002-79879783-000000000768', {'comments': 1, 'likes': 2}),
        ('b4aed-0000002-79879783-000000000768', {'comments': 1, 'likes': 2}),
    ])
{% endhighlight %}

