import urllib, re
import split_beautiful
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import Comment
from BeautifulSoup import CData
from BeautifulSoup import Declaration
from BeautifulSoup import ProcessingInstruction
import sys

def clean_data(content, start_text = None, depth = 0):
    """
    Returns cleaned versions of the content and comments.
    Arguments:
    - `content`: Main content of the page in HTML
    - `comments`: Comments found on the page in HTML
    """
    if depth == 0:
        content, comments = split_beautiful.findComments(content)
        comments = [ clean_data (comment, None, 1) for comment in comments ]
    soup = BeautifulSoup(content);

    [x.extract() for x in soup.findAll('script')]
    [x.extract() for x in soup.findAll('style')]


    #if start_text and soup.find(text=re.compile('.*' + start_text + '.*')):
        #parent = soup.find(text=re.compile('.*' + start_text + '.*')).findParent()
        #if parent.name == 'div':
        #    soup = parent
        #else:
        #    new_text = ''
        #    while parent:
        #        new_text += str(parent)
        #        parent = parent.nextSibling
        #    soup = BeautifulSoup(new_text)

    content = '\n'.join([x for x in soup.findAll(text=True)
                        if type(x) != Comment and
                           type(x) != CData and
                           type(x) != Declaration and
                           type(x) != ProcessingInstruction])
    content = '\n'.join( [x for x in content.split('\n') if len(x.split()) >= 12] )
    if depth == 0:
        return content, comments
    return content

if __name__ == "__main__":
    content = urllib.urlopen(sys.argv[1]).read()
    start = None
    if len(sys.argv) == 3:
        start = sys.argv[2]
    content, comments = clean_data( content, start )
    print "CONTENT"
    print "--------------------------------------------"
    print content
    for comment in comments:
        print "--------------------------------------------"
        print comment

