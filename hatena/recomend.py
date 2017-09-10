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
