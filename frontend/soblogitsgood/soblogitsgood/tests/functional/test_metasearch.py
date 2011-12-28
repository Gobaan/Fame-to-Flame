from soblogitsgood.tests import *

class TestMetasearchController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='metasearch', action='index'))
        # Test response...
