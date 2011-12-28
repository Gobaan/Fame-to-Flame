#!/usr/bin/python

import os
import unittest
from get_feeds import FeedLister


class FeedListTestCase( unittest.TestCase ):
  def setUp(self):
    dir = os.path.dirname(__file__) + "/testdata/"
    self.emptyBlog = ""
    self.blog = open(dir + "mockblog.txt").read()
    self.blogNoFeed = open(dir + "mockblog_nofeed.txt").read()
    self.blogManyFeeds = open(dir + "mockblog_manyfeeds.txt").read()
    self.blogList = [self.emptyBlog, self.blog,
                     self.blogNoFeed, self.blogManyFeeds]
    self.feed = "http://blogsofnote.blogspot.com/feeds/posts/default?alt=rss"

  # The normal case
  def testNormal(self):
    self.assertEquals(FeedLister().getFeedFromPage(self.blog), self.feed)

  # An empty string as the website
  def testEmptyPage(self):
    self.assertEquals(FeedLister().getFeedFromPage(self.emptyBlog), None)

  # A page with no rss feeds
  def testNoMatch(self):
    self.assertEquals(FeedLister().getFeedFromPage(self.blogNoFeed), None)

  # A page with multiple rss feeds
  def testMultiMatches(self):
    # In this case, return the first match
    self.assertEquals(FeedLister().getFeedFromPage(self.blogManyFeeds),
                      self.feed)


def getSuite():
  return unittest.TestLoader().loadTestsFromTestCase(FeedListTestCase)


if __name__ == "__main__":
  unittest.TextTestRunner().run(getSuite())
