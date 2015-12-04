---
layout: post
title: Comparison of Chat Message Platforms
---

If you're writing a chat app, the first big question to consider is whether you are going to write the actual chat backend. Why would you want to? You would get complete control over the functionality, reliability and interface. Why would you *not* want to? Well, persistent socket systems that scale to thousands or hundreds of thousands of users are no small undertaking. Plus, a bunch of good platforms already exist. It probably comes down do whether chat is part if your core business. If you're Snapchat, you probably want to write your own chat platform. If chat is just a feature you use to deliver your actual value, it probably does not make sense to spend the engineering time on it.

What platforms exist that could be used to write a chat app, and how do they stack up? Here is a rundown as of late 2015. My criteria is specific to what I'm trying to build:

- Excellent documentation is a must.
- iOS, Node and Python SDKs preferred.
- iOS notifications.
- Web hooks (so we can use stateless web servers).
- Chats with more than two participants.
- Need to be able to extend the messages with custom metadata.
- End-to-end message encryption would be ideal.
- Proven ability to handle a large number of sessions.

I evaluated eight platforms, and seriously considered three options before making a final decision.


# Also Rans

These platforms *could* be used to create a chat app, but all had various glaring issues.

- [Telegram](https://telegram.org/) - No SDKs, just a REST APIs and a bunch of iOS code you can refactor to meet your needs. Hey guys, I don't want to write HTTP request code manually for three platforms!
- [Intercom.io](https://www.intercom.io/) - Their primary focus is providing a call center chat app themselves, not enabling you to build your own app. As far as I could tell, chats were always one to one.
- [Pusher](https://pusher.com/) - They do much more than chat, not focused on that. No iOS notification support.
- [Firebase](https://www.firebase.com/) - They do *much* more than chat, you can build your whole app and deploy it inside their platform. No native chat semantics, you would need to implement everything yourself.
- [Iron.io](http://www.iron.io/) - It's a message queue. No iOS SDK. API is REST, not socket based.


# #3: Quickblox

[Quickblox](https://quickblox.com/) focuse on chat, and on the developer experience (they don't have a chat app themselves). They have been around for a while (2013), and they're based on XMPP, which is an open standard. They have an excellent reference iOS application.

No Python SDK, and no web hooks. But the killer was the difficulty of our prototype work. Calling their REST API from Python was super painful. The auth request has a timestamp, nonce and HMAC signature, which is super brittle. If the order of the parameters is not alphabetical, or there is any problem with how you setup the HMAC, you just get a generic signature error with no trouble-shooting information. Then you have a series of required custom HTTP headers.

All of these problems are solvable by writing your own Python SDK. But the iOS and Node.js SDKs were also hard to get working. Their Node library, admittedly in beta, was broken. Overall, their documentation was poor - it was hard to get stuff working. Take a look at how verbose the following code is:


```python
import random
import time
import hashlib
import hmac

import requests


APP_ID = 'XXX'
AUTH_KEY = 'XXX'
AUTH_SECRET = 'XXX'
USER_ID = 'XXX'
PASSWORD = 'XXX'
DIALOG_ID = 'XXX'


def create_session():
    nonce = str(random.randint(1, 10000))
    timestamp = str(int(time.time()))
    signature_raw_body = (
        'application_id=' + APP_ID +
        '&auth_key=' + AUTH_KEY +
        '&nonce=' + nonce +
        '&timestamp=' + timestamp +
        '&user[login]=admin' +
        '&user[password]=password')
    signature = hmac.new(AUTH_SECRET, signature_raw_body, hashlib.sha1).hexdigest()
    response = requests.post(
        'https://api.quickblox.com/session.json',
        headers={
            'Content-Type': 'application/json',
            'QuickBlox-REST-API-Version': '0.1.0',
        },
        json={
            'application_id': APP_ID,
            'auth_key': AUTH_KEY,
            'timestamp': timestamp,
            'nonce': nonce,
            'signature': signature,
            'user': {
                'login': 'admin',
                'password': 'password',
                }
        })
    json_data = response.json()
    return json_data['session']['token']


def get_messages(qb_token):
    return requests.get(
        'https://api.quickblox.com/chat/Message.json?chat_dialog_id=' + DIALOG_ID,
        headers={
            'QB-Token': qb_token,
        }
    )


if __name__ == '__main__':
    qb_token = create_session()
    messages = get_messages(qb_token)
    print messages, messages.content
```


# #2: PubNub

[PubNub](https://www.pubnub.com/) is not focused exclusively on chat, but chat is a first class topic in their documentation. Truly excellent SDKs for virtually every language you could care about. Sometimes there are multiple SDKs for the same language that are specialized for particular frameworks - think Django, Twisted and Tornado. They have a lot of mindshare in the developer community; I constantly hear about other engineers using PubNub for hackathon projects. They pop up organically in my Twitter feed a lot.

Prototyping could not have been simpler. See the bellow code. The only downside is that they do not have true web hook support. Their web hooks are limited to when conversations start and stop, versus firing on every chat message.

Why are web hooks a big deal? They probably are not for many use cases. But one thing we want to be able to do is have a Python bot that listens to all conversations and performs various actions in real-time. As far as I can tell, the PubNub model for this is to use something like Twisted, which is an asynchronous event-based networking engine in Python. You leave a socket open to PubNub all the time and get notified of new messages over that active connection.

That performs really well, which is why they do it. But it drastically increases the complexity with regards to production high availability, versus a vanilla web server. With a web server, if you loose a node (and you will, think EC2 instance going down), it's no problem. You simply have multiple nodes behind a load balancer. Because they are all stateless, recovery is automatic as new requests keep flowing to the remaining nodes.

With an active socket daemon, you have to solve the high availability problem yourself. If you create a master/hot backup architecture, you need to realize that the primary node is down and have the secondary server establish a connection and *resume any in progress conversations*. That's a separate critical code path that will execute only very rarely - a recipe for bugs. If you go active/active, then you have all the same problems of resuming a portion of the connections when a node fails, plus you have to figure out connection sharding.

None of these are insurmountable problems. But they are significant added complexity, which is what I'm trying to avoid by using an existing platform. PubNub has a super simple SDK, but then they force you to solve a bunch of architectural complexity yourself.

Here is our prototype code. Notice the paradigm; event loops. This code blocks until you kill the process.


```python
from pubnub import Pubnub


def callback(message, channel):
    print(message)


def error(message):
    print("ERROR : " + str(message))


def connect(message):
    print("CONNECTED")
    print pubnub.publish(channel='test', message='Hello from the PubNub Python SDK')


def reconnect(message):
    print("RECONNECTED")


def disconnect(message):
    print("DISCONNECTED")


pubnub = Pubnub(publish_key='XXX', subscribe_key='XXX', secret_key='XXX')

pubnub.subscribe(
    channels='dit',
    callback=callback,
    error=callback,
    connect=connect,
    reconnect=reconnect,
    disconnect=disconnect,
)
```


# #1: Layer

[Layer](https://layer.com/) is a new player. They focus solely on chat. They have good iOS and Node SDKs (but not Python). Their REST API semantics are dedicated to chat. Conversations and messages are first class concepts. Their documentation is good, if not as exhaustive as PubNub. Importantly, they have web hooks for each message (currently in private beta).

One downside is that they do not support end-to-end encryption per-se. Of course, you can manually encrypt your message bodies yourself. Being newer, they also do not have the track record that PubNub has.

Even though they do not have a Python SDK, our prototype code could not have been more Pythonic. This makes me confident we will be able to write clean code, and use a simple web server architecture.

Finally, there is significant upside to being a chat specific platform. The SDKs support concepts like read/unread, typing indicators, etc. You can do that yourself via PubNub, but you have to write more code. PubNub is schemaless - you are writing all the schema plus serialization yourself, separately for each language. Code is the enemy!


```python
import requests


APP_ID = 'XXX'
PLATFORM_API_TOKEN = 'XXX'
HOST = 'https://api.layer.com'
BASE_URL = HOST + '/apps/%s' % APP_ID
HEADERS = {
    'Accept': 'application/vnd.layer+json; version=1.0',
    'Authorization': 'Bearer %s' % PLATFORM_API_TOKEN,
    'Content-Type': 'application/json',
}


def _request(method, relative_url, data=None):
    data = data or {}
    callable_ = getattr(requests, method)
    return callable_(
        BASE_URL + relative_url,
        headers=HEADERS,
        json=data,
    )


def get_conversation():
    return _request('post', '/conversations', data={
        'participants': ['John', 'Jane'],
        'distinct': True,
    })


def get_messages(conversation_id):
    return _request('get', '/conversations/%s/messages' % conversation_id)


def post_message(conversation_id, text):
    return _request('post', '/conversations/%s/messages' % conversation_id, data={
        'sender': {
            'name': 'Chase',
        },
        'parts': [
            {
                'body': text,
                'mime_type': 'text/plain',
            }
        ]
    })


conversation = get_conversation()
conversation_id = conversation.json().get('id')
conversation_id = conversation_id.replace('layer:///conversations/', '')
print conversation_id

messages = get_messages(conversation_id)
print messages, messages.content

post_response = post_message(conversation_id, 'this is a test')
print post_response, post_response.content
```

# Conclusion

I hope this helps you if you need to make a similar decision. Hit me up on Twitter and let me know how it goes!
