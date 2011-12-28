import sqlite3
import logging
import threading
import time

from xmltools import xml

from multiprocessing import Pool

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect, Response

from soblogitsgood.lib.base import BaseController, render

log = logging.getLogger(__name__)

import sys
sys.path.append("/usr/lib/pymodules/python2.6")
sys.path.append("/usr/lib/python2.6/dist-packages/")
sys.path.append("/usr/local/lib/python2.6/dist-packages/")
sys.path.append("/usr/local/lib/python2.6/dist-packages/mechanize-0.2.4-py2.6.egg")
sys.path.append("../../parsers/")
sys.path.append("../../n-grams")
import ngrams
import amazon
import wired
import imdb
import epinions
import cnet
import buzzillions


USE_CACHE = True
WORKER_TIMEOUT = 10
positive_cutoff = .7
negative_cutoff = .6

# Global map of ongoing queries to their ResultSets
query_results = {}

"CREATE TABLE search_results(query, link, title, sentiment, content, score, max_score, product, parser)"
def alreadySearched(query, conn):
    if not conn: return False
    try:
        cursor = conn.cursor ()
        cursor.execute( """SELECT * FROM search_results WHERE query="%s" """ % query)
        return cursor.fetchone()
    except Exception , e:
        print "Error in alreadySearched:", e
        return False;

def retrieveCachedResults(query, conn):
    if not conn: return False
    cursor = conn.cursor ()
    cursor.execute( """SELECT link, title, sentiment, content, score, max_score, product, parser FROM search_results WHERE query="%s" """ % query);
    results = []
    for row in cursor:
        result = {}
        result['link'] = row[0]
        result['title'] = row[1]
        result['sentiment'] = float(row[2])
        result['content'] = row[3]
        result['score'] = float(row[4])
        result['max_score'] = float(row[5])
        result['product'] = row[6]
        result['parser'] = row[7]
        results += [result]
    return results

def store_mysql(searchquery, entries, conn):
    if not conn: return
    cursor = conn.cursor ()
    print 'storing mysql ' + searchquery
    for entry in entries:
        try:
            args = (searchquery.decode("utf-8", "replace"),
                    entry['link'].decode("utf-8", "replace"),
                    entry['title'].decode("utf-8", "replace").replace("'", ""),
                    str(entry['sentiment']).decode("utf-8", "replace"),
                    entry['content'].decode("utf-8", "replace").replace("'", ""),
                    str(entry['score']).decode("utf-8", "replace"),
                    str(entry['max_score']).decode("utf-8", "replace"),
                    str(entry['product']).decode("utf-8", "replace").replace("'", "''"),
                    str(entry['parser']).decode("utf-8", "replace"))
            query = ( u"""INSERT INTO search_results VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"""
                      % args)
            cursor.execute(query)
            conn.commit()

        except Exception , e: #TODO Fix this exception
            print "Store mysql error:", e

class ResultSet:
  """Keeps track of asynchronous results of queries"""
  def __init__(self, num_callbacks=1):
    self.mutex = threading.Lock()
    self.event = threading.Event()
    self.results = []
    self.callback_limit = num_callbacks
    self.callbacks = 0

  def addResults(self, results):
    self.callbacks += 1
    self.mutex.acquire()
    self.results.extend(results)
    self.event.set()
    self.mutex.release()

  def tryGetResults(self):
    self.mutex.acquire()
    try:
      if self.results:
        # Return available results
        ret = self.results
        self.results = []
        return ret
      elif self.callbacks >= self.callback_limit:
        # Indicate no more results
         return None
      else:
        # No results at this time
        return []
    finally:
      self.mutex.release()

  def getResults(self):
    self.mutex.acquire()
    try:
      if self.results:
        # Return available results
        ret = self.results
        self.results = []
        return ret
      elif self.callbacks >= self.callback_limit:
        # Indicate no more results
        return None
      else:
        # Block until we have results
        self.mutex.release()
        self.event.wait(timeout=WORKER_TIMEOUT)
        if not self.event.isSet():
          print "worker timeout"
          self.mutex.acquire()
          return None
        self.mutex.acquire()
        self.event.clear()

        ret = self.results
        self.results = []
        return ret
    finally:
      self.mutex.release()


