try:
    import json
except ImportError:
    import simplejson as json 

import urllib
import urllib2
import dateutil.parser

server_addr = 'localhost'
#Note need to figure out what makes a category, 
#and I guess put in hooks for sentiment?
class SearchFilter(object):
    def __init__(self,
                 query = '',
                 category = None,
                 sentiment = None,
                 start = None,
                 end = None,
                 random_seed = None,
                 limit = None): 
        # Add url or title?
        self.attributes = {
                      'query' : query,
                      'category' : category,
                      'sentiment': sentiment,
                      'start': start,
                      'end': end,
                      'random_seed': random_seed,
                      'limit' : limit,}

        for attr in self.attributes:
            setattr(self, attr, self.attributes[attr])

    def encode(self):
        return json.dumps(self.attributes, separators=(',', ':'))

    def decode(self, filter_json):
        if filter_json is None:
            # Set default attributes?
            return

        self.attributes = json.loads(filter_json)
        for attr in self.attributes:
            setattr(self, attr, self.attributes[attr])

    def toSQL(self):
        clause = []
        if self.start:
            clause += ["published <= '%s'" % dateutil.parser.parse(self.start)]
        if self.end:
            clause += ["published > '%s'" % dateutil.parser.parse(self.end)]
        clause = ' and '.join(clause)
        if clause:
            clause = ' WHERE ' + clause 

        if self.random_seed is not None:
            clause += ' ORDER BY RAND(%s) ' % self.random_seed

        clause += ' LIMIT %s' % min(self.limit or 50, 50)
        return clause 
            
 
    def toSolr(self):
        date_format = '%Y-%m-%dT%H:%M:%SZ'
        start, end = '*', '*'
        if self.start:
            start = dateutil.parser.parse(self.start).strftime(date_format)
        
        if self.end:
            end = dateutil.parser.parse(self.end).strftime(date_format)

        params = {'q' : '%s' % self.query,
                  'published' : '[%s TO %s]' % (start, end),
                  'rows' : min( self.limit or 50, 50 ), } 

        if self.random_seed is not None:
            params['sort'] = 'random_%s' % self.random_seed

        return params

class ConnectionError(Exception): pass

class UnknownType(ConnectionError): pass

#Todo test me
class Connection(object):
    types = ('solr')
    def __init__(self, type = 'solr'):
        if type not in Connection.types: 
            raise UnknownType

        self.type = type.lower()

    def getBlogPost(self, filter):
        url = 'http://%s:15863/%s/getBlogPost' % (server_addr, self.type)
        data = urllib.urlencode({'filter' : filter.encode()})
        f = urllib2.urlopen(url, data)
        return json.loads(f.read())
 
    def getBlog(self, filter):
        url = 'http://%s:15863/%s/getBlog' % (server_addr, self.type)
        data = urllib.urlencode({'filter' : filter.encode()})
        f = urllib2.urlopen(url, data)
        return json.loads(f.read())


if __name__ == '__main__':
    filter = SearchFilter('i',
                          'Technology', 
                          'good', 
                          '01-01-2010', 
                          '02-01-2010', 
                          5, 
                          5)
    json_str = filter.encode()
    print json_str
    filter2 = SearchFilter()
    filter2.decode(json_str)
    json_str2 = filter2.encode()
    print json_str2
    print '-' * 10
    client = Connection('solr')
    print '-' * 10
    client.getBlog(filter)
