"""My Bookmark class"""

from hatena.bookmark import Bookmark
from sqlalchemy import Table
from sqlalchemy.sql import select,insert,column


class MyBookmark(Bookmark):

    def register(self, url):
        """Register bookmark urls."""
        if self._has_record(url):
            return
        self._register(url)

    def save(self):
        self._load()
        for u in self.urls:
            if self._has_record(u.url):
                print("Existing!.")
                continue
            print("Register!.")
            self._register(u.url)
            # Append

    def _register(self, bookmark):
        """Register bookmark url."""
        self.md.clear()
        t = Table('my_bookmarks', self.md, autoload=True)
        i = insert(t).values(url=bookmark)
        i.execute()

    def _has_record(self, bookmark):
        """Check bookmark url is already existing."""
        t = Table('my_bookmarks', self.md)
        c_url = column('url')
        s = select(columns=[column('no')], from_obj=t).where(c_url==bookmark)
        return s.execute().scalar()
