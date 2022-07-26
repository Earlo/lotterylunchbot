from datetime import datetime
import os
from singleton import Singleton

import psycopg2
import psycopg2.extras


class Pools(metaclass=Singleton):
    def __init__(self):
        pass

    def __setitem__(self, i: int, data):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor() as cur:
                query = f"""INSERT INTO pools (
                    id,
                    name,
                    description,
                    public,
                    owner,
                    created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s) 
                    ON CONFLICT (id) DO UPDATE SET name = %s, description = %s, public = %s, owner = %s, updated_at = %s
                    """
                cur.execute(
                    query,
                    (
                        i,
                        data["name"],
                        data["description"],
                        data["public"],
                        data["owner"],
                        datetime.now(),
                        data["name"],
                        data["description"],
                        data["public"],
                        data["owner"],
                        datetime.now(),
                    ),
                )
                con.commit()

    def append(self, data):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor() as cur:
                query = f"""INSERT INTO pools (
                    name,
                    description,
                    public,
                    owner,
                    created_at
                    ) VALUES (%s, %s, %s, %s, %s) 
                    """
                cur.execute(
                    query,
                    (
                        data["name"],
                        data["description"],
                        data["public"],
                        data["owner"],
                        datetime.now(),
                    ),
                )
                con.commit()

    def __getitem__(self, i: int):
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

    def public_pools(self):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""SELECT * FROM pools WHERE public = TRUE;""")
                return cur.fetchall()

    def check_db(self):
        with psycopg2.connect(os.environ.get("DATABASE_URL")) as con:
            with con.cursor() as cur:
                # cur.execute("""drop table if exists pools;""")
                cur.execute(
                    """CREATE TABLE IF NOT EXISTS pools (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description VARCHAR(255),
                    public BOOLEAN NOT NULL DEFAULT FALSE,
                    owner INTEGER REFERENCES users(id),
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT unique_pool_id UNIQUE (id),
                    CONSTRAINT unique_pool_name UNIQUE (name)
                );"""
                )


POOLS = Pools()
