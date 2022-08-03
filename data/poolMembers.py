import os
from datetime import datetime

import psycopg2
import psycopg2.extras

from singleton import Singleton


class PoolMembers(metaclass=Singleton):
    def __init__(self):
        pass

    def __setitem__(self, account_pool: tuple, data):
        pass

    def __getitem__(self, account_pool: tuple):
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

    def is_member(self, account_id: int, pool_id: int) -> bool:
        with self.con:
            with self.con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    """SELECT * FROM poolMembers WHERE account = %s AND pool = %s;""",
                    (account_id, pool_id),
                )
                return cur.fetchone() is not None

    def is_admin(self, account_id: int, pool_id: int) -> bool:
        with self.con:
            with self.con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    """SELECT admin FROM poolMembers WHERE account = %s AND pool = %s;""",
                    (account_id, pool_id),
                )
                res = cur.fetchone()
                return res["admin"] if res is not None else False

    def count(self, pool_id: int) -> int:
        with self.con:
            with self.con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    """SELECT COUNT(*) FROM poolMembers WHERE pool = %s;""", (pool_id,)
                )
                return cur.fetchone()["count"]

    def get_meta(self, account_id: int, pool_id: int) -> tuple:
        with self.con:
            with self.con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    """SELECT * FROM poolMembers WHERE account = %s AND pool = %s;""",
                    (account_id, pool_id),
                )
                res = cur.fetchone()
                is_member = res is not None

                cur.execute(
                    """SELECT COUNT(*) FROM poolMembers WHERE pool = %s;""", (pool_id,)
                )
                count = cur.fetchone()["count"]
                return is_member, res["admin"] if is_member else False, count

    def append(self, account: int, pool: int, admin: bool = False):
        with self.con:
            with self.con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                # Check if there is an admin already
                cur.execute(
                    """SELECT admin FROM poolMembers WHERE pool = %s;""", (pool,)
                )
                res = cur.fetchone()
                has_admin = res is not None and res["admin"]
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
                            admin if has_admin else True,
                            datetime.now(),
                        ),
                    )
                    return cur.fetchone()
                except psycopg2.IntegrityError:
                    return None

    def remove_from(self, account: int, pool: int):
        with self.con:
            with self.con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    """DELETE FROM poolMembers WHERE account = %s AND pool = %s RETURNING *;""",
                    (account, pool),
                )
                return cur.fetchone()

    def check_db(self):
        self.con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        with self.con:
            with self.con.cursor() as cur:
                # cur.execute("drop table if exists poolMembers CASCADE;")
                cur.execute(
                    """CREATE TABLE IF NOT EXISTS poolMembers (
                    account INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
                    pool INTEGER REFERENCES pools(id) ON DELETE CASCADE,
                    admin BOOLEAN DEFAULT FALSE,
                    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT unique_account_pool UNIQUE (account, pool),
                    PRIMARY KEY (account, pool)
                );"""
                )

    def close_connection(self):
        print("closing pool_members")
        self.con.commit()
        self.con.close()
        print("pool_members closed")


POOL_MEMBERS = PoolMembers()
