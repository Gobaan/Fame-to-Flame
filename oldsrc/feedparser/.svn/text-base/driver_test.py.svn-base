import unittest
from driver import strip, getDoc


class mockFeed:
    def __init__(self):
        self.title = "title"
        self.link = "link"
        self.description = "description"

class mockItem:
    def __init__(self):
        self.title = "item title"
        self.link = "item link"
        self.description = "item description"

result = """<doc>
    <field name="channelTitle">title</field>
    <field name="channelLink">link</field>
    <field name="channelDescription">description</field>
    <field name="title">item title</field>
    <field name="link">item link</field>
    <field name="description">item description</field>
</doc>
"""

class DriverTestCase( unittest.TestCase ):
    def testStrip(self):
        self.assertEqual(strip("test"), "test")
        self.assertEqual(strip("test<br>"), "test")

    def testGetDoc(self):
        self.assertEqual(getDoc( mockFeed(), mockItem() ), result)

def getSuite():
  return unittest.TestLoader().loadTestsFromTestCase(DriverTestCase)

if __name__ == "__main__":
  unittest.TextTestRunner().run(getSuite())
