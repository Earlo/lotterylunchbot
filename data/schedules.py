import os
from singleton import Singleton

import psycopg2
import psycopg2.extras


class Schedules(metaclass=Singleton):
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
                    """CREATE TABLE IF NOT EXISTS schedules (
                    owner INTEGER REFERENCES users(id),
                    pool INTEGER REFERENCES pools(id),
                    weekday VARCHAR(8),
                    start_time TIME NOT NULL,
                    end_time TIME NOT NULL,
                    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (owner, pool)
                );"""
                )
