---
layout: post
title: Using HBase/Thrift through the Rackspace Load Balancer
tags: hbase
---

Using the binary [Thrift](http://thrift.apache.org/) protocol through a load balancer can be a little tricky. While it works out of the box in [HAProxy](http://blog.milford.io/2011/07/productionizing-the-hive-thrift-server/), you may run into some slight trouble running it through other load balancers. By default, when trying to access Thrift through the [Rackspace Cloud Load Balancers](http://www.rackspace.com/cloud/load-balancing/), you may get the following exception:

{% highlight bash %}
Traceback (most recent call last):

File "/usr/local/lib/python2.6/dist-packages/Django-1.2-py2.6.egg/django/core/handlers/base.py",
line 100, in get_response
response = callback(request, *callback_args, **callback_kwargs)
...
File "/usr/local/lib/python2.6/dist-packages/Thrift-0.2.0-py2.6-linux-x86_64.egg/thrift/protocol/TBinaryProtocol.py",
line 126, in readMessageBegin
sz = self.readI32()

File "/usr/local/lib/python2.6/dist-packages/Thrift-0.2.0-py2.6-linux-x86_64.egg/thrift/protocol/TBinaryProtocol.py",
line 203, in readI32
buff = self.trans.readAll(4)

File "/usr/local/lib/python2.6/dist-packages/Thrift-0.2.0-py2.6-linux-x86_64.egg/thrift/transport/TTransport.py",
line 58, in readAll
chunk = self.read(sz-have)

File "/usr/local/lib/python2.6/dist-packages/Thrift-0.2.0-py2.6-linux-x86_64.egg/thrift/transport/TTransport.py",
line 155, in read
self.__rbuf = StringIO(self.__trans.read(max(sz, self.DEFAULT_BUFFER)))

File "/usr/local/lib/python2.6/dist-packages/Thrift-0.2.0-py2.6-linux-x86_64.egg/thrift/transport/TSocket.py",
line 94, in read
raise TTransportException(type=TTransportException.END_OF_FILE,
message='TSocket read 0 bytes')

thrift.transport.TTransport.TTransportException: TSocket read 0 bytes
{% endhighlight %}

After playing around with the [HappyBase](https://github.com/wbolster/happybase) connection `transport` [settings](http://happybase.readthedocs.org/en/latest/api.html#connection), I was able to rule out [framed versus binary transport](https://github.com/wbolster/happybase/issues/6) as the issue. I was also able to verify that a connection directly to the machine worked. 

The issue turned out to be a setting on the Rackspace load balancer.

![Rackspace Load Balancer TCP Client First](/blog/images/rackspace_lb.png)

The default TCP protocol, called simply "TCP", did not work. By changing the setting to "TCP (Client First)", HappyBase was able to connect via Thrift.

What does this setting do? The [Rackspace documentation](http://docs.rackspace.com/loadbalancers/api/v1.0/clb-devguide/content/List_Load_Balancing_Protocols-d1e4269.html) simply says "This protocol is similiar to TCP, but is more efficient when a client is expected to write the data first". This would seem to hint that the regular TCP option attemps to read from the server socket when a client connects, where-as as an RPC protocol, Thrift [expects the client](http://en.wikipedia.org/wiki/Apache_Thrift) to send the first data packet.
