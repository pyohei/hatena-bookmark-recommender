"""Bookmark operation class."""

from datetime import date
import logging
import time

import feedparser
import requests
from feed import Feed
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.sql import insert, column, select

HATENA_FEED_URL =  "http://b.hatena.ne.jp/{user}/rss?of={no}"
# TODO: Change these parameters into argument.
START_FEED_ID = 0
#LAST_FEED_ID = 200
LAST_FEED_ID = 20

class Bookmark(object):

    def __init__(self, engine, user):
        self.engine = engine
        self.md = MetaData(self.engine)
        self.interval = 0.5
        self.user = user
        self._feeds = []

    @property
    def feeds(self):
        """Return feed data."""
        if not self._feeds:
            self._load()
        return self._feeds

    def _load(self):
        """Load feed info."""
        interval = 20 # API default setting.
        # User logging
        logging.info('User: {}, {}'.format(self.user.id, self.user.name))
        feeds = []
        start = START_FEED_ID
        end = LAST_FEED_ID

        for i in range(start, end, interval):
            # Feed list logging
            logging.info('Feed {} - {}'.format(i, i+interval))
            url = self._make_feed_api_url(i)
            feed = self._request(url)
            if not feed["entries"]:
                break
            feeds += self._process_entry(feed)
            time.sleep(self.interval)
        self._feeds = feeds

    def _make_feed_api_url(self, id):
        """Create api url of rss feed."""
        return HATENA_FEED_URL.format(user=self.user.name, no=str(id))

    def _request(self, url):
        """Request api.
        
        Request argument url and return result data as feedparser object..
        """
        return feedparser.parse(requests.get(url).text)

    def _process_entry(self, feed):
        l = []
        # Discontinue loop
        for f in feed["entries"]:
            link = f["link"]
            title = f['title']
            l.append(Feed(self.engine, link, title))
        return l

    def save(self):
        """Save url."""
        # TODO: Create test code.
        if not self._feeds:
            self._load()
        # TODO: Load user no
        for f in self._feeds:
            if not self._has_record(f.id):
                logging.info('*****************************')
                continue
            logging.info('++++++++++++++++++++++++++')
            self._register(f.id)
    
    def _register(self, url_id):
        """Register bookmark transaction."""
        logging.info('-----')
        logging.info(self.user.id)
        logging.info(url_id)
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
