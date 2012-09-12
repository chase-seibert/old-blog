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
from django.utils.encoding import smart_str, force_unicode
from xml.sax import saxutils
from xml.sax.saxutils import XMLGenerator
from xml.sax.xmlreader import AttributesNSImpl

def get_options():
    parser = OptionParser()
    parser.add_option('-f', '--file', dest='filename',
        help='blogger XML backup')
    parser.add_option('-o', '--output', dest='outputdir',
        help='directory to output Markdown files to')
    parser.add_option('-m', '--maxposts', dest='maxposts',
        help='Max number of posts to write out, useful for tracking down Liquid templating errors')
    parser.add_option('-c', '--comments', dest='comments',
        help='file to write Disqus comments XML to')
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

def escape(value):
    return strip_illegal_xml_characters(force_unicode(saxutils.escape(smart_str(value))))

def escape_html(value):
    return strip_illegal_xml_characters(force_unicode(smart_str(value)))

# http://maxharp3r.wordpress.com/2008/05/15/pythons-minidom-xml-and-illegal-unicode-characters/
def strip_illegal_xml_characters(input):

    if input:

        import re

        # unicode invalid characters
        RE_XML_ILLEGAL = u'([\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff])' + \
                         u'|' + \
                         u'([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])' % \
                          (unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
                           unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
                           unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
                           )
        input = re.sub(RE_XML_ILLEGAL, "", input)

        # ascii control characters, note the following are valid:
        #     \x09 ^I \t (Horizontal tab)
        #     \x0A ^J \f (Line feed)
        #     \x0D ^M \r (Carriage return)
        input = re.sub(r"[\x01-\x08\x0B-\x0C\x0E-\x1F\x7F]", "", input)

    return input

def tag(logger, name, contents, attrs={}):
    logger.startElementNS((None, name), name, attrs)
    logger.characters(escape_html(contents))
    logger.endElementNS((None, name), name)

def cdata(logger, name, contents, attrs={}):
    logger.startElementNS((None, name), name, attrs)
    if contents:
        logger._out.write('<![CDATA[')
        logger._out.write(smart_str(escape(contents)))
        logger._out.write(']]>')
    logger.endElementNS((None, name), name)

def write_comments_file(posts):

    with codecs.open(options.comments, mode="wb") as file:
        logger = XMLGenerator(file, 'UTF-8')
        logger.startDocument()
        #logger.startPrefixMapping(prefix, uri)
        logger.startElementNS((None, 'rss'), 'rss',
            AttributesNSImpl({}, {}))

        logger.startElementNS((None, 'channel'), 'channel',
            AttributesNSImpl({
                (None, "xmlns:content"): "http://purl.org/rss/1.0/modules/content/",
                (None, "xmlns:dsq"): "http://www.disqus.com/",
                (None, "xmlns:dc"): "http://purl.org/dc/elements/1.1/",
                (None, "xmlns:wp"): "http://wordpress.org/export/1.0/",
                }, {}))

        count = 0
        for id, post in posts.items():

            if not post.get("comments"):
                continue

            date_added = post.get("date")
            url = "/blog/%s/%02d/%02d/%s" % (
                    date_added.year,
                    date_added.month,
                    date_added.day,
                    slugify(post.get("title")))

            logger.startElementNS((None, 'item'), 'item',
                AttributesNSImpl({}, {}))

            tag(logger, "title", "re: " + post.get("title"))
            tag(logger, "link", "http://chase-seibert.github.com" + url)
            cdata(logger, "content:encoded", post.get("content"))
            tag(logger, "dsq:thread_identifier", url)
            tag(logger, "wp:post_date_gmt", post.get("date").strftime("%Y-%m-%d %H:%M:%S"))
            tag(logger, "wp:comment_status", "open")

            for comment in post.get("comments", []):

                message = comment.get("message")

                if message:

                    logger.startElementNS((None, 'wp:comment'), 'wp:comment',
                        AttributesNSImpl({}, {}))
                        
                    tag(logger, "wp:comment_id", count)
                    tag(logger, "wp:comment_author", comment.get("author"))
                    tag(logger, "wp:comment_date_gmt", comment.get("date").strftime("%Y-%m-%d %H:%M:%S"))
                    tag(logger, "wp:comment_content", comment.get("message"))
                    tag(logger, "wp:comment_approved", 1)
                    tag(logger, "wp:comment_parent", 0)

                    count += 1

                    logger.endElementNS((None, 'wp:comment'), 'wp:comment')

            logger.endElementNS((None, 'item'), 'item')

        logger.endElementNS((None, 'channel'), 'channel')

        logger.endElementNS((None, 'rss'), 'rss')
        logger.endDocument()

def main():

    get_options()
    posts = get_posts_and_comments()

    if options.outputdir:
        count = 0
        for _, post in posts.items():
            count += 1
            if count <= int(options.maxposts or 10000):
                write_markdown_file(post)

    if options.comments:
        write_comments_file(posts)

if __name__ == "__main__":
    main()
