"""Feed test"""
import unittest
import feed
from sqlalchemy import create_engine

class TestFeed(unittest.TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        self.target_url = 'http://www.hatena.ne.jp/'
        self.obj = feed.Feed(engine, self.target_url)
        def _create_test_data():
            """Create database for test.

            TODO: Finally I'm thinking to convert ORM function.
            """
            create_sql = """
                CREATE TABLE `feed` (
                  `id`    INTEGER PRIMARY KEY AUTOINCREMENT,
                  `url`   TEXT UNIQUE,
                  `title` TEXT
                );
             """
            insert_sql = """
                INSERT INTO `feed` (`url`, `title`)
                  VALUES ('http://test', 'test');
                """
            c = engine.connect()
            c.execute(create_sql)
            c.execute(insert_sql)
        _create_test_data()

    def test__make_entry_api_url(self):
        """Test code of _make_url"""
        result = 'http://b.hatena.ne.jp/entry/jsonlite/?url=http%3A%2F%2Fwww.hatena.ne.jp%2F'
        self.assertEqual(self.obj._make_entry_api_url(self.target_url), result)

    def test__request(self):
        """Test request"""
        # Same with result of `test__make_entry_api_url`
        url = 'http://b.hatena.ne.jp/entry/jsonlite/?url=http%3A%2F%2Fwww.hatena.ne.jp%2F'
        r = self.obj._request(url)
        self.assertIsInstance(r, dict)
    
    def test_extract(self):
        """Test extract user data
        
        This result is `User` instance.
        """
        # TODO: increase test case.
        # Success
        self.assertIsInstance(self.obj.extract()[0].name, unicode)
        # failure
        self.obj.url = 'http://www.hatena.aaaa.aaa'
        self.assertEqual(self.obj.extract(), [])

    def test__load_id(self):
        self.assertEqual(self.obj._load_id(), None)
        self.obj.url = 'http://test'
        self.assertEqual(self.obj._load_id(), 1)
    
    def test__append(self):
        self.obj.url = 'http://foobar'
        self.obj._append()
        self.assertEqual(self.obj._load_id(), 2)

    def test_id(self):
        self.assertEqual(self.obj.id, 2)
        self.obj.url = 'http://test'
        self.assertEqual(self.obj.id, 1)

if __name__ == '__main__':
    unittest.main()
