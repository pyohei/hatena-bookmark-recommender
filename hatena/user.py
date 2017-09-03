"""User

"""

import urllib
import time
from datetime import date
import requests
#from sqlalchemy import MetaData
#from sqlalchemy import Table

HATENA_ENTRY_URL = "http://b.hatena.ne.jp/entry/jsonlite/?url={url}"
ACCESS_INTERVAL = 0.5

class User:

    def __init__(self, engine, urls):
        # call twice, so in vain
        self.engine = engine 
        self.urls = urls
        self.interval = ACCESS_INTERVAL

    def extract(self):
        print "BookmarkUser extract"
        users = []
        for feedurl in self.urls:
            print "target url: %s" % (feedurl)
            url = self._make_entry_api_url(feedurl)
            f = self._request(url)
            # Don't examine patterns not "bookamark" keys
            print(f)
            if "bookmarks" not in f:
                continue
            for bookmark in f["bookmarks"]:
                #users.append([url[0], bookmark["user"]])
                if "user" not in bookmark:
                    continue
                users.append(bookmark["user"])
            #time.sleep(self.interval)
            time.sleep(1)
            ### TEST
            break
        return users

    def _make_entry_api_url(self, url):
        """Create hatena bookmark entry api url."""
        e_url = urllib.quote(url, safe='')
        return HATENA_ENTRY_URL.format(url=e_url)

    def _request(self, url):
        """Request api.
        
        Request argument url and return result data as dict.
        """
        #return self.opener.open(url)
        #r = self.opener.open(url)
        return requests.get(url).json()

    def save(self, users):
        for user in users:
            is_register = self.__is_register(user)
            print('{} -- {}'.format(user, str(is_register)))
            if is_register:
                self._update_recomend_time(user)
                continue
            self._append_user(user)

    def __is_register(self, user):
        sql = ("select * "
                "from users "
                "where user_name = '%s'; " % (
                    user)
                )
        c = self.engine.connect()
        print('hi')
        recs = c.execute(sql)
        #records = self.conn.fetchRecords(sql)
        print '----->'
        print recs
        # TODO: Fix
        for r in recs:
            return True
        return False

    def _update_recomend_time(self, user):
        sql =  ("update users "
                "set recomend_times = recomend_times + 1 "
                "where user_name = '%s' ;" % (
                    user))
        print('hi2')
        c = self.engine.connect()
        c.execute(sql)

    def _append_user(self, user):
        sql =  ("insert into users( "
                "  user_name, register_datetime) "
                "values ('%s', '%s'); " % (
                    user,
                    date.today().strftime("%Y%m%d"))
                )
        print(sql)
        c = self.engine.connect()
        c.execute(sql)
        

    def load_user_no(self, user):
        sql =  ("select user_no "
                "from users "
                "where user_name = '%s' ;" % (
                    user)
                )
        c = self.engine.connect()
        recs = c.execute(sql)
        #if len(recs) > 1:
        #    raise
        for r in recs:
            return r["user_no"]
        return None
