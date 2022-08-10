import os
from datetime import datetime

import psycopg
from psycopg.rows import dict_row

from data.schedules import TIMES
from singleton import Singleton


class PoolMembers(metaclass=Singleton):

    member_calendar_sql = """SELECT 
                                accounts.username, 
                                poolMembers.account, 
                                poolMembers.pool,
                                pools.name as pool_name,
                                calendar
                            FROM poolMembers 
                                JOIN schedules ON poolMembers.account = schedules.account
                                JOIN accounts ON poolMembers.account = accounts.id
                                JOIN pools ON poolMembers.pool = pools.id
                            WHERE accounts.disqualified = FALSE
                            """
    calendar_comparisions = [
        f"person_a.calendar[{{}}][{ti + 1}] AND person_b.calendar[{{}}][{ti + 1}]"
        for ti, t in enumerate(TIMES)
    ]

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

    def get_pairs(self, day: int) -> list:
        # the string_to_array(concat_ws is pretty disgusting
        # But it works.
        # TODO figure out how to do 2D array OR in postgres
        query = f"""SELECT 
                    person_a.account as a_account, person_a.username as a_username,
                    person_b.account as b_account, person_b.username as b_username,
                    person_a.pool, person_a.pool_name,
                    string_to_array(concat_ws(',' ,
                        {', '.join([comparison.format(day, day) for comparison in self.calendar_comparisions])}
                    ),',') as calendar_match
                FROM 
                    ({self.member_calendar_sql}) AS person_a
                JOIN
                    ({self.member_calendar_sql}) AS person_b
                ON person_a.account != person_b.account
                AND person_a.account > person_b.account
                AND person_a.pool = person_b.pool
                AND (
                    {' OR '.join([comparison.format(day, day) for comparison in self.calendar_comparisions])}
                )
            """
        with self.con.cursor(row_factory=dict_row) as cur:
            return cur.execute(query).fetchall()

    def is_member(self, account_id: int, pool_id: int) -> bool:
        with self.con.cursor(row_factory=dict_row) as cur:
            return (
                cur.execute(
                    """SELECT * FROM poolMembers WHERE account = %s AND pool = %s;""",
                    (account_id, pool_id),
                ).fetchone()
                is not None
            )

    def is_admin(self, account_id: int, pool_id: int) -> bool:
        with self.con.cursor(row_factory=dict_row) as cur:
            res = cur.execute(
                """SELECT admin FROM poolMembers WHERE account = %s AND pool = %s;""",
                (account_id, pool_id),
            ).fetchone()
            return res["admin"] if res is not None else False

    def count(self, pool_id: int) -> int:
        with self.con.cursor(row_factory=dict_row) as cur:
            return cur.execute(
                """SELECT COUNT(*) FROM poolMembers WHERE pool = %s;""", (pool_id,)
            ).fetchone()["count"]

    def get_meta(self, account_id: int, pool_id: int) -> tuple:
        with self.con.cursor(row_factory=dict_row) as cur:
            res = cur.execute(
                """SELECT * FROM poolMembers WHERE account = %s AND pool = %s;""",
                (account_id, pool_id),
            ).fetchone()
            is_member = res is not None
            count = cur.execute(
                """SELECT COUNT(*) FROM poolMembers WHERE pool = %s;""", (pool_id,)
            ).fetchone()["count"]
            return is_member, res["admin"] if is_member else False, count

    def append(self, account: int, pool: int, admin: bool = False):
        # Check if there is an admin already
        with self.con.cursor(row_factory=dict_row) as cur:
            res = cur.execute(
                """SELECT admin FROM poolMembers WHERE pool = %s;""", (pool,)
            ).fetchone()
            has_admin = res is not None and res["admin"]
            try:
                query = f"""INSERT INTO poolMembers (
                    account,
                    pool,
                    admin,
                    created
                    ) VALUES (%s, %s, %s, %s) 
                    RETURNING *;"""
                return cur.execute(
                    query,
                    (
                        account,
                        pool,
                        admin if has_admin else True,
                        datetime.now(),
                    ),
                ).fetchone()
            except psycopg.IntegrityError:
                return None

    def remove_from(self, account: int, pool: int):
        with self.con.cursor(row_factory=dict_row) as cur:
            return cur.execute(
                """DELETE FROM poolMembers WHERE account = %s AND pool = %s RETURNING *;""",
                (account, pool),
            ).fetchone()

    def check_db(self):
        self.con = psycopg.connect(os.environ.get("DATABASE_URL"))
        # self.con.execute("drop table if exists poolMembers CASCADE;")
        self.con.execute(
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
