#!/usr/bin/python

import unittest
import feedlister.feedlist_test as feedlist_test
import feedparser.driver_test as driver_test


if __name__ == "__main__":
  allTests = unittest.TestSuite()
  allTests.addTests(feedlist_test.getSuite())
  allTests.addTests(driver_test.getSuite())
  unittest.TextTestRunner().run(allTests)
