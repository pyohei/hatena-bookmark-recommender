"""Test of feed.py"""
import unittest
import feed
from sqlalchemy import create_engine

class TestFeed(unittest.TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        self.obj = feed.Feed(engine, 'test')

    def test__make_feed_api_url(self):
        """Test code of _make_url"""
        result = 'http://b.hatena.ne.jp/test/rss?of=test'
        self.assertEqual(self.obj._make_feed_api_url('test'), result)

if __name__ == '__main__':
    unittest.main()
