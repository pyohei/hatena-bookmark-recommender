"""Bookmark operation class."""

from datetime import date
import logging
import time
import feedparser
import requests
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.sql import insert, column, select

from .feed import Feed

HATENA_FEED_URL =  "http://b.hatena.ne.jp/{user}/rss?of={no}"

class Bookmark(object):

    def __init__(self, engine, user, start_no=0, end_no=100):
        self.engine = engine
        self.md = MetaData(self.engine)
        self.user = user
        self._feeds = []
        self.start_no = 0
        self.end_no = 100

    @property
    def feeds(self):
        """Return feed data."""
        if not self._feeds:
            self._load()
        return self._feeds

    def _load(self):
        """Load feed info."""
        interval = 20 # API default setting.

        for i in range(self.start_no,
                       self.end_no,
                       interval):
            url = self._make_feed_api_url(i)
            feed = self._request(url)
            if not feed["entries"]:
                break
            self._append_to_feeds(feed)
            time.sleep(2)

    def _make_feed_api_url(self, id):
        """Create api url of rss feed."""
        return HATENA_FEED_URL.format(user=self.user.name, no=str(id))

    def _request(self, url):
        """Request api.
        
        Request argument url and return result data as feedparser object..
        """
        return feedparser.parse(requests.get(url).text)

    def _append_to_feeds(self, feed):
        """Parse and append feed data."""
        for f in feed["entries"]:
            link = f["link"]
            title = f['title']
            self._feeds.append(Feed(self.engine, link, title))

    def save(self):
        """Save url."""
        if not self._feeds:
            self._load()
        # TODO: Load user no
        logging.info('SAVE BOOKMARK')
        for f in self._feeds:
            logging.info(f.url)
            if self._has_record(f.id):
                # TODO:
                #   Fix to use return if not existing new feed.
                #   To escape duplicate access.   
                logging.info('IGNORE')
                continue
            logging.info('ADD')
            self._register(f.id)
        logging.info('----------------------')
    
    def _register(self, url_id):
        """Register bookmark transaction."""
        self.md.clear()
        md = MetaData(self.engine)
        t = Table('bookmark', md, autoload=True)
        i = insert(t).values(url_id=url_id,
                             user_id=self.user.id,
                             registered_date=int(
                                 date.today().strftime("%Y%m%d")))
        i.execute()

    def _has_record(self, url_id):
        """Check bookmark url is already existing."""
        t = Table('bookmark', self.md)
        c_user = column('user_id')
        c_url = column('url_id')
        s = select(columns=[column('id')], from_obj=t).where(
                c_url==url_id).where(c_user==self.user.id)
        return s.execute().scalar()