### For printing results ###
def summarize(text, term):
    BACK = 50
    LENGTH = 400
    CHECK = 25
    index = text.lower().find(term.lower())
    if index < 0:
      left = 0
    # Find a chunk of text around the search term
    left = max(0, index - BACK)
    right = min(len(text), left + LENGTH)

    # Find if the ranges are close to periods
    lcheck = max(0, left - CHECK)
    rcheck = right - CHECK

    lstop = text.find(".", lcheck)
    rstop = text.find(".", rcheck)

    prefix = "..."
    postfix = "..."

    if abs(left - lstop) <= CHECK:
      left = lstop + 1
      prefix = ""
    if abs(right - rstop) <= CHECK:
      right = rstop + 1
      postfix = ""
    if left == 0:
      prefix = ""
    if right == len(text):
      postfix = ""

    return prefix + text[left:right].strip() + postfix# + "~%d, %d" % (left, right)

def boldTerm(text, terms):
    out = text
    index = -8
    for term in terms.split():
      while (True):
        index = out.lower().find(term.lower(), index + 8)
        if index >= 0:
          out = "%s<b>%s</b>%s" % (out[:index],
                                   out[index:index + len(term)],
                                   out[index + len(term):])
        else:
          break

    return out

def markupResult(result, query):
  ret = """
  <h3 class="resultLink">
    <a href="%s">%s</a><br/>
  </h3>
  <p class="result">
  """ % (result['link'], boldTerm(result['product'], query) + ' - ' + boldTerm(result['title'], query))

  try:
    ret += "<span class=\"source\">Source: " + result['parser'] + "</span><br/>"
  except KeyError, e:
    print "KeyError: %s" % e

  if result['sentiment'] >= positive_cutoff:
    ret += "<span class=\"good\">Sentiment: %d%%</span><br/>" % (result['sentiment'] * 100)
  elif result['sentiment'] < negative_cutoff:
    ret += "<span class=\"bad\">Sentiment: %d%%</span><br/>" % (result['sentiment'] * 100)
  else:
    ret += "<span class=\"neutral\">Sentiment: %d%%</span><br/>" % (result['sentiment'] * 100)

  ret += boldTerm(summarize(result['content'], query), query)
  ret += "</p>"
  return ret

def productfix(char):
  if char.isalnum():
    return char
  elif char == "-" or char == "_":
    return char
  elif char.isspace():
    return "_"
  else:
    return "_"

def fix(s):
  return "".join([productfix(c) for c in s])

