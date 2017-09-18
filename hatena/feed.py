"""Feed operation class"""

import logging
import urllib
import time
from user import User
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.sql import select, column, insert

import requests

HATENA_ENTRY_URL = "http://b.hatena.ne.jp/entry/jsonlite/?url={url}"

class Feed(object):
    """Bookmark user class."""

    def __init__(self, engine, url, title=''):
        logging.basicConfig(level=20)
        self.engine = engine 
        self.url = url
        self.title = title
        self.md = MetaData(self.engine)
        self.sleep_sec = 1

    @property
    def id(self):
        """Load feed id."""
        if not self._load_id():
            self._append()
        return self._load_id()

    def extract(self):
        """Extract bookmarked users from setted url."""
        users = []

        # TODO: Load id in __init__
        if not self._load_id():
            self._append()
        api_url = self._make_entry_api_url(self.url)
        result = self._request(api_url)
        if not result:
            return users
        for b in result.get('bookmarks', []):
            if "user" not in b:
                continue
            users.append(User(self.engine, b["user"]))
        time.sleep(self.sleep_sec)
        return users

    def _make_entry_api_url(self, url):
        """Create hatena bookmark entry api url."""
        e_url = urllib.quote(url, safe='')
        return HATENA_ENTRY_URL.format(url=e_url)

    def _request(self, url):
        """Request api.
        
        Request argument url and return result data as dict.
        """
        return requests.get(url).json()

    def _load_id(self):
        """Load feed id from database."""
        t = Table('feed', self.md)
        c_url = column('url')
        c_id = column('id')
        s = select(columns=[c_id], from_obj=t).where(c_url==self.url)
        r = s.execute().fetchone()
        if r:
            return r['id']
        return None

    def _append(self):
        """Add new feed url into database."""
        logging.info('SAVE MY FEED')
        logging.info(self.url)
        self.md.clear()
        md = MetaData(self.engine)
        t = Table('feed', md, autoload=True)
        i = insert(t).values(url=self.url,
                             title=self.title)
        i.execute()
        logging.info('----------------------')
