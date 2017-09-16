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
from sqlalchemy.sql import select, update

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
        logging.info('User: {}'.format(self.user))
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
        return HATENA_FEED_URL.format(user=self.user, no=str(id))

    def _request(self, url):
        """Request api.
        
        Request argument url and return result data as feedparser object..
        """
        return feedparser.parse(requests.get(url).text)

    def _process_entry(self, feed):
        l = []
        for f in feed["entries"]:
            link = f["link"]
            #l.append(link)
            l.append(Feed(self.engine, link))
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
            user_no = 0
            collect_no = 1
            for url in self.urls:
                if self._is_long_url(url.url):
                    logging.info("Url exceeds 255{}.".format(url.url))
                    continue
                is_register = self._is_register(url.url)
                if is_register:
                    self._update_recommend_time(url.url)
                    continue
                self._append_url(url.url, user_no, collect_no)
                collect_no += 1
    
    def _is_long_url(self, url):
        """Check the url is over database column setting."""
        return len(url) > 255

    def _load_recommend_time(self, url):
        """Load recommend time."""
        self.md.clear()
        t = Table('recomend_feed', self.md, auto_load=True)
        w = "url = '{}'".format(url)
        s = select(columns=['recomend_times'], from_obj=t).where(w)
        return s.execute().fetchone()['recomend_times']

    def _is_register(self, url):
        """Check the url is already registered in the same day."""
        t = Table('recomend_feed', self.md)
        w = "url = '{}' and collect_day = '{}' ".format(
            url, int(date.today().strftime("%Y%m%d")))
        s = select(columns=['no'], from_obj=t).where(w)
        return s.execute().scalar()

    def _update_recommend_time(self, url):
        """Update recommended user count."""
        self.md.clear()
        t = Table('recomend_feed', self.md, autoload=True)
        w = "url = '{}'".format(url)
        u = update(t).where(w).values(recomend_times=t.c.recomend_times+1)
        u.execute()

    def _append_url(self, url, user_no, c_no):
        """Append new url."""
        self.md.clear()
        md = MetaData(self.engine)
        table = Table('recomend_feed', md, autoload=True)
        v = table.insert().values(url=url,
                                  collect_day=int(date.today().strftime("%Y%m%d")),
                                  collect_no=c_no,
                                  user_no=user_no)
        c = self.engine.connect()
        c.execute(v)
