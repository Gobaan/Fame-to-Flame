from BeautifulSoup import BeautifulSoup
import re, sys, urllib
import helper
import pdb

score_pattern = re.compile("(\d)\.0 out of 5 stars")
#product_pattern = re.compile("http://www.amazon.com/([^/]*)/")
title_pattern = re.compile("</span>\s*<b>(.*)./b.")
title_pattern2 = re.compile("""<span style..vertical.align.middle..><b>(.*?)</b>""")
review_pattern = re.compile("(\d)\.0 out of 5 stars.*?<b>(.*?)</b>.*?(?:.*?This review is from:)?.*?</div>\s*(.*?)<div", re.DOTALL)
#review_pattern2 = re.compile("(?:\d)\.0 out of 5 stars.*?</span></span> </span>\s*(.*?)<div", re.DOTALL | re.MULTILINE)
product_pattern = re.compile('\<span id="btAsinTitle"( style="")?>([^\<]*)\<')

def parse_url(url, text):
    reviews = text.split("<!-- BOUNDARY -->")

    reviews = reviews[1:]
    lst = []
    for review in reviews:
        try:
            ret = {}
            ret['link'] = url
            ret['max_score'] = 5
            ret['score'] = score_pattern.search(review).groups()[0]
            content = re.sub(score_pattern, "", review_pattern.search(review).group(0))
            content = re.sub("<[^>]*>", "", content).strip()
            content = re.sub("<[^>]*>", "", content)
            content = re.sub("^[^>]*>" ,"", content)
            content = re.sub("<.*$" ,"", content)
            content =  content.strip().split("\n")
            while re.match("^\w+$",content[-1]) or re.search("Read more", content[-1]):
                content = content[:-1]
            ret['content'] = content[-1].strip()
#            print product_pattern.search(text).groups()
            ret['product'] = product_pattern.search(text).groups()[1].strip()
            ret['parser'] = 'Amazon'
            ret['title'] = content[0].strip()
            lst.append(ret)
        except Exception, e:
            print url, '-', e
    return lst


def search(keyword):
    print 'searching amazon'
    url = "http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=" + keyword + "%s&x=0&y=0"
    soup = BeautifulSoup(urllib.urlopen(url).read())
    #print soup
    urls = [x.a['href'] for x in soup.findAll('div', {"class": "productTitle"})][:5]
    responses = helper.parallel_fetch(urls)
    results = []
    for url in responses:
        results += parse_url(url, responses[url])
    #print results
    print 'returning amazon'
    return results

if __name__ == '__main__':
    for result in  search(sys.argv[1]):
        #print result
        print result['product']

