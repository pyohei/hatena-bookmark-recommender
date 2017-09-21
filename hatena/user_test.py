import unittest
import user
from sqlalchemy import create_engine
from sqlalchemy.sql import text

class TestUser(unittest.TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        # TODO: Delete?
        import logging
        logging.basicConfig(level=0, format='%(asctime)s, %(filename)s, %(funcName)s, %(message)s')
        self.obj = user.User(engine, 'hoge')
        def _create_test_data():
            """Create database for test."""
            create_sql = """
            CREATE TABLE `user` (
              `id`   INTEGER PRIMARY KEY AUTOINCREMENT,
              `name` TEXT UNIQUE
            );
            """
            insert_sql = text("INSERT INTO `user` (`name`) VALUES ('test');")
            c = engine.connect()
            c.execute(create_sql)
            c.execute(insert_sql)
        _create_test_data()

    def test__append_user(self):
        """Test append user."""
        self.obj._append_user()
        self.assertTrue(self.obj._load_user_no())

    def test__load_user_no(self):
        self.obj.name = 'test'
        self.assertEqual(self.obj._load_user_no(), 1)
        self.obj.name = 'hoge'
        self.obj._append_user()
        self.assertEqual(self.obj._load_user_no(), 2)
        self.obj.name = 'bar'
        self.assertEqual(self.obj._load_user_no(), None)

    def test_id(self):
        self.obj.name = 'test'
        self.assertEqual(self.obj.id, 1)
        

if __name__ == '__main__':
    unittest.main()
