"""My Bookmark class"""

from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.sql import select,insert


class Mybook(object):

    def __init__(self, engine):
        self.engine = engine
        self.md = MetaData(self.engine)

    def register(self, url):
        """Register bookmark urls."""
        if self._has_record(url):
            return
        self._register(url)

    def _register(self, bookmark):
        """Register bookmark url."""
        self.md.clear()
        t = Table('my_bookmarks', self.md, autoload=True)
        i = insert(t).values(url=bookmark)
        i.execute()

    def _has_record(self, bookmark):
        """Check bookmark url is already existing."""
        t = Table('my_bookmarks', self.md)
        w = "url = '{}'".format(bookmark)
        s = select(columns=['no'], from_obj=t).where(w)
        return s.execute().scalar()
