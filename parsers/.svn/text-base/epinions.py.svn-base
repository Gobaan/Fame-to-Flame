#!/usr/bin/python
import re
from BeautifulSoup import BeautifulSoup
import helper


get_movies = re.compile('href="/prices/(.*?)"', re.DOTALL)
get_review = re.compile('href="/review/(.*?)"', re.DOTALL)
get_text = re.compile('^<tr bgcolor="white">(.*?)^</tr>',
 re.DOTALL | re.MULTILINE)
get_title = re.compile('<title>(.*?) - (.*?) - (.*?)</title>', re.DOTALL)
get_rating = re.compile('alt="Product Rating: (.*?)"', re.DOTALL)

def extract_reviews(data):
  return

def process_url(url, raw_review):
    titles = get_title.search(raw_review)
    title = titles.group(1)
    product = titles.group(2)
    review = raw_review[raw_review.find("Full Review:"):]
    review = review.split('\n')
    # After getting the a Full Review Tag the next line containing
    # nothing but whitespace is followed by the review
    for start in xrange(len(review)):
        if not review[start].strip(): break

    for end in xrange(start + 1, len(review)):
        if not review[end].strip(): break

    ret = {}
    page = ' '.join([line.strip() for line in review[start + 1:end]])
    title_text = ''.join(BeautifulSoup(title,
        convertEntities = BeautifulSoup.HTML_ENTITIES).findAll(text=True))
    content = ''.join(BeautifulSoup(page,
        convertEntities = BeautifulSoup.HTML_ENTITIES).findAll(text=True))
    product_text = ''.join(BeautifulSoup(product,
        convertEntities = BeautifulSoup.HTML_ENTITIES).findAll(text=True))

    ret['content'] = content
    ret['title'] = title_text
    ret['product'] = product_text
    ret['link'] = url
    ret['max_score'] = 5
    ret['parser'] = 'Epinions'
    rating = get_rating.search(raw_review).group(1).strip()
    ret['score'] = rating
    return [ret]


def search (keyword, max_results = 5):
    base_url = "http://www99.epinions.com/search/?search_string=%s" % (keyword)
    responses = helper.parallel_fetch([base_url])
    urls = set(['http://www99.epinions.com/reviews/%s' % link
             for link in get_movies.findall( responses.values()[0] )[:5]])

    responses = helper.parallel_fetch(urls)
    reviews = []
    for url in responses:
      reviews += ["http://www99.epinions.com/review/%s" % review for review in
        get_review.findall(responses[url])]
    reviews = set(reviews)

    responses = helper.parallel_fetch(reviews)
    results = []
    for url in responses:
      results += process_url(url, responses[url])
    return results

if __name__ == '__main__':
    import sys
    for result in search(sys.argv[1]):
        print result
