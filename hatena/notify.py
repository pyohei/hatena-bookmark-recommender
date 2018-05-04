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

    def add_as_notified(self, url_id):
        self.md.clear()
        md = MetaData(self.engine)
        t = Table('notification', md, autoload=True)
        i = insert(t).values(url_id=url_id, 
                             notified_date=datetime.now().strftime('%Y%m%d'))
        i.execute()
