---
layout: post
title: REST API Design
tags: api
---

[REST](http://en.wikipedia.org/wiki/Representational_state_transfer) APIs operate over HTTP, use standard verbs like `GET` and `POST`, expose a common-sense URL structure and return resources in a well-defined format, typically JSON.

In spite of that simple definition, there is a wide degree of latitude when designing a REST API to fuck it up. Don't do that! Follow the guiding principle of making things as easy as possible for the calling developers. Provide the correct level of granularity, reduce the number of calls they need to make, and document the heck out of it.

In terms of granularity, I'm referring to whether the API exposes individual database records directly, with a thin CRUD layer, versus composing those into higher level resources that represent the problem domain the way your users think of it. The CRUD model makes a lot of sense for internal low-level data APIs, whereas the higher level model makese more sense for exposing to the outside world, as well as internal front-end and mobile developers. Remember - your relational data model details almost never aligns with the user's mental model of how your application works.

For the rest of this article, I'm going to be talking primarily about higher level APIs, hereto referred to as an [Intent API](http://www.thoughtworks.com/insights/blog/rest-api-design-resource-modeling).

## Resource Semantics

What's the difference between an Intent API and a CRUD API? The level of granularity. Instead of exposing implementation details of your actual database scheme (which may change), we instead expose higher order concepts of what the user intention is for your actual use cases.

For example, in a CRUD API for a bank, you might expose [Resources](http://restful-api-design.readthedocs.org/en/latest/resources.html) for Accounts, Account Holders and Transactions. You would allow callers to create an Accout record, and you would allow the creation of Transactions. A caller might implement a transfer between two accounts as two transactions; one debit from account A and one deposit to account B. Hopefully you can also make those two operations an atomic transaction somehow.

With an Intent API, you would probably not allow Account or Account Holder creation at all. Those are likely off-line manual tasks that you want performed by actual humans, or at the very least your own internal services, which then use the private CRUD API. You also likely to not want to allow the creation of a Transaction directly. But maybe you expose a Transfer Resource, as well Purchase and ChargeBack Resources.

What does this get you? By mapping to the intention of the user - what they are actually trying to accomplish - you have the opportunity to tailor an API endpoint to just the set of parameters that make sense for that operation. For a Transfer, you need two Account IDs. For Purchase, you need Vendor metadata. For a ChargeBack, you need a previous Transaction ID.

You also have the ability to ensure that operations are atomic and leave the data in a valid state. If a Transfer fails the second part of a two-stage commit, you can roll the first part back. You do not have to rely on the caller to do that properly.

What you have done is remove the burden of implementing business logic that's specific to your system from the callers, and placed it inside your system (where it belongs).

It's true that this is not strictly RESTful; you're exposing verbs as your Resources. You are likely going to expose nouns as well (Account, Transaction, Vendor), but your any call that's not [idempotent](http://en.wikipedia.org/wiki/Idempotence) should probably be a verb.

For an example of this in action, see the [GitHub API](https://developer.github.com/v3/repos/merging/):

```bash
POST /repos/:owner/:repo/merges
{
  "base": "master",
  "head": "cool_feature",
  "commit_message": "Shipped cool_feature!"
}
```

Notice that semantically speaking you're not creating a Commit Resource that actually represents the merging of two branches in git. Most users of git don't even understand what is actually happening to the data model for a merge; don't make your API callers have to understand it, either.

How do you know which intents to model for? I would start by looking at your core user scenarios, and think about what Resources you would want to have for each one, keeping in mind that you want to minimize the number of API calls required to display the user interface. You have to balance that against the cohesion and separation of concerns  of each Resource.


## URL Structure

On to implementation details! What should your URL structure look like? In general, you want to pick either plural or singular nouns and verbs and stick with that. I'm going to be opinionated and say that you should use plural nouns and singular verbs. For example:

- `/accounts` - list all Accounts
- `/accounts/123` - get the Account with ID 123
- `/accounts/123/transactions` - list Transactions associated with this Account
- `/accounts/123/transactions/123` - get a particular Transaction inside an Account
- `/transactions/123` - get the same Transaction outside the context of an Account
- `/transfer` - Create a transfer between two accounts (POST)

*Note:* there is no problem with exposing the same Resource at multiple end points. This is not a DRY model; remember that our guiding principle is making things easy for the developers. Maybe they don't know what Account is associated with a given Transaction.

Finally, you want to think about what content to display at the root endpoint of `/`. I have seen some APIs that use that endpoint as an opportunity to include likes to developer documentation and/or a list of all the endpoints in the system.


## Requests

The biggest decision here is how to take data from the caller. Most REST APIs will support URL parameters for most use cases. If you're doing that, make sure to support form POST encoding as well, it should be no extra work. These work well for simple key/value parameters, and are easy to implement for the caller.

For nested data, you have a choice of supporting JSON request bodies or using some type of prefix scheme in your key/value pairs. For example, you could represent the following JSON body:

```bash
{
    "user": "Chase Seibert",
    "account": {
        "id": 1,
        "name": "foobar"
    }
}
```

As the key/value pairs `?user=Chase Seibert&account__id=1&account__name=foobar`. Personally, I think that's both ugly and hard for the caller to implement in some cases.

Whatever you choose, make sure to inspect and respect the callers content-type.


## Metadata & Responses

For each API response, you want to have a consistent set of metadata that the callers can rely on being there, as well as a consistent overall packet structure. For example, you likely want to have well defined fields for pagination, results and error messages. But you may also want to include less obvious items, like an echo of the parameters that the user passed to you. This can be useful as signal that you have unambiguously received the arguments, parsed them out correctly and that they are valid for this API call.

Pagination is typically done by supporting something like `limit`, `offset` and `sortBy` as URL parameters. Then you include `nextPage` and `previousPage` fields in your response *which are absolute URLs* to those results in the API. *Note:* I'm using `camelCase` here versus `snake_case`. Given that most API consumers these days are either Javascript apps or native mobile apps (objective-c or Java), it might make sense to use their conventions and go with camel case. Just be consistent.

Error messages are great for developer sanity. Of course you want the primary signal of an error to be the proper HTTP status code for that error class.


## Versioning

You probably want to think about an API versioning strategy up front. In its simplest form, this is just a prefix like `/v1` that you prepend to every API endpoint. The idea is to plan ahead for having multiple supported versions in flight at the same time, to give developers a gentle transition for breaking changes to the API.

But how do you architect your code to be able to serve multiple versions? The heavy handed approach is to fork the code for each supported version. This is fairly simple, and has the advantage of being very predictably stable for older versions. A different approach might be to have the same codebase serve multiple versions. In that case, you will likely want to retain multiple versions of a subset of the unit tests, in addition.

A third hybrid approach would be to fork either with source control branches, or with actual running VMs or containers with that code on it. This has the disadvantage of making the older versions difficult to patch, either for hotfixes or infrastructure changes.

The most important thing is to have a plan up front. I would recommend launching with both a `/v1` and a `/v0` API that have some backwards incompatible difference, even if it's just a dummy endpoint that is removed in version 1.


## Authentication

If you're producing a public facing API, you almost certainly want to use OAuth. Don't write your own, find a framework. Even if your API is restricted to internal use, you should think about including at least some kind of caller identifier mechanism. This can come in handy when you go to produce analytics on who is using the API, in addition to being a prerequisite for rate limiting per caller.

Whichever auth mechanism you choose, you will want 100% of the API calls to be over HTTPS, so as not to leak those credentials. Don't even support a HTTP option.


## Documentation & Developers

Almost as important as the semantics of the API is having excellent, comprehensive documentation. Don't rely on automatically generated documentation here. Or, at least add a lof of explanatory detail about why the developer might want to use the API, and what each piece of the request and response mean. It's especially tricky to put yourself in the place of a person who doesn't know the intimate details of the models in your sytem. Run it by a third party for a sanity check.

Along with the text documentation, you will want to supply full, untruncated examples for common requests and responses. Go ahead and make sure they are pretty printed and perhaps even syntax highlighted. I would also recommend that you pretty print the actual API responses from the server.

A great way to expose examples is with interactive consoles. If you provide HTML documentation, you have even make the examples executable and tweakable in-line. The [Django REST Framework](http://www.django-rest-framework.org/) is a great example of this.


## Python Tooling

Here are some common frameworks for writing REST APIs in Python:

- [Django REST Framework](http://www.django-rest-framework.org/)
- [Flask RESTful](https://flask-restful.readthedocs.org/en/0.3.2/)
- [Flask API](http://flask.pocoo.org/docs/0.10/api/)

A good utility for working with REST APIs is [Bunch](https://github.com/dsc/bunch), which lets you easily translate between JSON API responses and Python objects. You can also go the other way, which may be useful for mapping your database objects to JSON.

For versioning, check out [Flask blueprints](http://flask.pocoo.org/docs/0.10/blueprints/#registering-blueprints).

Finally, depending on whether your API is internal or external, you can look into tools for creating API consoles:

- [Apigee](http://apigee.com/about/)
- [HurLit](https://www.hurl.it/)
- [RAML API Console](http://raml.org/projects.html) - [example](https://anypoint.mulesoft.com/apiplatform/popular/#/portals/apis/6308/versions/6302/pages/31760)
