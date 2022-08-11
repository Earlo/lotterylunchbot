import json
import os

import psycopg
from psycopg.rows import dict_row

from singleton import Singleton


class Logs(metaclass=Singleton):
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

    def add_entry(self, data: list):
        self.con.execute(
            f"""INSERT INTO lottery_log (pairs) VALUES (%s)""",
            (json.dumps(data),),
        )

    def check_db(self):
        # self.con.execute("drop table if exists lottery_log;")
        self.con.execute(
            f"""CREATE TABLE IF NOT EXISTS lottery_log (
                id serial PRIMARY KEY,
                date timestamp without time zone NOT NULL DEFAULT now(),
                pairs json NOT NULL
            );"""
        )

    def close_connection(self):
        print("closing logs")
        self.con.commit()
        self.con.close()
        print("logs closed")


LOGS = Logs()
