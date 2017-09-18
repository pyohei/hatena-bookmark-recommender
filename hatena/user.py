"""User class."""

import logging
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.sql import select,insert, column


class User(object):
    """User class."""

    def __init__(self, engine, name):
        logging.basicConfig(level=20)
        self.engine = engine 
        self.md = MetaData(self.engine)
        self.name = name

    @property
    def id(self):
        """Load id."""
        logging.info(self.name)
        n = self._load_user_no()
        if n:
            return n
        return self._append_user()

    def _is_register(self, name):
        """Check the user is already registered or not."""
        t = Table('user', self.md)
        c_name = column('name')
        s = select(columns=['name'], from_obj=t).where(c_name==name)
        return s.execute().scalar()

    def _append_user(self):
        """Add new recommend user."""
        self.md.clear()
        t = Table('user', self.md, autoload=True)
        i = insert(t).values(name=self.name)
        i.execute()
        # TODO: Change logic.
        return self._load_user_no()

    def _load_user_no(self):
        """Load user_no."""
        self.md.clear()
        t = Table('user', self.md, autoload=True)
        c_name = column('name')
        s = select(columns=[column('id')], from_obj=t).where(c_name==self.name)
        r = s.execute().fetchone()
        if r:
            return r['id']
        return None
