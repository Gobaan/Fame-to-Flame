from datetime import datetime
from dateutil import parser
from dateutil.tz import *
import sys
import codecs

# A class representing an amazon comment
class Comment:
  
    def __init__(self, title, sentiment):
        self.title = title
        self.content = ""
        self.sentiment = sentiment
        self.date = datetime.now(tzutc())

    def add(self, content):
        self.content += content

    def __str__(self):
        return self.title + "\n" + self.content + "\n\n"


def read_file(filename):
    comments = []

    if filename == "best":
        sentiment = "true"
    elif filename == "worst":
        sentiment = "false"
    else:
        print "Unexpected filename. Must be either 'good' or 'bad'."
        sys.exit(1)

    f = codecs.open(filename, "r", "latin-1")

    # first line is title of first comment
    line = f.readline()
    current = Comment(line.strip(), sentiment)

    line = f.readline()
    while line:
        if line.strip() == "<!-- BOUNDARY -->":
            comments += [current]
            current = Comment(f.readline().strip(), sentiment) 
        else:
            current.add(line)

        line = f.readline()
    
    return comments

# vi: ts=4 sw=4 sts=4
  
