#!/usr/bin/python

from xml.dom import minidom
from optparse import OptionParser

def get_options():
    parser = OptionParser()
    parser.add_option('-f', '--file', dest='filename',
        help='blogger XML backup')
    global options
    (options, args) = parser.parse_args()
    if not options.filename:
        parser.error("You must supply at least a --file")

def main():
    get_options()
    dom = minidom.parse(options.filename)
    print dom.toprettyxml()
    # feed > entry, id contains .post-
    # mutliple category items (tags), title, content
    # html decode content, replace <pre name="code" blocks
    # any other formatting to text? -> see beautiful soup code form Reach

if __name__ == "__main__":
    main()
