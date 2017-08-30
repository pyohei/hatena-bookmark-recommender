# -*- coding: utf-8 -*-

""" Recommend Selector

Select recommend data from database

"""


class Recommend(object):

    def __init__(self, engine):
        self.engine = engine

    def select(self):
        rank_urls = []
        recs = self.__load_top()
        for rec in recs:
            #if self._is_mybookmark(rec["url"]):
            #    print "oooooooooooppppppps"
            #    continue
            rank_urls.append(rec["url"])
        return rank_urls

    def __load_top(self, num=100):
        sql = ("SELECT * "
            "FROM recomend_feed "
            "ORDER BY recomend_times "
            "LIMIT %s " % num )
        c = self.engine.connect()
        return c.execute(sql)

    def _is_mybookmark(self, url):
        sql = ("SELECT * "
            "FROM my_bookmarks "
            "WHERE url = '%s'; " % (url))
        c = self.engine.connect()
        return c.execute(sql)

if __name__ == "__main__":
    # --- Path settings ---- "
    from os import path
    FULL_PATH = path.dirname(path.abspath(__file__))
    PYTHONPATH = "/".join(FULL_PATH.split("/")[:-1])
    import sys
    sys.path.append(PYTHONPATH)
    # --- ----- --- #
    from lib.dbConnector import DbConnector
    import conf
    CONNECTION = DbConnector(conf.CONNECTION)
    r = Recommend(CONNECTION)
    us = r.select()
    for n, u in enumerate(us):
        print n+1, u
