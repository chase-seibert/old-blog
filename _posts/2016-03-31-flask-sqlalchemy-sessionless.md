---
layout: post
title: Abstracting away session handling in Flask/SQLAlchemy
---

Having used the Django ORM for years, I appreciate the power of the SQLAlchemy ORM. Many complicated SQL queries that are not possible to express in a single Django QuerySet are possible in SQLAlchemy. But one thing I do not appreciate is the requirement to explicitly handle sessions all the time. It's another power feature; sometimes you need to manage your own sessions. But for web apps, most of the time the session should be tied to the request life cycle; the session should only be committed if the request returns a 200 status code, any errors should roll back the session. Also, passing the session around everywhere in your stack is just a pain.

In my apps, I have fallen into a interesting pattern. I use the [declarative base](http://docs.sqlalchemy.org/en/rel_0_8/orm/extensions/declarative.html) method of defining my Models. This allows me to not explicitly invoke a session for read queries. For writes, I actually implement methods on my base declarative object.

```python
from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine('sqlite://')
session = scoped_session(sessionmaker(autocommit=False, bind=engine))


class MyBase(object):

    def save(self):
        session.add(self)
        self._flush()
        return self

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save()

    def delete(self):
        session.delete(self)
        self._flush()

    def _flush(self):
        try:
            session.flush()
        except DatabaseError:
            session.rollback()
            raise


MyModel = declarative_base(cls=MyBase)
MyModel.query = session.query_property()
```

Then, all your Models inherit from `MyModel` and you can do things like `UserModel(name='Foo Bar').save()`, or `user = UserModel.query.get(1234); user.update(name='Bat'); user.delete()`. You never have to pass sessions around. Notice that I'm only *flushing* the session, however.


# Commits

When do things get committed? I do that in my Flask middleware:

```python
from sqlalchemy.exc import DatabaseError

from models import session  # this is the same session object defined above


@app.after_request
def session_commit(response):
    if response.status_code >= 400:
        return
    try:
        session.commit()
    except DatabaseError:
        session.rollback()
        raise
    # session.remove() is called for you by flask-sqlalchemy
```

If you go down this path, you will need to remember to commit sessions for non-Flask frameworks. For example, in command line scripts I just import the session and commit it at the end. For celery tasks, I do something like:

```python
class MyTask(Task):

    def __call__(self, *args, **kwargs):
        try:
            return super(MyTask, self).__call__(*args, **kwargs)
        finally:
            session.commit()
```

# Tests

A fun side-effect of this pattern is that your integration tests do not necessarily have to commit anything. Flushing is enough to be able to query for the records in the same transaction, which is typically all you need in tests.

That being said, I do still make sure to tear down sessions and re-create my schema for each test:

```python
from models import engine, session, MyModel


class MyTest(TestCase):

    def setUp(self):
        session.close()
        session.remove()
        MyModel.metadata.drop_all(engine)
        MyModel.metadata.create_all(engine)
        super(MyTest, self).setUp()
```

This mainly is to isolate tests from each other if they are invalidating the session with a DatabaseError, or if they are actually changing schema somehow.
