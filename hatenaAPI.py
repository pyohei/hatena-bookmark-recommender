#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""handler of hatena api

This module can collect recomend urls of specify hatena user.
"""

import urllib2
import conf
import feedparser
import json
import time
from dbConnector import DbConnector
import sys
from datetime import date

HATENA_FEED_URL =  "http://b.hatena.ne.jp/user/rss?of="
HATENA_ENTRY_URL = "http://b.hatena.ne.jp/entry/jsonlite/"

_CONNECTION = None
COLLECT_NO = 1

def main():

    # Get my feed infomation.
    print "--- start ---"
    f = Feed()
    urls = f.load()
    print urls
    tt = open("./bookmarks.txt", "w")
    tt.write("\n".join(urls))
    tt.close()

    # Gather users reading my feed.
    print "Explore Bookmark users"
    b = BookmarkUser(urls)
    users = b.extract()
    b.save(users)

    # Load feed data of my reading feed users
    for user in users:
        user_no = b.load_user_no(user)
        if not user_no:
            continue
        recFeed = Feed(user)    # this constract is so vain...
        urls = recFeed.load()
        recFeed.save(urls, user_no)
        time.sleep(0.5)
    print "--- end ---"

def _connectDb():
    global _CONNECTION
    if _CONNECTION:
        return _CONNECTION
    _CONNECTION= DbConnector(conf.CONNECTION)
    return _CONNECTION

class Feed:

    def __init__(self, user=""):
        self.opener = urllib2.build_opener()
        self.interval = conf.ACCESS_INTERVAL
        # set user name
        # user name on conf had better set in main module
        # or make new define like 'set_hatenaid'
        if user:
            self.user = user
        else:
            self.user = conf.HATENA_ID
        # set sleep time
        try:
            if self.interval > 0:
                import time
        except:
            pass

    def load(self):
        print "User: %s " % (self.user)
        urls = []
        # num = 0
        start = conf.START_FEED_ID
        end = conf.LAST_FEED_ID
        interval = conf.FEED_INTERVAL

        for i in range(start, end, interval):
            print "Feed no: From %s To %s" % (i, i+interval)
            url = self.__make_url(i)
            try:
                response = self.opener.open(url)
            except:
                continue
            feed = self.__parse_feed(response)
            if not feed["entries"]:
                break
            urls += self.__process_entry(feed)
            try:
                # time.sleep(self.interval)
                time.sleep(0.05)
            except:
                pass
        return urls

    def __make_url(self, id):
        u = HATENA_FEED_URL.replace("user", self.user)
        return u + str(id)

    def __parse_feed(self, response):
        c = response.read()
        p = feedparser.parse(c)
        return p

    def __process_entry(self, feed):
        l = []
        for f in feed["entries"]:
            link = f["link"]
            l.append(link)
        return l

    def save(self, urls, user_no):
        global COLLECT_NO
        #f = open("./long_urls.txt", "a")
        collect_no = 1
        for url in urls:
            #if self.__is_long_url(url):
            #    f.write("%s¥n" % (url))
            #    continue
            is_register = self.__is_register(url)
            if is_register:
                self.__update_recomend_time(url)
                continue
            self.__append_url(url, user_no)
            COLLECT_NO += 1
        #f.close()
    
    # change database setting
    def __is_long_url(self, url):
        l = len(url)
        if l > 255:
            return True
        return False

    def __is_register(self, user):
        conn = _connectDb()
        sql = ("select * "
                "from recomend_feed "
                "where url = '%s' "
                " and  collect_day = '%s' ;"% (
                    user,
                    date.today().strftime("%Y%m%d"))
                )
        records = conn.fetchRecords(sql)
        if records:
            return True
        return False

    def __update_recomend_time(self, url):
        conn = _connectDb()
        sql =  ("update recomend_feed "
                "set recomend_times = recomend_times + 1 "
                "where url = '%s' ;" % (
                    url))
        conn.updateRecords(sql)

    def __append_url(self, url, user_no):
        conn = _connectDb()
        sql =  ("insert into recomend_feed( "
                "  url, collect_day, collect_no, user_no) "
                "values ('%s', '%s', '%s', '%s'); " % (
                    url,
                    date.today().strftime("%Y%m%d"),
                    COLLECT_NO,
                    user_no)
                )
        conn.insertRecord(sql)
        #sys.exit(0)

class BookmarkUser:

    def __init__(self, urls):
        # call twice, so in vain
        self.opener = urllib2.build_opener()
        self.urls = urls
        self.interval = conf.ACCESS_INTERVAL

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
        conn = _connectDb()
        sql = ("select * "
                "from users "
                "where user_name = '%s'; " % (
                    user)
                )
        records = conn.fetchRecords(sql)
        if records:
            return True
        return False

    def __update_recomend_time(self, user):
        conn = _connectDb()
        sql =  ("update users "
                "set recomend_times = recomend_times + 1 "
                "where user_name = '%s' ;" % (
                    user))
        conn.updateRecords(sql)

    def __append_user(self, user):
        conn = _connectDb()
        sql =  ("insert into users( "
                "  user_name, register_datetime) "
                "values ('%s', '%s'); " % (
                    user,
                    date.today().strftime("%Y%m%d"))
                )
        conn.insertRecord(sql)
        #sys.exit(0)

    def load_user_no(self, user):
        conn = _connectDb()
        sql =  ("select user_no "
                "from users "
                "where user_name = '%s' ;" % (
                    user)
                )
        records = conn.fetchRecords(sql)
        if len(records) > 1:
            raise
        if not records:
            return None
        record = records[0]
        return record["user_no"]

if __name__ == "__main__":
    main()
