"""My Bookmark class"""

import logging
from hatena.bookmark import Bookmark
from sqlalchemy import Table
from sqlalchemy.sql import select,insert,column


class MyBookmark(Bookmark):
    """My bookmark class.

    Tish class is inherited from Bookmark class.
    """
    def __init__(self, engine, user):
        self._new_feeds = []
        super(MyBookmark, self).__init__(engine, user)

    def register(self, url):
        """Register bookmark feeds."""
        if self._has_record(url):
            return
        self._register(url)

    @property
    def new_feeds(self):
        return self._new_feeds

    def save(self):
        """Save bookmark as my bookmark."""
        logging.info('SAVE MY BOOKMARK')
        for f in self.feeds:
            logging.info(f.url)
            if self._has_record(f.id):
                logging.info('IGNORE')
                continue
            logging.info('ADD')
            self._register(f.id)
            self._new_feeds.append(f)
        logging.info('----------------------')

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
