#!/usr/bin/python
#import mechanize
from BeautifulSoup import BeautifulSoup
import re
import sys
import urllib
import helper

def parse(url, output):
    try:
        ret = {}
        soup = BeautifulSoup(output)
        ret['score'] = soup.find("span", {"class" : "rating"}).text
        ret['max_score'] = 5
        ret['link'] = url
        ret['title'] = soup.find("title").text
        get_content = re.compile('<p><strong>(.*)</?p> <div class=\"reviewWrap\"', re.DOTALL | re.MULTILINE)
        #matches = get_content.findall(output);

        if get_content.findall(output):
            ret['content'] = get_content.findall(output)[0]
        else:
            ret['content'] = soup.find("div", {"class" : "reviewSummary"}).text
        ret['content'] = re.sub("<[^>]*?>", "", ret['content'])
        ret['parser'] = 'CNET'
        ret['product'] = soup.find("div", {"class" : "titleWrap"}).find("span").text
        return ret
    except Exception , e:
        return None

def search(keyword):
    base_url = "http://reviews.cnet.com/1770-5_7-0.html?query=%s&tag=srch" % (keyword)
    output = urllib.urlopen(base_url).read()
    soup = BeautifulSoup(output)
    urls = [("http://reviews.cnet.com" + x.find("a", {"class" : "resultName"})['href'] + "?tag=contentMain;contentBody;1r")
            for x in soup.findAll("div", {"class" : "resultInfo"})]
    urls = [x for x in urls if x.find("http://", 1) == -1]
    responses = helper.parallel_fetch(urls)
    results = []
    for url in responses:
        results += [parse(url, responses[url])]
    return [x for x in results if x]

    #return soup

if __name__ == '__main__':
    results = search(sys.argv[1])
