import BeautifulSoup, re, urllib, sys

comment_id = re.compile("comment|usertext")

def findComments(text):
    """
    Returns a list of comments in the given text.

    - <a name="comments"></a> followed by a list
    - <div class=".*comment.*"></div>
    - <div id=".*comment.*"></div>
    - <ul/dd/ol class=".*comment.*"> - all items are comments
    - <ul/dd/ol id=".*comment.*"> - all items are comments
    """

    soup = BeautifulSoup.BeautifulSoup(text)

    commentList = []

    try:
        commentList += soup.find('a', {"name" : comment_id}).parent.ul.findAll('li')
    except:
        None
    if not commentList:
        commentList += soup.findAll('div', id=comment_id)

    if not commentList:
        commentList += soup.findAll('div', {"class" : comment_id})

    if not commentList:
        try:
            commentList += soup.find(['dl', 'ol', 'ul'], id=comment_id).findAll(['li', 'dd'], {recursive: False})
        except:
            None

    if not commentList:
        try:
            commentList += soup.find(['dl', 'ol', 'ul'], {"class" : comment_id}).findAll(['li', 'dd'], {recursive: False})
        except:
            None

    [comment.extract() for comment in commentList]

    return unicode(soup), [str(comment) for comment in commentList]

if __name__ == '__main__':
    f = urllib.urlopen(sys.argv[1])
    content, comments = findComments(f.read())
    for c in comments:
        print c
        print "-------------------------------------"

