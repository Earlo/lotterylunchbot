import json
import os

import psycopg2
import psycopg2.extensions
import psycopg2.extras

from singleton import Singleton


class Logs(metaclass=Singleton):
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

    def add_entry(self, data: list):
        with self.con:
            with self.con.cursor() as cur:
                cur.execute(
                    f"""INSERT INTO lottery_log (pairs) VALUES (%s)""",
                    (json.dumps(data),),
                )

    def check_db(self):
        self.con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        with self.con:
            with self.con.cursor() as cur:
                # cur.execute("drop table if exists lottery_log;")
                cur.execute(
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
