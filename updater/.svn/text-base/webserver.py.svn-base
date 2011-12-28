#TODO: make POST/GETs specific sites, instead of everything
import sqlite3
import store
import Feed, UpdateQueue
from threading import Thread

import cherrypy
from cherrypy import tools
from json import JSONEncoder

import traceback, sys

queue = UpdateQueue.UpdateQueue()

def feedExists(url, conn):
    """Returns whether or not the feed already exists in the DB."""
    c = conn.cursor()
    c.execute("SELECT feed_url FROM feeds WHERE feed_url = '"
              + url + "' limit 1")
    return c.fetchone()

class UpdateThread(Thread):
    "Thread that loops until quit, updating feeds"
    def run(self):
        conn = sqlite3.connect( "updater.db" )
        c = conn.cursor()
        c.execute( "SELECT * FROM feeds" )
        for row in c:
            queue.add( Feed.Feed(row[0], row[3], row[1], row[2], True) )
            print "Loading feeds for feed %s" % row[0]
        c.close()

        while(True):
            feed = queue.next()
            try:
                #Do we need another thread here?
                feed.update()
                # store.store_mysql(feed.feedEntries)
                print "About to store into SOLR"
                store.store_solr(feed.feedEntries)
                # free memory; don't hold onto entire entry set
                feed.feedEntries = None
                print "About to Save"
                feed.save(conn)
                print "Re-Adding to Queue"
                queue.add(feed)
            except Exception as e:
                print "Exception when processing feed URL " + feed.url
		traceback.print_exc(file=sys.stdout)

class Parser(object):
    def index(self, feed_url):
        """Handles a POST request.  Currently parses out the feed_url
        and adds it to the update queue"""
        conn = sqlite3.connect( 'updater.db' )
        if(not feedExists(feed_url, conn) ):
            print("Adding to Queue: ", feed_url)
            queue.add(Feed.Feed(feed_url))
        return "<HTML>POST OK.<BR><BR>%s" % feed_url

    def list (self):
        urls = [feed.url for feed in queue.__items__]
        urls = ['Length: %s' % len(urls)] + urls
        return '<BR>'.join(urls)

    list.exposed = True
    index.exposed = True

class ServerThread(Thread):
    "Thread that runs the webserver"
    def __init__(self, server):
        Thread.__init__(self)
        self.server = server

    def run(self):
        cherrypy.quickstart(self.server, '/', config='webserver.config')

def main():
    """Starts the webserver"""
    try:
        update_thread = UpdateThread()
        update_thread.start()

        server_thread = ServerThread(Parser())
        server_thread.start()
        server_thread.join()

    except KeyboardInterrupt:
        quit()

if __name__ == '__main__':
    store.initialize()
    main()

