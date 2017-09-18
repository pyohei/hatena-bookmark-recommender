"""My Bookmark class"""

from hatena.bookmark import Bookmark
from sqlalchemy import Table
from sqlalchemy.sql import select,insert,column


class MyBookmark(Bookmark):

    def register(self, url):
        """Register bookmark feeds."""
        if self._has_record(url):
            return
        self._register(url)

    def save(self):
        """Save bookmark as my bookmark."""
        for f in self.feeds:
            if self._has_record(f.id):
                continue
            self._register(f.id)

    def _register(self, url_id):
        """Register bookmark url."""
        self.md.clear()
        t = Table('my_bookmark', self.md, autoload=True)
        i = insert(t).values(url_id=url_id)
        i.execute()

    def _has_record(self, url_id):
        """Check bookmark url is already existing."""
        t = Table('my_bookmark', self.md)
        c_url = column('url_id')
        s = select(columns=[column('id')], from_obj=t).where(c_url==url_id)
        return s.execute().scalar()
