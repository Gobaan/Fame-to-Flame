#!/usr/bin/python

import urllib
import re
import socket
import sys

class FeedLister:
  def __init__(self):
    socket.setdefaulttimeout(5)
    self.pattern = re.compile(
    "<link rel=\"alternate\" type=\"application/rss\+xml\" title=\"(.*?)\" href=\"(.*?)\"")

  def getFeedList(self, urls):
    feeds = []
    for url in urls:
      feed = self.getFeedFromURL(url)
      if feed is not None:
        feeds.append(feed)
    return feeds

  def getFeedFromURL(self, url):
    try:
      blog = urllib.urlopen(url)
      return getFeedFromPage(blog.read())
    except Exception, e:
      # Timeout
      return None

  def getFeedFromPage(self, page):
    try:
      match = re.search(self.pattern, page)
      if match is not None:
        return match.group(2)
    except Exception, e:
      return None


if __name__ == "__main__":
  blogs = open("blogs")
  feeds = FeedLister().getFeeds(blogs)
  for feed in feeds:
    print feed
