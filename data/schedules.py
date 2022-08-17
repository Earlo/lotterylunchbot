import json
import os

import psycopg
from psycopg.rows import dict_row

from constants import DAYS, TIMES
from singleton import Singleton


class Schedules(metaclass=Singleton):
    def __init__(self):
        self.con = psycopg.connect(os.environ.get("DATABASE_URL"), autocommit=True)

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

    def update_schedule(
        self, account_id: int, calendar: list, pool_id: int | None = None
    ):
        date_table = json.dumps(calendar).replace("[", "{").replace("]", "}")
        ret = self.con.execute(
            f"""UPDATE schedules
            SET calendar = %s
            WHERE account = %s AND {pool_id is not None and f'pool = {pool_id}' or 'pool IS NULL'}""",
            (date_table, account_id),
        )
        print("ret", ret)

    def create_schedule(self, account_id: int, pool_id: int | None = None):
        with self.con.cursor() as cur:
            self.create_schedule_query(cur, account_id, pool_id)

    def create_schedule_query(
        self,
        cur: psycopg.cursor,
        account_id: int,
        pool_id: int | None = None,
    ):
        cur.execute(
            "INSERT INTO schedules (account, pool) VALUES (%s, %s) RETURNING *",
            (account_id, pool_id),
        )

    def get_schedule(self, account_id: int, pool_id: int | None = None) -> dict:
        with self.con.cursor(row_factory=dict_row) as cur:
            query = f"SELECT * FROM schedules WHERE account = {account_id} AND {pool_id is not None and f'pool = {pool_id}' or 'pool IS NULL'}"
            value = cur.execute(query).fetchone()
            if value is None:
                return self.create_schedule_query(cur, account_id, pool_id)
            return value

    def check_db(self):
        date_table = (
            json.dumps([[False for _ in range(len(TIMES))] for _ in range(len(DAYS))])
            .replace("[", "{")
            .replace("]", "}")
        )
        self.con.execute(
            f"""CREATE TABLE IF NOT EXISTS schedules (
            id SERIAL PRIMARY KEY,
            account INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
            pool INTEGER REFERENCES pools(id) ON DELETE CASCADE,
            calendar BOOLEAN[{len(DAYS)}][{len(TIMES)}] NOT NULL DEFAULT '{date_table}'::BOOLEAN[{len(DAYS)}][{len(TIMES)}],
            created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );"""
        )

    def close_connection(self):
        print("closing schedules")
        self.con.commit()
        self.con.close()
        print("schedules closed")


SCHEDULES = Schedules()
