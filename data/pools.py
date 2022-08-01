import os

from datetime import datetime
from singleton import Singleton

import psycopg2
import psycopg2.extras


class Pools(metaclass=Singleton):
    def __init__(self):
        pass

    def __setitem__(self, pool_id: int, data):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor() as cur:
                query = f"""INSERT INTO pools (
                    id,
                    name,
                    description,
                    public,
                    created_at
                    ) VALUES (%s, %s, %s, %s, %s) 
                    ON CONFLICT (id) DO UPDATE SET name = %s, description = %s, public = %s, updated_at = %s
                    RETURNING *;
                    """
                cur.execute(
                    query,
                    (
                        pool_id,
                        data["name"],
                        data["description"],
                        data["public"],
                        datetime.now(),
                        data["name"],
                        data["description"],
                        data["public"],
                        datetime.now(),
                    ),
                )
                return cur.fetchone()

    def append(self, data):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                query = f"""INSERT INTO pools (
                    name,
                    description,
                    public,
                    created_at
                    ) VALUES (%s, %s, %s, %s) 
                    RETURNING *;"""
                cur.execute(
                    query,
                    (
                        data["name"],
                        data["description"],
                        data["public"],
                        datetime.now(),
                    ),
                )
                return cur.fetchone()

    def __getitem__(self, pool_id: int):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""SELECT * FROM pools WHERE id = %s;""", (pool_id,))
                return cur.fetchone()

    def get_by_name(self, name: str):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""SELECT * FROM pools WHERE name ILIKE %s;""", (name,))
                return cur.fetchone()

    def __iter__(self):
        pass

    def __contains__(self, item):
        pass

    def __len__(self):
        pass

    def __delitem__(self, pool_id: int):
        # TODO: make check that this method is only called by an admin
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor() as cur:
                cur.execute(
                    """DELETE FROM pools WHERE id = %s
                    RETURNING *;""",
                    (pool_id,),
                )
                return cur.fetchone()

    def __repr__(self) -> str:
        return str(list(self.__iter__()))

    def update(self, pool_id: int, field: str, value):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor() as cur:
                cur.execute(
                    f"""UPDATE pools SET {field} = {value} WHERE id = {pool_id}
                    RETURNING *;""",
                )
                return cur.fetchone()

    def public_pools(self):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""SELECT * FROM pools WHERE public = TRUE;""")
                return cur.fetchall()

    def pools_in(self, account_id: int):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:

                cur.execute(
                    """SELECT public, name, member_count
                    FROM (
                        SELECT pool, count(account) AS member_count
                        FROM poolMembers
                        GROUP BY pool
                        ) AS members
                    JOIN poolMembers ON members.pool = poolMembers.pool AND poolMembers.account = %s
                    JOIN pools on poolMembers.pool = pools.id;""",
                    (account_id,),
                )
                return cur.fetchall()

    def check_db(self):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor() as cur:
                # cur.execute("drop table if exists pools CASCADE;")
                cur.execute(
                    """CREATE TABLE IF NOT EXISTS pools (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description VARCHAR(255),
                    public BOOLEAN NOT NULL DEFAULT FALSE,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT unique_pool_id UNIQUE (id),
                    CONSTRAINT unique_pool_name UNIQUE (name)
                );"""
                )


POOLS = Pools()
