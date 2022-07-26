import os
import psycopg2
import psycopg2.extras

from datetime import datetime
from singleton import Singleton


class AccountsPools(metaclass=Singleton):
    def __init__(self):
        pass

    def __setitem__(self, i: int, data):
        pass

    def __getitem__(self, i: int):
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

    def append(self, account_id: int, pool_id: int, admin: bool = False):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                query = f"""INSERT INTO accountsPools (
                    account_id,
                    pool_id,
                    admin,
                    created
                    ) VALUES (%s, %s, %s, %s) 
                    RETURNING *;"""
                cur.execute(
                    query,
                    (
                        account_id,
                        pool_id,
                        admin,
                        datetime.now(),
                    ),
                )
                return cur.fetchone()

    def check_db(self):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor() as cur:
                # cur.execute("drop table if exists accountsPools CASCADE;")
                cur.execute(
                    """CREATE TABLE IF NOT EXISTS accountsPools (
                    account_id INTEGER REFERENCES accounts(id),
                    pool_id INTEGER REFERENCES pools(id),
                    admin BOOLEAN DEFAULT FALSE,
                    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT unique_account_pool UNIQUE (account_id, pool_id),
                    PRIMARY KEY (account_id, pool_id)
                );"""
                )


ACCOUNTS_POOLS = AccountsPools()
