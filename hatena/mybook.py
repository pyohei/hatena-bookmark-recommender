"""My bookmark class 

"""


class Mybook(object):

    def __init__(self, engine):
        self.engine = engine

    def register(self, bookmarks):
        for b in bookmarks:
            if self._has_record(b):
                continue
            self._register(b)

    def _register(self, bookmark):
        sql = (
            "INSERT INTO my_bookmarks( "
            "  url) "
            "VALUES ('%s');" % (
                bookmark)
            )
        c = self.engine.connect()
        c.execute(sql)

    def _has_record(self, bookmark):
        sql = (
            "SELECT * "
            "FROM my_bookmarks "
            "WHERE url = '%s'; " % (
                bookmark)
            )
        c = self.engine.connect()
        records = c.execute(sql)
        for r in records:
            return True
        return False
