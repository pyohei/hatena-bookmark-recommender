#!/usr/local/bin/python
# -*- coding: utf-8 -*-

""" Feed 

"""

import urllib2
import feedparser
from datetime import date

HATENA_FEED_URL =  "http://b.hatena.ne.jp/user/rss?of="
HATENA_ENTRY_URL = "http://b.hatena.ne.jp/entry/jsonlite/"
ACCESS_INTERVAL = 0.5
START_FEED_ID = 0
#LAST_FEED_ID = 200
LAST_FEED_ID = 20
FEED_INTERVAL = 20

class Feed:

    def __init__(self, engine, user):
        self.engine = engine
        self.opener = urllib2.build_opener()
        self.interval = ACCESS_INTERVAL
        # set user name
        # user name on conf had better set in main module
        # or make new define like 'set_hatenaid'
        self.user = user

    def load(self):
        print "User: %s " % (self.user)
        urls = []
        # num = 0
        start = START_FEED_ID
        end = LAST_FEED_ID
        interval = FEED_INTERVAL

        for i in range(start, end, interval):
            print "Feed no: From %s To %s" % (i, i+interval)
            url = self._make_url(i)
            try:
                response = self.opener.open(url)
            except:
                continue
            feed = self._parse_feed(response)
            if not feed["entries"]:
                break
            urls += self._process_entry(feed)
            try:
                import time
                #time.sleep(self.interval)
                time.sleep(1)
                print("....")
            except:
                pass
        return urls

    def _make_url(self, id):
        u = HATENA_FEED_URL.replace("user", self.user)
        return u + str(id)

    def _parse_feed(self, response):
        c = response.read()
        p = feedparser.parse(c)
        return p

    def _process_entry(self, feed):
        l = []
        for f in feed["entries"]:
            link = f["link"]
            l.append(link)
        return l

    def save(self, urls, user_no):
        #f = open("./long_urls.txt", "a")
        collect_no = 1
        for url in urls:
            if self._is_long_url(url):
                print('Url exceeds 255')
                #f.write("%s\n" % (url))
                continue
            print(url)
            #is_register = self.__is_register(url)
            #if is_register:
            #    self.__update_recomend_time(url)
            #    continue
            self.__append_url(url, user_no, collect_no)
            collect_no += 1
        #f.close()
    
    # change database setting
    def _is_long_url(self, url):
        l = len(url)
        if l > 255:
            return True
        return False

    def __is_register(self, user):
        sql = ("select * "
                "from recomend_feed "
                "where url = '%s' "
                " and  collect_day = '%s' ;"% (
                    user,
                    date.today().strftime("%Y%m%d"))
                )
        records = self.conn.fetchRecords(sql)
        if records:
            return True
        return False

    def __update_recomend_time(self, url):
        sql =  ("update recomend_feed "
                "set recomend_times = recomend_times + 1 "
                "where url = '%s' ;" % (
                    url))
        self.conn.updateRecords(sql)

    def __append_url(self, url, user_no, c_no):
        #sql =  ("insert into recomend_feed( "
        #        "  url, collect_day, collect_no, user_no) "
        #        "values ('%s', '%s', '%s', '%s'); " % (
        #            url,
        #            date.today().strftime("%Y%m%d"),
        #            c_no,
        #            user_no)
        #        )
        #from sqlalchemy.orm import sessionmaker
        from sqlalchemy import MetaData
        from sqlalchemy import Table
        md = MetaData(self.engine)
        table = Table('recomend_feed', md, autoload=True)
        v = table.insert().values(url=url,
                                  collect_day=date.today().strftime("%Y%m%d"),
                                  collect_no=c_no,
                                  user_no=user_no)
        #print(str(upd))
        c = self.engine.connect()
        result = c.execute(v)
        print(result)
        #self.engine.insertRecord(sql)
