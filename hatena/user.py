#!/usr/local/bin/python
# -*- coding: utf-8 -*-

""" User

"""

import urllib2
import time
import json

HATENA_FEED_URL =  "http://b.hatena.ne.jp/user/rss?of="
HATENA_ENTRY_URL = "http://b.hatena.ne.jp/entry/jsonlite/"
ACCESS_INTERVAL = 0.5

class User:

    def __init__(self, conn, urls):
        # call twice, so in vain
        self.conn = conn
        self.opener = urllib2.build_opener()
        self.urls = urls
        self.interval = ACCESS_INTERVAL

    def extract(self):
        print "BookmarkUser extract"
        users = []
        for feedurl in self.urls:
            print "target url: %s" % (feedurl)
            url = self.__make_url(feedurl)
            response = self.opener.open(url)
            f = self.__parse(response)
            # Don't examine patterns not "bookamark" keys
            if "bookmarks" not in f:
                continue
            for bookmark in f["bookmarks"]:
                #users.append([url[0], bookmark["user"]])
                if "user" not in bookmark:
                    continue
                users.append(bookmark["user"])
            time.sleep(self.interval)
        return users

    def __make_url(self, target):
        return HATENA_ENTRY_URL + target

    def __parse(self, response):
        c = response.read()
        return json.loads(c)

    def save(self, users):
        for user in users:
            is_register = self.__is_register(user)
            if is_register:
                self.__update_recomend_time(user)
                continue
            self.__append_user(user)

    def __is_register(self, user):
        sql = ("select * "
                "from users "
                "where user_name = '%s'; " % (
                    user)
                )
        records = self.conn.fetchRecords(sql)
        if records:
            return True
        return False

    def __update_recomend_time(self, user):
        sql =  ("update users "
                "set recomend_times = recomend_times + 1 "
                "where user_name = '%s' ;" % (
                    user))
        self.conn.updateRecords(sql)

    def __append_user(self, user):
        sql =  ("insert into users( "
                "  user_name, register_datetime) "
                "values ('%s', '%s'); " % (
                    user,
                    date.today().strftime("%Y%m%d"))
                )
        self.conn.insertRecord(sql)
        #sys.exit(0)

    def load_user_no(self, user):
        sql =  ("select user_no "
                "from users "
                "where user_name = '%s' ;" % (
                    user)
                )
        records = self.conn.fetchRecords(sql)
        if len(records) > 1:
            raise
        if not records:
            return None
        record = records[0]
        return record["user_no"]
