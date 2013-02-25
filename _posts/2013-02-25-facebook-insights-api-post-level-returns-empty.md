---
layout: post
title: Facebook Page Post Insights Empty Results
tags: facebook
---

Spent a couple of hours tearing my hair out over the Facebook insights API this week. Say you have a Facebook page with an ID of **173304932707127**, and a post on that page with ID **497058920331725**. The [Facebook Insights API docs](https://developers.facebook.com/docs/reference/fql/insights/) would lead you to believe that you can query for post level details with just `/497058920331725/insights` as the URL. Instead, any query at that base URL just returns an empty data property:

![Facebook Insights Post Empty Data](/blog/images/insights_empty_data.png)

The fact that just `/497058920331725` correctly returns the meta data about the page would further strengthen your belief that there just is no insights data for this post.

![Facebook Insights Post Metadata](/blog/images/insights_post.png)

However, though it is mentioned nowhere in the docs, you in fact need to hit `/173304932707127_497058920331725/insights` to retreive insights data for that post.

![Facebook Insights Post Success](/blog/images/insights_with_data.png)
