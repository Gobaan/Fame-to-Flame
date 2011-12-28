#!/usr/bin/python

import re
import urllib

def pad(i):
  if i < 10:
    return "0%s" % i
  else:
    return str(i)

if __name__ == "__main__":
  sitepattern = re.compile("<h3 class=\"post-title\">[\s]*<a href=\"(.*?)\"")
  blogs = []

  for year in [pad(i) for i in range(2001, 2009)]:
    for month in [pad(i) for i in range(1,13)]:
      site = urllib.urlopen("http://blogsofnote.blogspot.com/%s_%s_01_archive.html" % (year, month))
      matches = re.finditer(sitepattern, site.read())
      for match in matches:
        blogs.append(match.group(1))

  for blog in blogs:
    print blog
