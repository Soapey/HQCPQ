from tkinter import messagebox
from sqlite3 import connect, Error, Cursor
from app.db.build_type_enum import BuildType


DEV_SQLITE_PATH = r"app\db\hqcpq.sqlite3"
PROD_SQLITE_PATH = r"app\db\hqcpq.sqlite3"


class SQLiteCursor:
    def __init__(self, build_type: BuildType) -> None:
        self.build_type: BuildType = build_type
        self.path = None
        self.connection = None
        self.cursor = None

    def __enter__(self):

        result: Cursor = None

        try:
            match self.build_type:
                case BuildType.DEVELOPMENT:
                    self.path = DEV_SQLITE_PATH
                case BuildType.PRODUCTION:
                    self.path = PROD_SQLITE_PATH

            self.connection = connect(self.path)
            self.cursor = self.connection.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON;")
            result = self.cursor
        except Error as e:
            messagebox.showerror(message=e)
        finally:
            return result

    def __exit__(self, exc_type, exc_value, exc_traceback):

        try:
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
        except Error as e:
            messagebox.showerror(message=e)
