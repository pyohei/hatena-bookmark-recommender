"""Test of bookmark.py"""
from datetime import date
import unittest
import bookmark
from sqlalchemy import create_engine

class TestBookmark(unittest.TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        # User class mock.
        u = UserMock()
        u.id = 1
        u.name = 'test'
        self.obj = bookmark.Bookmark(engine, u)
        def _create_test_data():
            """Create database for test.

            TODO: Finally I'm thinking to convert ORM function.
            """
            create_sql = """
                CREATE TABLE `bookmark` (
                `id`              INTEGER PRIMARY KEY AUTOINCREMENT,
                `url_id`          INTEGER,
                `user_id`         INTEGER,
                `registered_date` INTEGER
                );
            """
            insert_sql = """
                INSERT INTO `bookmark` 
                    (`url_id`, `user_id`, `registered_date`)
                  VALUES (1, 1, {});
            """.format(int(date.today().strftime("%Y%m%d")))
            c = engine.connect()
            c.execute(create_sql)
            c.execute(insert_sql)
        _create_test_data()
        self.response = None

    def test__make_feed_api_url(self):
        """Test code of _make_url"""
        result = 'http://b.hatena.ne.jp/test/rss?of=20'
        self.assertEqual(self.obj._make_feed_api_url(20), result)

    def test__request(self):
        """Test request"""
        url = 'http://b.hatena.ne.jp/sample/rss?of=sample'
        r = self.obj._request(url)
        self.assertIsInstance(r, dict)
        self.response = r

    def test_append_to_feeds(self):
        f = {'entries': [{'link': 'http://test1', 'title': 'test1'},
                         {'link': 'http://test2', 'title': 'test2'}]}
        self.obj._append_to_feeds(f)
        self.assertIsInstance(self.obj._feeds, list)

    def test_save(self):
        """Test save function."""
        feeds = []
        for i in range(105, 108):
            f = FeedMock()
            f.id = i
            f.url = 'test{}'.format(str(i))
            feeds.append(f)
        self.obj._feeds = feeds
        self.obj.save()
        for f in feeds:
            self.assertTrue(self.obj._has_record(f.id))

    def test_feeds(self):
        self.assertEqual(self.obj.feeds, [])

    def test__register(self):
        self.obj._register(100)
        self.assertTrue(self.obj._has_record(100))

    def test__has_record(self):
        self.assertTrue(self.obj._has_record(1))

class FeedMock(object):
    """Mock object for Feed."""
    pass

class UserMock(object):
    """Mock object for user."""
    pass

if __name__ == '__main__':
    unittest.main()
