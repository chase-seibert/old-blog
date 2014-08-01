---
layout: post
title: Sqoop/HBase Quickstart on Linux
tags: sqoop hadoop hbase
---

[Sqoop](http://sqoop.apache.org/) is a tool for bulk copying data between a relational database like MySQL and HDFS or another Hadoop based data store like Hive or HBase. It can either export a table or set of tables, or you can specify a custom SQL query to pull the data out. It's the best solution out there for moving massive data sets; it can even fan out sqoop workers to a configurable number of Hadoop data nodes, which will all run partitioned versions of the main SQL query in parallel.

# Install

To get started, you will need to install Sqoop. The easiest method on Linux is to use the [Cloudera](http://www.cloudera.com/content/cloudera-content/cloudera-docs/CDH4/latest/CDH4-Installation-Guide/CDH4-Installation-Guide.html) repository. You will also need the JDBC MySQL driver, and the JDK (Sqoop compiles a JAR on the fly and sends it out as a MapReduce job).

{% highlight bash %}
cat <<EOF >> /etc/apt/sources.list.d/cloudera.list
deb [arch=amd64] http://archive.cloudera.com/cdh4/ubuntu/precise/amd64/cdh precise-cdh4 contrib
deb-src http://archive.cloudera.com/cdh4/ubuntu/precise/amd64/cdh precise-cdh4 contrib
EOF
curl -s http://archive.cloudera.com/cdh4/ubuntu/lucid/amd64/cdh/archive.key| sudo apt-key add -
sudo apt-get update
sudo apt-get install sqoop libmysql-java openjdk-7-jdk
{% endhighlight %}

# Run it!

Say you have a MySQL table `user` and a HBase table with the same name. If you want to do a straight copy of the data and use the `id` column as the HBase rowkey and store all the columns in a HBase column family named `data`, all you need to do is:

{% highlight bash %}
sqoop-import --connect jdbc:mysql://$MYSQL_SERVER/$DATABASE --driver com.mysql.jdbc.Driver --username $USER --password $PASSWORD --table user --hbase-table user --hbase-row-key id --column-family data
{% endhighlight %}

At least for HBase, you are almost always want to compose some more sophisticated rowkey, to avoid [region hotspotting](http://my.safaribooksonline.com/book/databases/database-design/9781449314682/optimizing-splits-and-compactions/id3163684). If you can express that rowkey as a SQL statement, you're good to go. Instead of `--table`, you specify a `--query`, and change the column referenced in `--hbase-row-key`.

Say we want the rowkey to be the first five characters of the md5 hash of the `company_id` field in the `user` table, plus the `date_added` field formatted as an eight character string, plus the `id` field. Example: `a8f5c-20130101-47`.

{% highlight bash %}
sqoop-import --connect jdbc:mysql://$MYSQL_SERVER/$DATABASE --driver com.mysql.jdbc.Driver --username $USER --password $PASSWORD --hbase-table user --hbase-row-key id --column-family data --query "SELECT  CONCAT_WS('-', SUBSTR(MD5(a.company_id), 1, 5), DATE_FORMAT(a.date_added, '%Y%m%d'), a.id) as rowkey, a.* FROM user a WHERE \$CONDITIONS"
{% endhighlight %}

_Note: the `$CONDITIONS` is a placeholder for the dynamic partitioning of data across server. You may also need to specify a `--split-by` column._

# Tuning

For a large number of rows, you may find that Sqoop is using a lot of memory to copy the data over. You may even run into a `java.lang.OutOfMemoryError: Java heap space` or a `java.lang.OutOfMemoryError: GC overhead limit exceeded`. If you do, it's likely because the MySQL database driver is fetching all of the rows of the table, and keeping them in memory. You can tell it to chunk up the query into pages and use a cursor by changing the connect string to: `mysql://$MYSQL_SERVER/$DATABASE?dontTrackOpenResources=true\&defaultFetchSize=1000\&useCursorFetch=true`. See the [documentation](http://dev.mysql.com/doc/refman/5.1/en/connector-j-reference-configuration-properties.html).

# Trouble-shooting

If you get an error saying that sqoop cannot load the MySQL driver, you may need to do a manual `sudo cp /usr/share/java/mysql.jar /usr/lib/sqoop/lib` to copy it to the right place.

If you get the error `0000-00-00 00:00:00' can not be represented as java.sql.Timestamp`, you should modify your connect string to add the `zeroDateTimeBehavior` flag, ie `mysql://$MYSQL_SERVER/$DATABASE?zeroDateTimeBehavior=convertToNull`
