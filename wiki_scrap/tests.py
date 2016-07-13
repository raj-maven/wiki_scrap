import unittest

from pyramid import testing


class ViewHomeTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_it(self):
        from .views import home
        request = testing.DummyRequest()
        info = home(request)
        self.assertEqual(info['project'], 'wiki_scrap')

class ViewResultTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_it(self):
        from .views import result
        request = testing.DummyRequest()
        info = result(request)
        self.assertEqual(info['error'], 'Please enter the Url first.')