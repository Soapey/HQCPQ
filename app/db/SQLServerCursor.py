from tkinter import messagebox
from pypyodbc import connect, Cursor


DRIVER_NAME = "ODBC Driver 17 for SQL Server"
SERVER_NAME = "10.1.1.16,49172"
DATABASE_NAME = "HQCPQ"


connection_string = f"DRIVER={{{DRIVER_NAME}}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};trusted_connection=yes;"


class SQLServerCursor:
    def __init__(self) -> None:
        self.connection_string: str = None
        self.connection = None
        self.cursor: Cursor = None

    def __enter__(self):

        result: Cursor = None

        try:
            self.connection_string = connection_string
            self.connection = connect(self.connection_string)
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
