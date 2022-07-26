import os

from datetime import datetime
from singleton import Singleton

import psycopg2
import psycopg2.extras


class Pools(metaclass=Singleton):
    def __init__(self):
        pass

    def __setitem__(self, i: int, data):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor() as cur:
                query = f"""INSERT INTO pools (
                    id,
                    name,
                    description,
                    public,
                    created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s) 
                    ON CONFLICT (id) DO UPDATE SET name = %s, description = %s, public = %s, updated_at = %s
                    """
                cur.execute(
                    query,
                    (
                        i,
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
                con.commit()

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

    def __getitem__(self, i: int):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""SELECT * FROM pools WHERE id = %s;""", (i,))
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

    def __delitem__(self, key):
        pass

    def __repr__(self) -> str:
        return str(list(self.__iter__()))

    def public_pools(self):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""SELECT * FROM pools WHERE public = TRUE;""")
                return cur.fetchall()

    def pools_in(self, account_id: int):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    """SELECT 
                        pools.public, pools.name, count(*) 
                        FROM 
                        pools JOIN accountsPools ON pools.id = accountsPools.pool 
                        WHERE
                        accountsPools.account = %s GROUP BY pools.public, pools.name;""",
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
