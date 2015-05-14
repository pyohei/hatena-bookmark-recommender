#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""handler of hatena api

This module can collect recomend urls of specify hatena user.
"""

import conf
import feedparser
import json
import time
from lib.dbConnector import DbConnector
from hatena.mybook import Mybook
from hatena.feed import Feed
from hatena.user import User
import sys
from datetime import date


_CONNECTION = None
COLLECT_NO = 1

def main(is_all=False):

    # Get my feed infomation.
    conn = _connectDb()
    print "--- start ---"
    f = Feed(conn)
    urls = f.load()
    mb = Mybook(_connectDb())
    #mb.register(urls)

    if not is_all:
        urls = mb.select_urls(is_all=False)
    else:
        urls = mb.select_urls()
    print "success!"
    # Gather users reading my feed.
    print "Explore Bookmark users"
    b = User(conn, urls)
    users = b.extract()
    b.save(users)

    # Load feed data of my reading feed users
    for user in users:
        user_no = b.load_user_no(user)
        if not user_no:
            continue
        recFeed = Feed(conn, user)    # this constract is so vain...
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

if __name__ == "__main__":
    main()

