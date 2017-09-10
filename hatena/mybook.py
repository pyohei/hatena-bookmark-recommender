"""My Bookmark class"""

from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.sql import select,insert


class Mybook(object):

    def __init__(self, engine):
        self.engine = engine
        self.md = MetaData(self.engine)

    def register(self, bookmarks):
        for b in bookmarks:
            if self._has_record(b):
                continue
            self._register(b)

    def _register(self, bookmark):
        sql = (
            "INSERT INTO my_bookmarks( "
            "  url) "
            "VALUES ('%s');" % (
                bookmark)
            )
        c = self.engine.connect()
        c.execute(sql)

    def _has_record(self, bookmark):
        """Check bookmark url is already existing."""
        t = Table('my_bookmarks', self.md)
        w = "url = '{}'".format(bookmark)
        s = select(columns=['no'], from_obj=t).where(w)
        return s.execute().scalar()
