import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from soblogitsgood.lib.base import BaseController, render

import sys
# mydevenv screws up path
sys.path.append("/usr/local/lib/python2.6/dist-packages/solrpy-0.9.1-py2.6.egg")
sys.path.append("/usr/lib/pymodules/python2.6")
sys.path.append("/usr/lib/python2.6/dist-packages/")
sys.path.append("../../n-grams")
import ngrams
import solr

import matplotlib
matplotlib.use('Agg')
import pylab
import PIL, PIL.Image, StringIO, threading

imageThreadLock = threading.Lock()

log = logging.getLogger(__name__)

def sanitize(query):
  # Escape characters for Solr query
  escape_chars = ['+', '-', '!', '(', ')', '{', '}', '[', ']',
                  '^', '"', '~', '*', '?', ':', '\\']

  out = ""
  for char in query:
    if char in escape_chars:
      out += '\\'
    out += char

  out = out.replace("&&", "\\&&")
  out = out.replace("||", "\\||")

  return out

class HelloController(BaseController):

    def index(self):
        # Return a rendered template
        c.service = "search"
        return render('/index.mako')

    def search(self):
        c.service = "search"
        query = request.params['query']
        if request.params.has_key('start'):
          start = request.params['start']
        else:
          start = 0

        if query.strip() == "":
          return render('/index.mako')

        conn = solr.SolrConnection('http://localhost:8983/solr')

        # Grab data from Solr
        params = {'q': sanitize(query), 'rows' : 10, 'start': start}
        results = conn.query(**(params))
        conn.close()


        if len(results) == 0:
          c.query = query
          return render('/noresults.mako')

        # Send params to context
        c.start = start
        c.results = results
        c.query = query

        return render('/results.mako')

    def custom(self):
        c.service = "custom"
        query = request.params['query']

        if request.params.has_key('start'):
          start = float(request.params['start'])
        else:
          start = -1.0

        if request.params.has_key('end'):
          end = float(request.params['end'])
        else:
          end = 1.0

        if query.strip() == "":
          return render('/index.mako')

        conn = solr.SolrConnection('http://localhost:8983/solr')

        # Grab data from Solr
        params = {'q': sanitize(query) + " sentiment:[%f TO %f]" % (start, end),
                  'rows' : 10}
        results = conn.query(**(params))
        conn.close()

        c.query = query

        if len(results) == 0:
          return render('/noresults.mako')

        c.results = results
        c.start = start
        c.end = end

        return render('/custom.mako')

    def polarize(self):
        c.service = "polarize"

        query = request.params['query']

        if query.strip() == "":
          return render('/index.mako')

        conn = solr.SolrConnection('http://localhost:8983/solr')

        # Grab data from Solr
        params = {'q': sanitize(query) + " sentiment:[0.0 TO 1.0]", 'rows' : 10}
        good_results = conn.query(**(params))
        params = {'q': sanitize(query) + " sentiment:[-1.0 TO 0.0]", 'rows' : 10}
        bad_results = conn.query(**(params))
        conn.close()

        if not (good_results or bad_results):
          c.query = query
          return render('/noresults.mako')

        # Do ngrams analysis
        goodText = ''.join(hit['content'] for hit in good_results.results)
        badText = ''.join(hit['content'] for hit in bad_results.results)
        q, p = ngrams.main(goodText, badText, ngrams.getWordsForDisplay)

        # Send params to context
        c.goodTerms = q #[i[0] for i in q]
        c.badTerms = p #[i[0] for i in p]

        c.goodResults = good_results
        c.badResults = bad_results

        c.query = query

        return render('/polarize.mako')

    def analysis(self):
        query = request.params['query']

        if query.strip() == "":
          return render('/index.mako')

        conn = solr.SolrConnection('http://localhost:8983/solr')

        # Grab polarized data from Solr
        params = {'q': sanitize(query) + " sentiment:[0.0 TO 1.0]", 'rows' : 10}
        good_results = conn.query(**(params))
        params = {'q': sanitize(query) + " sentiment:[-1.0 TO 0.0]", 'rows' : 10}
        bad_results = conn.query(**(params))

        # Grab data from Solr
        params = {'q': sanitize(query), 'rows' : 500, 'start': 0}
        results = conn.query(**(params))
        conn.close()

        # Do ngrams analysis
        goodText = ''.join(hit['content'] for hit in good_results.results)
        badText = ''.join(hit['content'] for hit in bad_results.results)
        c.goodTerms, c.badTerms = ngrams.main(goodText, badText, ngrams.getWordsForDisplay)

        c.goodCount = good_results.numFound
        c.badCount = bad_results.numFound

        c.goodResults = good_results
        c.badResults = bad_results

        c.query = query

        if len(results) == 0:
          return render('/noresults.mako')

        c.results = results
        c.service = "analysis"
        return render('/analysis.mako')

    def testImg(self):
        SIZE = 2.5
        DPI = 100
        DIM = int(SIZE * DPI)
        SIDE = 0
        TOP = int(0.15 * DIM)

        global imageThreadLock

        gr = int(request.params['gr'])
        br = int(request.params['br'])

        percent = min(float(gr) / (gr + br), float(br) / (gr + br))

        if percent > 0.35:
          TOP = int(0.1 * DIM)

        # set the response type to PNG, since we at least hope to return a PNG image here
        response.content_type = 'image/png'

        # make a buffer to hold our data
        buffer = StringIO.StringIO()

        # lock graphics
        imageThreadLock.acquire()

        # we don't want different threads to write on each other's canvases, so make sure we have a new one
        pylab.close()

        pylab.figure(figsize=(SIZE,SIZE), dpi=DPI, frameon=False)

        canvas = pylab.get_current_fig_manager().canvas

        # quick simple plot
        pylab.pie([gr, br],
                  explode = [0.05, 0.05],
                  labels = ["Good", "Bad"],
                  colors = ['#49BD43', '#F95353'])

        canvas.draw()
        imageSize = canvas.get_width_height()
        imageRgb = canvas.tostring_rgb()
        pilImage = PIL.Image.fromstring("RGB", imageSize, imageRgb)

        pilImage = pilImage.crop([SIDE, TOP, DIM - SIDE, DIM - TOP])

        pilImage.save(buffer, "PNG") # <-- we will be sending the browser a "PNG file"

        # unlock graphics
        imageThreadLock.release()

        return buffer.getvalue()


    def feedback(self):
        # Get feedback for a result
        # request.params has guid and type ("up" or "down")

        conn = solr.SolrConnection('http://localhost:8983/solr')
        # Get solrpy to do the update
        conn.close()

# vi: set ts=4 sts=4 sw=4:
