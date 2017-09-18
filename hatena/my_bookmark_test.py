"""Test of mybook."""
import unittest
import my_bookmark
from sqlalchemy import create_engine

class TestMyBook(unittest.TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        u = UserMock()
        u.id = 100
        u.name = 'test'
        self.obj = my_bookmark.MyBookmark(engine, u)
        def _create_test_data():
            """Create database for test."""
            create_sql = """
                CREATE TABLE `my_bookmark` (
                `id`     INTEGER PRIMARY KEY AUTOINCREMENT,
                `url_id` INTEGER UNIQUE
                );
            """
            insert_sql = """
                INSERT INTO `my_bookmark` (url_id)
                  VALUES (1);
                """
            c = engine.connect()
            c.execute(create_sql)
            c.execute(insert_sql)
        _create_test_data()

    def test__has_record(self):
        self.assertTrue(self.obj._has_record(1))
        self.assertFalse(self.obj._has_record(2))

    def test__register(self):
        self.obj._register(2)
        self.assertTrue(self.obj._has_record(2))
    
    def test_save(self):
        self.obj.save()
        self.obj.save()
        self.assertTrue(self.obj._has_record(100))

    def test_new_feeds(self):
        # TODO: Add test code.
        pass

class FeedMock(object):
    """Mock object for Feed."""
    pass

class UserMock(object):
    """Mock object for user."""
    pass

if __name__ == '__main__':
    unittest.main()
