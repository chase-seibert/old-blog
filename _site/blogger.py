#!/usr/bin/python

from xml.dom import minidom
from optparse import OptionParser
import pprint
from datetime import datetime
import os
from django.template.defaultfilters import slugify
import codecs
from BeautifulSoup import BeautifulSoup
import html2text
import re
from disqusapi import DisqusAPI, APIError
import time
from gdata import service
import gdata
import atom
from gdata.sample_util import CLIENT_LOGIN, SettingsUtil
import gdata.blogger.client


def get_options():
    parser = OptionParser()
    parser.add_option('-f', '--file', dest='filename',
        help='blogger XML backup')
    parser.add_option('-o', '--output', dest='outputdir',
        help='directory to output Markdown files to')
    parser.add_option('-m', '--maxposts', dest='maxposts',
        help='Max number of posts to write out, useful for tracking down Liquid templating errors')
    parser.add_option('-t', '--disqustoken', dest='auth_token',
        help='Disqus API token')
    parser.add_option('-d', '--disquforum', dest='forum',
        help='Disqus forum name')
    parser.add_option('-r', '--redirect', dest='redirect',
        help='Redirect old blogger posts')
    global options
    (options, args) = parser.parse_args()
    if not options.filename:
        parser.error("You must supply at least a --file")

def get_text(node, name):
    try:
        return node.getElementsByTagName(name)[0].firstChild.data
    except (AttributeError, IndexError):
        pass

def get_date(node, name):
    return datetime.strptime(get_text(node, name)[0:19], "%Y-%m-%dT%H:%M:%S")

def tag_exists(node, name):
    try:
        if len(node.getElementsByTagName(name)) > 0:
            return True
    except AttributeError:
        pass
    return False

def get_tags(entry):
    tags = []
    for category in entry.getElementsByTagName("category"):
        try:
            term = category.attributes.get("term").nodeValue
            if "kind#post" not in term:
                tags.append(term)
        except AttributeError:
            pass
    return tags

def get_posts_and_comments():

    dom = minidom.parse(options.filename)
    feed = dom.getElementsByTagName("feed")[0]
    posts = {}
    for entry in feed.getElementsByTagName("entry"):

        if not ".post-" in get_text(entry, "id"):
            # it's a blogger meta-data entry
            continue

        if tag_exists(entry, "thr:in-reply-to"):
            # it's a comment; these come after all posts
            reply_to_id = entry.getElementsByTagName("thr:in-reply-to")[0].attributes.get("ref").nodeValue
            post = posts.get(reply_to_id)
            if post:
                if "comments" not in post:
                    post["comments"] = []
                post["comments"].append(dict(
                    author=get_text(entry.getElementsByTagName("author")[0], "name"),
                    message=get_text(entry, "content"),
                    date=get_date(entry, "published"),
                    ))
            continue

        posts[get_text(entry, "id")] = dict(
            title=get_text(entry, "title"),
            content=get_text(entry, "content"),
            date=get_date(entry, "published"),
            tags=get_tags(entry),
            )

    return posts

def write_markdown_file(post):

    date_added = post.get("date")
    slug = "%s-%02d-%02d-%s" % (
            date_added.year,
            date_added.month,
            date_added.day,
            slugify(post.get("title")))
    filepath = os.path.join(options.outputdir, slug + ".html")

    with codecs.open(filepath, encoding="utf-8", mode="w") as file:
        file.write("---\nlayout: post\ntitle: %s\ntags: %s\n---\n\n" % (
                    post.get("title", "").replace(":", "&#58;"),
                    ", ".join(post.get("tags"))
                    ))

        content = post.get("content")

        # manual hack fixups
        for (old_str, new_str) in (
            ("{{", "&#123;&#123;"),
            ("}}", "&#125;&#125;"),
            ("{%", "&#123;%"),
            ("%}", "%&#125;"),
            ):
            content = content.replace(old_str, new_str)

        print slug
        file.write(content)

