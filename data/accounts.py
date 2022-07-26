import os
import psycopg2
import psycopg2.extras

from datetime import datetime
from random import shuffle
from singleton import Singleton


class Accounts(metaclass=Singleton):
    def __init__(self):
        pass

    def __setitem__(self, account_id: int, data):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor() as cur:
                query = f"""INSERT INTO accounts (
                    id,
                    username,
                    first_name,
                    last_name,
                    joined
                    ) VALUES (%s, %s, %s, %s, %s) 
                    ON CONFLICT (id) DO UPDATE SET username = %s, first_name = %s, last_name = %s
                    """
                cur.execute(
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

    def __getitem__(self, account_id: int):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""SELECT * FROM accounts WHERE id = %s""", (account_id,))
                return cur.fetchone()

    def __iter__(self):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor() as cur:
                cur.execute(
                    """SELECT id
                    FROM accounts
                    ORDER BY joined DESC
                    """
                )
                for account in cur.fetchall():
                    yield account[0]

    def __contains__(self, item):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""SELECT * FROM accounts WHERE id = %s""", (item,))
                return cur.fetchone() is not None

    def __len__(self):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""SELECT COUNT(*) FROM accounts""")
                return cur.fetchone()[0]

    def __delitem__(self, key):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""DELETE FROM accounts WHERE id = %s""", (key,))

    def __repr__(self) -> str:
        return str(list(self.__iter__()))

    def get_qualified(self):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor() as cur:
                cur.execute("""SELECT id FROM accounts WHERE disqualified = FALSE""")
                return [x[0] for x in cur.fetchall()]

    def get_pairs(self):
        rngkeys = self.get_qualified()
        shuffle(rngkeys)
        if len(rngkeys) % 2 == 1:
            rngkeys.append(None)
        pairs = [[rngkeys[x * 2], rngkeys[x * 2 + 1]] for x in range(len(rngkeys) // 2)]
        return pairs

    def reset(self):
        self.disqualified_accounts = set()

    def save(self):
        pass

    def check_db(self):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor() as cur:
                # cur.execute("drop table if exists accounts cascade")
                cur.execute(
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


ACCOUNTS = Accounts()
