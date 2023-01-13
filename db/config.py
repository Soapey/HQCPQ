import sqlite3
from db.SQLCursor import SQLCursor


SQLITE_PATH = r'db\hqcpq.sqlite3'


def start():

    with SQLCursor(SQLITE_PATH) as cur:
        pass


if __name__ == '__main__':
    start()