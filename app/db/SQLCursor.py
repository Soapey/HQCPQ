import sqlite3


TEST_SQLITE_PATH = r'app\db\hqcpq-test.sqlite3'
PRODUCTION_SQLITE_PATH = r'app\db\hqcpq.sqlite3'


builds = {
    'test': TEST_SQLITE_PATH,
    'production': PRODUCTION_SQLITE_PATH
}


build_name: str


class SQLCursor():

    def __init__(self) -> None:
        self.path = builds[build_name]
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()

        self.cursor.execute('PRAGMA foreign_keys = ON;')

        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()