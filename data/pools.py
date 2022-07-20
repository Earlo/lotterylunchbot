import os
from singleton import Singleton

import psycopg2
import psycopg2.extras


class Pools(metaclass=Singleton):
    def __init__(self):
        self.check_db()

    def __setitem__(self, i, data):
        pass

    def __getitem__(self, i):
        pass

    def __iter__(self):
        pass

    def __contains__(self, item):
        pass

    def __len__(self):
        pass

    def __delitem__(self, key):
        pass

    def __repr__(self) -> str:
        return str(list(self.__iter__()))

    def public_pools(self):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""SELECT * FROM pools WHERE public = TRUE;""")
                return cur.fetchall()

    def check_db(self):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor() as cur:
                cur.execute(
                    """CREATE TABLE IF NOT EXISTS pools (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    public BOOLEAN NOT NULL DEFAULT FALSE,
                    owner INTEGER REFERENCES users(id),
                    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT unique_pool_id UNIQUE (id),
                    CONSTRAINT unique_pool_name UNIQUE (name)
                );"""
                )
