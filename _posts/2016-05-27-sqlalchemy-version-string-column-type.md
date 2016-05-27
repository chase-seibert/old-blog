---
layout: post
title: SQLAlchemy - Storing Application Version Strings
---

One example of when you might need to store application version numbers in
your database is when you're tracking which users have which versions of a
mobile app installed. In that case, you may want to preserve the ability to
easily sort the version numbers, so you can answer questions like "Which users
have a version greater than or equal to 9.3.2?"

In that case, you have two options. You can store the version number in three
different fields, such as major, minor and revision number. Or, you can pad
the values such that regular string sorting would work. Why? Because otherwise,
the sorting will be incorrect. For example, the string `10.0.0` is less than
the string `9.0.0` because the first character `9` is greater than `1`. This
would be the behavior you would get with a simple
`SELECT * FROM users ORDER BY version DESC;`

For example, the version `9.3.2` might be stored as `0009.0003.0002`. Here is
a drop-in implementation in SQLAlchemy which allows you to only deal with the
"nice" native format in Python, while storing the padded version in the
database.

```python
from sqlalchemy import types


def to_version_string(value):
    if not value:
        return None
    parts = value.split(VERSION_DELIM)
    if len(parts) > VERSION_NUMBER_PIECES:
        raise ValueError('Version string has too many parts')
    while len(parts) < VERSION_NUMBER_PIECES:
        parts.append('0')
    for part in parts:
        try:
            assert str(int(part)) == part
        except (ValueError, AssertionError):
            raise ValueError('Version part is not an integer')
    return VERSION_DELIM.join([part.zfill(4) for part in parts])


def from_version_string(value):
    if not value:
        return None
    parts = value.split(VERSION_DELIM)
    return VERSION_DELIM.join([str(int(part)) for part in parts])


class VersionString(types.TypeDecorator):
    """ stores a string like '0.9.4' as '0000.0009.0004' so it can be sorted """

    impl = types.String

    def process_bind_param(self, value, dialect):
        return to_version_string(value)

    def process_result_value(self, value, dialect):
        return from_version_string(value)
```

And some quick tests:

```python
from unittest import TestCase
from models import to_version_string, from_version_string


class VersionStringTests(TestCase):

    def test_to_version_string(self):
        self.assertEquals(to_version_string('9.3.2'), '0009.0003.0002')
        self.assertEquals(to_version_string('9.3'), '0009.0003.0000')
        self.assertEquals(to_version_string('9'), '0009.0000.0000')
        self.assertEquals(to_version_string(''), None)
        self.assertEquals(to_version_string(None), None)

    def test_to_version_string_bad(self):
        for value in [
            '9.3.2.1',
            '9.3.a',
            '9.03.2',
            'foobar',
        ]:
            with self.assertRaises(ValueError):
                to_version_string(value)

    def test_from_version_string(self):
        self.assertEquals(from_version_string('0009.0003.0002'), '9.3.2')
        self.assertEquals(from_version_string('0000.0000.0000'), '0.0.0')
        self.assertEquals(from_version_string(None), None)

```
