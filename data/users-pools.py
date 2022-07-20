import os
from singleton import Singleton

import psycopg2
import psycopg2.extras


class UsersPools(metaclass=Singleton):
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

    def check_db(self):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor() as cur:
                cur.execute(
                    """CREATE TABLE IF NOT EXISTS userspools (
                    user INTEGER REFERENCES users(id),
                    pool INTEGER REFERENCES pools(id),
                    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT unique_user_pool UNIQUE (user, pool),
                    PRIMARY KEY (user, pool),
                );"""
                )
