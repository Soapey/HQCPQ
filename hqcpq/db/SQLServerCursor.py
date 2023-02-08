from tkinter import messagebox
from pypyodbc import connect, Cursor
from hqcpq.db.build_type_enum import BuildType
from hqcpq.helpers import read_config


def connection_string(build_type: BuildType) -> str:

    config = read_config()

    driver = config["SQLServerSettings"]["driver"]
    server = config["SQLServerSettings"]["server"]
    username = config["SQLServerSettings"]["username"]
    password = config["SQLServerSettings"]["password"]

    match build_type:
        case BuildType.DEVELOPMENT:
            return f"DRIVER={{{driver}}};SERVER={server};DATABASE={config['SQLServerSettings']['development_database_name']};UID={username};PWD={password};"

        case BuildType.PRODUCTION:
            return f"DRIVER={{{driver}}};SERVER={server};DATABASE={config['SQLServerSettings']['production_database_name']};UID={username};PWD={password};"

    return None


class SQLServerCursor:
    def __init__(self, build_type: BuildType) -> None:
        self.build_type: BuildType = build_type
        self.connection_string: str = None
        self.connection = None
        self.cursor: Cursor = None

    def __enter__(self):

        result: Cursor = None

        try:
            self.connection_string = connection_string(self.build_type)
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
