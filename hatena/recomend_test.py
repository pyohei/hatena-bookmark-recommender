"""Test of `recommend.py`"""
from datetime import date
import unittest
import recomend
from sqlalchemy import create_engine

class TestRecommend(unittest.TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        self.obj = recomend.Recommend(engine)
        def _create_test_data():
            """Create database for test. """
            r_create_sql = """
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
            r_insert_sql = """
                INSERT INTO `recomend_feed` 
                  (`collect_day`, `collect_no`, `url`, `user_no`)
                  VALUES ({}, 1, 'http://test', 1),
                         ({}, 1, 'http://test2', 1)
                ;
                """.format(date.today().strftime("%Y%m%d"),
                           date.today().strftime("%Y%m%d"))
            b_create_sql = """
                CREATE TABLE `my_bookmarks` (
                  `no` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                  `url` text,
                  `is_search` tinyint DEFAULT 0,
                  `invalid` tinyint DEFAULT 0,
                  `update_time` timestamp
                );
                """
            b_insert_sql = """
                INSERT INTO `my_bookmarks` (url)
                  VALUES ('http://test');
                """
            c = engine.connect()
            c.execute(r_create_sql)
            c.execute(r_insert_sql)
            c.execute(b_create_sql)
            c.execute(b_insert_sql)
        _create_test_data()

    def test__load_top(self):
        # Case: fech one url.
        r1 = self.obj._load_top(1)
        self.assertEqual(len(r1.fetchall()), 1)
        # Case: fech two(all) url.
        r2 = self.obj._load_top(2)
        self.assertEqual(len(r2.fetchall()), 2)
        # Case: check url is correct.
        r3 = self.obj._load_top(1)
        self.assertEqual(r3.fetchone()[3], u'http://test')

    def test__is_mybookmark(self):
        self.assertTrue(self.obj._is_mybookmark('http://test'))

    def test_select(self):
        pass

if __name__ == '__main__':
    unittest.main()
