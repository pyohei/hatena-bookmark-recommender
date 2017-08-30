#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""handler of hatena api

This module can collect recomend urls of specify hatena user.
"""

import time
#from hatena.mybook import Mybook
from hatena.feed import Feed
from hatena.user import User
from hatena.recomend import Recommend
from sqlalchemy import create_engine


COLLECT_NO = 1
ENGINE = 'sqlite:///hatena.db'

def main(user):
    engine = create_engine(ENGINE)

    print "--- start ---"
    f = Feed(engine, user)
    urls = f.load()
    print(urls)
    f.save(urls, 1)

    #mb = Mybook(_connectDb())
    #mb.register(urls)

    #if not is_all:
    #    urls = mb.select_urls(is_all=False)
    #else:
    #    urls = mb.select_urls()
    print "success!"
    # Gather users reading my feed.
    print "Explore Bookmark users"
    print "--- Finish ---"
    b = User(engine, urls)
    users = b.extract()
    b.save(users)
    print "--- Finish ---"

    # Load feed data of my reading feed users
    for user in users:
        user_no = b.load_user_no(user)
        if not user_no:
            continue
        recFeed = Feed(engine, user)
        urls = recFeed.load()
        recFeed.save(urls, user_no)
        time.sleep(1)
        break
    r = Recommend(engine)
    recs = r.select()
    for r in recs:
        print(r)
    print "--- end ---"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', required=True, help='User name')
    args = parser.parse_args()
    main(args.user)

