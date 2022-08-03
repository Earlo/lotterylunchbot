import json
import os

import psycopg2
import psycopg2.extensions
import psycopg2.extras

from singleton import Singleton


class Schedules(metaclass=Singleton):
    def __init__(self):
        pass

    def __setitem__(self, schedule_id: int, data):
        pass

    def __getitem__(self, schedule_id: int):
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
        kek = []
        return str(list(self.__iter__()))

    def update_schedule(
        self, account_id: int, calendar: list, pool_id: int | None = None
    ):
        with psycopg2.connect(os.environ["DATABASE_URL"]) as conn:
            with conn.cursor() as cur:
                date_table = json.dumps(calendar).replace("[", "{").replace("]", "}")
                print("inserting", date_table)
                cur.execute(
                    """
                    UPDATE schedules
                    SET calendar = %s
                    WHERE account = %s
                """,
                    (date_table, account_id),
                )

    def create_schedule(self, account_id: int, pool_id: int | None = None):
        with psycopg2.connect(os.environ["DATABASE_URL"]) as conn:
            with conn.cursor() as cur:
                self.create_schedule_query(cur, account_id, pool_id)

    def create_schedule_query(
        self,
        cur: psycopg2.extensions.cursor,
        account_id: int,
        pool_id: int | None = None,
    ):
        cur.execute(
            "INSERT INTO schedules (account, pool) VALUES (%s, %s)",
            (account_id, pool_id),
        )

    def get_schedule(self, user_id: int) -> dict:
        with psycopg2.connect(os.environ["DATABASE_URL"]) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(
                    "SELECT calendar FROM schedules WHERE account = %s",
                    (user_id,),
                )
                return cur.fetchone()

    def check_db(self):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor() as cur:
                # cur.execute("drop table if exists schedules;")
                date_table = (
                    json.dumps(
                        [[False for _ in range(len(TIMES))] for _ in range(len(DAYS))]
                    )
                    .replace("[", "{")
                    .replace("]", "}")
                )
                cur.execute(
                    f"""CREATE TABLE IF NOT EXISTS schedules (
                    id SERIAL PRIMARY KEY,
                    account INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
                    pool INTEGER REFERENCES pools(id) ON DELETE CASCADE,
                    calendar BOOLEAN[{len(DAYS)}][{len(TIMES)}] NOT NULL DEFAULT '{date_table}'::BOOLEAN[{len(DAYS)}][{len(TIMES)}],
                    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                );"""
                )


SCHEDULES = Schedules()
DAYS = [
    "Mo",
    "Tu",
    "We",
    "Th",
    "Fr",
    "Sa",
    "Su",
]
TIMES = [
    "11:00",
    "12:00",
    "13:00",
    "14:00",
]

END_TIMES = [
    "11:00",
    "12:00",
    "13:00",
    "14:00",
    "15:00",
]
