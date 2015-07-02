---
layout: post
title: How to write effective unit tests
tags: testing
---

Unit tests differs from integration testing primarily in terms of what you're testing for. Where as with integration tests, you testing for whether the entire system behaves as expected when put together, with unit tests, your goal is simply to enable refactoring with confidence. Ideally, when you refactor something and it's broken, at least one unit test fails. But when you refactor something and it's working, unit tests pass.

Integration tests are naturally  *high leverage*; you can typically test a large swath of functionality with not much code. But they also are typically slower to run, test fewer edge cases and tend to not give you a very good idea of what is broken when they fail. To make sure your unit tests are complimentary, you want to make sure they are fast, test many edge cases, and test only one thing so you know what's broken when they fail.


## What not to do

It's common to have a large set of unit tests written that don't actually add much value. If you have many unit tests testing the same thing implicitly, then they will all fail at the same time. For example, you're testing all your Flask views, and many of them have a decorator to test if the user is logged in. If you break that decorator, many tests will fail. Ideally, you want to test the decorator itself in one set of tests, and then have the rest of your tests mock that out.

In the later case, what happens when you go to refactor how login works? Hopefully, you only have to update a handful of tests. Going through the process of mocking things out and only testing one unit at a time will also improve the quality of the code itself. You will see how your components could be designed better for separation of concerns, so that they are testable separately.

Some common anti-patterns:

- Unit tests for one unit of code allow that code to actually call into all it's dependencies
- Unit tests load a large database before they start
- Unit tests are slow, so you hate adding more and running them
- Assert on many things in one test, or assert on an entire nested JSON object, which is the same thing
    - Just think of what will happen if you ever change that JSON schema
- Forget to test branches in your code's logic
- Tests are verbose


## What to do, instead

- Mock other parts of the code base
- Mock database access when you can
    - or, make sure database access in your tests is fast to setup and reset between tests
    - you can leverage database transactions for this
- Devise a mechanism to run just one test, or a small set of tests, on demand
- Every logical branch in your code gets its own unit test
- Tests employ same DRY principles as any other code


## Example: a Flask app

Here is an example Flask app with a fictional ORM layer.

```python
from flask import Flask
from flask.json import jsonify

app = Flask(__name__)

@app.route('/user/<int:user_id'>/)
def get_user(user_id):
    if not request.user:
        return jsonify({'error': 'You are not logged in'})
    try:
        user = User.objects.get(id=user_id)
    except NotFoundError as e:
        return jsonify({'error': e})
    return jsonify(dict(id=user.id, name=user.name, email=user.email))
```

What tests would you want to write for this code, and how would they keep isolated from the rest of your code?

- Test that if you make do a `GET /user/1` that your view is called with a `user_id` of 1.
    - You *don't* need to test `@app.route` per say, but you do need to test that the part you have customized (the URL) is working.
    - Test what happens when you call this route with a non-integer.
    - Just verify that `get_user` is called with the right parameter, do NOT execute the body in this test. If you did, a breakage there would fail this test as well as subsequent tests.
    - For example, what if you misspelled `/user`, or forgot to specify that `user_id` was an `int`.
- Test what gets returned if `request.user` is NOT defined. That's a branch in your code.
    - If you turned that into a decorator, you would just want to verify that the decorator executed, but you could defer the testing of the logic to tests for that component. This is an example of improving your component design via testing.
- Test what happens if the `user_id` is not found.
- Test the return value of a successful call.
    - Again, this could be made better by having a `User.to_json()` method which is tested separately.
    - In that case, you would just assert that the return value is equal to `User.to_json()`, not what the actual JSON is.

For some of these test cases, you will need to actually create a record in the database for that `user_id` first. Your testing framework should give you a convenient place to do that. Again, the best way to do that is to write code to create just the record you need for this set of tests, versus running your tests against a full database backup. The later can be quite hard to maintain, and is generally slower.
