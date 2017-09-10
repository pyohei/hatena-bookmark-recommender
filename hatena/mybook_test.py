"""Test of mybook."""
import unittest
import mybook
from sqlalchemy import create_engine

class TestMyBook(unittest.TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        self.obj = mybook.Mybook(engine)
        def _create_test_data():
            """Create database for test."""
            create_sql = """
                CREATE TABLE `my_bookmarks` (
                  `no` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                  `url` text,
                  `is_search` tinyint DEFAULT 0,
                  `invalid` tinyint DEFAULT 0,
                  `update_time` timestamp
                );
                """
            insert_sql = """
                INSERT INTO `my_bookmarks` (url)
                  VALUES ('http://test');
                """
            c = engine.connect()
            c.execute(create_sql)
            c.execute(insert_sql)
        _create_test_data()

    def test__has_record(self):
        self.assertTrue(self.obj._has_record('http://test'))
        self.assertFalse(self.obj._has_record('http://TEST'))

    def test__register(self):
        self.obj._register("http://TEST")
        self.assertTrue(self.obj._has_record('http://TEST'))
    
    def test_register(self):
        urls = ['http://hoge', 'http://foo']
        self.obj.register(urls)
        for u in urls:
            self.assertTrue(self.obj._has_record(u))

if __name__ == '__main__':
    unittest.main()
