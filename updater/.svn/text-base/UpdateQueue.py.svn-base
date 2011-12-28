
import heapq, mutex, time, threading
#Note: this may have to be moved to some other language(Jython?) due to retarded Python threading

class UpdateQueue:
    """UpdateQueue that keeps track of feeds.  Is prioritized
    based on the next feed that should be updated."""

    def __init__(self):
        self.__items__ = []
        self.__lock__ = threading.Lock()

    def next(self):
        """Pops and returns the next feed to be updated off this queue."""
        self.__lock__.acquire()
        self.__added__ = False
        while len(self.__items__) == 0:
            self.__lock__.release()
            time.sleep(1)
            self.__lock__.acquire()
        item = heapq.heappop(self.__items__)
        self.__lock__.release()
        while (item.lastUpdated + item.updateInterval) - time.time() > 0:
            time.sleep((item.lastUpdated + item.updateInterval) - time.time())
        return item

    def add(self, feed):
        """Adds a feed to this queue."""
        self.__lock__.acquire()
        for item in self.__items__:
            if item.url == feed.url:
                self.__lock__.release()
                return None
        heapq.heappush(self.__items__, feed)
        self.__lock__.release()


