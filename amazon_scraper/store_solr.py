from __future__ import with_statement
import httplib, urllib
import htmllib
from datetime import datetime
from dateutil import parser
from dateutil.tz import *
from xml.sax.saxutils import escape
import comment_parser
import sys


from charlies_sentiment import *
sys.path.append("../updater")
from store import escape_string_xml
import re

def clean(text):
    text = re.sub(r'<.*?>', '', text)
    return text

i = 1
def store_solr(comments):
    global i
    global analyzer
    global cmd
    global initialized
    print "Storing comments into Solr."
    date_format = "%Y-%m-%dT%H:%M:%SZ"

    headers = {"Content-Type": "text/xml; charset=utf-8"};
    conn = httplib.HTTPConnection("localhost:8983");
    body = "<add>"
    template = """<doc><field name="guid">%s</field>
        <field name="title">%s</field>
        <field name="author">%s</field>
        <field name="link">%s</field>
        <field name="content">%s</field>
        <field name="published">%s</field>
        <field name="feedurl">%s</field>
        <field name="sentiment">%s</field>
        <field name="comments"></field>
        </doc>""".encode('utf-8')   

    for comment in comments:
        i += 1
        guid = escape_string_xml("TMPAMZNGUID" + str(i))
        feedurl = escape_string_xml("http://amazon.com")
        title = escape_string_xml(clean(comment.title))
        author = escape_string_xml("Amazon")
        link = escape_string_xml("http://amazon.com")
        comments = escape_string_xml("")
        content = escape_string_xml(clean(comment.content))
        sent = escape_string_xml(get_sentiment(feedurl, link, content))
	if not sent: continue
        date = datetime.now(tzutc())
        date = date.strftime(date_format).encode('utf-8')

        body += template % (guid, title, author, link, content, date, feedurl, sent)

    body += "</add>"

    f = open("solr_error.log", "r+")
    f.write(body)

    conn.request("POST", "/solr/update?commit=true", body, headers)
    resp = conn.getresponse()
    if resp.status != 200:
        print "Error while storing in Solr"
        f = open("solr_error.log", "r+")
        f.write(body)
        print resp.status
        print resp.read()
    conn.close()

def get_sentiment(feedurl, link, content):
  f = open('log.txt', 'a')
  f.write(content + '\n')
  f.write("url:" + feedurl + '\n')
  f.write("link:" + link + '\n')
  sentiment2 = classify(content)
  f.write("sentiment2: %s\n" % sentiment2)
  f.write("#BOUNDARY#\n")
  f.close()

  if not sentiment2:
     return False

  print 'sentiment%s' % sentiment2
  return str(sentiment2).encode('utf-8')
# ********** main!

train_on_amazon('../sentiment/reviews/cleaned_good', '../sentiment/reviews/cleaned_bad')
print "storing good"
comments = comment_parser.read_file("best")
store_solr(comments)

#div = 21
#num = len(comments)/div
#for i in range(div):
#    store_solr(comments[i*num:num])
#
print "storing bad"
comments = comment_parser.read_file("worst")
store_solr(comments)
#for i in range(1):
#    store_solr(comments[i*num:num])

# vi: ts=4 sw=4 sts=4
