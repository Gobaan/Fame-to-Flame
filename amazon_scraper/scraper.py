#!/usr/bin/python

import re
import gtk
import sys
import time
import subprocess

review_pattern = re.compile("(\d)\.0 out of 5 stars.*?<b>(.*?)</b>.*?</table>(?:.*?This review is from:)?.*?</div>\s*(.*?)<div", re.DOTALL)
#review_pattern = re.compile("<b>(.*?)</b><br />\s*(.*?)<div", re.DOTALL)
url_pattern = re.compile("http://www.amazon.com/(.*)/[dg]p/(.*?)(?:/|$)")
baseurl = "http://www.amazon.com/%s/product-reviews/%s/ref=cm_cr_pr_link_%d?ie=UTF8&showViewpoints=0&pageNumber=%d"
num_pages = 1

def handle_review(review):
  match = review_pattern.search(review)
  if not match:
    print review
    raise 'error'
  return "%s%s\n%s\n<!-- BOUNDARY -->\n" % match.groups()

def handle_page(data):
  # Split the page into reviews
  reviews = data.split("<!-- BOUNDARY -->")
  # discard the stuff before the first review
  reviews.pop(0)
  # Discard the best positive and best negative tool
  reviews.pop(0)
  reviews.pop(0)

  ret = []

  for review in reviews:
    ret.append(handle_review(review))

  return ret

def handle_asin(title, asin):
  # Read previous asins
  f = open("asins", 'r')
  asins = f.readlines()

  if asin + "\n" in asins:
    print "Found a duplicate ASIN, aborting"
    raise 'duplicate'

  f.close()

  # Start counting at 1
  for i in [j+1 for j in range(num_pages)]:
    url = baseurl % (title, asin, i, i)
    # wget that page (using urllib causes GET args to be lost for some reason)
    subprocess.call(["wget", url, "-O", "page%d" % i])

    # Sleep for 3 secs (hopefully alleviate amazon throttling)
    time.sleep(3)

    f = open("page%d" % i)
    reviews = handle_page(f.read())
    f.close()

    for review in reviews:
      if review[0] == '1':
        ff = open("worst", "a")
        ff.write(review[1:])
        ff.close()
      elif review[0] == '2':
        ff = open("bad", "a")
        ff.write(review[1:])
        ff.close()
      elif review[0] == '3':
        ff = open("neutral", "a")
        ff.write(review[1:])
        ff.close()
      elif review[0] == '4':
        ff = open("good", "a")
        ff.write(review[1:])
        ff.close()
      elif review[0] == '5':
        ff = open("best", "a")
        ff.write(review[1:])
        ff.close()

  f = open("asins", 'a')
  f.write(asin + "\n")
  f.close()

def handle_url(url):
  match = url_pattern.match(url)
  handle_asin(match.group(1), match.group(2))

def _clipboard_changed(clipboard, event):
  text = clipboard.wait_for_text()
  handle_url(text.split('?')[0])

if __name__ == "__main__":
  if len(sys.argv) > 1:
    handle_url(sys.argv[1].split('?')[0])
  else:
    clip = gtk.clipboard_get(gtk.gdk.SELECTION_PRIMARY)
    clip.connect("owner-change", _clipboard_changed)
    raw_input("Press enter to exit")
