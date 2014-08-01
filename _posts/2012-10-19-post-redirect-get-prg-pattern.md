---
layout: post
title: The Post/Redirect/Get (PRG) Pattern
tags: django view prg
---

Anyone who has used a web browser has probably encountered the dreaded "form resubmission" dialog. This happens when the user tries to refresh or use the back button to navigate back to a HTTP POST.

![Internet Explorer resubmit form dialog](/blog/images/resubmit_ie.png)
![Chrome resubmit form dialog](/blog/images/resubmit_chrome.png)
![Firefox resubmit form dialog](/blog/images/resubmit_firefox.jpeg)

A typical case where you might see this is when checking out from a web store. Maybe you have one page that takes your shipping address, and a second page that takes your billing information. The first page submits your data with an HTTP POST, and then returns a 200 response with the payment details form HTML. If the user hits the back button in their browser, or tries to refresh the second page, they will see one of the above dialogs.

To the typical user, such a dialog is absolutely terrifying. Even if they know what it means, there is no clearly correct course of action. If they hit "Ok", they may be creating [duplicate](http://en.wikipedia.org/wiki/Post/Redirect/Get) shipping address records. Or maybe it's just updating the one they already submitted. Or maybe it will just throw an error saying they can't submit this form again. There is no way to be sure; they don't know how it's implemented on the server.

If they hit cancel, they will be greeted with an even more obscure blank browser page. Hitting back forward again will prompt them with yet another resubmit form dialog!

# The PRG Pattern

To avoid this usability issue, you want to try to keep POST events out of the browser history. Conveniently, there there is a mechanism for this that all the browsers respect. **If a HTTP POST returns a HTTP 302 redirect, only the location of the redirect will be stored in the browser history.** Hitting the back button will skip over the POST, and the user can bounce freely between the first and second forms.

# Bad code

{% highlight python %}
def view_record(request, record_id):
    record = get_object_or_404(Record, pk=record_id)
    if request.method == "POST":
        record.name = request.POST.get("name")
        record.save()
    return render_to_response("page.html", locals())
{% endhighlight %}

# Good code

{% highlight python %}
def view_record(request, record_id):
    record = get_object_or_404(Record, pk=record_id)
    if request.method == "POST":
        record.name = request.POST.get("name")
        record.save()
        return HttpResponseRedirect(reverse("view_record", args=[record_id]))
    return render_to_response("page.html", locals())
{% endhighlight %}

# Caveats

* This only affects full page refreshes, Ajax calls are unaffected.
* In practice, this may sometimes require you to temporarily save state when otherwise you would not. For example, in multi-step forms. In those cases, you can often save the data safely in the [session scope](http://www.theserverside.com/news/1365146/Redirect-After-Post).
