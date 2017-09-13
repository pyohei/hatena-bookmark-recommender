"""Recommend url handle class."""
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.sql import select

class Recommend(object):

    def __init__(self, engine):
        self.engine = engine
        self.md = MetaData(self.engine)

    def select(self):
        rank_urls = []
        recs = self._load_top()
        for rec in recs:
            if self._is_mybookmark(rec["url"]):
                print(rec['url'])
                continue
            rank_urls.append(rec["url"])
        return rank_urls

    def _load_top(self, num=100):
        """Load top recommend url"""
        self.md.clear()
        t = Table('recomend_feed', self.md)
        s = select(columns=['*'], 
                   from_obj=t).order_by('recomend_times').limit(num)
        return s.execute()

    def _is_mybookmark(self, url):
        """Check the url is already registered as my bookmark."""
        self.md.clear()
        t = Table('my_bookmarks', self.md)
        w = "url = '{}'".format(url)
        s = select(columns=['url'], from_obj=t).where(w)
        return s.execute().scalar()
