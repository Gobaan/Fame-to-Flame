import unittest, time
from UpdateQueue import *
from Feed import *

class UpdateQueueTestCase( unittest.TestCase ):
    def testAdd(self):
        uq = UpdateQueue()
        f1 = Feed('feed2')
        f2 = Feed('feed4')
        f3 = Feed('feed5')
        f4 = Feed('feed1')
        f5 = Feed('feed3')
        f1.lastUpdated = 20
        f2.lastUpdated = 40
        f3.lastUpdated = 50
        f4.lastUpdated = 10
        f5.lastUpdated = 30
        f6 = feed('feed1')
        f5.updateInterval = 30 * 60
        uq.add(f1)
        uq.add(f2)
        uq.add(f3)
        uq.add(f4)
        uq.add(f5)
        uq.add(f6)
        self.assertEqual( uq.next(), f4 )
        self.assertEqual( uq.next(), f1 )
        self.assertEqual( uq.next(), f2 )
        self.assertEqual( uq.next(), f3 )
        self.assertEqual( uq.next(), f5 )

    def testNext(self):
        uq = UpdateQueue()
        f1 = Feed('feed1')
        f2 = Feed('feed2')
        f3 = Feed('feed3')
        f1.lastUpdated = 0
        f2.lastUpdated = time.time() - 5
        f3.lastUpdated = time.time()
        f2.updateInterval = 10
        f3.updateInterval = 6
        uq.add(f1)
        uq.add(f2)
        uq.add(f3)
        self.assertEqual(uq.next(), f1 )
        self.assertEqual(uq.next(), f2 )
        self.assertTrue(time.time() > (f2.lastUpdated + f2.updateInterval))
        self.assertEqual(uq.next(), f3 )
        self.assertTrue(time.time() > (f3.lastUpdated + f3.updateInterval))
        self.assertTrue((time.time() - (f3.lastUpdated + f3.updateInterval)) < 1)


def getSuite():
    return unittest.TestLoader().loadTestsFromTestCase(UpdateQueueTestCase)

if __name__ == "__main__":
  unittest.TextTestRunner().run(getSuite())
