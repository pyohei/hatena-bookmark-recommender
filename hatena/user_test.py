import unittest
import user
from sqlalchemy import create_engine

class TestUser(unittest.TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        self.target_url = 'http://www.hatena.ne.jp/'
        self.obj = user.User(engine, ['http://www.test'])
        def _create_test_data():
            """Create database for test.

            TODO: Finally I'm thinking to convert ORM function.
            """
            create_sql = """
                CREATE TABLE `users` (
                  `user_no` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                  `user_name` TEXT NOT NULL,
                  `recomend_times` INTEGER NOT NULL DEFAULT 1,
                  `register_datetime` datetime,
                  `update_time` timestamp
                  );
                """
            insert_sql = """
                INSERT INTO `users` (`user_name`, `recomend_times`, `register_datetime`)
                VALUES ('test', 1, '2017-01-01 00:00:00');
                """
            c = engine.connect()
            c.execute(create_sql)
            c.execute(insert_sql)
        def _count_recommend_times():
            sql = """
                SELECT recomend_times as cnt FROM users WHERE user_name = 'test'
                """
            c = engine.connect()
            r = c.execute(sql)
            return r.fetchone()['cnt']
        _create_test_data()
        self.count_recommend_times = _count_recommend_times

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
    
    def test__isregistered(self):
        """Test existing target user."""
        self.assertTrue(self.obj._is_register('test'))
        self.assertFalse(self.obj._is_register('test2'))

    def test__update_recommend_times(self):
        """Test existing target user."""
        self.assertEqual(self.count_recommend_times(), 1)
        self.obj._update_recommend_time('test')
        self.assertEqual(self.count_recommend_times(), 2)

if __name__ == '__main__':
    unittest.main()