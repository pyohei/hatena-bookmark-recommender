"""Test of feed.py"""
import unittest
import feed
from sqlalchemy import create_engine

class TestFeed(unittest.TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        self.obj = feed.Feed(engine, 'test')
        self.response = None

    def test__make_feed_api_url(self):
        """Test code of _make_url"""
        result = 'http://b.hatena.ne.jp/test/rss?of=test'
        self.assertEqual(self.obj._make_feed_api_url('test'), result)

    def test__request(self):
        """Test request"""
        # Same with result of `test__make_entry_api_url`
        url = 'http://b.hatena.ne.jp/sample/rss?of=sample'
        r = self.obj._request(url)
        self.assertIsInstance(r, dict)
        #self.assertEqual(r, 'aa')
        self.response = r

    def test__process_entry(self):
        url = 'http://b.hatena.ne.jp/sample/rss?of=sample'
        r = self.obj._request(url)
        self.assertIsInstance(self.obj._process_entry(r), list)

    def test__is_long_url(self):
        """Test url is 255 byte."""
        base = 'x' * 255
        self.assertFalse(self.obj._is_long_url(base))
        self.assertTrue(self.obj._is_long_url(base+'x'))

if __name__ == '__main__':
    unittest.main()
