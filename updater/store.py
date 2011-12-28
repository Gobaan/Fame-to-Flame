import MySQLdb
import httplib, urllib
import htmllib
from charlies_sentiment import *
from datetime import datetime
from dateutil import parser
from dateutil.tz import *
from xml.sax.saxutils import escape

# unused; escape_string doesn't exist anymore
def store_mysql(entries):
    print "store_mysql"
    date_format = "%Y-%m-%d %H:%M:%S"
    try:
        conn = MySQLdb.connect (host = "localhost",
                               user = "fydp",
                               charset = "utf8",
                               passwd = "fydp",
                               db = "fydp_db")
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        exit(1)

    try:
        cursor = conn.cursor ()
        for entry in entries:
            guid = escape_string(entry.guid)
            feedurl = escape_string(entry.feedurl)
            content = escape_string(entry.content)
            title = escape_string(entry.title)
            link = escape_string(entry.link)
            author = escape_string(entry.author)
        
            #TODO: comments = escape_string(entry.comments)

            date = get_date(entry.published)

            cursor.execute ("""
                INSERT INTO feeditem (guid, feedurl, content, title, link, author,
                    comments, published)
                VALUES
                    ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
            """ % (guid, feedurl, content, title, link, author, comments,
            date.strftime(date_format))
            )
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        exit(1)

    conn.commit()
    conn.close()


def store_solr(entries):
    print "store_solr"
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
        <field name="comments">%s</field>
        </doc>""".encode('utf-8')

    templateComm = """<doc><field name="guid">%s</field>
        <field name="title">%s</field>
        <field name="author">%s</field>
        <field name="link">%s</field>
        <field name="content">%s</field>
        <field name="published">%s</field>
        <field name="feedurl">%s</field>
        <field name="sentiment">%s</field>
        </doc>""".encode('utf-8')

    good_entries = ""
    for entry in entries:
        guid = escape_string_xml(entry.guid)
        feedurl = escape_string_xml(entry.feedurl)
        title = escape_string_xml(entry.title)
        author = escape_string_xml(entry.author)
        link = escape_string_xml(entry.link)
        content = escape_string_xml(entry.content)
        date = get_date(entry.published)
        date = date.strftime(date_format).encode('utf-8')

        # this is where sentiment is decided
        sent = get_sentiment(feedurl, link, content)
        if not sent: continue

        good_entries += '"' + escape_string_xml(entry.guid) + "\","

        if entry.comments != None:
            comment_list = ""

            if len(entry.comments) > 0:
                comment_list = store_solr(entry.comments)

            body += template % (guid, title, author, link, content, date, feedurl,
                    sent, comment_list)
        else:
            body += templateComm % (guid, title, author, link, content, date, feedurl,
                    sent)

    body += "</add>"

    conn.request("POST", "/solr/update?commit=true", body, headers)
    resp = conn.getresponse()
    if resp.status != 200:
        print "Error while storing in Solr"
        f = open("badlog", "w")
        f.write(body)
        f.close()
        print resp.status
        print resp.read()
    conn.close()

    return good_entries

# transform a raw date string into a datetime object; if the string is null or
# empty, choose now as the time
def get_date(raw):
    if not raw:
        return datetime.now(tzutc())
    else:
        return parser.parse(raw)

# takes a string and makes it safe for entry into Solr XML
# replaces nulls with empty strings, encodes it into utf-8, unescapes any HTML
# entities and escapes XML ones
def escape_string_xml(str):
    if not str:
        return "".encode('utf-8')

    str = str.encode('utf-8')

    # unescape html
    str = unescape_html(str)
    # escape XML
    str = escape(str)
    return str

# unescapes the HTML entities, and then re-escapes XML entities
# for Solr, since the request is supposed to be in XML, and since HTML
# entities will cause Solr to choke.
def unescape_html(s):
    p = htmllib.HTMLParser(None)
    p.save_bgn()
    p.feed(s)
    return p.save_end()

initialized = False
def initialize():

  print 'started'
  import subprocess
  cmd = 'java -cp ../sentiment/sentimentDemo.jar:../sentiment/lingpipe-3.9.2.jar PolarityWhole ../sentiment/reviews/'.split()

  analyzer = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout = subprocess.PIPE)
  f = open('log.txt', 'w')
  f.close()
  train_on_amazon('../sentiment/reviews/cleaned_good', '../sentiment/reviews/cleaned_bad')

if __name__ == '__main__':
  initialize()

def get_sentiment(feedurl, link, content):
  #global initialized
  #if not initialized:
  #   line = analyzer.stdout.readline().strip()
  #   while line != 'Enter Input Now':
  #      line = analyzer.stdout.readline().strip()
  #      print line
  #   initialized = True
  #   print 'initialized'


  #content = [line.strip() for line in content.split('\n') if len(line.split()) > 8 ]
  #analyzer.stdin.write(content + '\n')
  #analyzer.stdin.write("#BOUNDARY#\n")
  #out = analyzer.stdout.readline().strip()
  f = open('log.txt', 'a')
  f.write(content + '\n')
  f.write("url:" + feedurl + '\n')
  f.write("link:" + link + '\n')
  #f.write("sentiment: " + out.encode('utf-8') + '\n')
  sentiment2 = classify(content)
  f.write("sentiment2: %s\n" % sentiment2)
  f.write("#BOUNDARY#\n")
  f.close()

  print 'sentiment%s' % sentiment2
  if not sentiment2:
     return False
  return str(sentiment2).encode('utf-8')


# vi: set sw=4 sts=4:
