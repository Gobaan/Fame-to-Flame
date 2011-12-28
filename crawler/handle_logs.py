#!/usr/bin/python

import re
import sys
import socket
import urllib2

def handle_feed(feed):
  feed_handler = urllib2.urlopen("http://localhost:11000", "feed_url=%s" % feed)

def handle_url(url):
  # Do a sanity check on the url
  if url.endswith(("robots.txt", "gif", "jpg", "js", "png")):
    return

  # Go to the url and check if there is an rss feed available
  try:
    page = urllib2.urlopen(url)
    data = page.read()
    match = feed_pattern.search(data)
    if match:
      if match.group(2).startswith("http"):
        handle_feed(match.group(2))
      else:
        # Feed url may be relative
        handle_feed(url + match.group(2))
    else:
      match = isrss_pattern.search(data)
        if match:
          handle_feed(url)
  except Exception, e:
    # Timeout
    return

def handle_log_line(line):
  # Check if log line has a valid url for checking
  match = log_pattern.match(line)
  if match:
    handle_url(match.group(1))

if __name__ == "__main__":
  # Check args
  if len(sys.argv) <= 1:
    print "handle_logs requires a log file as an argument"
    sys.exit(0)

  # Open file
  with open(sys.argv[1]) as log_file:
    log_file = open(sys.argv[1])

    # Compile regexes we will need
    log_pattern = re.compile(".*?\s*200\s*[\-0-9]* (\S*?)\s")
    feed_pattern = re.compile(
        "<link rel=\"alternate\" type=\"application/rss\+xml\" title=\"(.*?)\" href=\"(.*?)\"")
    isrss_pattern = re.compile("<rss.*>")

    socket.setdefaulttimeout(5)

    # Handle each log line
    for line in log_file:
      handle_log_line(line)
