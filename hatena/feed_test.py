"""Test of feed.py"""
from datetime import date
import unittest
import feed
from sqlalchemy import create_engine

class TestFeed(unittest.TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        self.obj = feed.Feed(engine, 'test')
        def _create_test_data():
            """Create database for test.

            TODO: Finally I'm thinking to convert ORM function.
            """
            create_sql = """
                         CREATE TABLE `recomend_feed` (
                           `no` INTEGER PRIMARY KEY AUTOINCREMENT,
                           `collect_day` int ( 10 ) NOT NULL,
                           `collect_no` int ( 6 ) NOT NULL,
                           `url` text,
                           `recomend_times` int ( 5 ) DEFAULT 1,
                           `user_no` int ( 10 ),
                           `isAdapt` tinyint DEFAULT 0,
                           `update_time` timestamp
                         );
                """
            insert_sql = """
                INSERT INTO `recomend_feed` (`no`, `collect_day`, `collect_no`, `url`, `user_no`)
                VALUES (1, {}, 1, 'http://test', 1);
                """.format(date.today().strftime("%Y%m%d"))
            c = engine.connect()
            c.execute(create_sql)
            c.execute(insert_sql)
        _create_test_data()
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

    def test__isregistered(self):
        """Test existing target url."""
        self.assertTrue(self.obj._is_register('http://test'))
        self.assertFalse(self.obj._is_register('test2'))

    def test__load_recomend_time(self):
        """Test load recommend times."""
        self.assertEqual(self.obj._load_recommend_time('http://test'), 1)

    def test__update_recomend_time(self):
        """Test update recommend times."""
        self.assertEqual(self.obj._load_recommend_time('http://test'), 1)
        self.obj._update_recomend_time('http://test')
        self.assertEqual(self.obj._load_recommend_time('http://test'), 2)

    def test__append_url(self):
        """Test append recommend url."""
        url = 'http://hoge'
        self.obj._append_url(url, 1, 2)
        self.obj._update_recomend_time(url)
        self.assertEqual(self.obj._load_recommend_time(url), 2)
        self.assertTrue(self.obj._is_register(url))

if __name__ == '__main__':
    unittest.main()
