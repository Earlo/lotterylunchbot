from datetime import datetime
from random import shuffle
import os
from singleton import Singleton

import psycopg2
import psycopg2.extras


class Users(metaclass=Singleton):
    def __init__(self):
        self.check_db()

    def __setitem__(self, i, data):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor() as cur:
                query = f"""INSERT INTO users (
                    id,
                    username,
                    first_name,
                    last_name,
                    joined
                    ) VALUES (%s, %s, %s, %s, %s)
                    """
                cur.execute(query, (data['id'], data['username'],
                                    data['first_name'], data['last_name'], datetime.now()))

    def __getitem__(self, i):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""SELECT * FROM users WHERE id = %s""", (i,))
                return cur.fetchone()

    def __iter__(self):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    """SELECT *
                    FROM users
                    ORDER BY joined DESC
                    """
                )
                for user in cur.fetchall():
                    print("usrs", user)
                    yield user

    def __contains__(self, item):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""SELECT * FROM users WHERE id = %s""", (item,))
                return cur.fetchone() is not None

    def __len__(self):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""SELECT COUNT(*) FROM users""")
                return cur.fetchone()[0]

    def __delitem__(self, key):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""DELETE FROM users WHERE id = %s""", (key,))

    def get_qualified(self):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    """SELECT id FROM users WHERE disqualified = FALSE""")
                return [x[0] for x in cur.fetchall()]

    def get_pairs(self):
        rngkeys = self.get_qualified()
        shuffle(rngkeys)
        if (len(rngkeys) % 2 == 1):
            rngkeys.append(None)
        pairs = [[rngkeys[x*2], rngkeys[x*2+1]]
                 for x in range(len(rngkeys)//2)]
        print("pairs", pairs)
        return pairs

    def reset(self):
        self.disqualified_users = set()

    def save(self):
        pass

    def check_db(self):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor() as cur:
                cur.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    username TEXT,
                    joined TIMESTAMP,
                    disqualified BOOLEAN DEFAULT FALSE,
                    CONSTRAINT unique_id UNIQUE (id),
                    CONSTRAINT unique_username UNIQUE (username)
                );""")

    def __repr__(self) -> str:
        return str(list(self.__iter__()))