def write_comments_api(posts):
    disqus = DisqusAPI(
        os.environ.get('DISQUS_SECRET'),
        os.environ.get('DISQUS_APIKEY'),
        )

    access_token = os.environ.get('DISQUS_ACCESS_TOKEN')

    for id, post in posts.items():
        if not post.get("comments"):
            continue

        thread_id = None
        title = post.get("title")
        date_added = post.get("date")
        url = "http://chase-seibert.github.com/blog/%s/%02d/%02d/%s.html" % (
                date_added.year,
                date_added.month,
                date_added.day,
                slugify(title))
        print url

        try:
            thread = disqus.threads.create(
                access_token=access_token,
                method="POST",
                forum="chaseseibertblog",
                title=title,
                url=url)
            print "Created thread: " + thread.get("id")
            thread_id = thread.get("id")
        except APIError:
            # already exists
            thread = disqus.threads.list(
                access_token=access_token,
                forum="chaseseibertblog",
                thread="link:%s" % url,
                )[0]
            print "Thread already exists: " + thread.get("id")
            thread_id = thread.get("id")

        for comment in post.get("comments", []):

            try:

                new_comment = disqus.posts.create(
                    access_token=access_token,
                    method="POST",
                    thread=thread_id,
                    message=comment.get("message"),
                    #author_name=comment.get("author"),
                    #author_email="noreply@blogger.com",
                    date=time.mktime(comment.get("date").timetuple()))

                print "Created comment: " + new_comment.get("id")
            except UnicodeEncodeError:
                pass

def _login():

    blogger_service = service.GDataService(
        os.environ.get('GOOGLE_USERNAME'),
        os.environ.get('GOOGLE_PASSWORD'))
    blogger_service.source = 'import from bitkickers'
    blogger_service.service = 'blogger'
    blogger_service.account_type = 'GOOGLE'
    blogger_service.server = 'www.blogger.com'
    blogger_service.ProgrammaticLogin()

    # Authenticate using ClientLogin, AuthSub, or OAuth.
    #client = gdata.blogger.client.BloggerClient()
    #gdata.sample_util.authorize_client(
    #    client, service='blogger', source='Blogger_Python_Sample-2.0',
    #    scopes=['http://www.blogger.com/feeds/'])    

    return blogger_service

def redirect_blogger(posts):

    blogger_service = _login()

    #query = service.Query()
    #query.feed = '/feeds/default/blogs'
    #feed = blogger_service.Get(query.ToUri())
    #blog_id = feed.entry[0].GetSelfLink().href.split("/")[-1]
    blog_id = '7663029716914672257'

    template = '<link rel="canonical" href="%(url)s" /><script type="text/javascript">window.location = "%(url)s";</script>'

    feed = blogger_service.GetFeed('/feeds/' + blog_id + '/posts/default')
    while feed:
        for entry in feed.entry:

            title = entry.title.text
            print title
            post = get_post_by_title(posts, title)
            
            date_added = post.get("date")
            url = "http://chase-seibert.github.com/blog/%s/%02d/%02d/%s.html" % (
                    date_added.year,
                    date_added.month,
                    date_added.day,
                    slugify(title))

            new_content = template % dict(url=url)

            entry.content = atom.Content(content_type='html', text=new_content)
            blogger_service.Put(entry, entry.GetEditLink().href)

        try:
            feed = blogger_service.GetFeed(feed.GetNextLink().href)
        except AttributeError:
            feed = None

def get_post_by_title(posts, title):
    for _, post in posts.items():
        if post.get("title") == title:
            return post

def main():

    get_options()
    posts = get_posts_and_comments()

    if options.outputdir:
        count = 0
        for _, post in posts.items():
            count += 1
            if count <= int(options.maxposts or 10000):
                write_markdown_file(post)

    if options.auth_token:
        write_comments_api(posts)

    if options.redirect:
        redirect_blogger(posts)

if __name__ == "__main__":
    main()
