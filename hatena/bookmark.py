"""Bookmark operation class."""

from datetime import date
import logging
import time

import feedparser
import requests
from mybook import Mybook
from feed import Feed
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.sql import insert

HATENA_FEED_URL =  "http://b.hatena.ne.jp/{user}/rss?of={no}"
# TODO: Change these parameters into argument.
START_FEED_ID = 0
#LAST_FEED_ID = 200
LAST_FEED_ID = 20

class Bookmark(object):

    def __init__(self, engine, user, is_base_user=False):
        self.engine = engine
        self.md = MetaData(self.engine)
        self.interval = 0.5
        self.user = user
        self.is_base_user = is_base_user
        self.urls = []

    @property
    def feeds(self):
        if not self.urls:
            self._load()
        return self.urls

    def _load(self):
        """Load feed info."""
        interval = 20 # API default setting.
        logging.info('User: {}, {}'.format(self.user.id, self.user.name))
        feeds = []
        start = START_FEED_ID
        end = LAST_FEED_ID

        for i in range(start, end, interval):
            logging.info('Feed {} - {}'.format(i, i+interval))
            url = self._make_feed_api_url(i)
            feed = self._request(url)
            if not feed["entries"]:
                break
            feeds += self._process_entry(feed)
            time.sleep(self.interval)
        self.urls = feeds

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
        if not self.urls:
            self._load()
        if self.is_base_user:
            for u in self.urls:
                b = Mybook(self.engine)
                b.register(u.url)
        else:
            # TODO: Load user no
            for url in self.urls:
                # will discontinue
                if self._is_long_url(url.url):
                    logging.info("Url exceeds 255{}.".format(url.url))
                    continue
                self._append(url)
    
    def _is_long_url(self, url):
        """Check the url is over database column setting."""
        return len(url) > 255

    def _append(self, url):
        """Append url into bookmark."""
        logging.info('-----')
        logging.info(self.user.id)
        logging.info(url.id)
        self.md.clear()
        md = MetaData(self.engine)
        t = Table('bookmark', md, autoload=True)
        i = insert(t).values(url_id=url.id,
                             user_id=self.user.id,
                             registered_date=int(
                                 date.today().strftime("%Y%m%d")))
        i.execute()
