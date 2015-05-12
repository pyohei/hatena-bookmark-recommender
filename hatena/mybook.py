#!/usr/local/bin/python
# -*- coding: utf-8 -*-

""" My bookmark class 

"""


class Mybook(object):

    def __init__(self, conn):
        self.conn = conn

    def register(self, bookmarks):
        for b in bookmarks:
            if self.__has_record(b):
                continue
            self.__register(b)

    def __register(self, bookmark):
        sql = (
            "INSERT INTO my_bookmarks( "
            "  url) "
            "VALUES ('%s');" % (
                bookmark)
            )
        self.conn.insertRecord(sql)

    def __has_record(self, bookmark):
        sql = (
            "SELECT * "
            "FROM my_bookmarks "
            "WHERE url = '%s'; " % (
                bookmark)
            )
        records = self.conn.fetchRecords(sql)
        if records:
            return True
        return False

    def select_urls(self, is_all=False):
        sql = (
            "SELECT * "
            "FROM my_bookmarks "
            "WHERE invalid = 0 "
            )
        if not is_all:
            sql += "and is_search = 0 "
        sql += "; "
        recs = self.conn.fetchRecords(sql)
        return [ r["url"] for r in recs if "url" in r]
