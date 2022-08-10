import os
from datetime import datetime

import psycopg
from psycopg.rows import dict_row

from singleton import Singleton, run_and_get


class Pools(metaclass=Singleton):
    def __init__(self):
        pass

    def __setitem__(self, pool_id: int, data):
        with self.con.cursor(row_factory=dict_row) as cur:
            return cur.execute(
                """INSERT INTO pools (
                id,
                name,
                description,
                public,
                created_at
                ) VALUES (%s, %s, %s, %s, %s) 
                ON CONFLICT (id) DO UPDATE SET name = %s, description = %s, public = %s, updated_at = %s
                RETURNING *;
                """,
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
            ).fetchone()

    def append(self, data):
        with self.con.cursor(row_factory=dict_row) as cur:
            return cur.execute(
                """INSERT INTO pools (
                    name,
                    description,
                    public,
                    created_at
                ) VALUES (%s, %s, %s, %s) 
                RETURNING *;""",
                (
                    data["name"],
                    data["description"],
                    data["public"],
                    datetime.now(),
                ),
            ).fetchone()

    def __getitem__(self, pool_id: int):
        with self.con.cursor(row_factory=dict_row) as cur:
            return cur.execute(
                """SELECT * FROM pools WHERE id = %s;""", (pool_id,)
            ).fetchone()

    def get_by_name(self, name: str):
        with self.con.cursor(row_factory=dict_row) as cur:
            return cur.execute(
                """SELECT * FROM pools WHERE name ILIKE %s;""", (name,)
            ).fetchone()

    def __iter__(self):
        pass

    def __contains__(self, item):
        pass

    def __len__(self):
        pass

    def __delitem__(self, pool_id: int):
        # TODO: make check that this method is only called by an admin
        with self.con.cursor(row_factory=dict_row) as cur:
            return cur.execute(
                """DELETE FROM pools WHERE id = %s
                RETURNING *;""",
                (pool_id,),
            ).fetchone()

    def __repr__(self) -> str:
        return str(list(self.__iter__()))

    def update(self, pool_id: int, field: str, value):
        with self.con.cursor(row_factory=dict_row) as cur:
            return cur.execute(
                f"""UPDATE pools SET {field} = {value} WHERE id = {pool_id}
                RETURNING *;""",
            ).fetchone()

    def public_pools(self):
        with self.con.cursor(row_factory=dict_row) as cur:
            return cur.execute(
                """SELECT * FROM pools WHERE public = TRUE;"""
            ).fetchall()

    def availeable_pools(self, account_id: int):
        with self.con.cursor(row_factory=dict_row) as cur:
            return cur.execute(
                """SELECT * FROM pools WHERE public = TRUE OR id IN (
                    SELECT pool FROM poolMembers WHERE account = %s
                );""",
                (account_id,),
            ).fetchall()

    def pools_of(self, account_id: int):
        with self.con.cursor(row_factory=dict_row) as cur:
            return cur.execute(
                """SELECT * FROM pools WHERE id IN (
                    SELECT pool FROM poolMembers WHERE account = %s
                );""",
                (account_id,),
            ).fetchall()

    def pools_in(self, account_id: int):
        with self.con.cursor(row_factory=dict_row) as cur:
            return cur.execute(
                """SELECT public, name, member_count
                FROM (
                    SELECT pool, count(account) AS member_count
                    FROM poolMembers
                    GROUP BY pool
                    ) AS members
                JOIN poolMembers ON members.pool = poolMembers.pool AND poolMembers.account = %s
                JOIN pools on poolMembers.pool = pools.id;""",
                (account_id,),
            ).fetchall()

    def check_db(self):
        self.con = psycopg.connect(os.environ.get("DATABASE_URL"))
        print("self.con", self.con)
        # self.con.execute("drop table if exists pools CASCADE;")
        self.con.execute(
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

    def close_connection(self):
        print("closing pools")
        self.con.commit()
        self.con.close()
        print("pools closed")


POOLS = Pools()
