import getopt, sys
import SearchFilter

def usage():
    print '''
Usage: python SoBlogItsGood.py <args>
-h, --help                  Prints this information and exits
-v                          Prints extended information about each command
--blog                      Fetches a blog as opposed to a blog post
--post                      Fetches a blog post (default)
--solr                      Uses SQL instead of SOLR
--query='<string>'          List of terms to search the solr database for
--category=<Category>       Category to search for the terms in
--sentiment=<Good|Bad>      Whether the article sentiments should be good or bad
--startdate=<date>          Return only articles with published dates after this date
--enddate=<date>            Return only articles with published dates before this date
--randomseed=<int>          Specify a random seed for returned results for consistency
--limit=<int>               Specify how many articles to return (default/max = 50)
'''

def main():
    try:
        lowered_args = [arg.lower() for arg in sys.argv[1:]]
        opts, args = getopt.getopt(lowered_args, "hv",
                                                 ["help",
                                                  "blog",
                                                  "post",
                                                  "solr",
                                                  "query=",
                                                  "category=",
                                                  "sentiment=",
                                                  "startdate=",
                                                  "enddate=",
                                                  "randomseed=",
                                                  "limit=",
                                                 ])

    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    opts = dict(opts)
    if '-h' in opts or '--help' in opts or '-v' in opts:
        usage()
        sys.exit(0)
    opts['--query'] = '&'.join(opts['--query'].split())
    filter = SearchFilter.SearchFilter(opts['--query'],
                          opts['--category'],
                          opts['--sentiment'],
                          opts['--startdate'],
                          opts['--enddate'],
                          int(opts['--randomseed']),
                          int(opts['--limit']),
                        )
    type = 'solr'
    connection = SearchFilter.Connection(type)
    if '--blog' in opts:
        print 'fetching blog'
        print '\n'.join(connection.getBlog(filter))
    else:
        print 'fetching post'
        for elt in connection.getBlogPost(filter):
            print elt


if __name__ == "__main__":
    main()

