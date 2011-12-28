from HTMLParser import HTMLParser

import re
import urllib
import sys

match_comment = re.compile("comment|usertext")

class commentSplitter(HTMLParser):
    """Splits comments from document in HTML. The ways comments are recognized are:
    - <a name="comments"></a> followed by a list
    - <div class=".*comment.*"></div>
    - <div id=".*comment.*"></div>
    - <ul/dd/ol class=".*comment.*"> - all items are comments
    'usertext' can be used instead of 'comment' in any of the above.
    """

    def __init__(self):
        HTMLParser.__init__(self)
        self.inCommentList = False
        self.inDivComment = False
        self.foundAName = False
        self.inNameCommentList = False
        self.inNameCommentListComment = False
        self.inCommentListComment = False
        self.currentComment = ""
        self.commentList = []

    def handle_starttag(self, tag, attrs):
        tagclass = ""
        tagname = ""
        tagid = ""
        for (attr, value) in attrs:
            if attr == 'class':
                tagclass = value
            if attr == 'name':
                tagname = value
            if attr == 'id':
                tagid = value
        if tag == 'dl' or tag == 'ol' or tag == 'ul':
            if match_comment.search(tagclass) or match_comment.search(tagid):
                self.inCommentList = True
                self.inDivComment = False
                currentComment = ""
        if self.inCommentList and (tag == 'li' or tag == 'dd'):
            self.inCommentListComment = True
        if tag == 'div' and match_comment.search(tagclass) and not self.inCommentList:
            self.inDivComment = True
        if tag == 'a' and match_comment.search(tagname):
            self.foundAName = True
        if self.foundAName and not self.inNameCommentList and (tag == 'dl' or tag == 'ol' or tag == 'ul'):
            self.inNameCommentList = True
        if self.inNameCommentList and (tag == 'li' or tag == 'dd'):
            self.inNameCommentListComment = True

    def handle_endtag(self, tag):
        if self.inCommentList and (tag == 'dl' or tag == 'ol' or tag == 'ul'):
            self.inCommentList = False
        if self.inDivComment and tag == 'div':
            self.commentList += [self.currentComment]
            self.currentComment = ""
            self.inDivComment = False
        if self.inCommentList and (tag == 'li' or tag == 'dd'):
            self.commentList += [self.currentComment]
            self.currentComment = ""
            self.inCommentListComment = False
        if self.foundAName and self.inNameCommentList and (tag == 'dl' or tag == 'ol' or tag == 'ul'):
            self.inNameCommentList = False
            self.foundAName = False
        if self.inNameCommentList and (tag == 'li' or tag == 'dd'):
            self.commentList += [self.currentComment]
            self.currentComment = ""
            self.inNameCommentListComment = False

    def handle_data(self, data):
        if self.inDivComment or self.inCommentListComment or self.inNameCommentListComment:
            self.currentComment += data

def splitText(text):
    """
    Returns a list of comments in this article.  Assumes text is raw
    HTML.  Does some formatting of the text, uses commentSplitter to
    split, and then filters out all comments of less than 25 words.
    """
    text = re.sub( re.compile("//<!\\[CDATA\\[(.|\n)+?\\]\\]\\>"), "", text)
    text = re.sub( re.compile("</scr' *\+ *'ipt>"), "</script>'", text)
    cs = commentSplitter()
    name_tag = re.compile('<a name="comment')
    cs.feed(text)
    cs.close()
    cs.commentList = filter( lambda x: len(x.split()) < 25, cs.commentList )
    return cs.commentList

if __name__ == '__main__':
    f = urllib.urlopen(sys.argv[1])
    comments = splitText(f.read())
    for c in comments:
        print c
        print "-------------------------------------"

