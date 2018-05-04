# coding: utf-8
"""Notification recommend feed."""

import requests
import os
from datetime import datetime
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.sql import insert

class Notification(object):

    def __init__(self, engine):
        self.engine = engine 
        self.md = MetaData(self.engine)

    def send_line(self, rec):
        # rec is tuple of `(title, url, id)`
        body = rec[0] + '\n' + rec[1]
        params = {"value1": body}
        url = os.environ.get('HATENA_FEED_NOTIFICATION_URL', '')
        r = requests.post(url, params)
        print r
        self._set_as_notified(int(rec[2]))

    def _set_as_notified(self, url_id):
        self.md.clear()
        md = MetaData(self.engine)
        t = Table('notification', md, autoload=True)
        i = insert(t).values(url_id=url_id, 
                             notified_date=datetime.now().strftime('%Y%m%d'))
        i.execute()

def main():
    """Send message with Line"""
    params = {"value1": "{}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}
    url = os.environ.get('HATENA_FEED_NOTIFICATION_URL', '')
    r = requests.post(url, params)
    print(r)

def test():
    from sqlalchemy import create_engine
    ENGINE = 'sqlite:///hatena.db'
    engine = create_engine(ENGINE)
    n = Notification(engine)
    n._set_as_notified(1)

if __name__ == '__main__':
    test()
