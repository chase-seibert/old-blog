---
layout: post
title: Happybase Connection Pooling
tags: python hbase
---

Wrote a simple connection pool for [Happybase](https://github.com/wbolster/happybase) using [socketpool](https://pypi.python.org/pypi/socketpool).

{% highlight python %}
import time
import random
import contextlib
import happybase
from socketpool import ConnectionPool
from socketpool.conn import TcpConnector


class HappybaseConnectionPool(object):
    ''' singleton to share a connection pool per process '''

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(HappybaseConnectionPool, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, host, **options):
        options['host'] = host
        if not hasattr(self, 'pool'):
            self.pool = ConnectionPool(
                factory=HappybaseConnector,
                max_size=options.get('max_size', 10),
                options=options,
            )

    def connection(self, **options):
        return self.pool.connection(**options)

    @contextlib.contextmanager
    def table(self, table_name):
        with self.pool.connection() as connector:
            yield connector.table(table_name)


class HappybaseConnector(TcpConnector):

    def __init__(self, host, port, pool=None, **kwargs):
        self.host = host
        self.port = port
        self.connection = happybase.Connection(self.host, self.port)
        self._connected = True
        # use a 'jiggle' value to make sure there is some
        # randomization to expiry, to avoid many conns expiring very
        # closely together.
        self._life = time.time() - random.randint(0, 10)
        self._pool = pool
        self.logging = kwargs.get('logging')

    def is_connected(self):
        if self._connected and self.connection.transport.isOpen():
            try:
                # isOpen is unreliable, actually try to do something
                self.connection.tables()
                return True
            except:
                pass
        return False

    def handle_exception(self, exception):
        if self.logging:
            self.logging.error(exception)
        else:
            print exception

    def invalidate(self):
        self.connection.close()
        self._connected = False
        self._life = -1

    def open(self):
        pass

    def close(self):
        self.release()

    def __getattr__(self, name):
        if name in ['table', 'tables', 'create_table', 'delete_table',
                'enable_table', 'disable_table', 'is_table_enabled', 'compact_table']:
            return getattr(self.connection, name)
        else:
            raise AttributeError(name)
{% endhighlight %}

You can get a single pool object from anywhere in your stack with the following:

{% highlight python %}
pool = HappybaseConnectionPool('localhost', '9090')
with pool.connection() as connection:
     connection.create_table('foobar')
{% endhighlight %}

Note: happybase may be adding their [own connection pool](https://github.com/wbolster/happybase/issues/21) shortly.
