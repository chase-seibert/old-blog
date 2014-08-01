---
layout: post
title: Flatten entire HBase column families with Pig and Python UDFs
tags: hbase pig
---

Most [Pig](http://pig.apache.org/) tutorials you will find assume that you are working with data where you know all the column names ahead of time, and that the column names themselves are just labels, versus being composites of labels and data. For example, when working with [HBase](http://hbase.apache.org/), it's actually not uncommon for both of those assumptions to be false. Being a columnar database, it's very common to be working to rows that have [thousands of columns](https://issues.apache.org/jira/browse/HBASE-867). Under that circumstance, it's also common for the column names themselves to encode to dimensions, such as [date and counter type](https://www.facebook.com/video/video.php?v=707216889765).

How do you solve this mismatch? If you're in the early stages of designing a schema, you could reconsider a more row based approach. If you have to work with an existing schema, however, you can with the help of [Pig UDFs](http://ofps.oreilly.com/titles/9781449302641/udf_lists.html).

Say we have the following table:

<table>
    <tr>
        <th>rowkey</th>
        <th>cf1:20130101post</th>
        <th>cf1:20130101comment</th>
        <th>cf1:20130101like</th>
        <th>cf1:20130102post</th>
        <th>...</th>
    </tr>
    <tr>
        <td>ce410-00005031-00089182</td>
        <td>147</td>
        <td>5</td>
        <td>41</td>
        <td>153</td>
    </tr>
    <tr>
        <td>ce410-00005031-00021915</td>
        <td>1894</td>
        <td>33</td>
        <td>86</td>
        <td>1945</td>
    </tr>
    <tr>
        <td>5faa4-00009521-00019828</td>
        <td>30</td>
        <td>2</td>
        <td>8</td>
        <td>31</td>
    </tr>
    <tr>
        <td>...</td>
    </tr>
</table>

Here there is a composite row key, but also composite column keys. Because the date is part of the column keys, there are potentially many, many columns. Enumerating them all in your Pig scripts in impractical. Notice that they are also in the same column family. To load them all, you can do the following in Pig:

{% highlight sql %}
data = load 'hbase://table_name' using org.apache.pig.backend.hadoop.hbase.HBaseStorage('cf1:*', '-loadKey true') AS (id:chararray, stats:map[int]);
illustrate data;
{% endhighlight %}

This will result in all columns being loaded into a [Pig map](http://pig.apache.org/docs/r0.7.0/piglatin_ref2.html#Data+Types), which is just a collection of tuples:

<pre>
-----------------------------------------------------------------------------------------------------
| data         | id:chararray            | stats:map(:int)                                          |
-----------------------------------------------------------------------------------------------------
|              | ce410-00005031-00089182 | {20130101post=147,20130101comment=5,20130101like=41,...} |
-----------------------------------------------------------------------------------------------------
</pre>

So, now you have loaded all the data, but how to you parse the column names into their respective parts, so you can apply logic to the values? Here is a very simply Python implementation of a UDF that will turn that map into a bag:

{% highlight python %}
@outputSchema("values:bag{t:tuple(key, value)}")
def bag_of_tuples(map_dict):
    return map_dict.items()
{% endhighlight %}

You can include this UDF (place the above in a file called udfs.py in the current working directory for pig), and invoke it like this:

{% highlight sql %}
register 'udfs.py' using jython as py
data = load 'hbase://table_name' using org.apache.pig.backend.hadoop.hbase.HBaseStorage('cf1:*', '-loadKey true') AS (id:chararray, stats:map[int]);
databag = foreach data generate id, FLATTEN(py.bag_of_tuples(stats));
illustrate databag;
{% endhighlight %}

This is taking advantage of the built-in [FLATTEN](http://pig.apache.org/docs/r0.7.0/piglatin_ref2.html#Flatten+Operator) operator, which takes a bag and does a cross product with bag's row to produce N new rows.

<pre>
------------------------------------------------------------------------------
| databag      | id:chararray            | key:bytearray  | value:bytearray  |
------------------------------------------------------------------------------
|              | ce410-00005031-00089182 | 20130101post    | 147             |
------------------------------------------------------------------------------
|              | ce410-00005031-00089182 | 20130101comment | 5               |
------------------------------------------------------------------------------
|              | ce410-00005031-00089182 | 20130101like    | 41              |
------------------------------------------------------------------------------
</pre>

You can then process your data as normal. You can then write your data bag to HBase in the same format by using the built-in UDFs [TOMAP](http://pig.apache.org/docs/r0.9.1/api/org/apache/pig/builtin/TOMAP.html) and and same * syntax. Assuming you have produced new column names and values in your script, you can do:

{% highlight sql %}
...
mapped = foreach processed_data generate TOMAP(columnname, value) as stats;
store mapped into 'hbase://table_name' using org.apache.pig.backend.hadoop.hbase.HBaseStorage('stats:*');
{% endhighlight %}
