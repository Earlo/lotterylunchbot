import os
import psycopg2
import psycopg2.extras

from datetime import datetime
from singleton import Singleton


class PoolMembers(metaclass=Singleton):
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

    def append(self, account: int, pool: int, admin: bool = False):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                try:
                    query = f"""INSERT INTO poolMembers (
                        account,
                        pool,
                        admin,
                        created
                        ) VALUES (%s, %s, %s, %s) 
                        RETURNING *;"""
                    cur.execute(
                        query,
                        (
                            account,
                            pool,
                            admin,
                            datetime.now(),
                        ),
                    )
                    return cur.fetchone()
                except psycopg2.IntegrityError:
                    return None

    def check_db(self):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor() as cur:
                # cur.execute("drop table if exists accountsPools CASCADE;")
                cur.execute(
                    """CREATE TABLE IF NOT EXISTS poolMembers (
                    account INTEGER REFERENCES accounts(id),
                    pool INTEGER REFERENCES pools(id),
                    admin BOOLEAN DEFAULT FALSE,
                    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT unique_account_pool UNIQUE (account, pool),
                    PRIMARY KEY (account, pool)
                );"""
                )


POOL_MEMBERS = PoolMembers()
