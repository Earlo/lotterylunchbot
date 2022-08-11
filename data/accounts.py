import os
from datetime import datetime
from random import shuffle

import psycopg
from psycopg.rows import dict_row

from data.schedules import SCHEDULES
from singleton import Singleton


class Accounts(metaclass=Singleton):
    def __init__(self):
        self.con = psycopg.connect(os.environ.get("DATABASE_URL"), autocommit=True)

    def create_account(self, account_id: int, data):
        with self.con.cursor() as cur:
            query = f"""INSERT INTO accounts (
                id,
                username,
                first_name,
                last_name,
                joined
                ) VALUES (%s, %s, %s, %s, %s) 
                ON CONFLICT (id) DO UPDATE SET username = %s, first_name = %s, last_name = %s
                RETURNING id"""

            self.con.execute(
                query,
                (
                    account_id,
                    data["username"],
                    data["first_name"],
                    data["last_name"],
                    datetime.now(),
                    data["username"],
                    data["first_name"],
                    data["last_name"],
                ),
            )

            SCHEDULES.create_schedule_query(cur, account_id)

    def __getitem__(self, account_id: int):
        with self.con.cursor(row_factory=dict_row) as cur:
            return cur.execute(
                """SELECT * FROM accounts WHERE id = %s""", (account_id,)
            ).fetchone()

    def __iter__(self):
        with self.con.cursor(row_factory=dict_row) as cur:
            for account in cur.execute(
                """SELECT id
                FROM accounts
                ORDER BY joined DESC
                """
            ).fetchall():
                yield account[0]

    def __contains__(self, item):
        return (
            self.con.execute(
                """SELECT * FROM accounts WHERE id = %s""", (item,)
            ).fetchone()
            is not None
        )

    def __len__(self):
        return self.con.execute("""SELECT COUNT(*) FROM accounts""").fetchone()

    def __delitem__(self, key):
        self.con.execute("""DELETE FROM accounts WHERE id = %s""", (key,))

    def __repr__(self) -> str:
        return str(list(self.__iter__()))

    def set_disqualified(self, account_id: int, disqualified: bool):
        self.con.execute(
            """UPDATE accounts SET disqualified = %s WHERE id = %s""",
            (disqualified, account_id),
        )

    def get_qualified(self):
        with self.con.cursor(row_factory=dict_row) as cur:
            res = cur.execute(
                """SELECT id FROM accounts WHERE disqualified = FALSE"""
            ).fetchall()
            return [x[0] for x in res]

    def reset(self):
        self.disqualified_accounts = set()

    def save(self):
        pass

    def check_db(self):
        self.con.execute(
            """CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            joined TIMESTAMP,
            disqualified BOOLEAN DEFAULT FALSE,
            CONSTRAINT unique_id UNIQUE (id),
            CONSTRAINT unique_username UNIQUE (username)
            );"""
        )

    def close_connection(self):
        print("closing accounts")
        self.con.commit()
        self.con.close()
        print("accounts closed")


ACCOUNTS = Accounts()
