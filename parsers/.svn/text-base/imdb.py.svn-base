#!/usr/bin/python
import re
from BeautifulSoup import BeautifulSoup
from subprocess import Popen, PIPE
import helper

get_exact_matches = re.compile("""<p><b>Titles \(Exact Matches\)</b>(.*?)</table>""",
   re.DOTALL | re.MULTILINE)

get_partial_matches = re.compile("""<p><b>Titles \(Partial Matches\)</b>(.*?)</table>""",
   re.DOTALL | re.MULTILINE)

get_popular_matches = re.compile("""<p><b>Popular Titles</b>(.*?)</table>""",
   re.DOTALL | re.MULTILINE)
get_movies = re.compile('a href="/title/(.*?)/"', re.DOTALL)
get_text = re.compile('^<p>\n^<small>(.*?)</p>\n<p>(.*?)</p>', re.DOTALL | re.MULTILINE)
get_title = re.compile('^<b>(.*?)</b>', re.DOTALL | re.MULTILINE)
get_rating = re.compile('showtimes/(.*?).gif', re.DOTALL)
get_product = re.compile('<title>(.*?) - IMDb user reviews</title>')
f = Popen(["java",
           "-cp",
           "sentimentDemo.jar:lingpipe-4.0.0.jar",
           "PolarityWhole"], stdin = PIPE, stdout = PIPE)
f.stdout.readline()

def process_url(url, output):
  results = []
  product = get_product.search(output).group(1)
  matches = get_text.findall(output)
  for title_section, content in matches:
      ret = {}
      content = ''.join(BeautifulSoup(content.strip(),
        convertEntities = BeautifulSoup.HTML_ENTITIES).findAll(text=True))
      ret['content'] = content
      title = get_title.search(title_section).group(0)
      title_text = ''.join(BeautifulSoup(title,
        convertEntities = BeautifulSoup.HTML_ENTITIES).findAll(text=True))
      ret['title'] = title_text
      ret['link'] = url
      ret['max_score'] = 100
      ret['score'] = None
      ret['parser'] = 'imdb'
      ret['product'] = product
      # This try catch deals with sentiment missing
      try:
          rating = get_rating.search(title_section).group(1)
          ret['score'] = rating
          f.stdin.write("train\n")
          if int(rating) < 60:
            f.stdin.write("negative\n")
          elif int(rating) > 70:
            f.stdin.write("positive\n")
          f.stdin.write("%s\n" % content.encode('utf-8'))
      except Exception, e:
          f.stdin.write("test\n")
          f.stdin.write("%s\n" % content.encode('utf-8'))
          rating = f.stdout.readline().strip()
          if rating == "true":
            ret['score'] = '85'
          else:
            ret['score'] = '30'
      results += [ret]
  return results

def search (keyword, max_results = 10):
    base_url = "http://www.imdb.com/find?s=all&q=%s" % (keyword)
    responses = helper.parallel_fetch([base_url])

    exact_titles = get_exact_matches.search(responses.values()[0])
    popular_titles = get_popular_matches.search(responses.values()[0])
    partial_titles = get_partial_matches.search(responses.values()[0])
    titles = []

    if popular_titles:
      titles += [popular_titles.group(0)]

    if exact_titles:
      titles += [exact_titles.group(0)]

    if partial_titles:
      titles += [partial_titles.group(0)]

    titles = '\n'.join(titles).strip()
    if not titles: return []

    urls = ['http://www.imdb.com/title/%s/usercomments' %  link for link in
        get_movies.findall( titles )[:5]]
    responses = helper.parallel_fetch(urls)
    results = []
    for url in responses:
      results += process_url(url, responses[url])
    return results

if __name__ == '__main__':
    import sys
    for result in search(sys.argv[1]):
        print result
    f.stdin.write('exit\n')
