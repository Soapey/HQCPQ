from tkinter import messagebox
from pypyodbc import connect, Cursor
from app.db.build_type_enum import BuildType


DRIVER_NAME = "ODBC Driver 17 for SQL Server"
SERVER_NAME = "10.1.1.16,49172"
DEV_DATABASE_NAME = "HQCPQ_Dev"
PROD_DATABASE_NAME = "HQCPQ"
USER_NAME = "hqcpquser"
PWD = "hqcpqpwd"


dev_connection_string = f"DRIVER={{{DRIVER_NAME}}};SERVER={SERVER_NAME};DATABASE={DEV_DATABASE_NAME};UID={USER_NAME};PWD={PWD};"
prod_connection_string = f"DRIVER={{{DRIVER_NAME}}};SERVER={SERVER_NAME};DATABASE={PROD_DATABASE_NAME};UID={USER_NAME};PWD={PWD};"


class SQLServerCursor:
    def __init__(self, build_type: BuildType) -> None:
        self.build_type: BuildType = build_type
        self.connection_string: str = None
        self.connection = None
        self.cursor: Cursor = None

    def __enter__(self):

        result: Cursor = None

        try:
            match self.build_type:
                case BuildType.DEVELOPMENT:
                    self.connection_string = dev_connection_string
                case BuildType.PRODUCTION:
                    self.connection_string = prod_connection_string

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
