---
layout: post
title: Mocking HappyBase for unit testing HBase code
tags: python hbase
---

[HappyBase](https://github.com/wbolster/happybase) is a friendly interface to interact with [HBase](http://hbase.apache.org/) from Python. It lets you perform basic HBase operations like `get`, `put` and `scan`. But say you have a bunch of puts littered around your code. How do you unit test that? One method would be to mock out the happy base calls themselves, and just assert that they are called with specific parameters. But what if you want to test the final state of the HBase tables after a series of operations?

For that, you can replace the HappyBase `Table` class with a version that keeps the data in memory.

{% highlight python %}
from collections import defaultdict
import unittest
import happybase


class MockTable(object):

    def __init__(self, table_name):
        self.table_name = table_name
        self.data = defaultdict(dict)

    def put(self, row, data):
        self.data[row].update(data)

    def row(self, row, columns=None):
        return self.data[row]

    def scan(self, **options):
        ''' does not respect any options like start/stop row '''
        return self.data.items()


class MockConnection(object):
    ''' singleton object, so that multiple HBaseTables can collaborate '''

    _instance = None
    tables = dict()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MockConnection, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, *args, **kwargs):
        pass

    def is_table_enabled(self, name):
        return True

    def table(self, name):
        table = self.tables.get(name)
        if not table:
            table = MockTable(name)
            self.tables[name] = table
        return table

    def flush(self):
        self.tables = dict()


class HBaseTestCase(unittest.TestCase):
    ''' mock out calls to hbase
    if you over-ride setUp(), make sure to call super '''

    def setUp(self):
        happybase._Connection = happybase.Connection
        happybase.Connection = MockConnection
        MockConnection().flush()

    def tearDown(self):
        happybase.Connection = happybase._Connection
{% endhighlight %}

To use it, just have your unit test class extend `HBaseTestCase`.

{% highlight python %}
import happybase


class HappybaseMockTests(HBaseTestCase):

    def setUp(self):
        connection = happybase.Connection()
        self.table = connection.table('table-name')
        super(HappybaseMockTests, self).setUp()

    def test_put(self):
        self.table.put('row1', {'cf1:col1': '1', 'cf1:col2': '2', 'cf2:col1': '3'})
        self.assertEquals(self.table.row('row1'), {'cf1:col1': '1', 'cf1:col2': '2', 'cf2:col1': '3'})

    def test_scan(self):
        self.table.put('row1', {'cf1:col1': '1'})
        self.table.put('row1', {'cf1:col2': '2'})
        self.table.put('row2', {'cf2:col1': '3'})
        self.assertEquals(self.table.scan(), [('row1', {'cf1:col1': '1', 'cf1:col2': '2'}), ('row2', {'cf2:col1': '3'})]

{% endhighlight %}

*Note:* this version does not force you to use valid column families, it just created families on the fly as you put columns in. It also does not support any of the options on `scan`, such as filtering by a range of rowkeys. Some of those options could be added easily. Others would be very difficult, such as java based column filters. Hopefully this is enough you get you started testing your HBase code.
