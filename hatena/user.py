"""User class."""

import logging
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.sql import select,insert, column


class User(object):
    """User class."""

    def __init__(self, engine, name):
        self.engine = engine 
        self.md = MetaData(self.engine)
        self.name = name

    @property
    def id(self):
        """Load id."""
        logging.debug('Fetch id')
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
        # TODO: Change logic.
        _id = self._load_user_no()
        logging.info('Add new user(id={}, name={}).'.format(_id, self.name))
        return _id

    def _load_user_no(self):
        """Load user_no."""
        self.md.clear()
        t = Table('user', self.md, autoload=True)
        c_name = column('name')
        s = select(columns=[column('id')], 
                   from_obj=t).where(c_name==self.name)
        r = s.execute().fetchone()
        _id = None
        if r:
            _id = r['id']
        logging.info('Load user id(name={}, id={}).'.format(self.name, _id))
        return _id
