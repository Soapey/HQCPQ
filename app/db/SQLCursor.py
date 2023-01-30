from tkinter import messagebox
from sqlite3 import connect, Error, Cursor


PRODUCTION_SQLITE_PATH = r"app\db\hqcpq.sqlite3"


class SQLCursor:
    def __init__(self) -> None:
        self.path = PRODUCTION_SQLITE_PATH
        self.connection = None
        self.cursor = None

    def __enter__(self):

        result: Cursor = None

        try:
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
