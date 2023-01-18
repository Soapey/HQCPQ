import sqlite3
from db.config import builds
from app.core import build_name


class SQLCursor():

    def __init__(self) -> None:
        self.path = builds[build_name]
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()
        print('connection & cursor created.')
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        print('cursor & connection closed.')