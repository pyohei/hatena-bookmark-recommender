import unittest
import user
from sqlalchemy import create_engine

class TestUser(unittest.TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        self.target_url = 'http://www.hatena.ne.jp/'
        self.obj = user.User(engine, ['http://www.test'])

    def test__make_entry_api_url(self):
        """Test code of _make_url"""
        result = 'http://b.hatena.ne.jp/entry/jsonlite/?url=http%3A%2F%2Fwww.hatena.ne.jp%2F'
        self.assertEqual(self.obj._make_entry_api_url(self.target_url), result)

    def test__request(self):
        """Test request"""
        # Same with result of `test__make_entry_api_url`
        url = 'http://b.hatena.ne.jp/entry/jsonlite/?url=http%3A%2F%2Fwww.hatena.ne.jp%2F'
        r = self.obj._request(url)
        self.assertIsInstance(r.json(), dict)

if __name__ == '__main__':
    unittest.main()
