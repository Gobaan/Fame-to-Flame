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

class Link:

    def __init__(self, link):
        self.link = link
        self.entries = []

    def __retrieve_content__(self, str, link):
        filehandle = urllib.urlopen(link)
        content = filehandle.read()
        contentTypeSplit = filehandle.headers['content-type'].split('charset=');
        encoding = 'ISO-8859-1'
        if len( contentTypeSplit ) == 2:
          encoding = contentTypeSplit[-1]
        ucontent = unicode(content, encoding)
        return str + ucontent


    def update(self):
        content = self.__retrieve_content__('', self.link)
        title = BeautifulSoup(content).find('title').contents[0]
        content, comments_in_content = clean_data( content, '' )
        for i in range(0, len(comments_in_content)):
                self.entries.append(
                    FeedEntry.FeedEntry(self.link + '#comment' + str(i),
                                        None,
                                        comments_in_content[i],
                                        comments_in_content[i],
                                        title,
                                        self.link,
                                        None,
                                        None,
                                        None))

        self.entries.append(
                FeedEntry.FeedEntry(self.link,
                                    None,
                                    content,
                                    content,
                                    title,
                                    self.link,
                                    None,
                                    None,
                                    None))




