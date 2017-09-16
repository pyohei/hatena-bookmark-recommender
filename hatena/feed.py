"""Feed operation class"""

import logging
import urllib
import time
from user import User
#from datetime import date
from sqlalchemy import MetaData
#from sqlalchemy import Table
#from sqlalchemy.sql import select,update,insert
import requests

HATENA_ENTRY_URL = "http://b.hatena.ne.jp/entry/jsonlite/?url={url}"

class Feed(object):
    """Bookmark user class."""

    def __init__(self, engine, urls):
        logging.basicConfig(level=20)
        self.engine = engine 
        self.urls = [urls]
        self.url = urls
        self.md = MetaData(self.engine)
        self.sleep_sec = 1

    def extract(self):
        """Extract bookmarked users from setted url."""
        users = []
        for feedurl in self.urls:
            logging.info('URL:{}'.format(feedurl))
            api_url = self._make_entry_api_url(feedurl)
            result = self._request(api_url)
            if not result:
                continue
            for b in result.get('bookmarks', []):
                if "user" not in b:
                    continue
                # TODO: Ignore myself.
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
