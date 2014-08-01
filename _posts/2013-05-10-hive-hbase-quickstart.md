---
layout: post
title: Hive with HBase Quickstart
tags: hbase hive
---

Though there is some [decent documentation](https://cwiki.apache.org/confluence/display/Hive/HBaseIntegration), I found that setting up Hive with a HBase back-end to be somewhat fiddly. Hopefully this guide will help you get started quicker. This article presumes that you already have HBase set up. If not, see my [HBase quickstart](http://chase-seibert.github.io/blog/2013/02/01/getting-starting-with-hbase-and-pig.html).

Note: these directions are for development. They don't use HDFS, for example. For a full guide on production deployment, see the excellent [CDH4 directions](http://www.cloudera.com/content/cloudera-content/cloudera-docs/CDH4/latest/CDH4-Installation-Guide/cdh4ig_topic_18.html).

## Linux

{% highlight bash %}
sudo apt-get install hive

# create directory that Hive stores data in by default
sudo mkdir -p /user/hive/warehouse
sudo chown -R myusername:myusername /user/hive/warehouse/

# copy HBase JARs into the Hive lib
sudo cp /usr/share/hbase/hbase-0.92.1.jar /usr/lib/hive/lib
sudo cp /usr/share/hadoop-zookeeper/zookeeper-3.4.3.jar /usr/lib/hive/lib
{% endhighlight %}

## OSX

{% highlight bash %}
brew install hive
{% endhighlight %}

## Connect to HBase

Now, you can fire up hive with the `hive` command and create a table that's backed by HBase. For this example, my HBase table is called `test`, and has a column family of integer values called `values`. Note that the dropping/creating of tables is just effecting Hive meta-data; no actual changes are made in HBase.

{% highlight bash %}
DROP TABLE IF EXISTS test;

CREATE EXTERNAL TABLE
    test(key string, values map<string, int>)
STORED BY
    'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
WITH SERDEPROPERTIES (
    "hbase.columns.mapping" = ":key,values:"
    )
TBLPROPERTIES (
    "hbase.table.name" = "test"
    );

SELECT * FROM test;

>c4ca4-0000001-79879483-000000000124-000000000000000000000000000025607621 {'comments':0, 'likes':0}
>c4ca4-0000001-79879483-000000000124-000000000000000000000000000025607622 {'comments':0, 'likes':0}
{% endhighlight %}

## Simple Map Reduce Example

Give the above raw data in the table, here is example GROUP/SUM map reduce where you sum up the various HBase columns in the values column family. This example creates a view to handle the blowing apart of the HBase rowkey. You can use an `INSERT OVERWRITE` statement at the end to write the results back into Hbase.

{% highlight bash %}
CREATE VIEW
    test_view AS
SELECT
    substr(key, 0, 36) as org_date_asset_prefix,
    split(key, '-')[2] as inverse_date_str,
    stats['comments'] as comments,
    stats['likes'] as likes
FROM
    test;

SELECT
    org_date_asset_prefix,
    map(
      'comments', SUM(comments),
      'likes', SUM(likes)
    ) as stats
FROM
    test_view
GROUP BY
    org_date_asset_prefix;
{% endhighlight %}

## Thrift REST API

If you want to connect to Hive via thrift, you can start the thrift service with `hive --service hiveserver`. [Hiver](https://github.com/tebeka/hiver) is a nice little Python API wrapper.

{% highlight python %}
import hiver
client = hiver.connect(host, port)
client.execute('SHOW TABLES')
rows = client.fetchAll()
{% endhighlight %}
