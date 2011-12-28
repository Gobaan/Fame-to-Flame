#!/usr/bin/python
import re
from BeautifulSoup import BeautifulSoup
import helper

get_movies = re.compile('a href="/reviews/(.*?)"', re.DOTALL)
get_title = re.compile('<h3 class="summary">(.*?)</h3>',
  re.DOTALL | re.MULTILINE)
get_comments = re.compile(
  '<p class="bz-model-review-comments description">(.*?)</p>',
  re.DOTALL | re.MULTILINE)
get_ratio = re.compile(
  '<span class="prReviewHelpfulCount">(.*?)</span>', re.DOTALL)

get_rating = re.compile('<span class="rating">(.*?)</span>',
    re.DOTALL)

get_product = re.compile('<title>(.*?) Reviews | Buzzillions.com</title>')

def process_url(url, output):
    results = []
    product =  get_product.search(output).group(1)
    output = output[output.find('<div class="bz-model-review-content'):]
    titles = get_title.findall(output)
    comments = get_comments.findall(output)
    title_section = get_ratio.findall(output)
    ratings = get_rating.findall(output)
    for i in xrange(len(titles)):
        ret = {}
        ret['max_score'] = 5
        ret['score'] = ratings[i].strip()
        page = comments[i].strip()
        title = titles[i].strip()
        title_text = ''.join(BeautifulSoup(title,
          convertEntities = BeautifulSoup.HTML_ENTITIES).findAll(text=True))
        content = ''.join(BeautifulSoup(page,
          convertEntities = BeautifulSoup.HTML_ENTITIES).findAll(text=True))
        ret['content'] = content
        ret['title'] = title_text
        ret['link'] = url
        ret['parser'] = 'Buzzillions'
        ret['product'] = product
        results += [ret]
    return results

def search (keywords, max_results = 10):
    """
    Function search(keywords)
    Searches buzillions for the current set of keywords, note buzillions
    seems to aggressively throttle when more then 3 links are opened ?
    parameters:
    keywords - A string with all the keywords to search
    Output:
    Outputs a dictionary with the following keys
    title    - The title of this review
    title_section - The entire section containing the title in this review
    content  - The content of this review
    link     - The link that lead to this review
    """
    base_url = ("http://www.buzzillions.com/x/s?N=4294811422&D=x&cat=&extra=all-product&Ntt=%s" % keywords)
    responses = helper.parallel_fetch([base_url])
    urls = set([('http://www.buzzillions.com/reviews/%s' % link).split('#')[0]
             for link in get_movies.findall( responses.values()[0] )[:5]])
    responses = helper.parallel_fetch(urls)
    results = []
    for url in responses:
      results += process_url(url, responses[url])
    return results

if __name__ == '__main__':
    import sys
    for result in search(sys.argv[1]):
        print result
