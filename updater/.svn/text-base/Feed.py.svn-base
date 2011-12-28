import time, FeedEntry
import feedparser
import re
import urllib
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import Comment
from BeautifulSoup import CData
from BeautifulSoup import Declaration
from BeautifulSoup import ProcessingInstruction
import split_beautiful
from clean_data import clean_data
filterScript = re.compile("<script.*?ipt>|<style.*?style>", re.DOTALL)

class Feed:

    """Class representing a Feed that needs to be periodically updated."""
    def __init__(self,
                 url,
                 lastEntry = None,
                 updateInterval = 15 * 60 * 4,
                 lastUpdated = 0,
                 saved = False):
        self.url = url.encode('utf-8')
        self.feedEntries = None
        self.__saved__ = saved
        self.__lastEntry__ = lastEntry
        self.updateInterval = updateInterval
        self.lastUpdated = lastUpdated

    def update(self):
        self.feedEntries = []
        self.lastUpdated = time.time()

        if re.search( 'reddit', self.url ) or re.search( 'imbd', self.url ) :
            return

        print 'updating ' + self.url
        feed = feedparser.parse( self.url )
        if len(feed.entries) == 0:
            return
        if len(feed.entries) > 1000:
            print 'More than 1000 entries in feed: ' + self.url
            
        firstEntry = feed['entries'][0].link
        for entry in feed.entries:
            author = None
            comments = []
            guid = None
            updated = None
            summary = ""

            if entry.link == self.__lastEntry__:
                self.__lastEntry__ = firstEntry
                return;
            try:
                author = entry.author
            except AttributeError:
                pass

            try:
                updated = entry.updated
            except AttributeError:
                pass

            try:
                summary = entry.summary
            except AttributeError:
                pass

            summary = summary.encode('utf-8')
            
            content = self.__retrieve_content__(summary, entry.link)
            content, comments_in_content = clean_data( content, summary )

            for i in range(0, len(comments_in_content)):
                comments.append(
                    FeedEntry.FeedEntry(entry.link + '#comment' + str(i),
                                        feed.url,
                                        comments_in_content[i].encode('utf-8'),
                                        comments_in_content[i].encode('utf-8'),
                                        (entry.title + ' Comment ' + str(i)).encode('utf-8'),
                                        (entry.link + '#comment' + str(i)).encode('utf-8'),
                                        '',
                                        None,
                                        updated))

            self.feedEntries.append(
                FeedEntry.FeedEntry(entry.link.encode('utf-8'),
                                    feed.url,
                                    content.encode('utf-8'),
                                    content.encode('utf-8'),
                                    entry.title.encode('utf-8'),
                                    entry.link.encode('utf-8'),
                                    author.encode('utf-8'),
                                    comments,
                                    updated))
            
        self.__lastEntry__ = firstEntry;

    def __retrieve_content__(self, str, link):
        filehandle = urllib.urlopen(link)
        content = filehandle.read()
        contentTypeSplit = filehandle.headers['content-type'].split('charset=');

        encoding = 'ISO-8859-1'
        if len( contentTypeSplit ) == 2:
          encoding = contentTypeSplit[-1]
        ucontent = unicode(content, encoding)
        return str + ucontent

    def save(self, c):
        print 'saving feed ' + self.url
        if not self.__saved__:
            c.execute( "INSERT INTO feeds VALUES (?, ?, ?, ?)", (self.url,
                                                                 self.updateInterval,
                                                                 self.lastUpdated,
                                                                 self.__lastEntry__) )
            self.__saved__ = True
        else:
            c.execute( "UPDATE feeds SET last_updated= ?, last_entry = ? WHERE feed_url=?", (self.lastUpdated,
                                                                                             self.__lastEntry__,
                                                                                             self.url) )
        c.commit()

    #
    # Methods defined so that UpdateQueue sorts properly
    #
    def __eq__(self, other):
        return self.lastUpdated + self.updateInterval == other.lastUpdated + other.updateInterval

    def __ne__(self, other):
        return self.lastUpdated + self.updateInterval != other.lastUpdated + other.updateInterval

    def __lt__(self, other):
        return self.lastUpdated + self.updateInterval < other.lastUpdated + other.updateInterval

    def __gt__(self, other):
        return self.lastUpdated + self.updateInterval > other.lastUpdated + other.updateInterval

    def __le__(self, other):
        return self.lastUpdated + self.updateInterval <= other.lastUpdated + other.updateInterval

    def __ge__(self, other):
        return self.lastUpdated + self.updateInterval >= other.lastUpdated + other.updateInterval
