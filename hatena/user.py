"""User class."""

import logging
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.sql import select,insert, column


class User(object):
    """User class."""

    def __init__(self, engine, name):
        logging.basicConfig(level=20, format='%(asctime)s, %(filename)s, %(funcName)s, %(message)s')
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

    def _append_user(self):
        """Add new recommend user."""
        self.md.clear()
        t = Table('user', self.md, autoload=True)
        i = insert(t).values(name=self.name)
        i.execute()
        logging.info('Add!!!!!!')
        # TODO: Change logic.
        return self._load_user_no()

    def _load_user_no(self):
        """Load user_no."""
        self.md.clear()
        logging.info('LOAD!!!!!!')
        t = Table('user', self.md, autoload=True)
        c_name = column('name')
        s = select(columns=[column('id')], 
                   from_obj=t).where(c_name==self.name)
        r = s.execute().fetchone()
        if r:
            return r['id']
        return None
