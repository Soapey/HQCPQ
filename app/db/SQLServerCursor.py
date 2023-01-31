from tkinter import messagebox
from pypyodbc import connect, Cursor


DRIVER_NAME = "ODBC Driver 17 for SQL Server"
SERVER_NAME = "DESKTOP-A6HCEG9\SQLEXPRESS"
DATABASE_NAME = "HQCPQ"


connection_string = f"Driver={{{DRIVER_NAME}}};Server={SERVER_NAME};Database={DATABASE_NAME};Trusted_Connection=yes;"


class SQLServerCursor:
    def __init__(self) -> None:
        self.connection_string: str = None
        self.connection = None
        self.cursor: Cursor = None

    def __enter__(self):

        result: Cursor = None

        try:
            self.connection_string = connection_string
            self.connection = connect(connection_string)
            self.cursor = self.connection.cursor()
            result = self.cursor
        except Exception as e:
            messagebox.showerror(message=e)
        finally:
            return result

    def __exit__(self, exc_type, exc_value, exc_traceback):

        try:
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
        except Exception as e:
            messagebox.showerror(message=e)
