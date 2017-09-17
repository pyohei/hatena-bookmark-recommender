"""User class."""

import logging
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.sql import select,insert


class User(object):
    """User class."""

    def __init__(self, engine, user):
        logging.basicConfig(level=20)
        self.engine = engine 
        self.md = MetaData(self.engine)
        self.user = user

    @property
    def id(self):
        """Load id."""
        n = self._load_user_no()
        if n:
            #self._update_recommend_time(self.user)
            return n
        return self._append_user()
    no = id

    def _is_register(self, user):
        """Check the user is already registered or not."""
        t = Table('user', self.md)
        w = "name = '{}'".format(user)
        s = select(columns=['name'], from_obj=t).where(w)
        return s.execute().scalar()

    #def _update_recommend_time(self, user):
    #    """Update recommended user count."""
    #    self.md.clear()
    #    t = Table('user', self.md, autoload=True)
    #    w = "name = '{}'".format(user)
    #    u = update(t).where(w).values(recomend_times=t.c.recomend_times+1)
    #    u.execute()
          
    def _append_user(self):
        """Add new recommend user."""
        self.md.clear()
        t = Table('user', self.md, autoload=True)
        i = insert(t).values(name=self.user)
        i.execute()
        # TODO: Change logic.
        return self._load_user_no()

    def _load_user_no(self):
        """Load user_no."""
        self.md.clear()
        t = Table('user', self.md, autoload=True)
        w = "name = '{}'".format(self.user)
        s = select(columns=['id'], from_obj=t).where(w)
        r = s.execute().fetchone()
        if r:
            return r['id']
        return None