class MetasearchController(BaseController):
    # Dispatchers return results as dictionaries with the following format:
    #    title
    #    link
    #    content
    #    score*
    #    max_score*
    #    title_section*
    # Where asterisks mark optional fields
  def __init__(self):
    self.pool = Pool(len(self.getSearchers()))

  def getSearchWrappers(self, query):
    '''Generates functions that search for given query.
       Inner functions only need to know which searcher to use.
    '''
    def wrapper(searcher):
      return searcher(query)
    return wrapper

  def getCallbackWrapper(self, query, fromCache = False):
    def wrapper(current_results):
      actual_results = []
      for result in current_results:
        if result is None:
            continue
        result['sentiment'] = float(result['score']) / float(result['max_score'])
        if result['content'] is None:
            result['content'] = ""
        try:
            result['content'] = result['content'].decode("ascii")
            result['title'] = result['title'].decode("ascii")
            result['content'] = result['content'].encode("ascii")
            result['title'] = result['title'].encode("ascii")
            actual_results += [result]
        except Exception , e: #TODO Fix this exception
            print 'error with res -', e, result["parser"]
            continue
      query_results[query.replace(' ', '+')].addResults(actual_results)
      if not fromCache and USE_CACHE:
          conn = None
          conn = sqlite3.connect( "search_results")
          store_mysql(query, current_results, conn)

    #TODO: Cache results

    return wrapper

  def index(self):
    # Return a rendered template
    #return render('/metasearch.mako')
    # or, return a string
    c.service = "polarize"
    return render('/index.mako')

  def getSearchers(self):
    return [buzzillions.search, imdb.search, epinions.search, wired.search,
            cnet.search, amazon.search]

  def startAsyncSearch(self, query):
    if USE_CACHE:
      conn = None
      conn = sqlite3.connect( "search_results")
      query = query.replace(' ', '+')
      if alreadySearched(query, conn):
          print 'already searched'
          query_results[query.replace(' ', '+')] = ResultSet(1)
          try:
              self.getCallbackWrapper(query, True)(retrieveCachedResults(query, conn))
              return
          except Exception , e:
              print "Some exception in getting cached results"
              print e
    searchers = self.getSearchers()
    query_results[query.replace(' ', '+')] = ResultSet(len(searchers))
    [self.pool.apply_async(searcher,
                           (query,),
                           callback=self.getCallbackWrapper(query))
     for searcher in searchers]

  def getAllResults(self, query):
    self.startAsyncSearch(query)
    results = []
    while True:
      cur_results = query_results[query.replace(' ', '+')].getResults()
      if cur_results is None:
        break
      else:
        results.extend(cur_results)

    return results

  def getasyncresults(self):
    query = request.params['query']
    print "Get async: %s" % (query)
    try:
      results = query_results[query.replace(' ', '+')].tryGetResults()

      # Format nicely
      if results is None:
        print "No more results: %s" % (request.params['query'])
        ret = "<results>\n<stop/></results>"
      elif results == []:
        print "No results at this time: %s" % (request.params['query'])
        ret = "<results></results>"
      else:
        ret = "<results>\n"
        print "Got Results: %s" % (request.params['query'])
        for result in results:
          ret += ("<result><sentiment>%s</sentiment><source>%s</source><product>%s</product><cssproduct>%s</cssproduct><content>%s</content></result>\n"
              % (result['sentiment'],
                 result['parser'],
                 xml.escape(result['product']),
                 "".join([productfix(c) for c in result['product']]),
                 xml.escape(markupResult(result, request.params['query']))))

        ret += "</results>"

      response = Response(ret)
      response.headers['content-type'] = "text/xml"
      return response
    except KeyError:
      # Async request for a non-existant query
      return None

  def search(self):
    c.service = "search"
    c.query = request.params['query']

    if c.query.strip() == "":
      return render('/index.mako')

    self.startAsyncSearch(c.query)
    return render('/metaresults.mako')

  def polarize(self):
    c.service = "polarize"
    c.query = request.params['query']

    if c.query.strip() == "":
      return render('/index.mako')

    self.startAsyncSearch(c.query)
    return render('/polarize.mako')


  def analysis(self):
    c.service = "analysis"
    c.query = request.params['query']

    if c.query.strip() == "":
      return render('/index.mako')

    c.results = self.getAllResults(c.query)

    c.categories = {}
    for r in c.results:
      if r['parser'] not in c.categories:
        c.categories[r['parser']] = []
      if r['product'] not in c.categories[r['parser']]:
        c.categories[r['parser']].append(r['product'])

    narrowparsers = None
    narrowproducts = None

    if "narrow" in request.params:
      newresults = []
      narrowparsers = request.params['sources'].split(",")
      narrowparsers = [s[8:] for s in narrowparsers]
      narrowproducts = request.params['products'].split(",")
      narrowproducts = [s[7:] for s in narrowproducts]

      for r in c.results:
        if (fix(r['product']) in narrowproducts and
            r['parser'] in narrowparsers):
          newresults.append(r)

      c.results = newresults
    c.narrowparsers = narrowparsers
    c.narrowproducts = narrowproducts

    if len(c.results) == 0:
      return render('/noresults.mako')

    good_results = [hit for hit in c.results if hit['sentiment'] >= positive_cutoff]
    neutral_results = [hit for hit in c.results 
        if hit['sentiment'] < positive_cutoff and hit['sentiment'] >= negative_cutoff]
    bad_results = [hit for hit in c.results if hit['sentiment'] < negative_cutoff]

    sent_sum = 0.0
    for hit in c.results:
      sent_sum += hit['sentiment']

    c.mean = sent_sum / len(c.results)
    c.std_dev = 0
    for hit in c.results:
      c.std_dev += (hit['sentiment'] - c.mean)**2

    c.std_dev = (c.std_dev/len(c.results))**(1.0/2)

    c.verdict = ""
    if c.std_dev < 0.20:
      c.verdict = "Universal "
    elif c.std_dev < 0.35:
      c.verdict = "Disputed "
    else:
      c.verdict = "Hotly contested "

    if c.mean < 0.35:
      c.verdict += "disapproval"
    elif c.mean < 0.65:
      c.verdict += "mediocre reviews"
    else:
      c.verdict += "approval"

    goodText = ''
    badText = ''
    for hit in good_results:
        try:
            goodText += hit['content']
        except Exception , e:
            print 'good_results error', e
            pass
    for hit in bad_results:
        try:
            badText += hit['content']
        except Exception , e:
            print 'bad_results error', e
            pass

    #goodText = ''.join(hit['content'] for hit in good_results)
    #badText = ''.join(hit['content'] for hit in bad_results)

    c.goodTerms, c.badTerms = ngrams.main(goodText, badText,
        ngrams.getWordsForDisplay)

    c.goodResults = good_results
    c.neutralResults = neutral_results
    c.badResults = bad_results

    return render('/analysis.mako')

  def custom(self):
    c.service = "search"
    c.query = request.params['query']

    if c.query.strip() == "":
      return render('/index.mako')

    self.startAsyncSearch(c.query)
    return render('/custom.mako')

# vi: set ts=2 sts=2 sw=2:
