---
layout: post
title: HBase/Pig/Python Quickstart on OSX
tags: hbase pig hadoop python
---

Having spent a good chunk of the last two weeks getting a prototype analytics system running, I thought I would write up my findings. I was pleased to find that installing all the pieces was smooth via [Homebrew](http://mxcl.github.com/homebrew/), but getting them all to play together was less smooth.

# The Playing Field

* [Hadoop](http://hadoop.apache.org/) is an framework for distributed computing. It's also used interchangibly to reference an entire ecosystem of technologies.
- [HDFS](http://en.wikipedia.org/wiki/Apache_Hadoop#Hadoop_Distributed_File_System) is the underlying distributed file ssytem that makes Hadoop possible.
* [HBase](http://hbase.apache.org/) is non-relational data store built on top of Hadoop. It provides concepts like rows, columns and keys. The similarity to relational databases stops there.
* [Zookeeper](http://zookeeper.apache.org/) provides configuration management for Hadoop cluster machines
* [Pig](http://pig.apache.org/) is high level language for map/reduce queries
* [Hive](http://hive.apache.org/) is a SQL-like high level language for map/reduce queries
* [Thrift](http://wiki.apache.org/hadoop/Hbase/ThriftApi) is a REST API for HBase
* [HappyBase](https://github.com/wbolster/happybase) is a python client for Thrift

# Installing

{% highlight bash %}
brew install hadoop hbase pig hive
{% endhighlight %}

# Getting Started with HBase

First, you start the server with `start-hbase.sh`, then you can enter an interactive shell with `hbase shell` and create some test tables. HBase schema is a whole separate discussion. For now, we're going to create a table with a column family of "stats". Our primary keys are going to be in the format `md5(customer id)[:5] + customer id + date`.

{% highlight bash %}
create 'test_table', 'stats'
put 'test_table', 'c41e4:1:20130201', 'stats:count', 100
put 'test_table', 'c41e4:1:20130202', 'stats:count', 102
put 'test_table', 'ed516:2:20130201', 'stats:count', 80
scan 'test_table', {LIMIT=>25}
    ROW                                      COLUMN
     c41e4:1:20130201                        column=stats:count, timestamp=1359402726388, value=100
     c41e4:1:20130202                        column=stats:count, timestamp=1359402786126, value=102
     ed516:2:20130201                        column=stats:count, timestamp=1359402786180, value=80
    3 row(s) in 0.0150 seconds
{% endhighlight %}

Take a look at the full list of [HBase shell commands](http://wiki.apache.org/hadoop/Hbase/Shell).


# Getting Started with Pig

Getting Pig to connect to HBase is a little tricky. It involves some monkeying around with `CLASSPATH` variables. You can run these `export` commands in bash to set everything up properly. Note, this is for a very specific combination of versions, but you can substibute newer versions easily.

{% highlight bash %}
export JAVA_HOME=$(/usr/libexec/java_home)
export HBASE_HOME=/usr/local/Cellar/hbase/0.94.2/
export PIG_CLASSPATH="/usr/local/Cellar/hbase/0.94.2/libexec/conf/hbase-site.xml:/usr/local/Cellar/hbase/0.94.2/libexec/hbase-0.94.2.jar:/usr/local/Cellar/hbase/0.94.2/libexec/lib/zookeeper-3.4.3.jar:/usr/local/Cellar/hbase/0.94.2/libexec/lib/guava-11.0.2.jar:/usr/local/Cellar/hbase/0.94.2/libexec/lib/protobuf-java-2.4.0a.jar"
export HBASE_CONF_DIR=/usr/local/Cellar/hbase/0.94.2/libexec/conf
{% endhighlight %}

## Exporting Data

You can enter the pig shell (aka grunt), by simply running `pig`. You may find it useful if you run into problems to examine pig's classpath with `pip -secretDebugCmd`, and run pig in verbose mode with `pig -debug DEBUG -versbose`.

{% highlight bash %}
data = load 'hbase://test_table' using org.apache.pig.backend.hadoop.hbase.HBaseStorage('stats:count', '-loadKey true') AS (id:chararray, count:chararray);
store data into '/tmp/test_table.csv' using PigStorage(',');
cat /tmp/test_table.csv
grunt>
c41e4:1:20130201,100
c41e4:1:20130202,102
ed516:2:20130201,80
{% endhighlight %}

Note: the last `cat` command is Pig's version of cat. Outside pig, the data is actually stored in a _directory_ called `/tmp/test_table.csv/`, in separate parts files. But they are just regular text files.

## Importing Data

For this example, let's create a larger data set. Here is a simple python script to create a CSV file in the correct format.

{% highlight python %}
import random
for md5, customer_id in (('c41e4', 1), ('ed516', 2), ('a86f4', 3)):
    for month in range(1, 12):
        for day in range(1, 30):
            print '%s:%s:2013%02d%02d,%s' % (md5, customer_id, month, day, random.randint(50, 150))
{% endhighlight %}

You can grab a pre-rendered version and save it locally with `curl -L http://chase-seibert.github.com/blog/files/import.csv > /tmp/import.csv`. Then, you can import it in `pig` like so. One confusing note here is that you don't include the ID field in the store command; that's automatic.

{% highlight python %}
data = load '/tmp/import.csv' using PigStorage(',') AS (id:chararray,count:chararray);
store data into 'hbase://test_table' using org.apache.pig.backend.hadoop.hbase.HBaseStorage('stats:count');
{% endhighlight %}

If you switch back to hbase shell, you should be able to scan and see those records.

## Aggregating with Map/Reduce

There is a [lot](http://pig.apache.org/docs/r0.7.0/piglatin_ref1.html#Using+Comments+in+Scripts) you can do with the built-in [pig latin language](http://pig.apache.org/docs/r0.7.0/piglatin_ref2.html#Overview
). Here is one example, where we are going to get an average count by day for all customers. Because my day is only represented as an encoded portion of my row key, I will break that up as part of the aggregation.


{% highlight python %}
A = load 'hbase://test_table' using org.apache.pig.backend.hadoop.hbase.HBaseStorage('stats:count', '-loadKey true') AS (id:chararray, count:int);
B = foreach A generate id, FLATTEN(STRSPLIT(id, ':')) as (md5:chararray, customer_id:int, date:chararray), count;
C = group B by date;
D = foreach C generate group, AVG(B.count);
dump D;
...
20 seconds later
...
(20130101,63.333333333333336)
(20130102,97.33333333333333)
(20130103,96.66666666666667)
(20130104,94.0)
(20130105,74.0)
(20130106,135.33333333333334)
...
{% endhighlight %}

You could save this dataset back to HBase using `store D into 'hbase://test_table2' using org.apache.pig.backend.hadoop.hbase.HBaseStorage('stats:date stats:count');`. Remember that you need to create the table first.

# Trouble-shooting

If you have not setup your `CLASSPATH` propery (ie, the `export` statements), you may get any one of the following errors:

* `ERROR org.apache.pig.tools.grunt.Grunt - ERROR 2998: Unhandled internal error. org/apache/hadoop/hbase/filter/WritableByteArrayComparable`
