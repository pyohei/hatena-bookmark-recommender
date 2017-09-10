"""Test of `recommend.py`"""
import unittest
import recomend
from sqlalchemy import create_engine

class TestRecommend(unittest.TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        self.obj = recomend.Recommend(engine)
