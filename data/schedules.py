import os
from singleton import Singleton

import psycopg2
import psycopg2.extras


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
        return str(list(self.__iter__()))

    def add_schedule(
        self, user_id: int, pool_id: int, weekday: str, start_time: str, end_time: str
    ):
        with psycopg2.connect(os.environ["DATABASE_URL"]) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO schedules (account, pool, weekday, start_time, end_time) VALUES (%s, %s, %s, %s, %s)",
                    (user_id, pool_id, weekday, start_time, end_time),
                )

    def get_schedule(self, user_id: int) -> dict:
        with psycopg2.connect(os.environ["DATABASE_URL"]) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(
                    "SELECT weekday, start_time, end_time FROM schedules WHERE account = %s",
                    (user_id,),
                )
                values = cur.fetchall()
                schedule = {d: {"weekday": d, "available": False} for d in DAYS}
                for v in values:
                    schedule[v["weekday"]] = {
                        "weekday": v["weekday"],
                        "start_time": v["start_time"],
                        "end_time": v["end_time"],
                        "available": True,
                    }
                return schedule

    def check_db(self):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor() as cur:
                # cur.execute("drop table if exists schedules;")
                cur.execute(
                    """CREATE TABLE IF NOT EXISTS schedules (
                    id SERIAL PRIMARY KEY,
                    account INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
                    pool INTEGER REFERENCES pools(id) ON DELETE CASCADE,
                    weekday VARCHAR(8),
                    start_time TIME NOT NULL,
                    end_time TIME NOT NULL,
                    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                );"""
                )


SCHEDULES = Schedules()
DAYS = [
    "mon",
    "tue",
    "wed",
    "thu",
    "fri",
    "sat",
    "sun",
]
TIMES = [
    "11:00",
    "12:00",
    "13:00",
    "14:00",
]
