import feedparser
import re

itemTemplate = """<doc>
    <field name="channelTitle">%s</field>
    <field name="channelLink">%s</field>
    <field name="channelDescription">%s</field>
    <field name="title">%s</field>
    <field name="link">%s</field>
    <field name="description">%s</field>
</doc>
"""

def strip(string):
    return re.sub( "<.*>", "", string )

def getDoc( feed, item ):
    return itemTemplate % (strip(feed.title),
                           strip(feed.link),
                           strip(feed.description),
                           strip(item.title),
                           strip(item.link),
                           strip(item.description) )

def downloadAll( file, out ):
    for line in file:
        out.write( "<add>\n" )
        d = feedparser.parse( line )
        for item in d.entries:
            out.write( getDoc( d.feed, item ) )
        out.write("</add>")

if __name__ == "__main__":
    downloadAll( file("../feedlister/feeds"), file("out.xml", "w") )
